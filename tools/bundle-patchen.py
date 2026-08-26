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

# 9 — Stationsreihe: Beschriftung bleibt im Rahmen und bei ihrem Punkt
P.append((
 'const st=bildTeile,anz=st.length,reihen=anz>5?2:1,proReihe=Math.ceil(anz/reihen);\nfor(let ri=0;ri<reihen;ri++){\nconst von=ri*proReihe,bis=Math.min(anz,von+proReihe),k=bis-von;\nconst my=y+bh*(reihen===1?.42:(ri===0?.28:.72));\nlinie(L+MAXB*.06,my,L+MAXB*.94,my,{stroke:RAND,strokeWidth:Math.max(1,c(1.4))});\nfor(let ix=0;ix<k;ix++){\nconst px=k===1?L+MAXB*.5:L+MAXB*.10+(MAXB*.80)*(ix/(k-1));\ne.add(new Pe.fabric.Ellipse({left:px,top:my,originX:"center",originY:"center",rx:c(7),ry:c(7),\nfill:VOLL,stroke:RAND,strokeWidth:Math.max(1,c(1.2)),selectable:!1,evented:!1}));\nconst wort=st[von+ix];\n/* Aussen buendig statt mittig, sonst haengt die Beschriftung\n   ueber den Rahmen hinaus. */\nconst ersteZ=ix===0&&k>1,letzteZ=ix===k-1&&k>1;\ntxt(wort,{left:ersteZ?L+c(8):letzteZ?L+MAXB-c(8):px,top:my+c(24),\noriginX:ersteZ?"left":letzteZ?"right":"center",originY:"center",\nfontSize:c(11),fontFamily:GLATT,fill:SUB,maxB:MAXB/k*.92})}}}',
 'const st=bildTeile,anz=st.length,reihen=anz>5?2:1,proReihe=Math.ceil(anz/reihen);\n/* Jede Reihe bekommt ein eigenes Band. Punkt und Beschriftung liegen\n   darin, damit bei zwei Reihen nichts an den Rahmen stoesst. */\nconst bandH=bh/reihen,zg=c(13);\nfor(let ri=0;ri<reihen;ri++){\nconst von=ri*proReihe,bis=Math.min(anz,von+proReihe),k=bis-von;\nconst gp=Math.min(c(26),bandH*.40),my=y+bandH*ri+(bandH-gp)/2,ly=my+gp;\nconst pA=k===1?L+MAXB*.5:L+MAXB*.10,pE=k===1?L+MAXB*.5:L+MAXB*.90;\n/* Die Linie endet kurz hinter dem ersten und letzten Punkt, statt\n   quer durch den ganzen Rahmen zu laufen. */\nlinie(k===1?L+MAXB*.06:pA-c(14),my,k===1?L+MAXB*.94:pE+c(14),my,{stroke:RAND,strokeWidth:Math.max(1,c(1.4))});\nfor(let ix=0;ix<k;ix++){\nconst px=k===1?pA:pA+(pE-pA)*(ix/(k-1));\ne.add(new Pe.fabric.Ellipse({left:px,top:my,originX:"center",originY:"center",rx:c(7),ry:c(7),\nfill:VOLL,stroke:RAND,strokeWidth:Math.max(1,c(1.2)),selectable:!1,evented:!1}));\nconst wort=String(st[von+ix]);\n/* Mittig unter ihrem Punkt. Nur wer sonst ueber den Rahmen haengt,\n   rueckt so weit herein, wie noetig. */\nlet bw=0;try{bw=new Pe.fabric.Text(wort,{fontSize:zg,fontFamily:GLATT}).width||0}catch{}\nconst halb=Math.min(bw,MAXB/k*.92)/2;\nconst lx=Math.max(L+c(8)+halb,Math.min(L+MAXB-c(8)-halb,px));\ntxt(wort,{left:lx,top:ly,originX:"center",originY:"center",\nfontSize:zg,fontFamily:GLATT,fill:SUB,maxB:MAXB/k*.92})}}}',
 "Stationsreihe aufgeraeumt", 1))


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
    s, schildname = schild(s, p)
    print(f"  OK  Versionsschild zeigt {schildname}")
    if "brand-randomizer" in s:
        raise SystemExit("ABBRUCH: brand-randomizer noch im Bundle")
    open(p, "w", encoding="utf-8").write(s)
    print(f"\n{len(P)} Aenderungen eingetragen in {p}")

main()
