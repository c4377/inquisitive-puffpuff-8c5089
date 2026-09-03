#!/usr/bin/env python3
"""Elegante Serifen in die Schriftliste, plus Schrift-Kombinationen.

Aufruf: python3 tools/serifen-einbauen.py <alt.js> <neu.js>
"""
import sys, re, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")

NEUE_SCHRIFTEN = (
 '{name:"Bodoni Moda",category:"Display Serif",'
 'style:{fontFamily:"\'Bodoni Moda\', serif",fontWeight:"400"},'
 'description:"Hoher Kontrast, feine Haarlinien — am nächsten an Hatton und Atteron"},'
 '{name:"Prata",category:"Display Serif",'
 'style:{fontFamily:"Prata, serif",fontWeight:"400"},'
 'description:"Weicher und runder — die Richtung von Black Mango"},'
 '{name:"Italiana",category:"Display Serif",'
 'style:{fontFamily:"Italiana, serif",fontWeight:"400"},'
 'description:"Dünne, weite Versalien — der Ansam-Effekt, gut für Unterzeilen"},'
 '{name:"Marcellus",category:"Serif",'
 'style:{fontFamily:"Marcellus, serif",fontWeight:"400"},'
 'description:"Ruhige Antiqua, klassisch — angenehm im Fließtext"},'
)

KOMBIS = (
 'v.jsxs("div",{className:"mb-4 p-4 bg-gray-50 border border-gray-200 rounded-xl",children:['
 'v.jsx("p",{className:"text-[10px] font-bold text-gray-400 tracking-widest mb-1",'
 'children:"SCHRIFT-KOMBINATIONEN"}),'
 'v.jsx("p",{className:"text-xs text-gray-500 mb-3",'
 'children:"Ein Tipp setzt Titelschrift, Textkachel, Accent und Body zusammen. '
 'Die Signatur-Schrift bleibt, wie sie ist."}),'
 'v.jsx("div",{className:"flex flex-wrap gap-2",children:['
 '{kn:"Editorial",ku:"Bodoni Moda · Italiana",'
 'kt:{fontFamily:"Bodoni Moda",plateFontFamily:"Bodoni Moda",'
 'accentFontFamily:"Italiana",bodyFontFamily:"Montserrat"}},'
 '{kn:"Sanft",ku:"Prata · Marcellus",'
 'kt:{fontFamily:"Prata",plateFontFamily:"Prata",'
 'accentFontFamily:"Marcellus",bodyFontFamily:"Montserrat"}},'
 '{kn:"Weit",ku:"Italiana · Cormorant",'
 'kt:{fontFamily:"Italiana",plateFontFamily:"Cormorant Garamond",'
 'accentFontFamily:"Italiana",bodyFontFamily:"Montserrat"}},'
 '{kn:"Wie bisher",ku:"Petrona · Open Sans",'
 'kt:{fontFamily:"Petrona",plateFontFamily:"Petrona",'
 'accentFontFamily:"OpenSansBrand",bodyFontFamily:"OpenSansBrand"}}'
 '].map(kb=>{const ky=e.currentBrandConfig.typography||{},'
 'kz=ky.fontFamily===kb.kt.fontFamily&&ky.accentFontFamily===kb.kt.accentFontFamily;'
 'return v.jsxs("button",{onClick:()=>K("typography",{...ky,...kb.kt}),'
 'className:"px-3 py-2 rounded-lg border text-left transition-colors "+'
 '(kz?"bg-gray-900 text-white border-gray-900":'
 '"bg-white text-gray-700 border-gray-300 hover:border-gray-400"),children:['
 'v.jsx("span",{className:"block text-[12px] font-bold",children:kb.kn}),'
 'v.jsx("span",{className:"block text-[10px] opacity-70",children:kb.ku})'
 ']},kb.kn)})})]}),'
)

SCHRITTE = [
  ('{name:"Playfair Display",category:"Serif",style:{fontFamily:"Playfair Display, serif"},'
   'description:"Elegant & Classic"},',
   NEUE_SCHRIFTEN
   + '{name:"Playfair Display",category:"Serif",style:{fontFamily:"Playfair Display, serif"},'
     'description:"Elegant & Classic"},',
   'Vier Serifen in der Schriftliste', 1),

  ('{name:"Playfair Display",value:"Playfair Display"},',
   '{name:"Playfair Display",value:"Playfair Display"},'
   '{name:"Bodoni Moda",value:"Bodoni Moda"},{name:"Prata",value:"Prata"},'
   '{name:"Italiana",value:"Italiana"},{name:"Marcellus",value:"Marcellus"},',
   'Dieselben Schriften im Editor-Auswahlfeld', 1),

  ('children:"Typography"}),v.jsx(RK,{}),',
   'children:"Typography"}),v.jsx(RK,{}),' + KOMBIS,
   'Reihe mit den Schrift-Kombinationen', 1),
]

DA = [
  ('"Caption Import"', 'Caption-Import unangetastet'),
  ('l==="montserrat"', 'Fotostil Montserrat unangetastet'),
  ('"Montserrat auf Foto"', 'Version Montserrat auf Foto unangetastet'),
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
