#!/usr/bin/env python3
"""Zeichnet eine Textkachel aus einem Bundle — ohne die App zu starten.

Damit laesst sich eine Aenderung am Kartenzeichner ANSEHEN, bevor sie
veroeffentlicht wird. Genau das hat lange gefehlt: Aenderungen wurden
durch Lesen geprueft, und dreimal war die Annahme falsch.

Vorbereitung, einmalig:

    npm install fabric@5.3.0 --prefix tools/.pruefen

Aufruf:

    python3 tools/kachel-pruefen.py site/assets/index-B5kartenNN.js
    python3 tools/kachel-pruefen.py <bundle> --fassung zitat
    python3 tools/kachel-pruefen.py <bundle> --paar B
    python3 tools/kachel-pruefen.py <bundle> --grund "#E7E2CE"

Das Skript legt unter tools/.pruefen/ eine Seite ab und sagt, wie sie
aufgerufen wird. Aufmachen im Browser oder als Bild abziehen:

    (cd tools/.pruefen && python3 -m http.server 8080)
    chromium --headless --window-size=1120,1480 \\
      --virtual-time-budget=9000 --screenshot=kachel.png \\
      http://localhost:8080/kachel.html

Die Leinwand liegt bei 10,10. Vorgabe 800x1000 mit Massstab 2 —
genau wie die Vorschau im Content Plan. Fuer den Export: --scale 2.7
--breite 1080 --hoehe 1350.
"""
import argparse, os, re, shutil, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)
AUS = os.path.join(HIER, ".pruefen")

SEITE = """<!doctype html><html><head><meta charset="utf-8">
<title>Kachel-Pruefung</title>
<script src="fabric.min.js"></script>
<style>
@font-face{font-family:HelveticaNeueBrand;src:url(fonts/HelveticaNeue-Thin.otf) format("opentype");font-weight:200}
@font-face{font-family:HelveticaNeueBrand;src:url(fonts/HelveticaNeue-Light.otf) format("opentype");font-weight:300}
@font-face{font-family:HelveticaNeueBrand;src:url(fonts/HelveticaNeue-Roman.otf) format("opentype");font-weight:400}
@font-face{font-family:HelveticaNeueBrand;src:url(fonts/HelveticaNeue-Medium.otf) format("opentype");font-weight:500}
@font-face{font-family:HelveticaNeueBrand;src:url(fonts/HelveticaNeue-Bold.otf) format("opentype");font-weight:700}
@font-face{font-family:"Playfair Display";src:url(fonts/PlayfairDisplay-Regular.ttf) format("truetype");font-weight:400}
@font-face{font-family:PoppinsBold;src:url(fonts/Poppins-Bold.ttf) format("truetype");font-weight:700}
@font-face{font-family:ArchivoBlack;src:url(fonts/ArchivoBlack.ttf) format("truetype");font-weight:400}
@font-face{font-family:Anton;src:url(fonts/Anton.ttf) format("truetype");font-weight:400}
@font-face{font-family:AspektaBrand;src:url(fonts/Aspekta-400.woff2) format("woff2");font-weight:400}
@font-face{font-family:AspektaBrand;src:url(fonts/Aspekta-600.woff2) format("woff2");font-weight:600}
@font-face{font-family:AspektaBrand;src:url(fonts/Aspekta-700.woff2) format("woff2");font-weight:700}
@font-face{font-family:Inter;src:url(fonts/Inter-400.woff2) format("woff2");font-weight:400}
@font-face{font-family:Inter;src:url(fonts/Inter-700.woff2) format("woff2");font-weight:700}
@font-face{font-family:Marcellus;src:url(fonts/Marcellus-Regular.woff2) format("woff2");font-weight:400}
@font-face{font-family:Prata;src:url(fonts/Prata-Regular.woff2) format("woff2");font-weight:400}
__KANDIDATEN__
body{margin:10px;background:#2a2a2a}
#lage{position:fixed;right:12px;top:12px;color:#ddd;font:13px monospace;white-space:pre-wrap;max-width:320px}
</style></head><body>
<canvas id="cv" width="__BREITE__" height="__HOEHE__"></canvas>
<div id="lage">laedt…</div>
<script>
__KONFIG__
(async () => {
  const melde = t => { document.getElementById('lage').textContent = t; window.ERG = t; };
  try {
    await Promise.all(['200 40px "HelveticaNeueBrand"','300 40px "HelveticaNeueBrand"','400 40px "HelveticaNeueBrand"','500 40px "HelveticaNeueBrand"','700 40px "HelveticaNeueBrand"',
      '400 40px "Playfair Display"','700 40px "PoppinsBold"','400 40px "ArchivoBlack"',
      '400 40px "Anton"','400 40px "AspektaBrand"','700 40px "AspektaBrand"','400 40px "Inter"','700 40px "Inter"','400 40px "Marcellus"', __MEHRLADEN__].map(f => document.fonts.load(f)));
    const Pe = { fabric: window.fabric };
    const e = new fabric.StaticCanvas('cv');
    const r = __BREITE__, n = __HOEHE__, d = __SCALE__, h = 0.8;
    const c = ge => ge * d * h;
    const wt = __ZEICHNER__;
    const Je = __JE__;
    e.backgroundColor = Je.grundFarbe;
    e.add(new fabric.Rect({left:0,top:0,width:r,height:n,fill:Je.grundFarbe,selectable:false}));
    const ok = wt(Je, __TEXT__);
    e.renderAll();
    melde(ok ? "gezeichnet" : "wt gab false zurueck — Fassung zeichnet diesen Text nicht");
  } catch (err) { melde("FEHLER: " + err.message + "\\n" + err.stack); }
})();
</script></body></html>"""

