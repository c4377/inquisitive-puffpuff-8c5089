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
 'return (zh+Qe*17)%100>=50})(),Lt=(t._blurAn=dr)?Math.max(t.blur||0,12):t.blur',
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

# 6 — Textspalte endet vor dem Gesicht. Nicht auf weichgezeichneten
#     Folgefolien: dort ist kein Gesicht mehr zu erkennen, also
#     braucht der Text auch nicht auszuweichen.
P.append((
 'const Qt=(tt.ausrichtung==="links"?r*.82:r*.86)-(tt.polsterX||0)*2,',
 'const zfz=(!t._blurAn&&t._autoImage&&t._autoImage.faceZones)||[],'
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

# 15 — Ablauffolien: die Schlagzeile steht in Anton.
#      Der Zeichner nahm dort Playfair (SERIF) bzw. Helvetica
#      (GLATT). Groesse, Zeilenabstand und Ansatz bleiben so,
#      wie der Drop sie liefert — das ist die Fassung, die
#      Carina behalten will.
P.append(('const TITELSCHRIFT=FOLGE&&!LINKS?GLATT:SERIF;',
 'const TITELSCHRIFT=LINKS?SERIF:"Anton";',
 "Schlagzeile: Textkachel Playfair, alles andere Anton", 1))

# 16 — Fotoschrift ist Anton statt ArchivoBlack. Nur die Schrift —
#      die Versalien haengen ohnehin an beiden, und der starke
#      Tiefenverlauf bleibt auf Playfair beschraenkt (Patch 14),
#      sonst verdunkelt es doppelt.
P.append(('fotoSchriften:["ArchivoBlack"]', 'fotoSchriften:["Anton"]',
 "Fotoschrift Anton (Marke)", 1))
P.append((r'const i=e&&e.fotoSchriften||["ArchivoBlack"];return i[t%i.length]',
 r'const i=e&&e.fotoSchriften||["Anton"];return i[t%i.length]',
 "Fotoschrift Anton (Ersatzwert)", 1))

# 17 — Textkacheln zurueck auf karten70: Groesse, Zeilenabstand und
#      Ansatz. Die vier Werte haengen alle an LINKS, und LINKS ist
#      genau der Fall Textkachel — keine Kopfzeile, kein Foto.
#      Ablauffolien haben immer eine #Kopfzeile, fallen also in den
#      anderen Zweig und sind davon nicht betroffen. Mit dem
#      karten72-Wert stand der Text bei 11 Prozent, also oben im Eck.
P.append(('let A=passt(TT,c(LINKS?32:MITTE?(COVER?52:43):120),TITELSCHRIFT,MAXB,LINKS?6:MITTE?4:(titel.length>34?3:1));',
 'let A=passt(TT,c(LINKS?(COVER?65:52):MITTE?(COVER?52:43):120),TITELSCHRIFT,MAXB,LINKS?6:MITTE?4:(titel.length>34?3:1));',
 "Textkachel zurueck: LINKS-Groesse", 1))
P.append(('A.zeilen.length*A.groesse*1.24<=',
 'A.zeilen.length*A.groesse*1.06<=',
 "Textkachel zurueck: Umbruchpruefung", 1))
P.append(('A.groesse*(LINKS?1.24:1.10)',
 'A.groesse*(LINKS?1.06:1.10)',
 "Textkachel zurueck: Zeilenabstand", 3))
P.append(('let ty=MITTE?(LINKS?n*.11:Math.min(Math.max(n*.13,n*.47-gesamt/2),Math.max(n*.13,n*.84-gesamt)))+A.groesse*.55',
 'let ty=MITTE?Math.min(Math.max(n*.13,n*.47-gesamt/2),Math.max(n*.13,n*.84-gesamt))+A.groesse*.55',
 "Textkachel zurueck: Ansatz", 1))

# 18 — Auch die Textzone ignoriert das Gesicht, wenn weichgezeichnet.
#      Die Zone (oben, mitte, unten) kommt aus der Bildanalyse und
#      meidet dort das Gesicht. Auf einer weichgezeichneten Folie
#      faellt sie jetzt auf den Normalwert zurueck: unten mittig.
P.append(('const Oe=t.textAnchor&&typeof t.textAnchor=="object"?t.textAnchor:{row:$?"bottom":"mid",col:"center"}',
 'const Oe=!t._blurAn&&t.textAnchor&&typeof t.textAnchor=="object"?t.textAnchor:{row:$?"bottom":"mid",col:"center"}',
 "Textzone ohne Gesichtsruecksicht bei Weichzeichner", 1))

# 9 — Nur noch eine Abfrage: wofuer. Keine Fassungen mehr — die
#     Variante kommt aus dem Post selbst. Damit fallen Zz, Sr, Vc
#     und Kr weg, und die App schickt nur noch das Ziel.
P.append(('const Nr=Array.isArray(He.stories)?He.stories:[],De=i.map(Ze=>Ze.day===ae.day?{...Ze,caption:He.caption,stories:Nr}:Ze);t({contentPlan:De}),ue(`Caption für Tag ${ae.day}: Art ${Sr||"Standard"}, ${He.laenge} Zeichen${Nr.length?`, ${Nr.length} Stories`:""}.`)',
 'const De=i.map(Ze=>Ze.day===ae.day?{...Ze,caption:He.caption}:Ze);t({contentPlan:De}),ue(`Caption für Tag ${ae.day}: ${He.laenge} Zeichen.`)',
 "Meldung ohne Art und Stories", 1))
P.append(('const ss=Array.isArray(dd.stories)?dd.stories:[];R&&t({contentPlan:(e.contentPlan||[]).map(x=>x.day===R?{...x,caption:dd.caption,stories:ss}:x)})',
 'R&&t({contentPlan:(e.contentPlan||[]).map(x=>x.day===R?{...x,caption:dd.caption}:x)})',
 "Zweiter Weg speichert ohne Stories", 1))
P.append(('const nr=window.prompt(`Caption Tag ${ae.day} — welche Fassung?\\\\n1 = Carina Original (Direct Call-Out)\\\\n2 = Lisa Bisschop (Soft Educational)\\\\n3 = US-Sales (kurz, Pitch)\\\\n4 = Preis-Pause\\\\n5 = Geboren zum Verkaufen\\\\n6 = Ehrlich\\\\n7 = Kurz und fies\\\\n8 = Launch\\\\n9 = Persönlichkeits-Lüge\\\\n10 = Alles schon probiert\\\\n\\\\nMit 5 Stories: s anhängen, z.B. 4s.`,"1s");if(nr===null)return;const Zz=Number(String(nr).replace(/\\\\D/g,""))||0,Kr=/s/i.test(nr);const Sr=Zz>=1&&Zz<=3?Zz:0,Vc=Zz>=4&&Zz<=10?Zz-3:0;const zl=window.prompt(`Wofür? (leer = Money Room)\\\\n1 = Angebotsserie, die gerade läuft\\\\n2 = The Money Room\\\\n3 = Mentoring, das 1:1\\\\n4 = Das Intensive\\\\n5 = The Strategy`,"2");if(zl===null)return;const Zl=Number(String(zl).replace(/\\\\D/g,""))||2;',
 'const zl=window.prompt(`Welcher CTA?\\n1 = STRATEGY, 13 Voice Notes\\n2 = MOVE, The Money Room\\n3 = SPEICHERN\\n4 = 1:1, acht Plätze`,"2");if(zl===null)return;const Zl=Number(String(zl).replace(/\\D/g,""))||2;',
 "Nur noch die CTA-Abfrage (Caption Tag )", 1))
P.append(('const nr=window.prompt(`Caption — welche Fassung?\\\\n1 = Carina Original (Direct Call-Out)\\\\n2 = Lisa Bisschop (Soft Educational)\\\\n3 = US-Sales (kurz, Pitch)\\\\n4 = Preis-Pause\\\\n5 = Geboren zum Verkaufen\\\\n6 = Ehrlich\\\\n7 = Kurz und fies\\\\n8 = Launch\\\\n9 = Persönlichkeits-Lüge\\\\n10 = Alles schon probiert\\\\n\\\\nMit 5 Stories: s anhängen, z.B. 4s.`,"1s");if(nr===null)return;const Zz=Number(String(nr).replace(/\\\\D/g,""))||0,Kr=/s/i.test(nr);const Sr=Zz>=1&&Zz<=3?Zz:0,Vc=Zz>=4&&Zz<=10?Zz-3:0;const zl=window.prompt(`Wofür? (leer = Money Room)\\\\n1 = Angebotsserie, die gerade läuft\\\\n2 = The Money Room\\\\n3 = Mentoring, das 1:1\\\\n4 = Das Intensive\\\\n5 = The Strategy`,"2");if(zl===null)return;const Zl=Number(String(zl).replace(/\\\\D/g,""))||2;',
 'const zl=window.prompt(`Welcher CTA?\\n1 = STRATEGY, 13 Voice Notes\\n2 = MOVE, The Money Room\\n3 = SPEICHERN\\n4 = 1:1, acht Plätze`,"2");if(zl===null)return;const Zl=Number(String(zl).replace(/\\D/g,""))||2;',
 "Nur noch die CTA-Abfrage (Caption — we)", 1))
P.append(('art:Sr,voice:Vc,ziel:Zl,stories:Kr,', 'cta:Zl,',
 "App schickt nur noch den CTA", 2))

# 12 — Knopf "Captions": laedt site/captions.json und traegt die
#      Texte bei den passenden Tagen ein. Tage ohne Eintrag bleiben
#      unberuehrt.
#      Gespeichert wird ueber denselben Weg wie der Speichern-Knopf:
#      t({contentPlan}) loest den Effekt aus, der den Plan in die
#      Browser-Datenbank schreibt und, bei angemeldetem Konto, nach
#      zwei Sekunden in die Cloud. Die Meldung wartet das ab.
P.append(('v.jsxs("button",{onClick:()=>quSetzen(!0),',
 'v.jsxs("button",{onClick:async()=>{try{const cr=await fetch("/captions.json",{cache:"no-store"});if(!cr.ok)throw new Error("nicht gefunden");const cd=await cr.json();let cz=0;const cn=i.map(cx=>{const cq=cd[String(cx.day)];if(!cq||!cq.caption)return cx;cz++;return{...cx,caption:cq.caption}});t({contentPlan:cn}),ue(cz+" Captions eingetragen, speichere …"),setTimeout(()=>ue("Gespeichert."),2600),setTimeout(()=>ue(""),5200)}catch{ue("Captions konnten nicht geladen werden.")}},className:"px-2.5 py-1.5 bg-white text-purple-700 border border-purple-200 rounded-lg font-bold hover:bg-purple-50 transition-colors flex items-center whitespace-nowrap text-[11px]",children:[v.jsx(ke,{icon:AS,className:"mr-2"}),"Captions"]}),v.jsxs("button",{onClick:()=>quSetzen(!0),',
 "Knopf Captions", 1))

# (Block 19 ist entfallen: die Kachelfarben stehen jetzt im
#  Konfigurationsblock BS_KACHEL, siehe Eintrag 24.)

# 20 — Textkacheln laufen in der Marken-Grotesk statt in Playfair.
#      ACHTUNG, das hebt die Absicht aus Patch 15 teilweise auf:
#      dort stand "Textkachel Playfair" als gewollte Fassung. Carina
#      hat das am 3. September ausdruecklich umentschieden.
#      Der Zeichner setzt den Fliesstext ueber
#      FLIESSCHRIFT = LINKS ? SERIF : GLATT und die Schlagzeile ueber
#      TITELSCHRIFT = LINKS ? SERIF : "Anton". LINKS ist bei jeder
#      Kachel ohne #Kopfzeile wahr, also hing beides an SERIF.
#      Eine gesetzte Marken-Schrift (Je.markenSchrift) sticht das
#      weiterhin — nur der Ersatzwert wechselt.
P.append(('const SERIF=Je.markenSchrift||"Playfair Display"',
 'const SERIF=Je.markenSchrift||"HelveticaNeueBrand"',
 "Textkachel-Schrift: Grotesk statt Playfair", 1))

# 21 — Zwei tote Fassungen aus der Farbtafel. notiz und merken
#      stehen dort, aber keine Regel waehlt sie je aus: die
#      Laengenregel liefert nur wieder/linie/zettel/zitat, die
#      Reminder liefern aussage/zitat/zwei, zwei Knoepfe setzen
#      ablauf und hand, alles andere kommt aus aS(day-1).
P.append(('notiz:{grund:IV,schriftGrund:"#FFFFFF",schrift:hA,betont:hA,monogramm:lg,absender:"rgba(20,18,16,0.70)",fassung:"notiz",schriftart:"HelveticaNeueBrand"},',
 '', "tote Fassung notiz raus", 1))
P.append(('merken:{grund:IV,schriftGrund:uA,schrift:hA,betont:hA,monogramm:lg,absender:"rgba(20,18,16,0.70)",fassung:"merken",schriftart:"PoppinsBold"},',
 '', "tote Fassung merken raus", 1))

# 22 — Der Kartenpfad in T1 setzt zentriert und Grotesk. Wirkt nur,
#      wenn der Zeichner aussteigt (er tut das zum Beispiel, wenn
#      die Fassung "wieder" fuer den Text zu gross ausfaellt).
#      Sonst zeichnet wt und rechnet seine Ausrichtung selbst.
#      Steht hier, damit beide Wege dasselbe Bild ergeben.
P.append(('istKarte:!0,grundFarbe:h.grund,rundung:0,ausrichtung:"links",schriftFarbe:h.schrift,plattenFarbe:null,polsterX:0,schriftUeber:"Playfair Display",staerkeUeber:"400"',
 'istKarte:!0,grundFarbe:h.grund,rundung:0,ausrichtung:"mitte",schriftFarbe:h.schrift,plattenFarbe:null,polsterX:0,schriftUeber:"HelveticaNeueBrand",staerkeUeber:"400"',
 "Kartenpfad zentriert und Grotesk", 1))

# 23 — Erste Slide eines Fotoposts: Serife und deutlich groesser.
#      Vorher lief sie wie alle Folgeslides in Anton auf PV=34.
#      Im Vorbild traegt das Deckblatt eine Serife und ist klar
#      groesser als der Rest — daran soll es sich halten.
#
#      Schrift: kachelSchrift wird im Zusammenbau gesetzt und landet
#      ueber co(a) in schriftUeber. Das wird spaet angewandt
#      (tt.schriftUeber && (Qe = tt.schriftUeber)) und sticht die
#      Fotoschrift aus vT/fotoSchriften. "marke" liefert bewusst
#      keine Schrift, "playfair" liefert "Playfair Display".
#      Betrifft nur die Rolle deckblatt, nicht die Rolle foto.
#
#      Groesse: PV ist der Grundwert fuer Folien mit Foto (34).
#      Auf dem Deckblatt 46. sizeLocked sticht weiterhin — eine von
#      Hand gesetzte Groesse bleibt unangetastet.
P.append(('let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?PV:OV);',
 'let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?(t.folienRolle==="deckblatt"?BS_KACHEL.deckblattGroesse:(BS_KACHEL.fotoGroesse||PV)):OV);',
 "Deckblatt groesser (aus BS_KACHEL)", 1))

# 24 — EINE STELLE FUER DAS AUSSEHEN DER TEXTKACHELN.
#
#      Wer Farbe, Schrift, Groesse oder Abstaende aendern will, aendert
#      NUR diesen Block. Er steht ganz oben im Bundle, alle Stellen
#      unten lesen daraus. Kein Suchen mehr im minifizierten Code.
#
#        grundA / schriftA Farbpaar der einen Kachel
#        grundB / schriftB Farbpaar der anderen Kachel
#                          Grund und Schrift gehoeren zusammen und
#                          werden zusammen geaendert. Wer nur einen
#                          Grund tauscht, bekommt Text, den man nicht
#                          mehr liest.
#        schriftart        Schrift der Textkacheln
#        groesse           Ausgangsgroesse, schrumpft bis es passt
#        zeile             Zeilenabstand
#        absatz            Abstand zwischen den zwei Absaetzen
#        rand              Seitenrand als Anteil der Breite
#        mitte             Hoehe der Textmitte als Anteil
#        maxhoehe          hoechstens so viel Hoehe darf der Text
#        deckblattSchrift  Schrift der ersten Fotoslide
#        deckblattGroesse  Groesse der ersten Fotoslide
KONFIG = 'const BS_KACHEL={grundA:"#F6F2EB",schriftA:"#241C16",grundB:"#4A3B30",schriftB:"#FFFFFF",schriftart:"HelveticaNeueBrand",unterSchrift:"HelveticaNeueBrand",unterVerhaeltnis:1,gewicht:"300",leichtGewicht:"300",unterGewicht:"700",groesseAnteil:.098,enge:1,laufweite:-50,zeile:1.02,absatz:.55,rand:.0885,mitte:.575,maxhoehe:.90,name:"carinaannaprav",nameAnteil:.018,nameAbstand:1.9,fotoSchrift:"Fraunces",deckblattFamilie:"Fraunces",deckblattGewicht:"700",deckblattGroesse:68,spalteMin:.82,textHoehe:.70,textHoeheZaehler:.50,textUnten:.86,nameUnten:.945,umbruchRand:12,fotoZeile:0.98,folgeStil:"montserrat",folgeFamilie:"HelveticaNeueBrand",zweiteFamilie:"HelveticaNeueBrand",zweitAnteil:.75,teilungAb:52,bandAuf:0,folgeGewicht:"700",weichAnteil:0,lagenWechsel:1,fotoGroesse:44,schildGrund:"#A57F55",schildSchriftFarbe:"#FFFFFF",schildSchrift:"HelveticaNeueBrand",schildGewicht:"400",schildGroesse:.030,schildLaufweite:6,schildPolster:.9,schildHoehe:2.0,schildAbstand:.034,schildRundung:.004,schildNeigung:-3,bildKante:1350,bildGuete:.85,bildKontrast:0,bildHelligkeit:0,ablaufTitel:"HelveticaNeueBrand",ablaufTitelGewicht:"700",ablaufTiefeOben:.30,ablaufTiefeMitte:.22,ablaufTiefeUnten:.42,bildTon:"74,58,44",waermeTon:"150,112,76",waerme:.07,tiefeOben:.05,tiefeMitte:.10,tiefeUnten:.42,tiefeSchriften:"Fraunces|Playfair|Marcellus|Prata|Italiana|Cormorant|Bodoni|Inter|Aspekta|Helvetica"};'
P.append(('function t6(e,t){', KONFIG + 'function t6(e,t){',
 "Konfigurationsblock BS_KACHEL ganz oben", 1))

# 25 — Die Alltagskacheln bekommen eine eigene Fassung "marke" und
#      lesen ihre Farben aus dem Block. Vorher hatten stein und hell
#      als einzige kein Feld fassung, wurden deshalb als Ablauf-Fassung
#      gezeichnet und kamen linksbuendig mit winzigem Fliesstext heraus.
P.append(('stein:{grund:SF,schriftGrund:SF,schrift:"#FFFFFF",betont:"#FFFFFF",monogramm:"#FFFFFF",absender:"rgba(255,255,255,0.60)",schriftart:"Playfair Display"}',
 'stein:{grund:BS_KACHEL.grundB,schriftGrund:BS_KACHEL.grundB,schrift:BS_KACHEL.schriftB,betont:BS_KACHEL.schriftB,absender:BS_KACHEL.schriftB,fassung:"marke",schriftart:BS_KACHEL.schriftart}',
 "stein: Fassung marke, Farben aus dem Block", 1))
P.append(('hell:{grund:OW,schriftGrund:OW,schrift:OD,betont:OD,monogramm:OD,absender:"rgba(35,40,44,0.55)",schriftart:"Playfair Display"}',
 'hell:{grund:BS_KACHEL.grundA,schriftGrund:BS_KACHEL.grundA,schrift:BS_KACHEL.schriftA,betont:BS_KACHEL.schriftA,absender:BS_KACHEL.schriftA,fassung:"marke",schriftart:BS_KACHEL.schriftart}',
 "hell: Fassung marke, Farben aus dem Block", 1))
P.append(('linie:{grund:uA,schrift:hA,betont:hA,monogramm:F1,absender:"rgba(62,80,99,0.55)",fassung:"linie",schriftart:"PoppinsBold"}',
 'linie:{grund:BS_KACHEL.grundA,schriftGrund:BS_KACHEL.grundA,schrift:BS_KACHEL.schriftA,betont:BS_KACHEL.schriftA,absender:BS_KACHEL.schriftA,fassung:"marke",schriftart:BS_KACHEL.schriftart}',
 "linie: Fassung marke", 1))
P.append(('wieder:{grund:uA,schrift:hA,betont:hA,monogramm:F1,absender:"rgba(62,80,99,0.55)",fassung:"wieder",schriftart:"PoppinsBold"}',
 'wieder:{grund:BS_KACHEL.grundB,schriftGrund:BS_KACHEL.grundB,schrift:BS_KACHEL.schriftB,betont:BS_KACHEL.schriftB,absender:BS_KACHEL.schriftB,fassung:"marke",schriftart:BS_KACHEL.schriftart}',
 "wieder: Fassung marke", 1))

# 26 — Keine Wortmarke auf der Fassung marke. Im Vorbild steht unten
#      nichts; der Schriftzug bleibt fuer alle anderen Fassungen.
P.append(('Je.aufFoto!==!0&&txt("carinaannaprav"',
 'Je.aufFoto!==!0&&Je.fassung!=="marke"&&txt("carinaannaprav"',
 "Wortmarke nicht auf der Fassung marke", 1))

# 27 — Der Zeichner fuer die Fassung marke. Zentriert, zwei Absaetze,
#      der zweite fett als Pointe, Groesse schrumpft bis es passt.
#      Genau das Bild aus dem Vorbild, alle Werte aus BS_KACHEL.
ZWEIG = '\nif(FA==="marke"){\nconst K=BS_KACHEL;\nconst MAXB=r*(1-2*K.rand);\nconst LW=K.laufweite||0,MESS=MAXB/(1+LW/500);\nconst B0=ROH.replace(/\\*/g,"").split(/\\n\\s*\\n/).map(x=>x.trim()).filter(Boolean);\nconst BL=B0.length>1?B0:(()=>{const t2=teile(B0[0]||"");return t2[1]?[t2[0],t2[1]]:[B0[0]||""]})();\nif(!BL.length||!BL[0])return!1;\nconst NA=String(K.name||""),NG=r*(K.nameAnteil||.018);\nconst FAM=ix=>ix===0?K.schriftart:(K.unterSchrift||K.schriftart);\nconst GRO=(ix,g)=>ix===0?g:g*(K.unterVerhaeltnis||.64);\nconst GEW=ix=>ix===0?(K.gewicht||"700"):(K.unterGewicht||"400");\nlet gr=r*(K.groesseAnteil||.098),ZL=[];\nconst hoeheVon=g=>{const z=BL.map((b,ix)=>umbruch(b,GRO(ix,g),FAM(ix),MESS,GEW(ix)));\nconst hh=z.reduce((x,q,ix)=>x+q.length*GRO(ix,g)*K.zeile,0)\n+(BL.length-1)*g*K.absatz+(NA?g*K.nameAbstand:0);\nreturn{z:z,h:hh}};\nconst breiteste=(z,g)=>z.reduce((mx,q,ix)=>q.reduce((m2,zl)=>Math.max(m2,breit(zl,GRO(ix,g),FAM(ix),GEW(ix))),mx),0);\nfor(let i=0;i<60;i+=1){const m=hoeheVon(gr);ZL=m.z;if(m.h<=n*K.maxhoehe&&breiteste(m.z,gr)<=MESS)break;gr*=.95}\nconst M=hoeheVon(gr);ZL=M.z;\nlet y=n*K.mitte-M.h/2+GRO(0,gr)*.5;\nZL.forEach((blk,ix)=>{const g2=GRO(ix,gr);\nblk.forEach(z=>{txt(z,{left:r/2,top:y,originX:"center",originY:"center",\nfontSize:g2,fontFamily:FAM(ix),fontWeight:GEW(ix),fill:SCH,\ncharSpacing:LW,maxB:MESS});\ny+=g2*K.zeile});\nif(ix<ZL.length-1)y+=gr*K.absatz});\nif(NA)txt(NA,{left:r/2,top:y-gr*K.zeile+gr*K.nameAbstand,originX:"center",originY:"center",\nfontSize:NG,fontFamily:K.unterSchrift||K.schriftart,fontWeight:"500",charSpacing:150,\nfill:SCH,opacity:.5,maxB:MAXB});\nreturn!0}\n'
P.append((chr(10) + 'if(FA==="ablauf"){', ZWEIG + chr(10) + 'if(FA==="ablauf"){',
 "Zeichner-Zweig fuer die Fassung marke", 1))

# 28 — Fotokacheln in der Serife aus dem Vorbild statt in Anton.
#      Eintrag 16 setzt Anton; das kommt schon aus dem Drop und wird
#      hier nicht mehr ausgefuehrt. Deshalb ein eigener Eintrag, der
#      den fertigen Wert nochmal austauscht.
#
#      Achtung, Wechselwirkung mit Eintrag 14: der starke Tiefenverlauf
#      gilt nur fuer Playfair. Mit Anton als Fotoschrift traf das nie
#      zu. Jetzt greift er wieder — und das ist richtig so, die duenne
#      Serife braucht ihn auf dem Foto, sonst steht weisse Schrift auf
#      hellem Bild.
P.append(('fotoSchriften:["Anton"]', 'fotoSchriften:[BS_KACHEL.fotoSchrift]',
 "Fotoschrift aus BS_KACHEL", 1))
P.append((r'const i=e&&e.fotoSchriften||["Anton"];return i[t%i.length]',
 r'const i=e&&e.fotoSchriften||[BS_KACHEL.fotoSchrift];return i[t%i.length]',
 "Fotoschrift Ersatzwert aus BS_KACHEL", 1))

# 30 — Erste Fotoslide in Prata. Der Weg ueber kachelSchrift und co()
#      war zu indirekt: co() sucht die Familie in einer Auswahlliste,
#      und dort steht Prata nicht. Die Familie wird jetzt direkt gesetzt,
#      an derselben Stelle, an der schriftUeber wirkt.
#
#      Prata ist in site/index.html per @font-face registriert (NICHT im
#      gebauten CSS — dort steht sie nicht, das hatte mich getaeuscht)
#      und liegt als site/fonts/Prata-Regular.woff2.
P.append(('tt.schriftUeber&&(Qe=tt.schriftUeber),tt.flieszSchrift&&t.bodySchrift&&(Qe=t.bodySchrift);',
 'tt.schriftUeber&&(Qe=tt.schriftUeber),tt.flieszSchrift&&t.bodySchrift&&(Qe=t.bodySchrift),'
 '$e&&t.folienRolle==="deckblatt"&&BS_KACHEL.deckblattFamilie&&(Qe=BS_KACHEL.deckblattFamilie);',
 "Erste Fotoslide in der Deckblatt-Familie", 1))

# 31 — Prata muss vor dem Zeichnen geladen sein. Fabric misst sonst mit
#      der Ersatzschrift, haelt zu breite Zeilen fuer passend, und der
#      Text laeuft aus dem Bild. Genau die Falle aus EINBAU.md.
P.append(('["Anton","Montserrat","Playfair Display","Playfair","Instrument Serif","Syne","Archivo","Cormorant Garamond","AspektaBrand","HelveticaNeueBrand","Mirage","Rosaline","ZT Otez"]',
 '["Anton","Montserrat","Playfair Display","Playfair","Instrument Serif","Syne","Archivo","Cormorant Garamond","AspektaBrand","HelveticaNeueBrand","Mirage","Rosaline","ZT Otez","Prata","Inter"]',
 "Prata und Inter vorladen", 1))

# 32 — Folgeslides eines Fotoposts: linksbuendig, Inter, erste Zeile
#      fett. Der vorhandene Fotostil "montserrat" liefert genau das:
#
#        ausrichtung:"links", fettNurErste:!0, nurErsteZeilePlatte:!0
#
#      Er wird fuer Fotoslides ab der zweiten erzwungen. Wichtig: der
#      Groessenabzug
#
#        t.textStil==="montserrat" && (qe = qe*.70)
#
#      prueft t.textStil, nicht den hier ueberschriebenen Wert — er
#      greift also NICHT. fotoGroesse ist deshalb die echte Groesse:
#      44 gegen 52 auf der ersten Slide, also 15 Prozent kleiner.
P.append(('textStil:t.textStil||"platte",bandFarbe:t.bandFarbe||"weiss",kachelSchrift:t.kachelSchrift||"marke",karte:t.karte||"dunkel"});',
 'textStil:($e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeStil)||t.textStil||"platte",'
 'bandFarbe:t.bandFarbe||"weiss",kachelSchrift:t.kachelSchrift||"marke",karte:t.karte||"dunkel"});',
 "Folgeslides im Stil links mit fetter erster Zeile", 1))

# 33 — Und ihre Schrift. Steht nach den beiden vorhandenen
#      Zuweisungen, damit sie gewinnt: flieszSchrift des Stils wuerde
#      sonst t.bodySchrift durchlassen.
P.append(('$e&&t.folienRolle==="deckblatt"&&BS_KACHEL.deckblattFamilie&&(Qe=BS_KACHEL.deckblattFamilie);',
 '$e&&t.folienRolle==="deckblatt"&&BS_KACHEL.deckblattFamilie&&(Qe=BS_KACHEL.deckblattFamilie),'
 '$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);',
 "Folgeslides in der Folge-Familie", 1))

# 45 — Das Deckblatt darf fett sein.
#
#      Im Bundle steht eine Zeile, die jede Playfair-Variante hart auf
#      Gewicht 400 zurueckdreht. Wer deckblattFamilie auf "Playfair
#      Display" stellt, bekommt deshalb still eine duenne Ueberschrift
#      und sucht den Fehler in der Groesse. Das Deckblatt nimmt jetzt
#      deckblattGewicht, alles andere bleibt wie es war.
P.append(('/Playfair/.test(String(Qe))&&(kt="400");',
 '/Playfair/.test(String(Qe))&&(kt="400"),'
 '$e&&t.folienRolle==="deckblatt"&&BS_KACHEL.deckblattGewicht&&(kt=BS_KACHEL.deckblattGewicht);',
 "Deckblatt in deckblattGewicht statt hart 400", 1))

# 34 — Warmes Overlay ueber den Bildern.
#
#      Drei Ebenen liegen ueber einem Foto. Sie waren alle neutral
#      schwarz, dadurch wirkten die Bilder kuehl und grau:
#
#        1. flaches Abdunkeln mit der Deckkraft Et (normal .05,
#           bei Weichzeichner .42)
#        2. NEU: eine warme Lasur, bildTon nicht mehr schwarz
#        3. der Kantenverlauf oben und unten
#
#      bildTon dunkelt jetzt in warmem Braun ab, waermeTon legt die
#      Lasur darueber, und der Kantenverlauf ist ebenfalls warm.
#      Alle drei Werte stehen im Block.
P.append(('const ur=new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgba(0,0,0,${Et})`,selectable:!1});Et>0&&e.add(ur);',
 'const ur=new Pe.fabric.Rect({left:0,top:0,width:r,height:n,'
 'fill:`rgba(${BS_KACHEL.bildTon||"0,0,0"},${Et})`,selectable:!1});Et>0&&e.add(ur);'
 'BS_KACHEL.waerme>0&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,'
 'fill:`rgba(${BS_KACHEL.waermeTon},${BS_KACHEL.waerme})`,selectable:!1,evented:!1}));',
 "Warme Lasur ueber dem Bild", 1))

P.append(('colorStops:[{offset:0,color:"rgba(0,0,0,0.30)"},{offset:.18,color:"rgba(0,0,0,0.0)"},{offset:.82,color:"rgba(0,0,0,0.0)"},{offset:1,color:"rgba(0,0,0,0.35)"}]',
 'colorStops:[{offset:0,color:`rgba(${BS_KACHEL.bildTon},0.34)`},'
 '{offset:.18,color:`rgba(${BS_KACHEL.bildTon},0.0)`},'
 '{offset:.82,color:`rgba(${BS_KACHEL.bildTon},0.0)`},'
 '{offset:1,color:`rgba(${BS_KACHEL.bildTon},0.40)`}]',
 "Kantenverlauf warm statt schwarz", 1))

# 35 — Der Tiefenverlauf gilt fuer alle feinen Schriften, nicht nur
#      fuer Playfair.
#
#      Eintrag 14 hatte ihn auf Playfair beschraenkt, weil die
#      Fotoschrift damals Anton war und der Verlauf dort doppelt
#      verdunkelte. Seit die Fotoschrift eine Serife ist, war der
#      Verlauf damit AUS — und genau er macht weissen Text auf einem
#      Foto lesbar. Deshalb war das Vorbild besser zu lesen.
#
#      Die Liste steht jetzt im Block. Anton und ArchivoBlack sind
#      absichtlich nicht drin: die tragen ohne Verlauf.
P.append(('if($e&&/Playfair/.test(String(Qe))&&t.tiefenOverlay!==!1)',
 'if($e&&new RegExp(BS_KACHEL.tiefeSchriften||"Playfair").test(String(Qe))&&t.tiefenOverlay!==!1)',
 "Tiefenverlauf fuer alle feinen Schriften", 1))

# 36 — Der Tiefenverlauf war ein Vollflaechen-Dunkel, kein Verlauf.
#
#      Seine Werte waren .82 oben, .58 in der Mitte, .90 unten. Damit
#      dunkelt er das ganze Bild ab, nicht nur die Textzone. Zusammen
#      mit Abdunkeln, Lasur und Kantenverlauf blieben rechnerisch
#      9,5 Prozent vom Foto uebrig — dunkler Schlamm, in dem auch
#      weisser Text nicht mehr traegt, weil ihm der Kontrast zum
#      Untergrund fehlt.
#
#      Das Vorbild macht es anders: oben hell, unten dunkel, genau
#      dort wo der Text sitzt. Die drei Werte stehen jetzt im Block.
P.append(('colorStops:[{offset:0,color:"rgba(18,16,14,0.82)"},{offset:.5,color:"rgba(18,16,14,0.58)"},{offset:1,color:"rgba(18,16,14,0.90)"}]',
 'colorStops:[{offset:0,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.tiefeOben})`},'
 '{offset:.45,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.tiefeMitte})`},'
 '{offset:1,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.tiefeUnten})`}]',
 "Tiefenverlauf unten schwer statt ueberall dunkel", 1))

# 47 — Das Schildchen ueber der Ueberschrift der Fotokachel.
#
#      Im Vorbild steht ueber der Ueberschrift eine kleine beige
#      Flaeche mit dem Namen der Reihe ("Die 5 Levels von Hooks").
#      Sie ist das Element, das die Fotokacheln als Reihe lesbar
#      macht.
#
#      Es haengt nicht an einer festen Hoehe, sondern an der ersten
#      Zeile der Ueberschrift: De ist deren Mitte, Et ihre Hoehe, _e
#      der linke Rand. Wandert die Ueberschrift (Lage oben, mitte,
#      unten, mehr oder weniger Zeilen), wandert das Schild mit.
#
#      Der Text kommt aus t.schild. Eingetragen wird er im Tagesmenue
#      des Content Plans, siehe Eintrag 48.
SCHILD = ('(()=>{try{const SS=String(t.schild||"").trim();'
 'if(!SS||!$e||t.folienRolle!=="deckblatt")return;'
 'const KK=BS_KACHEL,sg=r*(KK.schildGroesse||.03),'
 'pol=sg*(KK.schildPolster||.9),bh=sg*(KK.schildHoehe||2),'
 'mess=new Pe.fabric.Text(SS,{fontSize:sg,fontFamily:KK.schildSchrift||KK.schriftart,'
 'fontWeight:KK.schildGewicht||"400",charSpacing:KK.schildLaufweite||0}),'
 'bw=mess.width+pol*2,'
 'my=De-Et/2-r*(KK.schildAbstand||.034)-bh/2,'
 'lx=tt.ausrichtung==="links"?_e:r/2-bw/2,'
 'rd=r*(KK.schildRundung||.004);'
 'const nei=Number(KK.schildNeigung)||0;'
 'e.add(new Pe.fabric.Rect({left:lx,top:my,width:bw,height:bh,originX:"left",originY:"center",'
 'angle:nei,fill:KK.schildGrund||"#A57F55",rx:rd,ry:rd,selectable:!1,evented:!1}));'
 'e.add(new Pe.fabric.Text(SS,{left:lx+pol,top:my,originX:"left",originY:"center",'
 'fontSize:sg,fontFamily:KK.schildSchrift||KK.schriftart,fontWeight:KK.schildGewicht||"400",'
 'charSpacing:KK.schildLaufweite||0,fill:KK.schildSchriftFarbe||"#FFFFFF",'
 'angle:nei,selectable:!1,evented:!1}));}catch(zz){}})();')
P.append(('dr.forEach((Je,rt)=>{if(!Je.length){',
 SCHILD + 'dr.forEach((Je,rt)=>{if(!Je.length){',
 "Schildchen ueber der ersten Zeile der Ueberschrift", 1))

# 48 — Und das Feld dazu im Tagesmenue des Content Plans.
#
#      Gleiche Form wie die vorhandenen Schalter daneben: der Wert
#      wird auf den Tag UND auf jede seiner Folien geschrieben, damit
#      der Zeichner ihn als t.schild vorfindet.
#
#      Das Feld ist bewusst unkontrolliert (defaultValue statt value)
#      und schreibt erst beim Verlassen. Ein kontrolliertes Feld
#      wuerde bei jedem Tastendruck den ganzen Plan neu zeichnen und
#      dabei den Schreibcursor verlieren.
P.append(('Qt=(ae,_e)=>{$(`Tag ${ae}: Stil ${_e}`);',
 'schildSetzen=(ae,_e)=>{const ve=i.map(He=>He.day===ae?{...He,schild:_e,'
 'slides:(Array.isArray(He.slides)?He.slides:[]).map(De=>De&&typeof De=="object"?{...De,schild:_e}:De)}:He);'
 't({contentPlan:Rt(ve,We)})},'
 'Qt=(ae,_e)=>{$(`Tag ${ae}: Stil ${_e}`);',
 "Setzer fuer das Schild", 1))

P.append(('v.jsx("span",{className:"block text-[10px] font-bold text-gray-400 mb-1.5",'
 'children:"SCHRIFT \u2014 je schmaler, desto mehr Text passt"})',
 'v.jsx("span",{className:"block text-[10px] font-bold text-gray-400 mb-1.5",'
 'children:"SCHILD \u2014 Name der Reihe, steht ueber der Ueberschrift"}),'
 'v.jsx("input",{type:"text",defaultValue:ae.schild||"",'
 'placeholder:"z. B. Die 5 Levels von Hooks",'
 'onClick:Mt=>Mt.stopPropagation(),'
 'onBlur:Mt=>schildSetzen(ae.day,Mt.target.value.trim()),'
 'onKeyDown:Mt=>{Mt.key==="Enter"&&Mt.target.blur()},'
 'className:"w-full mb-3 px-2.5 py-2 rounded-lg border border-gray-200 text-[11px]"}),'
 'v.jsx("span",{className:"block text-[10px] font-bold text-gray-400 mb-1.5",'
 'children:"SCHRIFT \u2014 je schmaler, desto mehr Text passt"})',
 "Eingabefeld fuer das Schild im Tagesmenue", 1))

# 49 — Die Luecken mitten in den Woertern.
#
#      "D afuer bin ich no ch nich t weit genug." Fabric misst die
#      Breite jedes Zeichens einmal und merkt sie sich global, fuer
#      die ganze Sitzung. Wird eine Kachel gezeichnet, bevor die
#      Schrift geladen ist, landen die Masse der Ersatzschrift im
#      Speicher. Danach zeichnet der Browser die richtigen Buchstaben,
#      setzt sie aber an die Stellen der falschen — Luecken mitten im
#      Wort. Sichtbar wird das nur bei charSpacing, weil Fabric dann
#      Zeichen fuer Zeichen setzt statt die Zeile am Stueck.
#
#      Drei Ursachen, alle drei hier:
#
#      1. Die Vorschau wartete gar nicht auf die Schriften. Die
#         Bedingung "i&&!u" wartete nur, wenn die Kachel als Bild
#         gebraucht wurde. Im Content Plan wurde sofort gezeichnet.
#      2. Der Zwischenspeicher wurde nie geleert.
#      3. Der Notausgang nach zwei Sekunden zeichnet mit
#         Ersatzschrift; kam die echte Schrift spaeter, blieb die
#         Kachel falsch, weil d(!0) auf einen bereits gesetzten Wert
#         keine Neuzeichnung ausloest.
P.append(('const g=()=>{p||d(!0)},m=setTimeout(g,2e3);',
 # Nachtrag karten135: der Speicher wird zusaetzlich geleert,
 # sobald der Browser mit dem Laden von Schriften fertig ist.
 # Die Freigabe in der Vorschau deckt nur ihre eigene Zeichnung
 # ab; jede andere Leinwand, die frueher zeichnet, fuellt ihn neu.
 'try{if(!window.__bsSchriftWacht){window.__bsSchriftWacht=1;'
 'document.fonts&&document.fonts.addEventListener&&document.fonts.addEventListener("loadingdone",'
 '()=>{try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}})}}catch(zz){}'
 'const g=()=>{if(p)return;try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}d(!0)},'
 'm=setTimeout(g,2e3);',
 "Zeichenbreiten-Speicher leeren, bevor gezeichnet wird", 1))
P.append(('Promise.all(w).then(()=>document.fonts.ready).catch(()=>{}).then(g)',
 'Promise.all(w).then(()=>document.fonts.ready).catch(()=>{}).then(()=>{if(p)return;'
 'try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}'
 'd(!1),Promise.resolve().then(()=>{p||d(!0)})})',
 "Nach dem Laden neu zeichnen, auch wenn der Notausgang schon lief", 1))
P.append(('if(!p||!e||i&&!u)return;', 'if(!p||!e||!u)return;',
 "Vorschau wartet auf die Schriften, nicht nur der Bildexport", 1))
P.append(('.flatMap(b=>["400","700"].map(B=>{try{return document.fonts.load(`${B} 16px "${b}"`)}',
 '.flatMap(b=>["400","500","700"].map(B=>{try{return document.fonts.load(`${B} 16px "${b}"`)}',
 "Auch das mittlere Gewicht vorladen, der Name steht in 500", 1))

# 50 — Die vorgeladenen Schriften kommen aus dem Block.
#
#      Die Liste der Schriften, auf die die Vorschau wartet, stand
#      fest im Bundle. Wer in BS_KACHEL eine Schrift eintraegt, die
#      nicht darin vorkommt, bekommt sie nicht vorgeladen — die
#      Kachel wird mit der Ersatzschrift gezeichnet, und nach 48
#      wissen wir, was das anrichtet. Die Liste liest jetzt aus dem
#      Block mit. Eine Schrift wechseln heisst weiterhin: eine Zeile
#      in BS_KACHEL aendern, sonst nichts.
P.append(('const y=["Playfair Display","Instrument Serif","Syne","Archivo","Montserrat","Inter","AspektaBrand","HelveticaNeueBrand","Petrona","OpenSansBrand"];',
 'const y=["Playfair Display","Instrument Serif","Syne","Archivo","Montserrat","Inter",'
 '"AspektaBrand","HelveticaNeueBrand","Petrona","OpenSansBrand",'
 'BS_KACHEL.schriftart,BS_KACHEL.unterSchrift,BS_KACHEL.deckblattFamilie,'
 'BS_KACHEL.folgeFamilie,BS_KACHEL.fotoSchrift,BS_KACHEL.schildSchrift];',
 "Vorgeladene Schriften aus BS_KACHEL ergaenzen", 1))

# 51 — Warum die Schrift auf den Fotos klein war.
#
#      Nicht die Ausgangsgroesse war schuld. Zwei andere Werte haben
#      sie kleingerechnet:
#
#      1. Die Textspalte. Erkennt die App ein Gesicht, weicht der Text
#         zur Seite aus — bis auf 42 Prozent der Breite. In einer so
#         schmalen Spalte braucht derselbe Satz doppelt so viele
#         Zeilen, und die Anpassungsschleife schrumpft ihn, bis er in
#         die erlaubte Hoehe passt. Deshalb standen manche Kacheln in
#         winziger Schrift in einem Streifen am linken Rand.
#      2. Die erlaubte Texthoehe von 74 Prozent (48 mit Zaehler).
#
#      Beide Werte stehen jetzt im Block: spalteMin und textHoehe.
P.append(('zbr=tt.ausrichtung==="links"?(zsp>0?Math.max(.42,Math.min(.82,zsp/3+.08)):.82):.86',
 'zbr=tt.ausrichtung==="links"?(zsp>0?Math.max(BS_KACHEL.spalteMin||.42,Math.min(.82,zsp/3+.08)):.82):.86',
 "Mindestbreite der Textspalte aus dem Block", 1))
P.append(('{const Je=n*(jr?.48:.74);let rt=0;for(;;){',
 'const SR=$e&&String(t.schild||"").trim()?r*((BS_KACHEL.schildGroesse||.03)*(BS_KACHEL.schildHoehe||2)'
 '+(BS_KACHEL.schildAbstand||.034)):0;'
 '{const Je=n*(jr?(BS_KACHEL.textHoeheZaehler||.48):(BS_KACHEL.textHoehe||.74))-SR;let rt=0;for(;;){',
 "Erlaubte Texthoehe aus dem Block, abzueglich des Schilds", 1))

# 52 — Schild und Plaettchen schliessen einander aus.
#
#      Die Fotokachel hatte schon eine Flaeche: nurErsteZeilePlatte
#      legt einen cremefarbenen Kasten hinter die erste Zeile und
#      trennt den Text dafuer in zwei Bloecke — mit Luecke dazwischen.
#      Steht darueber jetzt auch noch das Schild, hat die Kachel zwei
#      Kaesten uebereinander und eine Ueberschrift, die auseinander
#      faellt. Im Vorbild gibt es genau eine Flaeche, und das ist das
#      Schild.
#
#      Ist ein Schild eingetragen, entfallen deshalb Plaettchen und
#      Trennung. Die Ueberschrift laeuft wieder als ein Block ueber
#      das Bild. Ohne Schild bleibt alles wie es war.
P.append(('$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);',
 '$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);'
 '$e&&(tt.nurErsteZeilePlatte=!0,tt.fettNurErste=!0,'
 '(!BS_KACHEL.bandAuf||t.folienRolle!=="deckblatt"||String(t.schild||"").trim())'
 '&&(tt.platten=!1,tt.ohnePlatteErste=!0));',
 "Fotos immer fett/nicht fett; Kasten nur weg auf Folgeslides und mit Schild", 1))

# 53 — Auf Fotos keine Luecke zwischen den Saetzen.
#
#      Zwischen dem ersten Block und dem Rest stand eine leere Zeile.
#      Sie gehoerte zum Kasten: der Kasten trennte, die Luecke gab ihm
#      Luft. Ohne Kasten ist sie nur noch ein Loch. Auf Kacheln ohne
#      Foto bleibt sie.
P.append(('...tt.engZeilen&&pr?[[]]:[],', '...tt.engZeilen&&pr&&!$e?[[]]:[],',
 "Keine Leerzeile zwischen den Bloecken auf Fotos", 1))

# 54 — Die Folgeslides bekommen ihre Schrift auch ohne Foto.
#
#      Die Zuweisung haing an $e, also am Hintergrundbild. Folgeslides
#      ohne Bild fielen durch und behielten, was der Stil vorgab.
P.append(('$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);',
 't.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);',
 "Folge-Familie auch ohne Foto", 1))

# 55 — Platz fuer das Schild freihalten.
#
#      Der Text wird zwischen n*.1 und n*.9 eingeklemmt. Steht er
#      oben, sitzt seine erste Zeile bei n*.1 — und das Schild sitzt
#      darueber, also im Rand, halb angeschnitten in der Ecke. Genau
#      das war zu sehen.
#
#      Die untere Klammer nimmt jetzt die Hoehe des Schilds mit auf.
#      Ist eines eingetragen, faengt der Text so viel tiefer an, wie
#      das Schild samt Abstand braucht. Ohne Schild aendert sich
#      nichts.
P.append(('De-Et/2<n*.1&&(De=n*.1+Et/2)', 'De-Et/2<n*.1+SR&&(De=n*.1+SR+Et/2)',
 "Text faengt tiefer an, wenn ein Schild darueber steht", 1))

# 57 — Helvetica Neue Thin fuer alles, was nicht die Pointe ist.
#
#      Die Textkachel nimmt gewicht aus dem Block, dort steht jetzt
#      200. Auf den Fotokacheln stand das leichte Gewicht fest im
#      Bundle: fettNurErste&&!Ve?"400":kt. Es liest jetzt
#      leichtGewicht mit, damit beide Kachelarten denselben Schnitt
#      benutzen. Die Stelle kommt dreimal vor.
#
#      Wichtig: 200 muss vorgeladen werden. Ein Gewicht, das nicht in
#      der Ladeliste steht, kommt zu spaet — und was dann passiert,
#      steht in Abschnitt 48.
P.append(('fontWeight:tt.fettNurErste&&!Ve?"400":kt',
 'fontWeight:tt.fettNurErste&&!Ve?(BS_KACHEL.leichtGewicht||"400"):kt',
 "Leichtes Gewicht auf Fotos aus dem Block", 3))
P.append(('.flatMap(b=>["400","500","700"].map(B=>{try{return document.fonts.load(`${B} 16px "${b}"`)}',
 '.flatMap(b=>["200","400","500","700"].map(B=>{try{return document.fonts.load(`${B} 16px "${b}"`)}',
 "Auch das duenne Gewicht vorladen", 1))

# 58 — Auf Fotos lief der Text seitlich heraus.
#
#      Die Anpassungsschleife hat nur die HOEHE geprueft. Passt ein
#      einzelnes Wort nicht in die Spalte, setzt der Umbruch es
#      trotzdem in die Zeile — die Bedingung dafuer steht in $t:
#
#          Ht(Vt,rt,Ve)<=Qt-c(30) || ct.length===0
#
#      Das zweite Oder ist die Notbremse: eine Zeile darf nie leer
#      bleiben. Ein zu langes Wort landet also in der Zeile und
#      laeuft rechts hinaus. Sichtbar wurde das erst mit Fraunces,
#      weil der fette Schnitt rund 30 Prozent breiter setzt als
#      Helvetica, und mit deckblattGroesse 58 statt 52.
#
#      Dieselbe Luecke wie damals bei den Textkacheln, an der zweiten
#      Stelle: dort prueft die Schleife seit Abschnitt 45 auch die
#      Breite, hier nicht. Jetzt hier auch. Die laengste Zeile
#      bestimmt die Groesse mit.
P.append(('if((Ve.length+pt.length)*qe*1.3<=Je||qe<=c(16)||rt++>60)break;',
 'const zb=Math.max(0,...Ve.map(zz=>Ht(zz,qe,!0)),'
 '...pt.map(zz=>Ht(zz,qe,!tt.fettNurErste)));'
 'if(((Ve.length+pt.length)*qe*1.3<=Je&&zb<=Qt-c(BS_KACHEL.umbruchRand||30))||qe<=c(16)||rt++>60)break;',
 "Anpassungsschleife prueft auf Fotos auch die Breite", 1))

# 59 — Die fette Zeile war schwarz, wo kein Kasten mehr ist.
#
#      Die Textfarbe hing an Ve, also an "gehoert zum ersten Block":
#
#          fill: Ve ? bandSchriftFarbe (schwarz) : schriftFarbe (weiss)
#
#      Das stimmte, solange der erste Block IMMER auf dem hellen
#      Kasten stand. Seit Abschnitt 56 zeichnen die Folgeslides
#      keinen Kasten mehr — die fette Zeile stand also schwarz auf
#      dem Foto, waehrend der Rest weiss blieb.
#
#      Richtig ist: dunkel genau dann, wenn wirklich ein Kasten
#      darunter liegt. Das ist dieselbe Bedingung, mit der der Kasten
#      gezeichnet wird. Sie steht jetzt bei der Farbe und beim Rand.
PLATTE = '(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))'
P.append(('fill:Ve?tt.bandSchriftFarbe||"#000000":tt.schriftFarbe||"#FFFFFF"',
 'fill:' + PLATTE + '?tt.bandSchriftFarbe||"#000000":tt.schriftFarbe||"#FFFFFF"',
 "Farbe der ersten Zeile folgt dem Kasten, nicht dem Block", 1))
P.append(('fill:rr?tt.highlight:Ve?tt.bandSchriftFarbe||"#000000":tt.schriftFarbe||"#FFFFFF"',
 'fill:rr?tt.highlight:' + PLATTE + '?tt.bandSchriftFarbe||"#000000":tt.schriftFarbe||"#FFFFFF"',
 "Dasselbe im Zweig mit Hervorhebung", 1))
P.append(('stroke:Ve?void 0:ut,strokeWidth:Ve?0:st',
 'stroke:' + PLATTE + '?void 0:ut,strokeWidth:' + PLATTE + '?0:st',
 "Rand der ersten Zeile folgt dem Kasten", 1))

# 60 — Der Kasten wird nie schmaler als seine Zeile.
#
#      Die Breite kam aus EINER von zwei Messungen: bei kursiven
#      Woertern Wort fuer Wort (Ht), sonst der Satz am Stueck
#      (pt.width). Gezeichnet wird aber je nach Fall mal so, mal so.
#      Solange beide Messungen dasselbe ergeben, faellt das nicht auf
#      — nachgemessen stimmen sie bei Helvetica und Fraunces auf den
#      Pixel. Verlassen sollte man sich darauf nicht: sobald eine der
#      beiden zu klein ausfaellt, steht der Text ueber dem Kasten
#      hinaus, und man sucht den Fehler bei der Schrift.
#
#      Jetzt gilt der groessere der beiden Werte. Der Kasten kann
#      damit zu breit sein, nie zu schmal.
P.append(('ct=sr(Je)?Ht(Je,qe,!(tt.fettNurErste&&!Ve)):pt.width,qt=ct+It*2',
 'ct=Math.max(pt.width,Ht(Je,qe,!(tt.fettNurErste&&!Ve))),qt=ct+It*2',
 "Kastenbreite aus der groesseren der beiden Messungen", 1))

# 61 — Fraunces darf die Kachel fuellen.
#
#      Drei Werte, kein Umbau. Nachgerechnet mit der echten
#      Anpassungsschleife (tools/.pruefen/gross.html), Vorschau
#      800x1000, Text "Von der Idee zum vierstelligen Angebot. /
#      Schritt 30 von 30.":
#
#        vorher   Spalte .72, Rand 48, Start 58  ->  77 px, 6 Zeilen
#        Spalte .82                              ->  87 px, 5 Zeilen
#        + Rand 12 + Start 68                    ->  90 px, 5 Zeilen
#
#      Der Umbruch warf bisher c(30) der Spaltenbreite weg, das sind
#      48 Pixel oder 6 Prozent der Kachel. Der Sicherheitsabstand
#      stammte aus einer Zeit, in der Messen und Malen
#      auseinanderliefen; nachgemessen weichen sie um 0,1 Prozent ab
#      (messbreite.html). 12 reicht.
#
#      Achtung: spalteMin .82 heisst, dass die Spalte immer so breit
#      ist. Das Ausweichen vor Gesichtern ist damit praktisch aus —
#      es war der Grund fuer die winzige Schrift in Abschnitt 51.
#      Eine Zahl, falls es zurueck soll.
P.append(('Ht(Vt,rt,Ve)<=Qt-c(30)', 'Ht(Vt,rt,Ve)<=Qt-c(BS_KACHEL.umbruchRand||30)',
 "Umbruchrand aus dem Block", 1))

# 62 — Der Zeilenabstand auf Fotos war das Letzte, was Platz frass.
#
#      Et = qe * 1.3 auf Fotos. Im Vorbild nachgemessen: Zeilenschritt
#      39 Pixel bei einer Schriftgroesse von rund 38,6 — also etwa
#      1,0. Wir standen ein Drittel darueber, und jede Zeile Abstand
#      kostet Schriftgroesse, weil die Anpassungsschleife die Hoehe
#      aller Zeilen zusammenzaehlt.
#
#      Jetzt 1,10 aus dem Block. Etwas mehr als das Vorbild, weil
#      Fraunces laengere Ober- und Unterlaengen hat als eine Grotesk.
P.append(('Et=qe*(tt.engZeilen?1.17:$e?1.3:1.06)',
 'Et=qe*(tt.engZeilen?1.17:$e?(BS_KACHEL.fotoZeile||1.3):1.06)',
 "Zeilenabstand auf Fotos aus dem Block", 1))

# 63 — Ein Band, keine Treppe.
#
#      Jede Zeile bekam einen eigenen Kasten in ihrer eigenen Breite.
#      Solange der erste Block eine Zeile lang war, fiel das nicht auf.
#      Seit die Schrift die Kachel fuellt, sind es vier Zeilen — und
#      vier verschieden lange Kaesten sehen aus wie eine Treppe, bei
#      der der kurze Kasten "zu kurz" wirkt.
#
#      Alle Kaesten des ersten Blocks bekommen jetzt dieselbe Breite:
#      die der laengsten Zeile. Da sie mit Et untereinander stehen und
#      Et+c(1.5) hoch sind, stossen sie aneinander und ergeben eine
#      durchgehende Flaeche. Zeilen ohne Kasten bleiben unveraendert.
P.append(('dr.forEach((Je,rt)=>{if(!Je.length){',
 'const PB=(()=>{let mx=0;for(let ii=0;ii<Lt&&ii<dr.length;ii+=1){const zz=dr[ii];'
 'if(!zz||!zz.length)continue;'
 'const p2=new Pe.fabric.Text(zz.map(xx=>xx.w).join(" "),{fontSize:qe,fontFamily:Qe,fontWeight:kt});'
 'mx=Math.max(mx,p2.width,Ht(zz,qe,!0))}return mx})();'
 'dr.forEach((Je,rt)=>{if(!Je.length){',
 "Breiteste Zeile des ersten Blocks vorab messen", 1))
P.append((',qt=ct+It*2', ',qt=(Ve?Math.max(ct,PB):ct)+It*2',
 "Alle Kaesten des ersten Blocks gleich breit", 1))

# 64 — Der Look aus ihrem Beitrag: Serif oben, Grotesk darunter.
#
#      Ausgemessen an ihrem Bildschirmfoto (Kachel 1206 breit):
#
#        Serifenblock   Zeichenhoehe 71  ->  Groesse rund 95  (7,9%)
#        Zeilenschritt  91                ->  0,96 der Groesse
#        Grotesk-Block  Zeichenhoehe 53  ->  Groesse rund 71  (5,9%)
#        Verhaeltnis    71/95            =   0,75
#        linker Rand    122 von 1206     =   10,1%
#
#      Bisher lief die ganze Folie in EINER Familie. Jetzt bekommt der
#      zweite Block eine eigene: zweiteFamilie, und mit zweitAnteil
#      eine eigene Groesse.
#
#      Umbruch und Anpassungsschleife rechnen weiter mit der GROSSEN
#      Groesse. Das schaetzt den zweiten Block zu breit und zu hoch —
#      also immer zur sicheren Seite. Zeilen brechen frueher, nie
#      spaeter; nichts kann seitlich hinauslaufen.
P.append(('Ht=(Je,rt,Ve)=>{const pt={fontSize:rt,fontFamily:Qe,fontWeight:Ve?kt:"400"}',
 'Ht=(Je,rt,Ve)=>{const pt={fontSize:rt,fontFamily:Ve?Qe:(BS_KACHEL.zweiteFamilie||Qe),fontWeight:Ve?kt:"400"}',
 "Messung des zweiten Blocks in seiner Familie", 1))
P.append(('Et=qe*(tt.engZeilen?1.17:$e?(BS_KACHEL.fotoZeile||1.3):1.06)',
 'Et=qe*(tt.engZeilen?1.17:$e?(BS_KACHEL.fotoZeile||1.3):1.06),'
 'qe2=$e?Math.round(qe*(BS_KACHEL.zweitAnteil||1)):qe,'
 'Et2=$e?qe2*(BS_KACHEL.fotoZeile||1.3):Et,'
 'QeZ=$e?(BS_KACHEL.zweiteFamilie||Qe):Qe',
 "Groesse, Zeilenhoehe und Familie des zweiten Blocks", 1))
P.append(('ae=dr.reduce((zs,zz)=>zs+(zz.length?Et:tt.engZeilen?qe*.92:Et),0)',
 'ae=dr.reduce((zs,zz,ii)=>zs+(zz.length?(tt.nurErsteZeilePlatte&&ii>=Lt?Et2:Et):tt.engZeilen?qe*.92:Et),0)',
 "Gesamthoehe zaehlt den zweiten Block in seiner Zeilenhoehe", 1))
P.append(('De+=Et}),Zt.length&&', 'De+=(Ve?Et:Et2)}),Zt.length&&',
 "Zeilenvorschub des zweiten Blocks", 1))
P.append(('pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:qe,fontFamily:Qe,fontWeight:',
 'pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:Ve?qe:qe2,fontFamily:Ve?Qe:QeZ,fontWeight:',
 "Zeilenbreite in der Familie und Groesse des Blocks", 1))
P.append(('const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",fontSize:qe,fontFamily:Qe,fontWeight:',
 'const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",fontSize:Ve?qe:qe2,fontFamily:Ve?Qe:QeZ,fontWeight:',
 "Zeichnen in der Familie und Groesse des Blocks", 1))
P.append(('Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",fontSize:qe,fontFamily:Qe,fontWeight:',
 'Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",fontSize:Ve?qe:qe2,fontFamily:Ve?Qe:QeZ,fontWeight:',
 "Dasselbe im Zweig mit kursiven Woertern", 1))

# 65 — Auf Fotos gewinnt jetzt ihre Einstellung, nicht die Automatik.
#
#      Die Textlage wurde so bestimmt:
#
#        ve = fettNurErste && !blur && textAnchor.row  ...   // Automatik
#             || t.textLage                                  // ihre Wahl
#             || (Foto ? "unten" : "mitte")                  // Vorgabe
#
#      Die Automatik aus der Bildanalyse stand VOR ihrer Wahl. Wo ein
#      Gesicht erkannt wurde, war "unten" wirkungslos.
#
#      Aufgefallen ist es erst jetzt, und das ist meine Schuld: die
#      Automatik haengt an fettNurErste, und das galt frueher nur fuer
#      den Stil "montserrat". Seit Abschnitt 56 setze ich es auf allen
#      Fotokacheln — damit war die Automatik ueberall aktiv und ihre
#      Wahl ueberall wirkungslos.
#
#      Reihenfolge jetzt: ihre Wahl, dann die Automatik, dann die
#      Vorgabe. Der Schalter "auto" im Tagesmenue setzt textLage auf
#      nichts — dort greift die Automatik weiter.
P.append(('const ve=tt.fettNurErste&&!t._blurAn&&t.textAnchor&&t.textAnchor.row&&{top:"oben",mid:"mitte",bottom:"unten"}[t.textAnchor.row]||t.textLage||($e?"unten":"mitte")',
 # karten136: die Automatik allein liefert auf aehnlichen Fotos
 # immer dieselbe Zeile — im Raster sieht dann alles gleich aus.
 # Reihenfolge jetzt: eigene Wahl, sonst eine feste Streuung aus
 # der Bildadresse, und die Automatik nur noch als Wache: liegt in
 # der gestreuten Reihe ein Gesicht, gilt die ruhige Zone.
 'const ve=(()=>{const zA=(tt.fettNurErste&&!t._blurAn&&t.textAnchor&&t.textAnchor.row&&'
 '{top:"oben",mid:"mitte",bottom:"unten"}[t.textAnchor.row])||"";'
 'if(t.textLage)return t.textLage;'
 'if(!BS_KACHEL.lagenWechsel)return zA||($e?"unten":"mitte");'
 'const zs=String(t.background||t.text||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi++)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'const zL=["unten","mitte","oben"][zh%3];'
 'const zG=(!t._blurAn&&t._autoImage&&t._autoImage.faceZones)||[];'
 'const zR={oben:0,mitte:1,unten:2}[zL];'
 'return zG.some(zz=>Math.floor(zz/3)===zR)?(zA||($e?"unten":"mitte")):zL})()',
 "Eingestellte Textlage schlaegt die Automatik", 1))

# 66 — Der erste Block darf mehr als eine Zeile sein.
#
#      Im Bundle steht eine Stelle, die den ersten Block auf GENAU
#      EINE Zeile zusammenstreicht: sie sucht die groesste Zahl an
#      Woertern, die noch in eine Zeile passt, und schiebt alles
#      weitere in den zweiten Block.
#
#          Ve = Woerter, die in eine Zeile passen
#          Ve < rt.length && (pr = Rest + pr, er = erste Ve Woerter)
#
#      Das gehoert zum Kasten: der Kasten ist ein Balken hinter EINER
#      Zeile. Ohne Kasten ist es nur eine Kappung mitten im Satz — der
#      erste Satz bricht nach ein paar Woertern ab und der Rest steht
#      klein darunter. Genau das war zu sehen.
#
#      Wieder eine Folge davon, dass ich nurErsteZeilePlatte auf allen
#      Fotokacheln setze (Abschnitt 56). Vorher lief die Stelle nur im
#      Stil "montserrat".
#
#      Die Kappung passiert jetzt nur noch, wenn wirklich ein Kasten
#      gezeichnet wird. Im Vorbild laeuft der Serifenblock ueber vier
#      Zeilen — genau das geht damit wieder.
P.append(('Ve=Math.max(2,Math.min(Ve,rt.length)),Ve<rt.length&&(',
 'Ve=Math.max(2,Math.min(Ve,rt.length)),(tt.platten||!tt.ohnePlatteErste)&&Ve<rt.length&&(',
 "Erster Block nur mit Kasten auf eine Zeile gekappt", 1))

# 67 — Auf den Folgeslides war der erste Block nicht fett.
#
#      deckblattGewicht gilt nur fuer das Deckblatt. Auf den
#      Folgeslides blieb kt bei dem, was der Stil vorgab — also leicht.
#      Der grosse erste Block sah damit aus wie der kleine zweite, nur
#      groesser.
#
#      Folgeslides haben jetzt ihr eigenes folgeGewicht, gleiche Form
#      wie deckblattGewicht. Der zweite Block bleibt bei
#      leichtGewicht, fett und nicht fett stimmt damit auf beiden
#      Kachelarten.
P.append(('$e&&t.folienRolle==="deckblatt"&&BS_KACHEL.deckblattGewicht&&(kt=BS_KACHEL.deckblattGewicht);',
 '$e&&t.folienRolle==="deckblatt"&&BS_KACHEL.deckblattGewicht&&(kt=BS_KACHEL.deckblattGewicht),'
 '$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeGewicht&&(kt=BS_KACHEL.folgeGewicht);',
 "Erster Block der Folgeslides in folgeGewicht", 1))

# 68 — Der Text sucht sich die ruhige Zone, statt das Bild
#      weichzuzeichnen.
#
#      Zwei Dinge standen dem im Weg.
#
#      **Der Weichzeichner.** Eintrag 2 zeichnet etwa jedes zweite
#      Bild ab Folie 2 weich. Das war die Notloesung, damit Text
#      irgendwo lesbar wird. Der Anteil steht jetzt im Block:
#      weichAnteil 0 heisst gar keiner. Wichtig dabei: der Zeichner
#      benutzt die Bildanalyse nur, wenn NICHT weichgezeichnet wird
#      (`!t._blurAn`). Weichzeichnen aus heisst also zugleich
#      Bildanalyse an.
#
#      **Die feste Textlage.** Jeder Tag bekam eine Lage aus einer
#      rotierenden Liste ["unten","mitte","oben"], auch wenn sie
#      keine gewaehlt hatte. Seit Abschnitt 64 schlaegt die
#      eingestellte Lage die Automatik — und weil immer eine
#      eingestellt war, kam die Automatik nie zum Zug. Die Liste
#      entfaellt: ohne eigene Wahl entscheidet die Bildanalyse, wo
#      die ruhigste Zone liegt.
#
#      Ihre Wahl im Tagesmenue gilt unveraendert und schlaegt weiter
#      alles andere.
P.append(('return (zh+Qe*17)%100>=50})()',
 'return (zh+Qe*17)%100>=100-(BS_KACHEL.weichAnteil||0)})()',
 "Anteil weichgezeichneter Folgebilder aus dem Block", 1))
P.append(('textLage:rt.textLage||ot.textLage||lS[(ot.day-1)%lS.length]',
 'textLage:rt.textLage||ot.textLage',
 "Keine rotierende Vorgabe mehr, sonst kommt die Bildanalyse nie dran", 1))

# 69 — Plan speichern: kleinere Bilder, zweiter Versuch, ehrliche
#      Meldung.
#
#      "Plan konnte nicht gespeichert werden (UnknownError)." Der Plan
#      liegt in der IndexedDB des Browsers, und die Fotos stecken als
#      Datenzeilen im Plan selbst. Bei siebzig Tagen sind das schnell
#      zig Megabyte; auf dem iPhone meldet Safari das nicht als
#      "Speicher voll", sondern als UnknownError.
#
#      Drei Dinge, in dieser Reihenfolge:
#
#      1. **Bilder verkleinern.** Vor dem Schreiben wird jedes Bild
#         auf hoechstens bildKante (1350) an der langen Seite
#         gerechnet und als JPEG mit bildGuete (.85) gespeichert. Das
#         Seitenverhaeltnis bleibt — der vorhandene Helfer n9 haette
#         auf 2:3 beschnitten, und die Kachel schneidet danach noch
#         einmal auf 4:5. Bilder unter 200 KB und solche, die schon
#         klein genug sind, bleiben unangetastet; das Ergebnis wird
#         nur genommen, wenn es wirklich kuerzer ist. Damit ist der
#         zweite Speichervorgang so schnell wie vorher.
#
#         1350 ist die Hoehe des Exports (1080x1350). Groesser
#         gespeichert bringt nichts.
#
#      2. **Zweiter Versuch.** Schlaegt das Schreiben fehl, werden
#         Bilder-Vorrat und Pin-Archiv geloescht — beides ist
#         nachladbar — und es wird noch einmal geschrieben.
#
#      3. **Ehrliche Meldung.** Statt "UnknownError" steht jetzt der
#         Grund, die Groesse der Bilder im Plan und, wo der Browser
#         es hergibt, belegter und verfuegbarer Speicher.
P.append(('let l={__packed:2,gallery:r,days:s};return new Promise(o=>{const a=h=>{console.error("[BrandStudio] Plan konnte nicht gespeichert werden:",h),typeof window<"u"&&window.dispatchEvent(new CustomEvent("brandstudio:plan-save-failed",{detail:{reason:String(h&&h.name||h||"unbekannt")}})),o(!1)},u=t.transaction([wr],"readwrite");u.onabort=()=>a(u.error);const A=u.objectStore(wr).put(l,D3);A.onsuccess=()=>o(!0),A.onerror=()=>{a(A.error)}})', 'const zKlein=zu=>new Promise(zr=>{try{if(typeof zu!="string"||!/^data:image\\//.test(zu)||zu.length<200000)return zr(zu);const zi=new Image();zi.onload=()=>{try{const zM=BS_KACHEL.bildKante||1350,zw=zi.width,zh=zi.height,zf=Math.min(1,zM/Math.max(zw,zh));if(zf>=1&&zu.length<1200000)return zr(zu);const zc=document.createElement("canvas");zc.width=Math.max(1,Math.round(zw*zf)),zc.height=Math.max(1,Math.round(zh*zf));zc.getContext("2d").drawImage(zi,0,0,zc.width,zc.height);const zn=zc.toDataURL("image/jpeg",BS_KACHEL.bildGuete||.85);zr(zn&&zn.length<zu.length?zn:zu)}catch(ze){zr(zu)}};zi.onerror=()=>zr(zu);zi.src=zu}catch(ze){zr(zu)}});const rk=await Promise.all(r.map(zKlein));let l={__packed:2,gallery:rk,days:s};const zSchreib=zd=>new Promise(zo=>{try{const zu2=t.transaction([wr],"readwrite");zu2.onabort=()=>zo(zu2.error||new Error("abort"));const zA=zu2.objectStore(wr).put(zd,D3);zA.onsuccess=()=>zo(null);zA.onerror=()=>zo(zA.error||new Error("error"))}catch(ze){zo(ze)}});let zF=await zSchreib(l);if(zF){try{await new Promise(zf2=>{const zs2=t.transaction([wr],"readwrite").objectStore(wr);try{zs2.delete(W3)}catch(ze){}const zd2=zs2.delete(z3);zd2.onsuccess=()=>zf2();zd2.onerror=()=>zf2()})}catch(ze){}zF=await zSchreib(l)}if(zF){const zMB=zx=>Math.round(zx/1048576*10)/10+" MB",zB=rk.reduce((za,zx)=>za+(typeof zx=="string"?zx.length:0),0);let zP="";try{if(navigator.storage&&navigator.storage.estimate){const zq=await navigator.storage.estimate();if(zq&&zq.quota)zP=", belegt "+zMB(zq.usage||0)+" von "+zMB(zq.quota)}}catch(ze){}const zT=String(zF&&zF.name||zF||"unbekannt")+" \\u2014 Bilder im Plan "+zMB(zB)+zP;console.error("[BrandStudio] Plan konnte nicht gespeichert werden:",zF);typeof window<"u"&&window.dispatchEvent(new CustomEvent("brandstudio:plan-save-failed",{detail:{reason:zT}}));return!1}return!0',
 "Plan speichern: verkleinern, zweiter Versuch, ehrliche Meldung", 1))

# 70 — Text etwas hoeher, Wortmarke an feste Stelle, und ein Grading.
#
#      **Die Unterkante.** Der Text durfte bis n*.9 reichen. Die
#      Wortmarke wird darunter gezeichnet (De + qe*.5) und stand
#      dadurch auf der Kachelkante, halb angeschnitten. Zwei
#      Aenderungen statt einer:
#
#        textUnten  .86   der Text endet hoeher
#        nameUnten  .945  die Wortmarke steht an einer FESTEN Stelle
#                         und haengt nicht mehr an der Textlaenge
#
#      Die Wortmarke gehoert zur Kachel, nicht zum Textblock. Solange
#      sie am Text hing, verschob jede Zeile mehr sie nach unten aus
#      dem Bild.
#
#      Weil der Text jetzt zwischen .10 und .86 liegt, also in 76
#      Prozent der Hoehe, muss textHoehe darunter bleiben, sonst
#      klemmen beide Klammern und die Textlage steht wieder still
#      (Abschnitt 56). Deshalb .74 -> .70, Weg also 6 Prozent.
#
#      **Das Grading.** Bisher lag nur ein Verlauf ueber dem Bild —
#      der dunkelt gleichmaessig ab und nimmt Zeichnung heraus, statt
#      Kontrast zu geben. Jetzt wird das Bild selbst gerechnet:
#
#        bildKontrast    .18   spreizt Lichter und Tiefen
#        bildHelligkeit  -.06  setzt den Schwarzpunkt tiefer
#
#      Beide 0 heisst: kein Filter, keine Rechenzeit. Die Filter
#      laufen auf dem bereits auf 1800 Pixel begrenzten Bild.
P.append(('De+ae-Et/2>n*.9&&(De=n*.9-ae+Et/2)',
 'De+ae-Et/2>n*(BS_KACHEL.textUnten||.9)&&(De=n*(BS_KACHEL.textUnten||.9)-ae+Et/2)',
 "Unterkante des Textes aus dem Block", 1))
P.append(('Pe.fabric.Text(Ze,{left:_e,top:De+qe*.5,originX:"left",originY:"center"',
 'Pe.fabric.Text(Ze,{left:_e,top:n*(BS_KACHEL.nameUnten||.945),originX:"left",originY:"center"',
 "Wortmarke an fester Stelle statt am Textende", 1))
P.append(('me.set({originX:"center",originY:"center",left:r/2+pr,top:n/2+jr,scaleX:jt,scaleY:jt,selectable:!1});',
 'me.set({originX:"center",originY:"center",left:r/2+pr,top:n/2+jr,scaleX:jt,scaleY:jt,selectable:!1});'
 'try{const zK=Number(BS_KACHEL.bildKontrast)||0,zH=Number(BS_KACHEL.bildHelligkeit)||0,zFl=[];'
 'zK&&zFl.push(new Pe.fabric.Image.filters.Contrast({contrast:zK}));'
 'zH&&zFl.push(new Pe.fabric.Image.filters.Brightness({brightness:zH}));'
 'zFl.length&&(me.filters=zFl,me.applyFilters())}catch(ze){}',
 "Kontrast und Schwarzpunkt auf dem Bild selbst", 1))

# 71 — Nein, die Folgeslides waren noch weichgezeichnet.
#
#      Abschnitt 67 hat den Zufallsanteil an weichgezeichneten Bildern
#      auf 0 gesetzt. Davor steht aber noch eine zweite Bedingung, die
#      der Drop selbst mitbringt:
#
#          dr = Qe>0 && ( t.textStil==="montserrat" || Zufall )
#
#      Und **alle** Folgeslides haben textStil "montserrat" — das ist
#      der Stil, der sie linksbuendig mit fetter erster Zeile setzt
#      (folgeStil). Die erste Bedingung war also immer wahr, der
#      Zufallsanteil kam nie zum Zug. Weichgezeichnet wurde weiter,
#      und zwar jede einzelne Folgeslide.
#
#      Jetzt schaltet weichAnteil den ganzen Weichzeichner: bei 0
#      bleibt kein Bild weich, auch kein montserrat-Bild.
P.append(('const dr=Qe>0&&(t.textStil==="montserrat"||',
 'const dr=Qe>0&&(BS_KACHEL.weichAnteil||0)>0&&(t.textStil==="montserrat"||',
 "weichAnteil schaltet auch die montserrat-Folien", 1))

# 72 — Der Weichzeichner hat das Grading ueberschrieben.
#
#      Abschnitt 69 haengt Kontrast und Schwarzpunkt an me.filters.
#      Ein paar Zeilen weiter setzt der Weichzeichner me.filters=[...]
#      — mit eckigen Klammern, also ersetzend. Auf jedem
#      weichgezeichneten Bild war das Grading damit weg. Jetzt haengt
#      er sich an, statt zu ersetzen.
P.append(('me.filters=[new Pe.fabric.Image.filters.Blur({blur:Math.min(Lt/40,.5)})],me.applyFilters()',
 'me.filters=(me.filters||[]).concat([new Pe.fabric.Image.filters.Blur({blur:Math.min(Lt/40,.5)})]),me.applyFilters()',
 "Weichzeichner haengt sich an das Grading an", 1))

# 72 — Die Ablauf-Folien in dasselbe System.
#
#      Sie standen als einzige noch auf eigenen Werten: Grund
#      #EFEAE2, Schrift #141210, Titel in "Anton". Anton ist eine
#      schmale Grotesk und hat mit dem Rest nichts zu tun.
#
#        Farben   grundA / schriftA aus dem Block
#        Titel    ablaufTitel (HelveticaNeueBrand) in
#                 ablaufTitelGewicht (700)
#
#      Das Monogramm faellt weg, wie bei den anderen Kacheln
#      (Abschnitt 26): ht() zeichnet es, sobald monogrammFarbe gesetzt
#      ist.
#
#      Die Titelstaerke wird nur im Ablauf-Zweig gesetzt (kein
#      Kopfzeilen-Fall, also LINKS falsch). Der andere Zweig, der
#      dieselbe Zeile benutzt, bleibt unveraendert.
P.append(('ablauf:{grund:"#EFEAE2",schriftGrund:"#FFFFFF",schrift:"#141210",betont:"#141210",monogramm:"#141210",absender:"rgba(20,18,16,0.55)",fassung:"ablauf",schriftart:"Playfair Display"}',
 'ablauf:{grund:BS_KACHEL.grundA,schriftGrund:BS_KACHEL.grundA,schrift:BS_KACHEL.schriftA,'
 'betont:BS_KACHEL.schriftA,absender:BS_KACHEL.schriftA,fassung:"ablauf",schriftart:BS_KACHEL.schriftart}',
 "Ablauf-Farben aus dem Block", 1))
P.append(('TITELSCHRIFT=LINKS?SERIF:"Anton"',
 'TITELSCHRIFT=LINKS?SERIF:(BS_KACHEL.ablaufTitel||"Anton")',
 "Ablauf-Titelschrift aus dem Block", 1))
P.append(('txt(zl,{left:AX,top:ty,originX:AO,originY:"center",fontSize:A.groesse,fontFamily:TITELSCHRIFT,charSpacing:FOLGE&&!LINKS?25:0,fill:TINT,maxB:MAXB});',
 'txt(zl,{left:AX,top:ty,originX:AO,originY:"center",fontSize:A.groesse,fontFamily:TITELSCHRIFT,'
 '...(LINKS?{}:{fontWeight:BS_KACHEL.ablaufTitelGewicht||"400"}),'
 'charSpacing:FOLGE&&!LINKS?25:0,fill:TINT,maxB:MAXB});',
 "Ablauf-Titel in seinem Gewicht", 1))

# 73 — Das letzte Overlay, das noch ausserhalb des Systems lag.
#
#      Liegt eine Ablauf-Folie auf einem Foto, bekommt sie einen
#      eigenen Verlauf, fest im Bundle:
#
#          rgba(18,16,14, .62 / .38 / .66)
#
#      Kalter Ton, und oben wie unten mehr als 60 Prozent Abdunklung.
#      Waehrend die Fotokacheln seit Abschnitt 63 bei .05/.10/.42 in
#      warmem Ton liegen, stand hier noch der alte Wert — das Bild
#      war praktisch nicht mehr zu sehen.
#
#      Ablauf-Folien tragen viel kleinen Text und brauchen mehr Halt
#      als eine Ueberschrift, deshalb eigene Werte statt derselben:
#
#          ablaufTiefeOben   .30
#          ablaufTiefeMitte  .22
#          ablaufTiefeUnten  .42
#
#      Der Ton kommt aus bildTon, also derselbe warme Braunton wie
#      ueberall sonst.
P.append(('colorStops:[{offset:0,color:"rgba(18,16,14,0.62)"},{offset:.45,color:"rgba(18,16,14,0.38)"},{offset:1,color:"rgba(18,16,14,0.66)"}]',
 'colorStops:[{offset:0,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.ablaufTiefeOben})`},'
 '{offset:.45,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.ablaufTiefeMitte})`},'
 '{offset:1,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.ablaufTiefeUnten})`}]',
 "Ablauf-Verlauf aus dem Block, warm und heller", 1))

# 74 — Die Ansprache der Ablauf-Texte.
#
#      Dreiundzwanzig feste Texte in drei Feldern (Intensive 6, Money
#      Room 7, Mentoring 10). Der **Ablauf** bleibt unangetastet:
#      Kopfzeile, Titel, Unterzeile und die Listen- beziehungsweise
#      Stationeneintraege stehen Zeichen fuer Zeichen wie vorher. Nur
#      die letzte Zeile jedes Textes, der Fliesstext, ist neu.
#
#      Was sich aendert, in Stichworten:
#
#        - Die Doppelverneinung ("nicht X, nicht Y, sondern Z") faellt
#          weg. Sie ist Werbetext, keine Sprechweise, und stand in
#          fast jedem Absatz.
#        - Dafuer je ein konkretes Bild aus der Sache selbst
#          ("ich tippe mit, du siehst zu").
#        - An zwei Stellen ein Eingestaendnis statt einer Behauptung
#          ("Ich habe das lange anders geglaubt", "das ist der
#          unangenehme Teil").
#        - Zahlen, Preise und Bedingungen unveraendert: 888 und 444,
#          97 im Monat, drei Monate Minimum, zwoelf Monate, acht
#          Etappen, acht Plaetze, zwei Tage.
#
#      Die drei Bloecke werden als Ganzes ersetzt. Die Rekonstruktion
#      wurde vorher gegen das Original geprueft: mit den alten Texten
#      ergibt sie Zeichen fuer Zeichen dieselbe Zeile.
P.append(('["#CARINA | ANNA | PRAV\\nDas Intensive\\n>EINE SITZUNG, EIN FERTIGES ANGEBOT\\n[stationen: Du füllst aus | Ich arbeite durch | 40 Minuten live]\\nEine Sitzung, in der dein Angebot ausgearbeitet wird. Nicht besprochen, nicht analysiert, sondern umgebaut, während wir reden. Du gehst mit dem Angebot raus, nicht mit Notizen darüber.", "#CARINA | ANNA | PRAV\\nVorher\\n>DU FÜLLST EIN DOKUMENT AUS\\n[liste: Dein Angebot, wie es heute dasteht | Dein Preis und was er enthält | Woran es hängt, deiner Einschätzung nach]\\nIch lese das durch, bevor wir uns sehen, und komme mit einer Meinung in den Termin. Wir starten nicht bei null und nicht bei deiner Selbstvorstellung, sondern bei dem, was auf dem Papier schon schiefsteht.", "#CARINA | ANNA | PRAV\\nDie 40 Minuten\\n>NUR DEIN FALL, NICHTS ANDERES\\n[stationen: Angebot | Preis | Aufforderung | Einwand]\\nWir gehen die Stellen durch, die entscheiden, und ich schreibe deine Sätze um, während du zuhörst. Die Sitzung ist die Ausarbeitung, nicht die Besprechung davon. Was am Ende steht, kannst du am selben Tag verschicken.", "#CARINA | ANNA | PRAV\\nWas danach dasteht\\n>DEIN ANGEBOT, NEU GEBAUT\\n[liste: Ein Paket statt drei | Der Preis sichtbar | Der Beleg neben der Behauptung]\\nEs geht nicht um ein neues Angebot, sondern um die Reihenfolge in dem, das du schon hast. Kein Rebrand, keine Positionierungsschleife. Umgebaut wird, was schon steht.", "#CARINA | ANNA | PRAV\\nFür wen das ist\\n>UND FÜR WEN NICHT\\n[liste: Du hast ein Angebot oder eine Idee daraus | Du setzt diese Woche um, nicht irgendwann | Nicht, wenn du sammeln willst statt umzusetzen]\\nOb du weit bist, ist egal. Ob du umsetzt, nicht. Wenn du gerade in einem anderen Programm steckst und es noch nicht umgesetzt hast, ist jetzt der falsche Moment.", "#CARINA | ANNA | PRAV\\nSo kommst du rein\\n>AUF ANFRAGE, KEIN KAUFKNOPF\\n[liste: Du sagst mir, welcher Weg | Ich melde mich in zwei Tagen | Ich sage dir, ob ein Platz frei ist]\\n888 Euro, aus dem Money Room 444. Es gibt keinen Kaufknopf, weil ich vorher wissen will, ob das Intensive für dich das Richtige ist. Wenn der Money Room besser passt, sage ich dir das auch."]',
 '["#CARINA | ANNA | PRAV\\nDas Intensive\\n>EINE SITZUNG, EIN FERTIGES ANGEBOT\\n[stationen: Du füllst aus | Ich arbeite durch | 40 Minuten live]\\nWir setzen uns hin und bauen dein Angebot um, während wir reden. Ich tippe mit, du siehst zu, wie sich die Sätze verändern. Am Ende hast du das Angebot da liegen und nicht drei Seiten Notizen, die du nächste Woche nicht mehr verstehst.", "#CARINA | ANNA | PRAV\\nVorher\\n>DU FÜLLST EIN DOKUMENT AUS\\n[liste: Dein Angebot, wie es heute dasteht | Dein Preis und was er enthält | Woran es hängt, deiner Einschätzung nach]\\nIch lese das durch, bevor wir uns sehen, und komme mit einer Meinung in den Termin. Wir müssen dann nicht bei deiner Vorstellungsrunde anfangen. Ich sage dir gleich, was mir auf dem Papier aufgefallen ist.", "#CARINA | ANNA | PRAV\\nDie 40 Minuten\\n>NUR DEIN FALL, NICHTS ANDERES\\n[stationen: Angebot | Preis | Aufforderung | Einwand]\\nWir nehmen uns die vier Stellen vor, an denen es hängt, und ich schreibe deine Sätze um, während du zuhörst. Manchmal reicht ein anderes Wort, manchmal muss der ganze Absatz raus. Was am Ende dasteht, kannst du noch am selben Abend verschicken.", "#CARINA | ANNA | PRAV\\nWas danach dasteht\\n>DEIN ANGEBOT, NEU GEBAUT\\n[liste: Ein Paket statt drei | Der Preis sichtbar | Der Beleg neben der Behauptung]\\nMeistens fehlt dir kein neues Angebot. Es steht nur in der falschen Reihenfolge da. Wir bauen um, was du schon hast, und du musst dich dafür nicht neu erfinden und auch nicht neu positionieren.", "#CARINA | ANNA | PRAV\\nFür wen das ist\\n>UND FÜR WEN NICHT\\n[liste: Du hast ein Angebot oder eine Idee daraus | Du setzt diese Woche um, nicht irgendwann | Nicht, wenn du sammeln willst statt umzusetzen]\\nOb du schon weit bist, ist mir egal. Ob du diese Woche etwas machst, nicht. Wenn du gerade in einem anderen Programm steckst und da noch nichts umgesetzt hast, warte lieber. Dann bringt dir das hier auch nichts.", "#CARINA | ANNA | PRAV\\nSo kommst du rein\\n>AUF ANFRAGE, KEIN KAUFKNOPF\\n[liste: Du sagst mir, welcher Weg | Ich melde mich in zwei Tagen | Ich sage dir, ob ein Platz frei ist]\\n888 Euro, aus dem Money Room 444. Einen Kaufknopf gibt es nicht, weil ich vorher wissen will, ob das Intensive überhaupt das Richtige für dich ist. Und wenn der Money Room besser passt, sage ich dir das, statt dir die Sitzung zu verkaufen."]',
 "Ablauf-Texte Block 1 (6 Folien)", 1))
P.append(('["#CARINA | ANNA | PRAV\\nThe Money Room\\n>DER SCHRITT, DER DIESE WOCHE ZAHLT\\n[liste: Du bringst mit, was auf dem Tisch liegt | Du gehst mit einem Move raus | Du machst ihn, bevor wir uns wiedersehen]\\nKein Lernprogramm, kein Modul, das du nachholen musst. Ein Raum, in dem du fragst und eine Antwort bekommst, mit der du am selben Tag etwas machen kannst.", "#CARINA | ANNA | PRAV\\nDer Rhythmus\\n>ALLE ZWEI WOCHEN EIN SLOT\\n[stationen: Woche 1 Slot | Woche 2 Fragen | Woche 3 Slot | Woche 4 Fragen]\\nDie Termine kündige ich vorher an, damit du planen kannst. In der Woche dazwischen werden deine Fragen beantwortet. Wer nur mitliest, braucht wenig Zeit. Wer fragt, bekommt mehr zurück.", "#CARINA | ANNA | PRAV\\nWann es dir passt\\n>ALLES LIEGT HOCHGELADEN BEREIT\\n[liste: Was da war, bleibt da | Du holst es dir, wann du Zeit hast | Keine Uhrzeit, zu der du dabei sein musst]\\nDu musst nicht live dabei sein, um etwas davon zu haben. Was im Slot besprochen wurde, liegt danach bereit, und du nimmst es dir, wenn dein Kind schläft oder der Kalender es hergibt.", "#CARINA | ANNA | PRAV\\nDrei Monate Minimum\\n>WARUM DAS SO IST\\n[stationen: Monat 1 umbauen | Monat 2 verkaufen | Monat 3 nachschärfen]\\nWeil in vier Wochen niemand ein Business dreht. Ich will keine Ergebnisse, die nie eine Chance hatten. Danach gehst du, wann du willst, und kommst wieder, wann du willst.", "#CARINA | ANNA | PRAV\\nWas drin passiert\\n>DU FRAGST, DU BEKOMMST EINE ANTWORT\\n[liste: Kein Modul, das du nachholen musst | Keine Bibliothek, die dich anschaut | Eine Frage, eine Antwort, du machst es]\\nWenn du schon zehn Kurse gekauft und nichts umgesetzt hast, ist das hier das Gegenteil. Du bringst mit, was gerade auf dem Tisch liegt, und gehst mit dem Schritt raus, der diese Woche zahlt.", "#CARINA | ANNA | PRAV\\nFür wen das ist\\n>UND FÜR WEN NICHT\\n[liste: Deine Kundinnen sind zufrieden, du verkaufst trotzdem zu wenig | Du weißt, was zu tun wäre, nur nicht was zuerst | Nicht, wenn du einen Content-Kalender suchst]\\nFür fünfzigtausend im Jahr brauchst du vierzehn Kundinnen, nicht fünfundzwanzigtausend Aufrufe. Es hängt an deinem Angebot und daran, wem du es wie sagst — nicht an deiner Reichweite.", "#CARINA | ANNA | PRAV\\nUnd dazu\\n>DAS INTENSIVE ZUM MITGLIEDERPREIS\\n[liste: Wenn ein Fall größer ist als ein Slot | Eine Sitzung nur für dich | Zum halben Preis, solange du drin bist]\\n97 Euro im Monat, drei Monate Minimum, danach monatlich kündbar. Wenn ein Fall größer ist, als er in einen Slot passt, nimmst du dir die Sitzung zum halben Preis: 444 statt 888."]',
 '["#CARINA | ANNA | PRAV\\nThe Money Room\\n>DER SCHRITT, DER DIESE WOCHE ZAHLT\\n[liste: Du bringst mit, was auf dem Tisch liegt | Du gehst mit einem Move raus | Du machst ihn, bevor wir uns wiedersehen]\\nKein Lernprogramm, das du nachholen musst. Du kommst mit dem, was gerade ansteht, stellst deine Frage und bekommst eine Antwort, mit der du noch am selben Tag etwas anfangen kannst.", "#CARINA | ANNA | PRAV\\nDer Rhythmus\\n>ALLE ZWEI WOCHEN EIN SLOT\\n[stationen: Woche 1 Slot | Woche 2 Fragen | Woche 3 Slot | Woche 4 Fragen]\\nDie Termine kündige ich vorher an, damit du sie einplanen kannst. In der Woche dazwischen beantworte ich, was hereinkommt. Wer nur mitliest, braucht wenig Zeit. Wer fragt, holt mehr heraus, und das liegt an dir, nicht an mir.", "#CARINA | ANNA | PRAV\\nWann es dir passt\\n>ALLES LIEGT HOCHGELADEN BEREIT\\n[liste: Was da war, bleibt da | Du holst es dir, wann du Zeit hast | Keine Uhrzeit, zu der du dabei sein musst]\\nDu musst nicht live dabei sein. Was im Slot besprochen wurde, liegt danach bereit, und du holst es dir, wenn dein Kind schläft oder der Kalender es hergibt. Ich weiß, wie das ist.", "#CARINA | ANNA | PRAV\\nDrei Monate Minimum\\n>WARUM DAS SO IST\\n[stationen: Monat 1 umbauen | Monat 2 verkaufen | Monat 3 nachschärfen]\\nWeil in vier Wochen niemand ein Business dreht. Ich will keine Ergebnisse beurteilen, die nie eine Chance hatten. Danach gehst du, wann du willst, und kommst wieder, wann du willst.", "#CARINA | ANNA | PRAV\\nWas drin passiert\\n>DU FRAGST, DU BEKOMMST EINE ANTWORT\\n[liste: Kein Modul, das du nachholen musst | Keine Bibliothek, die dich anschaut | Eine Frage, eine Antwort, du machst es]\\nWenn du schon zehn Kurse gekauft und keinen zu Ende gebracht hast, ist das hier das Gegenteil davon. Du bringst mit, was gerade auf dem Tisch liegt, und gehst mit dem einen Schritt raus, der diese Woche zahlt.", "#CARINA | ANNA | PRAV\\nFür wen das ist\\n>UND FÜR WEN NICHT\\n[liste: Deine Kundinnen sind zufrieden, du verkaufst trotzdem zu wenig | Du weißt, was zu tun wäre, nur nicht was zuerst | Nicht, wenn du einen Content-Kalender suchst]\\nFür fünfzigtausend im Jahr brauchst du vierzehn Kundinnen, nicht fünfundzwanzigtausend Aufrufe. Ich habe das lange anders geglaubt. Es hängt an deinem Angebot und daran, wem du es wie sagst.", "#CARINA | ANNA | PRAV\\nUnd dazu\\n>DAS INTENSIVE ZUM MITGLIEDERPREIS\\n[liste: Wenn ein Fall größer ist als ein Slot | Eine Sitzung nur für dich | Zum halben Preis, solange du drin bist]\\n97 Euro im Monat, drei Monate Minimum, danach monatlich kündbar. Und wenn ein Fall größer ist, als er in einen Slot passt, nimmst du dir die Sitzung zum halben Preis: 444 statt 888."]',
 "Ablauf-Texte Block 2 (7 Folien)", 1))
P.append(('["#CARINA | ANNA | PRAV\\nMentoring\\n>ZWÖLF MONATE, ACHT ETAPPEN\\n[stationen: 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08]\\nZwölf Monate, in denen ich an deinem Business mitarbeite statt es zu kommentieren. Acht Etappen geben dem Jahr eine Form, damit wir nicht zwölf Monate lang improvisieren.", "#CARINA | ANNA | PRAV\\nEtappe 01\\n>BRAINSTORM\\n[liste: Was du hast | Was du kannst | Was schon verkauft wurde]\\nWir tragen zusammen, was da ist: dein Angebot, dein Preis, deine Zahlen, deine bisherigen Kundinnen. Ohne das arbeiten wir an einer Vorstellung von deinem Business statt an deinem Business.", "#CARINA | ANNA | PRAV\\nEtappe 02\\n>STRATEGIESITZUNG\\n[liste: Was zuerst drankommt | Was liegen bleibt | Woran wir dich messen]\\nWir entscheiden die Reihenfolge. Nicht alles auf einmal, sondern der eine Schritt, der als Nächstes zahlt. Am Ende weißt du, woran wir zwölf Monate arbeiten.", "#CARINA | ANNA | PRAV\\nEtappe 03\\n>ZUSAMMENFASSUNG\\n[liste: Schriftlich, nicht im Kopf | Dein Angebot in sechs Zeilen | Der Preis und was er enthält]\\nWas wir entschieden haben, steht danach schwarz auf weiß. Du musst dich nicht erinnern, was in einem Call gesagt wurde, und ich muss dich nicht daran erinnern.", "#CARINA | ANNA | PRAV\\nEtappe 04\\n>TESTPHASE\\n[liste: Du schickst es raus | Ich lese mit | Wir sehen, was passiert]\\nJetzt geht es an echte Menschen. Alles, was du rausschickst, kann vorher über meinen Tisch. Wir korrigieren an echten Gesprächen, nicht an Beispielen.", "#CARINA | ANNA | PRAV\\nEtappe 05\\n>PLAN\\n[stationen: Angebot | Preis | Aufforderung | Beweis]\\nAus dem, was funktioniert hat, wird ein Ablauf, den du wiederholen kannst. Welcher Post welchen Job hat, was im Gespräch passiert, was du sagst, wenn sie zögert.", "#CARINA | ANNA | PRAV\\nEtappe 06\\n>PRÜFEN\\n[liste: Was hat verkauft | Was war nur Beschäftigung | Was fällt weg]\\nBeweis heißt Zahl, nicht Dankbarkeit. Wir schauen auf das, was tatsächlich gekauft wurde, und streichen den Rest — auch wenn er dir ans Herz gewachsen ist.", "#CARINA | ANNA | PRAV\\nEtappe 07\\n>NACHSCHÄRFEN\\n[liste: Die ersten drei Sätze | Der Einwand, der bleibt | Die Stelle, an der sie abspringt]\\nOb eine Zahl gehalten wird, entscheidet sich in dem Satz davor. Hier gehen wir genau dorthin, wo es in deinen Texten noch bröckelt.", "#CARINA | ANNA | PRAV\\nEtappe 08\\n>UMSATZBOOSTER\\n[liste: Was jetzt skaliert | Was du wiederholst | Was du das nächste Mal höher ansetzt]\\nAm Ende steht nicht ein neues Angebot, sondern eines, das trägt. Und die Frage, wo bei gleichem Aufwand mehr drin ist.", "#CARINA | ANNA | PRAV\\nDanach\\n>WEITER ODER ALLEIN\\n[liste: Die Sätze, mit denen du verkaufst | Der Prozess dahinter | Die Zahlen, die du jetzt kennst]\\nAlles, was wir gebaut haben, bleibt deins. Kein Zugang, der dir wieder weggenommen wird. Acht Plätze, kein Kaufknopf: du sagst mir, welcher Weg, und ich melde mich innerhalb von zwei Tagen."]',
 '["#CARINA | ANNA | PRAV\\nMentoring\\n>ZWÖLF MONATE, ACHT ETAPPEN\\n[stationen: 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08]\\nZwölf Monate, in denen ich an deinem Business mitarbeite, statt es zu kommentieren. Die acht Etappen geben dem Jahr eine Form. Sonst improvisieren wir zwölf Monate lang und wundern uns im Dezember.", "#CARINA | ANNA | PRAV\\nEtappe 01\\n>BRAINSTORM\\n[liste: Was du hast | Was du kannst | Was schon verkauft wurde]\\nWir tragen erst einmal zusammen, was da ist: dein Angebot, dein Preis, deine Zahlen, deine bisherigen Kundinnen. Ohne das arbeiten wir an einer Vorstellung von deinem Business und nicht an deinem.", "#CARINA | ANNA | PRAV\\nEtappe 02\\n>STRATEGIESITZUNG\\n[liste: Was zuerst drankommt | Was liegen bleibt | Woran wir dich messen]\\nWir entscheiden die Reihenfolge. Nicht alles auf einmal, sondern der eine Schritt, der als Nächstes zahlt. Am Ende weißt du, woran wir das Jahr über arbeiten, und ich auch.", "#CARINA | ANNA | PRAV\\nEtappe 03\\n>ZUSAMMENFASSUNG\\n[liste: Schriftlich, nicht im Kopf | Dein Angebot in sechs Zeilen | Der Preis und was er enthält]\\nWas wir entschieden haben, steht danach schwarz auf weiß da. Du musst dich nicht erinnern, was in einem Call gesagt wurde, und ich muss dich nicht daran erinnern.", "#CARINA | ANNA | PRAV\\nEtappe 04\\n>TESTPHASE\\n[liste: Du schickst es raus | Ich lese mit | Wir sehen, was passiert]\\nJetzt geht es an echte Menschen. Alles, was du rausschickst, kann vorher über meinen Tisch. Wir korrigieren an echten Gesprächen und nicht an ausgedachten Beispielen.", "#CARINA | ANNA | PRAV\\nEtappe 05\\n>PLAN\\n[stationen: Angebot | Preis | Aufforderung | Beweis]\\nAus dem, was funktioniert hat, wird ein Ablauf, den du wiederholen kannst. Welcher Post welchen Job hat, was im Gespräch passiert und was du sagst, wenn sie zögert.", "#CARINA | ANNA | PRAV\\nEtappe 06\\n>PRÜFEN\\n[liste: Was hat verkauft | Was war nur Beschäftigung | Was fällt weg]\\nBeweis heißt Zahl, nicht Dankbarkeit. Wir schauen, was tatsächlich gekauft wurde, und streichen den Rest. Auch das, woran dein Herz hängt, und das ist der unangenehme Teil.", "#CARINA | ANNA | PRAV\\nEtappe 07\\n>NACHSCHÄRFEN\\n[liste: Die ersten drei Sätze | Der Einwand, der bleibt | Die Stelle, an der sie abspringt]\\nOb eine Zahl gehalten wird, entscheidet sich in dem Satz davor. Hier gehen wir genau dorthin, wo es in deinen Texten noch bröckelt. Meistens sind es drei, vier Stellen.", "#CARINA | ANNA | PRAV\\nEtappe 08\\n>UMSATZBOOSTER\\n[liste: Was jetzt skaliert | Was du wiederholst | Was du das nächste Mal höher ansetzt]\\nAm Ende steht kein neues Angebot, sondern eines, das trägt. Und die Frage, wo bei gleichem Aufwand mehr drin ist.", "#CARINA | ANNA | PRAV\\nDanach\\n>WEITER ODER ALLEIN\\n[liste: Die Sätze, mit denen du verkaufst | Der Prozess dahinter | Die Zahlen, die du jetzt kennst]\\nAlles, was wir gebaut haben, bleibt deins. Es gibt keinen Zugang, der dir wieder weggenommen wird. Acht Plätze, keinen Kaufknopf: du sagst mir, welcher Weg, und ich melde mich innerhalb von zwei Tagen."]',
 "Ablauf-Texte Block 3 (10 Folien)", 1))

# 75 — Der Wechsel fett/leicht war weg, sobald der Text nur einen
#      Satz hat.
#
#      Die Trennung in ersten und zweiten Block haengt an einer
#      Satzgrenze:
#
#          /^(.{10,90}?[.!?:])\s+(.*)$/
#
#      Bis Abschnitt 65 gab es daneben die Kappung auf eine Zeile: was
#      nicht in die erste Zeile passte, rutschte in den zweiten Block.
#      Damit gab es IMMER zwei Bloecke, auch bei einem einzigen Satz —
#      dafuer mitten im Wort getrennt, was sie zu Recht bemaengelt hat.
#
#      Die Kappung ist weg, und damit bei einsaetzigen Texten auch der
#      Wechsel. Ihre Kacheln bestehen fast alle aus einem Satz, also
#      stand alles in fettem Fraunces.
#
#      Neue Regel, in dieser Reihenfolge:
#
#        1. eigene Zeilenumbrueche im Text   (wie bisher)
#        2. Satzgrenze                       (wie bisher)
#        3. **Satzteilgrenze**: das Komma oder die Konjunktion (und,
#           aber, weil, denn, damit, sondern, oder), die der Mitte am
#           naechsten liegt, und zwar nur zwischen 25 und 78 Prozent
#           der Laenge, damit kein Zweizeiler mit einem Wort dahinter
#           entsteht.
#        4. sonst gar nicht — kurze Saetze bleiben ein Block.
#
#      Getrennt wird also an einer Stelle, an der man auch beim
#      Sprechen Luft holt:
#
#          Wie kommst du in die Energie,
#          aus der heraus verkauft wird?
#
#      teilungAb (52 Zeichen) legt fest, ab welcher Laenge ueberhaupt
#      geteilt wird.
P.append(('Je?(er=Je[1],pr=Je[2]):(er=pr,pr="");', 'Je?(er=Je[1],pr=Je[2]):(()=>{const zS=String(pr),zL=zS.length;if(zL<(BS_KACHEL.teilungAb||52)){er=zS,pr="";return}const zK=[];let zm;const zr1=/,\\s+/g;while((zm=zr1.exec(zS)))zK.push([zm.index+1,zm.index+zm[0].length]);const zr2=/\\s+(?:und|aber|weil|denn|damit|sondern|oder)\\s+/g;while((zm=zr2.exec(zS)))zK.push([zm.index,zm.index+zm[0].length-zm[0].replace(/^\\s+/,"").length]);const zG=zK.filter(k=>k[0]>zL*.25&&k[0]<zL*.78);if(!zG.length){er=zS,pr="";return}zG.sort((a,b)=>Math.abs(a[0]-zL/2)-Math.abs(b[0]-zL/2));er=zS.slice(0,zG[0][0]).trim(),pr=zS.slice(zG[0][1]).trim()})();',
 "Zweiter Block auch ohne Satzgrenze, an der Satzteilgrenze", 1))

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
