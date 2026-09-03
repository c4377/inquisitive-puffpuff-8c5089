#!/usr/bin/env python3
"""Die Schriftwahl aus den Einstellungen wirkt jetzt auch im Feed.

Aufruf: python3 tools/settings-wirken.py <alt.js> <neu.js>
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

SCHRITTE = [
  # 1 — Jede Fotokachel bekam bisher fest "anton" als Kachelschrift; damit hat
  #     T1 die Marken-Schrift ueberschrieben. "marke" heisst: die Marke entscheidet.
  ('nS=()=>"anton"',
   'nS=()=>"marke"',
   'Kachelschrift folgt der Marke statt fest Anton', 1),

  # 2 — Bei "marke" liefert co() null. Ohne den Notnagel "ArchivoBlack" bleibt
  #     schriftUeber leer, und die Schrift aus der Marke ueberlebt.
  ('polsterX:n*.45,schriftUeber:co(a)||"ArchivoBlack",randFarbe:null,randBreite:0,highlight:E1}',
   'polsterX:n*.45,schriftUeber:co(a),randFarbe:null,randBreite:0,highlight:E1}',
   'Stil "Band oben" ueberschreibt die Marken-Schrift nicht mehr', 1),

  # 3 — Auf der ersten Folie gewann bisher fotoSchriften (fest ["Anton"]) vor
  #     der Titelschrift aus den Einstellungen. Jetzt andersherum; fotoSchriften
  #     bleibt als Rueckfall, falls eine Marke keine Typografie hat.
  ('Tt=ct||(Ve===0?Vt||He.fontFamily:He.bodyFontFamily||"Montserrat")',
   'Tt=ct||(Ve===0?He.fontFamily||Vt:He.bodyFontFamily||"Montserrat")',
   'Titelschrift schlaegt fotoSchriften auf der ersten Folie', 1),

  # 4 — Der Kartenzeichner hatte Playfair fest verdrahtet. Die Ablauf-Folien
  #     behalten es (fester Bauplan), alle anderen Karten folgen der Marke.
  ('const SERIF="Playfair Display",FETT="PoppinsBold"',
   'const SERIF=Je.fassung!=="ablauf"&&Je.markenSchrift||"Playfair Display",FETT="PoppinsBold"',
   'Karten folgen der Marke, Ablauf behaelt Playfair', 1),
  ('Ab.aufFoto=!0,Ab.schriftFarbe="#FFFFFF",Ab.absenderFarbe="rgba(255,255,255,0.72)";',
   'Ab.aufFoto=!0,Ab.schriftFarbe="#FFFFFF",Ab.absenderFarbe="rgba(255,255,255,0.72)",'
   'Ab.markenSchrift=t.plateFont||t.fontFamily;',
   'Marken-Schrift an den Zeichner (Karte auf Foto)', 1),
  # 5 — Kuratierte Marken wurden beim Laden aus dem Code neu aufgebaut; von den
  #     eigenen Aenderungen ueberlebten nur Markenzeile und Logo. Die Schriftwahl
  #     war nach dem naechsten Neuladen also wieder weg.
  # 6 — Anton und Archivo Black waren bisher nur pro Tag erreichbar, nicht als
  #     Titelschrift der Marke. Ohne sie waere Schritt 1 eine Einbahnstrasse.
  ('{name:"Bodoni Moda",category:"Display Serif",',
   '{name:"Anton",category:"Display Sans",style:{fontFamily:"Anton, sans-serif",fontWeight:"400"},'
   'description:"Schmal, laut, Versalien — der bisherige Standard auf Fotos"},'
   '{name:"ArchivoBlack",category:"Display Sans",style:{fontFamily:"ArchivoBlack, sans-serif",fontWeight:"400"},'
   'description:"Sehr fett und breit"},'
   '{name:"Bodoni Moda",category:"Display Serif",',
   'Anton und Archivo Black in der Schriftliste', 1),

  ('n=["brandText","logo","logoUrl"]',
   'n=["brandText","logo","logoUrl","typography"]',
   'Eigene Schriftwahl ueberlebt das Neuladen', 1),

  ('e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Ye.grundFarbe,selectable:!1,evented:!1})),'
   'ht(Ye),Ye.fassung=Ye.fassung||"ablauf",wt(Ye,t.text)',
   'e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Ye.grundFarbe,selectable:!1,evented:!1})),'
   'ht(Ye),Ye.fassung=Ye.fassung||"ablauf",Ye.markenSchrift=t.plateFont||t.fontFamily,wt(Ye,t.text)',
   'Marken-Schrift an den Zeichner (Textkachel)', 1),
]

DA = [
  ('l==="montserrat"', 'Fotostil Montserrat unangetastet'),
  ('"Montserrat auf Foto"', 'Version Montserrat auf Foto unangetastet'),
  ('SCHRIFT-KOMBINATIONEN', 'Schrift-Kombinationen unangetastet'),
  ('"Caption Import"', 'Caption-Import unangetastet'),
]

fehler = False
for a, b, was, soll in SCHRITTE:
    ist = s.count(a)
    if ist != soll:
        print(f"ABBRUCH: {was}: {ist} Fundstellen statt {soll}")
        fehler = True
        continue
    s = s.replace(a, b)
    print(f"ok  {was} ({ist}x)")
if fehler:
    sys.exit("Nichts geschrieben.")

for stueck, was in DA:
    print(("da    " if stueck in s else "FEHLT ") + was)

schild = neu_pfad.stem.replace("index-B5", "")
treffer = re.findall(r'children:"karten[0-9a-z]+"', s)
if len(treffer) != 1:
    sys.exit(f"ABBRUCH: Versionsschild {len(treffer)}x gefunden, erwartet 1x")
s = s.replace(treffer[0], f'children:"{schild}"')
print(f'ok  Versionsschild {treffer[0]} -> {schild}')

neu_pfad.write_text(s, encoding="utf-8")
print(f"geschrieben: {neu_pfad} ({len(s)} Zeichen)")