BEISPIEL = ("Alle denken, du schreibst kurz einen Post und stellst ihn online."
            "\n\nNiemand sieht die zwei Stunden, die du vorher am ersten Satz "
            "gesessen bist.")


def bloecke_holen(quelle, anfang):
    """Den Funktionskoerper ab 'anfang' per Klammerbalance ausschneiden."""
    p = quelle.find(anfang)
    if p < 0:
        raise SystemExit(f"ABBRUCH: '{anfang}' nicht im Bundle gefunden")
    start = quelle.find("{", p + len(anfang) - 1)
    tiefe = 0
    for k in range(start, len(quelle)):
        if quelle[k] == "{":
            tiefe += 1
        elif quelle[k] == "}":
            tiefe -= 1
            if tiefe == 0:
                return quelle[p:k + 1]
    raise SystemExit("ABBRUCH: Klammern gehen nicht auf")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--fassung", default="marke")
    ap.add_argument("--paar", default="A", help="Farbpaar A oder B aus BS_KACHEL")
    ap.add_argument("--wert", action="append", default=[],
                    metavar="NAME=WERT",
                    help="einen Wert aus BS_KACHEL ueberschreiben, mehrfach moeglich")
    ap.add_argument("--grund", default=None, help="Hintergrund, sonst aus dem Paar")
    ap.add_argument("--schrift", default=None, help="Schriftfarbe, sonst aus dem Paar")
    ap.add_argument("--text", default=BEISPIEL)
    ap.add_argument("--breite", type=int, default=800,
                    help="Leinwandbreite. 800 wie die Vorschau im Content Plan")
    ap.add_argument("--hoehe", type=int, default=1000)
    ap.add_argument("--scale", type=float, default=2.0,
                    help="Massstab. 2 in der Vorschau, 2.7 beim Export")
    a = ap.parse_args()

    s = open(a.bundle, encoding="utf-8", errors="replace").read()

    zeichner = bloecke_holen(s, "wt=(Je,rt)=>{")[len("wt="):]

    i = s.find("const BS_KACHEL=")
    if i < 0:
        raise SystemExit("ABBRUCH: BS_KACHEL fehlt im Bundle — falsche Fassung?")
    konfig = s[i:s.find("};", i) + 2]
    for paar_txt in a.wert:
        if "=" not in paar_txt:
            raise SystemExit("ABBRUCH: --wert braucht NAME=WERT, bekam " + paar_txt)
        name, wert = paar_txt.split("=", 1)
        muster = re.compile(r'\b%s:("[^"]*"|[^,}]+)' % re.escape(name))
        if not muster.search(konfig):
            raise SystemExit("ABBRUCH: %s steht nicht in BS_KACHEL" % name)
        ersatz = wert if wert[:1] in "0123456789.-" else '"%s"' % wert
        konfig = muster.sub(lambda m: name + ":" + ersatz, konfig, count=1)
    werte = dict(re.findall(r'(\w+):"([^"]*)"', konfig))

    paar = a.paar.upper()
    if paar not in ("A", "B"):
        raise SystemExit("ABBRUCH: --paar nimmt A oder B")
    grund = a.grund or werte.get("grund" + paar, "#EEEEEE")
    schrift = a.schrift or werte.get("schrift" + paar, "#111111")
    je = ('{fassung:%r,grundFarbe:%r,schriftGrund:%r,schriftFarbe:%r,'
          'monogrammFarbe:%r,absenderFarbe:%r,markenSchrift:"",rolle:"deckblatt"}'
          % (a.fassung, grund, grund, schrift, schrift, schrift)).replace("'", '"')

    os.makedirs(AUS, exist_ok=True)
    fabric = os.path.join(AUS, "node_modules", "fabric", "dist", "fabric.min.js")
    if not os.path.exists(fabric):
        raise SystemExit("ABBRUCH: fabric fehlt.\n"
                         "  npm install fabric@5.3.0 --prefix tools/.pruefen")
    shutil.copy(fabric, os.path.join(AUS, "fabric.min.js"))
    ziel_fonts = os.path.join(AUS, "fonts")
    if not os.path.isdir(ziel_fonts):
        shutil.copytree(os.path.join(WURZEL, "site", "fonts"), ziel_fonts)

    kand = "\n".join(
        '@font-face{font-family:"%s";src:url(fonts/%s.woff2) format("woff2");'
        'font-weight:100 900}' % (fam, datei)
        for fam, datei in (("Inter", "Inter-400"), ("DM Sans", "DMSans-400"),
                           ("Plus Jakarta Sans", "Jakarta-400"),
                           ("Figtree", "Figtree-400"),
                           ("Schibsted Grotesk", "Schibsted-400"),
                           ("Manrope", "Manrope-400"))
        if os.path.exists(os.path.join(AUS, "fonts", datei + ".woff2")))
    laden = ",".join("'%s 40px \"%s\"'" % (g, f)
                     for f in ("Inter", "DM Sans", "Plus Jakarta Sans", "Figtree",
                               "Schibsted Grotesk", "Manrope", "Marcellus", "Prata")
                     for g in ("400", "700"))
    seite = (SEITE.replace("__KANDIDATEN__", kand)
                  .replace("__MEHRLADEN__", laden)
                  .replace("__KONFIG__", konfig)
                  .replace("__ZEICHNER__", zeichner)
                  .replace("__JE__", je)
                  .replace("__TEXT__", repr(a.text).replace("'", '"'))
                  .replace("__BREITE__", str(a.breite))
                  .replace("__HOEHE__", str(a.hoehe))
                  .replace("__SCALE__", str(a.scale)))
    pfad = os.path.join(AUS, "kachel.html")
    open(pfad, "w", encoding="utf-8").write(seite)

    print(f"  Fassung   {a.fassung}")
    print(f"  Grund     {grund}")
    print(f"  Schrift   {schrift}")
    print(f"  Leinwand  {a.breite}x{a.hoehe}, Massstab {a.scale}")
    print(f"  Seite     {pfad}")
    print()
    print("  (cd tools/.pruefen && python3 -m http.server 8080)")
    print("  dann http://localhost:8080/kachel.html aufmachen")


main()
