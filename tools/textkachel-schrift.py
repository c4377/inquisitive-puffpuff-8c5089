#!/usr/bin/env python3
"""Textkacheln bekommen die Schrift der Marke, nicht ArchivoBlack.

Aufruf: python3 tools/textkachel-schrift.py <alt.js> <neu.js>

Fehler: `plateFont` wird im Zusammenbau als `ct||Vt||He.plateFontFamily`
gesetzt. `Vt` kommt aus `vT(..., {hatFoto:!qt})`, und vT liefert ohne Foto
fest "ArchivoBlack". Fuer jede Textkachel stand darin also ArchivoBlack —
frueher egal, weil der Kartenzeichner Playfair fest verdrahtet hatte, seit
Version 73s aber nicht mehr. Ergebnis: fette Grotesk, die aus der Kachel
laeuft. Die Kacheln nehmen jetzt die Textkachel-Schrift aus der Marke.
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

SCHRITTE = [
  ('bodySchrift:He.bodyFontFamily||"Montserrat",',
   'bodySchrift:He.bodyFontFamily||"Montserrat",'
   'platteSchrift:He.plateFontFamily||He.fontFamily||"",',
   'Textkachel-Schrift der Marke wandert mit an den Zeichner', 1),
  ('Ye.markenSchrift=t.reminderArt==="ablauf"||t.karte==="ablauf"?"":t.plateFont||t.fontFamily,',
   'Ye.markenSchrift=t.reminderArt==="ablauf"||t.karte==="ablauf"?"":t.platteSchrift||"",',
   'Textkacheln nehmen die Marken-Schrift statt ArchivoBlack', 1),
]

DA = [
  ('"Caption Import"', 'Caption-Import unangetastet'),
  ('SCHRIFT-KOMBINATIONEN', 'Schrift-Kombinationen unangetastet'),
  ('iS=["montserrat"]', 'Fliesstext bleibt Standard'),
  ('qe=Math.round(qe*.70)', 'Schriftgroesse bleibt bei 70 Prozent'),
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
