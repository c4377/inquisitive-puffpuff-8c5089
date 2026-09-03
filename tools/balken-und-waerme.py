#!/usr/bin/env python3
"""Fliesstext-Stil: Balken statt Fettdruck, kleinere und waermere Schrift.
Textkacheln folgen der Marke, echte Ablauf-Folien behalten Playfair.

Aufruf: python3 tools/balken-und-waerme.py <alt.js> <neu.js>
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

WARM_SCHRIFT = "#F6F1E6"   # dasselbe warme Papierweiss, das die Karten schon nutzen
WARM_BALKEN  = "#F6F1E6"
BALKEN_TINTE = "#1A1614"

SCHRITTE = [
  # 1 — Der Einstieg steht auf einem Balken und ist nicht mehr fett; die Schrift
  #     ist waermer als Reinweiss. staerkeUeber 400 macht auch die erste Zeile normal.
  ('if(t&&l==="montserrat")return{platten:!1,nurErsteZeilePlatte:!0,ohnePlatteErste:!0,'
   'fettNurErste:!0,rundung:0,ausrichtung:"links",schriftFarbe:"#FFFFFF",'
   'bandSchriftFarbe:"#FFFFFF",plattenFarbe:null,polsterX:0,flieszSchrift:!0,engZeilen:!0,'
   'staerkeUeber:"700",randFarbe:null,randBreite:0,highlight:wa,highlightFlaeche:null}',
   'if(t&&l==="montserrat")return{platten:!1,nurErsteZeilePlatte:!0,'
   'fettNurErste:!0,rundung:0,ausrichtung:"links",schriftFarbe:"' + WARM_SCHRIFT + '",'
   'bandSchriftFarbe:"' + BALKEN_TINTE + '",plattenFarbe:"' + WARM_BALKEN + '",'
   'polsterX:n*.42,flieszSchrift:!0,engZeilen:!0,'
   'staerkeUeber:"400",randFarbe:null,randBreite:0,highlight:wa,highlightFlaeche:null}',
   'Balken statt Fettdruck, warmes Weiss statt Reinweiss', 1),

  # 2 — Im Beispiel steht der Text kleiner. Der Stil startet mit 84 Prozent;
  #     die Schrumpfschleife arbeitet danach von dieser Groesse aus weiter.
  ('const tt=T1({schrift:Qe,hatFoto:$e,',
   't.textStil==="montserrat"&&(qe=Math.round(qe*.84));const tt=T1({schrift:Qe,hatFoto:$e,',
   'Fliesstext startet mit kleinerer Schrift', 1),

  # 3 — Textkacheln ohne eigene Fassung sind bisher als "ablauf" durchgelaufen
  #     und haben darum Playfair behalten. Ob Playfair bleibt, entscheidet jetzt
  #     der Tag selbst: nur echte Ablauf-Folien behalten es.
  ('Je.fassung!=="ablauf"&&Je.markenSchrift||"Playfair Display"',
   'Je.markenSchrift||"Playfair Display"',
   'Playfair haengt nicht mehr an der Fassung', 1),
  ('Ye.fassung=Ye.fassung||"ablauf",Ye.markenSchrift=t.plateFont||t.fontFamily,',
   'Ye.fassung=Ye.fassung||"ablauf",'
   'Ye.markenSchrift=t.reminderArt==="ablauf"||t.karte==="ablauf"?"":t.plateFont||t.fontFamily,',
   'Textkacheln folgen der Marke, echte Ablauf-Tage nicht', 1),
  ('Ab.markenSchrift=t.plateFont||t.fontFamily;',
   'Ab.markenSchrift="";',
   'Ablauf auf Foto behaelt Playfair', 1),
]

DA = [
  ('"Caption Import"', 'Caption-Import unangetastet'),
  ('SCHRIFT-KOMBINATIONEN', 'Schrift-Kombinationen unangetastet'),
  ('nS=()=>"marke"', 'Marken-Schrift wirkt weiter'),
  ('Fließtext auf Foto', 'Version Fliesstext auf Foto'),
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
