#!/usr/bin/env python3
"""Traegt die Aenderungen nach, die nur im Bundle leben.

Aufruf:  python3 tools/bundle-patchen.py site/assets/index-B5kartenNN.js

Jeder Drop aus der Bau-Session setzt sie zurueck. Was hier steht, ist in
OFFENE-BUNDLE-AENDERUNGEN.md beschrieben. Jede Ersetzung muss GENAU einmal
passen — sonst bricht das Skript ab, statt stillschweigend danebenzugreifen.
"""
import sys, re

def tausche(s, alt, neu, was, anzahl=1):
    n = s.count(alt)
    if n != anzahl:
        raise SystemExit(f"ABBRUCH bei '{was}': Muster {n}x gefunden, erwartet {anzahl}x")
    return s.replace(alt, neu, anzahl if anzahl > 1 else 1), was

P = []

# 1 — Verlauf hinter Playfair auf Foto
P.append((
 'colorStops:[{offset:0,color:"rgba(18,16,14,0.34)"},{offset:.5,color:"rgba(18,16,14,0.16)"},{offset:1,color:"rgba(18,16,14,0.40)"}]',
 'colorStops:[{offset:0,color:"rgba(18,16,14,0.82)"},{offset:.5,color:"rgba(18,16,14,0.58)"},{offset:1,color:"rgba(18,16,14,0.90)"}]',
 "Verlauf 0.82/0.58/0.90", 1))

# 2 — Weichzeichner: ab Folie 2, etwa jedes zweite Bild, Keim aus der Bildadresse
P.append((
 'const dr=_&&(i.slideIndex||0)>0,Lt=dr?Math.max(t.blur||0,12):t.blur',
 'const dr=Qe>0&&(()=>{const zs=String(ge||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi++)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'return (zh+Qe*17)%100>=50})(),Lt=dr?Math.max(t.blur||0,12):t.blur',
 "Weichzeichner gestreut", 1))

# 3 — Farbfolien: rund ein Drittel ab Folie 2
P.append((
 'const qt={...pt},Vt=stJa&&typeof qt.background=="string"&&qt.background.length>5;',
 'const qt={...pt},Vt=stJa&&typeof qt.background=="string"&&qt.background.length>5'
 '&&(ct===0||ot.karte==="ablauf"||ot.reminderArt==="ablauf"'
 '||((zA,zB)=>{let zh=Math.imul(zA^2654435769,374761393)'
 '+Math.imul(zB^2246822519,668265263)|0;zh=Math.imul(zh^zh>>>13,1274126177);'
 'return((zh^zh>>>16)>>>0)%100})(De,ct)>=34);',
 "Farbfolien gestreut", 1))

# 4 — Ersatzwert der Bildanalyse: Mitte -> unten mittig
P.append((
 'quietZone:4,busyZone:4,quietLabel:"center",busyLabel:"center"',
 'quietZone:7,busyZone:4,quietLabel:"bottom-center",busyLabel:"center"',
 "Ersatzwert unten mittig", 1))

# 5 — Zone unter dem Gesicht mitmeiden
P.append((
 'let R=-1,q=0;for(let N=0;N<9;N++)j.has(N)||(R===-1||T[N]<T[R])&&(R=N);',
 'let R=-1,q=0;const jx=new Set(j);j.forEach(N=>{N+3<9&&jx.add(N+3)});'
 'const jw=jx.size<9?jx:j;'
 'for(let N=0;N<9;N++)jw.has(N)||(R===-1||T[N]<T[R])&&(R=N);',
 "Zone unter dem Gesicht", 1))

# 6 — Textspalte endet vor dem Gesicht
P.append((
 'const Qt=(tt.ausrichtung==="links"?r*.82:r*.86)-(tt.polsterX||0)*2,',
 'const zfz=(t._autoImage&&t._autoImage.faceZones)||[],'
 'zsp=zfz.length?Math.min.apply(null,zfz.map(zz=>zz%3)):-1,'
 'zbr=tt.ausrichtung==="links"?(zsp>0?Math.max(.42,Math.min(.82,zsp/3+.08)):.82):.86,'
 'Qt=r*zbr-(tt.polsterX||0)*2,',
 "Textbreite vor dem Gesicht", 1))

# 7 — Sternchen: kursiv, keine Farbe, nirgends gedruckt
P.append((
 'setSelectionStyles({fill:g,fontStyle:"italic",fontFamily:y}',
 'setSelectionStyles({fontStyle:"italic"}',
 "Auszeichnung kursiv statt farbig", 3))
P.append((
 '$V(e,c.replace(/\\*\\*/g,""),', '$V(e,c.replace(/\\*/g,""),',
 "Noir: einfache Sternchen entfernen", 1))
