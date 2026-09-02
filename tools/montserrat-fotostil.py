#!/usr/bin/env python3
"""Fotostil "Montserrat auf Foto" + zwei Korrekturen.

Aufruf: python3 tools/montserrat-fotostil.py <alt.js> <neu.js>
Jede Ersetzung wird gezaehlt; stimmt die Anzahl nicht, wird nichts geschrieben.
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

STIL = (
 'if(t&&l==="montserrat")return{platten:!1,nurErsteZeilePlatte:!0,'
 'ohnePlatteErste:!0,fettNurErste:!0,rundung:0,ausrichtung:"links",'
 'schriftFarbe:"#FFFFFF",bandSchriftFarbe:"#FFFFFF",plattenFarbe:null,polsterX:0,'
 'schriftUeber:"Montserrat",staerkeUeber:"700",randFarbe:null,randBreite:0,'
 'highlight:wa,highlightFlaeche:null};'
)

SCHRITTE = [
  # 1 — der neue Stil im Stil-Aufloeser T1
  ('kachelSchrift:a="marke",karte:u="dunkel"}={})=>{',
   'kachelSchrift:a="marke",karte:u="dunkel"}={})=>{' + STIL,
   'Stil "montserrat" in T1', 1),

  # 2 — Der Rest hinter dem Eingangssatz wird mit 400 gemessen, nicht mit 700.
  ('pt=tt.nurErsteZeilePlatte&&pr?$t(_t(pr),qe,!0):[]',
   'pt=tt.nurErsteZeilePlatte&&pr?$t(_t(pr),qe,!tt.fettNurErste):[]',
   'Zeilenumbruch des Fliesstexts misst mit 400 (Schrumpfschleife)', 1),
  ('const dr=tt.nurErsteZeilePlatte?[...$t(_t(er),qe,!0),...pr?$t(_t(pr),qe,!0):[]]',
   'const dr=tt.nurErsteZeilePlatte?[...$t(_t(er),qe,!0),...pr?$t(_t(pr),qe,!tt.fettNurErste):[]]',
   'Zeilenumbruch des Fliesstexts misst mit 400 (Zeilenaufbau)', 1),

  # 3 — keine weisse Platte hinter dem Eingangssatz, wenn der Stil sie nicht will
  ('!ge&&(tt.platten||Ve)&&e.add(new Pe.fabric.Rect({',
   '!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste)&&e.add(new Pe.fabric.Rect({',
   'Platte hinter dem Eingangssatz abschaltbar', 1),

  # 4 — Fett nur auf dem Eingangssatz
  ('pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:qe,fontFamily:Qe,fontWeight:kt}),'
   'ct=sr(Je)?Ht(Je,qe,!0):pt.width',
   'pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:qe,fontFamily:Qe,'
   'fontWeight:tt.fettNurErste&&!Ve?"400":kt}),'
   'ct=sr(Je)?Ht(Je,qe,!(tt.fettNurErste&&!Ve)):pt.width',
   'Breitenmessung je Zeile mit der richtigen Staerke', 1),
  ('const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",'
   'fontSize:qe,fontFamily:Qe,fontWeight:kt,fontStyle:tt.kursiv||rr?"italic":"normal"',
   'const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",'
   'fontSize:qe,fontFamily:Qe,fontWeight:tt.fettNurErste&&!Ve?"400":kt,'
   'fontStyle:tt.kursiv||rr?"italic":"normal"',
   'Fett nur auf dem Eingangssatz (ganze Zeile)', 1),
  ('Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",'
   'fontSize:qe,fontFamily:Qe,fontWeight:kt,'
   'fontStyle:tt.kursiv||xt.kursiv&&!tt.highlight?"italic":"normal"',
   'Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",'
   'fontSize:qe,fontFamily:Qe,fontWeight:tt.fettNurErste&&!Ve?"400":kt,'
   'fontStyle:tt.kursiv||xt.kursiv&&!tt.highlight?"italic":"normal"',
   'Fett nur auf dem Eingangssatz (einzelne Woerter)', 1),

  # 5 — ohne Platte braucht auch der Eingangssatz seinen Schatten
  ('shadow:(ge||!tt.platten&&!Ve)&&!lt?me():void 0})',
   'shadow:(ge||!tt.platten&&(!Ve||tt.ohnePlatteErste))&&!lt?me():void 0})',
   'Schatten auch auf dem Eingangssatz ohne Platte', 1),

  # 6 — Auf der ersten, scharfen Folie richtet sich die Texthoehe nach der
  #     ruhigen Zone aus der Gesichtserkennung. Auf den verwischten Folgefolien
  #     bleibt es bei der normalen Lage.
  ('const ve=t.textLage||($e?"unten":"mitte")',
   'const ve=tt.fettNurErste&&!t._blurAn&&t.textAnchor&&t.textAnchor.row&&'
   '{top:"oben",mid:"mitte",bottom:"unten"}[t.textAnchor.row]'
   '||t.textLage||($e?"unten":"mitte")',
   'Erste Folie richtet sich nach der ruhigen Zone', 1),

  # 7 — Folie 1 scharf, alle weiteren verwischt (statt zufaellig etwa jede zweite)
  ('const dr=Qe>0&&(()=>{const zs=String(ge||"");',
   'const dr=Qe>0&&(t.textStil==="montserrat"||(()=>{const zs=String(ge||"");',
   'Verwischen: Stil montserrat immer ab Folie 2 (Anfang)', 1),
  ('return (zh+Qe*17)%100>=50})(),Lt=(t._blurAn=dr)?Math.max(t.blur||0,12):t.blur;',
   'return (zh+Qe*17)%100>=50})()),Lt=(t._blurAn=dr)?Math.max(t.blur||0,12):t.blur;',
   'Verwischen: Stil montserrat immer ab Folie 2 (Ende)', 1),

  # 8 — "Serif auf Foto" raus, "Montserrat auf Foto" rein
  ('{wert:"serif",label:"Serif auf Foto"},',
   '{wert:"montserrat",label:"Montserrat auf Foto"},',
   'Version "Serif auf Foto" ersetzt', 1),
  ('ae.karte==="ablauf"&&ae.reminderArt!=="ablauf"?"serif":ae.tileMode==="xpost"?"xpost"',
   'ae.textStil==="montserrat"?"montserrat":ae.tileMode==="xpost"?"xpost"',
   'Aktiver Knopf wird an textStil erkannt', 1),
  ('_e==="xpost"?De.tileMode="xpost":_e==="serif"?(De.tileMode="photo",De.karte="ablauf")'
   ':_e==="foto"&&(De.tileMode="photo"),De})',
   '_e==="xpost"?De.tileMode="xpost":(_e==="foto"||_e==="montserrat")&&(De.tileMode="photo"),'
   '_e==="montserrat"?De.textStil="montserrat"'
   ':De.textStil==="montserrat"&&(De.textStil=void 0),De})',
   'Version montserrat setzt Foto und Textstil', 1),
  ('_e==="foto"&&setTimeout(()=>{try{jr(ae,Rt(ve,We))}catch{}},0)',
   '(_e==="foto"||_e==="montserrat")&&setTimeout(()=>{try{jr(ae,Rt(ve,We))}catch{}},0)',
   'Version montserrat holt auch die Fotos', 1),
  ('[["Band oben","bandOben"],["Ausgestanzt","ausgestanzt"]]',
   '[["Band oben","bandOben"],["Ausgestanzt","ausgestanzt"],["Montserrat","montserrat"]]',
   'Montserrat auch in der Reihe TEXT-STIL', 1),

  # 9 — Beim Umstellen auf Foto behaelt jede Folie ihr Bild. Vorher fiel ueber
  #     ein Streuwerk etwa jede dritte Folie aus dem Foto heraus und wurde
  #     wieder als Textkachel gezeichnet.
  ('const qt={...pt},Vt=stJa&&typeof qt.background=="string"&&qt.background.length>5'
   '&&(ct===0||ot.karte==="ablauf"||ot.reminderArt==="ablauf"'
   '||((zA,zB)=>{let zh=Math.imul(zA^2654435769,374761393)+Math.imul(zB^2246822519,668265263)|0;'
   'zh=Math.imul(zh^zh>>>13,1274126177);return((zh^zh>>>16)>>>0)%100})(De,ct)>=34);',
   'const qt={...pt},Vt=stJa&&typeof qt.background=="string"&&qt.background.length>5;',
   'Kein Zufallsausfall mehr beim Umstellen auf Foto', 1),
]

DA = [
  ('"Bulk Content Import"', 'Bulk-Import unangetastet'),
  ('"Caption Import"', 'Caption-Import unangetastet'),
  ('Serif auf Foto', 'ACHTUNG: "Serif auf Foto" steht noch irgendwo'),
]

fehler = False
for altstueck, neustueck, was, soll in SCHRITTE:
    ist = s.count(altstueck)
    if ist != soll:
        print(f"ABBRUCH: {was}: {ist} Fundstellen statt {soll}")
        fehler = True
        continue
    s = s.replace(altstueck, neustueck)
    print(f"ok  {was} ({ist}x)")

if fehler:
    sys.exit("Nichts geschrieben.")

for stueck, was in DA:
    print(("da    " if stueck in s else "weg   ") + was)

schild = neu_pfad.stem.replace("index-B5", "")
treffer = re.findall(r'children:"karten[0-9a-z]+"', s)
if len(treffer) != 1:
    sys.exit(f"ABBRUCH: Versionsschild {len(treffer)}x gefunden, erwartet 1x")
s = s.replace(treffer[0], f'children:"{schild}"')
print(f'ok  Versionsschild {treffer[0]} -> {schild}')

neu_pfad.write_text(s, encoding="utf-8")
print(f"geschrieben: {neu_pfad} ({len(s)} Zeichen)")
