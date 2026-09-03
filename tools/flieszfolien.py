#!/usr/bin/env python3
"""Fotostil als Fliesstext: ruhige Sans aus der Marke, Abstaende wie im Beispiel.

Aufruf: python3 tools/flieszfolien.py <alt.js> <neu.js>
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

SCHRITTE = [
  # 1 — Die Schrift kommt jetzt aus der Marke (Body-Schrift), nicht mehr fest
  #     Montserrat. Damit laesst sich der ruhige Grotesk in den Einstellungen
  #     waehlen und gilt fuer alle Folien des Posts, auch die erste.
  ('schriftUeber:"Montserrat",staerkeUeber:"700"',
   'flieszSchrift:!0,engZeilen:!0,staerkeUeber:"700"',
   'Fotostil nimmt die Body-Schrift der Marke', 1),
  ('tt.schriftUeber&&(Qe=tt.schriftUeber);',
   'tt.schriftUeber&&(Qe=tt.schriftUeber),tt.flieszSchrift&&t.bodySchrift&&(Qe=t.bodySchrift);',
   'Body-Schrift schlaegt beim Fliesstext-Stil durch', 1),
  ('textStil:oS(ot.textStil)||(D1(ot.day)?sS(ot.day):oS(rt.textStil)||"platte"),',
   'textStil:oS(ot.textStil)||(D1(ot.day)?sS(ot.day):oS(rt.textStil)||"platte"),'
   'bodySchrift:He.bodyFontFamily||"Montserrat",',
   'Body-Schrift wandert mit an den Zeichner', 1),

  # 2 — Abstaende wie in Carinas Beispiel: enge Zeilen innerhalb eines Absatzes,
  #     dafuer eine ganze Leerzeile dazwischen. Vorher lag beides bei 1.3, der
  #     Absatz stand also genauso eng wie seine eigenen Zeilen.
  ('Et=qe*($e?1.3:1.06)',
   'Et=qe*(tt.engZeilen?1.17:$e?1.3:1.06)',
   'Zeilen im Absatz enger (1.17 statt 1.3)', 1),
  ('dr.forEach((Je,rt)=>{if(!Je.length){De+=Et;return}',
   'dr.forEach((Je,rt)=>{if(!Je.length){De+=tt.engZeilen?qe*.92:Et;return}',
   'Leerzeile zwischen Absaetzen bleibt eine volle Zeile', 1),
  ('ae=dr.length*Et+(Zt.length?Zt.length*ur+qe*.7:0)',
   'ae=dr.reduce((zs,zz)=>zs+(zz.length?Et:tt.engZeilen?qe*.92:Et),0)'
   '+(Zt.length?Zt.length*ur+qe*.7:0)',
   'Gesamthoehe zaehlt Leerzeilen richtig mit', 1),

  # 2b — Beim Aufteilen in Einstieg und Rest werden die Leerzeilen dazwischen
  #      weggeschnitten. Im Fliesstext-Stil steht deshalb immer eine Leerzeile
  #      zwischen dem fetten Einstieg und dem, was danach kommt.
  ('const dr=tt.nurErsteZeilePlatte?[...$t(_t(er),qe,!0),'
   '...pr?$t(_t(pr),qe,!tt.fettNurErste):[]]',
   'const dr=tt.nurErsteZeilePlatte?[...$t(_t(er),qe,!0),'
   '...tt.engZeilen&&pr?[[]]:[],...pr?$t(_t(pr),qe,!tt.fettNurErste):[]]',
   'Leerzeile zwischen fettem Einstieg und Fliesstext', 1),

  # 3 — Der Stil heisst nicht mehr nach einer Schrift, die er nicht mehr fest hat.
  ('{wert:"montserrat",label:"Montserrat auf Foto"}',
   '{wert:"montserrat",label:"Fließtext auf Foto"}',
   'Version heisst jetzt "Fließtext auf Foto"', 1),
  ('["Montserrat","montserrat"]',
   '["Fließtext","montserrat"]',
   'Textstil-Knopf heisst jetzt "Fließtext"', 1),

  # 4 — Carina will Prata mit einer ruhigeren Sans. Helvetica Neue liegt schon
  #     im Projekt (Thin bis Bold) und kommt dem Beispiel am naechsten.
  ('{kn:"Sanft",ku:"Prata · Marcellus",kt:{fontFamily:"Prata",plateFontFamily:"Prata",'
   'accentFontFamily:"Marcellus",bodyFontFamily:"Montserrat"}}',
   '{kn:"Sanft",ku:"Prata · Helvetica",kt:{fontFamily:"Prata",plateFontFamily:"Prata",'
   'accentFontFamily:"Italiana",bodyFontFamily:"HelveticaNeueBrand"}}',
   'Kombination "Sanft" ist jetzt Prata mit Helvetica Neue', 1),
]

DA = [
  ('"Caption Import"', 'Caption-Import unangetastet'),
  ('SCHRIFT-KOMBINATIONEN', 'Schrift-Kombinationen unangetastet'),
  ('Je.fassung!=="ablauf"&&Je.markenSchrift', 'Ablauf behaelt Playfair'),
  ('nS=()=>"marke"', 'Marken-Schrift wirkt weiter'),
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