P.append((
 'const $=F.split(" "),z=S=>{try{return new e.Text(S,{fontSize:j.size,fontFamily:A.display}).width||0}',
 'const $=F.split(" "),z=S=>{try{return new e.Text(S,{fontSize:j.size,fontFamily:A.display,fontStyle:K.has(S)?"italic":"normal"}).width||0}',
 "Noir: Breite misst kursiv mit", 1))
P.append((
 'fontSize:j.size,fontFamily:A.display,fontWeight:"400",fill:K.has(S)?fl.accent:d,selectable:!1',
 'fontSize:j.size,fontFamily:A.display,fontWeight:"400",fontStyle:K.has(S)?"italic":"normal",fill:d,selectable:!1',
 "Noir: kursiv statt Akzentfarbe", 1))
P.append((
 't.add(new e.Text(h,{left:i/2,top:Q,originX:"center"',
 't.add(new e.Text(String(h).replace(/\\*/g,""),{left:i/2,top:Q,originX:"center"',
 "Noir: Kopfzeile entsternt", 1))
P.append((
 'f&&t.add(new e.Textbox(f,{left:i/2',
 'f&&t.add(new e.Textbox(String(f).replace(/\\*/g,""),{left:i/2',
 "Noir: Unterzeile entsternt", 1))
P.append((
 'const zl=ROH.split(/\\r?\\n/).map(x=>x.trim());',
 'const zl=ROH.replace(/\\*/g,"").split(/\\r?\\n/).map(x=>x.trim());',
 "Ablauf-Karte entsternt", 1))

# 8 — Randomizer raus, Startseite ist der Contentplan
P.append(('{path:"/brand-randomizer",icon:f3,label:"Randomizer"},', '',
 "Menuepunkt Randomizer", 1))
P.append(('{title:"1. Brand Randomizer",description:"Create or choose your Brand Style",'
 'icon:_1,color:"from-purple-500 to-pink-500",link:"/brand-randomizer",completed:t},', '',
 "Dashboard-Schrittkarte", 1))
P.append(('path:"/",element:v.jsx(kV,{})', 'path:"/",element:v.jsx(MG,{})',
 "Startseite = Contentplan", 1))
P.append(('to:"/brand-randomizer"', 'to:"/brand-settings"',
 "Randomizer-Verweise umgebogen", 2))

# 9 — Caption-Abfrage: Umbrueche und Zifferfilter waren doppelt
#     maskiert. Der Prompt zeigte \n als Text, und mit dem "s"
#     fuer Stories ging die Zahl verloren — es kam immer die
#     Standard-Fassung heraus.
P.append((
 'welche Fassung?\\\\n1 = Carina Original (Direct Call-Out)\\\\n2 = Lisa Bisschop (Soft Educational)\\\\n3 = US-Sales (kurz, Pitch)\\\\n4 = Preis-Pause\\\\n5 = Geboren zum Verkaufen\\\\n6 = Ehrlich\\\\n7 = Kurz und fies\\\\n8 = Launch\\\\n9 = Persönlichkeits-Lüge\\\\n10 = Alles schon probiert\\\\n\\\\nMit 5 Stories: s anhängen, z.B. 4s.',
 'welche Fassung?\\n1 = Carina Original (Direct Call-Out)\\n2 = Lisa Bisschop (Soft Educational)\\n3 = US-Sales (kurz, Pitch)\\n4 = Preis-Pause\\n5 = Geboren zum Verkaufen\\n6 = Ehrlich\\n7 = Kurz und fies\\n8 = Launch\\n9 = Persönlichkeits-Lüge\\n10 = Alles schon probiert\\n\\nMit 5 Stories: s anhängen, z.B. 4s.',
 "Caption-Abfrage lesbar", 2))
P.append((
 'Number(String(nr).replace(/\\\\D/g,""))||0',
 'Number(String(nr).replace(/\\D/g,""))||0',
 "Caption-Abfrage erkennt die Zahl", 2))

# 10 — Monogramm: der Ring steht links unten, die Buchstaben standen
#      in der Kartenmitte. Jetzt sitzen sie im Ring und werden
#      kleiner gerechnet, damit sie hineinpassen.
P.append((
 'const Vt=c(38),Tt=rt.slice(0,1),xt=rt.slice(1)||"",rr=Cr=>new Pe.fabric.Text(Cr,{fontSize:Vt,fontFamily:"Playfair Display"}).width,Ut=rr(Tt),Ir=xt?rr(xt):0,Hr=xt?Ir*.23:0,Br=Ut+Ir-Hr,Mt=r/2-Br/2;',
 'const zMx=r*.10+pt,Tt=rt.slice(0,1),xt=rt.slice(1)||"",rr=(Cr,gg)=>new Pe.fabric.Text(Cr,{fontSize:gg,fontFamily:"Playfair Display"}).width;let Vt=c(17),Ut=rr(Tt,Vt),Ir=xt?rr(xt,Vt):0,Hr=xt?Ir*.23:0,Br=Ut+Ir-Hr;/* in den Ring hinein passen, nicht darueber hinaus */const zBr=pt*1.5;if(Br>zBr&&Br>0){const zf=zBr/Br;Vt*=zf,Ut*=zf,Ir*=zf,Hr*=zf,Br=zBr}const Mt=zMx-Br/2;',
 "Monogramm zusammengefuehrt", 1))



