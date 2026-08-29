#!/usr/bin/env python3
"""Baut den Caption-Import in das laufende Bundle ein.

Aufruf: python3 tools/caption-import-einbauen.py <alt.js> <neu.js>
Jede Ersetzung wird gezaehlt; stimmt die Anzahl nicht, bricht das
Skript ab und schreibt nichts.
"""
import sys, pathlib

alt_pfad, neu_pfad = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = alt_pfad.read_text(encoding="utf-8")
bauteil = pathlib.Path("tools/caption-import.js").read_text(encoding="utf-8").strip()

HANDLER = (
 '[capOffen,capSetzen]=ce.useState(!1),'
 'capEintragen=(cpLi,cpMo)=>{'
 'const cpKm=new Map(cpLi.map(x=>[Number(x.tag),x.caption]));let cpZ=0,cpG=0;'
 'const cpNp=(i||[]).map(x=>{const c=cpKm.get(Number(x.day));'
 'if(c===void 0)return x;'
 'if(cpMo==="leer"&&String(x.caption||"").trim())return cpG++,x;'
 'return cpZ++,{...x,caption:c}}),'
 'cpOhne=cpLi.map(x=>Number(x.tag)).filter(n=>!(i||[]).some(y=>Number(y.day)===n));'
 'capSetzen(!1),t({contentPlan:cpNp}),'
 'ue(cpZ+" Captions eingetragen"+(cpG?", "+cpG+" vorhandene gelassen":"")'
 '+(cpOhne.length?", ohne Tag "+cpOhne.join(", "):"")+", speichere …"),'
 'setTimeout(()=>ue("Gespeichert."),2600),setTimeout(()=>ue(""),6200)},'
)

MOUNT_ALT = 'abOffen&&v.jsx(AblaufMenue,{isOpen:!0,onClose:()=>abSetzen(!1),onAnlegen:abAnlegen}),'
KNOPF_ALT = ('v.jsxs("button",{onClick:async()=>{try{const cr=await fetch("/captions.json",{cache:"no-store"});'
 'if(!cr.ok)throw new Error("nicht gefunden");const cd=await cr.json();let cz=0;'
 'const cn=i.map(cx=>{const cq=cd[String(cx.day)];if(!cq||!cq.caption)return cx;cz++;return{...cx,caption:cq.caption}});'
 't({contentPlan:cn}),ue(cz+" Captions eingetragen, speichere …"),'
 'setTimeout(()=>ue("Gespeichert."),2600),setTimeout(()=>ue(""),5200)}'
 'catch{ue("Captions konnten nicht geladen werden.")}},')

SCHRITTE = [
  ('AblaufMenue=({isOpen:e,onClose:t,onAnlegen:r})=>{',
   bauteil + 'AblaufMenue=({isOpen:e,onClose:t,onAnlegen:r})=>{',
   'Dialog CaptionImport eingefuegt', 1),
  ('[abOffen,abSetzen]=ce.useState(!1),abAnlegen=',
   '[abOffen,abSetzen]=ce.useState(!1),' + HANDLER + 'abAnlegen=',
   'Zustand capOffen und Funktion capEintragen', 1),
  (MOUNT_ALT,
   MOUNT_ALT + 'capOffen&&v.jsx(CaptionImport,{isOpen:!0,onClose:()=>capSetzen(!1),onImport:capEintragen}),',
   'Dialog eingehaengt', 1),
  (KNOPF_ALT,
   'v.jsxs("button",{onClick:()=>capSetzen(!0),',
   'Captions-Knopf oeffnet jetzt den Import', 1),
  # Absturz im Bulk-Import: "existing" gibt es nicht. Gemeint ist der
  # bisherige Plan, der ein paar Zeilen darueber als "ut" bereitliegt.
  # Der Fehler flog erst nach t({contentPlan:st}), der Import lief also
  # durch — nur die Rueckmeldung ging verloren.
  ('const Ve=existing.length>0;',
   'const Ve=ut.length>0;',
   'Absturz im Bulk-Import behoben (existing -> ut)', 1),
]

DA = [
  ('"Bulk Content Import"', 'Bulk-Import unangetastet'),
  ('"Caption Import"', 'neuer Dialog vorhanden'),
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
    print(("ok  " if stueck in s else "FEHLT ") + was)

# Versionsschild auf den echten Dateinamen setzen
schild = neu_pfad.stem.replace("index-B5", "")
import re
treffer = re.findall(r'children:"karten[0-9a-z]+"', s)
if len(treffer) != 1:
    sys.exit(f"ABBRUCH: Versionsschild {len(treffer)}x gefunden, erwartet 1x")
s = s.replace(treffer[0], f'children:"{schild}"')
print(f'ok  Versionsschild {treffer[0]} -> {schild}')

neu_pfad.write_text(s, encoding="utf-8")
print(f"geschrieben: {neu_pfad} ({len(s)} Zeichen)")
