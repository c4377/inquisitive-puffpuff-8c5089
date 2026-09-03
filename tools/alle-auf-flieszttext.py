#!/usr/bin/env python3
"""Fliesstext wird der Standard fuer alle Tage, und die Schrift wird kleiner.

Aufruf: python3 tools/alle-auf-flieszttext.py <alt.js> <neu.js>
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

SCHRITTE = [
  # 1 — Bisher war "Band oben" der Standard fuer jeden Tag ohne eigene Wahl.
  #     Jetzt ist es der Fliesstext-Stil; damit stellen sich alle vorhandenen
  #     Tage um, ohne dass am gespeicherten Plan etwas geaendert wird. Wer einen
  #     einzelnen Tag anders will, waehlt ihn im Tagesmenue weiterhin selbst.
  ('iS=["bandOben"]',
   'iS=["montserrat"]',
   'Fliesstext ist der Standard fuer alle Tage', 1),

  # 2 — Noch kleiner. 84 Prozent war Carina zu gross; das Vorbild liegt tiefer.
  ('qe=Math.round(qe*.84)',
   'qe=Math.round(qe*.70)',
   'Schrift von 84 auf 70 Prozent', 1),
]

DA = [
  ('"Caption Import"', 'Caption-Import unangetastet'),
  ('SCHRIFT-KOMBINATIONEN', 'Schrift-Kombinationen unangetastet'),
  ('Je.markenSchrift||"Playfair Display"', 'Textkacheln folgen der Marke'),
  ('["Band oben","bandOben"]', 'Band oben weiter waehlbar'),
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