# 14 — Der starke Tiefenverlauf gilt wieder nur fuer Playfair.
#      Er war fuer die duenne Serife gedacht. Seit die Fotoschrift
#      Anton ist, traf die Bedingung auf jedem zweiten Tag zu und
#      legte sich auf den ohnehin vorhandenen Kantenverlauf —
#      doppelt verdunkelt. Anton traegt auch ohne.
P.append(('if($e&&/Playfair|Anton/.test(String(Qe))&&t.tiefenOverlay!==!1)',
 'if($e&&/Playfair/.test(String(Qe))&&t.tiefenOverlay!==!1)',
 "Tiefenverlauf nur fuer Playfair", 1))

# 15 — Zurueck auf den Stand vor dem Gestaltungsdurchgang:
#      Schriften und Textplatzierung wie in karten70. Nur die Farben
#      aus karten72 bleiben.
P.append(('nS=()=>"anton"',
 'nS=()=>"playfair"',
 "Zurueck: Kachelschrift", 1))
P.append(('let A=passt(TT,c(LINKS?32:MITTE?(COVER?52:43):120),TITELSCHRIFT,MAXB,LINKS?6:MITTE?4:(titel.length>34?3:1));',
 'let A=passt(TT,c(LINKS?(COVER?65:52):MITTE?(COVER?52:43):120),TITELSCHRIFT,MAXB,LINKS?6:MITTE?4:(titel.length>34?3:1));',
 "Zurueck: LINKS-Groesse", 1))
P.append(('A.zeilen.length*A.groesse*1.24<=',
 'A.zeilen.length*A.groesse*1.06<=',
 "Zurueck: Umbruchpruefung", 1))
P.append(('A.groesse*(LINKS?1.24:1.10)',
 'A.groesse*(LINKS?1.06:1.10)',
 "Zurueck: Zeilenabstand", 3))
P.append(('let ty=MITTE?(LINKS?n*.11:Math.min(Math.max(n*.13,n*.47-gesamt/2),Math.max(n*.13,n*.84-gesamt)))+A.groesse*.55',
 'let ty=MITTE?Math.min(Math.max(n*.13,n*.47-gesamt/2),Math.max(n*.13,n*.84-gesamt))+A.groesse*.55',
 "Zurueck: Ansatz", 1))

# Nicht mehr ersetzen, nur noch nachsehen: Aenderungen, die die
# Bau-Session inzwischen selbst mitliefert. Verschwinden sie wieder,
# bricht das Skript ab, statt sie stillschweigend zu verlieren.
DA = [
 ("const bandH=bh/reihen", "Stationsreihe (kommt aus dem Drop)", 1),
]


def schild(s, pfad):
    """Das Versionsschild in der Kopfzeile auf den echten Dateinamen setzen.

    Die Bau-Session traegt dort den Namen ihres Drops ein. Nach dem Patchen
    heisst die Datei anders — dann zeigt das Schild eine Datei an, die gar
    nicht geladen ist, und man kann nicht mehr sehen, welcher Stand live ist.
    """
    import os
    name = os.path.basename(pfad)
    name = re.sub(r"^index-B5", "", name)
    name = re.sub(r"\.js$", "", name)
    s2, n = re.subn(r'children:"karten[0-9]+[a-z]*"', 'children:"%s"' % name, s)
    if n != 1:
        raise SystemExit(f"ABBRUCH beim Versionsschild: {n}x gefunden, erwartet 1x")
    return s2, name


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Aufruf: bundle-patchen.py <bundle.js>")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    for alt, neu, was, anz in P:
        s, name = tausche(s, alt, neu, was, anz)
        print(f"  OK  {name}")
    for muster, was, anzahl in DA:
        n = s.count(muster)
        if n != anzahl:
            raise SystemExit(f"ABBRUCH bei '{was}': {n}x gefunden, erwartet {anzahl}x")
        print(f"  DA  {was}")
    s, schildname = schild(s, p)
    print(f"  OK  Versionsschild zeigt {schildname}")
    if "brand-randomizer" in s:
        raise SystemExit("ABBRUCH: brand-randomizer noch im Bundle")
    open(p, "w", encoding="utf-8").write(s)
    print(f"\n{len(P)} Aenderungen eingetragen in {p}")

main()
