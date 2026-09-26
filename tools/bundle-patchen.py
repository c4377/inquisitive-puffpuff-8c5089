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
# Der zweite Stil. Er ersetzt den Grundstil nicht, er liegt als
# Aufsatz darueber: site/dunkel/index.html setzt window.BS_STIL und
# der Block wird nach dem Anlegen ueberschrieben. Ein Bundle, zwei
# Feeds, dieselben Bilder und derselbe Plan (IndexedDB haengt an der
# Domain, nicht am Pfad).
DUNKEL = ('const BS_DUNKEL={grundA:"#FFFFFF",schriftA:"#000000",'
 'grundB:"#FFFFFF",schriftB:"#000000",'
 'deckblattFamilie:"Playfair Display",fotoSchrift:"Playfair Display",'
 'deckblattGewicht:"400",deckblattGroesse:98.9,fotoGroesse:64.1,zweiteFamilie:"Nothing You Could Do",zweitAnteil:.651,'
 'schriftart:"Marcellus",unterSchrift:"Marcellus",name:"",zeile:.95,absatz:0,'
 'kachelEinBlock:1,kachelSatzUmbruch:1,rand:.11,mitte:.50,maxhoehe:.46,groesseAnteil:.115,gewicht:"400",'
 'betontGewicht:"700",handAnteil:1.15,handGroesse:0.9486,folgeZweitHand:1,'
 'unterGewicht:"400",unterVerhaeltnis:1,laufweite:-35,fotoLaufweite:-20,'
 'folgeFamilie:"Playfair Display",ablaufTitel:"Playfair Display",'
 'nameSchrift:"Playfair Display",nameGewicht:"400",nameLaufweite:60,'
 'nameAnteil:.030,folgeAusrichtung:"mitte",textAnteil:28,textJede:7,'
 'geteilt:1,geteiltAnteil:25,geteiltOben:.16,geteiltUnten:.86,geteiltLuft:.05,'
 'deckblattSchnitte:"full|full|wide|full|wide|full",'
 'tonReihe:"14,13,12|26,20,16|12,16,20|22,14,20",tonNeutral:"13,13,13",'
 'versalAnteil:15,versalFamilie:"Shadows Into Light",versalGewicht:"400",'
 'versalLaufweite:20,versalGroesse:.065,versalZweitAnteil:1,'
 'fotoAusrichtung:"mitte",fotoSchriftFarbe:"#FFFFFF",'
 'bildTon:"14,13,12",waerme:0,waermeTon:"14,13,12",'
 'bildSaettigung:-1,saettigungReihe:"-1|0.1",saettigungWechsel:1,'
 'bildSchwarzpunkt:.07,bildVignette:.6,schwarzGrund:.2,textGrundZiel:4,textGrundMax:1.8,auflageReihe:"1|0.2|0.65|0.35",vignetteReihe:"1|0|0.55|0.25",auflageWechsel:1,folgeFuss:.86,lagenReihe:"unten",spalteBreit:.93,fotoRand:.035,textHoehe:.80,textMitte:.58,textLageUnten:.80,textMesseOben:.60,nameZeigen:0,'
 'bildHeben:0,bildSpreizung:.28,'
 'tiefeOben:.55,tiefeKnickOben:.16,tiefeMitte:.08,tiefeKnick:.60,tiefeKnickUnten:.999,tiefeUnten:.85,kanteOben:0,kanteUnten:0,'
 'saumStaerke:0,bildSchleier:.06,'
 'nameFarbe:"#F2EFE9",schildGrund:"#F2EFE9",schildSchriftFarbe:"#171512"};')
SCHALTER = 'if(typeof window<"u"&&window.BS_STIL==="dunkel")Object.assign(BS_KACHEL,BS_DUNKEL);'

KONFIG = 'const BS_KACHEL={grundA:"#F6F2EB",schriftA:"#241C16",grundB:"#4A3B30",schriftB:"#FFFFFF",schriftart:"HelveticaNeueBrand",unterSchrift:"HelveticaNeueBrand",unterVerhaeltnis:1,gewicht:"300",leichtGewicht:"300",unterGewicht:"700",groesseAnteil:.098,enge:1,laufweite:-50,zeile:1.02,absatz:.55,rand:.0885,mitte:.575,maxhoehe:.90,name:"carinaannaprav",nameAnteil:.042,nameDeckkraft:1,nameFarbe:"#E8836B",nameSchrift:"HelveticaNeueBrand",nameGewicht:"700",nameLaufweite:-50,nameAbstand:1.9,fotoSchrift:"Fraunces",deckblattFamilie:"Fraunces",deckblattGewicht:"700",deckblattGroesse:68,spalteMin:.82,textHoehe:.70,textHoeheZaehler:.50,textUnten:.86,nameUnten:.945,umbruchRand:12,fotoZeile:0.98,folgeStil:"montserrat",folgeFamilie:"Montserrat",zweiteFamilie:"HelveticaNeueBrand",zweitAnteil:.75,teilungAb:52,fotoSchriftFarbe:"#FFFFFF",bandAuf:0,folgeGewicht:"700",weichAnteil:0,lagenWechsel:1,folgeLage:"unten",folgeGroesseAnteil:.049,folgeMaxhoehe:.70,folgeAusrichtung:"links",textAnteil:67,fotoGroesse:44,schildGrund:"#E8836B",schildSchriftFarbe:"#241C16",schildSchrift:"HelveticaNeueBrand",schildGewicht:"400",schildGroesse:.030,schildLaufweite:6,schildPolster:.9,schildHoehe:2.0,schildAbstand:.034,schildRundung:.004,schildNeigung:-3,bildKante:2400,bildGuete:.84,bildKontrast:0,bildHelligkeit:0,bildSchleier:.05,bildSchleierWiederholung:.28,kanteOben:.34,kanteUnten:.40,ablaufTitel:"Montserrat",ablaufTitelGewicht:"700",ablaufTiefeOben:.30,ablaufTiefeMitte:.22,ablaufTiefeUnten:.42,bildTon:"74,58,44",waermeTon:"150,112,76",waerme:.07,tiefeOben:0,tiefeMitte:0,tiefeUnten:0,saumTon:"232,131,107",saumMitte:.08,saumStaerke:.30,saumWeite:.58,tiefeSchriften:"DM Serif|Nohemi|Shadows|Montserrat|Fraunces|Playfair|Marcellus|Prata|Italiana|Cormorant|Bodoni|Inter|Aspekta|Helvetica"};'
P.append(('function t6(e,t){', DUNKEL + KONFIG + SCHALTER + 'function t6(e,t){',
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
 'colorStops:[{offset:0,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.kanteOben})`},'
 '{offset:.18,color:`rgba(${BS_KACHEL.bildTon},0.0)`},'
 '{offset:.82,color:`rgba(${BS_KACHEL.bildTon},0.0)`},'
 '{offset:1,color:`rgba(${BS_KACHEL.bildTon},${BS_KACHEL.kanteUnten})`}]',
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
 'zbr=tt.ausrichtung==="links"?(zsp>0?Math.max(BS_KACHEL.spalteMin||.42,Math.min(.82,zsp/3+.08)):.82):'
 '(BS_KACHEL.spalteBreit||.86)',
 "Breite der Textspalte aus dem Block (min und max)", 1))
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
 'BS_KACHEL.fotoSchriftFarbe&&(tt.schriftFarbe=BS_KACHEL.fotoSchriftFarbe),'
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
 'QeZ=$e?(BS_KACHEL.zweiteFamilie||Qe):Qe,'
 # Notbremse: keine Zeile darf breiter sein als der Platz zwischen
 # den Raendern. Wenn doch, wird der ganze Block gleichmaessig
 # verkleinert — gleichmaessig, damit die Zeilen nicht
 # unterschiedlich gross werden.
 'zF=$e?(()=>{try{let zmx=0;'
 'for(let zi=0;zi<dr.length;zi+=1){const zz=dr[zi];if(!zz||!zz.length)continue;'
 'const zie=tt.nurErsteZeilePlatte&&zi<Lt;'
 'const zp=new Pe.fabric.Text(zz.map(zx=>zx.w).join(" "),{fontSize:zie?qe:qe2,'
 'fontFamily:zie?Qe:QeZ,fontWeight:tt.fettNurErste&&!zie?(BS_KACHEL.leichtGewicht||"400"):kt});'
 'zmx=Math.max(zmx,zp.width)}'
 'const zpl=r*(1-2*(BS_KACHEL.fotoRand||.09));'
 'return zmx>zpl?zpl/zmx:1}catch(zz){return 1}})():1',
 "Groesse, Zeilenhoehe und Familie des zweiten Blocks", 1))
P.append(('ae=dr.reduce((zs,zz)=>zs+(zz.length?Et:tt.engZeilen?qe*.92:Et),0)',
 'ae=dr.reduce((zs,zz,ii)=>zs+(zz.length?(tt.nurErsteZeilePlatte&&ii>=Lt?Et2:Et)*zF:(tt.engZeilen?qe*.92:Et)*zF),0)',
 "Gesamthoehe zaehlt den zweiten Block in seiner Zeilenhoehe", 1))
P.append(('De+=Et}),Zt.length&&', 'De+=(Ve?Et:Et2)*zF}),Zt.length&&',
 "Zeilenvorschub des zweiten Blocks", 1))
P.append(('pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:qe,fontFamily:Qe,fontWeight:',
 'pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,fontWeight:',
 "Zeilenbreite in der Familie und Groesse des Blocks", 1))
P.append(('const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",fontSize:qe,fontFamily:Qe,fontWeight:',
 'const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,fontWeight:',
 "Zeichnen in der Familie und Groesse des Blocks", 1))
P.append(('Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",fontSize:qe,fontFamily:Qe,fontWeight:',
 'Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,fontWeight:',
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

# 78 — Mehr Textkacheln im Raster.
#
#      Ob ein Tag ein Foto bekommt, entschied:
#
#          tS = e => { const t=(e%10+10)%10; return !(t===4||t===9) }
#
#      Also: von zehn Tagen bekommen acht ein Bild, zwei bleiben Text.
#      Zwanzig Prozent Textkacheln — im Raster verschwinden die
#      zwischen den Fotos.
#
#      Der Anteil steht jetzt im Block. textAnteil ist der Anteil der
#      Tage OHNE Foto, in Prozent:
#
#          (pt*37+13)%100 >= textAnteil   ->  Foto
#
#      Der Multiplikator 37 ist teilerfremd zu 100, die Reihe laeuft
#      also einmal durch alle Werte, bevor sie sich wiederholt: bei
#      35 sind es genau 35 von 100 Tagen, gleichmaessig verteilt, nie
#      zwei Textkacheln direkt hintereinander.
#
#      textAnteil auf 0 stellt die alte Regel wieder her.
P.append(('Vt=(qt?!Oe(ct,pt):tS(pt))&&He.length>0',
 'Vt=(BS_KACHEL.textAnteil?((pt*37+13)%100)>=BS_KACHEL.textAnteil:(qt?!Oe(ct,pt):tS(pt)))&&He.length>0',
 "Anteil der Textkacheln aus dem Block", 1))

# 81 — Der orange Lichtsaum am Rand der Fotos.
#
#      Zwei radiale Verlaeufe, je einer in einer Ecke, und zwar in
#      zwei diagonal gegenueberliegenden. Welches Paar drankommt,
#      entscheidet eine feste Streuung aus der Bildadresse — bei
#      geradem Wert oben links und unten rechts, sonst oben rechts
#      und unten links. Dasselbe Bild bekommt immer dieselben Ecken.
#
#      Der Ton ist orange-rosa (232,131,107), kein reines Orange.
#
#      (Frueher: ein radialer Verlauf ueber dem Bild, in der Mitte durchsichtig,
#      an den Raendern orange. Er gibt dem Foto Licht von aussen,
#      statt es einzufaerben, und bindet die Fotokacheln farblich an
#      die warmen Textkacheln.
#
#        saumTon       217,123,43   derselbe Orangeton wie das Rad
#        saumMitte     .18          bei 55 Prozent des Radius
#        saumStaerke   .62          aussen
#
#      saumStaerke auf 0 schaltet ihn ab. Er liegt UEBER dem
#      Tiefenverlauf, damit die Ecken nicht doppelt abgedunkelt und
#      dann eingefaerbt werden, sondern das Orange auf dem fertigen
#      Bild sitzt.
#
#      Ein Rahmen rundum wurde probiert und verworfen: im Raster
#      stehen fuenfzehn Rahmen nebeneinander und das Bild wird zur
#      Briefmarke.
P.append(('${BS_KACHEL.tiefeUnten})`}]})}))}', '${BS_KACHEL.tiefeUnten})`}]})})),BS_KACHEL.saumStaerke&&(()=>{const zs=String(t.background||t.text||"");let zh=0;for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;const zE=zh%2?[[r,0],[0,n]]:[[0,0],[r,n]];const zR=Math.max(r,n)*(BS_KACHEL.saumWeite||.62);zE.forEach(zk=>{e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"radial",coords:{x1:zk[0],y1:zk[1],r1:0,x2:zk[0],y2:zk[1],r2:zR},colorStops:[{offset:0,color:`rgba(${BS_KACHEL.saumTon},${BS_KACHEL.saumStaerke})`},{offset:.55,color:`rgba(${BS_KACHEL.saumTon},${BS_KACHEL.saumMitte})`},{offset:1,color:`rgba(${BS_KACHEL.saumTon},0)`}]})}))})})()}',
 "Oranger Lichtsaum am Bildrand", 1))

# 83 — Zeichenbreiten-Speicher vor JEDER Kachel leeren.
#
#      Nachgemessen an ihrem Fall "Du kannst niemanden auf ein Niveau
#      ziehen,": bei Umbruchgrenze 637 und Groesse 109 ergeben beide
#      Messwege — Canvas measureText und fabric.Text.width — dieselben
#      Breiten (561, 612, 371, 376, 389) und denselben Umbruch:
#
#          Du kannst / niemanden / auf ein / Niveau / ziehen,
#
#      Auf ihrem Bildschirm stand aber
#
#          Du kannst / niemanden auf ein / Niveau ziehen,
#
#      also deutlich laengere Zeilen. "niemanden auf ein" misst rund
#      1030 Pixel — das haette nie in 637 gepasst. Beim Umbruch wurde
#      also mit einer viel schmaleren Schrift gerechnet als beim
#      Zeichnen: die Ersatzschrift aus dem Zeichenbreiten-Speicher.
#
#      Die bisherigen Freigaben (Abschnitte 48 und 76) haengen an
#      Ereignissen: vor der Freigabe der Vorschau, und wenn der
#      Browser mit dem Laden fertig ist. Beide koennen zu frueh oder
#      zu spaet liegen, und eine einmal gezeichnete Kachel wird davon
#      nicht neu gezeichnet.
#
#      Jetzt wird der Speicher am Anfang JEDER Kachel geleert. Damit
#      gilt ohne Ausnahme: gemessen wird mit derselben Schrift, mit
#      der im selben Durchgang gezeichnet wird. Der Preis ist etwas
#      Rechenzeit pro Kachel, der Gewinn ist, dass diese Fehlerklasse
#      nicht wiederkommen kann.
P.append(('Ca=async(e,t,r,n,i={})=>{var yn,_n,Jr,xr,zr,ti,nn,_i,ki,ri;',
 'Ca=async(e,t,r,n,i={})=>{var yn,_n,Jr,xr,zr,ti,nn,_i,ki,ri;'
 'try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}',
 "Speicher vor jeder Kachel leeren", 1))

# 87 — Der flache Schleier ueber dem Foto haengt nicht mehr an der Kachel.
#
#      Carina: "Tag 8 ist perfekt der Rest ist mit overlay blass."
#      Gemessen im Vollaufbau (tools/.pruefen/schleier.html, gleiches
#      Foto, alle fuenf Ebenen):
#
#        Et=.05   Mittel 143   Streuung 24.1   hellstes 187
#        Et=.20   Mittel 132   Streuung 20.4   hellstes 167
#        Et=.25   Mittel 128   Streuung 19.2   hellstes 162
#        Et=.55   Mittel 104   Streuung 11.9   hellstes 125
#
#      Ein Fuenftel Kontrast weg, die Lichter um 25 Stufen gedeckelt —
#      genau das sieht sie als "blass".
#
#      Woher der Unterschied kommt: die automatische Bildzuweisung
#      schreibt jeder Folie ein overlay mit (hK gibt .2 zurueck, wenn
#      die Bildanalyse geklappt hat, sonst .25). Der Zeichner liest
#      das als t.overlay und dunkelt damit ab. Eine Kachel, deren Bild
#      NICHT ueber die Zuweisung kam, hat kein overlay und landet beim
#      Vorgabewert .05 — das ist Tag 8. Der Unterschied ist also nicht
#      das Bild und nicht die Ecke, sondern ein gespeicherter Wert.
#
#      bildSchleier deckelt ihn. Kein Foto kann dunkler verschleiert
#      werden als der Block erlaubt; wer weniger will, darf weniger.
#      Der Weichzeichner-Pfad bleibt ausgenommen: dort traegt die .42
#      den Text ueber dem unscharfen Bild, und ohne sie waere er weg.
#
#      Zweiter Fall: bildVerblasst=.55. Das ist KEIN Versehen, sondern
#      eine Folgefolie, die das Bild des Deckblatts noch einmal zeigt
#      ($l wird nur wahr, wenn die Folie keinen eigenen Hintergrund
#      hat und den des Deckblatts erbt). Die .55 sorgt dafuer, dass
#      sie als Hintergrund liest und nicht als Wiederholung. Sie wird
#      deshalb nicht gedeckelt, sondern bekommt einen eigenen Wert.
#      Angesehen in tools/.pruefen/wiederholung.html, Text in der
#      Mitte, also ohne Hilfe vom Kantenverlauf: bei .55 ist das Bild
#      fast weg, bei .20 ist es so stark wie das Deckblatt selbst,
#      bei .28 kommt es durch und die weisse Fraunces traegt noch.
#      Darum bildSchleierWiederholung:.28.
#
#      Absichtlich NICHT angefasst: die warme Lasur, der Kantenverlauf
#      und die Filterkette der App (contrastBoost .07, satBoost .3,
#      hellBoost .13). Die liegen auf JEDER Kachel, auch auf Tag 8 —
#      und Tag 8 nennt sie perfekt. Was auf Tag 8 gleich ist, ist
#      nicht die Ursache. kanteOben und kanteUnten stehen jetzt
#      trotzdem im Block, damit der Kantenverlauf spaeter an einer
#      Stelle aenderbar ist; die Werte sind unveraendert.
P.append(('t.bildVerblasst===!0?Et=.55:Et=dr?.42:.05;',
 't.bildVerblasst===!0?Et=.55:Et=dr?.42:.05;'
 'dr||(t.bildVerblasst===!0'
 '?typeof BS_KACHEL.bildSchleierWiederholung=="number"&&(Et=BS_KACHEL.bildSchleierWiederholung)'
 ':typeof BS_KACHEL.bildSchleier=="number"&&(Et=Math.min(Et,BS_KACHEL.bildSchleier)));',
 "Flacher Schleier kommt aus dem Block", 1))

# 88 — Das Schild in Orange-Rosa, und die Wortmarke auf JEDER Kachel.
#
#      **Das Schild.** Es war beige-tan (#A57F55) mit weisser Schrift,
#      also 3,6:1 — schon unter der Grenze fuer kleine Schrift, und
#      es hatte mit dem Saum in den Ecken nichts zu tun. Jetzt ist es
#      derselbe Ton wie der Saum, 232,131,107 = #E8836B, damit die
#      Kachel EINE Akzentfarbe hat statt zweier.
#
#      Weiss auf diesem Orange-Rosa waere 2,7:1 und matscht (angesehen
#      in tools/.pruefen/schildfarbe.html, vier Varianten am selben
#      Foto). Espresso #241C16 darauf sind 6,3:1 und stehen scharf.
#      Ein dunkleres Orange, das Weiss tragen wuerde (#C9614B, 4,3:1),
#      liest sich rot statt rosa. Also helles Schild, dunkle Schrift.
#
#      **Die Wortmarke.** Sie wurde an zwei Stellen im Code gezeichnet
#      und war deshalb zweimal etwas anderes:
#
#        Fotokachel   qe*.42 gross (haengt an der Ueberschrift!),
#                     OpenSansBrand — das ist OpenSans-BOLD, eine
#                     dritte Schrift neben Helvetica und Fraunces
#        Textkachel   r*.018 gross, also ein Viertel davon, mittig
#                     direkt unter dem Text statt an fester Stelle,
#                     Deckkraft .5
#
#      Auf der Fotokachel war sie damit auch noch von der Laenge der
#      Ueberschrift abhaengig: kurze Ueberschrift, grosse Wortmarke.
#      Genau der Fehler, den Eintrag 70 fuer die POSITION schon
#      behoben hat — fuer die GROESSE stand er noch offen.
#
#      Jetzt kommen beide aus denselben vier Werten:
#
#        nameAnteil     .042   Anteil der Kachelbreite, feste Groesse
#        nameDeckkraft  .55
#        nameSchrift    HelveticaNeueBrand
#        nameGewicht    400
#
#      .042 ist gemessen: die Fotokachel zeichnete die Wortmarke bei
#      diesem Text 34 Pixel hoch auf 800 Breite. Die Fotokachel bleibt
#      also so gross wie sie war, nur haengt sie nicht mehr an der
#      Ueberschrift, und die Textkachel zieht nach.
P.append(('if(NA)txt(NA,{left:r/2,top:y-gr*K.zeile+gr*K.nameAbstand,originX:"center",originY:"center",\n'
 'fontSize:NG,fontFamily:K.unterSchrift||K.schriftart,fontWeight:"500",charSpacing:150,\n'
 'fill:SCH,opacity:.5,maxB:MAXB});',
 'if(NA)txt(NA,{left:r/2,top:n*(K.nameUnten||.945),originX:"center",originY:"center",\n'
 'fontSize:NG,fontFamily:K.nameSchrift||K.unterSchrift||K.schriftart,'
 'fontWeight:(K.nameGewicht||"400"),charSpacing:150,\n'
 'fill:SCH,opacity:(K.nameDeckkraft||.55),maxB:MAXB});',
 "Wortmarke der Textkachel an dieselbe feste Stelle", 1))
P.append(('fontSize:Math.round(qe*.42),fontFamily:"OpenSansBrand",fill:"rgba(255,255,255,0.55)"',
 'fontSize:Math.round(r*(BS_KACHEL.nameAnteil||.042)),'
 'fontFamily:BS_KACHEL.nameSchrift||"OpenSansBrand",fontWeight:(BS_KACHEL.nameGewicht||"400"),'
 'charSpacing:150,fill:`rgba(255,255,255,${BS_KACHEL.nameDeckkraft||.55})`',
 "Wortmarke der Fotokachel aus dem Block statt aus der Ueberschrift", 1))

# 89 — Montserrat auf den Folgefolien, Helvetica Neue auf Folie 1.
#
#      Sieben Werte im Block standen auf HelveticaNeueBrand. Zwei
#      davon gehoeren den Folgefolien und stehen jetzt auf Montserrat:
#
#        folgeFamilie   die Folien 2 und weiter
#        ablaufTitel    die Ablauf-Folien, die immer Folgefolien sind
#
#      Die anderen fuenf gehoeren Folie 1 und bleiben Helvetica Neue:
#      schriftart, unterSchrift, zweiteFamilie, schildSchrift und
#      nameSchrift. Fraunces bleibt, wo Fraunces war (fotoSchrift,
#      deckblattFamilie).
#
#      **Die Wortmarke bleibt ueberall Helvetica**, auch auf den
#      Folgefolien. Sie ist eine Marke und keine Textschrift; wenn sie
#      zwischen Folie 1 und Folie 2 desselben Beitrags die Schrift
#      wechselt, liest sich das wie ein Fehler.
#
#      Zwei Stellen konnten die Regel nicht sehen und mussten sie
#      lernen — sonst waere eine Folgefolie halb Montserrat gewesen:
#
#        1. Die zweite Zeile auf einer Fotokachel kam immer aus
#           zweiteFamilie, egal ob Deckblatt oder Folgefolie. Auf
#           einer Folgefolie mit Bild stand dann die Ueberschrift in
#           Montserrat und die Zeile darunter in Helvetica.
#        2. Die Fassung "marke" nahm immer schriftart. Eine
#           Folgefolie ohne Bild blieb dadurch Helvetica.
#
#      Beide lesen jetzt die Rolle der Folie. Die Rolle steht schon
#      im Zeichner (Je.rolle beziehungsweise t.folienRolle) und hat
#      genau drei Werte: deckblatt, inhalt, abschluss — die
#      Ablauf-Fassung rechnet oben im selben Zeichner damit.
#
#      Die Regeln bleiben unangetastet: laufweite -50, zeile 1.02,
#      groesseAnteil .098, gewicht 300, unterGewicht 700. Montserrat
#      ist breiter als Helvetica Neue, also bricht der Anpassungslauf
#      frueher um — dieselbe Regel, ein anderes Ergebnis. Das ist
#      genau das gewuenschte Verhalten und kein Nachjustieren wert.
#
#      **Die Schriftdatei.** Im Projekt lagen nur zwei feste Schnitte
#      (Montserrat-Regular 400 und Montserrat-Bold 700). Der Schnitt
#      der Marke ist aber **Light 300**, und der haette ueber Google
#      kommen muessen — bei einer Schrift, die der Zeichner auf dem
#      Canvas ausmisst, ist das genau die Falle, die schon dreimal
#      zugeschnappt ist (gemessen mit der Ersatzschrift, gezeichnet
#      mit der richtigen). Deshalb liegt jetzt EINE Datei im Projekt,
#      Montserrat-Variable.woff2, angemeldet fuer 100 bis 900 mit
#      font-display:block. Kein Schnitt kann mehr fehlen, und die
#      zwei festen Dateien sind raus.
#
#      Nachgesehen: die App laedt Montserrat ohnehin schon in
#      700/600/400/300/100 vor, und Montserrat steht in ihrer Liste
#      bekannter Schriften. tiefeSchriften kennt es jetzt auch, damit
#      der Tiefenverlauf greift, wenn eine Folgefolie in Montserrat
#      auf einem Foto steht.
#
#      Nicht angefasst: folgeStil "montserrat". Das ist der Name
#      eines Layouts, keine Schrift.

P.append(('QeZ=$e?(BS_KACHEL.zweiteFamilie||Qe):Qe',
 'QeZ=$e?((t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie)'
 '||BS_KACHEL.zweiteFamilie||Qe):Qe',
 "Zweite Zeile auf dem Foto folgt der Rolle der Folie", 1))
P.append(('const FAM=ix=>ix===0?K.schriftart:(K.unterSchrift||K.schriftart);',
 'const FOLGE=!!(Je.rolle&&Je.rolle!=="deckblatt")&&!!K.folgeFamilie;\n'
 'const FAM=ix=>FOLGE?K.folgeFamilie:(ix===0?K.schriftart:(K.unterSchrift||K.schriftart));',
 "Textkachel in der Fassung marke folgt der Rolle der Folie", 1))

# 90 — Die Wortmarke in Orange-Rosa, und der Text der Folgefolien
#      geht nach unten.
#
#      **Die Farbe.** Die Wortmarke war weiss auf dem Foto und
#      Textfarbe auf der Textkachel — zwei Farben fuer dieselbe Marke,
#      und keine davon die Akzentfarbe. Jetzt steht sie im Block:
#
#        nameFarbe      #E8836B   derselbe Ton wie Saum und Schild
#        nameDeckkraft  1         voll, weil der Ton sonst wegkippt
#
#      Auf der Creme-Kachel sind das 2,4:1. Fuer Lesetext waere das zu
#      wenig; fuer eine Wortmarke, die man nicht liest sondern
#      wiedererkennt, ist es richtig — und mit .55 Deckkraft, wie
#      vorher, waere sie fast verschwunden. Auf dem Foto steht sie
#      ueber dem Kantenverlauf unten und traegt.
#
#      **Die Textlage.** Die Lage wuerfelt aus dem Bildnamen zwischen
#      oben, mitte und unten. Der Schutz davor, dass der Text auf
#      einem Gesicht landet, fragte t._autoImage.faceZones — und das
#      gibt es nur, wenn das Bild durch die automatische Zuweisung
#      gelaufen ist. Eine Folgefolie, die das Bild des Deckblatts
#      erbt, hat es NICHT. Dort hiess "keine Gesichtszonen bekannt"
#      bisher "also kein Gesicht im Weg", und der Text landete oben
#      im Gesicht.
#
#      Zwei Aenderungen:
#
#        1. folgeLage "unten" — die Folgefolien wuerfeln gar nicht
#           mehr, der Text steht unten. Leerer Wert schaltet das
#           Wuerfeln dort wieder ein.
#        2. "oben" wird nur noch genommen, wenn die Gesichtszonen
#           WIRKLICH bekannt sind (Array vorhanden). Ist nichts
#           bekannt, faellt es auf unten zurueck. Unbekannt heisst
#           jetzt vorsichtig statt sorglos.
#
#      Nachgerechnet, nicht geraten: die Lage-Funktion aus dem
#      gebauten Bundle in node laufen lassen, neun Bildnamen, drei
#      Wissensstaende. Ergebnis fuer die Namen, die "oben" wuerfeln:
#      ohne Analyse -> unten, Analyse ohne Gesicht -> oben, Gesicht
#      oben -> unten. Folgefolien in allen Faellen unten.
#
#      Nicht angefasst: "mitte" ohne Analyse bleibt "mitte". Auf dem
#      Deckblatt gibt es die Analyse praktisch immer, und die
#      Folgefolien stehen jetzt ohnehin unten.
P.append(('fill:`rgba(255,255,255,${BS_KACHEL.nameDeckkraft||.55})`,selectable:!1})),Le()',
 'fill:BS_KACHEL.nameFarbe||"#FFFFFF",opacity:(BS_KACHEL.nameDeckkraft||.55),'
 'selectable:!1})),Le()',
 "Wortmarke der Fotokachel in der Blockfarbe", 1))
P.append(('fill:SCH,opacity:(K.nameDeckkraft||.55),maxB:MAXB});',
 'fill:K.nameFarbe||SCH,opacity:(K.nameDeckkraft||.55),maxB:MAXB});',
 "Wortmarke der Textkachel in der Blockfarbe", 1))
P.append(('const ve=(()=>{const zA=(tt.fettNurErste&&!t._blurAn&&t.textAnchor&&t.textAnchor.row&&{top:"oben",mid:"mitte",bottom:"unten"}[t.textAnchor.row])||"";if(t.textLage)return t.textLage;if(!BS_KACHEL.lagenWechsel)return zA||($e?"unten":"mitte");const zs=String(t.background||t.text||"");let zh=0;for(let zi=0;zi<zs.length;zi++)zh=(zh*31+zs.charCodeAt(zi))%99991;const zL=["unten","mitte","oben"][zh%3];const zG=(!t._blurAn&&t._autoImage&&t._autoImage.faceZones)||[];const zR={oben:0,mitte:1,unten:2}[zL];return zG.some(zz=>Math.floor(zz/3)===zR)?(zA||($e?"unten":"mitte")):zL})()',
 'const ve=(()=>{const zA=(tt.fettNurErste&&!t._blurAn&&t.textAnchor&&t.textAnchor.row&&{top:"oben",mid:"mitte",bottom:"unten"}[t.textAnchor.row])||"";'
 'if(t.textLage)return t.textLage;'
 'const zAus=zA||($e?"unten":"mitte");'
 'if(t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeLage)return BS_KACHEL.folgeLage;'
 'if(!BS_KACHEL.lagenWechsel)return zAus;'
 'const zs=String(t.background||t.text||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi++)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'const zL=["unten","mitte","oben"][zh%3];'
 'const zW=!t._blurAn&&t._autoImage&&Array.isArray(t._autoImage.faceZones);'
 'if(zL==="oben"&&!zW)return zAus;'
 'const zG=(zW&&t._autoImage.faceZones)||[];'
 'const zR={oben:0,mitte:1,unten:2}[zL];'
 'return zG.some(zz=>Math.floor(zz/3)===zR)?zAus:zL})()',
 "Oben nur, wenn die Gesichtszonen wirklich bekannt sind", 1))

# 91 — Die Textkachel ab Folie 2: so gross wie am Foto, linksbuendig.
#
#      Die Textkachel setzte immer aus denselben zwei Zahlen:
#      groesseAnteil .098 als Startgroesse und maxhoehe .90 als
#      Deckel. Auf einer Folgefolie ist das zu laut — die Fotokachel
#      arbeitet mit einem viel engeren Deckel (textHoehe .70) und
#      setzt ihren Fliesztext kleiner.
#
#      Gemessen, nicht geschaetzt. Zeilenabstand aus dem Bild geholt
#      und durch zeile beziehungsweise fotoZeile geteilt:
#
#        Fotokachel Ueberschrift   ~80 px auf 800 Breite
#        Fotokachel Fliesztext     ~60 px   (qe * zweitAnteil .75)
#        Textkachel bisher         ~78 px
#        Textkachel mit .070       ~56 px
#
#      Der Fliesztext der Fotokachel ist Helvetica, der der
#      Folgefolie Montserrat, und Montserrat traegt bei gleicher
#      Pixelzahl optisch dicker auf. Deshalb .070 (56 px) und nicht
#      .075 (60 px): gerechnet gleich gross waere es einen Tick zu
#      gross gewesen.
#
#        folgeGroesseAnteil  .049    Startgroesse ab Folie 2
#        folgeMaxhoehe       .70     derselbe Deckel wie am Foto
#        folgeAusrichtung    links   statt mittig
#
#      Alle drei greifen nur, wenn die Folie eine Rolle hat und die
#      nicht "deckblatt" ist — dieselbe Weiche wie bei der Schrift in
#      Eintrag 89. Folie 1 bleibt unangetastet.
#
#      Die Wortmarke rueckt mit nach links. Sie sitzt am selben Rand
#      wie der Text (r*rand), nicht an einem eigenen — sonst haette
#      die Kachel zwei linke Kanten.
#      Nachtrag: .070 war Carina noch zu gross, sie wollte 30 Prozent
#      weniger. .070 * 0.7 = .049. Nachgemessen am gebauten Bundle
#      ueber den Zeilenabstand: 57 px vorher, 40 px nachher, also
#      Faktor 0.70 — die 30 Prozent sind wirklich 30 Prozent und
#      nicht nur eine kleinere Zahl im Block. Der Fliesztext ist damit
#      deutlich kleiner als am Foto; das ist Absicht, eine Folgefolie
#      soll ruhiger sein als das Deckblatt.
#
P.append(('let gr=r*(K.groesseAnteil||.098),ZL=[];',
 'const LI=FOLGE&&K.folgeAusrichtung==="links",'
 'GA=(FOLGE&&K.folgeGroesseAnteil)||K.groesseAnteil||.098,'
 'MH=(FOLGE&&K.folgeMaxhoehe)||K.maxhoehe;'
 'let gr=r*GA,ZL=[];',
 "Folgetextkachel: eigene Startgroesse, Hoehe und Ausrichtung", 1))
P.append(('if(m.h<=n*K.maxhoehe&&breiteste(m.z,gr)<=MESS)break;gr*=.95}',
 'if(m.h<=n*MH&&breiteste(m.z,gr)<=MESS)break;gr*=.95}',
 "Anpassungslauf nimmt die Hoehe der Folgetextkachel", 1))
P.append(('blk.forEach(z=>{txt(z,{left:r/2,top:y,originX:"center",originY:"center",',
 'blk.forEach(z=>{txt(z,{left:LI?r*K.rand:r/2,top:y,originX:LI?"left":"center",originY:"center",',
 "Folgetextkachel linksbuendig", 1))
P.append(('if(NA)txt(NA,{left:r/2,top:n*(K.nameUnten||.945),originX:"center",originY:"center",',
 'if(NA)txt(NA,{left:LI?r*K.rand:r/2,top:n*(K.nameUnten||.945),originX:LI?"left":"center",originY:"center",',
 "Wortmarke folgt der Ausrichtung der Kachel", 1))

# 92 — Die Wortmarke fett und in der Laufweite der Marke.
#
#      Sie stand in 400 mit charSpacing 150, also +0,15 em gesperrt.
#      Das war ein Rest aus der Bau-Session und passte zu nichts:
#      der ganze uebrige Satz laeuft auf laufweite -50, also -0,05 em
#      eng. Zwei Zeilen weit auseinander unter einem engen Satz.
#
#        nameGewicht    700    fett wie der betonte Block
#        nameLaufweite  -50    dieselbe Enge wie der Rest
#
#      Die 150 stand an beiden Zeichenstellen hart im Code. Sie kommt
#      jetzt aus dem Block, und der Vergleich ist ==null und nicht
#      ||150 — sonst waere eine Laufweite von 0 stillschweigend zu
#      150 geworden.
P.append(('fontWeight:(BS_KACHEL.nameGewicht||"400"),charSpacing:150,fill:BS_KACHEL.nameFarbe',
 'fontWeight:(BS_KACHEL.nameGewicht||"400"),'
 'charSpacing:(BS_KACHEL.nameLaufweite==null?150:BS_KACHEL.nameLaufweite),'
 'fill:BS_KACHEL.nameFarbe',
 "Laufweite der Wortmarke auf dem Foto aus dem Block", 1))
P.append(('fontWeight:(K.nameGewicht||"400"),charSpacing:150,\nfill:K.nameFarbe||SCH',
 'fontWeight:(K.nameGewicht||"400"),'
 'charSpacing:(K.nameLaufweite==null?150:K.nameLaufweite),\nfill:K.nameFarbe||SCH',
 "Laufweite der Wortmarke auf der Textkachel aus dem Block", 1))

# 93 — Der Zwilling: ein Bundle, zwei Feeds.
#
#      Carina moechte den Stil eines anderen Accounts ausprobieren,
#      ohne ihren eigenen Feed dafuer aufzugeben. Weil ALLES aus
#      einem flachen Objekt liest, kostet das keinen zweiten Zeichner
#      und keine zweite App:
#
#        site/index.html          setzt nichts       -> Grundstil
#        site/dunkel/index.html   window.BS_STIL     -> Aufsatz
#
#      Der Schalter steht als gewoehnliches <script> VOR dem Modul,
#      weil Module verzoegert ausgefuehrt werden — sonst laege der
#      Wert noch nicht vor, wenn der Block angelegt wird.
#
#      Und er MERKT sich die Wahl. Die App setzt ihre eigenen
#      Adressen (/content-planner und so weiter, React Router ohne
#      basename) und verliert dabei das "/dunkel" aus dem Pfad. Ohne
#      das Merken waere der Zwilling nach dem ersten Klick und einem
#      Neuladen wieder hell. Regel: /dunkel/... schaltet dunkel und
#      merkt es, / schaltet zurueck, alles andere behaelt das
#      Gemerkte. Durchgerechnet fuer sechs Faelle in node.
#
#      Die Seite im Unterordner laedt dieselben Dateien ueber
#      ABSOLUTE Pfade (/assets/, /fonts/), sonst suchte sie unter
#      /dunkel/assets/. Und in netlify.toml und _redirects steht die
#      Regel fuer /dunkel/* VOR der Sammelregel /* — sonst schluckt
#      die den Zwilling.
#
#      IndexedDB haengt an der Domain und nicht am Pfad: beide Feeds
#      sehen denselben Plan und dieselben Bilder. Das ist Absicht —
#      derselbe Inhalt in zwei Anzuegen.
#
#      Die Form von BS_KACHEL bleibt ein Objektliteral, damit
#      kachel-pruefen.py den Block weiter herausschneiden kann. Der
#      Aufsatz kommt davor, der Schalter dahinter.
#
#      Drei Werte konnten den Aufsatz noch nicht bedienen und stehen
#      jetzt auch im Block:
#
#        bildSaettigung   die App HOB die Saettigung um .3; fuer den
#                         fast schwarzweissen Look muss sie unter
#                         null. Die Bedingung war Ze>0 und liesz
#                         negative Werte stillschweigend fallen.
#        bildHeben        die milchige Aufhellung um .13
#        fotoAusrichtung  mittig statt links, an EINER Stelle gesetzt
#                         statt an sechs Vergleichen geaendert
P.append(('const De=typeof t.hellBoost=="number"?t.hellBoost:.13,Ze=typeof t.satBoost=="number"?t.satBoost:.3;Ze>0&&',
 'const De=typeof BS_KACHEL.bildHeben=="number"?BS_KACHEL.bildHeben:(typeof t.hellBoost=="number"?t.hellBoost:.13),'
 'Ze=typeof BS_KACHEL.bildSaettigung=="number"?BS_KACHEL.bildSaettigung:(typeof t.satBoost=="number"?t.satBoost:.3);Ze!==0&&',
 "Saettigung und Aufhellung des Bildes aus dem Block", 1))
P.append(('$e&&(tt.nurErsteZeilePlatte=!0,tt.fettNurErste=!0,BS_KACHEL.fotoSchriftFarbe&&(tt.schriftFarbe=BS_KACHEL.fotoSchriftFarbe)',
 '$e&&(tt.nurErsteZeilePlatte=!0,tt.fettNurErste=!0,'
 'BS_KACHEL.fotoAusrichtung&&(tt.ausrichtung=BS_KACHEL.fotoAusrichtung),'
 'BS_KACHEL.fotoSchriftFarbe&&(tt.schriftFarbe=BS_KACHEL.fotoSchriftFarbe)',
 "Ausrichtung der Fotokachel aus dem Block", 1))

# 95 — Die geteilte Kachel, und der Aufsatz war loechrig.
#
#      **Loechrig.** Der Aufsatz aus Eintrag 93 hat nur die
#      Fotokachel umgestellt. Die Textkacheln, die Folgefolien und
#      der Ablauf lasen weiter schriftart, unterSchrift, folgeFamilie
#      und ablaufTitel — und die standen im Grundstil auf Montserrat.
#      Im dunklen Feed stand also die Haelfte in Grotesk. Alle vier
#      stehen jetzt im Aufsatz, dazu die Wortmarke (Serife, nicht
#      fett, wieder gesperrt statt eng — sie ist hier ein leiser
#      Absender und kein Akzent).
#
#      textAnteil 67 -> 8. Im Vorbild ist praktisch jede Kachel ein
#      Foto; 67 hiess zwei Drittel Textkacheln. Der Grundstil behaelt
#      seine 67.
#
#      **Die Teilung.** Im Vorbild steht die Frage oben in der Serife
#      und die Antwort unten in der Handschrift, dazwischen atmet das
#      Bild. Bisher flossen beide Bloecke als einer: eine Hoehe, eine
#      Lage, alles zusammen.
#
#      Der Zeichner kennt die Grenze laengst — Lt ist die Zahl der
#      Zeilen des ersten Blocks, danach wird kleiner und leichter
#      gesetzt. Es fehlte nur, De an dieser Grenze neu zu setzen:
#
#        rt === 0    ->  oben bei geteiltOben
#        rt === Lt   ->  so weit unten, dass der zweite Block genau
#                        auf textUnten endet
#
#      Zwei Zeilen in der Zeichenschleife, kein zweiter Weg. Sie
#      greifen nur, wenn geteilt gesetzt ist UND es eine Fotokachel
#      mit zwei Bloecken ist — der Grundstil merkt nichts davon.
P.append(('dr.forEach((Je,rt)=>{if(!Je.length){De+=tt.engZeilen?qe*.92:Et;return}',
 'const zGT=!!BS_KACHEL.geteilt&&$e&&tt.nurErsteZeilePlatte===!0&&Lt>0&&dr.length>Lt;'
 'dr.forEach((Je,rt)=>{'
 'if(zGT&&rt===0)De=n*(BS_KACHEL.geteiltOben||.16)+Et/2;'
 'if(zGT&&rt===Lt)De=n*(BS_KACHEL.textUnten||.86)-(dr.length-Lt)*Et2*zF+Et2/2;'
 'if(!Je.length){De+=tt.engZeilen?qe*.92:Et;return}',
 "Geteilte Kachel: erster Block oben, zweiter unten", 1))

# 96 — Gesperrter Versalsatz, und drei Wuerfel, damit die Fotos
#      reichen.
#
#      Wenn fast jede Kachel ein Foto ist, sieht man dasselbe Bild
#      alle paar Tage wieder. Drei Dinge wechseln jetzt je Kachel.
#      Alle drei wuerfeln aus BILD **und** TEXT:
#
#          String(t.background) + "|" + String(t.text)
#
#      Nicht nur aus dem Bild — sonst bekaeme dasselbe Foto an jedem
#      Tag denselben Ausschnitt und denselben Ton, und der ganze
#      Aufwand waere umsonst. Nachgerechnet: dasselbe Foto mit vier
#      Texten ergibt vier verschiedene Ausschnitte und Toene.
#
#      **1. Der Ausschnitt.** Den Wechsel gab es laengst — Ye kennt
#      full, wide, bust, lower, close, face mit Zoom 1 bis 2,3, und
#      et dreht ihn durch. Nur war er an den FOLIENINDEX gebunden und
#      das Deckblatt stand hart auf "full": Zoom 1, mittig, immer.
#      Deshalb sah im Raster jede Kachel gleich gerahmt aus.
#      deckblattSchnitte gibt dem Deckblatt eine eigene Reihe.
#      Absichtlich ohne face und close (Zoom 1,85 bis 2,3) — das ist
#      fuer eine Kachel im Raster zu nah.
#      Ein von Hand gesetzter Ausschnitt (imageLocked) gewinnt
#      weiterhin, daran wurde nichts geaendert.
#
#      **2. Der Ton.** tonReihe gibt vier fast schwarze Toene, warm
#      bis kuehl bis violett. Der gewuerfelte Ton geht in alle drei
#      Ebenen ueber dem Bild: flaches Abdunkeln, Kantenverlauf,
#      Tiefenverlauf. Er wird EINMAL oben in der Kachel bestimmt,
#      damit die drei Ebenen nicht auseinanderlaufen.
#
#      **3. Der Versalsatz.** versalAnteil Prozent der Fotokacheln
#      werden zu Grossbuchstaben in Montserrat 500, weit gesperrt und
#      klein — die Reel-Cover im Vorbild.
#
#      Dabei fehlte etwas Grundsaetzliches: der Zeichner konnte gar
#      keine Laufweite auf dem Foto. charSpacing stand weder beim
#      Zeichnen noch beim Messen. Es reicht nicht, es beim Zeichnen
#      zu setzen — dann bricht der Umbruch zu spaet um und der Text
#      laeuft raus. Deshalb steht es jetzt an vier Stellen:
#
#          Ht    misst die Zeilenbreite  -> davon haengt der Umbruch
#          Tt    zeichnet die Zeile
#          zF    die Notbremse
#          PB    die Plattenbreite
#
#      Verteilung ueber dreissig Bilder nachgerechnet: 9 von 30
#      Versalsatz (30 Prozent), Ausschnitte 11/10/9, Toene 8/8/6/8.
P.append(('Ca=async(e,t,r,n,i={})=>{var yn,_n,Jr,xr,zr,ti,nn,_i,ki,ri;try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}',
 'Ca=async(e,t,r,n,i={})=>{var yn,_n,Jr,xr,zr,ti,nn,_i,ki,ri;try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}'
 'const zTon=(()=>{try{const zl=String(BS_KACHEL.tonReihe||"").split("|").filter(Boolean);'
 'if(!zl.length)return BS_KACHEL.bildTon;'
 'const zs=String(t.background||"")+"|"+String(t.text||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'return zl[(zh*13+7)%zl.length]}catch(zz){return BS_KACHEL.bildTon}})();',
 "Farbton je Kachel aus der tonReihe", 1))
P.append(('fill:`rgba(${BS_KACHEL.bildTon||"0,0,0"},${Et})`', 'fill:`rgba(${zTon||"0,0,0"},${Et})`',
 "Flaches Abdunkeln im Ton der Kachel", 1))
P.append(('lt=Ye[Qe===0?"full":et[Qe%et.length]]',
 'zDS=(()=>{try{const zl=String(BS_KACHEL.deckblattSchnitte||"").split("|").filter(Boolean);'
 'if(!zl.length)return"full";'
 'const zs=String(t.background||"")+"|"+String(t.text||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'return zl[(zh*5+3)%zl.length]}catch(zz){return"full"}})(),'
 'lt=Ye[Qe===0?zDS:et[Qe%et.length]]',
 "Deckblatt bekommt wechselnde Bildausschnitte", 1))
P.append(('$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeGewicht&&(kt=BS_KACHEL.folgeGewicht);const br=(Je,rt)=>{',
 '$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeGewicht&&(kt=BS_KACHEL.folgeGewicht);'
 'const zVS=(()=>{try{if(!$e||!BS_KACHEL.versalAnteil)return!1;'
 'const zs=String(t.background||"")+"|"+String(t.text||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'return((zh*7+11)%100)<BS_KACHEL.versalAnteil}catch(zz){return!1}})();'
 'const zCS=zVS?(BS_KACHEL.versalLaufweite||0):(BS_KACHEL.fotoLaufweite||0);'
 'zVS&&BS_KACHEL.versalFamilie&&(Qe=BS_KACHEL.versalFamilie);'
 'zVS&&BS_KACHEL.versalGewicht&&(kt=BS_KACHEL.versalGewicht);'
 'const br=(Je,rt)=>{',
 "Versalsatz: Entscheidung, Schrift, Gewicht, Laufweite", 1))
P.append(('Ht=(Je,rt,Ve)=>{const pt={fontSize:rt,fontFamily:Ve?Qe:(BS_KACHEL.zweiteFamilie||Qe),fontWeight:Ve?kt:"400"};',
 'Ht=(Je,rt,Ve)=>{const pt={fontSize:rt,fontFamily:Ve?Qe:((zVS&&BS_KACHEL.versalFamilie)||BS_KACHEL.zweiteFamilie||Qe),fontWeight:Ve?kt:"400",charSpacing:zCS};',
 "Laufweite beim Messen der Zeilen", 1))
P.append(('const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,',
 'const Tt=(xt,rr,Ut)=>new Pe.fabric.Text(xt,{left:Ut,top:De,originX:"left",originY:"center",charSpacing:zCS,fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,',
 "Laufweite beim Zeichnen der Zeile", 1))
P.append(('const zp=new Pe.fabric.Text(zz.map(zx=>zx.w).join(" "),{fontSize:zie?qe:qe2,fontFamily:zie?Qe:QeZ,',
 'const zp=new Pe.fabric.Text(zz.map(zx=>zx.w).join(" "),{charSpacing:zCS,fontSize:zie?qe:qe2,fontFamily:zie?Qe:QeZ,',
 "Laufweite in der Notbremse", 1))
P.append(('const p2=new Pe.fabric.Text(zz.map(xx=>xx.w).join(" "),{fontSize:qe,fontFamily:Qe,fontWeight:kt});',
 'const p2=new Pe.fabric.Text(zz.map(xx=>xx.w).join(" "),{charSpacing:zCS,fontSize:qe,fontFamily:Qe,fontWeight:kt});',
 "Laufweite bei der Plattenbreite", 1))
P.append(('QeZ=$e?((t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie)||BS_KACHEL.zweiteFamilie||Qe):Qe',
 'QeZ=$e?((zVS&&BS_KACHEL.versalFamilie)||(t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie)||BS_KACHEL.zweiteFamilie||Qe):Qe',
 "Zweiter Block folgt dem Versalsatz", 1))
P.append(('const SR=$e&&String(t.schild||"").trim()?r*((BS_KACHEL.schildGroesse||.03)*(BS_KACHEL.schildHoehe||2)+(BS_KACHEL.schildAbstand||.034)):0;',
 'const SR=$e&&String(t.schild||"").trim()?r*((BS_KACHEL.schildGroesse||.03)*(BS_KACHEL.schildHoehe||2)+(BS_KACHEL.schildAbstand||.034)):0;'
 'if(zVS){er=String(er||"").toUpperCase();pr=String(pr||"").toUpperCase();'
 'BS_KACHEL.versalGroesse&&(qe=Math.max(c(11),Math.round(r*BS_KACHEL.versalGroesse)))}',
 "Versalsatz: Grossbuchstaben und feste Groesse", 1))

# 97 — Ganz schwarzweiss, und die Schriften ausgemessen statt
#      geraten.
#
#      **Schwarzweiss.** bildSaettigung -.55 -> -1. Allein bringt das
#      aber ein flaues Grau, und flaues Grau sieht alt aus. Was jung
#      wirkt, ist nicht das Fehlen von Farbe, sondern die Tiefe:
#      richtige Schwarzwerte und saubere Lichter. Deshalb kommt
#      bildSpreizung dazu.
#
#      Die App hatte einen Kontrastwert (contrastBoost .07), aber nur
#      als Vorgabe je Kachel und nicht im Block — dieselbe Luecke wie
#      bei der Saettigung. Und dieselbe Falle: die Bedingung war
#      He>0, ein negativer Wert waere stillschweigend gefallen.
#      Jetzt He!==0.
#
#        bildSaettigung  -1     ganz schwarzweiss
#        bildSpreizung   .28    statt .07 — dafuer die Tiefe
#
#      Vier Fassungen am selben Foto angesehen: -.55/.07 (bisher),
#      -1/.07 (flau und grau), -1/.28 (Tiefe, klar), -1/.28 kuehl.
#      Genommen wurde -1/.28.
#
#      **Die Schriften.** Playfair und Caveat waren Platzhalter und
#      Carina hat sie abgelehnt. Sechs Paarungen am selben Foto
#      gerendert. Wichtig dabei, weil es in diesem Projekt schon
#      dreimal danebengegangen ist: die Schriften wurden NACHGEMESSEN
#      und nicht angeschaut. Derselbe Satz in 40 px:
#
#          Playfair Display    323,6      Cormorant Garamond  278,9
#          Prata               347,5      Marcellus           319,4
#          Bodoni Moda         333,2      Italiana            298,3
#
#      Sechs verschiedene Breiten, also sechs wirklich geladene
#      Schriften. Die drei in der oberen Reihe SEHEN sich aehnlich,
#      weil sie alle Didone-Serifen sind — das ist kein Ladefehler.
#
#      Genommen: Prata fuer die Serife, Shadows Into Light fuer die
#      Handschrift. Prata ist geometrischer und weniger verspielt als
#      Playfair, Shadows Into Light ist ein feiner Stift statt eines
#      Filzstifts. Die anderen fuenf Paarungen sind einen Wert
#      entfernt.
#
#      Shadows Into Light liegt als Datei im Projekt. Und die
#      Ladeliste der App zog bisher nur sechs Werte aus dem Block —
#      zweiteFamilie, nameSchrift, versalFamilie und ablaufTitel
#      fehlten. Bei einem Zeichner, der auf dem Canvas misst, heisst
#      das: mit der Ersatzschrift gemessen, mit der richtigen
#      gezeichnet. Alle vier stehen jetzt drin.
P.append(('const He=typeof t.contrastBoost=="number"?t.contrastBoost:.07;He>0&&',
 'const He=typeof BS_KACHEL.bildSpreizung=="number"?BS_KACHEL.bildSpreizung:(typeof t.contrastBoost=="number"?t.contrastBoost:.07);He!==0&&',
 "Kontrast des Bildes aus dem Block", 1))
P.append(('BS_KACHEL.schriftart,BS_KACHEL.unterSchrift,BS_KACHEL.deckblattFamilie,BS_KACHEL.folgeFamilie,BS_KACHEL.fotoSchrift,BS_KACHEL.schildSchrift',
 'BS_KACHEL.schriftart,BS_KACHEL.unterSchrift,BS_KACHEL.deckblattFamilie,BS_KACHEL.folgeFamilie,BS_KACHEL.fotoSchrift,BS_KACHEL.schildSchrift,'
 'BS_KACHEL.zweiteFamilie,BS_KACHEL.nameSchrift,BS_KACHEL.versalFamilie,BS_KACHEL.ablaufTitel',
 "Vier weitere Schriften des Blocks vorladen", 1))

# 98 — DM Serif Display, und ein vorbereiteter Platz fuer Nohemi.
#
#      **DM Serif Display** loest Prata ab (das wiederum Playfair
#      abgeloest hatte). Nachgemessen wie immer, derselbe Satz in
#      40 px: DM Serif Display 312,8 — Prata 347,5 — Playfair 323,6.
#      Drei Breiten, drei wirklich geladene Schriften. DM Serif
#      Display ist deutlich fetter und kompakter als die beiden
#      anderen, es traegt also mehr Text auf gleicher Breite.
#      Regular und Kursiv liegen im Projekt.
#
#      **Nohemi** liegt NICHT im Projekt. Sie ist von Pangram Pangram
#      und fuer den kommerziellen Gebrauch kostenpflichtig; ich kann
#      sie nicht mitliefern, ohne Carinas Lizenz zu unterlaufen. Was
#      geht, ist alles andere vorzubereiten: die vier Anmeldungen
#      (300/400/500/700) stehen in beiden Seiten, tiefeSchriften
#      kennt den Namen. Sobald die lizenzierten Dateien unter
#
#          site/fonts/Nohemi-Light.woff2
#          site/fonts/Nohemi-Regular.woff2
#          site/fonts/Nohemi-Medium.woff2
#          site/fonts/Nohemi-Bold.woff2
#
#      liegen, reicht "Nohemi" als Wert im Block. Fehlt eine Datei,
#      laeuft alles unveraendert weiter — eine @font-face-Regel ohne
#      Datei tut nichts.

# 99 — Der zweite Block rueckt nach oben.
#
#      Die geteilte Kachel aus Eintrag 95 setzte den zweiten Block auf
#      textUnten, also .86 — die Unterkante, die fuer einen
#      DURCHLAUFENDEN Text gedacht ist. Geteilt heisst das: Serife
#      ganz oben, Handschrift ganz unten, dazwischen ein halbes Bild
#      Luft. Zu weit.
#
#      Der zweite Block bekommt eine eigene Unterkante. Vier Werte am
#      selben Foto angesehen: .86 (bisher, weit auseinander), .72
#      (immer noch weit), .62 (zwei Bloecke, die zusammengehoeren),
#      .54 (klebt und liegt im Gesicht). Genommen: .62.
#
#        geteiltUnten  .62
#
#      Faellt der Wert weg, gilt wieder textUnten — die Teilung
#      funktioniert also weiter, auch wenn ihn jemand loescht.

# 100 — Der zweite Block sass links, weil er in der falschen Groesse
#       gemessen wurde.
#
#       Carina: "es ist links lastig". Auf den Kacheln, wo der zweite
#       Block laenger war, lief die Handschrift links aus dem Bild.
#
#       Die Zeile wird mittig gesetzt ueber
#
#           Vt = r/2 - ct/2
#
#       und ct kam aus Math.max(pt.width, Ht(Je, qe, ...)). pt misst
#       richtig, naemlich mit (Ve?qe:qe2)*zF. Ht wurde aber IMMER mit
#       qe gerufen — der Groesse des ERSTEN Blocks. Der zweite Block
#       wird in zweitAnteil gezeichnet, also in 62 Prozent, und in
#       100 Prozent gemessen. Math.max nimmt dann die zu grosse Zahl.
#
#           gemessene Breite  = 1/0,62 = 1,61 x die echte
#           Versatz nach links = (1,61-1)/2 = 31 % der Zeilenbreite
#
#       Bei einer 300 px breiten Zeile sind das 92 px auf einer
#       Kachel von 800 px. Genau das Bild aus dem Screenshot.
#
#       Warum es im warmen Feed nie aufgefallen ist: dort steht die
#       Fotokachel auf ausrichtung "links", und dann gilt Vt = _e —
#       ct spielt gar keine Rolle. Der Fehler war die ganze Zeit da,
#       er brauchte nur eine mittig gesetzte Kachel, um sichtbar zu
#       werden.
#
#       Dabei bekommt pt auch die Laufweite, die ihm seit dem
#       Versalsatz fehlte. Sie war bisher nur in Ht, und Math.max hat
#       das gedeckt — aber zwei Messungen desselben Textes, die
#       verschiedene Dinge messen, sind eine Falle und keine
#       Absicherung.
P.append(('pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,fontWeight:tt.fettNurErste&&!Ve?(BS_KACHEL.leichtGewicht||"400"):kt}),ct=Math.max(pt.width,Ht(Je,qe,!(tt.fettNurErste&&!Ve)))',
 'pt=new Pe.fabric.Text(Je.map(xt=>xt.w).join(" "),{charSpacing:zCS,fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,fontWeight:tt.fettNurErste&&!Ve?(BS_KACHEL.leichtGewicht||"400"):kt}),ct=Math.max(pt.width,Ht(Je,(Ve?qe:qe2)*zF,!(tt.fettNurErste&&!Ve)))',
 "Die Zeile wird in ihrer eigenen Groesse gemessen", 1))

# 101 — Der Abstand haengt am ersten Block, und die Versalien sind
#       am Vorbild ausgemessen.
#
#       **Der Abstand.** geteiltUnten .62 war immer noch eine FESTE
#       Unterkante. Bei einer kurzen Ueberschrift wie "Ich
#       manifestiere." steht der erste Block bei .16 und der zweite
#       bei .62 — dazwischen ein halbes Bild Luft, ganz gleich wie
#       kurz die Ueberschrift ist. Der Abstand darf nicht von der
#       Kachel abhaengen, sondern vom ersten Block.
#
#       geteiltLuft .05 setzt den zweiten Block genau so weit unter
#       den ersten. geteiltUnten bleibt als Deckel: passt beides
#       zusammen nicht mehr, gewinnt die Unterkante.
#
#       **Die Versalien.** Carina fragt, ob sie gegenueber dem
#       Vorbild zu klein sind. Sie sind es. Nachgemessen im
#       Screenshot des Vorbilds: das Raster hat Rinnen bei x=400/803
#       und y=1025/1561/2097, eine Kachel ist also 400 breit. Die
#       Versalzeilen der Reel-Kachel sind 16 bis 17 Pixel hoch:
#
#           Versalhoehe im Vorbild   17/400  = 0,043 der Breite
#           Versalhoehe bei uns      19/800  = 0,024 der Breite
#
#       Also gut vierzig Prozent zu klein. Die Versalhoehe von
#       Montserrat ist rund 0,70 der Schriftgroesse, gebraucht wird
#       also 0,043/0,70 = 0,061.
#
#           versalGroesse  .034  ->  .060
#
#       Gegengemessen an der eigenen Kachel: 34 Pixel auf 800 Breite
#       = 0,043. Dieselbe Zahl wie im Vorbild.
#
#       Nebenbei aus derselben Messung, fuer spaeter: die Serifenzeile
#       im Vorbild ist 28 bis 29 Pixel hoch, also 0,071 der Breite.
P.append(('if(zGT&&rt===Lt)De=n*(BS_KACHEL.geteiltUnten||BS_KACHEL.textUnten||.86)-(dr.length-Lt)*Et2*zF+Et2/2;',
 'if(zGT&&rt===Lt){const zU=n*(BS_KACHEL.geteiltUnten||BS_KACHEL.textUnten||.86)-(dr.length-Lt)*Et2*zF+Et2/2;'
 'De=BS_KACHEL.geteiltLuft?Math.max(De,Math.min(De+n*BS_KACHEL.geteiltLuft,zU)):zU;}',
 "Der zweite Block haengt am ersten statt an der Unterkante", 1))

# 102 — Die Versalien waren die falsche Schrift. Nicht zu klein,
#       sondern grundsaetzlich falsch.
#
#       Ich hatte den gesperrten Versalsatz als GROTESK gebaut:
#       Montserrat 500 mit Laufweite 280. Carina: "Das passt null
#       dazu, zeig das Vorbild fuer Versalien." Also die vier
#       Versalkacheln aus ihrem Screenshot herausgeschnitten und
#       angesehen — was ich haette tun sollen, BEVOR ich etwas baue.
#
#       Im Vorbild sind die Versalien keine Grotesk, sondern
#       DIESELBE HANDSCHRIFT wie auf den anderen Kacheln, nur in
#       Grossbuchstaben. Handgezeichnet, leicht schraeg, ungleiche
#       Striche, kaum gesperrt. Der gesperrte Groteskblock ist das
#       Gegenteil davon: technisch, gleichmaessig, weit auseinander.
#
#       Die Groessenmessung aus Eintrag 101 bleibt richtig — 0,043
#       der Kachelbreite. Sie war nur an der falschen Schrift
#       gemessen. Nachgerechnet fuer die Kandidaten: alle vier haben
#       eine Versalhoehe von rund 0,72 der Schriftgroesse, also
#       bleibt versalGroesse .060.
#
#           versalFamilie     Montserrat -> Kalam
#           versalGewicht     500 -> 400
#           versalLaufweite   280 -> 20      (fast keine)
#           versalZweitAnteil 1               (beide Bloecke gleich gross)
#
#       versalZweitAnteil ist neu: im Vorbild sind der obere und der
#       untere Block GLEICH gross, waehrend sonst zweitAnteil den
#       zweiten Block verkleinert.
#
#       Sechs Handschriften am selben Foto verglichen (Montserrat
#       gesperrt, Caveat 700, Kalam, Gloria Hallelujah, Architects
#       Daughter, Shadows Into Light), alle auf dieselbe Versalhoehe
#       gerechnet. Kalam kommt dem Vorbild am naechsten: gleicher
#       Schraegstand, gleiche Strichstaerke.
P.append(('qe2=$e?Math.round(qe*(BS_KACHEL.zweitAnteil||1)):qe',
 'qe2=$e?Math.round(qe*((zVS&&BS_KACHEL.versalZweitAnteil)||BS_KACHEL.zweitAnteil||1)):qe',
 "Im Versalsatz sind beide Bloecke gleich gross", 1))

# 103 — Jede Kachel ein Bild, und die Farbe wechselt.
#
#      **Jede Kachel ein Bild.** textAnteil ist der Anteil der Tage
#      OHNE Foto. Er stand auf 8. Auf 0 darf er nicht: 0 ist falsch
#      im Sinne von JavaScript und schaltet die alte Regel wieder
#      ein (Eintrag 78). Also 1 — das trifft genau den einen Tag von
#      hundert, an dem die Reihe (pt*37+13)%100 den Wert 0 hat.
#      Praktisch: jede Kachel ein Bild.
#
#      **Der Farbwechsel.** bildSaettigung war EIN Wert fuer alle.
#      saettigungReihe macht daraus eine Reihe, gewuerfelt aus Bild
#      und Text wie Ausschnitt und Ton:
#
#          -1     schwarzweiss
#          -0.55  entzogene Farbe
#          0.1    Farbe
#
#      Die Reihe "-1|-0.55|-1|0.1|-1|-0.55" ergibt ueber 300 Kacheln
#      145 schwarzweiss, 101 entzogen, 54 Farbe — also knapp die
#      Haelfte schwarzweiss, ein Drittel entzogen, Farbe als Akzent.
#      So liegt es auch im Vorbild. Nachgerechnet ausserdem: keine
#      zwei Farbkacheln nebeneinander und keine zwei uebereinander
#      im Dreierraster.
#
#      Warum 0.1 und nicht 0 fuer "Farbe": die Bedingung am Filter
#      ist Ze!==0, eine glatte Null wuerde den Filter ueberspringen.
#      Das waere zwar dasselbe Ergebnis, aber ein Wert, der nur
#      zufaellig funktioniert. 0.1 gibt der Farbkachel ausserdem
#      etwas mehr Leben.

# 104 — Die zwei Bloecke sind ineinander gerutscht. Mein Deckel war
#       kein Deckel, sondern ein Zug nach oben.
#
#       In Eintrag 101 habe ich geschrieben: "geteiltUnten bleibt als
#       Deckel: passt beides zusammen nicht mehr, gewinnt die
#       Unterkante." Das war als Absicherung gemeint und war das
#       Gegenteil. Math.min nimmt den KLEINEREN Wert, also den weiter
#       OBEN. Sobald der erste Block lang genug war, lag die feste
#       Unterkante .62 hoeher als das Ende des ersten Blocks — und
#       der zweite Block wurde in den ersten hineingezogen.
#
#       Nachgerechnet, drei Handschriftzeilen, Kachel 1000 hoch:
#
#           Serifenzeilen   1     2     3     4     5
#           Luecke alt     70    56    37    24     8   Pixel
#           Luecke neu     70    70    67    64    62   Pixel
#
#       Die Luecke schrumpft mit jeder Zeile der Ueberschrift gegen
#       null. Bei Carinas Kachel (vier Zeilen, laengerer zweiter
#       Block) ist sie durch null durch.
#
#       Zwei Aenderungen:
#
#         1. Math.max(De, ...) davor. De ist das Ende des ersten
#            Blocks; der zweite kann nie darueber landen. Das ist
#            eine Absicherung, die diesen Namen verdient.
#         2. geteiltUnten .62 -> .86. Der Wert soll die Notbremse
#            sein und nicht die Anordnung bestimmen. Die Anordnung
#            macht geteiltLuft.
#
#       Nachgerechnet fuer eine bis sieben Serifenzeilen: die Luecke
#       liegt zwischen 60 und 70 Pixeln, die Unterkante des zweiten
#       Blocks zwischen .54 und .68 der Kachelhoehe. Nichts laeuft
#       mehr aus dem Bild und nichts ueberlappt.

# 105 — Das Kennzeichen des Vorbilds: Auszeichnung MITTEN im Satz.
#
#       Carina hat das Vorbild noch einmal geschickt. Beim Zaehlen
#       Kachel fuer Kachel: von den neun Kacheln ohne Reel sind nur
#       ZWEI geteilt. Die anderen sieben sind ein Block in der
#       unteren Haelfte — und in JEDEM dieser Saetze wechselt die
#       Schrift mitten drin:
#
#           Was definitiv KEINE Gruende sind     Handschrift
#           brauchst du KEINEN GRUND             fett
#           siehst du GANZ SCHOEN SCHEISSE aus   kursiv
#           die ERSTE Generation, NEUANFANG      kursiv und fett
#
#       Das ist das Kennzeichen dieses Feeds, und ich hatte es
#       ueberhaupt nicht. Ich habe die ganze Zeit an Anordnung und
#       Grading gearbeitet und das Offensichtliche uebersehen.
#
#       Der Zeichner kann Auszeichnung je Wort laengst — die Zeile
#       wird Wort fuer Wort gesetzt, sobald eines ausgezeichnet ist,
#       und _t kannte *kursiv*. Es fehlten zwei Auszeichnungen und
#       die Schrift je Wort:
#
#           **fett**       betontGewicht (700)
#           *kursiv*       gab es schon
#           _Handschrift_  handFamilie, sonst zweiteFamilie
#
#       handAnteil 1.15 gleicht aus, dass eine Handschrift bei
#       gleicher Pixelzahl kleiner wirkt als eine Serife.
#
#       Wichtig und leicht zu uebersehen: die Auszeichnung muss beim
#       MESSEN genauso gelten wie beim Zeichnen. Ht misst jetzt jedes
#       Wort mit seiner eigenen Schrift, seinem Schnitt und seiner
#       Groesse — sonst bricht die Zeile falsch um und sitzt nicht
#       mittig. Genau der Fehler aus Eintrag 100, nur eine Ebene
#       tiefer.
#
#       Und die Teilung wird zur Ausnahme: geteiltAnteil 25 statt
#       "immer". Im Vorbild sind es zwei von neun.
P.append((r'_t=Je=>{const rt=[];return String(Je||"").split(/(\*[^*]+\*)/).filter(Boolean).forEach(Ve=>{const pt=/^\*[^*]+\*$/.test(Ve),nr=pt?Ve.slice(1,-1):Ve;pt?nr.split(/\s+/).filter(Boolean).forEach(ct=>rt.push({w:ct,kursiv:!0})):',
 r'_t=Je=>{const rt=[];return String(Je||"").split(/(\*\*[^*]+\*\*|\*[^*]+\*|_[^_\n]+_)/).filter(Boolean).forEach(Ve=>{'
 r'const zf=/^\*\*[^*]+\*\*$/.test(Ve),zk=!zf&&/^\*[^*]+\*$/.test(Ve),zh=/^_[^_\n]+_$/.test(Ve),'
 r'pt=zf||zk||zh,nr=zf?Ve.slice(2,-2):(zk||zh)?Ve.slice(1,-1):Ve;'
 r'pt?nr.split(/\s+/).filter(Boolean).forEach(ct=>rt.push({w:ct,kursiv:zk,fett:zf,hand:zh})):',
 "Wortzerleger: **fett**, *kursiv*, _Handschrift_", 1))
P.append(('sr=Je=>Je.some(rt=>rt.kursiv),',
 'sr=Je=>Je.some(rt=>rt.kursiv||rt.fett||rt.hand),'
 'zwf=(xt,zg)=>xt&&xt.hand?(BS_KACHEL.handFamilie||BS_KACHEL.zweiteFamilie||zg):zg,'
 'zwg=(xt,zg)=>xt&&xt.fett?(BS_KACHEL.betontGewicht||"700"):zg,'
 'zws=(xt,zg)=>xt&&xt.hand?zg*(BS_KACHEL.handAnteil||1):zg,',
 "Drei kleine Helfer fuer Schrift, Schnitt und Groesse je Wort", 1))
P.append(('return Je.reduce((Vt,Tt)=>Vt+new Pe.fabric.Text(Tt.w,{...pt,fontStyle:Tt.kursiv?"italic":"normal"}).width,0)+ct*Math.max(0,Je.length-1)},',
 'return Je.reduce((Vt,Tt)=>Vt+new Pe.fabric.Text(Tt.w,{...pt,'
 'fontFamily:zwf(Tt,pt.fontFamily),fontWeight:zwg(Tt,pt.fontWeight),fontSize:zws(Tt,pt.fontSize),'
 'fontStyle:Tt.kursiv?"italic":"normal"}).width,0)+ct*Math.max(0,Je.length-1)},',
 "Jedes Wort wird mit seiner eigenen Schrift gemessen", 1))
P.append(('Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",fontSize:(Ve?qe:qe2)*zF,fontFamily:Ve?Qe:QeZ,fontWeight:tt.fettNurErste&&!Ve?(BS_KACHEL.leichtGewicht||"400"):kt,',
 'Ut=new Pe.fabric.Text(xt.w,{left:Vt,top:De,originX:"left",originY:"center",charSpacing:zCS,'
 'fontSize:zws(xt,(Ve?qe:qe2)*zF),fontFamily:zwf(xt,Ve?Qe:QeZ),'
 'fontWeight:zwg(xt,tt.fettNurErste&&!Ve?(BS_KACHEL.leichtGewicht||"400"):kt),',
 "Jedes Wort wird mit seiner eigenen Schrift gezeichnet", 1))
P.append(('const zGT=!!BS_KACHEL.geteilt&&$e&&tt.nurErsteZeilePlatte===!0&&Lt>0&&dr.length>Lt;',
 'const zGT=(BS_KACHEL.geteiltAnteil?(()=>{const zs=String(t.background||"")+"|"+String(t.text||"");let zh=0;'
 'for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 'return((zh*11+3)%100)<BS_KACHEL.geteiltAnteil})():!!BS_KACHEL.geteilt)'
 '&&$e&&tt.nurErsteZeilePlatte===!0&&Lt>0&&dr.length>Lt;',
 "Die geteilte Kachel ist nur noch ein Teil der Kacheln", 1))

# 106 — Eine Handschrift statt zwei.
#
#      Kalam war nur fuer die Versalien da; ueberall sonst — die
#      zweite Zeile, das _Wort_ mitten im Satz — steht Shadows Into
#      Light. Zwei Handschriften in einem Feed sind eine zu viel,
#      und Carina will die eine. Kalam ist raus, Datei und Anmeldung
#      geloescht.
#
#      Die Groesse musste dabei mit. Die Versalhoehe ist am Vorbild
#      auf 0,043 der Kachelbreite festgelegt (Eintrag 101), und die
#      beiden Schriften haben verschieden hohe Versalien:
#
#          Kalam                Versalhoehe 0,72 der Schriftgroesse
#          Shadows Into Light   Versalhoehe 0,67
#
#      Bei unveraendertem versalGroesse .060 waeren die Versalien
#      also 0,040 statt 0,043 herausgekommen, gut sieben Prozent zu
#      klein. 0,043/0,67 = .0642, gerundet auf .065.
#
#      Das ist der Punkt, an dem ein Schriftwechsel im Block sonst
#      still danebengeht: die Zahl gilt fuer die SCHRIFT, nicht fuer
#      das Layout. Wer versalFamilie aendert, muss versalGroesse
#      nachziehen.

# 107 — Warum jeder Tag dasselbe Bild bekam.
#
#      Carina: "nur Bilder im Wechsel wie bei Vorbild". Der Grund ist
#      eine Zeile in der Bildzuweisung.
#
#      ed(folien, bilder, r) nimmt die Bilder n[(r+d)%i] — r ist der
#      Startpunkt in der Bildreihe. Beim Aufbau des ganzen Plans lief
#      r so:
#
#          let Ze=0;
#          for (jeder Tag) { ed(Tt, He, Ze); Ze += Tt.length; }
#
#      Der Startpunkt rueckt also um die ZAHL DER FOLIEN weiter, und
#      gerechnet wird modulo der Zahl der Bilder. Ist die eine ein
#      Vielfaches der anderen, ist der Rest immer null:
#
#          3 Bilder,  6 Folien je Tag -> 0,0,0,0,0,0,0,0,0,0,0,0
#          4 Bilder,  8 Folien        -> 0,0,0,0,0,0,0,0,0,0,0,0
#          6 Bilder,  6 Folien        -> 0,0,0,0,0,0,0,0,0,0,0,0
#          8 Bilder,  8 Folien        -> 0,0,0,0,0,0,0,0,0,0,0,0
#          5 Bilder, 10 Folien        -> 0,0,0,0,0,0,0,0,0,0,0,0
#
#      Jeder Tag dasselbe Deckblattbild. Bei 5 Bildern und 6 Folien
#      ging es zufaellig gut — deshalb faellt es nicht immer auf.
#
#      Der Startpunkt ist jetzt der TAG selbst:
#
#          0,1,2,0,1,2,...   nie zweimal dasselbe hintereinander,
#                            solange mehr als ein Bild da ist
#
#      Das ist auch die richtige Groesse: der Wechsel gehoert an den
#      Tag, nicht an die Zahl der Folien in einem Beitrag.

P.append(('if(Vt)try{Tt=await ed(Tt,He,Ze),Ze+=Tt.length}catch{}',
 'if(Vt)try{Tt=await ed(Tt,He,pt),Ze+=Tt.length}catch{}',
 "Die Bildreihe rueckt pro TAG weiter, nicht pro Folie", 1))

# 108 — Warum das Vorbild anders aussieht. Beide Raster durchgemessen.
#
#      Frage: hat im Vorbild jeder Beitrag ein Bild? ANTWORT: ja,
#      ausnahmslos. Gemessen ueber den Quartilsabstand der Helligkeit
#      je Kachel — eine Flaeche hat 0, ein Foto hat Streuung. Im
#      Vorbild liegt der kleinste Wert bei 31, bei zwoelf von zwoelf
#      Kacheln. In Carinas Feed haben zwei von sechs gemessenen
#      Kacheln den Wert 0: reine Flaeche, gar kein Bild. Das sind
#      Tage aus einer alten Erzeugung; der Plan muss einmal neu
#      gebaut werden, sonst hilft textAnteil 1 nichts.
#
#      Was NICHT der Unterschied ist — die Schriftgroesse:
#          Vorbild  0,070 bis 0,072 der Kachelbreite
#          Carina   0,066 bis 0,085
#      Praktisch gleich.
#
#      Was der Unterschied IST:
#
#      1. Der Ausschnitt. deckblattSchnitte stand auf
#         full|wide|bust|wide|full|bust, im Mittel 1,35-facher Zoom.
#         Das Vorbild zoomt NICHT hinein: die Person ist klein im
#         Bild, drumherum ist Platz, und genau dort steht der Text.
#         Bei 1,35 bis 1,7 fuellt die Person die Kachel und der Text
#         landet im Gesicht. Neu: full|full|wide|full|wide|full,
#         im Mittel 1,12.
#
#      2. Das Schwarz. Im Vorbild liegen 44 Prozent der Kachelflaeche
#         unter Helligkeit 40, bei Carina 30. Und das laesst sich
#         NICHT nachstellen: durchgerechnet mit Kontrast .28, .40 und
#         .52 kommt dasselbe Foto auf 7,6 / 10,7 / 13,5 Prozent. Die
#         Dunkelheit im Vorbild steckt in den FOTOS — Studio, dunkler
#         Hintergrund, dunkle Kleidung —, nicht in der Bearbeitung.
#         Kein Wert im Block holt das nach.

# 109 — Die schwarzen Kacheln waren nicht die Textkachel-Regel.
#       Ich habe die Verweise selbst zerschossen.
#
#       Carina: "Allllllles sind Fotoposts!!!!!" — und sie hat recht,
#       meine Erklaerung von vorhin war zu bequem. Nachgesehen:
#
#       Beim LADEN prueft die App jede Kachel: zeigt ihr background
#       auf ein Bild, das noch in der Bibliothek liegt? Wenn nicht,
#       wird der Verweis geloescht ("zeigten auf geloeschte Fotos").
#       Die Kachel ist dann schwarz.
#
#       Beim SPEICHERN verkleinere ich seit Eintrag 84 zu grosse
#       Bilder (zKlein) — und schreibe sie damit als NEUE Datenadresse
#       in die Bibliothek. Die Kacheln im Plan zeigen aber weiter auf
#       die ALTE Adresse. Beim naechsten Laden findet die Pruefung
#       den Verweis nicht mehr und loescht ihn.
#
#       Also: mein eigenes Verkleinern hat die Bilder aus dem Plan
#       geworfen. Kein Wunder, dass "jeder Tag ein Foto" nichts
#       geholfen hat — die Fotos waren zugewiesen und wurden beim
#       Laden wieder entfernt.
#
#       Zwei Reparaturen:
#
#       1. Beim Speichern wandern die Verweise mit. Aus der Liste der
#          verkleinerten Bilder wird eine Abbildung alt -> neu, und
#          die Kacheln im Plan werden mitgezogen. Damit kann der
#          Bruch nicht mehr entstehen.
#
#       2. Beim Laden wird ein Verweis, der ins Leere zeigt, ERSETZT
#          statt geloescht — durch ein Bild aus der Bibliothek,
#          reihum nach Tag und Folie. Nur wenn die Bibliothek leer
#          ist, bleibt die Kachel ohne Bild. Das heilt die Plaene,
#          die den Bruch schon haben, ohne neu erzeugen zu muessen.
#
#       Dazu: textAnteil 1 liess einen Tag von hundert ohne Foto,
#       weil 0 als "nicht gesetzt" galt. Die Bedingung fragt jetzt
#       auf !=null statt auf wahr, damit ist 0 ein gueltiger Wert:
#
#           textAnteil 0  ->  100 von 100 Tagen bekommen ein Foto
#           textAnteil 1  ->   99 von 100
#
P.append(('const rk=await Promise.all(r.map(zKlein));let l={__packed:2,gallery:rk,days:s};',
 'const rk=await Promise.all(r.map(zKlein));'
 'const zAbb={};r.forEach((zo,zi)=>{if(typeof zo=="string"&&typeof rk[zi]=="string"&&zo!==rk[zi])zAbb[zo]=rk[zi]});'
 'const zTage=Object.keys(zAbb).length&&Array.isArray(s)?s.map(zt=>zt&&Array.isArray(zt.slides)'
 '?{...zt,slides:zt.slides.map(zf=>zf&&typeof zf.background=="string"&&zAbb[zf.background]'
 '?{...zf,background:zAbb[zf.background]}:zf)}:zt):s;'
 'let l={__packed:2,gallery:rk,days:zTage};',
 "Verkleinerte Bilder: die Verweise im Plan wandern mit", 1))
P.append(('Z=H.map(pe=>({...pe,slides:pe.slides.map(ye=>{const ue=ye&&ye.background;return typeof ue!="string"||!ue||re.has(ue)?ye:(fe++,{...ye,background:null,overlay:void 0,_autoImage:void 0})})}))',
 'const zListe=Array.from(re);'
 'Z=H.map((pe,zi)=>({...pe,slides:pe.slides.map((ye,zj)=>{const ue=ye&&ye.background;'
 'const zHat=typeof ue=="string"&&!!ue;'
 'if(zHat&&re.has(ue))return ye;'
 'const zNeu=zListe.length?zListe[(zi+zj)%zListe.length]:null;'
 'if(zHat){fe++;return{...ye,background:zNeu,overlay:void 0,_autoImage:void 0}}'
 'if(zNeu&&BS_KACHEL.textAnteil===0&&!(ye&&ye.karte)){fe++;return{...ye,background:zNeu,overlay:void 0,_autoImage:void 0}}'
 'return ye})}))',
 "Fehlendes Bild wird ergaenzt, kaputter Verweis ersetzt", 1))
P.append(('Vt=(BS_KACHEL.textAnteil?((pt*37+13)%100)>=BS_KACHEL.textAnteil:',
 'Vt=(BS_KACHEL.textAnteil!=null?((pt*37+13)%100)>=BS_KACHEL.textAnteil:',
 "textAnteil 0 heisst jeder Tag ein Foto", 1))

# 110 — Die Reparatur reparierte nur die Haelfte.
#
#      In Eintrag 109 habe ich beim Laden einen KAPUTTEN Bildverweis
#      ersetzt statt geloescht. Nur: die schwarzen Kacheln bei Carina
#      hatten gar keinen Verweis. Sie stammen aus einer Erzeugung, in
#      der textAnteil noch 67 oder 8 war — dort waren sie ABSICHTLICH
#      Textkacheln. Ein Verweis, der nie da war, kann nicht kaputt
#      sein, und meine Reparatur hat sie nicht angefasst.
#
#      Jetzt gibt es zwei Faelle:
#
#          Verweis da, zeigt ins Leere   -> ersetzen  (immer)
#          gar kein Verweis              -> ergaenzen (nur wenn
#                                           textAnteil 0 ist)
#
#      Die Bedingung ist genau der Wert, der ohnehin sagt "jeder Tag
#      bekommt ein Foto". Im warmen Stil steht er auf 67, dort wird
#      nichts ergaenzt und die Textkacheln bleiben Textkacheln.
#      Durchgespielt:
#
#          textAnteil  0  ->  jede Folie bekommt ein Bild
#          textAnteil 67  ->  nur der kaputte Verweis wird ersetzt
#
#      Ausgenommen sind Folien mit einer eigenen Karte (Ablauf), die
#      zeichnen ihr eigenes Layout und brauchen kein Foto.

# 111 — Jetzt holt sich der ZEICHNER das Bild, nicht der Ladevorgang.
#
#      Dritter Anlauf, und diesmal an der Stelle, an der es nicht
#      mehr schiefgehen kann. Die beiden Reparaturen davor (109, 110)
#      haengen am Ladevorgang, und der hat eine Bedingung, die ich
#      nicht sicher beurteilen kann:
#
#          contentPlan: A.current ? re.contentPlan : Z
#
#      A.current wird wahr, sobald irgendwer im Lauf der Sitzung
#      einen contentPlan schreibt. Ist es beim Laden schon wahr, wird
#      der reparierte Plan Z einfach weggeworfen. Genau das erklaert,
#      warum zweimal nichts passiert ist.
#
#      Statt weiter am Ladevorgang zu drehen: der Zeichner selbst
#      prueft es. Ca bekommt die Kachel; hat sie kein Bild, der Stil
#      verlangt aber eines (textAnteil 0) und es ist keine
#      Ablauf-Karte, holt er sich eines aus window.__bsBilder. Die
#      Liste wird beim Laden hinterlegt.
#
#      Das ist unabhaengig davon, ob der Plan repariert wurde, ob er
#      neu erzeugt wurde oder ob er aus dem Speicher kommt. Jede
#      Zeichnung heilt sich selbst — auch der Export, weil der durch
#      dieselbe Funktion geht.
#
#      Welches Bild: gewuerfelt aus Text und Folienindex, damit
#      verschiedene Tage verschiedene Bilder bekommen. Der Plan
#      selbst wird dabei NICHT veraendert; die Kachel wird nur fuer
#      diese eine Zeichnung ergaenzt. Wer den Tag neu erzeugt,
#      bekommt eine richtige Zuweisung.
P.append(('Y=Array.isArray(_)?_:[];let Z=H;',
 'Y=Array.isArray(_)?_:[];'
 'try{if(typeof window<"u"){const zLib=Y.map(pe=>typeof pe=="string"?pe:(pe&&(pe.src||pe.url||pe.dataUrl))||"").filter(Boolean);'
 'const zPlan=[];H.forEach(pe=>(pe.slides||[]).forEach(ye=>{const zb=ye&&ye.background;'
 'if(typeof zb=="string"&&zb&&zLib.indexOf(zb)<0&&zPlan.indexOf(zb)<0)zPlan.push(zb)}));'
 'window.__bsBilder=zLib.concat(zPlan)}}catch(zz){}'
 'let Z=H;',
 "Die Bilderliste liegt global bereit", 1))
P.append(('Ca=async(e,t,r,n,i={})=>{var yn,_n,Jr,xr,zr,ti,nn,_i,ki,ri;try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}',
 'Ca=async(e,t,r,n,i={})=>{var yn,_n,Jr,xr,zr,ti,nn,_i,ki,ri;try{Pe.fabric.util.clearFabricFontCache()}catch(zz){}'
 'try{if(typeof window<"u"&&typeof t.background=="string"&&t.background){'
 'const zL=window.__bsBilder=window.__bsBilder||[];'
 'if(zL.indexOf(t.background)<0)zL.push(t.background)}}catch(zz){}'
 '(()=>{try{if(!t.background&&BS_KACHEL.textAnteil===0&&t.karte!=="ablauf"){'
 'const zB=(typeof window<"u"&&window.__bsBilder)||[];if(!zB.length)return;'
 'const zs=String(t.text||"")+"|"+String(typeof t._tag=="number"?t._tag:(i.slideIndex||0));let zh=0;'
 'for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 't={...t,background:zB[zh%zB.length]}}}catch(zz){}})();',
 "Zeichner: keine Kachel ohne Bild, wenn der Stil das verlangt", 1))

# 112 — Mein eigener Schutz hat die Ergaenzung blockiert.
#
#      In Eintrag 111 steht die Bedingung
#
#          !t.background && textAnteil===0 && !t.karte
#
#      Das !t.karte sollte die Ablauf-Karte aussparen. Aber karte ist
#      auf fast JEDER Kachel gesetzt — die Fassung baut sie mit
#      karte:t.karte||"dunkel", und Zitat- und Kartenfolien tragen
#      sie ohnehin. Damit war die Bedingung fast nie wahr und die
#      Ergaenzung lief praktisch nie. Richtig ist
#
#          t.karte !== "ablauf"
#
#      Zweiter Punkt: die Bilderliste kam nur aus der BIBLIOTHEK
#      (brandImages). Liegen die Fotos nur in den Kacheln des Plans
#      und nicht in der Bibliothek, ist die Liste leer und es gibt
#      nichts zu ergaenzen. Sie wird jetzt aus beidem gefuellt, und
#      der Zeichner merkt sich zusaetzlich jedes Bild, das er sieht.
#      Damit kann eine Kachel ohne Bild sich bei einer Kachel mit
#      Bild bedienen, ganz ohne Bibliothek und ohne Ladevorgang.
#
#      Durchgespielt mit sieben Tagen, davon vier mit karte:
#      alle bekommen ein Bild ausser der Ablauf-Karte.

# 113 — Die Haelfte schwarzweiss, und schwarzweiss heisst neutral.
#
#      Carina: "es sollten 50% schwarz weiss sein". Nachgerechnet war
#      der Anteil schon 50 — die Reihe hatte drei von sechs auf -1,
#      und ueber 600 Kacheln kommen 50,2 Prozent heraus. Es SAH nur
#      nicht so aus, aus zwei Gruenden:
#
#      1. Der Rest war unausgewogen: 33 Prozent "entzogen" (-0,55)
#         gegen 17 Prozent Farbe. Entzogene Farbe liest sich im
#         Raster wie Farbe, nicht wie ein eigener Zustand. Die
#         gefuehlte Bilanz war also ein Viertel schwarzweiss gegen
#         drei Viertel bunt. Die Reihe hat jetzt acht Eintraege:
#         vier mal -1, zwei mal -0,55, zwei mal 0,1 — gemessen
#         50,2 / 25,0 / 24,8 Prozent.
#
#      2. Wichtiger: die schwarzweissen Kacheln waren gar nicht
#         schwarzweiss. Ueber jedem Bild liegt ein Farbton aus
#         tonReihe, und der wuerfelt UNABHAENGIG von der Saettigung —
#         eine entsaettigte Kachel bekam so einen warmen oder
#         violetten Schleier und war damit wieder getoent. Zwei
#         Wuerfel, die einander widersprechen.
#
#         Jetzt gilt: ist die Kachel auf -1, nimmt sie tonNeutral
#         (13,13,13) statt eines Tons aus der Reihe. Schwarzweiss
#         heisst schwarzweiss.
#
#      Anmerkung fuer spaeter: die Filterkette der App legt nach der
#      Entsaettigung noch eine ColorMatrix mit warmTone .18 darueber
#      (R x1,007 G x1,004 B x0,996). Das ist ein Rest Waerme, den man
#      bei genauem Hinsehen noch sieht. Nicht angefasst, weil er auf
#      jeder Kachel gleich liegt — aber er ist der naechste Kandidat,
#      falls das Schwarzweiss noch nicht neutral genug ist.

# 114 — Schwarzweiss haengt nicht mehr am Bildfilter.
#
#      Carina sieht kein einziges schwarzweisses Bild, obwohl die
#      Reihe nachweislich die Haelfte auf -1 stellt. Die Entsaettigung
#      lief bisher ueber fabric.Image.filters.Saturation, und dieser
#      Weg hat eine Stelle, die alles still wegwirft:
#
#          try{me.applyFilters()}catch{me.filters=[];...}
#
#      Schlaegt applyFilters fehl — auf einem Telefon mit grossen
#      Bildern durchaus moeglich, siehe die Safari-Abstuerze in
#      Eintrag 70 — werden ALLE Filter geloescht. Ergebnis: jedes
#      Bild in voller Farbe, und zwar ohne jede Meldung.
#
#      Drei Aenderungen, damit das nicht mehr davon abhaengt:
#
#      1. Schwarzweiss kommt jetzt zusaetzlich ueber den Mischmodus:
#         eine graue Flaeche mit globalCompositeOperation
#         "saturation" ueber dem Bild. Das ist eine Zeichenoperation,
#         kein Pixelfilter — sie braucht keinen zweiten Bildspeicher
#         und kann nicht fehlschlagen.
#      2. Der Mischmodus wird einmal geprueft (BS_MISCHBAR). Kann der
#         Browser ihn nicht, bleibt die Flaeche weg — sonst laege ein
#         grauer Kasten ueber dem Foto.
#      3. Schlaegt die Filterkette doch fehl, wird nicht mehr alles
#         geworfen: der Saettigungsfilter wird allein noch einmal
#         versucht.
#
#      Nachgemessen an vier Kacheln, Farbigkeit als mittlerer Abstand
#      zwischen groesstem und kleinstem Farbkanal:
#
#          schwarzweiss, Filter und Mischmodus    0,0
#          schwarzweiss, NUR Mischmodus           0,0
#          entzogen -0,55                        11,7
#          Farbe 0,1                             31,9
#
#      Die zweite Zeile ist der Punkt: auch mit vollstaendig
#      abgeschalteter Filterkette ist die Kachel schwarzweiss.
P.append(('if(typeof window<"u"&&window.BS_STIL==="dunkel")Object.assign(BS_KACHEL,BS_DUNKEL);',
 'if(typeof window<"u"&&window.BS_STIL==="dunkel")Object.assign(BS_KACHEL,BS_DUNKEL);'
 'const BS_MISCHBAR=(()=>{try{const zc=document.createElement("canvas").getContext("2d");'
 'zc.globalCompositeOperation="saturation";return zc.globalCompositeOperation==="saturation"}catch(zz){return!1}})();',
 "Einmal pruefen, ob der Browser den Mischmodus kann", 1))
P.append(('const ur=new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgba(${zTon||"0,0,0"},${Et})`,selectable:!1});Et>0&&e.add(ur);',
 'zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",'
 'globalCompositeOperation:"saturation",selectable:!1,evented:!1}));'
 'const ur=new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgba(${zTon||"0,0,0"},${Et})`,selectable:!1});Et>0&&e.add(ur);',
 "Schwarzweiss auch ohne Filter, ueber den Mischmodus", 1))
P.append(('try{me.applyFilters()}catch{me.filters=[];try{me.applyFilters()}catch{}}',
 'try{me.applyFilters()}catch{try{me.filters=(Ze!==0&&Pe.fabric.Image.filters.Saturation)?[new Pe.fabric.Image.filters.Saturation({saturation:Ze})]:[];me.applyFilters()}catch{me.filters=[];try{me.applyFilters()}catch{}}}',
 "Schlaegt die Filterkette fehl, bleibt wenigstens die Saettigung", 1))

# 115 — 50/50, und die Zwischenstufe faellt weg.
#
#      Carina: "zuviele, also 50/50". Die Reihe hatte acht Eintraege
#      — vier schwarzweiss, zwei entzogen, zwei Farbe. Das ist zwar
#      rechnerisch die Haelfte schwarzweiss, aber die entzogenen
#      Kacheln liegen optisch nah am Schwarzweiss, und im Raster
#      wirkt es dann wie drei Viertel.
#
#      Jetzt zwei Eintraege, sonst nichts:
#
#          saettigungReihe  "-1|0.1"
#
#      Nachgerechnet ueber 2000 Kacheln: 50,0 Prozent schwarzweiss,
#      50,0 Prozent Farbe. Die Zwischenstufe -0,55 ist raus; wer sie
#      zurueck will, haengt sie einfach wieder in die Reihe.
#
#      Kleine Lehre nebenbei: eine erste Messung ueber 800 Kacheln
#      ergab 43,3 Prozent und sah nach einem Rundungsfehler in der
#      Reihe aus. Es war die Stichprobe: die Testtexte unterschieden
#      sich nur durch eine hochzaehlende Zahl, und das faerbt den
#      Wuerfel. Mit 2000 unabhaengigeren Texten sind es exakt 50,0.
#      Bei so einer Zahl lohnt der zweite Durchlauf.


# 116 — "50/50 !!! Also immer wechseln." Nicht die Haelfte im Mittel,
#      sondern abwechselnd: Tag 1 Farbe, Tag 2 schwarzweiss, Tag 3
#      Farbe. Der Wuerfel aus 115 trifft die Haelfte auf 2000 Kacheln
#      genau, aber im sichtbaren Ausschnitt — neun Kacheln auf dem
#      Schirm — liegen dann eben doch mal vier schwarzweisse
#      nebeneinander. Zufall sieht nicht aus wie Wechsel.
#
#      Der Zeichner wusste bisher nicht, der wievielte Tag er ist. Die
#      Vorschau reicht ihm nur {slideIndex, totalSlides, scale,
#      globalBrandName, typography}. Die Tagesnummer liegt eine Ebene
#      hoeher: im Raster als ae.day, beim Laden als re.day. Also wird
#      sie an beiden Stellen auf die Folie gestempelt (_tag) und im
#      Zeichner gelesen — dann ist es kein Wuerfeln mehr, sondern
#      zl[tag % zl.length].
#
#      Kennt eine Kachel ihren Tag nicht (Ausgabewege, die Folien ohne
#      Plan bauen), faellt sie auf den Hash-Weg aus 115 zurueck. Der
#      Wechsel ist damit ueberall dort streng, wo eine Tagesnummer da
#      ist, und nirgends kaputt, wo keine ist.
#
#      Nachgerechnet ueber 14 Tage: Tag 1 Farbe, Tag 2 schwarzweiss,
#      ... Tag 14 schwarzweiss — 7 von 14, lueckenlos abwechselnd.

# Die Tagesnummer wandert beim Laden auf jede Folie.
P.append(('const H=(Array.isArray(S)?S:[]).filter(re=>re&&typeof re=="object").map(re=>({...re,slides:Array.isArray(re.slides)?re.slides.filter(Boolean):[]})).filter(re=>re.slides.length>0)',
 'const H=(Array.isArray(S)?S:[]).filter(re=>re&&typeof re=="object").map(re=>({...re,slides:Array.isArray(re.slides)?re.slides.filter(Boolean).map(ye=>typeof re.day=="number"?{...ye,_tag:re.day}:ye):[]})).filter(re=>re.slides.length>0)',
 "Tagesnummer beim Laden auf jede Folie stempeln", 1))

# Das Raster gibt die Tagesnummer mit.
P.append(('v.jsx(uG,{data:{...Ze,slideNumber:void 0},brandName:At}',
 'v.jsx(uG,{data:{...Ze,slideNumber:void 0,_tag:ae.day},brandName:At}',
 "Raster reicht die Tagesnummer an die Kachel durch", 1))

# Kennt die Kachel ihren Tag, wird streng abgewechselt statt gewuerfelt.
P.append(('const zSat=(()=>{try{const zl=String(BS_KACHEL.saettigungReihe||"").split("|").filter(zx=>zx!=="");if(!zl.length)return null;',
 'const zSat=(()=>{try{const zl=String(BS_KACHEL.saettigungReihe||"").split("|").filter(zx=>zx!=="");'
 'if(BS_KACHEL.saettigungWechsel&&zl.length&&typeof t._tag=="number"){'
 'const zv=parseFloat(zl[((t._tag%zl.length)+zl.length)%zl.length]);if(!isNaN(zv))return zv}'
 'if(!zl.length)return null;',
 "strenger Wechsel nach Tagesnummer, Hash nur als Rueckfall", 1))


# 117 — Nachgemessen: woran das Vorbild wirklich anders aussieht.
#
#      Nicht geraten, sondern die neun Kacheln aus beiden Rastern
#      Pixel fuer Pixel verglichen (Helligkeit nach BT.709):
#
#                          meins   Vorbild
#          dunkelstes Pixel    4,9      0,0
#          p01                17,2      1,0
#          p05                23,3      3,7
#          Mitte (p50)        89,0     55,5
#          Lichter (p95)     176,7    178,3
#          Farbigkeit          8,5      8,4
#
#      Die Lichter sind gleich. Die Farbigkeit ist gleich. Der ganze
#      Unterschied sitzt unten: KEINE ihrer neun Kacheln enthaelt ein
#      einziges schwarzes Pixel, ALLE neun des Vorbilds tun es.
#
#      (a) Schwarzpunkt. Die Tonwertkette im Bundle haengt komplett an
#      t.warmEditorial — fehlt das Feld, laeuft weder Kontrast noch
#      Saettigung, das Foto geht roh durch. Und selbst wo sie laeuft,
#      ist fabric Contrast eine Streckung um Mittelgrau: sie hebt die
#      Lichter genauso wie sie die Tiefen senkt.
#
#      Gebraucht wird ein Schwarzpunkt: Tiefen auf Null, Weiss bleibt
#      Weiss. Das ist keine Filterkette, das ist eine Zeichenoperation
#      — eine Flaeche im Mischmodus color-burn, direkt auf dem Foto und
#      unter allem Text. Sie kann nicht fehlschlagen (aus demselben
#      Grund wie die Schwarzweiss-Flaeche aus 114) und sie ruehrt den
#      Text nicht an, weil er spaeter gezeichnet wird.
#
#          color-burn(b, g) = 1 - (1-b)/g   mit g = 1 - bildSchwarzpunkt
#
#      In Chromium nachgemessen ueber alle 256 Graustufen: groesste
#      Abweichung zur Formel 1 von 255. Weiss bleibt exakt 255.
#
#      bildSchwarzpunkt .13, auf ihre echten Kacheln gerechnet:
#
#                          vorher  nachher   Vorbild
#          dunkelstes Pixel   4,9      0,0       0,0
#          p01               17,2      0,0       1,0
#          p05               23,3      0,9       3,7
#          Mitte             89,0     63,7      55,5
#          schwarz (<40)    19,1%    37,1%     48,5%
#
#      (b) Wo der Text sitzt. Der Anteil sehr heller Pixel je Zehntel
#      der Kachelhoehe zeigt beim Vorbild zwei Baenke mit einer Luecke
#      dazwischen, bei mir einen Schmier ueber die ganze Kachel. Je
#      Kachel gemessen faengt der Textblock im Vorbild bei 0,58 an und
#      endet bei 0,88 — er sitzt im unteren Drittel. Meiner sass in
#      der Mitte, und zwar fest verdrahtet:
#
#          He = tt.istKarte ? .42 : ve==="oben" ? .24
#             : ve==="unten" ? .7 : .5
#
#      Die .5 ist jetzt BS_KACHEL.textMitte, im dunklen Aufsatz .73 —
#      die gemessene Mitte des Vorbilds. Geteilte Kacheln bleiben, wie
#      sie waren, die rechnen ueber geteiltOben/geteiltUnten.
#
#      (c) Die Wortmarke. Im Vorbild steht auf keiner Kachel ein
#      Handle; bei mir auf jeder, unten links — im Profil das letzte
#      Zehntel (2,70 Prozent gegen 0,31). nameZeigen:0 schaltet sie
#      ab. nameZeigen weg oder auf 1, und sie ist wieder da.
#
#      Nicht geaendert: der Bildausschnitt. Die Detaildichte ist 5,37
#      gegen 4,59, aber die Streuung im Vorbild geht von 0,84 bis 9,12
#      — daraus laesst sich kein Zoom ableiten. Und der Rest des
#      Schwarzanteils (37 gegen 48 Prozent) steckt in den Fotos, nicht
#      im Code: dunkle Raeume gegen helle graue Wand.

# Kann der Browser color-burn? Einmal fragen, nicht je Kachel.
P.append(('const BS_MISCHBAR=',
 'const BS_BRENNBAR=(()=>{try{const zc=document.createElement("canvas").getContext("2d");'
 'zc.globalCompositeOperation="color-burn";return zc.globalCompositeOperation==="color-burn"}catch(zz){return!1}})();'
 'const BS_MISCHBAR=',
 "Erkennung color-burn", 1))

# Der Schwarzpunkt: eine Flaeche auf dem Foto, unter allem Text.
P.append(('zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));',
 '(()=>{const zP=Number(BS_KACHEL.bildSchwarzpunkt)||0;if(!(zP>0)||!BS_BRENNBAR||!t.background)return;'
 'const zg=Math.max(0,Math.min(255,Math.round(255*(1-zP))));'
 'e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgb(${zg},${zg},${zg})`,'
 'globalCompositeOperation:"color-burn",selectable:!1,evented:!1}))})();'
 'zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));',
 "Schwarzpunkt als color-burn-Flaeche", 1))

# Der Sitz des Textblocks war fest verdrahtet.
P.append((':ve==="oben"?.24:ve==="unten"?.7:.5;let De=n*He-ae/2+Et/2;',
 ':ve==="oben"?.24:ve==="unten"?.7:(BS_KACHEL.textMitte||.5);let De=n*He-ae/2+Et/2;',
 "Sitz des Textblocks kommt aus dem Block", 1))

# Die Wortmarke laesst sich abschalten.
P.append(('tt.platten||e.add(new Pe.fabric.Text(Ze,{left:_e,top:n*(BS_KACHEL.nameUnten||.945)',
 '(tt.platten||BS_KACHEL.nameZeigen===0)||e.add(new Pe.fabric.Text(Ze,{left:_e,top:n*(BS_KACHEL.nameUnten||.945)',
 "Wortmarke abschaltbar", 1))


# 118 — Die Farbbremse. Carina: "die farbigen Bilder sind vom grading
#      zu weit weg von normalen Farben."
#
#      Sie hat recht, und der Grund steckt in 117. color-burn rechnet
#      je Kanal:
#
#          out_c = 1 - (1 - b_c) / g
#
#      Jeder Kanal bekommt seinen eigenen Schwarzpunkt. Der dunkelste
#      Kanal faellt weiter als der hellste — der Abstand dazwischen
#      waechst, und der Abstand zwischen den Kanaelen IST die
#      Saettigung. Auf einer Schwarzweisskachel passiert nichts (alle
#      drei Kanaele sind gleich), auf einer Farbkachel drueckt es die
#      Farbe hoch.
#
#      In Chromium ueber ihre fuenf Farbkacheln gemessen:
#
#          ohne alles          0,160
#          nur Schwarzpunkt    0,248     das ist plus 55 Prozent
#
#      Die Bremse ist eine zweite Flaeche direkt hinter dem
#      Schwarzpunkt: Mischmodus saturation, halbdurchsichtiges
#      Mittelgrau. Volldeckend waere sie Schwarzweiss, mit Alpha
#      mischt sie linear zwischen "gebrannt" und "gebrannt und grau"
#      — also eine Entsaettigung mit Regler.
#
#          Bremse 0,20   0,209
#          Bremse 0,30   0,186     ungefaehr das Niveau des Vorbilds
#          Bremse 0,42   0,160     genau der Ausgangswert
#
#      .42 gewaehlt: nicht "sieht besser aus", sondern der gemessene
#      Wert, der die Saettigung exakt dahin zurueckbringt, wo sie vor
#      dem Schwarzpunkt war.
#
#      Sie kostet nichts. Mittel 76,1, Schwarzanteil 35,9 Prozent,
#      dunkelstes Pixel 0,0 — bei jeder Bremsstufe identisch. Die
#      Bremse ruehrt nur die Saettigung an, nicht den Ton. Der
#      Farbton verschiebt sich um hoechstens 2 Grad, unsichtbar.
#
#      Sie haengt am Schwarzpunkt (steht in derselben Klammer, hinter
#      demselben return) und laeuft nicht auf Schwarzweisskacheln, wo
#      es nichts zu bremsen gibt. Kein Schwarzpunkt, keine Bremse.

P.append(('const BS_BRENNBAR=',
 'const BS_FARBMISCH=(()=>{try{const zc=document.createElement("canvas").getContext("2d");'
 'zc.globalCompositeOperation="color";return zc.globalCompositeOperation==="color"}catch(zz){return!1}})();'
 'const BS_BRENNBAR=',
 "Erkennung Mischmodus color", 1))

P.append(('globalCompositeOperation:"color-burn",selectable:!1,evented:!1}))})();',
 'globalCompositeOperation:"color-burn",selectable:!1,evented:!1}));'
 'if(BS_KACHEL.bildFarbNeutral!==0&&BS_FARBMISCH&&!(zSat<=-.99))try{'
 'const zel=me.getElement&&me.getElement();if(zel){'
 'let zq=zel,zf=1;const zM=Number(BS_KACHEL.bildMitteltoene)||0;'
 'if(zM>0)try{const zKa=Number(BS_KACHEL.bildFarbKante)||640;'
 'zf=Math.min(1,zKa/Math.max(zel.width||1,zel.height||1));'
 'const zc=document.createElement("canvas");'
 'zc.width=Math.max(1,Math.round((zel.width||1)*zf));'
 'zc.height=Math.max(1,Math.round((zel.height||1)*zf));'
 'const zx=zc.getContext("2d",{willReadFrequently:!0});'
 'zx.drawImage(zel,0,0,zc.width,zc.height);'
 'const zd=zx.getImageData(0,0,zc.width,zc.height),za=zd.data;'
 'for(let zi=0;zi<za.length;zi+=4){const zr=za[zi],zgn=za[zi+1],zbl=za[zi+2];'
 'const zlu=.2126*zr+.7152*zgn+.0722*zbl;let zw;'
 'if(zlu<=50||zlu>=225)zw=0;else if(zlu<75)zw=(zlu-50)/25;else if(zlu<=170)zw=1;else zw=(225-zlu)/55;'
 'if(zw<=0)continue;const zn=-zM*zw,zmx=Math.max(zr,zgn,zbl);'
 'if(zmx!==zr)za[zi]=Math.max(0,Math.min(255,zr+(zmx-zr)*zn));'
 'if(zmx!==zgn)za[zi+1]=Math.max(0,Math.min(255,zgn+(zmx-zgn)*zn));'
 'if(zmx!==zbl)za[zi+2]=Math.max(0,Math.min(255,zbl+(zmx-zbl)*zn));}'
 'zx.putImageData(zd,0,0);zq=zc}catch(zz){zq=zel;zf=1}'
 'e.add(new Pe.fabric.Image(zq,{originX:"center",originY:"center",left:me.left,top:me.top,'
 'scaleX:me.scaleX/zf,scaleY:me.scaleY/zf,globalCompositeOperation:"color",selectable:!1,evented:!1}))'
 '}}catch(zz){}})();',
 "Farbschicht: Helligkeit gebrannt, Farbe vom Original, Mitteltonfenster", 1))


# 119 — Die Bremse aus 118 war falsch, und zwar weil ich im falschen
#      Raum gemessen habe. Carina: "Neeeeeein das ist viel zu flach."
#
#      118 hat die Saettigung als (max-min)/max gemessen, HSV. Diese
#      Zahl steigt schon dadurch, dass ein Pixel dunkler wird — sie
#      sagt nichts darueber, wie bunt etwas AUSSIEHT. In CIELAB, wo
#      Buntheit das ist, was das Auge Buntheit nennt (C* = Wurzel aus
#      a*^2 + b*^2), sehen dieselben Bilder so aus:
#
#                              Buntheit  L0-25  L25-50  L50-75  L75+
#          roh                    6,14    4,58    8,11    5,10   3,31
#          Schwarzpunkt je Kanal  6,90    6,06    9,77    4,90   3,92
#          plus Bremse .42        3,98    3,56    5,57    2,79   2,32
#          Vorbild                7,09    4,20   12,34   13,89   1,78
#
#      Der Schwarzpunkt hebt die Buntheit um 12 Prozent. Die Bremse
#      hat 35 Prozent weggenommen. Ich habe also fuenfmal so stark
#      gegengesteuert wie noetig — in HSV sah das nach plus 75 Prozent
#      aus, und ich habe der Zahl geglaubt statt dem Bild.
#
#      Der Fehler dahinter: eine oertliche Ursache global behandelt.
#      color-burn rechnet je Kanal und multipliziert die Kanal-
#      abstaende mit 1/g. In den Tiefen macht das viel (4,58 auf
#      6,06), in den Mitteltoenen nichts (5,10 auf 4,90). Eine
#      Entsaettigung ueber die ganze Kachel trifft dafuer alles
#      gleichmaessig und raeumt genau dort ab, wo das Bild lebt:
#      Mitteltoene 5,10 auf 2,79.
#
#      Richtig ist, den Schwarzpunkt gar nicht erst auf die Farbe
#      wirken zu lassen. Nach der Brennflaeche wird dasselbe Foto ein
#      zweites Mal gezeichnet, im Mischmodus color: der nimmt Farbton
#      und Saettigung von der Quelle und die Helligkeit vom Untergrund.
#      Ergebnis: gebrannte Helligkeit, unveraenderte Farbe.
#
#          Schwarzpunkt farbneutral  5,95   5,19   8,47   4,21   3,40
#
#      6,14 vorher, 5,95 nachher — drei Prozent. Und die Tiefen
#      bleiben, wo sie sein sollen: p05 1,7, Schwarzanteil 36,0
#      Prozent, dunkelstes Pixel 0.
#
#      Faellt der Mischmodus color aus, bleibt es beim Brennen je
#      Kanal (BS_FARBMISCH); der Schwarzpunkt geht dabei nie verloren.
#      bildFarbNeutral:0 schaltet die Rueckholung ab.
#
#      Bleibt eine Sache, die der Code nicht loesen kann: die
#      Mitteltoene. 5,10 gegen 13,89 beim Vorbild, ueber das Doppelte.
#      Das sind Fotos in warmem Licht gegen Fotos an einer grauen
#      Wand.


# 120 — Die Mitteltoene. Carina: "Ja mach die Mitteltoene 0.2".
#
#      Buntheit in CIELAB, je Helligkeitsband:
#
#                            gesamt  L0-25  L25-50  L50-75  L75+
#          meins (karten180)   5,95   5,19    8,47    4,21   3,40
#          Vorbild             7,09   4,20   12,34   13,89   1,78
#
#      Zwei Sachen stehen da. Die Tiefen sind bei mir BUNTER als beim
#      Vorbild (5,19 gegen 4,20) — ein globaler Saettigungsschub macht
#      es also schlimmer, nicht besser. Nachgerechnet mit der Formel
#      von fabric.Image.filters.Saturation:
#
#                          gesamt  L0-25  L25-50  L50-75
#          global 0,45       8,55   7,97   12,48    5,71
#
#      Die Mitteltoene treffen (12,48 gegen 12,34), aber die Tiefen
#      schiessen auf fast das Doppelte des Vorbilds. Deshalb ein
#      Fenster ueber der Helligkeit statt eines Reglers ueber allem:
#
#          bis 50      nichts
#          50 bis 75   Rampe hinein
#          75 bis 170  voll
#          170 bis 225 Rampe hinaus
#          ab 225      nichts
#
#      Die Grenzen sind CIELAB L 25 und L 75, in 8-Bit umgerechnet.
#
#                          gesamt  L0-25  L25-50  L50-75
#          Fenster 0,20      6,91   5,71   10,22    5,11
#          Vorbild           7,09   4,20   12,34   13,89
#
#      Gesamtbuntheit 6,91 gegen 7,09 — auf zwei Prozent am Vorbild,
#      und die Tiefen bewegen sich kaum (5,19 auf 5,71).
#
#      WO ES SITZT. Die Farbschicht aus 119 wird ohnehin schon ein
#      zweites Mal gezeichnet. Sie traegt nur Farbton und Saettigung,
#      die Zeichnung steckt in der Helligkeit darunter — Farbe braucht
#      also wenig Aufloesung. Deshalb wird nur eine kleine Kopie
#      durchgerechnet (bildFarbKante, 640 Pixel lange Kante): rund
#      eine halbe Million Pixel statt vier Millionen. Dasselbe
#      Prinzip, nach dem JPEG und Video die Farbe unterabtasten.
#
#      Faellt der Pixeldurchlauf aus (getImageData auf einer
#      verunreinigten Flaeche), faengt die innere Klammer das ab und
#      die Farbschicht wird unveraendert gezeichnet — dann fehlt der
#      Mitteltonschub, aber nichts ist kaputt.
#
#      WAS NICHT GEHT: L50-75, 5,11 gegen 13,89. Nachgesehen, woraus
#      dieses Band bei ihr besteht: 71,9 Prozent der Pixel darin sind
#      praktisch neutral (C* unter 3), beim Vorbild nur 9,9 Prozent.
#      Das ist die graue Wand. Saettigung multipliziert vorhandene
#      Buntheit, und null mal irgendwas bleibt null. Grau laesst sich
#      nicht saettigen, nur einfaerben — und das waere kein Grading
#      mehr.


# 121 — Weniger Schwarzpunkt, dafuer eine Vignette. Carina: "Nein
#      zurueck und lieber weniger schwarzpunkt und mehr Vignette."
#
#      Der Mitteltonschub aus 120 ist wieder aus (bildMitteltoene
#      steht nicht mehr im Aufsatz; der Code dafuer bleibt, er
#      schlaeft bei 0).
#
#      Erst nachgesehen, was ueberhaupt an Vignette da war: nichts
#      Rundes. kanteOben und kanteUnten sind EIN senkrechter Verlauf,
#      oben 0 bis 0,18 und unten 0,82 bis 1. Die Seiten und die Ecken
#      werden gar nicht dunkler. Darum lagen ihre Ecken bei 69, die
#      des Vorbilds bei 49.
#
#      Neu ist ein runder Verlauf (fabric Gradient, type radial),
#      Mittelpunkt leicht oberhalb der Kachelmitte, damit das Gesicht
#      offen bleibt:
#
#          bildVignette        Deckkraft am Rand         .6
#          bildVignetteInnen   ab wo er anfaengt         .45
#          bildVignetteWeite   Radius, mal laengere Kante .72
#          bildVignetteMitte   Hoehe des Mittelpunkts    .45
#
#      Ueber alle neun Kacheln gemessen:
#
#                                  Ecken  Mitte  p05  dunkelstes
#          Punkt .13, keine Vig     36,1   84,3  3,3        0,0
#          Punkt .07, Vignette .6   32,8   93,5  8,8        0,0
#          Vorbild                  41,3   83,8  5,4        0,0
#
#      Die Ecken werden dunkler UND die Mitte heller — das ist der
#      Unterschied zwischen Vignette und Schwarzpunkt. Der Schwarzpunkt
#      zieht alles nach unten, die Vignette nimmt nur den Rand und
#      laesst das Motiv stehen. Verhaeltnis Mitte zu Ecken 2,34 vorher,
#      2,85 jetzt.
#
#      Der Schwarzpunkt bleibt drin, nur schwaecher: das dunkelste
#      Pixel ist weiter 0.
#
#      Nachgeprueft im echten fabric der App (5.5.2, ueber window.
#      fabric in der laufenden Seite), weil radiale Verlaeufe leicht
#      im falschen Koordinatenraum landen: Mitte 132,8, Ecke oben
#      links 59,9, Ecke unten rechts 7,0. Sitzt.

P.append(('colorStops:[{offset:0,color:`rgba(${zTon},${BS_KACHEL.kanteOben})`},{offset:.18,color:`rgba(${zTon},0.0)`},'
 '{offset:.82,color:`rgba(${zTon},0.0)`},{offset:1,color:`rgba(${zTon},${BS_KACHEL.kanteUnten})`}]})});e.add(ve)}catch{}',
 'colorStops:[{offset:0,color:`rgba(${zTon},${BS_KACHEL.kanteOben})`},{offset:.18,color:`rgba(${zTon},0.0)`},'
 '{offset:.82,color:`rgba(${zTon},0.0)`},{offset:1,color:`rgba(${zTon},${BS_KACHEL.kanteUnten})`}]})});e.add(ve)}catch{}'
 'try{const zVi=Number(BS_KACHEL.bildVignette)||0;if(zVi>0){'
 'const zVr=Math.max(r,n)*(Number(BS_KACHEL.bildVignetteWeite)||.72),'
 'zVx=r/2,zVy=n*(Number(BS_KACHEL.bildVignetteMitte)||.45),'
 'zVi2=Number(BS_KACHEL.bildVignetteInnen)||.45,zVt=zTon||"0,0,0";'
 'e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,'
 'fill:new Pe.fabric.Gradient({type:"radial",'
 'coords:{x1:zVx,y1:zVy,r1:zVr*zVi2,x2:zVx,y2:zVy,r2:zVr},'
 'colorStops:[{offset:0,color:`rgba(${zVt},0)`},{offset:1,color:`rgba(${zVt},${zVi})`}]})}))}}catch{}',
 "Vignette als runder Verlauf", 1))


# 122 — Die Folgeslides bekommen eine feste Unterkante. Carina: "Die
#      Schrift der Folge slides soll besser immer auf der selben Hoehe
#      vermutlich mittig unten sein."
#
#      Warum sie wandert: He ist keine Textkante, sondern die MITTE des
#      Blocks. Auf Folgeslides ist ve gleich "unten" (folgeLage) und
#      damit He gleich 0,7 — der Block wird auf 70 Prozent Hoehe
#      zentriert. Wo er dann tatsaechlich endet, haengt an seiner
#      eigenen Hoehe:
#
#          Unterkante = 0,7 + Zeilen * Zeilenhoehe/2
#
#      Bei 70 Pixel Zeilenhoehe auf 1350:
#
#          Zeilen   1      2      3      4      5      6
#          unten  0,726  0,752  0,778  0,804  0,830  0,856
#
#      13 Prozent der Kachelhoehe Unterschied, 175 Pixel. Genau das
#      sieht man, wenn man durch die Folien blaettert.
#
#      Jetzt wird auf Folgeslides die UNTERKANTE festgenagelt statt
#      der Mitte — dieselbe Rechnung, die der textUnten-Deckel schon
#      immer benutzt, nur als Regel statt als Ausnahme:
#
#          De = n * folgeFuss - ae + Et/2
#
#          Zeilen   1      2      3      4      5      6
#          unten  0,860  0,860  0,860  0,860  0,860  0,860
#
#      folgeFuss .86, derselbe Wert wie geteiltUnten — geteilte
#      Kacheln und Folgeslides enden damit auf einer Linie.
#
#      Die Bedingung ist die im Bundle ueberall gleiche: t.folienRolle
#      gesetzt und nicht "deckblatt". Nach derselben Pruefung laufen
#      schon folgeStil, folgeFamilie, folgeGewicht und folgeLage.
#      Deckblaetter und Textkacheln bleiben unberuehrt, und ohne
#      folgeFuss aendert sich gar nichts — der warme Feed hat den Wert
#      nicht.

P.append(('let De=n*He-ae/2+Et/2;if(De+ae-Et/2>n*(BS_KACHEL.textUnten||.9)',
 'let De=n*He-ae/2+Et/2;const zFF=Number(BS_KACHEL.folgeFuss)||0;'
 'zFF>0&&t.folienRolle&&t.folienRolle!=="deckblatt"&&(De=n*zFF-ae+Et/2);'
 'if(De+ae-Et/2>n*(BS_KACHEL.textUnten||.9)',
 "Folgeslides haengen an der Unterkante", 1))


# 123 — Die Fotos kommen durch. Carina: "Viel mehr sollen die
#      durchkommen." Kein Code, nur Zahlen — aber die richtigen.
#
#      Erst gemessen, was ueberhaupt auf dem Foto liegt. Die alte
#      Kachel traegt vier Lagen; ich habe sie aus den Kachelbildern
#      zurueckgerechnet (beobachtet = foto*(1-a) + ton*a) und dann
#      Varianten daraufgelegt:
#
#                                      Foto   obere    Kontrast unterm
#                                    gesamt  Haelfte   Text (schlecht. 5 %)
#          vorher                     59,8 %   72,9 %   10,5:1   3,7:1
#          alles gleichmaessig runter 76,6 %   85,0 %    8,3:1   2,4:1
#          oben ganz frei, Fuss bleibt 74,0 %  91,7 %    9,4:1   2,7:1
#
#      Der Unterschied zwischen den letzten beiden ist der Punkt. Wer
#      alles gleichmaessig herunterdreht, verliert genau dort, wo der
#      Text steht. Wer NUR die Lagen wegnimmt, die ueber der ganzen
#      Kachel liegen (bildSchleier, tiefeOben, tiefeMitte, kanteOben)
#      und den Fuss stehen laesst (tiefeUnten .62, kanteUnten .55),
#      bekommt die obere Haelfte fast geschenkt: 72,9 auf 91,7
#      Prozent, waehrend der Kontrast unterm Text kaum nachgibt.
#
#      SACKGASSE, weil zuerst versucht: den Schatten der Schrift
#      staerker machen und dafuer die Auflage wegnehmen. In Chromium
#      ueber echten Text gemessen, Ring um die Glyphen:
#
#          Grund 190   Deckkraft 0,50 blur 30   2,3:1
#                      Deckkraft 0,95 blur 56   2,5:1
#                      Deckkraft 0,80 blur  8   2,6:1
#
#      Von 0,50 auf 0,95 kauft 0,2 Stufen. Ein weicher Schatten
#      verteilt das Dunkel so duenn, dass direkt neben der Glyphe fast
#      nichts ankommt, und ein harter sieht aus wie eine Kontur.
#      Der Schatten ist hier kein Hebel — deshalb gar nicht angefasst.
#
#      Geaendert sind vier Zahlen im dunklen Aufsatz:
#
#          bildSchleier  .10 -> 0
#          tiefeOben     .06 -> 0
#          tiefeMitte    .10 -> 0
#          kanteOben     .30 -> .06
#
#      tiefeUnten und kanteUnten bleiben, wo sie waren: sie sind der
#      Grund, auf dem die Schrift steht.


# 124 — Ein weicher Fleck unter dem Text, damit der Fuss weg kann.
#      Carina: "Text geht jetzt unter das ist bloed also bitte unter
#      dem Text blurred shadow und bitte weniger Schwarzwerden."
#
#      Beides zusammen geht nur, wenn das Dunkel dorthin wandert, wo
#      der Text steht, statt ueber der halben Kachel zu liegen. Der
#      Fuss aus 123 (tiefeUnten .62, kanteUnten .55) deckt die untere
#      Haelfte ab, egal ob dort drei Zeilen stehen oder sechs.
#
#      Neu: nach dem Zeichnen des Textes wird sein tatsaechlicher
#      Kasten ausgemessen — ueber getBoundingRect aller Objekte, die
#      seit zIdx dazugekommen sind — und ein weicher ovaler Verlauf
#      genau darum gelegt. Mit insertAt an die Stelle zIdx, also UNTER
#      den Text und UEBER das Foto.
#
#      Ausmessen statt rechnen ist hier wichtig: bei geteilten Kacheln
#      springt De mitten in der Schleife (geteiltOben/geteiltUnten),
#      und der Zweittext haengt noch hinten dran. Der Kasten kennt das
#      Ergebnis, die Formel vorher nicht.
#
#      Der Verlauf ist ein Kreis, den gradientTransform zur Ellipse
#      zieht: [rx,0,0,ry,cx,cy] auf coords r1 0, r2 1. Die Stufen
#      bilden eine Glaettung nach (1, .84, .5, .16, 0), damit keine
#      Kante sichtbar wird.
#
#      Ueber alle neun Kacheln gemessen:
#
#                              Foto  obere    Kontrast unterm
#                            gesamt Haelfte   Text (schlecht. 5 %)
#          karten183          59,8 %  72,9 %        3,7:1
#          karten184          74,0 %  91,7 %        2,7:1
#          jetzt              75,3 %  92,3 %        3,8:1
#
#      Der Fuss faellt von .62 auf .12 und von .55 auf .15 — und der
#      Text steht trotzdem besser da als vor allem hier, weil das
#      Dunkel jetzt dort liegt, wo er ist.
#
#      In fabric 5.5.2 der laufenden App nachgeprueft: insertAt gibt
#      es, und die Ellipse sitzt auf dem gemessenen Kasten
#      (Helligkeit Textmitte 21, Bild oben 161).
#
#      bildTextFleck 0 schaltet ihn ab. bildTextFleckLuft (.15 von der
#      Hoehe) und bildTextFleckBreite (.20 von der Breite) sagen, wie
#      weit er ueber den Text hinausreicht.



# 125 — Zurueck auf den Stand von 183. Carina: "Ok nein zurueck zu vor
#      2 Aenderungen oder 3."
#
#      Zwei zurueck heisst 183, drei zurueck heisst 182. Der
#      Unterschied zwischen beiden ist folgeFuss — die feste
#      Unterkante auf den Folgeslides aus 122, die sie selbst
#      angefragt hat. Also 183: die beiden Schritte an der Auflage
#      fallen weg, die feste Hoehe bleibt.
#
#      Damit sind wieder da:
#
#          bildSchleier  .10        (war 0)
#          tiefeOben     .06        (war 0)
#          tiefeMitte    .10        (war 0)
#          tiefeUnten    .62        (war .12)
#          kanteOben     .30        (war .06)
#          kanteUnten    .55        (war .15)
#
#      Und wieder weg ist der weiche Fleck unter dem Text samt seinem
#      zIdx-Merker. Der Code dafuer steht nicht mehr im Bundle; er ist
#      in 124 vollstaendig aufgeschrieben, falls er zurueckkommen soll.
#
#      Geblieben ist alles bis 183: Schwarzpunkt .07, Farbschicht,
#      Vignette .6, Textsitz .73, folgeFuss .86, keine Wortmarke.
#
#      Gemacht als neue Datei karten186 mit dem Inhalt von 183, nicht
#      als Rueckbau: die alten Namen bleiben Weiterleitungen, und
#      niemand faengt sich eine weisse Seite ein, weil sein Browser
#      noch die alte index.html im Speicher hat.


# 126 — Nicht jede Kachel gleich. Carina: "Ich glaube sowas brauchen
#      wir ja aber nicht fuer alle. Also ich sehe ein paar die sind
#      geil aber die kommen nur wenn daneben was ist mit overlay und
#      ohne Vignette oder so."
#
#      Das ist keine Zahl, das ist ein Rhythmus. Eine offene Kachel
#      wirkt offen, weil neben ihr eine geschlossene liegt. Bisher
#      bekam jede dieselbe Auflage.
#
#      Zwei Reihen, getrennt, weil sie "mit overlay und ohne Vignette"
#      als eigene Kombination genannt hat:
#
#          auflageReihe    "1|0.2|0.65|0.35"   mal bildSchleier,
#                                              tiefe*, kante*
#          vignetteReihe   "1|0|0.55|0.25"     mal bildVignette
#          auflageWechsel  1                   nach Tagesnummer
#
#      Vier Eintraege, nicht drei. Drei waere die Spaltenzahl des
#      Rasters — dann stuende in jeder Spalte immer derselbe Wert und
#      es gaebe senkrechte Streifen. Vier ist teilerfremd zu drei, der
#      Rhythmus laeuft diagonal:
#
#          T 1 A0.2   T 2 A0.65  T 3 A0.35
#          T 4 A1     T 5 A0.2   T 6 A0.65
#          T 7 A0.35  T 8 A1     T 9 A0.2
#
#      Jede Spalte traegt alle vier Staerken. Neben jeder offenen
#      Kachel liegt eine geschlossene.
#
#      NEBENWIRKUNG, absichtlich: saettigungReihe hat zwei Eintraege,
#      auflageReihe vier. Das laeuft im Gleichtakt — die Farbkacheln
#      bekommen immer die leichte Auflage, die Schwarzweisskacheln
#      immer die schwere. Sieht gut aus (offen und farbig gegen
#      geschlossen und grau), ist aber eine feste Kopplung. Ein
#      fuenfter Eintrag in einer der beiden Reihen loest sie.
#
#      BS_REIHE ist die Mechanik aus 116, jetzt als eigene Funktion:
#      Tagesnummer wenn vorhanden, sonst Hash. Ohne Reihe im Aufsatz
#      kommt 1 zurueck und nichts aendert sich — der warme Feed
#      bleibt unberuehrt.

P.append(('const BS_MISCHBAR=',
 'const BS_REIHE=(zl,zw,zt,zs)=>{try{const za=String(zl||"").split("|").filter(zx=>zx!=="");'
 'if(!za.length)return null;'
 'if(zw&&typeof zt=="number"){const zv=parseFloat(za[((zt%za.length)+za.length)%za.length]);return isNaN(zv)?null:zv}'
 'const zq=String(zs||"");let zh=0;for(let zi=0;zi<zq.length;zi+=1)zh=(zh*31+zq.charCodeAt(zi))%99991;'
 'const zv=parseFloat(za[(zh*7+5)%za.length]);return isNaN(zv)?null:zv}catch(zz){return null}};'
 'const BS_MISCHBAR=',
 "BS_REIHE: eine Reihe je Kachel lesen", 1))

P.append(('}catch(zz){return BS_KACHEL.bildTon}})();',
 '}catch(zz){return BS_KACHEL.bildTon}})();'
 'const zSaat=String(t.background||"")+"|"+String(t.text||"");'
 'let zAuf=(()=>{const zv=BS_REIHE(BS_KACHEL.auflageReihe,BS_KACHEL.auflageWechsel,t._tag,zSaat);return zv==null?1:zv})();'
 'const zVig=(()=>{const zv=BS_REIHE(BS_KACHEL.vignetteReihe,BS_KACHEL.auflageWechsel,t._tag,zSaat+"|v");return zv==null?1:zv})();',
 "zAuf und zVig je Kachel", 1))

P.append(('fill:`rgba(${zTon||"0,0,0"},${Et})`,selectable:!1});',
 'fill:`rgba(${zTon||"0,0,0"},${Et*zAuf})`,selectable:!1});',
 "Schleier mal zAuf", 1))

P.append(('colorStops:[{offset:0,color:`rgba(${zTon},${BS_KACHEL.tiefeOben})`},{offset:.45,color:`rgba(${zTon},${BS_KACHEL.tiefeMitte})`},{offset:1,color:`rgba(${zTon},${BS_KACHEL.tiefeUnten})`}]',
 'colorStops:[{offset:0,color:`rgba(${zTon},${BS_KACHEL.tiefeOben*zAuf})`},'
 '{offset:(BS_KACHEL.tiefeKnick==null?.45:BS_KACHEL.tiefeKnick),color:`rgba(${zTon},${BS_KACHEL.tiefeMitte*zAuf})`},'
 '{offset:(BS_KACHEL.tiefeKnickUnten==null?.999:BS_KACHEL.tiefeKnickUnten),color:`rgba(${zTon},${BS_KACHEL.tiefeUnten*zAuf})`},'
 '{offset:1,color:`rgba(${zTon},${BS_KACHEL.tiefeUnten*zAuf})`}]',
 "Tiefe mal zAuf, mit zwei Knicken", 1))

P.append(('colorStops:[{offset:0,color:`rgba(${zTon},${BS_KACHEL.kanteOben})`},{offset:.18,color:`rgba(${zTon},0.0)`},{offset:.82,color:`rgba(${zTon},0.0)`},{offset:1,color:`rgba(${zTon},${BS_KACHEL.kanteUnten})`}]',
 'colorStops:[{offset:0,color:`rgba(${zTon},${BS_KACHEL.kanteOben*zAuf})`},{offset:.18,color:`rgba(${zTon},0.0)`},{offset:.82,color:`rgba(${zTon},0.0)`},{offset:1,color:`rgba(${zTon},${BS_KACHEL.kanteUnten*zAuf})`}]',
 "Kante mal zAuf", 1))

P.append(('const zVi=Number(BS_KACHEL.bildVignette)||0;',
 'const zVi=(Number(BS_KACHEL.bildVignette)||0)*zVig;',
 "Vignette mal zVig", 1))


# 127 — Die Auflage faengt erst beim Text an. Carina: "Nicht vor dem
#      Text das overlay."
#
#      Erst nachgesehen, ob wirklich etwas VOR dem Text liegt: nein.
#      Alle e.add-Aufrufe zwischen Textschleife und renderAll sind
#      Text selbst; die Platte je Zeile steht davor, nicht danach, und
#      auf Fotokacheln laeuft sie ohnehin nicht (ge). Die Reihenfolge
#      stimmt.
#
#      Gemeint ist also: der Verlauf faengt oberhalb des Textes an.
#      Der Text sitzt ab 0,58; der Verlauf lief seit 0,45 — er
#      verdunkelt also ein Stueck Bild, das gar keine Schrift traegt.
#
#      Der Verlauf hatte drei Stufen (0 / 0,45 / 1) und stieg von der
#      Mitte bis zur Unterkante linear an. Jetzt vier:
#
#          0                 tiefeOben        0
#          tiefeKnick        tiefeMitte       0     bei .52
#          tiefeKnickUnten   tiefeUnten     .45     bei .68
#          1                 tiefeUnten     .45
#
#      Also: bis 52 Prozent gar nichts, bis 68 Prozent aufsteigen,
#      danach stehen bleiben. Ohne die beiden neuen Felder bleibt es
#      bei drei Stufen (.45 und .999 als Vorgabe), der warme Feed
#      merkt nichts.
#
#      Das ist auf BEIDEN Seiten besser, nicht ein Tausch:
#
#                          Foto  ueber dem   Kontrast unterm
#                        gesamt   Text       Text (schlecht. 5 %)
#          vorher         59,8 %   72,9 %          3,7:1
#          jetzt          68,0 %   85,6 %          3,8:1
#
#      Weil dieselbe Menge Dunkel jetzt dort liegt, wo sie gebraucht
#      wird, statt ueber die halbe Kachel verteilt zu sein. Dadurch
#      war Luft, auch den Rest zu senken: bildSchleier .10 auf .06,
#      kanteOben .30 auf .16, kanteUnten .55 auf .35, tiefeUnten .62
#      auf .45.
#
#      In fabric 5.5.2 der laufenden App nachgemessen, ob vier Stufen
#      mit eigenen Offsets so fallen wie gerechnet — bei 0,52 noch
#      255, bei 0,60 dann 200 (gerechnet 201), ab 0,68 konstant 146.


# 128 — Die Auflage richtet sich nach dem Foto. Carina: "Es gibt hier
#      einige die passen aber es gibt welche da geht der Text unter
#      wegen den Farben und der fehlenden Tiefe."
#
#      Der Rhythmus aus 126 wuerfelt die Staerke nach der Tagesnummer
#      — er weiss nichts darueber, WAS auf dem Foto liegt. Auf einer
#      hellen Wand mit Faktor 0,2 steht weisse Schrift auf 1,2:1. Das
#      ist die Ursache, nicht die Zahl.
#
#      Jetzt wird vor dem Zeichnen nachgesehen. Auf einer 96 Pixel
#      breiten Miniatur wird das Band, in dem der Text landet
#      (textMesseOben .55 bis textMesseUnten .92, mittlere 80 Prozent
#      der Breite), durch den Schwarzpunkt gerechnet, und dann sucht
#      eine Halbierung den KLEINSTEN Faktor, bei dem das 95. Quantil
#      des Bandes noch textGrundZiel (4:1) gegen Weiss haelt.
#
#      Gerechnet wird mit genau der Verlaufsform, die spaeter
#      gezeichnet wird — dieselben vier Stufen, dieselbe Kante. Keine
#      Naeherung ueber einen Mittelwert: bei einem Verlauf, der erst
#      bei 0,52 anfaengt, sagt ein Mittelwert nichts ueber die obere
#      Textzeile.
#
#      zAuf = max(Rhythmus, gemessen). Der Rhythmus bleibt also die
#      Untergrenze fuer dunkle Fotos, und helle bekommen so viel, wie
#      sie brauchen. textGrundMax 1.8 deckelt nach oben.
#
#      Ueber die neun Kacheln, mit aus den Kachelbildern
#      zurueckgerechneten Fotos:
#
#                          schlechteste  Mittel  mittlerer Faktor
#          nur Rhythmus         1,2:1     2,7:1        0,55
#          mit Messung          2,7:1     4,5:1        1,22
#
#      Der Messblock laeuft in einer eigenen Klammer mit try/catch:
#      schlaegt getImageData fehl, bleibt es beim Rhythmus. Ohne
#      textGrundZiel im Aufsatz passiert gar nichts.
#
#      In Chromium mit genau diesem Block gegen die neun Bilder
#      laufen lassen: keine Fehler, Faktoren monoton, dunkle Kacheln
#      bleiben beim Rhythmus (k1 0,20 bleibt 0,20), helle steigen
#      (k5 0,20 auf 1,17).

P.append(('const ur=new Pe.fabric.Rect(',
 'try{const zZiel=Number(BS_KACHEL.textGrundZiel)||0;if(zZiel>0&&t.background){const zel=me.getElement&&me.getElement();if(zel&&zel.width){const zbr=96,zsk=Math.min(1,zbr/Math.max(zel.width,zel.height));const zc=document.createElement("canvas");zc.width=Math.max(8,Math.round(zel.width*zsk));zc.height=Math.max(8,Math.round(zel.height*zsk));const zx=zc.getContext("2d",{willReadFrequently:!0});zx.drawImage(zel,0,0,zc.width,zc.height);const zo=Math.floor(zc.height*(BS_KACHEL.textMesseOben==null?.55:BS_KACHEL.textMesseOben)),zu=Math.min(zc.height,Math.ceil(zc.height*(BS_KACHEL.textMesseUnten==null?.92:BS_KACHEL.textMesseUnten))),zli=Math.floor(zc.width*.1),zbre=Math.max(1,Math.ceil(zc.width*.8));const zdd=zx.getImageData(zli,zo,zbre,Math.max(1,zu-zo)).data;const zPu=Number(BS_KACHEL.bildSchwarzpunkt)||0,zgg=1-zPu;const zTa=String(zTon||"13,13,13").split(",").map(zv2=>parseFloat(zv2)||0);const zTl=.2126*(zTa[0]||13)+.7152*(zTa[1]||13)+.0722*(zTa[2]||13);const zPk=[],zYy=[];for(let zi=0,zj=0;zi<zdd.length;zi+=4,zj++){let zL=.2126*zdd[zi]+.7152*zdd[zi+1]+.0722*zdd[zi+2];if(zPu>0)zL=255*Math.max(0,Math.min(1,1-Math.min(1,(1-zL/255)/zgg)));zPk.push(zL);zYy.push((zo+Math.floor(zj/zbre))/zc.height)}const zSt=[[0,Number(BS_KACHEL.tiefeOben)||0],[BS_KACHEL.tiefeKnick==null?.45:Number(BS_KACHEL.tiefeKnick),Number(BS_KACHEL.tiefeMitte)||0],[BS_KACHEL.tiefeKnickUnten==null?.999:Number(BS_KACHEL.tiefeKnickUnten),Number(BS_KACHEL.tiefeUnten)||0],[1,Number(BS_KACHEL.tiefeUnten)||0]];const zIp=zy=>{for(let zi=1;zi<zSt.length;zi+=1){if(zy<=zSt[zi][0]){const zx0=zSt[zi-1][0],zy0=zSt[zi-1][1],zx1=zSt[zi][0],zy1=zSt[zi][1];return zx1===zx0?zy1:zy0+(zy1-zy0)*(zy-zx0)/(zx1-zx0)}}return zSt[zSt.length-1][1]};const zSchl=Number(BS_KACHEL.bildSchleier)||0,zKo=Number(BS_KACHEL.kanteOben)||0,zKu=Number(BS_KACHEL.kanteUnten)||0;const zAl=(zy,zf)=>{const zt2=zIp(zy)*zf,zk2=zy<=.18?zKo*zf*(1-zy/.18):(zy>=.82?zKu*zf*((zy-.82)/.18):0);return 1-(1-zSchl*zf)*(1-zt2)*(1-zk2)};const zQu=BS_KACHEL.textGrundQuantil==null?.95:Number(BS_KACHEL.textGrundQuantil);const zKn=zf=>{const zA2=[];for(let zi=0;zi<zPk.length;zi+=1){const za=zAl(zYy[zi],zf);zA2.push(zPk[zi]*(1-za)+zTl*za)}zA2.sort((za,zb)=>za-zb);const zv=zA2[Math.floor((zA2.length-1)*zQu)]/255,zY=zv<=.04045?zv/12.92:Math.pow((zv+.055)/1.055,2.4);return 1.05/(zY+.05)};const zMx=Number(BS_KACHEL.textGrundMax)||1.8;let zN=0;if(zKn(0)<zZiel){if(zKn(zMx)<zZiel)zN=zMx;else{let zlo=0,zhi=zMx;for(let zi=0;zi<16;zi+=1){const zm=(zlo+zhi)/2;zKn(zm)>=zZiel?zhi=zm:zlo=zm}zN=zhi}}if(zN>zAuf)zAuf=zN}}}catch(zz){}'
 'const ur=new Pe.fabric.Rect(',
 "Grund unterm Text messen und die Auflage anheben", 1))


# 129 — Nur noch zwei Lagen. Carina: "Text nur mehr entweder mittig
#      oder unten."
#
#      Woher "oben" kam: lagenWechsel wuerfelt aus einer im Code fest
#      verdrahteten Liste.
#
#          const zL=["unten","mitte","oben"][zh%3]
#
#      Die Liste ist jetzt lagenReihe, im dunklen Aufsatz
#      "unten|mitte". Dazu eine Klammer um das ganze ve, die auch von
#      aussen gesetzte Lagen (t.textLage, t.textAnchor.row) auf die
#      erlaubten zieht — sonst kaeme "oben" durch die Hintertuer.
#
#      In node ueber 600 Kacheln: 302 unten, 298 mitte, 0 oben. Eine
#      Kachel mit textLage "oben" landet auf mitte. Ohne lagenReihe
#      (warmer Feed) bleibt alles wie es war, auch "oben".
#
#      ZWEITE HAELFTE, sonst waere es keine Aenderung: die beiden
#      Lagen lagen praktisch aufeinander. "unten" stand fest im Code
#      auf .7, "mitte" kam aus textMitte und war seit 178 auf .73 —
#      drei Hundertstel Unterschied, im Bild nicht zu sehen. Beide
#      sind jetzt Felder:
#
#          textLageUnten  .80    Block etwa .72 bis .88
#          textMitte      .58    Block etwa .50 bis .66
#
#      textMesseOben wandert von .55 auf .52. Nicht hoeher: der
#      Verlauf faengt bei tiefeKnick .52 an, und was darueber liegt,
#      kann kein Faktor abdunkeln — die Suche aus 128 wuerde dann bei
#      jeder helleren Kachel am Anschlag landen, statt zu messen.

P.append(('const zL=["unten","mitte","oben"][zh%3];',
 'const zLl=String(BS_KACHEL.lagenReihe||"unten|mitte|oben").split("|").filter(zx=>zx!=="");'
 'const zL=zLl[zh%zLl.length];',
 "Lagen kommen aus lagenReihe", 1))

P.append(('const ve=(()=>{const zA=(tt.fettNurErste',
 'const ve=(zv=>{try{const zLe=String(BS_KACHEL.lagenReihe||"").split("|").filter(zx=>zx!=="");'
 'if(!zLe.length||zLe.indexOf(zv)>=0)return zv;'
 'return zLe.indexOf("mitte")>=0?"mitte":zLe[0]}catch(zz){return zv}})((()=>{const zA=(tt.fettNurErste',
 "erlaubte Lagen erzwingen (Anfang)", 1))

P.append(('return zG.some(zz=>Math.floor(zz/3)===zR)?zAus:zL})(),He=tt.istKarte?',
 'return zG.some(zz=>Math.floor(zz/3)===zR)?zAus:zL})()),He=tt.istKarte?',
 "erlaubte Lagen erzwingen (Ende)", 1))

P.append(('He=tt.istKarte?.42:ve==="oben"?.24:ve==="unten"?.7:(BS_KACHEL.textMitte||.5)',
 'He=tt.istKarte?.42:ve==="oben"?(BS_KACHEL.textLageOben||.24):'
 've==="unten"?(BS_KACHEL.textLageUnten||.7):(BS_KACHEL.textMitte||.5)',
 "Lagenhoehen aus dem Block", 1))


# 130 — Alles unten, und ein Regler fuer das Schwarz. Carina: "Da sind
#      welche zu hoch platziere alle unten und ich stell sie hoeher
#      wenn's geht aber das schwarz ist manchmal zu stark kannst du
#      mich das auch einstellen lassen."
#
#      Erstes: lagenReihe von "unten|mitte" auf "unten". In node ueber
#      600 Kacheln: 600 unten. Auch eine Kachel mit textLage "oben"
#      oder "mitte" landet unten, weil die Klammer aus 129 alles auf
#      die erlaubte Liste zieht. Der warme Feed hat keine lagenReihe
#      und bleibt, wie er war.
#
#      Zweites: ein Regler. Die Kacheln liegen als fertige Canvas da —
#      eine Zahl im Block zu aendern zeichnet nichts neu. Also merkt
#      der Regler den Wert und laedt die Seite neu; die index.html
#      reicht ihn VOR dem Modul als window.BS_SCHWARZ weiter (der
#      Zeichner liest ihn schon bei der ersten Kachel), und im
#      Zeichner multipliziert zSw beides:
#
#          zVig  = Reihenwert * zSw
#          zAuf  = ... * zSw     ganz zuletzt
#
#      "Ganz zuletzt" ist wichtig: die Messung aus 128 hebt zAuf an,
#      damit der Text lesbar bleibt. Stuende der Regler davor, koennte
#      sie ihn ueberstimmen und der Regler waere auf hellen Fotos
#      wirkungslos. So gewinnt immer die Handeinstellung — auf 0
#      Prozent liegt gar nichts mehr auf dem Foto, auch wenn der Text
#      dann verschwindet. Das ist ihre Entscheidung, nicht meine.
#
#      Der Regler haengt wie der Stil-Schalter am body, nicht in der
#      React-App, und reagiert auf "change" statt "input" — sonst
#      wuerde die Seite waehrend des Schiebens bei jedem Pixel neu
#      laden.
#
#      In Chromium durchgespielt: Regler da, Startwert 100 Prozent,
#      nach dem Schieben auf 60 steht 0.6 im Speicher, window.
#      BS_SCHWARZ ist 0.6 und der Regler zeigt wieder 60 Prozent.
#      Zurueck auf 100 loescht den Eintrag. Keine Seitenfehler.

P.append(('const zSaat=String(t.background||"")+"|"+String(t.text||"");',
 'const zSw=(()=>{try{if(typeof window>"u")return 1;'
 'const zk=window.BS_SCHWARZ_TAG;'
 'if(zk&&typeof t._tag=="number"){const ze=parseFloat(zk[String(t._tag)]);if(isFinite(ze)&&ze>=0)return ze}'
 'const zv=parseFloat(window.BS_SCHWARZ);if(isFinite(zv)&&zv>=0)return zv;'
 'const zg=Number(BS_KACHEL.schwarzGrund);return isFinite(zg)&&zg>=0?zg:1}catch(zz){return 1}})();'
 'const zSaat=String(t.background||"")+"|"+String(t.text||"");',
 "zSw: der Regler, je Tag oder allgemein", 1))

P.append(('const zVig=(()=>{const zv=BS_REIHE(BS_KACHEL.vignetteReihe,BS_KACHEL.auflageWechsel,t._tag,zSaat+"|v");return zv==null?1:zv})();',
 'const zVig=(()=>{const zv=BS_REIHE(BS_KACHEL.vignetteReihe,BS_KACHEL.auflageWechsel,t._tag,zSaat+"|v");return (zv==null?1:zv)*zSw})();',
 "Vignette folgt dem Regler", 1))

P.append(('if(zN>zAuf)zAuf=zN}}}catch(zz){}const ur=new Pe.fabric.Rect(',
 'if(zN>zAuf)zAuf=zN}}}catch(zz){}zAuf*=zSw;const ur=new Pe.fabric.Rect(',
 "Auflage folgt dem Regler, nach der Messung", 1))


# 131 — Nachgemessen: unten ja, oben nein. Carina: "Ich glaube bei ihr
#      ist oben und unten schwarzes Band."
#
#      Unten stimmt, oben nicht. Zeilenmedian je Kachel des Vorbilds,
#      damit die Schrift nicht dazwischenfunkt, ueber die zwoelf
#      sichtbaren Kacheln:
#
#          unterste 24 Zeilen   Mittel 5 bis 38, meist unter 30
#          oberste 24 Zeilen    Kachel 1: 129, Kachel 2: 143,
#                               Kachel 9: 209
#
#      Jede Kachel wird unten dunkel, keine einzige hat oben etwas,
#      das nicht das Foto selbst waere. Die dunklen Oberkanten (3, 4,
#      5, 6, 8) sind dunkle Fotos.
#
#      Und es ist kein Band mit Kante, sondern ein Verlauf. Kachel 1
#      auf den letzten 60 Zeilen: 32, 29, 25, 21, 16, 12, 5, 3, 3, 3.
#
#      Ueber die sieben Kacheln, deren Foto dort hell genug ist, um
#      den Abfall ueberhaupt zu sehen, auf den Wert bei 0,72
#      bezogen — das ist die noetige Deckkraft:
#
#          Anteil  0,70  0,75  0,80  0,84  0,88  0,92  0,96  0,98
#          Alpha   0,00  0,06  0,22  0,33  0,52  0,66  0,75  0,79
#
#      Also: bis etwa 0,73 nichts, dann fast gerade auf ~0,80 an der
#      Unterkante. Unser Fuss lief flacher und begann frueher — bei
#      0,75 lagen wir schon auf 0,45, wo das Vorbild 0,06 hat, und an
#      der Unterkante nur auf 0,64.
#
#      Vier Zahlen, kein Code:
#
#          tiefeKnick       .52 -> .60     mit tiefeMitte .08 als
#                                          kleinem Sockel, damit die
#                                          erste Textzeile nicht voellig
#                                          nackt steht
#          tiefeKnickUnten  .68 -> .999    eine gerade Rampe statt
#                                          Plateau
#          tiefeUnten       .45 -> .85
#          kanteUnten       .35 -> 0       die Rampe macht das allein
#
#      textMesseOben wandert mit, .52 auf .60: die Messung aus 128
#      darf nur dort suchen, wo der Verlauf ueberhaupt wirkt.
#
#      Nachgerechnet ueber die neun Kacheln: schlechtester Kontrast
#      unterm Text 4,1:1 (vorher 5,2:1), Mittel 8,2:1. Das Band ist
#      deutlich staerker und der Text bleibt trotzdem gut lesbar,
#      weil beides jetzt an derselben Stelle sitzt.


# 132 — Schwarz je Kachel, und ein Band auch oben. Carina: "Schwarz
#      pro Bild und bitte oben unten schwarz wie Julia".
#
#      OBEN. Ich hatte in 131 gemessen, dass das Vorbild oben KEIN
#      Band hat (oberste 24 Zeilen: 129, 143, 209 bei den hellen
#      Fotos) — dort ist es das Foto selbst, das dunkel ist. Sie will
#      es trotzdem, und das ist ihre Entscheidung; der Messwert steht
#      in 131, falls sie es wieder abschalten will.
#
#      Der Verlauf hat jetzt fuenf Stufen statt vier:
#
#          0                 tiefeOben       .55
#          tiefeKnickOben    tiefeMitte      .08   bei .16
#          tiefeKnick        tiefeMitte      .08   bei .60
#          tiefeKnickUnten   tiefeUnten      .85   bei .999
#          1                 tiefeUnten      .85
#
#      kanteOben faellt auf 0 — sonst lagen zwei Rampen uebereinander
#      und die Oberkante haette 1-(1-.55)(1-.16) = .62 statt .55.
#      Ein Regler, nicht zwei.
#
#      Die neue Stufe muss AN ZWEI STELLEN stehen: im gezeichneten
#      Verlauf und in zSt, dem Modell, mit dem die Messung aus 128
#      sucht. Stuenden sie auseinander, wuerde die Messung mit einem
#      Verlauf rechnen, den es nicht gibt.
#
#      SCHWARZ JE KACHEL. window.BS_SCHWARZ_TAG ist ein flaches
#      Objekt, {"47":0.4}. Der Zeichner sucht darin seine eigene
#      Tagesnummer (t._tag, seit 116 auf jeder Folie) und faellt sonst
#      auf den allgemeinen Wert zurueck.
#
#      Die Bedienung sitzt im selben Schildchen wie der Stil-Schalter,
#      am body, nicht in der React-App. Welche Kachel gemeint ist,
#      liest sie aus dem DOM: von der angetippten Stelle nach oben
#      gehen und im ersten Vorfahren, der ein Schildchen "Tag 47"
#      enthaelt, die Nummer nehmen. Der Zuhoerer laeuft in der
#      capture-Phase und ruft kein preventDefault — die Kachel geht
#      trotzdem auf, er hoert nur mit.
#
#      Die Auswahl ueberlebt das Neuladen (BS_SCHWARZ_WAHL), sonst
#      muesste man nach jeder Reglerbewegung wieder antippen. Steht
#      der Regler wieder auf dem allgemeinen Wert, faellt der Eintrag
#      raus statt als Ausnahme stehenzubleiben.
#
#      In Chromium durchgespielt: Klick auf eine Kachel mit "Tag 47"
#      setzt die Anzeige auf "Tag 47", Regler auf 40 speichert
#      {"47":0.4}, nach dem Neuladen steht window.BS_SCHWARZ_TAG so in
#      der Seite und der Regler zeigt wieder 40 Prozent. "alle"
#      schaltet ohne Neuladen zurueck und laesst die Ausnahme stehen.
#      Keine Seitenfehler.

P.append(('{offset:(BS_KACHEL.tiefeKnick==null?.45:BS_KACHEL.tiefeKnick),color:`rgba(${zTon},${BS_KACHEL.tiefeMitte*zAuf})`},',
 '{offset:(BS_KACHEL.tiefeKnickOben==null?0:BS_KACHEL.tiefeKnickOben),color:`rgba(${zTon},${BS_KACHEL.tiefeMitte*zAuf})`},'
 '{offset:(BS_KACHEL.tiefeKnick==null?.45:BS_KACHEL.tiefeKnick),color:`rgba(${zTon},${BS_KACHEL.tiefeMitte*zAuf})`},',
 "Rampe oben im Verlauf", 1))

P.append(('const zSt=[[0,Number(BS_KACHEL.tiefeOben)||0],',
 'const zSt=[[0,Number(BS_KACHEL.tiefeOben)||0],'
 '[BS_KACHEL.tiefeKnickOben==null?0:Number(BS_KACHEL.tiefeKnickOben),Number(BS_KACHEL.tiefeMitte)||0],',
 "Rampe oben auch in der Messung", 1))


# 133 — Das Grundoverlay steht auf 20 Prozent. Carina: "Ich seh wenn
#      ich den neuen Schalter auf 20% stell sind viele super und die
#      paar die nicht gehen wuerden einen schwaerzeren Helferbalken
#      kriegen also bitte stell die Grundoverlay auf 20% verstellbar
#      und dann pro Kachel verstellbar und oben und unten schwarz
#      vinette."
#
#      Sie hat den Wert selbst gefunden. Bleibt nur, ihn zur Vorgabe
#      zu machen, ohne dass sich bei ihr etwas ruckt.
#
#      NICHT gemacht: die Zahlen im Block mit 0,2 durchmultiplizieren.
#      Dann waere ihre gespeicherte 0,2 auf die neuen Zahlen gefallen
#      und sie saehe ploetzlich 4 Prozent — und dasselbe waere mit
#      jeder Ausnahme je Kachel passiert. Eine Wanderung dafuer zu
#      bauen waere Arbeit fuer einen Fehler, den man auch weglassen
#      kann.
#
#      Stattdessen: schwarzGrund .2 im Aufsatz, und zSw faellt darauf
#      zurueck, wenn nichts gespeichert ist. Ihre 0,2 bedeutet damit
#      genau dasselbe wie die neue Vorgabe — es ruckt nichts.
#
#      Der Regler haengt am body und kennt BS_KACHEL nicht. Damit die
#      Zahl nicht zweimal im Projekt steht, hinterlegt der Zeichner
#      sie direkt nach dem Aufsatz als window.BS_GRUND, und der Regler
#      liest sie dort.
#
#      "Standard" heisst im Regler jetzt der Grundwert: schiebt man
#      auf 20 Prozent, faellt der gespeicherte Eintrag raus, statt als
#      Ausnahme stehenzubleiben.
#
#      Pro Kachel verstellbar war schon da (132), die Baender oben und
#      unten auch (132/131). Sie folgen dem Regler mit, sind also bei
#      20 Prozent der Helferbalken, den sie meint: fuer eine einzelne
#      Kachel hochdrehen und der Balken wird schwaerzer.
#
#      In Chromium durchgespielt: frisch zeigt der Regler 20 Prozent
#      und im Speicher steht nichts; mit ihrer alten 0,2 zeigt er
#      ebenfalls 20 und nichts springt; auf 20 gestellt loescht den
#      Eintrag; auf 60 speichert 0.6. Keine Seitenfehler.

P.append(('if(typeof window<"u"&&window.BS_STIL==="dunkel")Object.assign(BS_KACHEL,BS_DUNKEL);',
 'if(typeof window<"u"&&window.BS_STIL==="dunkel")Object.assign(BS_KACHEL,BS_DUNKEL);'
 'try{if(typeof window<"u"){const zg=Number(BS_KACHEL.schwarzGrund);window.BS_GRUND=isFinite(zg)&&zg>=0?zg:1}}catch(zz){}',
 "Grundwert fuer den Regler hinterlegen", 1))


# 134 — Die Handschrift 20 Prozent groesser. Carina: "Okay jetzt das
#      Handwritten noch 20% groesser".
#
#      Die Handschrift steht an zwei Stellen im Bild, und beide haengen
#      an einer anderen Zahl:
#
#          zweiter Block auf dem Deckblatt   qe * zweitAnteil (.62)
#          Versalkacheln, ganze Kachel       r * versalGroesse (.065)
#
#      An zweitAnteil zu drehen waere falsch gewesen: dieselbe Zahl
#      bestimmt auch den zweiten Block auf den FOLGESLIDES, und der ist
#      keine Handschrift, sondern folgeFamilie — die Serife. Die haette
#      dann mit vergroessert.
#
#      Deshalb ein eigener Faktor handGroesse (1.2), der nur greift,
#      wo auch wirklich Handschrift steht. Die Bedingung ist dieselbe,
#      nach der weiter unten die Schriftfamilie gewaehlt wird:
#
#          zVS || !(t.folienRolle && t.folienRolle !== "deckblatt")
#
#      Also: Versalkachel, oder Deckblatt beziehungsweise gar keine
#      Rolle. Nachgerechnet:
#
#          Deckblatt, zweiter Block   62 -> 74
#          ohne folienRolle           62 -> 74
#          Folgeslide (DM Serif)      62 -> 62     bleibt
#          Versalkachel              100 -> 120
#          versalGroesse            .065 -> .078
#
#      handAnteil (1.15) bleibt, wie es ist: das ist das Verhaeltnis
#      einzelner handgeschriebener Woerter zum Text um sie herum, kein
#      absolutes Mass. Waechst der Text, wachsen sie mit.

P.append(('BS_KACHEL.versalGroesse&&(qe=Math.max(c(11),Math.round(r*BS_KACHEL.versalGroesse)))',
 'BS_KACHEL.versalGroesse&&(qe=Math.max(c(11),Math.round(r*BS_KACHEL.versalGroesse*(Number(BS_KACHEL.handGroesse)||1))))',
 "Versalgroesse mal handGroesse", 1))

P.append(('qe2=$e?Math.round(qe*((zVS&&BS_KACHEL.versalZweitAnteil)||BS_KACHEL.zweitAnteil||1)):qe',
 'qe2=$e?Math.round(qe*((zVS&&BS_KACHEL.versalZweitAnteil)||BS_KACHEL.zweitAnteil||1)'
 '*((zVS||!(t.folienRolle&&t.folienRolle!=="deckblatt"))?(Number(BS_KACHEL.handGroesse)||1):1)):qe',
 "zweiter Block mal handGroesse, nur wo er Handschrift ist", 1))


# 135 — Das Bild darf den Satz nicht mehr umwerfen. Carina: "Wenn ich
#      das Bild aendere soll die gesetzte Schrift aber gleich bleiben
#      gerade hat es sich geaendert ploetzlich nach dem neuen Bild auf
#      1. slide."
#
#      Ursache: fast jede Entscheidung im Zeichner haengt an einem
#      Hash, und der Hash lief ueber
#
#          String(t.background||"") + "|" + String(t.text||"")
#
#      Also ueber die BILDADRESSE. Neues Bild, neuer Hash, neue
#      Entscheidung — und zwei davon sind Satz, nicht Bild:
#
#          zVS   Versalien oder Serife    (versalAnteil 30)
#          zGT   geteilte Kachel          (geteiltAnteil 25)
#
#      Beide lesen jetzt nur noch String(t.text||""). Der Text ist die
#      Identitaet der Kachel, das Bild ist austauschbar.
#
#      NICHT t._tag genommen, obwohl die Tagesnummer noch stabiler
#      waere: sie steht auf den Kacheln des Rasters und auf geladenen
#      Plaenen, aber nicht sicher auf einer frisch angelegten Folie im
#      Einzelansicht-Editor. Dann saehe dieselbe Kachel im Raster
#      anders aus als im Editor — ein schlimmerer Fehler als der, den
#      wir beheben.
#
#      In node gegengerechnet, vier Bildadressen bei gleichem Text:
#      vorher sprang "geteilt" zwischen ja und nein, jetzt steht bei
#      allen vieren dasselbe.
#
#      WAS WEITER AM BILD HAENGT, mit Absicht:
#
#          zDS   der Ausschnitt (deckblattSchnitte) — ein neues Foto
#                braucht seinen eigenen Anschnitt
#          zTon  der Farbton (tonReihe) — eine Einfaerbung des Fotos,
#                kein Satz
#
#      Alles andere ist inzwischen tagesgebunden (saettigungWechsel,
#      auflageWechsel) oder abgeschaltet (saumStaerke 0, lagenReihe
#      nur "unten") und aendert sich ohnehin nicht mehr.
#
#      Nebenwirkung, einmalig: welche Kacheln Versalien bekommen und
#      welche geteilt werden, wuerfelt sich einmal neu — die
#      Verteilung bleibt (30 und 25 Prozent), aber es trifft andere.

P.append(('const zVS=(()=>{try{if(!$e||!BS_KACHEL.versalAnteil)return!1;const zs=String(t.background||"")+"|"+String(t.text||"");',
 'const zVS=(()=>{try{if(!$e||!BS_KACHEL.versalAnteil)return!1;const zs=String(t.text||"");',
 "Versalien haengen am Text, nicht am Bild", 1))

P.append(('const zGT=(BS_KACHEL.geteiltAnteil?(()=>{const zs=String(t.background||"")+"|"+String(t.text||"");',
 'const zGT=(BS_KACHEL.geteiltAnteil?(()=>{const zs=String(t.text||"");',
 "Teilung haengt am Text, nicht am Bild", 1))


# 136 — Weniger Handschrift, mehr Serife. Carina: "Verteilst du bitte
#      mehr dm serif als die Handschrift danke".
#
#      Die Handschrift uebernimmt eine ganze Kachel nur an einer
#      Stelle: versalAnteil entscheidet, ob eine Fotokachel in
#      Versalien gesetzt wird (versalFamilie, Shadows Into Light)
#      statt in DM Serif. Sonst ist die Handschrift immer nur der
#      zweite Block unter der Serifenzeile.
#
#      Der Regler tut, was draufsteht — 4000 Texte durchgerechnet:
#
#          versalAnteil 30 -> 31,6 %
#          versalAnteil 20 -> 21,4 %
#          versalAnteil 15 -> 16,2 %
#          versalAnteil 10 -> 10,6 %
#
#      Und auf ihren achtzehn echten Saetzen aus den Screenshots:
#
#          30 -> 5 von 18      15 -> 3 von 18
#
#      Warum es nach mehr aussah: der alte Hash lief noch ueber die
#      Bildadresse (bis 135), und in dem Raster, das sie zuletzt
#      geschickt hat, lagen sechs von neun Versalkacheln nebeneinander.
#      Ein Wuerfel verteilt nicht gleichmaessig, er verteilt zufaellig.
#
#      Auf 15 gesetzt. NICHT auf einen Wechsel nach Tagesnummer
#      umgestellt, obwohl das die Verteilung im Raster garantieren
#      wuerde: 135 hat die Entscheidung gerade erst an den Text
#      gehaengt, damit sie sich beim Bildwechsel nicht aendert und im
#      Editor dasselbe steht wie im Raster. Ein Tageswechsel wuerde
#      genau das wieder aufgeben.


# 138 — Der Punkt wandert ins Menue. Carina: "Doch bitte ins Menue".
#
#      Das Menue steht im Bundle als flache Liste:
#
#          a=[{path:"/",icon:b3,label:"Dashboard"}, ... ,
#             {path:"/brand-settings",icon:ux,label:"Settings"}]
#
#      Sie wird an ZWEI Stellen gezeichnet — einmal die breite Leiste,
#      einmal das aufgeklappte Menue auf schmalen Schirmen. Beide bauen
#      einen Router-Verweis (Qa mit to:). Fuer /profilbilder/ waere das
#      falsch: die Seite ist keine Route der App, der Router faende
#      nichts und zeigte eine leere Flaeche.
#
#      Deshalb traegt der neue Eintrag extern:!0, und beide
#      Zeichenstellen entscheiden danach:
#
#          v.jsxs(h.extern?"a":Qa,{[h.extern?"href":"to"]:h.path, ...
#
#      Ein echter Verweis mit href statt eines Router-Ziels — ein
#      richtiger Seitenwechsel, der auch die Regel in der netlify.toml
#      durchlaeuft.
#
#      Das Icon ist hx, dasselbe wie bei Worksheets. Die Icons kommen
#      aus einem anderen Bundle-Stueck und sind hier nur als kurze
#      Namen sichtbar; einen neuen haette ich nicht hereinholen
#      koennen, ohne den Import anzufassen.
#
#      Die Pille aus 137 am body ist wieder weg — zwei Wege zur selben
#      Seite sind einer zu viel.
#
#      In Chromium in beiden Breiten geprueft: breit steht der Eintrag
#      als <a href="/profilbilder/"> in der Leiste, schmal im
#      aufgeklappten Menue, beide sichtbar, keine Seitenfehler.

P.append(('{path:"/brand-settings",icon:ux,label:"Settings"}]',
 '{path:"/profilbilder/",icon:hx,label:"Profilbilder",extern:!0},{path:"/brand-settings",icon:ux,label:"Settings"}]',
 "Menueeintrag Profilbilder", 1))

P.append(('v.jsxs(Qa,{to:h.path,className:`flex items-center space-x-2 px-3 py-2',
 'v.jsxs(h.extern?"a":Qa,{[h.extern?"href":"to"]:h.path,className:`flex items-center space-x-2 px-3 py-2',
 "breite Ansicht: externer Eintrag als echter Verweis", 1))

P.append(('v.jsxs(Qa,{to:h.path,onClick:u,className:`flex items-center space-x-4 px-4 py-4',
 'v.jsxs(h.extern?"a":Qa,{[h.extern?"href":"to"]:h.path,onClick:u,className:`flex items-center space-x-4 px-4 py-4',
 "schmale Ansicht: externer Eintrag als echter Verweis", 1))


# 139 — Andere Handschrift fuer die Unterzeile. Carina hat aus zwoelf
#      Proben "Nothing You Could Do" gewaehlt.
#
#      Es sind zwei getrennte Felder, deshalb ging es ohne Umbau:
#
#          zweiteFamilie   die Unterzeile unter der Serife, und ueber
#                          handFamilie||zweiteFamilie auch einzelne
#                          handgeschriebene Woerter mitten im Satz
#          versalFamilie   die Versalkacheln — bleibt Shadows Into Light
#
#      Die Datei liegt im Projekt, nicht bei Google: der Zeichner MISST
#      Texte auf dem Canvas, und ueber das Netz geladen waere die
#      Schrift beim ersten Bild manchmal noch nicht da. zweiteFamilie
#      steht ohnehin schon in der Vorlade-Liste des Bundles, es war
#      also nur die Datei und eine Zeile @font-face.
#
#      DABEI EINEN ALTEN FEHLER GEFUNDEN. Die neue Schrift war
#      angemeldet, wurde aber nicht benutzt — im Browser gemessen:
#      dieselben Pixel wie die Ersatzschrift. Grund: ich hatte den
#      Kommentar davor als HTML-Kommentar geschrieben, und der steht
#      in einem <style>-Block. Fuer den CSS-Parser ist der Text
#      zwischen den Klammern gewoehnlicher Unsinn; er verschluckt sich
#      und wirft die naechste Regel gleich mit weg.
#
#      In den beiden index.html standen VIER solcher Kommentare, und
#      der erste sass direkt vor Montserrat. Nachgezaehlt, welche
#      erklaerten Familien der Browser wirklich kennt:
#
#          vorher   53 Schriften, es fehlte: Montserrat
#          nachher  57 Schriften, es fehlt: keine
#
#      Montserrat ist die Schrift der Folgeslides im warmen Feed. Sie
#      kam bisher ueber den Google-Link, deshalb ist es nie
#      aufgefallen — die oertliche Datei, wegen der sie ueberhaupt hier
#      liegt, hat nie gegriffen. Jetzt schon.
#
#      Alle vier Kommentare sind jetzt CSS-Kommentare. Nachgemessen
#      auf beiden Seiten: 57 Schriften, keine fehlt, und Montserrat,
#      Shadows Into Light und Nothing You Could Do zeichnen jeweils
#      andere Pixel als die Ersatzschrift.


# 140 — DM Serif 10 Prozent groesser, Handschrift bleibt.
#
#      Die zwei Groessen standen bisher nur im warmen Grundblock:
#
#          deckblattGroesse 68   die erste Folie
#          fotoGroesse      44   die Folgeslides
#
#      Sie im Aufsatz zu setzen statt im Grundblock ist der ganze
#      Punkt — sonst waere der warme Feed mitgewachsen. Jetzt 74,8 und
#      48,4.
#
#      DIE GEGENRECHNUNG. Die Handschrift ist kein eigenes Mass,
#      sondern ein Anteil an der Serife:
#
#          Unterzeile = deckblattGroesse * zweitAnteil * handGroesse
#
#      Ohne Gegenrechnung waere sie um dieselben 10 Prozent
#      mitgewachsen — und ihre Groesse hat Carina zwei Schritte vorher
#      selbst gewaehlt (134). Deshalb handGroesse von 1.2 auf 1.0909,
#      also durch 1,1 geteilt. Nachgerechnet:
#
#                          Serife   Handschrift
#          vorher            68,0        50,6
#          nachher           74,8        50,6
#
#      Auf den Folgeslides waechst der zweite Block mit — dort steht
#      keine Handschrift, sondern folgeFamilie, also die Serife
#      selbst. 27,3 auf 30,0, dieselben 10 Prozent.


# 141 — Playfair Display statt DM Serif, eng gestellt. Carina hat aus
#      den Proben "Playfair 20" gewaehlt, also die erste Enger-Stufe.
#
#      Sechs Felder im Aufsatz tragen die Serife und wechseln alle
#      mit: deckblattFamilie, fotoSchrift, schriftart, folgeFamilie,
#      ablaufTitel, nameSchrift.
#
#      DIE ENGSTELLUNG STEHT WOANDERS, ALS MAN DENKT. laufweite gilt
#      nicht fuer Fotokacheln — die lesen fotoLaufweite:
#
#          zCS = zVS ? versalLaufweite : fotoLaufweite
#
#      Das Feld gab es noch gar nicht, also stand dort 0. Jetzt -20.
#      Nebenwirkung: zCS gilt auch fuer den zweiten Block, die
#      Handschrift wird also mit 2 Prozent enger gesetzt. Bei -20 ist
#      das kaum zu sehen; wer es trennen will, braucht ein eigenes
#      Feld.
#
#      ZWEI FALLEN GEPRUEFT, bevor umgestellt:
#
#      1. tiefeSchriften. Der Verlauf unten haengt an
#         new RegExp(BS_KACHEL.tiefeSchriften).test(Qe). Die Liste
#         enthaelt "Playfair" — der Verlauf bleibt also an. Haette sie
#         nur "DM Serif" enthalten, waere mit der Schrift das ganze
#         Band verschwunden.
#      2. /Playfair/.test(Qe) && (kt="400") setzt das Gewicht hart auf
#         400. Steht aber vor der Zeile, die deckblattGewicht
#         anwendet — das gewinnt weiter.
#
#      Und Playfair war NUR ueber den Google-Link da, wie Montserrat
#      in 139. Fuer eine Schrift, mit der der Zeichner rechnet, ist das
#      zu spaet. Jetzt liegt sie als variable Datei im Projekt (400 bis
#      900, 38 kB, SIL Open Font License).
#
#      Im Browser nachgemessen: vier Playfair-Schnitte angemeldet, 58
#      Schriften gesamt, und Playfair zeichnet andere Pixel als die
#      Ersatzschrift.


# 142 — Playfair groesser. Carina: "Groesser Playfair".
#
#      Vorher nachgemessen, statt der eigenen Vermutung zu glauben:
#      ich hatte in 141 geschrieben, Playfair sei "zarter und wirkt
#      kleiner". Bei 100 px im Browser:
#
#                        Playfair   DM Serif
#          Versalhoehe H      71        67
#          Mittellaenge x     53        49
#          Zeilenbreite     1735      1702
#
#      Playfair ist also GROESSER als DM Serif, nicht kleiner — um
#      sechs Prozent in der Versalhoehe. Was leichter wirkt, sind die
#      duenneren Striche, nicht die Groesse. Haette ich auf gleiche
#      Versalhoehe "korrigiert", waere die Schrift kleiner geworden,
#      also das Gegenteil des Auftrags.
#
#      Deshalb ein echter Schritt statt einer Korrektur: plus 15
#      Prozent.
#
#          deckblattGroesse  74,8 -> 86
#          fotoGroesse       48,4 -> 55,7
#          handGroesse    1,0909 -> 0,9486   (durch 1,15 geteilt)
#
#      Die Handschrift bleibt damit wieder stehen: 50,6 vorher und
#      nachher. Gegenueber dem Anfang der Reihe (DM Serif bei 68) ist
#      die Versalhoehe jetzt 34 Prozent groesser.
#
#      GRENZE, die man kennen sollte: der Zeichner verkleinert in einer
#      Schleife, bis der Block in textHoehe (.74 der Kachelhoehe) und
#      in die Breite passt. Bei langen Texten ist die Groesse also
#      schon vorher gedeckelt und diese Zahl aendert dort nichts — sie
#      wirkt auf kurze Saetze.


# 143 — Folgeslides bleiben bei DM Serif. Carina: "Fuer die folgeslides
#      faende ich jetzt schoener wenn es hier dennoch dm serif ist
#      oder?"
#
#      Ein Feld: folgeFamilie zurueck auf DM Serif Display. Das
#      Deckblatt bleibt Playfair, ebenso schriftart, ablaufTitel,
#      fotoSchrift und nameSchrift — sie hat ausdruecklich nur die
#      Folgeslides gemeint.
#
#      Es trifft dort beides, Kopfzeile und zweiten Block: QeZ liest
#      auf Folgeslides ebenfalls folgeFamilie.
#
#      GEPRUEFT, damit nichts anderes mitkippt: der Verlauf unten
#      haengt an new RegExp(tiefeSchriften).test(Qe), und Qe ist auf
#      Folgeslides jetzt "DM Serif Display". Die Liste enthaelt sowohl
#      "DM Serif" als auch "Playfair" — der Verlauf bleibt auf beiden
#      Folienarten an.
#
#      GROESSE, unangetastet: Playfair traegt bei gleicher Punktgroesse
#      sechs Prozent mehr Versalhoehe (71 gegen 67 bei 100 px, in 142
#      gemessen). Die Folgeslides werden damit optisch etwas kleiner
#      als vorher:
#
#          fotoGroesse 55,7 mit Playfair   Versalhoehe 39,5
#          fotoGroesse 55,7 mit DM Serif   Versalhoehe 37,3
#
#      Wer die alte Hoehe zurueck will, setzt fotoGroesse auf 59,0.
#      Nicht von selbst gemacht: sie hat nach der Schrift gefragt,
#      nicht nach der Groesse.


# 144 — Folgeslides wieder Playfair, und die Handschrift auch dort im
#      zweiten Teil. Carina: "Ok nein zurueck auf Playfair und mehr
#      Einsatz der Handschrift im 2. Teil".
#
#      Erstes: folgeFamilie zurueck auf Playfair Display, 143 also
#      wieder rueckgaengig.
#
#      Zweites: der zweite Block trug auf Folgeslides bisher die
#      Serife, nicht die Handschrift. Das steckt in QeZ:
#
#          QeZ = (zVS && versalFamilie)
#             || (folienRolle && folienRolle!=="deckblatt" && folgeFamilie)
#             || zweiteFamilie
#
#      Der mittlere Zweig faengt Folgeslides ab, bevor zweiteFamilie
#      drankommt. folgeZweitHand:1 laesst ihn ins Leere laufen, dann
#      faellt es auf zweiteFamilie durch — Nothing You Could Do, wie
#      auf dem Deckblatt.
#
#      DAZU GEHOERT die Groesse: handGroesse ist seit 140/142 die
#      Gegenrechnung, die die Handschrift stehen laesst, waehrend die
#      Serife waechst. Sie war auf Folgeslides bewusst ausgeschaltet,
#      weil dort keine Handschrift stand. Jetzt steht dort welche,
#      also gilt sie auch dort — sonst waere sie die einzige Stelle
#      ohne die Gegenrechnung.
#
#      In node durchgerechnet:
#
#          Deckblatt      zweiter Block  Nothing You Could Do   51
#          Folgeslide     zweiter Block  Nothing You Could Do   33
#          Versalkachel   zweiter Block  Shadows Into Light     82
#
#      Die Versalkacheln bleiben also unberuehrt: dort greift der
#      erste Zweig, versalFamilie.

P.append(('QeZ=$e?((zVS&&BS_KACHEL.versalFamilie)||(t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie)||BS_KACHEL.zweiteFamilie||Qe):Qe',
 'QeZ=$e?((zVS&&BS_KACHEL.versalFamilie)||(BS_KACHEL.folgeZweitHand?!1:(t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeFamilie))||BS_KACHEL.zweiteFamilie||Qe):Qe',
 "zweiter Block auf Folgeslides wird Handschrift", 1))

P.append(('*((zVS||!(t.folienRolle&&t.folienRolle!=="deckblatt"))?(Number(BS_KACHEL.handGroesse)||1):1)):qe',
 '*((zVS||BS_KACHEL.folgeZweitHand||!(t.folienRolle&&t.folienRolle!=="deckblatt"))?(Number(BS_KACHEL.handGroesse)||1):1)):qe',
 "handGroesse gilt dort mit", 1))


# 145 — Die Unterteile fuenf Prozent groesser. Carina: "Noch Groesse
#      auch die Unterteile ca 5% mehr".
#
#      Zwei Zahlen kaemen dafuer in Frage, und nur eine ist richtig.
#
#      handGroesse waere falsch: sie skaliert seit 134 auch die
#      Versalkacheln, denn dort steht
#      versalGroesse * handGroesse. Die ganze Kachel waere
#      mitgewachsen, obwohl nur die Unterteile gemeint waren.
#
#      zweitAnteil trifft genau: er gilt fuer den zweiten Block auf
#      Deckblatt und Folgeslide. Auf Versalkacheln gewinnt in
#      derselben Zeile versalZweitAnteil (1), die bleiben also
#      unberuehrt.
#
#          .62 -> .651
#
#      Nachgerechnet:
#
#                            vorher  nachher
#          Deckblatt           50,6     53,1   +4,9 %
#          Folgeslide          32,8     34,4   +4,9 %
#          Versalkachel        94,9     94,9   unveraendert
#
#      Die Kopfzeilen bleiben, wo sie sind: 86 und 55,7.


# 146 — Noch einmal 15 Prozent, Kopf und Unterzeile zusammen. Carina
#      hat die App neben eine Vorlage gehalten: "Nein so gross".
#
#      Beide Bilder ausgemessen, Zeilenabstand als Mass (der ist
#      sauber zu finden, die Glyphenbreite nicht — auf ihrem Foto ist
#      die Wand fast so hell wie die Schrift):
#
#                        Kopf   Unterzeile   Verhaeltnis
#          App          109,5        56,5         0,516
#          Vorlage       48,5        25,0         0,515
#
#      Das VERHAELTNIS stimmt also schon, auf ein Tausendstel. Es geht
#      nur um die Groesse im Ganzen. Und die haengt davon ab, worauf
#      man bezieht:
#
#                        auf die Hoehe   auf die Breite
#          App                  7,90 %          9,86 %
#          Vorlage              9,08 %         12,31 %
#          Faktor                1,149           1,252
#
#      Die Vorlage hat 394 zu 534, also 0,738 — weder 4:5 noch 3:4.
#      Ein Ausschnitt. Deshalb sind beide Bezuege angreifbar, und ich
#      habe den KLEINEREN genommen: 15 Prozent statt 25.
#
#      Nicht mit dem Zeilenumbruch zu erklaeren: beide brechen den
#      Satz gleich (3 Zeilen Kopf, 5 Zeilen Unterzeile). Das spricht
#      dafuer, dass sich das Verhaeltnis Schrift zu Textspalte kaum
#      unterscheidet — noch ein Grund, vorsichtig zu sein.
#
#          deckblattGroesse  86  -> 98,9
#          fotoGroesse     55,7  -> 64,1
#
#      zweitAnteil und handGroesse bleiben, damit die Unterzeile
#      diesmal MITWAECHST: 53,1 auf 61,1. Sie hat beides gemeint.
#
#      VORBEHALT: der Zeichner verkleinert, bis der Block in textHoehe
#      und in die Textspalte passt. Wo dieser Deckel schon greift,
#      aendert die Zahl nichts — dann waere textHoehe oder der
#      Seitenrand der Hebel, nicht die Schriftgroesse.

# 147  Der Rahmen war der Deckel, nicht die Schriftgroesse
#
#      "Es ist zu klein - der erlaubte Frame wirkt zu klein." Sie hat
#      damit den Vorbehalt aus 146 bestaetigt. Nachgemessen, welche der
#      beiden Bremsen wirklich greift:
#
#      1. Die Textspalte. zbr war fuer mittigen Satz fest .86, davon
#         geht umbruchRand 12 ab: rund 83,6 Prozent der Kachelbreite.
#      2. Die Hoehe. textHoehe .70 mal Zeilenzahl.
#      3. Ein zweiter Deckel danach: zF verkleinert den fertigen Block
#         auf r*(1-2*fotoRand), fotoRand .09 — also 82 Prozent.
#
#      Es ist die BREITE. Der zweite Deckel lag mit 82 Prozent sogar
#      noch unter der Spalte, hat den Block also nochmal geschrumpft.
#      Die laengste Zeile der Vorlage misst 86,3 Prozent der
#      Kachelbreite — mehr, als der Rahmen ueberhaupt zuliess. Die
#      Schrift KONNTE nicht so gross werden, egal welche Zahl in
#      deckblattGroesse steht.
#
#      Damit die Spalte einstellbar wird, liest zbr jetzt spalteBreit
#      statt der festen .86. Der warme Feed hat den Wert nicht und
#      faellt auf .86 zurueck — dort aendert sich nichts.
#
#          spalteBreit  (neu)  .93   Umbruchspalte 83,6 -> 90,6 %
#          fotoRand     .09 -> .035  zweiter Deckel  82  -> 93 %
#          textHoehe    .70 -> .80   damit die Hoehe nicht neu bremst
#
#      Wirksam also 82 -> 90,6 Prozent, gut 10 Prozent mehr Platz bei
#      gleichem Umbruch — zusaetzlich zu den 15 Prozent aus 146.

# 149  Textkacheln zurueck im dunklen Zwilling
#
#      "Baue dort wieder Textkacheln, bitte Farben olivgrau und weisse
#      Schrift duenne Playfair sehr eng in Abstand und Zeile also wie
#      die Quotes."
#
#      Erst nachgesehen, WER die Textkachel ueberhaupt zeichnet. Eine
#      Sonde im Zeichner: die Kachel kommt als karte:"hell" herein und
#      wird von der Fassung "marke" gemalt — nicht von dem Zweig, an
#      dem wir den ganzen Abend gearbeitet haben. Das ist wichtig,
#      weil dieser Zeichner schon vollstaendig aus dem Block liest:
#
#          grundA/schriftA   Grund und Schrift der Textkachel
#          schriftart        Familie des ersten Blocks
#          unterSchrift      Familie des zweiten Blocks
#          gewicht           Schnitt oben, unterGewicht unten
#          laufweite         Laufweite (charSpacing)
#          zeile / absatz    Zeilenabstand und Absatzluft
#          name              Wortmarke unten, leer heisst keine
#
#      Es brauchte also fast keinen Code, nur Werte. gewicht,
#      laufweite, zeile, absatz, groesseAnteil, maxhoehe, rand und
#      mitte werden ausschliesslich hier gelesen (K = BS_KACHEL, das
#      Kuerzel steht genau einmal im Bundle) — Fotokacheln lesen
#      deckblattGroesse, fotoLaufweite, fotoZeile. Die Fotokacheln
#      bleiben also unberuehrt.
#
#      DUENN: Playfair Display faengt bei 400 an, duenner geht nicht.
#      Die Familie "Playfair" (die neuere, ohne Display) hat 300.
#      Deshalb liegt sie jetzt selbst gehostet in site/fonts/ und ihr
#      @font-face steht nur in site/dunkel/index.html. Gemessen, 80px,
#      gleicher Satz, Tinte als Summe der Helligkeit:
#
#          Playfair Display 400   Tinte 9235   Breite 632
#          Playfair 400           Tinte 6351   Breite 572
#          Playfair 300           Tinte 5965   Breite 572
#          Playfair 300, -35      Tinte 5964   Breite 524
#
#      Also 35 Prozent weniger Tinte und 17 Prozent schmaler als
#      vorher. Das ist ein echtes Duenn, kein gefuehltes.
#
#      Zwei Code-Aenderungen bleiben:
#        - der Schnitt 300 muss mit vorgeladen werden, sonst misst der
#          Zeichner den falschen (er misst auf dem Canvas),
#        - "neu generieren" entschied ueber Foto oder Text mit einer
#          eigenen Regel; jetzt folgt es textAnteil wie der Import.
#          Sonst gaebe es keinen Knopf, mit dem bestehende Tage die
#          Textkacheln zurueckbekommen: bei textAnteil 0 hat der
#          Zeichner jeder bildlosen Kachel ein Foto aufgezwungen und
#          das Laden hat es sogar in den Plan geschrieben.
P.append(('["200","400","500","700"]','["200","300","400","500","700"]',
 "Schnitt 300 wird mit vorgeladen", 1))
P.append(('qt=(It||!Oe(st,ut))&&ae.length>0;',
 'qt=(It||(BS_KACHEL.textAnteil!=null?((ut*37+13)%100)>=BS_KACHEL.textAnteil:!Oe(st,ut)))&&ae.length>0;',
 "Neu generieren folgt textAnteil wie der Import", 1))

# 150  "Mehr wie die Quotes"
#
#      Beide nebeneinander gerendert und die Zeilenabstaende im Bild
#      ausgemessen, statt zu raten. Der Unterschied war nicht die
#      Groesse, sondern der UMBRUCH: der Zeichner zerlegt einen
#      einzelnen Absatz automatisch in Kopf und Unterzeile (teile()).
#      Deshalb brach unsere Kachel am Satzende um, das Zitat nicht —
#      und weil beide Haelften getrennt umbrechen, blieben Zeilen kurz
#      und die Schrift klein.
#
#      kachelEinBlock schaltet diese Zerlegung ab. Steht die Zahl
#      nicht im Block, bleibt alles wie bisher — der warme Feed sieht
#      nichts davon. Zwei echte Absaetze im Text werden weiterhin als
#      zwei Bloecke gesetzt, nur das automatische Zerlegen entfaellt.
#
#      Dazu der Satzspiegel des Zitats:
#
#          rand           .0885 -> .11    Spalte 82 -> 78 Prozent
#          mitte          .575  -> .50    sitzt wie das Zitat
#          maxhoehe       .90   -> .46    Zitat deckelt bei .44
#          groesseAnteil  .098  -> .115   Startgroesse
#          absatz         .45   -> .30
#
#      Nachgemessen im gerenderten Bild, Zeilenabstand in Pixeln:
#
#          Zitat        5 Zeilen, Abstand 43
#          Textkachel   5 Zeilen, Abstand 44
#
#      Und der Umbruch ist Wort fuer Wort derselbe. Uebrig bleiben
#      genau die Unterschiede, die sie wollte: olivgrau statt creme,
#      weiss statt blaugrau, Playfair 300 statt Display 400.
P.append(('const BL=B0.length>1?B0:(()=>{const t2=teile(B0[0]||"");return t2[1]?[t2[0],t2[1]]:[B0[0]||""]})();',
 'const zSatz=zx=>{const zr=[];let za="";String(zx||"").split(/\\s+/).filter(Boolean).forEach(zw=>{za=za?za+" "+zw:zw;if(/[.!?\\u2026]["\\u00bb\\u201d)\\u2019]?$/.test(zw)){zr.push(za);za=""}});if(za)zr.push(za);return zr.length?zr:[String(zx||"")]};const BL=BS_KACHEL.kachelSatzUmbruch?B0.reduce((za,zb)=>za.concat(zSatz(zb)),[]):(B0.length>1?B0:(BS_KACHEL.kachelEinBlock?[B0[0]||""]:'
 '(()=>{const t2=teile(B0[0]||"");return t2[1]?[t2[0],t2[1]]:[B0[0]||""]})()));',
 "Textkachel: Umbruch am Satzende statt Kopf und Unterzeile", 1))

# 151  Textkachel: Anthrazit mit Hautfarbe
#
#      Nur zwei Werte, kein Code.
#
#          grundA/grundB      #4F5347 -> #2B2C2E   Anthrazit
#          schriftA/schriftB  #FFFFFF -> #E7C9B4   Hautton
#
#      Kontrast gerechnet, nicht geschaetzt: 8,93 zu 1. Auch fuer eine
#      duenne 300er Playfair reichlich (AAA braucht 7 zu 1).

# 152  Der Hautton wird orangener
#
#          schriftA/schriftB  #E7C9B4 -> #E8B48C
#
#      Gerechnet statt geschaetzt. Der Farbton bleibt gleich (HSV 25
#      auf 26 Grad), die Saettigung geht von 22 auf 40 Prozent — also
#      wirklich orangener, nicht nur dunkler. Kontrast auf dem
#      Anthrazit 8,93 -> 7,55 zu 1, damit immer noch ueber AAA (7).
#
#      Weiter Richtung ihrer Terrakotta (#E8836B, Saettigung 54) waere
#      moeglich, dort faellt der Kontrast aber auf 5,25 — fuer eine
#      duenne 300er Playfair zu wenig.

# 153  Umbruch am Satzende
#
#      "Breche bei Texten beim Punkt bitte um." kachelSatzUmbruch
#      zerlegt den Text in Saetze und setzt jeden Satz als eigenen
#      Block — der Zeichner bricht zwischen Bloecken ohnehin um.
#
#      Erkannt wird ein Satzende an einem Wort, das auf . ! ? oder …
#      endet, auch mit Anfuehrung oder Klammer dahinter. Bewusst OHNE
#      Lookbehind im regulaeren Ausdruck: das laeuft auch dort, wo die
#      neuere Syntax fehlt.
#
#      Damit die Saetze nicht wie Kopf und Unterzeile aussehen:
#
#          unterVerhaeltnis  .62 -> 1     alle Saetze gleich gross
#          absatz            .30 -> 0     ein Umbruch, keine Luft
#
#      Zwei echte Leerzeilen im Text bleiben zwei Bloecke, und jeder
#      davon wird zusaetzlich an seinen Satzenden gebrochen.

# 155  Alle 4 Posts eine Textkachel
#
#      textAnteil war ein ANTEIL: 28 Prozent, per Hash verteilt. Das
#      ergibt mal drei Fotos hintereinander, mal zwei Textkacheln
#      nebeneinander. Sie wollte einen Takt, keinen Wuerfel — wie
#      damals beim strengen Wechsel schwarzweiss/farbig.
#
#      textJede zaehlt stattdessen: Rest 0 bei Teilung durch 4 heisst
#      Textkachel, alles andere Foto. An zwei Stellen, damit Import und
#      "neu generieren" denselben Takt schlagen. Steht textJede nicht
#      im Block, gilt weiter textAnteil — der warme Grundblock merkt
#      also nichts.
#
#      Nachgemessen im Browser, Import von zwoelf Tagen, protokolliert
#      wurde die Entscheidung je Tag (Index, Foto?, Bilder im Pool):
#
#          [0,false,4] [1,true,4] [2,true,4]  [3,true,4]
#          [4,false,4] [5,true,4] [6,true,4]  [7,true,4]
#          [8,false,4] [9,true,4] [10,true,4] [11,true,4]
#
#      Also genau 0, 4, 8 — jeder vierte Post, drei von zwoelf.
#
#      MERKE fuer den naechsten Test: die App schreibt ihren eigenen
#      Stand in die Datenbank zurueck, sobald sie geladen hat. Wer
#      Bilder VOR dem Laden hineinsaet, dessen Saat wird ueberschrieben
#      — die Bibliothek war dann leer und JEDER Tag wurde zur
#      Textkachel, in jeder Fassung. Erst saeen, wenn die App steht.

P.append(('(BS_KACHEL.textAnteil!=null?((pt*37+13)%100)>=BS_KACHEL.textAnteil:(qt?!Oe(ct,pt):tS(pt)))',
 '(BS_KACHEL.textJede?(pt%BS_KACHEL.textJede)!==0:BS_KACHEL.textAnteil!=null?'
 '((pt*37+13)%100)>=BS_KACHEL.textAnteil:(qt?!Oe(ct,pt):tS(pt)))',
 "Import: jeder vierte Post wird Textkachel", 1))
P.append(('qt=(It||(BS_KACHEL.textAnteil!=null?((ut*37+13)%100)>=BS_KACHEL.textAnteil:!Oe(st,ut)))&&ae.length>0;',
 'qt=(It||(BS_KACHEL.textJede?(ut%BS_KACHEL.textJede)!==0:BS_KACHEL.textAnteil!=null?'
 '((ut*37+13)%100)>=BS_KACHEL.textAnteil:!Oe(st,ut)))&&ae.length>0;',
 "Neu generieren schlaegt denselben Takt", 1))

# 156  Der Takt muss beim ZEICHNEN entschieden werden
#
#      Sie hat einen Bildschirmabzug ihres echten Feeds geschickt:
#      Textkacheln auf Tag 1, 2, 5, 7, 9, 10 — sechs von zehn, kein
#      Takt. "Ne."
#
#      Grund: 155 aendert nur, was beim IMPORT und beim "neu
#      generieren" entschieden wird. Ihr Plan liegt aber laengst
#      gespeichert da, und dort steht bei jeder Folie fest, ob ein Bild
#      dranhaengt. Der Zeichner nimmt einfach das, was gespeichert ist.
#      Alte Folien ohne Bild wurden also Textkacheln, egal in welchem
#      Takt.
#
#      Jetzt entscheidet der Zeichner selbst: Rest 0 bei Teilung der
#      Tagesnummer minus eins durch textJede heisst Textkachel — dann
#      wird ein gespeichertes Bild fuer die Anzeige weggelassen. Sonst
#      Fotokachel — fehlt das Bild, holt er eins aus der Bibliothek.
#      Nichts davon wird in den Plan zurueckgeschrieben.
#
#      NACHGESTELLT UND ZUERST FALSCH: der erste Versuch hatte die
#      Bedingung "!t.karte" — also nur Kacheln ohne Kartenart. Der
#      Plan-Normierer vergibt aber JEDER Kachel eine, "hell" oder
#      "stein" im Wechsel. Damit lief die Regel nie, und das Gitter sah
#      genauso aus wie auf ihrem Abzug. Erst mit der Bedingung auf
#      leer, "hell" oder "stein" — und ohne reminderArt, damit Quotes,
#      Ablauf und Reminder ihre eigene Fassung behalten — stimmte es.
#
#      Gitter mit zehn Tagen, Bilder absichtlich krumm verteilt
#      (nur 3, 4, 6, 8 hatten eines gespeichert):
#
#          vorher   Text auf 1, 2, 5, 7, 9, 10
#          nachher  Text auf 1, 5, 9
#
#      Tag 2, 7 und 10 haben ihr Bild aus der Bibliothek bekommen.

# 157  Farbwelt "Tinte / Sand" fuer die Textkachel
#
#          grundA/grundB      #2B2C2E -> #1B1E23
#          schriftA/schriftB  #E8B48C -> #DCC9B0
#
#      Kontrast 7,55 -> 10,37 zu 1. Der Grund hat denselben kuehlen
#      Kern wie die Schwarzweissfotos, der Sandton bleibt warm genug,
#      damit es nicht klinisch wird.
#
#      Aus sechs gerechneten Farbwelten ausgewaehlt. Die zweite
#      Empfehlung — "Papier / Tinte" fuer die 30-Schritt-Serie — ist
#      hinfaellig: die Serie ist aus ihrem Plan raus. Sie stand nur
#      noch in site/captions.json, und das ist ein Archiv vom
#      3. September, kein Abbild des laufenden Plans. MERKE: fuer
#      Aussagen ueber ihren Content zaehlt der Plan im Browser, nicht
#      die Datei im Projekt.

# 158  Die Textkachel wird ein weichgezeichnetes Foto
#
#      "Mach die Textkacheln komplett blurred Foto mit weisser
#      Schrift." Damit dreht sich die Regel aus 156 um: der vierte Tag
#      bekommt jetzt ein Bild, statt seines beraubt zu werden.
#
#          vorher   Takttag -> background auf null, flacher Farbgrund
#          nachher  Takttag -> Bild behalten oder eins holen,
#                              dazu blur = textBlur (20)
#
#      Der Zeichner rechnet blur/40, gedeckelt bei 0,5 — 20 ist also
#      das Maximum, das der Filter hergibt. Und weil die Kachel nun ein
#      Bild hat, laeuft sie durch den Fotozweig: Schrift wird
#      fotoSchriftFarbe, und die steht im dunklen Block auf #FFFFFF.
#      Die weisse Schrift kommt also von selbst, ohne zweite Regel.
#
#      GEPRUEFT MIT EINEM SCHARFEN TESTBILD: ein glatter Verlauf haette
#      nichts gezeigt, weichgezeichnet sieht er aus wie vorher. Erst
#      mit einem Raster aus harten Linien war zu sehen, dass die
#      Unschaerfe wirklich greift — Tag 1, 5 und 9 loesen sich auf, die
#      anderen sieben bleiben scharf.
#
#      Die Farbwelt Tinte/Sand aus 157 wird damit nur noch dort
#      sichtbar, wo gar kein Bild da ist. Die Werte bleiben stehen.

# 159  Caption im Bulk-Import: alles, nicht nur die erste Zeile
#
#      "Wenn ich dir im bulk import was gebe und da steht caption:
#      schreib das in die caption nicht auf den slide."
#
#      Der Leser kannte "caption:" bereits — aber nur EINE Zeile
#      davon. Jede weitere Zeile fiel in den Folienpuffer, und ihre
#      Captions haben Absaetze. Ergebnis: der halbe Bildtext stand auf
#      der Folie.
#
#      Jetzt schaltet "caption:" einen Sammelmodus ein. Alle folgenden
#      Zeilen gehen in die Caption, bis wieder "Tag N" oder "Slide N"
#      kommt. Leerzeilen bleiben dabei erhalten — sie werden sonst
#      ganz oben verworfen, und damit waeren die Absaetze weg.
#
#      Nebenbei mitgenommen: "Caption :" mit Leerzeichen wird jetzt
#      auch erkannt (vorher haette substring(8) den Text angeschnitten),
#      und die fertige Caption wird am Ende getrimmt.
#
#      GEPRUEFT ohne Browser: die Leserfunktion aus beiden Bundles
#      herausgeloest und denselben Text hindurchgeschickt.
#
#          karten217  Slide 2 = "…meine Nummer.\nIch hab das monatel…"
#                     Caption = nur der erste Absatz
#          karten218  Slide 2 = "…meine Nummer."
#                     Caption = alle drei Absaetze, mit Leerzeilen
P.append(('let n=null,i=[],s=[];const l=()=>{',
 'let n=null,i=[],s=[],zKap=!1;const l=()=>{',
 "Bulk-Import: Sammelmodus fuer die Caption", 1))
P.append(('return r.forEach(o=>{const a=o.trim();if(!a)return;const u=a.match(/^(?:Tag|Day|Woche)',
 'return r.forEach(o=>{const a=o.trim();'
 'if(zKap){if(!/^(?:Tag|Day|Woche|Slide|Folie|Bild|Page)\\s*\\d+\\s*[:.\\-\\u2013\\u2014]/i.test(a)){'
 'if(n)n.caption=n.caption?n.caption+`\\n`+a:a;return}zKap=!1}'
 'if(!a)return;const u=a.match(/^(?:Tag|Day|Woche)',
 "Bulk-Import: alle Zeilen nach caption: gehoeren zur Caption", 1))
P.append(('if(a.toLowerCase().startsWith("caption:")){n&&(n.caption=a.substring(8).trim());return}',
 'if(/^caption\\s*:/i.test(a)){if(n){n.caption=a.replace(/^caption\\s*:/i,"").trim();zKap=!0}return}',
 "Bulk-Import: caption: schaltet den Sammelmodus ein", 1))
P.append(('l(),n&&(n.slides=i.length>0?i:["Inhalt..."],t.push(n)),t}',
 'l(),n&&(n.slides=i.length>0?i:["Inhalt..."],t.push(n)),'
 't.map(zx=>(zx.caption=String(zx.caption||"").trim(),zx))}',
 "Bulk-Import: Leerzeilen am Ende der Caption abschneiden", 1))

# 160  "Du schreibst den Teil immer noch auf die slide"
#
#      Sie hatte recht, 159 war zu kurz gesprungen. Ich habe den Leser
#      diesmal nicht mit EINEM Beispiel geprueft, sondern mit zehn
#      Eingabeformen. Zwei sind durchgefallen — und beide betreffen
#      genau ihre Texte:
#
#          Caption enthaelt "Woche 1 war anstrengend."  -> LECK
#          Caption enthaelt "Bild 2 zeigt es."          -> LECK
#
#      Der Sammelmodus endete an JEDER Zeile, die mit Tag, Day, Woche,
#      Slide, Folie, Bild oder Page plus Ziffer beginnt. In Prosa
#      passiert das staendig. Der Rest der Caption landete dann auf
#      einer Folie — genau ihr Befund.
#
#      Der Unterschied zwischen Ueberschrift und Prosa ist das
#      Trennzeichen: eine echte Ueberschrift heisst "Tag 41: Titel",
#      Prosa heisst "Woche 1 war anstrengend". Der Sammelmodus endet
#      jetzt nur noch, wenn nach der Ziffer ein : . - oder Gedanken-
#      strich folgt. Fuer den normalen Zeilenleser bleibt die alte,
#      grosszuegige Regel — dort ist sie richtig.
#
#      NACHGEPRUEFT mit vier ECHTEN Captions aus captions.json (1815
#      Zeichen): alle vier vollstaendig in der Caption, alle Folien
#      sauber. Und alle zehn Eingabeformen gruen.
#
#      LEHRE: ein einziger Testfall beweist nur, dass der eine Fall
#      geht. Bei einem Parser gehoert eine Tabelle von Formen dazu.

# 161  Weichzeichner raus, Takt auf 7
#
#      "Vergiss das blurred, mach einfach nur Foto Kacheln mal und
#      vielleicht alle 7 eine Textkachel und die muessen wir noch
#      ausbaldovern."
#
#      Damit faellt 158 wieder weg: die Taktkachel bekommt kein Bild
#      mehr aufgedraengt, sondern gibt ihres ab und ist wieder eine
#      echte Textkachel. Und der Takt geht von 4 auf 7.
#
#          textJede  4 -> 7
#          textBlur  entfaellt
#
#      Gerendert mit 14 Tagen, alle mit gespeichertem Foto:
#      Textkacheln auf Tag 1 und Tag 8, die uebrigen zwoelf Fotos,
#      alle scharf.
#
#      OFFEN, ausdruecklich von ihr: wie die Textkachel selbst
#      aussieht. Sie steht jetzt in Tinte/Sand da, das ist der Stand
#      aus 157 und keine Entscheidung.

# 162  Andere Farben, andere Serife fuer die Textkachel
#
#      Erst die sieben selbst gehosteten Serifen gegeneinander
#      gemessen: 100 px, derselbe Satz "Hxn Zahlen", Versalhoehe und
#      Tinte auf dem Canvas gezaehlt.
#
#          Playfair 300           Versalhoehe 63  Breite 464  Tinte  5957
#          Cormorant Garamond 300 Versalhoehe 73  Breite 465  Tinte  4808
#          Bodoni Moda 400        Versalhoehe 75  Breite 534  Tinte  8750
#          Marcellus 400          Versalhoehe 73  Breite 520  Tinte  9243
#          Prata 400              Versalhoehe 81  Breite 571  Tinte 11291
#          Italiana 400           Versalhoehe 75  Breite 471  Tinte  6128
#          DM Serif Display 400   Versalhoehe 71  Breite 509  Tinte 12545
#
#      Cormorant Garamond 300 ist die einzige, die BREITENGLEICH zu
#      Playfair ist (465 zu 464). Damit bleibt der Umbruch Wort fuer
#      Wort derselbe, und groesseAnteil muss nicht nachgezogen werden.
#      Dabei ist sie 16 Prozent hoeher in den Versalien und traegt 19
#      Prozent weniger Tinte — also feiner UND optisch groesser.
#
#          schriftart/unterSchrift  Playfair -> Cormorant Garamond
#          grundA/grundB    #1B1E23 -> #241C16   Espresso
#          schriftA/schriftB #DCC9B0 -> #E9A473  Apricot
#
#      Kontrast 8,00 zu 1. #241C16 ist die Farbe ihres urspruenglichen
#      warmen Feeds — die einzige Farbwelt mit eigener Geschichte.

# 163  Die Textkachel wird umgedreht
#
#      Fuenfmal hintereinander "andere Farben", und fuenfmal war meine
#      Antwort derselbe Bauplan: dunkler Grund, warme Schrift.
#
#          #171512 / #F2EFE9    #4F5347 / #FFFFFF
#          #2B2C2E / #E7C9B4    #2B2C2E / #E8B48C
#          #1B1E23 / #DCC9B0    #241C16 / #E9A473
#
#      Statt den siebten Braunton zu suchen, kippt jetzt das Prinzip:
#      heller Grund, dunkle Schrift.
#
#          grundA/grundB      #241C16 -> #EDE7DE   Papier
#          schriftA/schriftB  #E9A473 -> #241C16   Espresso als TINTE
#
#      Kontrast 13,64 zu 1. Die Palette bleibt ihre, nur die Rollen
#      tauschen. Und im Raster ist das der eigentliche Gewinn: alle
#      Fotokacheln sind dunkel, jede siebte Kachel ist jetzt hell —
#      damit wird sie zur Pause statt zum naechsten Bild.

# 164  Schwarz auf Weiss, hart
#
#      Nach sechs Paletten und einer Umkehrung habe ich aufgehoert zu
#      raten und gefragt — mit vier Richtungen, die sich in der ART
#      unterscheiden, nicht im Farbton. Ihre Wahl: hart.
#
#          grundA/grundB      #EDE7DE -> #FFFFFF
#          schriftA/schriftB  #241C16 -> #000000
#
#      Kontrast 21,00 zu 1, das Maximum. Kein Beige, keine Waerme.
#
#      MERKE: sechs Vorschlaege in Folge, die alle im selben Schema
#      lagen, waren sechs verlorene Runden. Eine Frage mit Optionen,
#      die sich grundsaetzlich unterscheiden, hat es in einer geklaert.

# 165  Italiana statt Cormorant, und auf den Folien dieselbe
#
#      "Schoen die Schrift aber das hat schon wer exakt so und deshalb
#      bitte eine andere und auf den slides die gleiche."
#
#      Cormorant Garamond ist tatsaechlich ueberall — sie hat recht.
#      Aus der Messtabelle von 162 die naechstliegende gesucht: es
#      zaehlt die BREITE, denn die entscheidet ueber den Umbruch.
#
#          Cormorant Garamond 300  Breite 465  Versalhoehe 73
#          Italiana 400            Breite 471  Versalhoehe 75   +1,3 %
#          Marcellus 400           Breite 520                  +11,8 %
#          Bodoni Moda 400         Breite 534                  +14,8 %
#          Prata 400               Breite 571                  +22,8 %
#
#      Italiana liegt 1,3 Prozent daneben, alle anderen zweistellig.
#      Also Italiana — fein, hoher Kontrast, deutlich seltener.
#
#      Und diesmal ueberall dieselbe: schriftart, unterSchrift,
#      deckblattFamilie, fotoSchrift, folgeFamilie, ablaufTitel.
#      Vorher stand auf den Folien noch Playfair Display.
#
#      VORHER GEPRUEFT, weil es hier schon einmal fast schiefging:
#      tiefeSchriften enthaelt "Italiana". Stuende sie nicht drin,
#      waere mit dem Schriftwechsel das dunkle Band unter dem Text
#      lautlos verschwunden.
#
#      Italiana hat nur den Schnitt 400, deshalb gewicht und
#      unterGewicht von 300 auf 400. Fett ausgezeichnete Woerter
#      (**Wort**) haben damit keinen echten fetten Schnitt mehr.

# 166  Italiana war unlesbar — Marcellus
#
#      "Das kann niemand lesen die Schrift." Stimmt. Ich hatte Italiana
#      allein nach der BREITE ausgesucht, damit der Umbruch gleich
#      bleibt, und die Lesbarkeit gar nicht geprueft. Italiana ist eine
#      Zierschrift, keine Textschrift.
#
#      Also nachgemessen, was ich beim ersten Mal haette messen sollen:
#      "Handeln" bei 100 px, Tintendeckung pro Flaeche als Mass fuer
#      Substanz.
#
#          DM Serif Display    0,381
#          Marcellus           0,258
#          Prata               0,249
#          Playfair Display    0,244
#          Bodoni Moda         0,232
#          Italiana            0,191
#          Cormorant Garamond  0,167
#
#      Italiana liegt fast am Ende — und schlimmer als der Wert sind
#      ihre Formen: sehr offen, ungleichmaessiger Strichkontrast, auf
#      eine Zeile im Feed nicht ausgelegt.
#
#      Marcellus: 35 Prozent mehr Deckung als Italiana, konventionelle
#      roemische Formen, und immer noch selten. Sie laeuft 11 Prozent
#      breiter, der Zeichner faengt das ueber die Anpassungsschleife ab.
#
#      LEHRE: Breite entscheidet ueber den Umbruch, Deckung und Form
#      entscheiden ueber die Lesbarkeit. Ich hatte nur das Erste
#      gemessen.

# 167  Playfair bleibt auf den Fotos
#
#      "Auf den Fotos sollte Playfair bleiben wie gehabt !!!!"
#
#      Ich hatte in 165 "auf den slides die gleiche" so gelesen, dass
#      ueberall dieselbe Schrift stehen soll. Gemeint war das Gegenteil
#      der Wirkung: die Fotokacheln behalten Playfair Display, die neue
#      Schrift gilt nur der Textkachel.
#
#          deckblattFamilie  Marcellus -> Playfair Display
#          fotoSchrift       Marcellus -> Playfair Display
#          folgeFamilie      Marcellus -> Playfair Display
#          ablaufTitel       Marcellus -> Playfair Display
#          schriftart        Marcellus  (Textkachel, bleibt)
#          unterSchrift      Marcellus  (Textkachel, bleibt)
#
#      Damit stehen im dunklen Feed zwei Serifen nebeneinander:
#      Playfair Display auf allen Fotos, Marcellus auf jeder siebten
#      Kachel. Das ist gewollt — die Textkachel soll sich absetzen.

# 168  Ein geoeffneter Post darf sich nicht veraendern
#
#      "Wenn ich einen Post oeffne soll der so bleiben wie er aussah
#      nicht ploetzlich Textkachel werden."
#
#      Ursache: seit 156 hat der ZEICHNER ueber den Takt entschieden,
#      bei jedem Zeichnen neu. Eine gespeicherte Fotokachel, deren
#      Tagesnummer auf den Takt fiel, wurde beim Zeichnen ihres Bildes
#      beraubt — im Gitter wie im Editor. Wer sie oeffnete, sah etwas
#      anderes als das, was im Plan steht.
#
#      Damals war das die richtige Antwort auf eine andere Frage: der
#      Takt sollte ohne "neu generieren" sofort im Gitter sichtbar
#      sein. Der Preis war, dass die Anzeige nicht mehr dem Plan
#      entspricht — und der Preis ist zu hoch.
#
#      Der Zeichner entscheidet jetzt gar nichts mehr ueber den Takt.
#      Er zeichnet, was im Plan steht. Der Takt wird beim IMPORT und
#      beim NEU GENERIEREN in den Plan geschrieben (die beiden Stellen
#      aus 155) und bleibt dort stehen, auch wenn sie eine Kachel von
#      Hand aendert.
#
#      Geprueft: Plan mit 14 Tagen, alle mit gespeichertem Foto. Tag 1
#      faellt auf den Takt. Vorher wurde er beim Oeffnen zur
#      Textkachel, jetzt zeigen Gitter und Editor dasselbe Foto.
#
#      FOLGE FUER SIE: der Takt greift erst nach einem Klick auf "neu
#      generieren". Was jetzt im Plan steht, bleibt so, wie es ist.

# 169  Feed blaetterbar — wieder ausgebaut in 170
#
#      Stand nur in karten228. Was es war und warum es wieder weg
#      ist, steht in 170.

# 170  Blaettern wieder raus
#
#      "Bau das Blaettern wieder aus."
#
#      Die vier Ersetzungen aus 169 sind ersatzlos gestrichen, ebenso
#      seiteGross in der Konfiguration. karten229 ist Zeichen fuer
#      Zeichen karten227, nur das Versionsschild ist anders — das ist
#      geprueft, nicht behauptet.
#
#      DAMIT IST DIE WEISSE SEITE ZURUECK. Die faule Gitterkachel uG
#      setzt ihren Beobachter einmal und trennt ihn dann; was einmal
#      gesehen wurde, bleibt gezeichnet. Bei 197 Tagen heisst das 197
#      gezeichnete Kacheln gleichzeitig, und irgendwann gibt der
#      Browser auf. Das ist die Ursache, nicht das Blaettern — das
#      Blaettern war nur eine von zwei moeglichen Antworten darauf.
#
#      Die andere waere, den Beobachter wieder anzuhaengen, damit
#      Kacheln beim Herausscrollen frei werden. Der Feed bleibt dann
#      eine einzige lange Bahn. Preis: beim Zurueckscrollen wird neu
#      gezeichnet, das kann kurz flackern.

# 171 — Screenshot-Zuordnung: zeigen, warum etwas nicht trifft
# a) Pruefliste: fuer JEDEN Platzhalter der beste Wert, auch unter der Schwelle
P.append((
 'rG=.45,ZC=(e,t)=>{',
 'rG=.45,zPruefung=(e,t)=>e.map(n=>{let zb=null;t.forEach(zs=>{const zl=eG(n.matchText,zs.ocrText);(!zb||zl>zb.score)&&(zb={score:zl,ocr:zs.ocrText||""})});const zw=zb?zb.score:0,zt=String(n.id||"").split("_");return{id:n.id,wert:zw,treffer:zw>=rG,wo:zt.length>1?"Tag "+zt[0]+" \\u00b7 Slide "+(Number(zt[1])+1):String(n.id||""),suchtext:n.matchText||"",naechster:zb&&zb.ocr?zb.ocr.replace(/\\s+/g," ").trim().slice(0,80):""}}).sort((zx,zy)=>zx.wert-zy.wert),ZC=(e,t)=>{',
 "Pruefliste zPruefung", 1))

# b) Die Liste in den Dialog, unter den gruenen Kasten
P.append((
 'zugeordnet."]})]})}),r.length>0&&v.jsxs("div",{className:"sticky bottom-0',
 'zugeordnet."]}),i.length>0&&v.jsxs("details",{className:"bg-gray-50 border border-gray-200 rounded-xl p-3",children:[v.jsxs("summary",{className:"cursor-pointer text-xs font-bold text-gray-700",children:["Warum trifft etwas nicht? (",r.length," Platzhalter, Schwelle ",rG,")"]}),v.jsx("div",{className:"mt-3 space-y-2",children:zPruefung(r,i).map(zx=>v.jsxs("div",{className:"flex gap-2 items-start text-xs",children:[v.jsx("span",{className:"font-mono shrink-0 w-9 text-right font-bold "+(zx.treffer?"text-green-700":"text-red-600"),children:zx.wert.toFixed(2)}),v.jsxs("span",{className:"flex-1 min-w-0",children:[v.jsxs("span",{className:"block text-gray-800",children:[v.jsx("span",{className:"text-gray-400",children:zx.wo}),"  ",zx.suchtext||"(leer)"]}),v.jsx("span",{className:"block text-gray-500 truncate",children:zx.naechster?"n\\u00e4chster: "+zx.naechster:"kein Screenshot in der Bibliothek"})]})]},zx.id))})]})]})}),r.length>0&&v.jsxs("div",{className:"sticky bottom-0',
 "Pruefliste im Dialog", 1))

# 171  Warum trifft ein Screenshot nicht?
#
#      Sie hat 131 Screenshots in der Bibliothek und 61 Platzhalter im
#      Plan, und die Zuordnung greift nicht bei allen. Bisher stand im
#      Dialog nur "X von N zugeordnet" — welche und warum nicht, blieb
#      im Dunkeln, und die Schwelle von 0,45 ist von aussen unsichtbar.
#
#      Der Dialog zeigt jetzt eine aufklappbare Liste, schlechtester
#      Wert zuerst: Wert, Tag und Slide, der Suchtext, und der Anfang
#      des OCR-Textes des Screenshots, der am naechsten dran war.
#
#      Damit ist die Frage beantwortbar, ohne zu raten: 0,00 mit einem
#      passenden "naechster" heisst, der Suchtext beschreibt, statt zu
#      zitieren. 1,00 bei einem einzigen kurzen Wort heisst, der
#      Suchtext ist zu unspezifisch und trifft irgendeinen.
#
#      Nur eine Anzeige — die Zuordnung selbst (ZC, rG) ist unberuehrt.
#
#      GEPRUEFT im Browser gegen eine nachgebaute Bibliothek mit drei
#      Screenshots und vier Platzhaltern:
#          0.00  Tag 1 · Slide 3  DM von einer Kundin
#          1.00  Tag 1 · Slide 2  seit unserem Gespraech schlafe ich...
#          1.00  Tag 2 · Slide 1  30 Anmeldungen fuer den Workshop
#          1.00  Tag 2 · Slide 2  Schlaf
#      Der Dialog meldete "3 von 4 zugeordnet" — die 0,00-Zeile ist
#      genau die fehlende.

# 172 — Kennung je Screenshot, neuer OCR-Lauf, Treffer per Kennung
P.append((
 '}},async uploadScreenshot(e){',
 '}},async updateScreenshotOcr({url:e,ocrText:t}){try{if(!Kr||!e)return{ok:!1,error:"Keine Supabase-Verbindung"};const{error:n}=await Kr.from("screenshot_library").update({ocr_text:t||""}).eq("url",e);return n?(console.error("OCR-Nachtrag fehlgeschlagen:",n),{ok:!1,error:n.message||"Nicht gespeichert"}):{ok:!0,error:null}}catch(n){return{ok:!1,error:(n==null?void 0:n.message)||"Unbekannter Fehler"}}},async uploadScreenshot(e){',
 'Supabase: OCR-Text nachtragen', 1))

P.append((
 'rG=.45,zPruefung=',
 'rG=.45,zKennung=zu=>{const zs=String(zu||"");if(!zs)return"S-00000";let zh=5381;for(let zi=0;zi<zs.length;zi+=1)zh=(zh*33^zs.charCodeAt(zi))>>>0;let zc=zh.toString(36).toUpperCase();while(zc.length<5)zc="0"+zc;return"S-"+zc.slice(-5)},zCode=zu=>{const zm=String(zu||"").toUpperCase().match(/S-[0-9A-Z]{5}/);return zm?zm[0]:null},zPruefung=',
 'Kennung aus der Adresse', 1))

P.append((
 'ZC=(e,t)=>{const r={};return e.forEach(n=>{let i=null;',
 'ZC=(e,t)=>{const r={};return e.forEach(n=>{const zk=zCode(n.matchText);if(zk){const zf=t.find(zx=>zx.kennung===zk);if(zf){r[n.id]={screenshotId:zf.id,score:1,perKennung:!0};return}}let i=null;',
 'Kennung schlaegt Aehnlichkeit', 1))

P.append((
 'zPruefung=(e,t)=>e.map(n=>{let zb=null;',
 'zPruefung=(e,t)=>e.map(n=>{const zk=zCode(n.matchText),zkf=zk?t.find(zx=>zx.kennung===zk):null;if(zk)return{id:n.id,wert:zkf?1:0,treffer:!!zkf,kennung:zk,wo:(zx=>zx.length>1?"Tag "+zx[0]+" \\u00b7 Slide "+(Number(zx[1])+1):String(n.id||""))(String(n.id||"").split("_")),suchtext:n.matchText||"",naechster:zkf?"Kennung gefunden":"Kennung "+zk+" gibt es in der Bibliothek nicht"};let zb=null;',
 'Kennung in der Pruefliste', 1))

P.append((
 '[f,p]=ce.useState(null),g=ce.useRef(null);',
 '[f,p]=ce.useState(null),[zMeld,zSetzMeld]=ce.useState(""),g=ce.useRef(null);',
 'Meldezeile', 1))

P.append((
 'const T=B.map((j,R)=>({id:`lib_${R}`,dataUrl:j.url,ocrText:j.ocrText,progress:1,fromLibrary:!0}));',
 'const T=B.map((j,R)=>({id:`lib_${R}`,dataUrl:j.url,ocrText:j.ocrText,progress:1,fromLibrary:!0,kennung:zKennung(j.url)}));',
 'Kennung an jede Bibliothekskachel', 1))

P.append((
 'R.dataUrl=I,s(F=>F.map(ee=>ee.id===j?{...ee,dataUrl:I}:ee))',
 'R.dataUrl=I,R.kennung=zKennung(I),s(F=>F.map(ee=>ee.id===j?{...ee,dataUrl:I,kennung:zKennung(I)}:ee))',
 'Kennung an frisch hochgeladene', 1))

P.append((
 'v.jsxs("button",{onClick:()=>{var b;return(b=g.current)==null?void 0:b.click()},disabled:l,',
 'i.length>0&&v.jsxs("div",{className:"flex gap-2",children:[v.jsx("button",{onClick:()=>{const zt=i.map(zx=>(zx.kennung||"?")+"\\t"+String(zx.ocrText||"").replace(/\\s+/g," ").trim()).join("\\n");let zo=!1;try{const ze=document.createElement("textarea");ze.value=zt;ze.style.position="fixed";ze.style.opacity="0";document.body.appendChild(ze);ze.select();zo=document.execCommand("copy");document.body.removeChild(ze)}catch(zz){}try{navigator.clipboard&&navigator.clipboard.writeText(zt).then(()=>zSetzMeld(i.length+" Kennungen kopiert"),()=>{})}catch(zz){}zSetzMeld(zo||navigator.clipboard?i.length+" Kennungen kopiert":"Kopieren ging nicht")},className:"flex-1 py-2 rounded-lg border border-gray-200 bg-white text-xs font-bold text-gray-700 hover:bg-gray-50",children:"Kennungen + Text kopieren"}),v.jsx("button",{onClick:zNeuOcr,disabled:l,className:"flex-1 py-2 rounded-lg border border-purple-200 bg-white text-xs font-bold text-purple-700 hover:bg-purple-50 disabled:opacity-40",children:l?"OCR läuft…":"OCR neu einlesen"})]}),zMeld&&v.jsx("div",{className:"text-xs text-gray-500",children:zMeld}),v.jsxs("button",{onClick:()=>{var b;return(b=g.current)==null?void 0:b.click()},disabled:l,',
 'Knoepfe kopieren + OCR neu', 1))

P.append((
 'v.jsx("div",{className:"flex-1 min-w-0",children:b.progress<1?',
 'v.jsxs("div",{className:"flex-1 min-w-0",children:[v.jsx("p",{className:"text-[10px] font-mono font-bold text-purple-700",children:b.kennung||""}),b.progress<1?',
 'Kennung in der Liste (auf)', 1))

P.append((
 'children:b.ocrText.slice(0,60)||"(kein Text erkannt)"})})]},b.id))',
 'children:b.ocrText.slice(0,60)||"(kein Text erkannt)"})]})]},b.id))',
 'Kennung in der Liste (zu)', 1))

P.append((
 'const m=async b=>{const B=Array.from(b||[]);',
 'const zNeuOcr=async()=>{o(!0),zSetzMeld("");let zn=0,zf=0;for(const zit of i){if(!zit.fromLibrary)continue;s(K=>K.map(F=>F.id===zit.id?{...F,progress:0}:F));const zt=await tG(zit.dataUrl,zp=>{s(K=>K.map(F=>F.id===zit.id?{...F,progress:zp}:F))});s(K=>K.map(F=>F.id===zit.id?{...F,ocrText:zt||F.ocrText,progress:1}:F));if(zt){zn+=1;const zr=await au.updateScreenshotOcr({url:zit.dataUrl,ocrText:zt});zr.ok||(zf+=1)}else zf+=1;zSetzMeld(zn+" neu gelesen"+(zf?", "+zf+" ohne Text":""))}s(K=>(u(ZC(r,K)),K)),o(!1),zSetzMeld(zn+" von "+i.length+" neu eingelesen"+(zf?", "+zf+" ohne Ergebnis":""))},m=async b=>{const B=Array.from(b||[]);',
 'OCR neu einlesen', 1))

# 172  Kennung je Screenshot und ein neuer OCR-Lauf
#
#      "Baue mir eine Kennung die den Screenshot labelt und mach einen
#      erneuten OCR Scan moeglich. Dann kann ich die Labels mit dem OCR
#      Scan dem Content weitergeben und es passt besser zusammen."
#
#      Der aehnlichkeitsbasierte Abgleich hat bei ihr 0 von 61 Platz-
#      haltern getroffen. Statt an der Schwelle zu drehen, bekommt jeder
#      Screenshot eine feste KENNUNG, und die schlaegt jede Aehnlichkeit.
#
#      KENNUNG: djb2-xor ueber die Bildadresse, 5 Stellen Base36,
#      "S-PXQPF". Sie haengt nur an der Adresse — nicht an Reihenfolge,
#      nicht an einer laufenden Nummer. Ein geloeschter Screenshot
#      verschiebt also keine andere Kennung. Bei 131 Bildern liegt die
#      Wahrscheinlichkeit einer Doppelung bei rund 0,014 Prozent.
#
#      ABGLEICH: steht "S-PXQPF" im Platzhaltertext, wird genau der
#      Screenshot genommen, Wert 1,00, ohne Wortvergleich. Sonst laeuft
#      der alte Weg weiter. Die Pruefliste aus 171 zeigt bei einer
#      Kennung, die es nicht gibt, genau das an.
#
#      OCR NEU EINLESEN: laeuft ueber alle Bilder der Bibliothek,
#      schreibt den Text per update in screenshot_library zurueck.
#      WICHTIG: ein leeres Ergebnis ueberschreibt nichts — weder in
#      Supabase noch in der Anzeige. Ein fehlgeschlagener Lauf kann also
#      keine vorhandenen Texte vernichten.
#
#      KENNUNGEN + TEXT KOPIEREN: legt "S-PXQPF<Tab>OCR-Text" je Zeile
#      in die Zwischenablage. Damit kann sie beim Schreiben des Plans
#      direkt die Kennung in die Slide setzen.
#
#      GEPRUEFT im Browser gegen eine nachgebaute Bibliothek mit drei
#      Screenshots:
#          Kennungen S-PXQPC / S-PXQPF / S-PXQPE, alle verschieden
#          "Screenshot: S-PXQPF" -> 1,00, "Kennung gefunden"
#          "Screenshot: S-XXXXX" -> 0,00, "gibt es in der Bibliothek nicht"
#          2 von 3 zugeordnet, "Platzieren" wird aktiv
#          Kopieren legt die Zeilen in die Zwischenablage
#          OCR-Lauf ohne Ergebnis: Texte vorher = Texte nachher

# 173 — Eine Kachel, die einmal ein Bild war, konnte sich nie mehr aendern
P.append((
 'const{brandSettings:l}=In(),o=ce.useRef(null),a=ce.useRef(null),[u,d]=ce.useState(!1),[A,h]=ce.useState(null),c=ce.useRef(0),f=ce.useRef(Promise.resolve());return ce.useEffect(',
 'const{brandSettings:l}=In(),o=ce.useRef(null),a=ce.useRef(null),[u,d]=ce.useState(!1),[A,h]=ce.useState(null),c=ce.useRef(0),f=ce.useRef(Promise.resolve()),zFing=(()=>{try{return JSON.stringify(e,(zk,zv)=>typeof zv=="string"&&zv.length>64?zv.length+":"+zv.slice(0,24):zv)}catch(zz){return""}})(),zVor=ce.useRef(""),[zNeu,zSetzNeu]=ce.useState(0);ce.useEffect(()=>{if(zVor.current&&zVor.current!==zFing){h(null),zSetzNeu(zx=>zx+1)}zVor.current=zFing},[zFing]);return ce.useEffect(',
 'Kachel merkt sich ihren Inhalt', 1))

P.append((
 '},[e,u,n]),v.jsx("div",{className:"bs-canvas-fit',
 '},[e,u,n,zNeu]),v.jsx("div",{className:"bs-canvas-fit',
 'Zeichnen nach Inhaltswechsel', 1))

# 173  Die Kachel konnte sich nie mehr aendern
#
#      "Der Screenshot taucht eben nicht auf trotz Match."
#
#      Nachgestellt: Treffer per Kennung, "Platzieren" gedrueckt, Plan
#      in der Datenbank korrekt mit overlayImage — und die Kachel zeigt
#      weiter den alten Text. Nach dem Neuladen ist der Screenshot da.
#
#      URSACHE, mit Sonden im laufenden Bundle eingekreist. Das Gitter
#      liefert die neuen Daten (Sonde: "ov:ja"), uG und XV zeichnen sich
#      neu — aber der ZEICHEN-EFFEKT lief nie wieder. Der Grund:
#
#          useEffect(()=>{ if(!o.current) return;
#            const p=new fabric.StaticCanvas(o.current,...);
#            return a.current=p, ()=>{ p.dispose(); a.current=null } },[A])
#
#      A ist das fertige Bild. Sobald es da ist, rendert die Komponente
#      ein <img> STATT des <canvas>. Dieser Effekt laeuft dann noch
#      einmal, raeumt den Canvas ab und setzt a.current=null — und
#      findet kein o.current mehr, um einen neuen zu bauen. Ab da bricht
#      der Zeichen-Effekt bei "if(!p) return" sofort ab.
#
#      Eine Kachel konnte sich also nie wieder aendern, sobald sie
#      einmal ein Bild erzeugt hatte. Nur ein Neuladen half. Das betraf
#      nicht nur Screenshots, sondern jede Aenderung am Plan.
#
#      REPARATUR: die Kachel merkt sich einen Fingerabdruck ihres
#      Inhalts (JSON, lange Zeichenketten auf Laenge+Anfang gekuerzt,
#      damit ein data-Bild das nicht teuer macht). Aendert er sich,
#      wird A auf null gesetzt — der <canvas> kommt zurueck, der
#      Effekt baut ihn neu — und ein Zaehler in den Abhaengigkeiten des
#      Zeichen-Effekts loest genau ein Neuzeichnen aus.
#
#      Der Canvas wird danach wie bisher wieder abgeraeumt. Kein
#      Mehrverbrauch an Speicher, keine Schleife.
#
#      GEPRUEFT im Browser:
#          vorher   Bild vor und nach "Platzieren" Byte fuer Byte gleich
#          nachher  9739 Byte -> 7995 Byte, der Screenshot steht da
#          12 Kacheln = 12 Zeichnungen, 8 Sekunden spaeter immer noch 12
#          0 Canvas im DOM, 12 Kachelbilder

# 174 — Die Kennung allein macht eine Slide zum Platzhalter
P.append((
 'q$=e=>{if(!e||typeof e!="string")return null;const t=e.trim();if(!/screenshot/i.test(t))return null;',
 'q$=e=>{if(!e||typeof e!="string")return null;const t=e.trim();const zk=t.toUpperCase().match(/\\bS-[0-9A-Z]{5}\\b/);if(zk)return zk[0];if(!/screenshot/i.test(t))return null;',
 'Kennung allein genuegt', 1))

P.append((
 'zCode=zu=>{const zm=String(zu||"").toUpperCase().match(/S-[0-9A-Z]{5}/);return zm?zm[0]:null},',
 'zCode=zu=>{const zm=String(zu||"").toUpperCase().match(/\\bS-[0-9A-Z]{5}\\b/);return zm?zm[0]:null},',
 'Kennung mit Wortgrenzen', 1))

P.append((
 'children:"[SCREENSHOT — …]"}),"-Platzhalter im aktuellen Plan gefunden. Füge sie per Bulk Import ein, z.\xa0B.:"',
 'children:"S-XXXXX"}),"-Kennung und kein „Screenshot“ im Plan gefunden. Schreib die Kennung aus der Liste unten in die Slide, z.\xa0B.:"',
 'Hinweistext', 1))

P.append((
 'children:\'[SCREENSHOT — "Btw: 30 Anmeldungen für den Workshop"]\'',
 'children:"Slide 2: S-PXQPF"',
 'Beispiel', 1))

# 174  Die Kennung allein genuegt
#
#      "Der Check soll auf die Id gehen, jetzt gehst du in dem Kasten
#      immer noch ueber den Text???"
#
#      Berechtigt. Die Kennungspruefung aus 172 schlaegt zwar jede
#      Aehnlichkeit — aber sie kam nur zum Zug, wenn die Slide ueber-
#      haupt als Platzhalter erkannt wurde, und dafuer verlangte q$ das
#      Wort "Screenshot". Eine Slide, in der nur "S-PXQPF" stand, war
#      unsichtbar. Der Text blieb also der Tuerhueter, obwohl die
#      Kennung entscheiden sollte.
#
#      Jetzt: steht irgendwo im Slide-Text eine Kennung, ist die Slide
#      ein Platzhalter und die Kennung IST der Suchtext. Alles andere
#      in der Zeile wird ignoriert. Gross- und Kleinschreibung egal.
#      Ohne Kennung laeuft der alte Weg ueber das Zitat unveraendert
#      weiter.
#
#      Wortgrenzen dazu, damit nichts hineinrutscht, was zufaellig so
#      aussieht: "Die S-Klasse von Mercedes." ist kein Platzhalter.
#
#      GEPRUEFT im Browser, Bibliothek mit einem Screenshot S-RLFHP:
#          "S-RLFHP"               -> 1,00  Kennung gefunden
#          "s-rlfhp"               -> 1,00  Kennung gefunden
#          "Screenshot: S-RLFHP"   -> 1,00  Kennung gefunden
#          "Die S-Klasse von ..."  -> gar kein Platzhalter
#          Zitat ohne Kennung      -> alter Weg, Wortvergleich
#      4 Platzhalter im Plan, 3 von 4 zugeordnet.

# 175 — Der Screenshot wurde stillschweigend nicht gezeichnet
P.append((
 'Ae=ge=>new Promise(Fe=>{if(!ge)return Fe(!1);Pe.fabric.Image.fromURL(ge,me=>{if(!me)return Fe(!1);if(t.overlayIsScreenshot){',
 'Ae=ge=>new Promise(Fe=>{if(!ge)return Fe(!1);const zMal=me=>{if(t.overlayIsScreenshot){',
 'Zeichnen des Screenshots als eigene Funktion', 1))

P.append((
 'e.add(me),Fe(!0)},{crossOrigin:"anonymous"})}),$=typeof t.background=="string"',
 'e.add(me),Fe(!0)};Pe.fabric.Image.fromURL(ge,zm=>{if(zm&&zm.width>0)return zMal(zm);Pe.fabric.Image.fromURL(ge,zn=>{zn&&zn.width>0?zMal(zn):Fe(!1)},{crossOrigin:null})},{crossOrigin:"anonymous"})}),$=typeof t.background=="string"',
 'Zweiter Ladeversuch ohne CORS', 1))

# 175  Warum der Screenshot nicht kam
#
#      "Es stehen zuerst die Kuerzel dort und sind dann weg, aka ok
#      erkannt — aber das Bild des Screenshots kommt dann nicht."
#
#      Genau nachgestellt: Server, der die JSON-Schnittstelle mit CORS
#      ausliefert, die BILDER aber ohne. Ergebnis: leere Kachel, kein
#      Foto, kein Screenshot. Ihr Symptom, Punkt fuer Punkt.
#
#      Der Zeichner laedt Bilder mit crossOrigin:"anonymous". Fehlt die
#      Freigabe, scheitert das Laden. Und jetzt der eigentliche Fehler:
#
#          fabric.Image.fromURL liefert dann KEIN null, sondern ein
#          Bild mit width 0.
#
#      Der bestehende Code prueft nur "if(!me) return" — ein Bild der
#      Breite 0 rutscht durch. Danach rechnet er
#      "r*scale/me.width" = Unendlich, die weisse Platte bekommt NaN
#      als Breite, und es wird gar nichts sichtbar. Kein Fehler, keine
#      Meldung, nur eine leere Kachel.
#
#      REPARATUR: Ladeversuch als eigene Funktion, dann
#        1. Versuch mit crossOrigin "anonymous" — Breite pruefen
#        2. schlaegt der fehl: noch einmal OHNE crossOrigin
#      Damit wird das Bild sichtbar, auch wenn der Bucket keine
#      Freigabe schickt.
#
#      PREIS, ehrlich: ein ohne crossOrigin geladenes Bild macht den
#      Canvas "unrein". Solche Kacheln lassen sich nicht mehr in ein
#      Bild umwandeln — gemessen: 1 von 4 statt 4 von 4. Sie behalten
#      ihren Canvas (mehr Speicher) und "Alle in Fotos" kann sie nicht
#      exportieren. Die eigentliche Heilung ist die CORS-Freigabe am
#      Supabase-Bucket. Der zweite Versuch ist das Netz, nicht die Kur.
#
#      GEPRUEFT, beide Richtungen:
#          ohne CORS  vorher leere Kacheln -> nachher Screenshot da
#          mit  CORS  34% rot / 60% blau auf Tag 1, unveraendert wie
#                     vor der Aenderung, also kein Rueckschritt

# 176 — Rosa Fehlerkacheln: gezeichnet auf einen Canvas, den es nicht mehr gibt
P.append((
 'f.current=f.current.then(async()=>{var b;if(w===c.current&&a.current)return Ca(p,e,g,m,{',
 'f.current=f.current.then(async()=>{var b;if(w===c.current&&a.current===p)return Ca(p,e,g,m,{',
 'Nur auf den aktuellen Canvas zeichnen', 1))

P.append((
 '.catch(b=>{console.error("renderSlide failed:",b);try{p.clear(),p.backgroundColor="#FFE9E9"',
 '.catch(b=>{if(a.current!==p)return;console.error("renderSlide failed:",b);try{p.clear(),p.backgroundColor="#FFE9E9"',
 'Keine Fehlerkachel bei veraltetem Canvas', 1))

# 176  Rosa Fehlerkacheln
#
#      Auf der Kachel stand: "Zeichnen fehlgeschlagen /
#      null is not an object (evaluating '...clearRect')".
#
#      clearRect auf einem Canvas, den es nicht mehr gibt. Und das ist
#      eine Folge von 173: seitdem wird der Canvas bei jeder
#      Inhaltsaenderung abgeraeumt und neu gebaut.
#
#      Der Zeichen-Effekt merkt sich seinen Canvas beim Start:
#
#          const p = a.current;
#          f.current = f.current.then(async () => {
#            if (w === c.current && a.current) return Ca(p, e, ...)  })
#
#      Die Pruefung fragt "gibt es ueberhaupt einen Canvas", gezeichnet
#      wird aber auf das gemerkte p. Wenn zwischen Einreihen und
#      Ausfuehren der Canvas ausgetauscht wurde, ist a.current der NEUE
#      und p der abgeraeumte alte. Ca ruft darauf clear() -> der
#      Zeichenkontext ist null -> Ausnahme -> rosa Kachel.
#
#      Bei ihr faellt das auf, weil ~100 Kacheln lange zeichnen und
#      Aenderungen mitten hinein fallen. Im Test mit 9 schnellen
#      Kacheln war es nicht zu provozieren.
#
#      ZWEI ZEILEN:
#        1. a.current === p statt a.current — nie auf einen Canvas
#           zeichnen, der nicht mehr der aktuelle ist. Der uebersprungene
#           Lauf ist nicht verloren: der Effekt laeuft mit dem neuen
#           Canvas ohnehin erneut.
#        2. im catch zuerst pruefen, ob p noch aktuell ist. Ein
#           Lebenszyklus-Rennen soll keine Fehlerkachel malen.
#
#      GEPRUEFT: Screenshot auf Foto und Textkachel unveraendert
#      (34% rot / 60% blau), "Platzieren" aktualisiert die Kachel weiter
#      (9739 -> 7995 Byte), 12 Kacheln gezeichnet, keine Schleife,
#      0 Canvas im DOM.

# 177 — Die Fehlerkachel spricht Deutsch
P.append((
 'const B=String(b&&b.message?b.message:b).slice(0,140);p.add(new Pe.fabric.Text("Zeichnen fehlgeschlagen",{left:20,top:20,fontSize:22,fontFamily:"Helvetica",fill:"#B00020",selectable:!1})),p.add(new Pe.fabric.Textbox(B,{left:20,top:56,width:Math.max(120,g-40),fontSize:15,fontFamily:"Helvetica",fill:"#7A0016",selectable:!1})),p.renderAll()',
 'const B=(zm=>{if(/null is not an object|Cannot read propert|of null|of undefined|undefined is not an object/i.test(zm))return "Die Kachel wurde neu gebaut, w\\u00e4hrend sie noch gezeichnet hat. Beim n\\u00e4chsten Zeichnen ist sie wieder da.";if(/SecurityError|tainted|cross-origin|crossorigin|insecure/i.test(zm))return "Ein Bild ist nicht freigegeben. In Supabase beim Bucket die Herkunft dieser Seite erlauben.";if(/load|network|fetch|Failed to|ERR_/i.test(zm))return "Ein Bild konnte nicht geladen werden. Adresse pr\\u00fcfen oder den Screenshot neu hochladen.";if(/quota|memory|allocation|out of/i.test(zm))return "Der Speicher ist voll. Weniger Tage offen halten und neu laden.";return "Unerwarteter Fehler. Die genaue Meldung steht in der Entwicklerkonsole:\\n"+zm.slice(0,90);})(String(b&&b.message?b.message:b));p.add(new Pe.fabric.Textbox("Diese Kachel kam nicht durch",{left:g*.08,top:m*.30,width:g*.84,fontSize:g*.055,fontFamily:"Helvetica",fontWeight:"700",fill:"#B00020",textAlign:"center",lineHeight:1.2,selectable:!1})),p.add(new Pe.fabric.Textbox(B,{left:g*.08,top:m*.42,width:g*.84,fontSize:g*.040,fontFamily:"Helvetica",fill:"#7A0016",textAlign:"center",lineHeight:1.35,selectable:!1})),p.renderAll()',
 'Fehlerkachel spricht Deutsch', 1))

# 177  Die Fehlerkachel spricht Deutsch
#
#      "Null is not an object - na geh bitte schreib gescheit."
#
#      Zu Recht. Die Fehlerkachel hat die rohe Browsermeldung
#      hingeschrieben, in Englisch, in 15 Pixeln, hinter dem Tag-Schild.
#      Das sagt ihr nichts.
#
#      Jetzt: die Meldung wird uebersetzt, gross und mittig gesetzt.
#
#          null/undefined-Zugriff -> "Die Kachel wurde neu gebaut,
#            waehrend sie noch gezeichnet hat. Beim naechsten Zeichnen
#            ist sie wieder da."
#          SecurityError/tainted  -> "Ein Bild ist nicht freigegeben.
#            In Supabase beim Bucket die Herkunft dieser Seite erlauben."
#          Ladefehler             -> "Ein Bild konnte nicht geladen
#            werden. Adresse pruefen oder neu hochladen."
#          Speicher               -> "Der Speicher ist voll. Weniger
#            Tage offen halten und neu laden."
#          alles andere           -> kurzer Hinweis plus die ersten 90
#            Zeichen der Originalmeldung, damit nichts verloren geht.
#
#      Ueberschrift "Zeichnen fehlgeschlagen" -> "Diese Kachel kam nicht
#      durch". Schrift von 22 auf g*0.055 (also 44 statt 22 auf einer
#      800er Flaeche), Text von 15 auf g*0.040, beides zentriert und auf
#      30 bzw. 42 Prozent Hoehe — weg vom Tag-Schild.
#
#      Die technische Meldung geht weiter per console.error hinaus.
#
#      GEPRUEFT: Fehler kuenstlich ausgeloest, Kachel zeigt gross und
#      lesbar "Diese Kachel kam nicht durch" mit dem deutschen Satz.

# 178 — Jeder Ausgang des Zeichners zeichnet den Screenshot
P.append((
 'fill:"rgba(247,244,239,0.75)",selectable:!1})),e.renderAll();return}',
 'fill:"rgba(247,244,239,0.75)",selectable:!1})),t.overlayImage&&await Ae(t.overlayImage).catch(()=>{}),e.renderAll();return}',
 'Ausgang 1: Deckblatt', 1))

P.append((
 'if(wt(Ab,t.text)){e.renderAll();return}',
 'if(wt(Ab,t.text)){t.overlayImage&&await Ae(t.overlayImage).catch(()=>{}),e.renderAll();return}',
 'Ausgang 2: Karte auf dem Foto', 1))

P.append((
 'wt(Ye,t.text))){e.renderAll();return}',
 'wt(Ye,t.text))){t.overlayImage&&await Ae(t.overlayImage).catch(()=>{}),e.renderAll();return}',
 'Ausgang 3: Karte auf Farbgrund', 1))

P.append((
 'opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1})),Le(),e.renderAll();return}',
 'opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1})),Le(),t.overlayImage&&await Ae(t.overlayImage).catch(()=>{}),e.renderAll();return}',
 'Ausgang 4: Name unten', 1))

P.append((
 'if(!jt&&!_t&&!ar){e.renderAll();return}',
 'if(!jt&&!_t&&!ar){t.overlayImage&&await Ae(t.overlayImage).catch(()=>{}),e.renderAll();return}',
 'Ausgang 5: nichts zu setzen', 1))

P.append((
 'Pe.fabric.Image.fromURL(ge,zn=>{zn&&zn.width>0?zMal(zn):Fe(!1)},{crossOrigin:null})',
 'Pe.fabric.Image.fromURL(ge,zn=>{if(zn&&zn.width>0)return zMal(zn);try{const zb=r*.72,zh2=zb*.46,zx=r/2,zy=n/2;e.add(new Pe.fabric.Rect({left:zx,top:zy,originX:"center",originY:"center",width:zb,height:zh2,rx:14*d,ry:14*d,fill:"#FFF3F3",stroke:"#B00020",strokeWidth:2*d,selectable:!1}));e.add(new Pe.fabric.Textbox("Screenshot konnte nicht geladen werden",{left:zx-zb/2,top:zy-zh2*.30,width:zb,fontSize:r*.038,fontFamily:"Helvetica",fontWeight:"700",fill:"#B00020",textAlign:"center",lineHeight:1.2,selectable:!1}));e.add(new Pe.fabric.Textbox(String(ge).slice(-40),{left:zx-zb/2,top:zy+zh2*.04,width:zb,fontSize:r*.026,fontFamily:"Helvetica",fill:"#7A0016",textAlign:"center",lineHeight:1.25,selectable:!1}))}catch(zz){}Fe(!1)},{crossOrigin:null})',
 'Sichtbare Meldung, wenn der Screenshot nicht ladbar ist', 1))

# 178  Jeder Ausgang zeichnet den Screenshot, und Scheitern wird sichtbar
#
#      "Geht nicht ums Erkennen, sondern dass es der Zeichner zeichnet!!!"
#
#      Nachgezaehlt: der Zeichner hat 21 Ausgaenge. 16 zeichnen den
#      Screenshot vor dem Verlassen, 5 nicht — darunter die beiden
#      Karten-Ausgaenge (Karte auf dem Foto, Karte auf Farbgrund).
#      Diese Luecke ist jetzt geschlossen: 21 von 21.
#
#      EHRLICH: in einer Matrix aus 12 Konfigurationen (karte hell /
#      stein / keine, mit und ohne Foto, mit und ohne Text) aendert das
#      NICHTS — vorher wie nachher wird der Screenshot ueberall
#      gezeichnet. Auch der Durchlauf mit ihrem echten Plan (100 Tage,
#      619 Slides, 103 Platzhalter, 52 Zuordnungen) zeigt die
#      Screenshots auf den Kacheln. Ihr Fall ist hier also nicht
#      nachstellbar; die Luecke war trotzdem real und ist zu.
#
#      DESHALB ZUSAETZLICH: ein stilles Scheitern wird sichtbar. Wenn
#      beide Ladeversuche fehlschlagen (mit und ohne CORS), zeichnet
#      die Kachel jetzt einen rot umrandeten Kasten:
#
#          "Screenshot konnte nicht geladen werden"
#          <die letzten 40 Zeichen der Adresse>
#
#      Damit steht auf der Kachel, ob der Zeichner es gar nicht erst
#      versucht hat (nichts zu sehen) oder ob das Bild nicht kommt
#      (Kasten mit Adresse). Das trennt die beiden Faelle endlich.
#
#      GEPRUEFT: kaputte Adresse -> Kasten mit Adresse; gute Adresse
#      daneben -> Screenshot. Keine Veraenderung an den 12
#      Konfigurationen.

# 179 — Ein Fehlschlag hat die Kachel fuer immer vergiftet
P.append((
 'zVor=ce.useRef(""),[zNeu,zSetzNeu]=ce.useState(0);',
 'zVor=ce.useRef(""),zVers=ce.useRef(0),[zNeu,zSetzNeu]=ce.useState(0);',
 'Zaehler fuer Wiederholungen', 1))

P.append((
 'Promise.resolve(f.current).then(()=>{if(i&&a.current)try{const b=a.current.toDataURL({format:"jpeg",quality:.85,multiplier:.5});',
 'Promise.resolve(f.current).then(()=>{zVers.current=0;if(i&&a.current)try{const b=a.current.toDataURL({format:"jpeg",quality:.85,multiplier:.5});',
 'Nach Erfolg zuruecksetzen', 1))

P.append((
 '.catch(b=>{if(a.current!==p)return;console.error("renderSlide failed:",b);',
 '.catch(b=>{if(a.current!==p)return;const zM=String(b&&b.message?b.message:b);if(/null is not an object|Cannot read propert|of null|of undefined|undefined is not an object/i.test(zM)&&zVers.current<3){zVers.current+=1;zSetzNeu(zx=>zx+1);return}console.error("renderSlide failed:",b);',
 'Statt Meldung: noch einmal zeichnen', 1))

P.append((
 'f.current=f.current.then(async()=>{var b;',
 'const zLauf=f.current.then(async()=>{var b;',
 'Lauf getrennt von der Kette', 1))

P.append((
 'typography})}),Promise.resolve(f.current).then(()=>{zVers.current=0;',
 'typography})});f.current=zLauf.catch(()=>{}),Promise.resolve(zLauf).then(()=>{zVers.current=0;',
 'Kette bleibt sauber, Fehler wird trotzdem behandelt', 1))

P.append((
 'return "Die Kachel wurde neu gebaut, w\\u00e4hrend sie noch gezeichnet hat. Beim n\\u00e4chsten Zeichnen ist sie wieder da.";',
 'return "Die Kachel wurde beim Zeichnen unterbrochen und hat sich nach drei weiteren Versuchen nicht erholt. Seite neu laden.";',
 'Meldung stimmt jetzt: Versuche sind erschoepft', 1))

# 179  Ein Fehlschlag hat die Kachel fuer immer vergiftet
#
#      "Geht. Es steht manchmal nur, es konnte nicht gezeichnet werden
#      und kaeme beim naechsten Mal."
#
#      Meine eigene Meldung aus 177 — und sie war eine Luege. Die
#      Kachel kam NICHT beim naechsten Mal. Grund:
#
#          f.current = f.current.then(async () => { ... })
#
#      Der Zeichner reiht seine Laeufe in eine Kette. Scheitert ein
#      Glied, ist f.current ein ABGELEHNTES Versprechen — und jedes
#      spaetere .then() darauf wird uebersprungen. Ab dem ersten Fehler
#      zeichnet diese Kachel nie wieder. Sie malt nur noch die
#      Fehlermeldung, bei jedem Anlauf.
#
#      Das erklaert auch, warum die rosa Kacheln blieben, obwohl 176
#      die Ursache des Rennens behoben hat: die Kette war vergiftet.
#
#      REPARATUR, zwei Teile:
#        1. Lauf und Kette trennen:
#             const zLauf = f.current.then(async () => {...});
#             f.current  = zLauf.catch(() => {});
#             Promise.resolve(zLauf).then(...).catch(...)
#           Reihenfolge bleibt, Fehlerbehandlung bleibt, aber die Kette
#           traegt nie eine Ablehnung weiter.
#        2. Beim Lebenszyklus-Rennen wird wirklich noch einmal
#           gezeichnet statt es nur zu behaupten: bis zu DREI weitere
#           Versuche ueber einen Zaehler in den Abhaengigkeiten, nach
#           einem gelungenen Zeichnen zurueckgesetzt. Erst wenn auch
#           die drei scheitern, erscheint die Meldung — und die sagt
#           jetzt die Wahrheit: "hat sich nach drei weiteren Versuchen
#           nicht erholt. Seite neu laden."
#
#      GEPRUEFT, Fehler kuenstlich erzwungen:
#          zwei Fehlschlaege, dann klappt es -> normale Kachel
#          dauerhafter Fehler -> genau 4 Versuche, dann die Meldung,
#            keine Schleife
#          12 Konfigurationen vorher = nachher
#          12 Kacheln = 12 Zeichnungen, 0 Canvas im DOM

# 180 — Textkachel auf Bodoni Moda
P.append((
 'schriftart:"Marcellus",unterSchrift:"Marcellus"',
 'schriftart:"Bodoni Moda",unterSchrift:"Bodoni Moda"',
 'Textkachel auf Bodoni Moda', 1))

# 180  Textkachel auf Bodoni Moda
#
#      "Marcellus und Playfair finde ich zu unterschiedlich." — stimmt,
#      und der Grund ist benennbar: Playfair ist eine Didone, duenne
#      Haarstriche gegen dicke Grundstriche. Marcellus ist eine
#      roemische Kapitalis, fast gleichmaessig dick. Zwei Welten.
#
#      Verglichen wurden Playfair Display, Prata, Bodoni Moda,
#      DM Serif Display und Marcellus, gerendert mit den echten
#      Schriftdateien im selben Satz und derselben Groesse:
#
#          Playfair Display  dieselbe Stimme wie das Foto
#          Prata             gleiche Welt, etwas fester
#          Bodoni Moda       mehr Kontrast, eleganter, feinere Haare
#          DM Serif Display  viel zu schwer, wirkt fett
#          Marcellus         flacher Kontrast, andere Welt
#
#      Sie hat Bodoni Moda gewaehlt. Nur schriftart und unterSchrift
#      wechseln; Playfair bleibt auf Fotos, Deckblatt, Folgeslides,
#      Name und Ablauf.
#
#      Bodoni steht in tiefeSchriften, das dunkle Band unter dem Text
#      bleibt also erhalten. Die Schriftdateien liegen als
#      BodoniModa-Regular (400) und -Bold (700) vor.
#
#      MOEGLICHE NACHBESSERUNG: Bodonis Haarstriche koennen auf dem
#      Handy duenn werden. Falls ja, gewicht von "400" auf "500" oder
#      "600" — das ist ein Wort.

# 181 — Kein Versalien-Wechsel auf dem Cover, nur noch eine Handschrift
P.append((
 'versalAnteil:15',
 'versalAnteil:0',
 'Kein Versalien-Wechsel mehr', 1))

P.append((
 'versalFamilie:"Shadows Into Light"',
 'versalFamilie:""',
 'Zweite Handschrift raus', 1))

# 181  Der zufaellige Versalien-Wechsel ist weg
#
#      "Es sind immer noch 2 Handschriften, ich will diesen
#      Versalien-Wechsel nicht auf dem Cover, da gibt's keine
#      Versalien-Schrift auf den Covers."
#
#      Im Zeichner stand:
#
#          const zVS = (() => {
#            if (!$e || !BS_KACHEL.versalAnteil) return false;
#            let zh = 0; for (...) zh = (zh*31 + charCode) % 99991;
#            return ((zh*7+11) % 100) < BS_KACHEL.versalAnteil;  // 15
#          })();
#          zVS && versalFamilie && (Qe = versalFamilie);
#
#      Auf JEDER Fotokachel — Cover eingeschlossen — wurde per Hash
#      ueber den Text gewuerfelt, und bei 15 von 100 wurde die ganze
#      Schrift auf "Shadows Into Light" umgestellt, dazu Laufweite 20.
#      Nicht nach Rolle, nicht nach Inhalt: nach Zufall. Genau daher
#      kam der Eindruck, der Account sei uneinig — der Blick sucht eine
#      Regel und findet keine.
#
#          versalAnteil   15 -> 0     der Wechsel feuert nie mehr
#          versalFamilie  "Shadows Into Light" -> ""
#
#      Damit ist auch die zweite Handschrift weg. Uebrig bleiben DREI
#      Schriften mit je einer Rolle:
#
#          Playfair Display      Deckblatt, Foto, Folgeslides, Name,
#                                Ablauf — die Aussage
#          Bodoni Moda           nur die Textkachel — die Pause
#          Nothing You Could Do  nur mit _Unterstrichen_ markierte
#                                Woerter — der Nachsatz
#
#      OFFEN GEBLIEBEN: schildSchrift steht weiter auf dem Grundwert
#      HelveticaNeueBrand, und folgeStil auf "montserrat". Beides
#      betrifft nur Kleinkram (Schildchen, Versalienstil auf
#      Folgeslides) und war nicht Teil ihrer Ansage.

# 182 — Alle Fotos als Story 9:16 herunterladen
P.append((
 'finally{o(!1)}}};return e.currentBrandConfig?v.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32",children:[',
 'finally{o(!1)}}};const[zSLauft,zSSetzLauft]=ce.useState(!1),[zSStand,zSSetzStand]=ce.useState("");const zStoryExport=async()=>{if(zSLauft)return;zSSetzLauft(!0),zSSetzStand("Fotos werden gesammelt \\u2026");try{const zRoh=(typeof window<"u"&&window.__bsBilder)||[];const zListe=[...new Set(zRoh.filter(zx=>typeof zx=="string"&&zx.length>5))];if(!zListe.length){zSSetzStand("Keine Fotos in der Bibliothek gefunden."),zSSetzLauft(!1);return}const zZip=new Dl,zOrd=zZip.folder("Stories_9_16");let zOk=0;for(let zi=0;zi<zListe.length;zi+=1){zSSetzStand("Zeichne "+(zi+1)+" von "+zListe.length+" \\u2026");const zc=document.createElement("canvas");zc.width=1080,zc.height=1920,zc.style.display="none";document.body.appendChild(zc);const zk=new Pe.fabric.StaticCanvas(zc,{width:1080,height:1920});try{await Ca(zk,{background:zListe[zi],text:"",format:"9:16",visualElements:[],satBoost:-1},1080,1920,{slideIndex:0,totalSlides:1,scale:1080/400,globalBrandName:""});let zd="";try{const zx2=zc.getContext("2d"),zim=zx2.getImageData(0,0,1080,1920),zdd=zim.data;for(let zq=0;zq<zdd.length;zq+=4){const zg=(zdd[zq]*.2126+zdd[zq+1]*.7152+zdd[zq+2]*.0722)|0;zdd[zq]=zg,zdd[zq+1]=zg,zdd[zq+2]=zg}zx2.putImageData(zim,0,0);zd=zc.toDataURL("image/jpeg",.92)}catch(zsw){zd=zk.toDataURL({format:"jpeg",quality:.92,multiplier:1})}zd&&zd.length>2e3&&(zOrd.file("Story-"+String(zi+1).padStart(3,"0")+".jpg",zd.split(",")[1],{base64:!0}),zOk+=1)}catch(zf){console.warn("Story-Export: ein Foto ging nicht",zf)}finally{try{zk.dispose()}catch(zz){}zc.parentNode&&zc.parentNode.removeChild(zc)}}if(!zOk){zSSetzStand("Kein Foto liess sich zeichnen."),zSSetzLauft(!1);return}zSSetzStand("ZIP wird gepackt \\u2026");const zBlob=await zZip.generateAsync({type:"blob"});ls.saveAs(zBlob,"BrandStudio-Stories-9-16.zip");zSSetzStand(zOk+" von "+zListe.length+" Fotos als ZIP geladen.")}catch(zz){zSSetzStand("Fehlgeschlagen: "+String(zz&&zz.message?zz.message:zz).slice(0,90))}zSSetzLauft(!1)};return e.currentBrandConfig?v.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32",children:[v.jsxs("div",{className:"mb-6 rounded-2xl border border-gray-200 bg-white p-4 flex flex-col sm:flex-row sm:items-center gap-3",children:[v.jsxs("div",{className:"flex-1 min-w-0",children:[v.jsx("div",{className:"text-sm font-bold text-gray-900",children:"Alle Fotos als Story (9:16)"}),v.jsx("div",{className:"text-[11px] text-gray-500 mt-0.5",children:zSStand||"Jedes Foto aus deiner Bibliothek: 1080\\u00d71920, Zoom-Schnitt, Bildlook wie im Feed \\u2014 als ein ZIP zum Ablegen in einen Ordner."})]}),v.jsx("button",{onClick:zStoryExport,disabled:zSLauft,className:"px-4 py-2.5 rounded-lg bg-gray-900 text-white text-xs font-bold disabled:opacity-40 whitespace-nowrap",children:zSLauft?"L\\u00e4uft \\u2026":"Als ZIP laden"})]}),',
 'Story-Export: alle Fotos 9:16 als ZIP', 1))

# 182  Alle Fotos als Story (9:16) als ein ZIP
#
#      "Legst du mir unter Stories alle Fotos auf Zoom geschnitten,
#      schwarzweiss, wie du sie im Feed nutzt, aber 9:16 rein zum
#      Download auf den Laptop?"
#
#      Auf der Stories-Seite oben ein Block mit einem Knopf. Er nimmt
#      jedes Foto aus window.__bsBilder (Bibliothek plus alle im Plan
#      verwendeten Bilder, doppelte raus), zeichnet es einzeln mit dem
#      ECHTEN Zeichner Ca auf 1080x1920 und packt alles per JSZip in
#      ein ZIP mit dem Ordner Stories_9_16.
#
#      Weil Ca benutzt wird, ist der Bildlook derselbe wie im Feed:
#      Zoom-Schnitt auf 9:16, Schleier, Vignette, Korn. Kein Text, kein
#      Name (globalBrandName leer).
#
#      SCHWARZWEISS WIRD GERECHNET, NICHT GEHOFFT. Der Zeichner
#      entsaettigt ueber einen Rechteck mit
#      globalCompositeOperation:"saturation" — und das haengt an
#      BS_MISCHBAR, also daran, ob der Browser diesen Mischmodus kann.
#      Im Test kam es farbig heraus. Deshalb rechnet der Export die
#      Luminanz jetzt selbst ueber getImageData (0.2126/0.7152/0.0722)
#      und faellt nur bei einem "unreinen" Canvas auf den alten Weg
#      zurueck.
#
#      GEPRUEFT: drei Fotos im Pool, ZIP mit drei Dateien, jede
#      1080x1920, Farbigkeit 0.0 (vorher 253), Helligkeit 54 — genau
#      die Luminanz von reinem Rot. Also echtes Schwarzweiss.
#
#      ZUM LAPTOP: die Bibliothek liegt in der IndexedDB des Browsers,
#      in dem sie arbeitet. Ein ZIP, das am Handy entsteht, muss ueber
#      Dateien/iCloud auf den Laptop. Am Laptop selbst waere die
#      Bibliothek leer — ausser die Bilder liegen auch im
#      Supabase-Pool, dann genuegen dort dieselben zwei
#      Supabase-Werte, ganz ohne Konto.

# 183 — ZIP-Eintraege als Blob statt Base64
P.append((
 'zd&&zd.length>2e3&&(zOrd.file("Story-"+String(zi+1).padStart(3,"0")+".jpg",zd.split(",")[1],{base64:!0}),zOk+=1)',
 'if(zd&&zd.length>2e3){const zbl=await(await fetch(zd)).blob();zbl&&zbl.size>2e3&&(zOrd.file("Story-"+String(zi+1).padStart(3,"0")+".jpg",zbl),zOk+=1)}',
 'ZIP-Eintraege als Blob statt Base64', 1))

# 183  Der Export soll auch mit 200 Fotos am Handy durchhalten
#
#      Sie macht den Export am Handy und schiebt das ZIP dann auf den
#      Laptop (Weg A). Damit haengt es an Safaris Speicher.
#
#      Bisher ging jedes Bild als BASE64-Zeichenkette in das ZIP. Base64
#      blaeht um ein Drittel auf, und JSZip haelt alles bis zum Packen
#      im Speicher. Bei 200 Fotos zu je etwa 250 KB waeren das rund 50 MB
#      echte Daten, aber 67 MB als Zeichenketten — zusaetzlich zum
#      spaeteren Blob. Genau daran stirbt Safari.
#
#      Jetzt wird die Daten-URL sofort in einen Blob verwandelt
#      (derselbe Weg, den "Alle in Fotos" schon nimmt) und der Blob ins
#      ZIP gelegt. Kein Base64, kein doppeltes Halten.
#
#      GEPRUEFT: drei Fotos, ZIP unveraendert lesbar, jede Datei
#      1080x1920, Farbigkeit 0.0, 13-18 KB je Bild.

# 184 — Story-Export: oben links schwarzweiss, der Rest farbig
P.append((
 'const zZip=new Dl,zOrd=zZip.folder("Stories_9_16");let zOk=0;for(let zi=0;zi<zListe.length;zi+=1){zSSetzStand("Zeichne "+(zi+1)+" von "+zListe.length+" \\u2026");const zc=document.createElement("canvas");zc.width=1080,zc.height=1920,zc.style.display="none";document.body.appendChild(zc);const zk=new Pe.fabric.StaticCanvas(zc,{width:1080,height:1920});try{await Ca(zk,{background:zListe[zi],text:"",format:"9:16",visualElements:[],satBoost:-1},1080,1920,{slideIndex:0,totalSlides:1,scale:1080/400,globalBrandName:""});let zd="";try{const zx2=zc.getContext("2d"),zim=zx2.getImageData(0,0,1080,1920),zdd=zim.data;for(let zq=0;zq<zdd.length;zq+=4){const zg=(zdd[zq]*.2126+zdd[zq+1]*.7152+zdd[zq+2]*.0722)|0;zdd[zq]=zg,zdd[zq+1]=zg,zdd[zq+2]=zg}zx2.putImageData(zim,0,0);zd=zc.toDataURL("image/jpeg",.92)}catch(zsw){zd=zk.toDataURL({format:"jpeg",quality:.92,multiplier:1})}if(zd&&zd.length>2e3){const zbl=await(await fetch(zd)).blob();zbl&&zbl.size>2e3&&(zOrd.file("Story-"+String(zi+1).padStart(3,"0")+".jpg",zbl),zOk+=1)}}catch(zf){console.warn("Story-Export: ein Foto ging nicht",zf)}finally{try{zk.dispose()}catch(zz){}zc.parentNode&&zc.parentNode.removeChild(zc)}}',
 'const zZip=new Dl,zOrd=zZip.folder("Stories_9_16");let zOk=0;const zLad=zu=>new Promise(zr=>{const za=new Image;za.crossOrigin="anonymous";za.onload=()=>zr(za);za.onerror=()=>{const zb2=new Image;zb2.onload=()=>zr(zb2);zb2.onerror=()=>zr(null);zb2.src=zu};za.src=zu});for(let zi=0;zi<zListe.length;zi+=1){zSSetzStand("Schneide "+(zi+1)+" von "+zListe.length+" \\u2026");try{const zim=await zLad(zListe[zi]);if(!zim||!zim.width||!zim.height)continue;const zc=document.createElement("canvas");zc.width=1080,zc.height=1920;const zx=zc.getContext("2d");zx.fillStyle="#000",zx.fillRect(0,0,1080,1920);try{zx.filter="grayscale(1)"}catch(zz){}const zf=Math.max(1080/zim.width,1920/zim.height),zw=zim.width*zf,zh=zim.height*zf;zx.drawImage(zim,(1080-zw)/2,(1920-zh)/2,zw,zh);try{zx.filter="none"}catch(zz){}try{const zid=zx.getImageData(0,0,1080,1920),zdd=zid.data;let zbunt=0;for(let zq=0;zq<zdd.length;zq+=4e3)if(Math.max(zdd[zq],zdd[zq+1],zdd[zq+2])-Math.min(zdd[zq],zdd[zq+1],zdd[zq+2])>8){zbunt=1;break}if(zbunt){for(let zq=0;zq<zdd.length;zq+=4){const zg=(zdd[zq]*.2126+zdd[zq+1]*.7152+zdd[zq+2]*.0722)|0;zdd[zq]=zg,zdd[zq+1]=zg,zdd[zq+2]=zg}zx.putImageData(zid,0,0)}}catch(zz){}const zbl=await new Promise(zr=>{try{zc.toBlob(zr,"image/jpeg",.92)}catch(zz){zr(null)}});zbl&&zbl.size>2e3&&(zOrd.file("Story-"+String(zi+1).padStart(3,"0")+".jpg",zbl),zOk+=1)}catch(zfe){console.warn("Story-Export: ein Foto ging nicht",zfe)}}',
 'Export schneidet und entsaettigt selbst', 1))

# 184  Ein Viertel schwarzweiss, Balken statt Schnitt
#
#      Ihr Bild aus dem Export: das obere linke VIERTEL war
#      schwarzweiss, der Rest farbig. Dazu schwarze Balken oben und
#      unten statt eines Zoom-Schnitts.
#
#      ZWEI URSACHEN, beide meine.
#
#      1. RETINA. fabric legt den Canvas mit devicePixelRatio an, auf
#         ihrem iPhone also 2160x3840. Meine Umrechnung las und schrieb
#         getImageData(0,0,1080,1920) — genau ein Viertel, oben links.
#         Deshalb war nur dieses Viertel grau. Im Testrechner mit
#         Pixelverhaeltnis 1 war es nie zu sehen.
#
#      2. BALKEN. Ich habe den Feed-Zeichner Ca mit format:"9:16"
#         benutzt. Der legt bei 9:16 das Bild HINEIN statt es zu
#         fuellen, Rest schwarz. "Auf Zoom geschnitten" war es damit
#         nie.
#
#      REPARATUR: der Export benutzt Ca gar nicht mehr. Er laedt das
#      Bild selbst, legt einen Canvas mit genau 1080x1920 an (kein
#      Retina, weil selbst erzeugt), rechnet den Fuellfaktor
#      Math.max(1080/w, 1920/h), zeichnet mittig — das ist der
#      Zoom-Schnitt — und entsaettigt zweifach abgesichert:
#      ctx.filter="grayscale(1)" beim Zeichnen, danach eine Stichprobe
#      ueber die Pixel und, falls doch Farbe drin ist, die
#      Luminanzschleife ueber die ganze Flaeche.
#
#      FOLGE: der Feed-Look (Schleier, Vignette, Korn) ist im Export
#      nicht mehr drin. Es ist das reine Foto, schwarzweiss, gefuellt.
#
#      GEPRUEFT: drei Fotos, jede Datei 1080x1920, Farbigkeit in ALLEN
#      VIER VIERTELN 0.0, schwarze Balken oben 0 Prozent, unten 0
#      Prozent.

# 185 — Der Export sagt vorher, wie viele es sein sollten
P.append((
 'const[zSLauft,zSSetzLauft]=ce.useState(!1),[zSStand,zSSetzStand]=ce.useState("");',
 'const[zSLauft,zSSetzLauft]=ce.useState(!1),[zSStand,zSSetzStand]=ce.useState("");const zFotos=(()=>{try{const zL=(Array.isArray(e.brandImages)?e.brandImages:[]).map(zx=>typeof zx=="string"?zx:(zx&&(zx.src||zx.url||zx.dataUrl))||"").filter(zx=>zx&&zx.length>5);const zP=[];(Array.isArray(e.contentPlan)?e.contentPlan:[]).forEach(zt=>(Array.isArray(zt.slides)?zt.slides:[]).forEach(zs2=>{const zb=zs2&&zs2.background;if(typeof zb=="string"&&zb.length>5)zP.push(zb)}));const zW=(typeof window<"u"&&Array.isArray(window.__bsBilder))?window.__bsBilder.filter(zx=>typeof zx=="string"&&zx.length>5):[];const zU=[...new Set([...zL,...zP,...zW])];return{lib:new Set(zL).size,plan:new Set(zP).size,liste:zU}}catch(zz){return{lib:0,plan:0,liste:[]}}})();',
 'Fotos aus Bibliothek und Plan getrennt zaehlen', 1))

P.append((
 'const zRoh=(typeof window<"u"&&window.__bsBilder)||[];const zListe=[...new Set(zRoh.filter(zx=>typeof zx=="string"&&zx.length>5))];',
 'const zListe=zFotos.liste;',
 'Export nimmt die gezaehlte Liste', 1))

P.append((
 'children:zSStand||"Jedes Foto aus deiner Bibliothek: 1080\\u00d71920, Zoom-Schnitt, Bildlook wie im Feed \\u2014 als ein ZIP zum Ablegen in einen Ordner."',
 'children:zSStand||(zFotos.liste.length+" verschiedene Fotos \\u2014 "+zFotos.lib+" in der Bibliothek, "+zFotos.plan+" im Plan verwendet. 1080\\u00d71920, Zoom-Schnitt, schwarzwei\\u00df, als ein ZIP.")',
 'Aufschluesselung statt Werbetext', 1))

# 185  Wie viele sollten kommen?
#
#      Nach dem ersten Lauf kamen 59 Bilder heraus und die Frage:
#      "Aber wieviele sollten kommen?" Darauf konnte ich nur raten,
#      weil ihre Bibliothek in ihrem Browser liegt.
#
#      Jetzt rechnet die App es aus und schreibt es hin, BEVOR man
#      drueckt:
#
#          "59 verschiedene Fotos — 43 in der Bibliothek,
#           31 im Plan verwendet."
#
#      Gezaehlt wird aus zwei Quellen, getrennt und dann vereinigt:
#          brandImages   die Bibliothek (Zeichenketten oder Objekte
#                        mit src/url/dataUrl)
#          contentPlan   jedes background aus jeder Slide
#          window.__bsBilder als drittes Netz, falls etwas nur dort
#                        haengt
#      Doppelte Adressen zaehlen einmal — deshalb ist die Summe der
#      beiden Zahlen groesser als die Gesamtzahl, wenn ein Foto in der
#      Bibliothek liegt UND im Plan verwendet wird.
#
#      Der Export nimmt genau diese Liste. Damit ist die Zahl davor und
#      die Zahl danach dieselbe, und eine Abweichung heisst wirklich:
#      dieses Foto liess sich nicht laden.
#
#      GEPRUEFT: Testplan mit drei Fotos und leerer Bibliothek zeigt
#      "3 verschiedene Fotos — 0 in der Bibliothek, 3 im Plan
#      verwendet", ZIP enthaelt drei Dateien, alle Viertel 0.0.

# 186 — Nicht die Rohfotos, sondern die fertigen Kacheln in 9:16
P.append((
 'const zFotos=(()=>{try{const zL=(Array.isArray(e.brandImages)?e.brandImages:[]).map(zx=>typeof zx=="string"?zx:(zx&&(zx.src||zx.url||zx.dataUrl))||"").filter(zx=>zx&&zx.length>5);const zP=[];(Array.isArray(e.contentPlan)?e.contentPlan:[]).forEach(zt=>(Array.isArray(zt.slides)?zt.slides:[]).forEach(zs2=>{const zb=zs2&&zs2.background;if(typeof zb=="string"&&zb.length>5)zP.push(zb)}));const zW=(typeof window<"u"&&Array.isArray(window.__bsBilder))?window.__bsBilder.filter(zx=>typeof zx=="string"&&zx.length>5):[];const zU=[...new Set([...zL,...zP,...zW])];return{lib:new Set(zL).size,plan:new Set(zP).size,liste:zU}}catch(zz){return{lib:0,plan:0,liste:[]}}})();const zStoryExport=async()=>{if(zSLauft)return;zSSetzLauft(!0),zSSetzStand("Fotos werden gesammelt \\u2026");try{const zListe=zFotos.liste;if(!zListe.length){zSSetzStand("Keine Fotos in der Bibliothek gefunden."),zSSetzLauft(!1);return}const zZip=new Dl,zOrd=zZip.folder("Stories_9_16");let zOk=0;const zLad=zu=>new Promise(zr=>{const za=new Image;za.crossOrigin="anonymous";za.onload=()=>zr(za);za.onerror=()=>{const zb2=new Image;zb2.onload=()=>zr(zb2);zb2.onerror=()=>zr(null);zb2.src=zu};za.src=zu});for(let zi=0;zi<zListe.length;zi+=1){zSSetzStand("Schneide "+(zi+1)+" von "+zListe.length+" \\u2026");try{const zim=await zLad(zListe[zi]);if(!zim||!zim.width||!zim.height)continue;const zc=document.createElement("canvas");zc.width=1080,zc.height=1920;const zx=zc.getContext("2d");zx.fillStyle="#000",zx.fillRect(0,0,1080,1920);try{zx.filter="grayscale(1)"}catch(zz){}const zf=Math.max(1080/zim.width,1920/zim.height),zw=zim.width*zf,zh=zim.height*zf;zx.drawImage(zim,(1080-zw)/2,(1920-zh)/2,zw,zh);try{zx.filter="none"}catch(zz){}try{const zid=zx.getImageData(0,0,1080,1920),zdd=zid.data;let zbunt=0;for(let zq=0;zq<zdd.length;zq+=4e3)if(Math.max(zdd[zq],zdd[zq+1],zdd[zq+2])-Math.min(zdd[zq],zdd[zq+1],zdd[zq+2])>8){zbunt=1;break}if(zbunt){for(let zq=0;zq<zdd.length;zq+=4){const zg=(zdd[zq]*.2126+zdd[zq+1]*.7152+zdd[zq+2]*.0722)|0;zdd[zq]=zg,zdd[zq+1]=zg,zdd[zq+2]=zg}zx.putImageData(zid,0,0)}}catch(zz){}const zbl=await new Promise(zr=>{try{zc.toBlob(zr,"image/jpeg",.92)}catch(zz){zr(null)}});zbl&&zbl.size>2e3&&(zOrd.file("Story-"+String(zi+1).padStart(3,"0")+".jpg",zbl),zOk+=1)}catch(zfe){console.warn("Story-Export: ein Foto ging nicht",zfe)}}if(!zOk){zSSetzStand("Kein Foto liess sich zeichnen."),zSSetzLauft(!1);return}zSSetzStand("ZIP wird gepackt \\u2026");const zBlob=await zZip.generateAsync({type:"blob"});ls.saveAs(zBlob,"BrandStudio-Stories-9-16.zip");zSSetzStand(zOk+" von "+zListe.length+" Fotos als ZIP geladen.")}catch(zz){zSSetzStand("Fehlgeschlagen: "+String(zz&&zz.message?zz.message:zz).slice(0,90))}zSSetzLauft(!1)};',
 'const zFotos=(()=>{try{const zA=[];(Array.isArray(e.contentPlan)?e.contentPlan:[]).forEach(zt=>(Array.isArray(zt.slides)?zt.slides:[]).forEach((zs2,zk2)=>{const zb=zs2&&zs2.background;if(typeof zb=="string"&&zb.length>5)zA.push({tag:zt.day,nr:zk2+1,slide:zs2})}));return zA}catch(zz){return[]}})();const zSchnitt=zu=>new Promise(zr=>{try{const za=new Image;za.crossOrigin="anonymous";const zfertig=zi2=>{try{if(!zi2||!zi2.width)return zr(zu);const zc2=document.createElement("canvas");zc2.width=1080,zc2.height=1920;const zx2=zc2.getContext("2d");const zf2=Math.max(1080/zi2.width,1920/zi2.height),zw2=zi2.width*zf2,zh2=zi2.height*zf2;zx2.drawImage(zi2,(1080-zw2)/2,(1920-zh2)/2,zw2,zh2);zr(zc2.toDataURL("image/jpeg",.95))}catch(zz){zr(zu)}};za.onload=()=>zfertig(za);za.onerror=()=>{const zb2=new Image;zb2.onload=()=>zfertig(zb2);zb2.onerror=()=>zr(zu);zb2.src=zu};za.src=zu}catch(zz){zr(zu)}});const zStoryExport=async(zMitText)=>{if(zSLauft)return;zSSetzLauft(!0),zSSetzStand("Wird gezeichnet \\u2026");try{if(!zFotos.length){zSSetzStand("Keine Kachel mit Foto gefunden."),zSSetzLauft(!1);return}const zZip=new Dl,zOrd=zZip.folder(zMitText?"Stories_9_16_mit_Text":"Stories_9_16_ohne_Text");let zOk=0;for(let zi=0;zi<zFotos.length;zi+=1){const zE=zFotos[zi];zSSetzStand("Zeichne "+(zi+1)+" von "+zFotos.length+" \\u2026");const zc=document.createElement("canvas");zc.width=1080,zc.height=1920,zc.style.display="none";document.body.appendChild(zc);const zk=new Pe.fabric.StaticCanvas(zc,{width:1080,height:1920,enableRetinaScaling:!1});try{const zBg=await zSchnitt(zE.slide.background);const zD={...zE.slide,background:zBg,format:"9:16",visualElements:zE.slide.visualElements||[],_tag:zE.tag};if(!zMitText){zD.text="",zD.secondaryText="",zD.footerText="",zD.label="",zD.cta="",zD.statement=""}await Ca(zk,zD,1080,1920,{slideIndex:zE.nr-1,totalSlides:1,scale:1080/400,globalBrandName:zMitText?(((e.currentBrandConfig||{}).brandText)||""):"",typography:(e.currentBrandConfig||{}).typography});const zd=zk.toDataURL({format:"jpeg",quality:.92,multiplier:1});if(zd&&zd.length>2e3){const zbl=await(await fetch(zd)).blob();zbl&&zbl.size>2e3&&(zOrd.file("Tag"+String(zE.tag).padStart(3,"0")+"_Slide"+zE.nr+".jpg",zbl),zOk+=1)}}catch(zfe){console.warn("Story-Export: eine Kachel ging nicht",zfe)}finally{try{zk.dispose()}catch(zz){}zc.parentNode&&zc.parentNode.removeChild(zc)}}if(!zOk){zSSetzStand("Keine Kachel liess sich zeichnen."),zSSetzLauft(!1);return}zSSetzStand("ZIP wird gepackt \\u2026");const zBlob=await zZip.generateAsync({type:"blob"});ls.saveAs(zBlob,zMitText?"Stories-9-16-mit-Text.zip":"Stories-9-16-ohne-Text.zip");zSSetzStand(zOk+" von "+zFotos.length+" Kacheln als ZIP geladen.")}catch(zz){zSSetzStand("Fehlgeschlagen: "+String(zz&&zz.message?zz.message:zz).slice(0,90))}zSSetzLauft(!1)};',
 'Export durch den echten Zeichner, 9:16', 1))

P.append((
 'v.jsx("div",{className:"text-[11px] text-gray-500 mt-0.5",children:zSStand||(zFotos.liste.length+" verschiedene Fotos \\u2014 "+zFotos.lib+" in der Bibliothek, "+zFotos.plan+" im Plan verwendet. 1080\\u00d71920, Zoom-Schnitt, schwarzwei\\u00df, als ein ZIP.")})]}),v.jsx("button",{onClick:zStoryExport,disabled:zSLauft,className:"px-4 py-2.5 rounded-lg bg-gray-900 text-white text-xs font-bold disabled:opacity-40 whitespace-nowrap",children:zSLauft?"L\\u00e4uft \\u2026":"Als ZIP laden"})]}),',
 'v.jsx("div",{className:"text-[11px] text-gray-500 mt-0.5",children:zSStand||(zFotos.length+" Kacheln mit Foto \\u2014 dieselben Bilder wie im Feed, gezeichnet auf 1080\\u00d71920 statt 4:5.")})]}),v.jsxs("div",{className:"flex gap-2",children:[v.jsx("button",{onClick:()=>zStoryExport(!0),disabled:zSLauft,className:"px-4 py-2.5 rounded-lg bg-gray-900 text-white text-xs font-bold disabled:opacity-40 whitespace-nowrap",children:zSLauft?"L\\u00e4uft \\u2026":"Mit Text"}),v.jsx("button",{onClick:()=>zStoryExport(!1),disabled:zSLauft,className:"px-4 py-2.5 rounded-lg border border-gray-300 bg-white text-gray-800 text-xs font-bold disabled:opacity-40 whitespace-nowrap",children:"Nur Foto"})]})]}),',
 'Zwei Knoepfe: mit Text und nur Foto', 1))

# 186  Es sind die fertigen Kacheln, nicht die Rohfotos
#
#      "Jedes Mal, wenn du meinen Feed kreierst, entscheidest DU
#      schwarzweiss, entscheidest DU, wie viel. Du erstellst da
#      literally neue Bilder. Und genau diese Bilder will ich nur eben
#      im anderen Format."
#
#      Damit war 184 der falsche Weg: dort habe ich den Zeichner
#      umgangen und die Rohfotos selbst beschnitten und entsaettigt.
#      Herausgekommen waeren Fotos — sie will die KACHELN.
#
#      Jetzt laeuft der Export wieder durch Ca, den echten Zeichner,
#      nur eben auf 1080x1920. Alles, was der Zeichner entscheidet
#      (Schwarzweiss, Schleier, Vignette, Korn, Schrift, Lage), kommt
#      damit automatisch mit — es ist dieselbe Kachel im anderen
#      Format.
#
#      DREI DINGE MUSSTEN DAFUER STIMMEN:
#
#      1. KEINE BALKEN. Ca legt bei format:"9:16" das Foto hinein
#         statt es zu fuellen. Deshalb wird das Foto VORHER auf
#         1080x1920 fuellend geschnitten (Math.max-Faktor, mittig) und
#         das Ergebnis als background uebergeben. Fuer Ca ist es dann
#         schon 9:16, also kein Rand.
#      2. KEIN RETINA-VIERTEL. Der Export-Canvas wird mit
#         enableRetinaScaling:!1 angelegt. Damit ist der Canvas genau
#         1080x1920 und nicht 2160x3840.
#      3. NICHTS SELBST ENTSAETTIGEN. Die Farbentscheidung gehoert dem
#         Zeichner. Meine Luminanzschleife ist raus.
#
#      ZWEI KNOEPFE, weil "die Bilder" beides heissen kann:
#          Mit Text  — die Kachel wie im Feed, samt Schrift und Name
#          Nur Foto  — dieselbe Kachel, aber text/secondaryText/
#                      footerText/label/cta/statement geleert
#      Dateinamen: Tag007_Slide1.jpg, damit die Zuordnung bleibt.
#
#      GEPRUEFT: Testplan mit drei Fotokacheln. "Mit Text" ergibt
#      1080x1920 mit der Schrift unten, "Nur Foto" dieselbe Kachel ohne
#      Schrift, in beiden Faellen schwarze Balken oben 0 Prozent, unten
#      0 Prozent. Die Farbigkeit bleibt die des Zeichners — im
#      Testrechner farbig, weil dort weder BS_MISCHBAR noch ihre
#      Kachelwerte greifen.

# 187 — Helle und dunkle Fotos abwechseln, statt sie zu haeufen
P.append((
 'ed=async(e,t=[],r=0)=>{const n=await AK(t);if(n.length===0)return e;',
 'ed=async(e,t=[],r=0)=>{const zMisch=zn=>{try{if(!Array.isArray(zn)||zn.length<4)return zn;const zhell=zx=>{try{const zb=zx&&zx.zoneBrightness;if(Array.isArray(zb)&&zb.length){let zsu=0,zza=0;for(let zi=0;zi<zb.length;zi+=1){const zv=Number(zb[zi]);isFinite(zv)&&(zsu+=zv,zza+=1)}return zza?zsu/zza:128}if(zb&&typeof zb=="object"){const zw=Object.values(zb).map(Number).filter(zv=>isFinite(zv));if(zw.length)return zw.reduce((za,zb2)=>za+zb2,0)/zw.length}return 128}catch(zz){return 128}};const zs=[...zn].sort((za,zb2)=>(zhell(za)-zhell(zb2))||String((za||{}).src||"").localeCompare(String((zb2||{}).src||"")));const zm=Math.ceil(zs.length/2),zd=zs.slice(0,zm),zl=zs.slice(zm),zo=[];for(let zi=0;zi<zm;zi+=1){zd[zi]&&zo.push(zd[zi]),zl[zi]&&zo.push(zl[zi])}return zo.length===zn.length?zo:zn}catch(zz){return zn}};const n=zMisch(await AK(t));if(n.length===0)return e;',
 'Helle und dunkle Fotos abwechseln', 1))

# 187  Tag 1 bis 20 nicht nur schwarze Blazer
#
#      "Kannst du ueber die Fotos schauen, dass bei Tag 1 bis 20 nicht
#      nur Fotos mit schwarzen Blazern sind? Das macht den Feed
#      einheitlich, und dann kommen weiter oben erst die mit den blauen
#      Bildern."
#
#      URSACHE: die Zuordnung ist rein sequentiell. In ed() steht
#
#          l = Array.from({length: s}, (u,d) => n[(r+d) % i])
#
#      also nimmt Tag r das Bild mit Index r. Die Reihenfolge des Pools
#      IST die Reihenfolge des Feeds. Wer die Blazerbilder zusammen
#      hochlaedt, bekommt zwanzig Blazertage am Stueck.
#
#      Der Zeichner misst die Helligkeit jedes Fotos ohnehin schon
#      (zoneBrightness aus AK). Diese Zahl wird jetzt benutzt:
#
#          nach mittlerer Helligkeit sortieren
#          in zwei Haelften teilen — dunkel und hell
#          abwechselnd austeilen: dunkel, hell, dunkel, hell ...
#
#      Bei Gleichstand entscheidet die Bildadresse, damit die
#      Reihenfolge bei jedem Aufruf dieselbe ist — ed() wird pro Tag
#      erneut aufgerufen, eine zufaellige Mischung wuerde Tage
#      kollidieren lassen.
#
#      Da der dunkle Feed schwarzweiss ist, ist "dunkel gegen hell"
#      genau der Unterschied, den sie sieht: Blazer gegen Jeans.
#
#      GEPRUEFT isoliert mit 20 dunklen und 20 hellen Bildern:
#          vorher  Tag 1-20: DDDDDDDDDDDDDDDDDDDD
#          nachher Tag 1-20: DHDHDHDHDHDHDHDHDHDH
#          alle 40 Bilder noch da, zweiter Lauf identisch
#
#      GREIFT ERST BEIM NEU ZUORDNEN: der bestehende Plan bleibt, wie
#      er ist. Erst "Neu laden" (Bilder neu zuordnen) oder ein neuer
#      Import verteilt nach der neuen Ordnung. Gesperrte Tage bleiben
#      unberuehrt.

# 188 — Kacheln beim Rausscrollen wieder freigeben
P.append((
 'uG=({data:e,brandName:t,rootMargin:r="600px"})=>{const n=ce.useRef(null),[i,s]=ce.useState(!1);return ce.useEffect(()=>{if(i)return;const l=n.current;if(!l)return;if(typeof IntersectionObserver>"u"){s(!0);return}const o=new IntersectionObserver(a=>{a.some(u=>u.isIntersecting)&&(s(!0),o.disconnect())},{rootMargin:r});return o.observe(l),()=>o.disconnect()},[i,r]),',
 'uG=({data:e,brandName:t,rootMargin:r="600px"})=>{const n=ce.useRef(null),[i,s]=ce.useState(!1);return ce.useEffect(()=>{const l=n.current;if(!l)return;if(typeof IntersectionObserver>"u"){s(!0);return}let zVerz=null;const o=new IntersectionObserver(a=>{const zSicht=a.some(u=>u.isIntersecting);if(zSicht){zVerz&&(clearTimeout(zVerz),zVerz=null),s(zv=>zv||!0)}else{zVerz&&clearTimeout(zVerz),zVerz=setTimeout(()=>{zVerz=null,s(zv=>zv?!1:zv)},1200)}},{rootMargin:r});return o.observe(l),()=>{zVerz&&clearTimeout(zVerz),o.disconnect()}},[r]),',
 'Kacheln beim Rausscrollen wieder freigeben', 1))

# 188  Die weisse Seite bei 112 Tagen
#
#      "Wenn ich von Tag 112 nach Tag 1 scrolle, kommt bei Tag 20 ein
#      white screen."
#
#      Das ist die Ursache aus 169, die seit dem Ausbau des Blaetterns
#      (170) wieder offen war. Die faule Gitterkachel uG hat ihren
#      Beobachter beim ersten Sichtkontakt getrennt:
#
#          if (i) return;                       // schon sichtbar gewesen
#          ... a.some(isIntersecting) && (s(!0), o.disconnect())
#
#      Was einmal gesehen wurde, blieb gezeichnet. Wer durchscrollt,
#      haelt am Ende ALLE Kacheln gleichzeitig im Speicher.
#
#      Jetzt der zweite Weg, den 170 schon aufgeschrieben hatte: der
#      Beobachter bleibt dran. Kommt eine Kachel in Sicht, wird sie
#      gezeichnet; verlaesst sie den Bereich, wird sie nach 1200 ms
#      wieder freigegeben. Die Verzoegerung verhindert Flattern beim
#      schnellen Vorbeiscrollen und beim kurzen Zurueckwischen.
#
#      Der rootMargin von 600px bleibt: rund drei Bildschirme bleiben
#      geladen, damit beim normalen Scrollen nichts grau aufblitzt.
#
#      GEPRUEFT mit 112 Tagen, Fenster 420x850, einmal komplett
#      durchgescrollt:
#          karten246  112 gezeichnete Kacheln, 0 Platzhalter
#          karten247   25 gezeichnete Kacheln, 87 Platzhalter
#      Die sichtbaren Kacheln sind gezeichnet, keine grauen Loecher.
#
#      PREIS: beim Zurueckscrollen wird neu gezeichnet. Das kann kurz
#      grau aufblitzen. Dafuer gibt es keine Obergrenze mehr, ab der
#      die Seite stirbt.

# 189  "carinaannaprav sollte noch auf den Posts stehen"
#
#      Der Name stand nur noch auf den Textkacheln. Auf den Fotokacheln
#      war er weg, und zwar durch einen Schalter, den der dunkle Feed
#      selbst gesetzt hat:
#
#          (tt.platten || BS_KACHEL.nameZeigen === 0) || e.add(Name)
#
#      BS_DUNKEL trug nameZeigen:0 - also nie. Der Schalter geht wieder
#      an.
#
#      Dazu die Angleichung: auf den Textkacheln zeichnet der
#      Kartenzeichner den Namen in PoppinsBold, Laufweite 140, auf
#      Hoehe .905, in rgba(246,241,230,0.55). Auf den Fotokacheln stand
#      Playfair in .030 auf Hoehe .945 - eine zweite Handschrift fuer
#      denselben Namen. Jetzt beide gleich.
#
#      Die Groesse .0104 waere rechnerisch dasselbe wie c(14), sieht im
#      Gitter aber halb so gross aus (die Kartenkacheln zeichnen auf
#      einer anderen Flaeche). Gemessen und auf .026 gesetzt: der Name
#      ist auf Foto- und Textkachel gleich breit.
#
#      GEPRUEFT mit einer Foto- und einer Textkachel nebeneinander:
#          karten247  Foto: kein Name       Text: carinaannaprav
#          karten248  Foto: carinaannaprav  Text: carinaannaprav
#      Der echte 100-Tage-Plan zeichnet unveraendert (dieselben
#      Kartenkacheln wie in 247, byte-gleicher Schnappschuss).

P.append((
 'nameZeigen:0',
 'nameZeigen:1',
 'Name auf den Fotokacheln wieder einschalten', 1))

P.append((
 'nameSchrift:"Playfair Display",nameGewicht:"400",nameLaufweite:60,nameAnteil:.030',
 'nameSchrift:"PoppinsBold",nameGewicht:"700",nameLaufweite:140,nameAnteil:.026,nameUnten:.905',
 'Foto-Name genauso setzen wie auf den Textkacheln', 1))

P.append((
 'nameFarbe:"#F2EFE9"',
 'nameFarbe:"rgba(246,241,230,0.55)",nameDeckkraft:1',
 'Gleiche Deckkraft wie der Name auf den Textkacheln', 1))


# 190  Der Screenshot allein erklaert nichts
#
#      "Der Screenshot alleine hilft nicht, mach eine erklaerende
#      Hook-Zeile dazu und mach ihn passend zum 3:4 Format. Am
#      Textkachel sehe ich keinen Namen."
#
#      DREI SACHEN.
#
#      (1) HOOK-ZEILE. Beim Platzieren hat Pt() den Text der Folie
#      geleert (text:"") und nur das Bild gesetzt. Uebrig blieb ein
#      Screenshot ohne ein Wort dazu.
#
#      Der Text steht aber schon im Plan: der Platzhalter ist fast
#      immer Folie 0, und Folie 1 desselben Tages erklaert ihn.
#
#          Tag 2  Folie 0  [Screenshot S-R52ZN]
#                 Folie 1  Das ist die Reaktion einer Kundin auf
#                          einen klaren Impuls.
#
#      Genau die Zeile wird jetzt als overlayHook mitgenommen: erst die
#      naechste Folie ohne Platzhalter, sonst die vorige, sonst der
#      Tagestitel ohne sein "BEWEIS - " davor. Auf 120 Zeichen gekuerzt,
#      an der Wortgrenze. Eine schon gesetzte Hook-Zeile bleibt stehen.
#
#      (2) INS FORMAT. Der Screenshot wurde auf 80% der Breite skaliert
#      und mittig gesetzt - in seiner eigenen Hoehe. Ein hochkantes
#      Handybild ragte damit oben und unten aus der Kachel heraus und
#      hat sie komplett zugedeckt.
#
#      Jetzt bekommt er eine Box: unter der Hook-Zeile bis .865 (ueber
#      dem Namen), quer bis .09 Rand. Skaliert wird mit Math.min von
#      Breite und Hoehe - er passt ganz hinein, nichts wird
#      abgeschnitten, nichts ragt heraus. Der vorhandene Groessen-
#      regler wirkt weiter, .8 ist jetzt "voll".
#
#      Die Hook-Zeile braucht eine Farbe, die auf dem Kachelgrund
#      lesbar ist. Der Grundton wird in Ca gemerkt (zGrundTon), weil er
#      in einem Block steht, den Ae() nicht sieht.
#
#      (3) NAME AUF DER TEXTKACHEL. Gemessen, warum er dort fehlt:
#
#          wt f=ablauf  ABS=rgba(246,241,230,0.55)  grund=#2B211A
#          wt f=marke   ABS=#000000                 grund=#FFFFFF
#
#      Der Kartenzeichner hat sich bei fassung "marke" selbst
#      ausgenommen: Je.fassung!=="marke". Die Markenkachel war die
#      einzige ohne Namen. Die Bedingung faellt weg.
#
#      Dazu zwei Kleinigkeiten aus demselben Durchgang: auf
#      Plattenkacheln war der Name ebenfalls unterdrueckt (tt.platten),
#      jetzt steht er dort in der Plattenfarbe. Und wo ein
#      Monogrammring sitzt, rueckt er um c(42) nach rechts, statt im
#      Ring zu liegen.
#
#      GEPRUEFT an vier Kacheln - Platte, dunkler Text, Foto,
#      Screenshot: auf allen vieren steht der Name. Der echte
#      100-Tage-Plan: 52 Screenshots platziert, alle mit Hook-Zeile aus
#      dem eigenen Tag, 100 Kacheln ohne Seitenfehler.


P.append((
 'Ca=async(e,t,r,n,i={})=>{',
 'Ca=async(e,t,r,n,i={})=>{let zGrundTon="";',
 'Merker fuer den Grundton der Kachel', 1))

P.append((
 'lt=!_C(et),wt=(Je,rt)=>{',
 'lt=(zGrundTon=et,!_C(et)),wt=(Je,rt)=>{',
 'Grundton merken, damit der Screenshot-Haken lesbar bleibt', 1))

P.append((
 'if(t.overlayIsScreenshot){const et=r*(typeof t.overlayImageScale=="number"?t.overlayImageScale:.8)/me.width,lt=me.width*et,wt=me.height*et,tt=r/2+(typeof t.overlayImageX=="number"?t.overlayImageX:0)*d,Qt=n/2+(typeof t.overlayImageY=="number"?t.overlayImageY:0)*d,Wt=10*d;e.add(new Pe.fabric.Rect({left:tt,top:Qt,originX:"center",originY:"center",width:lt+Wt*2,height:wt+Wt*2,rx:12*d,ry:12*d,fill:F,selectable:!1,shadow:"rgba(0,0,0,0.22) 0px 10px 30px"})),me.set({originX:"center",originY:"center",left:tt,top:Qt,scaleX:et,scaleY:et,selectable:!1,clipPath:new Pe.fabric.Rect({width:me.width,height:me.height,rx:6/et,ry:6/et,originX:"center",originY:"center"})}),e.add(me),Fe(!0);return}',
 'if(t.overlayIsScreenshot){const zHk=String(t.overlayHook||"").replace(/\\*/g,"").trim(),zBg=String(zGrundTon||t.plateOverride||t.backgroundColor||"#000000"),zTint=w(zBg)>150?"#241C16":"#F6F1E6",zRd=r*.09,Wt=10*d;let zOben=n*.115;if(zHk){const zTb=new Pe.fabric.Textbox(zHk,{left:r/2,top:n*.10,originX:"center",originY:"top",width:r-zRd*2,fontSize:Math.round(r*(BS_KACHEL.hakenAnteil||.055)),fontFamily:BS_KACHEL.deckblattFamilie||"Playfair Display",fontWeight:"400",fill:zTint,textAlign:"center",lineHeight:1.18,selectable:!1,evented:!1});for(let zi=0;zi<4&&zTb.height>n*.30;zi+=1)zTb.set({fontSize:Math.round(zTb.fontSize*.88)});e.add(zTb),zOben=n*.10+zTb.height+n*.045}const zUnten=n*.865,zH=Math.max(n*.24,zUnten-zOben),zF=typeof t.overlayImageScale=="number"?Math.max(.3,Math.min(1,t.overlayImageScale/.8)):1,et=Math.min((r-zRd*2-Wt*2)/me.width,(zH-Wt*2)/me.height)*zF,lt=me.width*et,wt=me.height*et,tt=r/2+(typeof t.overlayImageX=="number"?t.overlayImageX:0)*d,Qt=zOben+zH/2+(typeof t.overlayImageY=="number"?t.overlayImageY:0)*d;e.add(new Pe.fabric.Rect({left:tt,top:Qt,originX:"center",originY:"center",width:lt+Wt*2,height:wt+Wt*2,rx:12*d,ry:12*d,fill:F,selectable:!1,shadow:"rgba(0,0,0,0.22) 0px 10px 30px"})),me.set({originX:"center",originY:"center",left:tt,top:Qt,scaleX:et,scaleY:et,selectable:!1,clipPath:new Pe.fabric.Rect({width:me.width,height:me.height,rx:6/et,ry:6/et,originX:"center",originY:"center"})}),e.add(me),Fe(!0);return}',
 'Screenshot: erklaerende Hook-Zeile und ins Format eingepasst', 1))

P.append((
 '(tt.platten||BS_KACHEL.nameZeigen===0)||e.add(new Pe.fabric.Text(Ze,{left:_e,',
 'BS_KACHEL.nameZeigen===0||e.add(new Pe.fabric.Text(Ze,{left:_e+(Ye&&Ye.istKarte&&Ye.monogrammFarbe?c(42):0),',
 'Name auch auf Plattenkacheln, und nicht mehr im Monogramm', 1))

P.append((
 'fill:BS_KACHEL.nameFarbe||"#FFFFFF",opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1}))',
 'fill:tt.platten?(tt.bandSchriftFarbe||tt.schriftFarbe||"#241C16"):(BS_KACHEL.nameFarbe||"#FFFFFF"),opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1}))',
 'Name auf der Platte in der Plattenfarbe', 1))

P.append((
 'Je.aufFoto!==!0&&Je.fassung!=="marke"&&txt("carinaannaprav",',
 'Je.aufFoto!==!0&&txt("carinaannaprav",',
 'Name auch auf der Markenkachel (das war die Textkachel ohne Namen)', 1))

P.append((
 'const He=(e.contentPlan||[]).map(ot=>({...ot,slides:(ot.slides||[]).map((dt,ut)=>{const st=`${ot.day}_${ut}`;return _e[st]?{...dt,overlayImage:_e[st],overlayIsScreenshot:!0,overlayImageScale:.8,overlayImageRounded:!1,overlayImageX:0,overlayImageY:0,text:"",_wasScreenshot:!0}:dt})}));',
 'const zSauber=zx=>String(zx||"").replace(/\\*/g,"").replace(/\\s+/g," ").trim(),zTauglich=zs=>{if(!zs)return"";const zt=zSauber(zs.text);return!zt||q$(zs.text)?"":zt},zKurz=zt=>zt.length<=120?zt:zt.slice(0,117).replace(/\\s+\\S*$/,"")+"…",zHaken=(ot,ut)=>{try{const zs=ot.slides||[];for(let zi=ut+1;zi<zs.length;zi+=1){const zt=zTauglich(zs[zi]);if(zt)return zKurz(zt)}for(let zi=ut-1;zi>=0;zi-=1){const zt=zTauglich(zs[zi]);if(zt)return zKurz(zt)}const zT=zSauber(ot.title).replace(/^[^–—-]{2,24}[–—-]\\s*/,"");return zT?zKurz(zT):""}catch(zz){return""}};const He=(e.contentPlan||[]).map(ot=>({...ot,slides:(ot.slides||[]).map((dt,ut)=>{const st=`${ot.day}_${ut}`;return _e[st]?{...dt,overlayImage:_e[st],overlayIsScreenshot:!0,overlayImageScale:.8,overlayImageRounded:!1,overlayImageX:0,overlayImageY:0,overlayHook:zSauber(dt.overlayHook)||zHaken(ot,ut),text:"",_wasScreenshot:!0}:dt})}));',
 'Beim Platzieren die Hook-Zeile aus dem Tag mitnehmen', 1))

# 191  Der Haken gehoert der Folie, nicht dem Nachbarn
#
#      "Stop, du nimmst den Text auf Slide 2 und schreibst ihn zum
#      Screenshot - nein, es wird dort eigener Text stehen und Slide 2
#      bleibt Slide 2."
#
#      190 hat sich die Hook-Zeile von der naechsten Folie geliehen.
#      Das war falsch: die Zeile stand dann zweimal im Karussell, und
#      Folie 2 hat ihren eigenen Zweck verloren.
#
#      Jetzt kommt der Haken NUR aus dem Text der Screenshot-Folie
#      selbst. Der Bulk-Import sammelt ohnehin alle Zeilen unter einer
#      "Slide N:"-Ueberschrift zu einer Folie - Haken und Kennung
#      duerfen also einfach untereinander stehen:
#
#          Slide 1: Das ist die Reaktion einer Kundin auf einen
#                   klaren Impuls.
#          [Screenshot S-R52ZN]
#
#      zEigen() nimmt den Folientext, wirft je Zeile die Klammer, die
#      Kennung und ein fuehrendes "Screenshot" weg und behaelt, was an
#      echten Woertern uebrig bleibt. Ist der Rest selbst wieder ein
#      Platzhalter (q$ erkennt ihn, z.B. "Beweis-Screenshot aus deiner
#      Sammlung"), gilt er nicht als Haken.
#
#      Steht auf der Folie nur die Kennung, bleibt der Screenshot ohne
#      Zeile. Nichts wird geborgt.
#
#      zTauglich und zHaken aus 190 fallen weg.
#
#      GEPRUEFT mit zwei Tagen:
#          Tag 1  Haken + Kennung auf einer Folie -> Haken steht da
#          Tag 2  nur Kennung, Erklaerung auf Folie 2 -> kein Haken,
#                 Folie 2 unveraendert
#      4 Folien vorher, 4 Folien nachher. Am echten Plan: 52
#      Screenshots platziert, keine geborgten Zeilen mehr.

P.append((
 'const zSauber=zx=>String(zx||"").replace(/\\*/g,"").replace(/\\s+/g," ").trim(),zTauglich=zs=>{if(!zs)return"";const zt=zSauber(zs.text);return!zt||q$(zs.text)?"":zt},zKurz=zt=>zt.length<=120?zt:zt.slice(0,117).replace(/\\s+\\S*$/,"")+"…",zHaken=(ot,ut)=>{try{const zs=ot.slides||[];for(let zi=ut+1;zi<zs.length;zi+=1){const zt=zTauglich(zs[zi]);if(zt)return zKurz(zt)}for(let zi=ut-1;zi>=0;zi-=1){const zt=zTauglich(zs[zi]);if(zt)return zKurz(zt)}const zT=zSauber(ot.title).replace(/^[^–—-]{2,24}[–—-]\\s*/,"");return zT?zKurz(zT):""}catch(zz){return""}};',
 'const zSauber=zx=>String(zx||"").replace(/\\*/g,"").replace(/\\s+/g," ").trim(),zKurz=zt=>zt.length<=120?zt:zt.slice(0,117).replace(/\\s+\\S*$/,"")+"…",zEigen=zt=>{try{const zr=String(zt||"").split(/\\r?\\n/).map(zz=>{let zc=String(zz).replace(/\\[[^\\]]*\\]/g," ").replace(/\\bS-[0-9A-Z]{5}\\b/ig," ");zc=zc.replace(/^\\s*screenshot\\s*[:\\u2013\\u2014-]?\\s*/i," ");return zSauber(zc)}).filter(zz=>/[a-zA-ZÀ-ÿ]{2}/.test(zz)),zt2=zSauber(zr.join(" "));return zt2&&!q$(zt2)?zKurz(zt2):""}catch(zz){return""}};',
 'Haken kommt aus dem eigenen Text der Folie, nicht vom Nachbarn', 1))

P.append((
 'overlayHook:zSauber(dt.overlayHook)||zHaken(ot,ut)',
 'overlayHook:zSauber(dt.overlayHook)||zEigen(dt.text)',
 'Kein Text mehr von der naechsten Folie holen', 1))

# 192  "In Fotos speichern" ganz oben, Caption darunter
#
#      Das Kachelmenue hatte die beiden Punkte, die sie taeglich
#      braucht, an Stelle 10 und 11 - unter Layout-Stil, Unschaerfe,
#      Grosse Headline und Tiefen-Overlay. Auf dem Handy heisst das
#      scrollen, jedes Mal.
#
#      Beide Knoepfe wandern direkt unter die Kopfzeile "Tag N",
#      "In Fotos speichern" zuerst. Sonst aendert sich nichts: gleiche
#      Knoepfe, gleiche Klicks, nur an anderer Stelle.
#
#      Neue Reihenfolge:
#          In Fotos speichern
#          Caption
#          Als gepostet sperren
#          Bearbeiten
#          Tauschen mit Tag ...
#          ...
#          Export
#          Post loeschen
#
#      GEPRUEFT im Menue von Tag 2, Fenster 430x900.

P.append((
 'v.jsxs("button",{onClick:()=>{h(null),d(u===ae.day?null:ae.day)},className:"w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50",children:[v.jsx(ke,{icon:cS,className:"text-base text-gray-500"})," Caption"]}),v.jsxs("button",{onClick:()=>{h(null),Zt(ae)},disabled:ot,className:"w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-purple-700 hover:bg-purple-50 border-b border-gray-50 disabled:opacity-50",children:[v.jsx(ke,{icon:H1,className:"text-base"})," In Fotos speichern"]}),',
 '',
 'Caption und "In Fotos speichern" aus der Mitte des Menues nehmen', 1))

P.append((
 'children:"✕"})})]}),',
 'children:"✕"})})]}),v.jsxs("button",{onClick:()=>{h(null),Zt(ae)},disabled:ot,className:"w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-purple-700 hover:bg-purple-50 border-b border-gray-50 disabled:opacity-50",children:[v.jsx(ke,{icon:H1,className:"text-base"})," In Fotos speichern"]}),v.jsxs("button",{onClick:()=>{h(null),d(u===ae.day?null:ae.day)},className:"w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50",children:[v.jsx(ke,{icon:cS,className:"text-base text-gray-500"})," Caption"]}),',
 '… und ganz oben wieder einsetzen, Fotos zuerst', 1))

# 193  Export raus, und der Zoom beim Scrollen
#
#      "Export brauch ich nicht. Und wenn ich nach unten scrolle kommt
#      manchmal dann diese Einstellung wieso" (dazu ein Bild: die Seite
#      etwa vierfach vergroessert, das Logo fuellt den halben Schirm)
#
#      EXPORT faellt aus dem Kachelmenue. "In Fotos speichern" macht
#      dasselbe fuer den Weg, den sie geht.
#
#      DER ZOOM ist keine Einstellung, sondern iOS. Safari zoomt von
#      selbst hinein, sobald ein Eingabefeld den Fokus bekommt und
#      dessen Schrift KLEINER ALS 16px ist - und bleibt danach drin.
#      Die App hat solche Felder reichlich: text-sm ist 14px, text-xs
#      12px. Beim Scrollen landet der Finger unterwegs auf einem, iOS
#      hakt es als Antippen ab, zoomt, und der Rest der Seite ist
#      ploetzlich viermal so gross.
#
#      Gegenmittel in beiden index.html, nicht im Bundle:
#          input,textarea,select{font-size:16px!important}
#          html{touch-action:manipulation}
#
#      Das !important muss sein: die Tailwind-Klasse text-sm ist eine
#      Klasse (0,1,0) und schlaegt den Elementwaehler (0,0,1), und ihr
#      Stylesheet wird spaeter geladen.
#
#      touch-action:manipulation nimmt das Doppeltipp-Zoomen weg -
#      Wischen und Zusammenziehen mit zwei Fingern bleiben, sie kann
#      also weiter absichtlich hineinzoomen.
#
#      GEPRUEFT im Browser: alle Felder rechnen 16px, touchAction steht
#      auf manipulation, das Menue hat keinen Export mehr.

P.append((
 'v.jsxs("button",{onClick:()=>{h(null),St(ae)},disabled:ot,className:"w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50 disabled:opacity-50",children:[v.jsx(ke,{icon:M1,className:"text-base text-gray-500"})," Export"]}),',
 '',
 'Export aus dem Kachelmenue nehmen', 1))

# 194  Die Seite laedt bei Tag 40 neu
#
#      "Jetzt komme ich gar nicht mehr zu Tag 1, es laedt neu bei Tag
#      40." Das ist kein Absturz der App, das ist iOS: Safari wirft den
#      Tab weg, wenn er zu viel Speicher haelt, und laedt ihn neu.
#
#      GEMESSEN, 112 Tage mit Fotos und Screenshots, einmal
#      durchgescrollt, Spitze der gleichzeitig belegten Leinwandflaeche:
#
#          karten247   39,2 Mpx  (~157 MB)   49 Kacheln behalten
#          karten252   39,2 Mpx  (~157 MB)   49 Kacheln behalten
#          karten253    8,1 Mpx  (~ 32 MB)   25 Kacheln behalten
#
#      Wichtig: 247 und 252 sind gleich. Die Aenderungen 249-252 haben
#      das NICHT verursacht - die Decke war schon vorher da, ihr Plan
#      ist nur darueber hinausgewachsen.
#
#      URSACHE: jede Kachel, die in den 600px-Rand scrollt, faengt
#      SOFORT an zu zeichnen. Beim schnellen Scrollen waren das ueber
#      50 gleichzeitig, jede mit einer Leinwand von 800x1000 - allein
#      3,2 MB Bildspeicher pro Stueck, und dazu die Fotos.
#
#      ZWEI SACHEN dagegen:
#
#      (1) Eine Warteschlange (zSchlitz). Es zeichnen hoechstens VIER
#          Gitterkacheln gleichzeitig, der Rest wartet. Der Platz wird
#          im finally freigegeben und zur Sicherheit auch nach 15 s,
#          falls ein Bild nie zurueckmeldet - sonst stuende die
#          Schlange fuer immer.
#
#      (2) setDimensions wandert IN die Warteschlange. Vorher wurde
#          die Leinwand sofort auf 800x1000 vergroessert, auch wenn die
#          Kachel noch gar nicht dran war - die 3,2 MB waren also schon
#          belegt, waehrend sie wartete. Jetzt bleibt sie bei den
#          voreingestellten 300x150, bis sie wirklich zeichnet.
#
#      Der Editor und der Export (asImage:false) gehen NICHT durch die
#      Schlange: dort zaehlt jede Sekunde, und es ist immer nur eine
#      Leinwand offen.
#
#      NEBENBEI besser geworden: weil weniger Kacheln fertig werden,
#      waehrend sie schon aus dem Bild gescrollt sind, greift das
#      Freigeben aus 188 wieder richtig - 25 statt 49 behaltene
#      Kacheln.
#
#      GEPRUEFT ausserdem: Gitter zeichnet unveraendert (Platte, Text,
#      Foto, Screenshot), der Editor oeffnet mit 1600x2000.

P.append((
 'e.renderAll()},XV=ce.forwardRef(',
 'e.renderAll()},zSchlitz=()=>{const W=(window.__bsMalQ=window.__bsMalQ||{n:0,q:[],max:4});return new Promise(ok=>{const start=()=>{W.n+=1;let weg=!1;const frei=()=>{if(weg)return;weg=!0;W.n-=1;const nx=W.q.shift();nx&&nx()};setTimeout(frei,15e3);ok(frei)};W.n<W.max?start():W.q.push(start)})},XV=ce.forwardRef(',
 'Warteschlange fuer das Zeichnen anlegen', 1))

P.append((
 'e.format==="4:5"&&(g=800,m=1e3),p.setDimensions({width:g,height:m});const y=g/400,w=++c.current;const zLauf=f.current.then(async()=>{var b;if(w===c.current&&a.current===p)return Ca(p,e,g,m,{slideIndex:e.slideNumber?e.slideNumber-1:0,totalSlides:e.totalSlides||(e.slideNumber?2:1),scale:y,globalBrandName:typeof e.brandText=="string"&&e.brandText.trim()?e.brandText:n,typography:(b=l==null?void 0:l.currentBrandConfig)==null?void 0:b.typography})});',
 'e.format==="4:5"&&(g=800,m=1e3);const y=g/400,w=++c.current;const zLauf=f.current.then(async()=>{var b;if(w!==c.current||a.current!==p)return;const zFrei=i?await zSchlitz():()=>{};try{if(w!==c.current||a.current!==p)return;p.setDimensions({width:g,height:m});return await Ca(p,e,g,m,{slideIndex:e.slideNumber?e.slideNumber-1:0,totalSlides:e.totalSlides||(e.slideNumber?2:1),scale:y,globalBrandName:typeof e.brandText=="string"&&e.brandText.trim()?e.brandText:n,typography:(b=l==null?void 0:l.currentBrandConfig)==null?void 0:b.typography})}finally{zFrei()}});',
 'Hoechstens vier Gitterkacheln gleichzeitig, und erst dann die Leinwand gross machen', 1))

# 195  Der Storyschreiber sprach von einem anderen Geschaeft
#
#      "Ich find den Storyschreiber richtig gut. Aber ich glaube, er ist
#      grad nicht kohaerent mit meinem Content und dem Kurs."
#
#      Stimmt. In der App lagen FUENF Positionierungen nebeneinander:
#
#        write-stories   carinaannaprav.at, erster vierstelliger Verkauf,
#                        Mentoring + 1:1, Angebotscheck VERBOTEN
#        build-webinar   dieselbe Marke, aber "keine 20k-Monate" —
#                        write-stories erlaubte sie ausdruecklich
#        write-reminder  Kanon v3, "naechster Money-Making Move"
#        write-pins      limitlessselling.at, Vinted als Kernbeweis —
#                        write-stories: "Vinted ist RAUS"
#        storyStrategy   Angebotscheck als CTA, also genau das, was
#                        write-stories verboten hat
#
#      Und in ihrem echten 100-Tage-Plan kommt von alldem fast nichts
#      vor: 1:1 elfmal, Instagram achtmal, Workshop einmal. Kein
#      Limitless, kein Vinted, kein Mentoring, kein "vierstellig".
#
#      Ihre Entscheidung: Marke carinaannaprav, Einladung auf THE
#      STRATEGY (Audio-Kurs ab 15.9.), und der Ton soll aus ihrem
#      eigenen Content kommen.
#
#      IM BUNDLE (hier): der Storyschreiber schickt jetzt echte Saetze
#      aus dem Content-Plan mit. zStimmen() sammelt alle Folientexte,
#      wirft Platzhalter und Screenshot-Zeilen weg, nimmt nur 20-200
#      Zeichen und verteilt 24 Stueck gleichmaessig ueber den ganzen
#      Plan. Der Versatz haengt an der Tagesnummer, damit nicht jeder
#      Tag dieselbe Probe bekommt.
#
#      IN DER FUNKTION (netlify/functions/write-stories.mjs, nicht hier):
#      Demi-Bermejo-Block raus, doppelter MONDAY-Ton raus, veralteter
#      Beweiskatalog raus, Angebotscheck-Verbot raus. Dafuer EIN
#      Angebotsblock ganz oben und die Regel, dass Zahlen, Kundinnen
#      und Privatleben nur aus dem mitgelieferten Material stammen
#      duerfen.
#
#      GEPRUEFT im Browser: der Aufruf traegt 24 Saetze, 1625 Zeichen,
#      kein Platzhalter darunter.

P.append((
 '},OT=({isOpen:e,onClose:t,day:r})=>{',
 '},zStimmen=(zp,zTag)=>{try{const zA=[];(zp||[]).forEach(zd=>((zd&&zd.slides)||[]).forEach(zs=>{const zt=String(typeof zs=="string"?zs:(zs&&zs.text)||"").replace(/\\s+/g," ").trim();if(!zt||zt.length<20||zt.length>200)return;if(zt.indexOf("[")>=0||/\\bS-[0-9A-Z]{5}\\b/.test(zt)||/screenshot/i.test(zt))return;zA.push(zt)}));if(!zA.length)return[];const zN=Math.min(24,zA.length),zS=Math.max(1,Math.floor(zA.length/zN)),zO=(Number(zTag)||0)%zS,zR=[];for(let zi=0;zi<zN;zi+=1){const zx=zA[(zO+zi*zS)%zA.length];zx&&zR.indexOf(zx)<0&&zR.push(zx)}return zR}catch(zz){return[]}},OT=({isOpen:e,onClose:t,day:r})=>{',
 'Sammler fuer echte Saetze aus dem Content-Plan', 1))

P.append((
 'count:5,monday:n.mondayTon===!0',
 'count:5,monday:n.mondayTon===!0,stimmen:zStimmen(n.contentPlan,r.day)',
 'Sprachbeispiele an den Storyschreiber mitschicken', 1))

# 196  Ab Folie 2 klebte der Text am Fuss
#
#      "Setz bei den Carousels mit Foto den Text mehr in die Mitte als
#      nur unten ab Slide 2."
#
#      Schuld war EINE Zeile. Jede Folienseite (alles ausser dem
#      Deckblatt) wurde am Fuss ausgerichtet:
#
#          De = n*BS_KACHEL.folgeFuss - ae + Et/2        // folgeFuss .86
#
#      Der Block haengt also mit seiner UNTERKANTE auf 86% der Hoehe,
#      egal wie kurz der Text ist. Bei zwei Zeilen sitzt alles ganz
#      unten.
#
#      NICHT ueber die Lagen-Namen geloest, obwohl es naheliegt:
#      BS_DUNKEL traegt lagenReihe:"unten", und der Filter davor wirft
#      jede Mittellage wieder auf "unten" zurueck. Ein folgeLage:"mitte"
#      waere wirkungslos verpufft. Deshalb direkt an die Positionszeile.
#
#      Jetzt: Folienseite MIT Foto wird um folgeMitte (.58) ZENTRIERT,
#      Folienseite OHNE Foto behaelt den Fuss, das Deckblatt bleibt
#      unberuehrt. Die Klammer danach (textUnten .86) greift weiter —
#      ein langer Text rutscht also nicht aus der Kachel.
#
#      GEMESSEN an der senkrechten Mitte des Textblocks:
#
#          Kachel                    254     255
#          Deckblatt mit Foto        .725    .725   unveraendert
#          Folie 2 mit Foto, kurz    .732    .573   in die Mitte
#          Folie 2 ohne Foto         .468    .468   unveraendert
#
#      folgeMitte ist ein eigener Regler: hoeher heisst tiefer.

P.append((
 'const zFF=Number(BS_KACHEL.folgeFuss)||0;zFF>0&&t.folienRolle&&t.folienRolle!=="deckblatt"&&(De=n*zFF-ae+Et/2);',
 'const zFF=Number(BS_KACHEL.folgeFuss)||0;zFF>0&&t.folienRolle&&t.folienRolle!=="deckblatt"&&(De=$e?n*(Number(BS_KACHEL.folgeMitte)||.58)-ae/2+Et/2:n*zFF-ae+Et/2);',
 'Folienseiten mit Foto mittig setzen statt an den Fuss', 1))

P.append((
 'folgeFuss:.86',
 'folgeFuss:.86,folgeMitte:.58',
 'Die Hoehe dafuer als eigener Regler', 1))

# 197  Das Storymenue war tot, wenn keine Marke gewaehlt war
#
#      "Ich brauche ausserdem das Storymenue funktionierend."
#
#      Der Story Planner zeigte nur "Bitte waehle zuerst eine Brand im
#      Dashboard". Posts laeuft ohne gewaehlte Marke, Stories nicht -
#      deshalb faellt es nie auf, man kommt nur nie hinein.
#
#      Der Waechter ist NICHT ueberfluessig: nimmt man ihn weg, stuerzt
#      die Seite ab mit
#          TypeError: Cannot read properties of undefined
#                     (reading 'typography')
#      Gemessen mit einer Probefassung ohne Waechter.
#
#      Also nicht den Waechter entfernen, sondern die Marke besorgen:
#      ein Effekt nimmt die erste aus brandConfigurations, sobald die
#      Daten geladen sind und keine gewaehlt ist - genau das, was das
#      Dashboard tut. Die App liefert curated_carina mit, es ist also
#      immer eine da.
#
#      Der Effekt steht direkt vor dem return, nach allen anderen
#      Hooks. In KX gibt es keinen vorgezogenen Ausstieg auf
#      Komponentenebene, die Hook-Reihenfolge bleibt also stabil.
#
#      GEPRUEFT: der Planer zeichnet jetzt seine ganze Leiste -
#      Mit Text, Nur Foto, Style Shifter, Bulk Text Input, Strategie,
#      + Slide, Edit Sequence, Alle in Fotos, Bild generieren - und die
#      Vorschaukachel in Playfair auf Schwarz.

P.append((
 'zSSetzLauft(!1)};return e.currentBrandConfig?v.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32",children:[',
 'zSSetzLauft(!1)};ce.useEffect(()=>{try{if(!r||e.currentBrandConfig)return;const zL=(e.brandConfigurations||[])[0];zL&&t({currentBrandConfig:zL})}catch(zz){}},[r,e.currentBrandConfig,e.brandConfigurations]);return e.currentBrandConfig?v.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32",children:[',
 'Story Planner waehlt die Marke selbst, wenn keine gewaehlt ist', 1))

# 198  Kaffee statt Schwarzweiss - aber nur dort, wo Schwarzweiss war
#
#      "Statt den schwarz weiss Posts (die 50% rotierenden) Farben
#      lassen aber ein komplettes overlay drueber geben in einem
#      dunklen Coffee braun."
#      Und danach: "Die Rotation sollte aber bleiben. Du solltest nur
#      die anpassen, die schwarz weiss waren."
#
#      ERSTER ANLAUF WAR FALSCH (karten258, zurueckgenommen): dort ist
#      saettigungReihe auf "0" gegangen und der Ueberzug lag auf ALLEN
#      Fotokacheln. Damit war die Rotation weg.
#
#      JETZT bleibt die Reihe "-1|0.1" woertlich stehen. Sie entscheidet
#      weiter, welche Kachel welchen Look bekommt - nur heisst der Slot
#      "-1" nicht mehr schwarzweiss, sondern Farbe mit Kaffee-Ueberzug:
#
#        - der Graustich-Rect (globalCompositeOperation "saturation")
#          zeichnet nicht mehr. Er haengt jetzt an swBleibt===1, das
#          nirgends gesetzt ist - so bleibt der Weg zurueck offen.
#        - der Ueberzug-Rect zeichnet NUR bei zSat<=-.99, also genau
#          auf denselben Kacheln.
#
#      zSat selbst wird NICHT veraendert. Das ist Absicht: der
#      Farbmisch-Block prueft "bildFarbNeutral!==0 && !(zSat<=-.99)"
#      und wuerde sonst auf diesen Kacheln anspringen und ein ZWEITES
#      volles Bild zeichnen - die Speicherlast aus 194. Mit zSat=-1
#      bleibt er aus, so wie bisher.
#
#      tonNeutral wird von "13,13,13" auf Kaffee gesetzt. Dieser Wert
#      greift ohnehin nur bei zSat===-1, also genau auf den betroffenen
#      Kacheln. tonReihe bleibt unangetastet - die andere Haelfte
#      aendert sich nicht.
#
#      Drei Regler: bildUeberzug (.42), ueberzugTon ("62,44,32",
#      #3E2C20), ueberzugModus. Der Modus geht ueber
#      globalCompositeOperation und faellt ohne BS_MISCHBAR auf
#      source-over zurueck.
#
#      GEPRUEFT an sechs Tagen mit demselben Foto: Tag 2, 4 und 6
#      tragen den Kaffee, Tag 1, 3 und 5 sind unveraendert farbig.
#      Keine Kachel mehr schwarzweiss.

P.append((
 'bildTon:"14,13,12"',
 'bildTon:"14,13,12",bildUeberzug:.42,ueberzugTon:"62,44,32",ueberzugModus:"source-over"',
 'Die drei Regler fuer den Ueberzug', 1))

P.append((
 'tonNeutral:"13,13,13"',
 'tonNeutral:"62,44,32"',
 'Der Schleier der frueher schwarzweissen Kacheln wird warm', 1))

P.append((
 'zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));',
 'BS_KACHEL.swBleibt===1&&zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));',
 'Kein Entsaettigen mehr - das Foto bleibt farbig', 1))

P.append((
 'const ur=new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgba(${zTon||"0,0,0"},${Et*zAuf})`,selectable:!1});',
 '(()=>{const zU=Number(BS_KACHEL.bildUeberzug)||0;if(!(zU>0)||!t.background||!(zSat<=-.99))return;const zM=BS_MISCHBAR?(BS_KACHEL.ueberzugModus||"source-over"):"source-over";e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgba(${BS_KACHEL.ueberzugTon||zTon||"0,0,0"},${zU})`,globalCompositeOperation:zM,selectable:!1,evented:!1}))})();const ur=new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgba(${zTon||"0,0,0"},${Et*zAuf})`,selectable:!1});',
 'Kaffee-Ueberzug, nur wo die Reihe bisher schwarzweiss gesagt hat', 1))

# 199  Anthrazit statt Kaffee
#
#      "Ok machs doch Anthrazit statt coffee."
#
#      Zwei Werte, sonst nichts. Der Ueberzug aus 198 bleibt wo er ist -
#      auf denselben Kacheln, mit derselben Deckkraft, in derselben
#      Rotation. Nur die Farbe wechselt von "62,44,32" (#3E2C20) auf
#      "56,62,66" (#383E42, RAL 7016 Anthrazitgrau).
#
#      tonNeutral zieht mit, damit der Schleier derselben Kacheln nicht
#      warm bleibt, waehrend der Ueberzug kuehl ist.
#
#      GEPRUEFT an denselben sechs Tagen: 2, 4 und 6 jetzt kuehl grau
#      statt braun, 1, 3 und 5 unveraendert farbig.

P.append((
 'ueberzugTon:"62,44,32"',
 'ueberzugTon:"56,62,66"',
 'Ueberzug in Anthrazit statt Kaffee (RAL 7016, #383E42)', 1))

P.append((
 'tonNeutral:"62,44,32"',
 'tonNeutral:"56,62,66"',
 'Der Schleier derselben Kacheln zieht mit', 1))

# 200  Doch wieder schwarz statt Anthrazit
#
#      "Und mach lieber wieder schwarz statt Anthrazit oder zumindest
#      duenkler."
#
#      ueberzugTon von "56,62,66" auf "0,0,0". tonNeutral zurueck auf
#      seinen alten Wert "13,13,13" - damit liegt auf diesen Kacheln
#      genau der Schleier, den der Feed vorher hatte.
#
#      Was von 198 bleibt: die Rotation entscheidet weiter, welche
#      Kachel welchen Look bekommt, der frueher schwarzweisse Slot ist
#      jetzt FARBE unter einem schwarzen Ueberzug. Deckkraft weiter
#      bildUeberzug = .42.
#
#      GEPRUEFT an denselben sechs Tagen: 2, 4 und 6 dunkel und
#      neutral, kein Blaustich mehr, 1, 3 und 5 unveraendert farbig.

P.append((
 'ueberzugTon:"56,62,66"',
 'ueberzugTon:"0,0,0"',
 'Ueberzug wieder schwarz statt Anthrazit', 1))

P.append((
 'tonNeutral:"56,62,66"',
 'tonNeutral:"13,13,13"',
 'Und der Schleier zurueck auf den alten neutralen Wert', 1))

# 201  Harte Regel: der Text sitzt mittig
#
#      "Baue eine harte Regel das Text immer mittig ist nicht soweit
#      unten."
#
#      EINE Zeile, hinter der ganzen Lagen-Rechnung. Sie ueberschreibt
#      alles, was vorher entschieden wurde:
#
#          BS_KACHEL.textImmerMitte===1 &&
#            (De = n*(BS_KACHEL.textMitte||.5) - ae/2 + Et/2)
#
#      Damit sind auf einen Schlag ausser Kraft:
#        - lagenReihe "unten" und der Filter, der jede Mittellage
#          zurueckgeworfen hat
#        - textLageUnten .80
#        - folgeLage "unten"
#        - folgeFuss .86, der Fuss ab Folie 2
#        - der Lagenwechsel nach Textpruefsumme
#
#      Die Klammern DANACH bleiben absichtlich stehen: textUnten .86
#      faengt einen zu langen Block, die obere Klammer n*.1+SR haelt
#      ihn unter dem Schild. Ein langer Text rutscht also weiter nicht
#      aus der Kachel.
#
#      GEMESSEN an der senkrechten Mitte des Textblocks:
#
#          Kachel                    262     263
#          Deckblatt mit Foto        .721    .571   <- das war es
#          Folie mit Foto            .574    .574   schon aus 196
#          Folie ohne Foto, kurz     .467    .467   unveraendert
#          Folie ohne Foto, lang     .468    .468   unveraendert
#
#      Die beiden Textkacheln sind unveraendert, weil sie gar nicht
#      durch diese Zeile laufen: sie gehen ueber den Kartenzeichner
#      (exit3) und sitzen dort ohnehin mittig.
#
#      textImmerMitte=0 schaltet alles zurueck.

P.append((
 'const zFF=Number(BS_KACHEL.folgeFuss)||0;zFF>0&&t.folienRolle&&t.folienRolle!=="deckblatt"&&(De=$e?n*(Number(BS_KACHEL.folgeMitte)||.58)-ae/2+Et/2:n*zFF-ae+Et/2);',
 'const zFF=Number(BS_KACHEL.folgeFuss)||0;zFF>0&&t.folienRolle&&t.folienRolle!=="deckblatt"&&(De=$e?n*(Number(BS_KACHEL.folgeMitte)||.58)-ae/2+Et/2:n*zFF-ae+Et/2);BS_KACHEL.textImmerMitte===1&&(De=n*(Number(BS_KACHEL.textMitte)||.5)-ae/2+Et/2);',
 'Harte Regel: der Textblock sitzt mittig, egal was Lage und Fuss sagen', 1))

P.append((
 'bildTon:"14,13,12"',
 'bildTon:"14,13,12",textImmerMitte:1',
 'Die Regel einschalten', 1))

# 202  Der Ueberzug war dreieinhalbmal zu dunkel
#
#      "Das overlay ist extrem dunkel was ist da los bei den
#      rotierenden mit schwarz?"
#
#      GEMESSEN, mittlere Helligkeit der Kachel (0-255), Tag 2 und 4
#      sind die rotierenden, Tag 1 und 3 die andere Haelfte:
#
#          karten257 (vorher, schwarzweiss)   81  79  |  71  80
#          karten260 (Anthrazit .42)          63  63  |  71  80
#          karten263 (schwarz .42)            23  23  |  71  80
#
#      Der Grund ist die REIHENFOLGE. Der Ueberzug liegt direkt auf dem
#      Foto - darueber kommen erst der Tiefenverlauf (tiefeOben .55,
#      tiefeUnten .85) und die Vignette (.6). Die multiplizieren den
#      Ueberzug, sie addieren ihn nicht. 42% Schwarz unten heissen
#      deshalb nicht 42% weniger Licht, sondern knapp drei Viertel.
#
#      EIN IRRWEG, der hier nicht steht: die Vermutung, die
#      Selbstregelung zAuf dunkle ein zweites Mal ab, weil sie das
#      Quellbild misst und den Ueberzug nicht kennt. Gegenprobe mit
#      zAuf *= (1 - bildUeberzug) und derselben Korrektur an der
#      Vignette: 23 -> 24. Wirkungslos, wieder verworfen.
#
#      Stattdessen die Deckkraft gemessen:
#
#          bildUeberzug   .08  .15  .22  .30  .42
#          Helligkeit      64   54   45   35   23
#
#      .15 gewaehlt: deutlich dunkler als das Anthrazit, das ihr zu
#      hell war, und weit weg von den 23.
#
#      "Komplettes Overlay" und "so hell wie der Rest des Feeds"
#      schliessen sich aus - ein Ueberzug dunkelt nun einmal ab. Die
#      Tabelle steht hier, damit der naechste Wunsch ein Nachschlagen
#      ist und kein Versuch.

P.append((
 'bildUeberzug:.42',
 'bildUeberzug:.15',
 'Ueberzug von 42% auf 15% - gemessen, nicht geschaetzt', 1))

# 203  Auf den Ueberzugskacheln kein Tiefenverlauf und keine Vignette
#
#      "Dann nimm auf diesen (!) den Tiefenverlauf und die Vignette
#      weg."
#
#      Ein Merker zUeberAn, ganz oben in Ca gesetzt, sobald der
#      Ueberzug gezeichnet wurde. Der Tiefenverlauf und die Vignette
#      fragen ihn ab und zeichnen dann nicht. Beide sind an zwei ganz
#      verschiedenen Stellen in Ca, deshalb ein Merker und keine
#      Bedingung vor Ort - zSat ist an der Verlaufsstelle nicht in
#      Reichweite.
#
#      KORREKTUR ZU 202. Dort steht, der Verlauf und die Vignette
#      wuerden den Ueberzug multiplizieren und deshalb sei er so
#      dunkel. Das ist FALSCH, jetzt gegengemessen:
#
#          bildUeberzug .15   mit Verlauf+Vignette  54
#                             ohne                  56
#          bildUeberzug .42   mit                   23
#                       .38   ohne                  28
#
#      Zwei Punkte Unterschied. Die beiden Ebenen tragen fast nichts
#      zur Dunkelheit bei - die Steilheit kommt woanders her und ist
#      weiter nicht erklaert. Die gemessene Kurve gilt trotzdem, die
#      Erklaerung dazu nicht.
#
#      Was sich WIRKLICH aendert, ist der Charakter: die Kachel ist
#      jetzt gleichmaessig statt oben und unten abgedunkelt und in den
#      Ecken abgeschattet.
#
#      Neue Kurve ohne die beiden Ebenen:
#          bildUeberzug   .15  .28  .38  .48
#          Helligkeit      56   39   28   20
#
#      Bei .15 geblieben, also derselbe Helligkeitswert wie vorher.
#
#      ACHTUNG: der Tiefenverlauf hat auch die Schrift lesbar gemacht.
#      Auf diesen Kacheln steht die Headline jetzt auf dem blanken Foto
#      plus 15% Schwarz. Bei einem hellen Foto kann das knapp werden.

P.append((
 'Ca=async(e,t,r,n,i={})=>{let zGrundTon="";',
 'Ca=async(e,t,r,n,i={})=>{let zGrundTon="";let zUeberAn=!1;',
 'Merker: auf dieser Kachel liegt der Ueberzug', 1))

P.append((
 'globalCompositeOperation:zM,selectable:!1,evented:!1}))})();',
 'globalCompositeOperation:zM,selectable:!1,evented:!1})),zUeberAn=!0})();',
 'Den Merker setzen, sobald der Ueberzug gezeichnet ist', 1))

P.append((
 'const zVi=(Number(BS_KACHEL.bildVignette)||0)*zVig;if(zVi>0){',
 'const zVi=(Number(BS_KACHEL.bildVignette)||0)*zVig;if(zVi>0&&!zUeberAn){',
 'Keine Vignette unter dem Ueberzug', 1))

P.append((
 'if($e&&new RegExp(BS_KACHEL.tiefeSchriften||"Playfair").test(String(Qe))&&t.tiefenOverlay!==!1){',
 'if($e&&!zUeberAn&&new RegExp(BS_KACHEL.tiefeSchriften||"Playfair").test(String(Qe))&&t.tiefenOverlay!==!1){',
 'Kein Tiefenverlauf unter dem Ueberzug', 1))

# 204  Ein Stueck dunkler
#
#      "Bissi duenkler."
#
#      bildUeberzug von .15 auf .21. Gemessen: 56 -> 47. Der naechste
#      Stuetzpunkt der Kurve waere .28 mit 39 gewesen - das ist ein
#      Sprung, kein Stueck, deshalb dazwischen.
#
#      Kurve ohne Tiefenverlauf und Vignette (aus 203), jetzt mit dem
#      neuen Punkt:
#          bildUeberzug   .15  .21  .28  .38  .48
#          Helligkeit      56   47   39   28   20

P.append((
 'bildUeberzug:.15',
 'bildUeberzug:.21',
 'Ein Stueck dunkler: 15% auf 21%', 1))

# 205  Zurueck zu schwarzweiss
#
#      "Geh lieber zurueck zum schwarz weiss danke."
#
#      ZWEI WERTE, kein Code angefasst:
#          bildUeberzug: .21 -> 0    der Ueberzug zeichnet nicht mehr
#          swBleibt: 1               der Graustich-Rect zeichnet wieder
#
#      Damit faellt die ganze Kette 198-204 von selbst weg: ohne
#      Ueberzug bleibt zUeberAn falsch, also kommen Tiefenverlauf und
#      Vignette aus 203 von allein zurueck. tonNeutral steht seit 200
#      wieder auf "13,13,13", der Rotationsslot ist also exakt der
#      alte.
#
#      GEMESSEN: Tag 2 = 80, Tag 4 = 79. Referenz karten257, vor der
#      ganzen Uebung: 81 und 79. Wiederhergestellt.
#
#      Die Mechanik bleibt im Bundle liegen und ist ueber diese zwei
#      Werte jederzeit wieder einschaltbar. Die gemessenen Kurven
#      stehen in 202, 203 und 204.
#
#      WAS BLEIBT: 197 (Story Planner oeffnet) und 201 (Text sitzt
#      mittig) sind unberuehrt - die gehoerten nicht zu dieser Kette.

P.append((
 'bildUeberzug:.21',
 'bildUeberzug:0,swBleibt:1',
 'Ueberzug aus, Entsaettigung wieder an - zurueck zu schwarzweiss', 1))

# 206  Story-Folien sahen aus wie aus einer anderen App
#
#      "Also bitte genauso wie die Feed Posts und auch die Text
#      Skalierung gleich und kein Hintergrund."
#      Dazu ein Bild: weisse Kaestchen hinter jeder Textzeile, Schrift
#      viel zu gross, quer ueber die ganze Kachel.
#
#      URSACHE: der Story Planner gibt dem Zeichner nur Farben und
#      Schriften der Marke mit:
#
#          <Kl data={{...E, fontFamily, accentFontFamily, color,
#                     backgroundColor, accentColor, secondaryColor}} />
#
#      Kein textBands, keine folienRolle, kein format. Der Zeichner
#      faellt damit in das alte Layout - dieselbe Falle wie bei
#      bandStyle:"none". Die weissen Kaestchen sind die Zeilenplatten
#      aus diesem Layout.
#
#      zStoryFeed() ergaenzt genau die vier Eigenschaften, die eine
#      Feed-Kachel ausmachen:
#          format "9:16", textBands true,
#          folienRolle (erste Folie deckblatt, Rest folge, damit die
#            Deckblatt- und Folgeschrift greifen),
#          _tag (damit Saettigung und Vignette rotieren wie im Feed)
#      Alles andere faellt im Zeichner auf dieselben Vorgaben wie beim
#      Feed zurueck: textStil "platte", kachelSchrift "marke", karte
#      "dunkel".
#
#      Die weissen Kaestchen verschwinden dabei von selbst: liegt ein
#      Foto darunter, setzt der Zeichner tt.platten=!1.
#
#      AN ZWEI STELLEN, sonst sieht der Export anders aus als das
#      Gitter: die Vorschaukachel und "Alle in Fotos".
#
#      GEPRUEFT mit den fuenf Folien aus der Story-Strategie: vorher
#      winzige Schrift unten auf schwarzem Grund, jetzt dunkle Karte,
#      Playfair in Feed-Groesse, Handle mit Monogramm.

P.append((
 ',KX=()=>{',
 ',zStoryFeed=(zs,zi)=>{try{return{...zs,format:"9:16",textBands:!0,folienRolle:(zs&&zs.folienRolle)||(zi===0?"deckblatt":"folge"),_tag:typeof (zs&&zs._tag)=="number"?zs._tag:(Number(zi)||0)+1}}catch(zz){return zs}},KX=()=>{',
 'Story-Folien bekommen dieselben Eigenschaften wie Feed-Kacheln', 1))

P.append((
 'v.jsx(Kl,{data:{...E,fontFamily:e.currentBrandConfig.typography.fontFamily,',
 'v.jsx(Kl,{data:{...zStoryFeed(E,H),fontFamily:e.currentBrandConfig.typography.fontFamily,',
 'Im Gitter', 1))

P.append((
 'await Ca(W,{...pe,visualElements:pe.visualElements||[]},ye,ue,{slideIndex:fe,',
 'await Ca(W,{...zStoryFeed(pe,fe),visualElements:pe.visualElements||[]},ye,ue,{slideIndex:fe,',
 'Und beim Export, damit beide gleich aussehen', 1))

# 207  Screenshot-Knopf im Story Planner, und 9:16 bekommt eigene
#      Schriftgroessen
#
#      "Ich hab keinen Button um den Screenshot zu setzen und die
#      Skalierung der Schrift ist 40% zu gross."
#
#      DER KNOPF. Der Dialog cG nimmt alles ueber Props:
#          cG({isOpen, onClose, placeholders, onApply})
#      Er laedt die Bibliothek selbst aus Supabase, gleicht selbst ab
#      und kann OCR selbst nachlesen. Fuer die Stories fehlten also nur
#      zwei Funktionen: zSsPlatz() sammelt die Platzhalter aus den
#      Story-Folien ein (id "s_<index>", matchText aus q$), zSsLegen()
#      schreibt die Treffer zurueck. Kein neues OCR, keine zweite
#      Bibliothek - dieselben Kennungen wie im Content-Plan.
#
#      Die Hook-Zeile entsteht dabei wie in 191: aus dem eigenen Text
#      der Folie, Klammer und Kennung weggeworfen.
#
#      DIE SCHRIFT. Zwei Hebel, weil einer nicht reicht:
#
#      (1) qe, die Startgroesse. Wirkt auf KURZE Texte - die loesen die
#          Schrumpfschleife nie aus und behalten den Startwert.
#      (2) Je, das Hoehenbudget der Schrumpfschleife. Wirkt auf LANGE
#          Texte - dort bestimmt nicht der Startwert die Groesse,
#          sondern wann die Schleife aufhoert.
#
#      Erst nur (1) gebaut - wirkungslos, gemessen an einem langen
#      Satz: identische Kachel bei .71, .55 und .45. Der Grund steht
#      oben.
#
#      GEMESSEN, Hoehe des Textblocks als Anteil der Kachel:
#
#          langer Satz    aus    .393 (7 Zeilen)
#                         .60    .133 (3 Zeilen)
#          kurzer Satz    aus    .054
#                         .60    .030      -44%
#
#      Der kurze Satz isoliert die reine Schriftgroesse: .60 ergibt
#      -44%, also genau ihre 40%. storyAnteil greift nur bei
#      format "9:16", der Feed bleibt unberuehrt.

P.append((
 'bildTon:"14,13,12"',
 'bildTon:"14,13,12",storyAnteil:.60',
 'Schriftgroesse fuer 9:16 als eigener Wert', 1))

P.append((
 'let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?(t.folienRolle==="deckblatt"?BS_KACHEL.deckblattGroesse:(BS_KACHEL.fotoGroesse||PV)):OV);',
 'let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?(t.folienRolle==="deckblatt"?BS_KACHEL.deckblattGroesse:(BS_KACHEL.fotoGroesse||PV)):OV);t.format==="9:16"&&BS_KACHEL.storyAnteil&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.storyAnteil))));',
 'Startgroesse auf Story-Kacheln kleiner - das wirkt auf kurze Texte', 1))

P.append((
 'const Je=n*(jr?(BS_KACHEL.textHoeheZaehler||.48):(BS_KACHEL.textHoehe||.74))-SR;',
 'const Je=n*(jr?(BS_KACHEL.textHoeheZaehler||.48):(BS_KACHEL.textHoehe||.74))*(t.format==="9:16"&&BS_KACHEL.storyAnteil?Number(BS_KACHEL.storyAnteil):1)-SR;',
 'Und das Hoehenbudget - das wirkt auf lange Texte', 1))

P.append((
 'zSSetzLauft(!1)};ce.useEffect(()=>{try{if(!r||e.currentBrandConfig)return;',
 'zSSetzLauft(!1)};const[zSsAuf,zSetzSsAuf]=ce.useState(!1);const zSsPlatz=()=>{const zr=[];(i||[]).forEach((zx,zi)=>{const zm=q$(zx&&zx.text);zm&&zr.push({id:"s_"+zi,matchText:zm})});return zr};const zSsLegen=async zm=>{s(zl=>zl.map((zx,zi)=>{const zu=zm&&zm["s_"+zi];if(!zu)return zx;const zHk=(()=>{try{const zt=String(zx.text||"").split(/\\r?\\n/).map(zz=>String(zz).replace(/\\[[^\\]]*\\]/g," ").replace(/\\bS-[0-9A-Z]{5}\\b/ig," ").replace(/^\\s*screenshot\\s*[:\\u2013\\u2014-]?\\s*/i," ").replace(/\\s+/g," ").trim()).filter(zz=>/[a-zA-Z\\u00C0-\\u00FF]{2}/.test(zz)).join(" ").trim();return zt&&!q$(zt)?zt:""}catch(zz){return""}})();return{...zx,overlayImage:zu,overlayIsScreenshot:!0,overlayImageScale:.8,overlayImageRounded:!1,overlayImageX:0,overlayImageY:0,overlayHook:zHk,text:"",_wasScreenshot:!0}}))};ce.useEffect(()=>{try{if(!r||e.currentBrandConfig)return;',
 'Platzhalter einsammeln und Treffer in die Story-Folien schreiben', 1))

P.append((
 'children:[v.jsx(ke,{icon:HX,className:"mr-1"})," + Slide"]})]}),',
 'children:[v.jsx(ke,{icon:HX,className:"mr-1"})," + Slide"]}),v.jsxs("button",{onClick:()=>zSetzSsAuf(!0),className:"text-sm bg-emerald-50 text-emerald-700 px-3 py-1 rounded-lg font-bold hover:bg-emerald-100 transition-colors flex items-center",children:[v.jsx(ke,{icon:RX,className:"mr-1"})," Screenshots"]})]}),',
 'Der Knopf neben "+ Slide"', 1))

P.append((
 'return e.currentBrandConfig?v.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32",children:[',
 'return e.currentBrandConfig?v.jsxs("div",{className:"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32",children:[v.jsx(cG,{isOpen:zSsAuf,onClose:()=>zSetzSsAuf(!1),placeholders:zSsPlatz(),onApply:zSsLegen}),',
 'Derselbe Dialog wie im Content-Plan, mit den Story-Folien gefuettert', 1))

# 208  Strategie und "+ Slide" raus
#
#      "Button Strategie und + slide loeschen."
#
#      Nur die beiden Knoepfe aus der Leiste. Der Strategie-Bereich und
#      die Funktion hinter "+ Slide" bleiben im Bundle liegen - sie
#      sind nur nicht mehr erreichbar. Das haelt den Weg zurueck offen
#      und spart einen Eingriff in die Zustandslogik.
#
#      GEPRUEFT: die Leiste zeigt jetzt
#          Bulk Text Input, Screenshots, Edit Sequence, Alle in Fotos
#      keine Seitenfehler.

P.append((
 'v.jsxs("button",{onClick:()=>m(!g),className:`text-sm px-3 py-1 rounded-lg font-bold transition-colors flex items-center ${g?"bg-amber-500 text-white":"bg-amber-50 text-amber-700 hover:bg-amber-100"}`,children:[v.jsx(ke,{icon:DX,className:"mr-1"})," Strategie"]}),v.jsxs("button",{onClick:D,className:"text-sm bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold hover:bg-gray-200 transition-colors flex items-center",children:[v.jsx(ke,{icon:HX,className:"mr-1"})," + Slide"]}),',
 '',
 'Die Knoepfe Strategie und + Slide aus der Story-Leiste nehmen', 1))

# 209  "Grosse Headline" hat nichts getan
#
#      "Same Branding wie der Feed nur prominenter."
#
#      Fuer die Pinnable Posts braucht es kein neues Layout. Der
#      Schalter dafuer stand schon im Kachelmenue - "Grosse Headline",
#      mit An/Aus-Anzeige. Er hat auf den Feed-Kacheln aber NICHTS
#      getan: bigHeadline wird nur im alten Layout gelesen
#
#          ae = t.bigHeadline===!0 ? Math.round(ur*1.35) : ur
#
#      und der Feed-Zeichner kennt ihn nicht. Gemessen an zwei
#      gleichen Kacheln, eine mit Schalter an: beide .235.
#
#      Jetzt greift er im Feed-Zeichner, ueber dieselben zwei Hebel wie
#      bei den Stories in 207 - Startgroesse UND Hoehenbudget. Nur der
#      Startwert haette wieder nichts gebracht, die Schrumpfschleife
#      haette ihn zurueckgeholt.
#
#      Dazu: der Tagesschalter setzt bigHeadline jetzt auf ALLE Folien
#      des Tages, nicht nur auf die erste. Ein Pinnable ist ein ganzes
#      Karussell, nicht nur sein Deckblatt. Bisheriges Verhalten geht
#      dabei nicht verloren - es hat ja nichts bewirkt.
#
#      GEMESSEN, Hoehe des Textblocks:
#          karten270  aus .235   gross .235   (kein Unterschied)
#          karten271  aus .235   gross .564
#
#      pinnAnteil 1.35, derselbe Faktor, den das alte Layout benutzt
#      hat. Schrift, Farben, Name, Kachelgrund bleiben unveraendert -
#      es ist dasselbe Branding, nur lauter.

P.append((
 'bildTon:"14,13,12"',
 'bildTon:"14,13,12",pinnAnteil:1.35',
 'Wie stark "Gross" vergroessert', 1))

P.append((
 'let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?(t.folienRolle==="deckblatt"?BS_KACHEL.deckblattGroesse:(BS_KACHEL.fotoGroesse||PV)):OV);t.format==="9:16"&&BS_KACHEL.storyAnteil&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.storyAnteil))));',
 'let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?(t.folienRolle==="deckblatt"?BS_KACHEL.deckblattGroesse:(BS_KACHEL.fotoGroesse||PV)):OV);t.format==="9:16"&&BS_KACHEL.storyAnteil&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.storyAnteil))));t.bigHeadline===!0&&BS_KACHEL.pinnAnteil&&(qe=Math.round(qe*Number(BS_KACHEL.pinnAnteil)));',
 '"Grosse Headline" wirkt jetzt auch im Feed-Zeichner', 1))

P.append((
 'const Je=n*(jr?(BS_KACHEL.textHoeheZaehler||.48):(BS_KACHEL.textHoehe||.74))*(t.format==="9:16"&&BS_KACHEL.storyAnteil?Number(BS_KACHEL.storyAnteil):1)-SR;',
 'const Je=n*(jr?(BS_KACHEL.textHoeheZaehler||.48):(BS_KACHEL.textHoehe||.74))*(t.format==="9:16"&&BS_KACHEL.storyAnteil?Number(BS_KACHEL.storyAnteil):1)*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)-SR;',
 'Und das Hoehenbudget waechst mit, sonst schrumpft die Schleife es zurueck', 1))

P.append((
 'const He=(ve.slides||[]).map((De,Ze)=>Ze===0?{...De,bigHeadline:De.bigHeadline!==!0}:De);return{...ve,slides:He}});t({contentPlan:Rt(_e,We)})},Ne=ae=>{',
 'const He=(ve.slides||[]).map((De,Ze)=>({...De,bigHeadline:(((ve.slides||[])[0]||{}).bigHeadline)!==!0}));return{...ve,slides:He}});t({contentPlan:Rt(_e,We)})},Ne=ae=>{',
 '"Gross" gilt fuer das ganze Karussell, nicht nur fuer die erste Folie', 1))

# 210  Die zwei Pinnable Posts
#
#      "Mach bitte neue Pinnable Posts ... Same Branding wie der Feed
#       nur prominenter ... 15.000 gemacht durch energetisches
#       Auftreten, und mit 18 habe ich Premium Fitnessmitgliedschaften
#       verkauft. Suechte rauslassen."
#
#      Es sind zwei Posts, nicht drei - die "4 Suechte" hat sie
#      ausdruecklich gestrichen.
#
#      Ein neuer Knopf "Pinnable" neben "Ablauf" legt beide Karussells
#      an: je sieben Folien, 4:5, jede Folie mit bigHeadline - also
#      derselbe Feed-Look, nur in der grossen Fassung aus 209. Kein
#      eigenes Layout, keine eigenen Farben.
#
#      Die Tagesnummern haengen sich hinten an den Plan (hoechster Tag
#      + 1 und + 2), damit nichts ueberschrieben wird. optional:!0,
#      damit sie nicht in der Pflichtfolge stehen.
#
#      Der Schlusssatz beider Posts ruft das ManyChat-Stichwort auf.
#      START ist aus ihrem eigenen Folientext uebernommen ("Schreib mir
#      START, wenn dein Content endlich arbeiten soll") - sie muss es
#      bestaetigen, sonst loest die Automation nicht aus. In
#      netlify/functions/write-stories.mjs steht STICHWORT weiter leer.
#
#      GEPRUEFT im Browser: Knopf da, zwei Tage angelegt, erste Folie
#          {"tage":2,"ersteTitel":"Pinnable \u2014 15 Tage","gross":true}
#      keine Seitenfehler.

P.append((
 "abAnlegen=(ae,_e)=>{",
 "pinAnlegen=()=>{const zN=(i||[]).reduce((zx,zr)=>Math.max(zx,Number(zr&&zr.day)||0),0);const zMk=(zT,zTi,zNr)=>({day:zN+zNr,title:zTi,optional:!0,slides:zT.map(zx=>({text:zx,visualElements:[],format:\"4:5\",bigHeadline:!0}))});const zA=[\"15 Tage.\\n15.000 Euro an Anfragen.\", \"Nicht durch eine neue Strategie.\\nDurch mein Auftreten.\", \"Ich habe aufgehört, mein Angebot zu erklären.\\nIch bin damit aufgetreten.\", \"Das klingt nach Soft Skill.\\nIst es nicht.\", \"Es ist der Unterschied zwischen einer, die hofft, dass jemand fragt — und einer, die weiß, was sie da hat.\", \"Du denkst, dafür brauchst du erst Ergebnisse.\\nDie Ergebnisse kommen danach. Nicht davor.\", \"Schreib mir START, wenn du wissen willst, wie das bei dir aussieht.\"],zB=[\"Mit 18 habe ich Premium-Mitgliedschaften verkauft.\", \"Nicht, weil ich ein Skript hatte.\", \"Sondern weil ich nie so getan habe, als müsste ich jemanden überreden.\", \"Verkaufen hat für mich nie so ausgesehen wie das, was Sales-Typen daraus gemacht haben.\", \"Die brauchen einen Bedarf, den sie erst erzeugen.\\nIch hatte etwas, das jemand haben wollte.\", \"Daran hat sich bis heute nichts geändert.\\nNur der Preis.\", \"Schreib mir START, wenn du verkaufen willst, ohne jemanden zu überreden.\"];t({contentPlan:Rt([...i,zMk(zA,\"Pinnable \\u2014 15 Tage\",1),zMk(zB,\"Pinnable \\u2014 Mit 18\",2)],We)});$(\"Zwei Pinnable Posts angelegt: Tag \"+(zN+1)+\" und \"+(zN+2))},abAnlegen=(ae,_e)=>{",
 "Die zwei Pinnable-Karussells anlegen", 1))

P.append((
 "v.jsxs(\"button\",{onClick:()=>abSetzen(!0),className:\"px-2.5 py-1.5 bg-white text-purple-700 border border-purple-200 rounded-lg font-bold hover:bg-purple-50 transition-colors flex items-center whitespace-nowrap text-[11px]\",children:[v.jsx(ke,{icon:AS,className:\"mr-2\"}),\"Ablauf\"]}),",
 "v.jsxs(\"button\",{onClick:()=>abSetzen(!0),className:\"px-2.5 py-1.5 bg-white text-purple-700 border border-purple-200 rounded-lg font-bold hover:bg-purple-50 transition-colors flex items-center whitespace-nowrap text-[11px]\",children:[v.jsx(ke,{icon:AS,className:\"mr-2\"}),\"Ablauf\"]}),v.jsxs(\"button\",{onClick:pinAnlegen,className:\"px-2.5 py-1.5 bg-white text-emerald-700 border border-emerald-200 rounded-lg font-bold hover:bg-emerald-50 transition-colors flex items-center whitespace-nowrap text-[11px]\",children:[v.jsx(ke,{icon:AS,className:\"mr-2\"}),\"Pinnable\"]}),",
 "Der Knopf neben Ablauf", 1))

# 211  Die Pinnable Posts sahen aus wie Reminder-Zettel
#
#      "Ernsthaft?" - mit einem Bild von zwei beigen Notizzetteln auf
#      blaugrauem Grund. Kein Foto, keine Feed-Schrift, ein Etikett
#      REMINDER darueber. Genau das Gegenteil von "Same Branding wie
#      der Feed".
#
#      Schuld war EIN Feld: optional:!0. Ich hatte es gesetzt, damit
#      die zwei Tage nicht in der Pflichtfolge stehen. optional ist
#      aber genau der Schalter, an dem die App einen Reminder erkennt:
#
#          istReminder=(ot.optional===!0||!!ot.reminderArt)
#                      &&ot.reminderArt!=="ablauf"
#
#      Zwei Folgen davon, beide sichtbar:
#        - karte wird aus der Textlaenge gewaehlt, <=110 Zeichen
#          ergibt "zettel" - die beige Notiz mit REMINDER-Zeile.
#        - im zweiten Durchgang wird das Foto abgeraeumt:
#          background:null, overlay:void 0.
#      Der Ablauf-Post entkommt dem nur ueber reminderArt==="ablauf".
#
#      optional faellt also weg. Dafuer tileMode:"photo" - derselbe
#      Wert, den der Ablauf-Post schon setzt. Damit haengen die zwei
#      Tage nicht am Hell/Dunkel-Rhythmus (textJede:7), sondern liegen
#      fest auf der Fotoseite. Die Schaltung ist abgesichert: ohne
#      Bilder im Pool (Ze.length>0) faellt sie von selbst zurueck.
#
#      Dazu ersetzt ein zweiter Druck auf den Knopf die alten
#      Pinnable-Tage, statt weitere anzuhaengen - sonst muesste sie die
#      kaputten von Hand loeschen.
#
#      NACHGESTELLT im Browser, gleicher Plan, nur anderes Bundle:
#          karten272  Tag 4 = beiger Zettel mit REMINDER
#          karten273  Tag 4 = Feed-Kachel, gleiche Schrift und
#                     gleicher Aufbau wie ein gewoehnlicher Tag
#      keine Seitenfehler.
#
#      NICHT geprueft: ob die zwei Tage im echten Feed ein Foto
#      bekommen. Der Bildpool laedt in der Testumgebung nicht - dort
#      bleiben ALLE Tage hell, auch gewoehnliche. Das ist eine Grenze
#      des Aufbaus, kein Befund ueber die App.

P.append((
 "pinAnlegen=()=>{const zN=(i||[]).reduce((zx,zr)=>Math.max(zx,Number(zr&&zr.day)||0),0);const zMk=(zT,zTi,zNr)=>({day:zN+zNr,title:zTi,optional:!0,slides:",
 "pinAnlegen=()=>{const zAlt=(i||[]).filter(zr=>!/^Pinnable/.test(String((zr&&zr.title)||\"\")));const zN=zAlt.reduce((zx,zr)=>Math.max(zx,Number(zr&&zr.day)||0),0);const zMk=(zT,zTi,zNr)=>({day:zN+zNr,title:zTi,tileMode:\"photo\",slides:",
 "Kein optional mehr (das war die Reminder-Schaltung), dafuer tileMode photo wie beim Ablauf-Post", 1))

P.append((
 "t({contentPlan:Rt([...i,zMk(zA,\"Pinnable \\u2014 15 Tage\",1),zMk(zB,\"Pinnable \\u2014 Mit 18\",2)],We)});",
 "t({contentPlan:Rt([...zAlt,zMk(zA,\"Pinnable \\u2014 15 Tage\",1),zMk(zB,\"Pinnable \\u2014 Mit 18\",2)],We)});",
 "An den bereinigten Plan anhaengen, damit ein zweiter Druck die alten ersetzt", 1))

# 212  Pinnable in normaler Schriftgroesse
#
#      "Ich moechte lieber Fotos Und den Text im Verhaeltnis Groesse
#       zu den anderen Posts."
#
#      Damit faellt bigHeadline wieder weg. Ich hatte es auf jede
#      Pinnable-Folie gesetzt, weil sie vorher "viel mehr
#      intensiviert" wollte - im Feed sieht das aber nicht nach
#      prominent aus, sondern nach anders.
#
#      Der Schalter selbst bleibt (211/209), er wird nur nicht mehr
#      automatisch gesetzt. Sie kann ihn pro Tag im Kachelmenue
#      anschalten.
#
#      tileMode:"photo" bleibt - das ist der Hebel fuer die Fotos.
#
#      GEPRUEFT ueber die Felder der erzeugten Folie, nicht ueber das
#      Bild: die Pinnable-Folie hat jetzt DIESELBE Feldliste wie eine
#      gewoehnliche Folie, bigHeadline ist nicht mehr dabei.
#          karten273  gross:true
#          karten274  gross:false
#
#      Dabei ausserdem gelernt: background steht bei KEINER Folie im
#      gespeicherten Plan, auch bei gewoehnlichen nicht. Fotos werden
#      erst beim Zeichnen zugeteilt. Die Pinnable-Tage sind ab hier
#      also nicht mehr von einem gewoehnlichen Tag zu unterscheiden.

P.append((
 "slides:zT.map(zx=>({text:zx,visualElements:[],format:\"4:5\",bigHeadline:!0}))});const zA=",
 "slides:zT.map(zx=>({text:zx,visualElements:[],format:\"4:5\"}))});const zA=",
 "Pinnable-Folien in normaler Feed-Schriftgroesse, ohne bigHeadline", 1))

# 213  Das Stichwort heisst STARTEN, nicht START
#
#      "STARTEN ist was den ManyChat Flow startet nicht START."
#
#      Ich hatte START aus einer ihrer eigenen Folien abgeleitet
#      ("Schreib mir START, wenn dein Content endlich arbeiten soll")
#      und als Vermutung gekennzeichnet. Die Vermutung war falsch.
#
#      Ein falsches Stichwort ist kein Schoenheitsfehler: die
#      Automation loest nicht aus, und wer geantwortet hat, bekommt
#      nichts. Deshalb an ALLEN drei Stellen geaendert:
#
#        1. Bundle - die Schlusszeile beider Pinnable Posts (hier).
#        2. netlify/functions/write-stories.mjs - STICHWORT stand
#           bisher absichtlich LEER, damit der Storyschreiber keins
#           erfindet. Jetzt 'STARTEN'. Der Angebotsblock schaltet
#           damit von "lade OHNE Stichwort ein" auf die Fassung mit
#           Wort um.
#        3. src/utils/germanContentTemplates.js - die alte
#           Wochenvorlage sagte ebenfalls START. Sie steckt nicht im
#           Bundle, waere aber die naechste Quelle fuer das falsche
#           Wort gewesen.
#
#      GEPRUEFT: der gerenderte Angebotsblock nennt STARTEN und
#      verlangt ausdruecklich nichts ausser dem Wort.

P.append((
 "Schreib mir START, wenn du wissen willst, wie das bei dir aussieht.",
 "Schreib mir STARTEN, wenn du wissen willst, wie das bei dir aussieht.",
 "Das ManyChat-Stichwort im Pinnable-Post A", 1))

P.append((
 "Schreib mir START, wenn du verkaufen willst, ohne jemanden zu überreden.",
 "Schreib mir STARTEN, wenn du verkaufen willst, ohne jemanden zu überreden.",
 "Das ManyChat-Stichwort im Pinnable-Post B", 1))

# 214  Der geteilte Post war nur unsichtbar, nicht weg
#
#      "Wir hatten so eine 2 Teile Version der Slide gibts die noch" -
#      "Richte den Split Post wie er war also mit Helvetica und so."
#
#      Der Zeichner konnte ihn die ganze Zeit: Zweig
#      if(t.splitBands===!0) - obere Haelfte Bandfarbe mit Text auf
#      weissen Plaettchen in Helvetica, untere Haelfte das Foto. Auch
#      der Setter kannte ihn schon:
#
#          _e==="split"?De.tileMode="split":...
#
#      und die Anzeige der aktiven Fassung ebenfalls
#      (ae.tileMode==="split"?"split":...).
#
#      Gefehlt hat NUR der Chip in der VERSION-Reihe des
#      Kachelmenues. Ein Listeneintrag, sonst nichts - kein neuer
#      Zeichencode, keine neue Logik. Deshalb kommt er auch genau so
#      zurueck wie frueher, Helvetica und Plaettchen inklusive.
#
#      splitImage greift dabei direkt in den Bildpool (xo) und geht
#      NICHT ueber den normalen Zuteiler ed. Darum zeigt diese Kachel
#      auch in der Testumgebung ein Foto, waehrend alle anderen dort
#      leer bleiben.
#
#      GEPRUEFT im Browser: Chip da, Klick setzt tileMode auf "split",
#      die Kachel zeichnet zweigeteilt. Keine Seitenfehler.

P.append((
 "{wert:\"standard\",label:\"Standard\"},{wert:\"foto\",label:\"Foto\"},{wert:\"montserrat\",label:\"Fließtext auf Foto\"}",
 "{wert:\"standard\",label:\"Standard\"},{wert:\"foto\",label:\"Foto\"},{wert:\"split\",label:\"Geteilt\"},{wert:\"montserrat\",label:\"Fließtext auf Foto\"}",
 "Der Chip \"Geteilt\" zurueck in die VERSION-Reihe", 1))

# 215  Der geteilte Post: weisser Kopf mit schwarzem Rahmen
#
#      "Statt Playfair haette ich lieber dieselbe Schrift wie die
#       andere aber auf weissem Hintergrund der schwarz umrahmt ist
#       in schwarz und der 2. Teil wie er ist und die Folge Folien
#       wie sie sind in der Handschrift."
#
#      Drei Aenderungen, alle am Split-Zweig:
#
#      1. Obere Haelfte war ein zweites Foto (Fe(t.background,!0)).
#         Jetzt weisser Grund mit schwarzem Rahmen, Staerke c(9),
#         innen gesetzt damit er nicht ueber die Kante laeuft.
#      2. Die Plaettchen hinter den Zeilen entfallen OBEN - auf
#         weissem Grund waeren sie unsichtbar und wuerden nur die
#         Zeilenhoehe aufblaehen. Die Schrift dort ist schwarz statt
#         Oe. Beides nur fuer lt==="oben"; unten bleibt alles wie es
#         war, samt Plaettchen und Bandlogik.
#      3. Nur das DECKBLATT wird geteilt:
#
#             splitBands:ot.tileMode==="split"&&ta==="deckblatt"
#
#         ta kommt aus CG(index, anzahl) und ist nur bei Index 0
#         "deckblatt". Die Folgefolien bleiben damit gewoehnliche
#         Feed-Folien - Playfair und Handschrift, wie sie sind.
#
#      Die Schrift oben war nie Playfair: sie kommt aus
#      typography.bodyFontFamily, bei ihrer Marke OpenSansBrand.
#      "Statt Playfair" meint das Deckblatt, das vorher wie jedes
#      andere Cover gesetzt war.
#
#      GEPRUEFT im Browser, Tag mit drei Folien:
#          Folie 1  weisser Kopf, schwarzer Rahmen, schwarze Serifenlose,
#                   Foto unten
#          Folie 2  gewoehnliche Feed-Folie, nicht geteilt
#      keine Seitenfehler.

P.append((
 "splitBands:ot.tileMode===\"split\"?!0:void 0",
 "splitBands:ot.tileMode===\"split\"&&ta===\"deckblatt\"?!0:void 0",
 "Nur das Deckblatt wird geteilt, die Folgefolien bleiben gewoehnliche Feed-Folien", 1))

P.append((
 "await Fe(t.background,!0),await Fe(t.splitImage||t.overlayImage||t.background,!1);",
 "(()=>{const zRa=c(9);e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:ge,fill:\"#FFFFFF\",selectable:!1})),e.add(new Pe.fabric.Rect({left:zRa/2,top:zRa/2,width:Math.max(1,r-zRa),height:Math.max(1,ge-zRa),fill:\"transparent\",stroke:\"#000000\",strokeWidth:zRa,selectable:!1}))})(),await Fe(t.splitImage||t.overlayImage||t.background,!1);",
 "Obere Haelfte: weisser Grund mit schwarzem Rahmen statt Foto", 1))

P.append((
 "e.add(new Pe.fabric.Rect({left:r/2,top:jr,width:Zt,height:sr*.98,originX:\"center\",originY:\"center\",fill:dr.plattenFarbe,rx:dr.rundung,ry:dr.rundung,selectable:!1}));",
 "lt!==\"oben\"&&e.add(new Pe.fabric.Rect({left:r/2,top:jr,width:Zt,height:sr*.98,originX:\"center\",originY:\"center\",fill:dr.plattenFarbe,rx:dr.rundung,ry:dr.rundung,selectable:!1}));",
 "Keine Plaettchen auf dem weissen Teil - dort waeren sie unsichtbar", 1))

P.append((
 "fontStyle:ur.kursiv?\"italic\":\"normal\",fontWeight:\"400\",fill:Oe,selectable:!1}",
 "fontStyle:ur.kursiv?\"italic\":\"normal\",fontWeight:\"400\",fill:lt===\"oben\"?\"#000000\":Oe,selectable:!1}",
 "Schwarze Schrift oben (kursive Woerter)", 1))

P.append((
 "originY:\"center\",fontSize:tt,fontFamily:wt,fontWeight:\"400\",fill:Oe,selectable:!1}",
 "originY:\"center\",fontSize:tt,fontFamily:wt,fontWeight:\"400\",fill:lt===\"oben\"?\"#000000\":Oe,selectable:!1}",
 "Schwarze Schrift oben (gewoehnliche Zeilen)", 1))

# 216  215 wieder zurueck - es ging nie um den geteilten Post
#
#      "Aehm ich meinte nicht die geteilten aendere das zurueck ich
#       meinte alle Posts."
#
#      Ich hatte ihren Satz auf den geteilten Post bezogen, weil wir
#      gerade darueber gesprochen hatten. Gemeint waren die Deckblaetter
#      aller Posts.
#
#      Alle fuenf Eingriffe aus 215 sind hier umgedreht. Nachgerechnet:
#      der Stand ist danach BYTEWEISE wieder karten276.
#
#      Die Abschnitte 214 (der Chip "Geteilt") und alles davor bleiben.
#      Was sie wirklich will, ist noch nicht gebaut - erst muss klar
#      sein, ob das Foto auf dem Deckblatt verschwindet.

P.append((
 "splitBands:ot.tileMode===\"split\"&&ta===\"deckblatt\"?!0:void 0",
 "splitBands:ot.tileMode===\"split\"?!0:void 0",
 "Zurueck: Nur das Deckblatt wird geteilt, die Folgefolien bleiben gewoehnliche Feed-Folien", 1))

P.append((
 "(()=>{const zRa=c(9);e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:ge,fill:\"#FFFFFF\",selectable:!1})),e.add(new Pe.fabric.Rect({left:zRa/2,top:zRa/2,width:Math.max(1,r-zRa),height:Math.max(1,ge-zRa),fill:\"transparent\",stroke:\"#000000\",strokeWidth:zRa,selectable:!1}))})(),await Fe(t.splitImage||t.overlayImage||t.background,!1);",
 "await Fe(t.background,!0),await Fe(t.splitImage||t.overlayImage||t.background,!1);",
 "Zurueck: Obere Haelfte: weisser Grund mit schwarzem Rahmen statt Foto", 1))

P.append((
 "lt!==\"oben\"&&e.add(new Pe.fabric.Rect({left:r/2,top:jr,width:Zt,height:sr*.98,originX:\"center\",originY:\"center\",fill:dr.plattenFarbe,rx:dr.rundung,ry:dr.rundung,selectable:!1}));",
 "e.add(new Pe.fabric.Rect({left:r/2,top:jr,width:Zt,height:sr*.98,originX:\"center\",originY:\"center\",fill:dr.plattenFarbe,rx:dr.rundung,ry:dr.rundung,selectable:!1}));",
 "Zurueck: Keine Plaettchen auf dem weissen Teil - dort waeren sie unsichtbar", 1))

P.append((
 "fontStyle:ur.kursiv?\"italic\":\"normal\",fontWeight:\"400\",fill:lt===\"oben\"?\"#000000\":Oe,selectable:!1}",
 "fontStyle:ur.kursiv?\"italic\":\"normal\",fontWeight:\"400\",fill:Oe,selectable:!1}",
 "Zurueck: Schwarze Schrift oben (kursive Woerter)", 1))

P.append((
 "originY:\"center\",fontSize:tt,fontFamily:wt,fontWeight:\"400\",fill:lt===\"oben\"?\"#000000\":Oe,selectable:!1}",
 "originY:\"center\",fontSize:tt,fontFamily:wt,fontWeight:\"400\",fill:Oe,selectable:!1}",
 "Zurueck: Schwarze Schrift oben (gewoehnliche Zeilen)", 1))

# 217  Deckblaetter: weisser Kasten mit schwarzem Rahmen
#
#      "Statt Playfair ... dieselbe Schrift wie die andere aber auf
#       weissem Hintergrund der schwarz umrahmt ist in schwarz und
#       der 2. Teil wie er ist und die Folge Folien wie sie sind in
#       der Handschrift" - und dann: "ich meinte alle Posts".
#      Auf Nachfrage: das Foto bleibt, der Kasten sitzt darauf.
#
#      Ein Schalter zKa traegt alles:
#
#          zKa = BS_KACHEL.kastenAn===1
#                && t.folienRolle==="deckblatt"
#                && !tt.istKarte
#
#      Karten (Zettel, Ablauf, Reminder) sind ausgenommen, die haben
#      ihre eigene Gestalt. Folgefolien ebenfalls - dort ist
#      folienRolle nie "deckblatt", Playfair und Handschrift bleiben.
#
#      Was zKa bewirkt:
#        - Qe wird die Flieszschrift der Marke statt deckblattFamilie.
#        - EIN Kasten hinter dem ganzen Ueberschriftsblock: weiss,
#          darauf ein schwarzer Rahmen. Breite aus PB (die breiteste
#          Ueberschriftszeile, war schon berechnet), Hoehe Lt*Et*zF.
#          Auf r*.94 gedeckelt, damit er nie ueber die Kachel laeuft.
#        - Die Plaettchen je Zeile entfallen dort - der Kasten ist
#          schon da.
#        - Ueberschrift schwarz, ohne Schlagschatten. Der Schatten
#          wuerde auf Weiss nur schmieren.
#        - zGT (der geteilte Textsatz, geteiltAnteil 25) bleibt auf
#          Deckblaettern aus. Er verschiebt De mitten in der Schleife,
#          und der Kasten wird vorher gemessen.
#
#      Ohne Foto ist nurErsteZeilePlatte nicht gesetzt, damit Lt=0 und
#      der Kasten faellt von selbst weg. Reine Textdeckblaetter bleiben
#      also wie sie waren.
#
#      Der zweite Teil ist unberuehrt: QeZ, Groesse, Farbe, Schatten
#      der Handschrift stehen wie vorher.
#
#      GEPRUEFT im Browser, Deckblatt mit Foto:
#          eine Zeile   Kasten eng um "15 Tage."
#          vier Zeilen  Kasten waechst mit, Handschrift darunter frei
#      keine Seitenfehler.

P.append((
 "t.folienRolle&&t.folienRolle!==\"deckblatt\"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);",
 "t.folienRolle&&t.folienRolle!==\"deckblatt\"&&BS_KACHEL.folgeFamilie&&(Qe=BS_KACHEL.folgeFamilie);const zKa=BS_KACHEL.kastenAn===1&&t.folienRolle===\"deckblatt\"&&!tt.istKarte;zKa&&(Qe=(i.typography&&i.typography.bodyFontFamily)||t.bodyFontFamily||\"HelveticaNeueBrand\");",
 "zKa: der Kasten gilt auf jedem Deckblatt ausser auf Karten; Schrift dort die Flieszschrift", 1))

P.append((
 "&&$e&&tt.nurErsteZeilePlatte===!0&&Lt>0&&dr.length>Lt;dr.forEach((Je,rt)=>{",
 "&&$e&&tt.nurErsteZeilePlatte===!0&&Lt>0&&dr.length>Lt&&!zKa;zKa&&Lt>0&&(()=>{const zPx=r*(Number(BS_KACHEL.kastenPolsterX)||.055),zPy=r*(Number(BS_KACHEL.kastenPolsterY)||.045),zRa=Math.max(1,r*(Number(BS_KACHEL.kastenRahmen)||.009)),zB=Math.min(r*.94,PB+It*2+zPx*2),zH=Lt*Et*zF+zPy*2,zX=tt.ausrichtung===\"links\"?Math.min(r-zB/2,_e-It+zB/2):r/2,zY=De+(Lt-1)*Et*zF/2;e.add(new Pe.fabric.Rect({left:zX,top:zY,width:zB,height:zH,originX:\"center\",originY:\"center\",fill:\"#FFFFFF\",selectable:!1,evented:!1})),e.add(new Pe.fabric.Rect({left:zX,top:zY,width:Math.max(1,zB-zRa),height:Math.max(1,zH-zRa),originX:\"center\",originY:\"center\",fill:\"transparent\",stroke:\"#000000\",strokeWidth:zRa,selectable:!1,evented:!1}))})();dr.forEach((Je,rt)=>{",
 "Der weisse Kasten mit schwarzem Rahmen hinter dem Ueberschriftsblock; zGT bleibt dabei aus", 1))

P.append((
 "!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste)&&e.add(new Pe.fabric.Rect({left:tt.ausrichtung===\"links\"?_e-It+qt/2:r/2,top:De,width:qt,height:Et+c(1.5)",
 "!(zKa&&Ve)&&!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste)&&e.add(new Pe.fabric.Rect({left:tt.ausrichtung===\"links\"?_e-It+qt/2:r/2,top:De,width:qt,height:Et+c(1.5)",
 "Keine Plaettchen je Zeile, wo schon der Kasten liegt", 1))

P.append((
 "fill:(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":tt.schriftFarbe||\"#FFFFFF\",selectable:!1,stroke:",
 "fill:zKa&&Ve?\"#000000\":(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":tt.schriftFarbe||\"#FFFFFF\",selectable:!1,stroke:",
 "Schwarze Ueberschrift im Kasten (ganze Zeile)", 1))

P.append((
 "shadow:(ge||!tt.platten&&(!Ve||tt.ohnePlatteErste))&&!lt?me():void 0});",
 "shadow:zKa&&Ve?void 0:((ge||!tt.platten&&(!Ve||tt.ohnePlatteErste))&&!lt?me():void 0)});",
 "Kein Schlagschatten auf Weiss (ganze Zeile)", 1))

P.append((
 "fill:rr?tt.highlight:(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":tt.schriftFarbe||\"#FFFFFF\",selectable:!1,shadow:(ge||!tt.platten)&&!lt?me():void 0});",
 "fill:rr?tt.highlight:zKa&&Ve?\"#000000\":(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":tt.schriftFarbe||\"#FFFFFF\",selectable:!1,shadow:zKa&&Ve?void 0:((ge||!tt.platten)&&!lt?me():void 0)});",
 "Dasselbe fuer hervorgehobene Einzelwoerter", 1))

P.append((
 "geteilt:1,geteiltAnteil:25",
 "geteilt:1,geteiltAnteil:25,kastenAn:1,kastenPolsterX:.055,kastenPolsterY:.045,kastenRahmen:.009",
 "Den Kasten einschalten und seine Masse", 1))

# 218  Kasten kleiner, Schreibschrift statt Serifenlose
#
#      "Kleiner? Und die Schreibschrift statt die non serif?"
#
#      Schrift: Qe wird im Kasten BS_KACHEL.zweiteFamilie
#      ("Nothing You Could Do") - dieselbe Hand wie die zweite Zeile.
#
#      Kleiner war der lehrreiche Teil. Erster Versuch: nur die
#      Startgroesse qe mal .72. Ergebnis: KEIN Unterschied. Dieselbe
#      Falle wie bei der Story-Schrift in 207 - die Schrumpfschleife
#      fuellt das Hoehenbudget Je wieder auf, egal wo sie anfaengt.
#
#      Zweiter Versuch: nur die Spalte schmaler. Ergebnis: schmaler
#      UND hoeher, sechs Zeilen statt vier. Auch nicht kleiner,
#      nur anders geschnitten.
#
#      Was wirkt, sind alle drei zusammen:
#        qe            * kastenAnteil   (Startgroesse)
#        Je            * kastenAnteil   (Hoehenbudget)
#        Qt aus kastenSpalte statt zbr  (Spaltenbreite)
#      Erst dann schrumpft der Block wirklich: vier Zeilen statt
#      sechs, Luft links und rechts, Foto ringsum sichtbar.
#
#      Dazu ein Abstand unter dem Kasten. Der Kasten reicht um
#      kastenPolsterY tiefer als die letzte Zeile, die Handschrift
#      setzte davor genau auf seiner Unterkante auf. zKaLuft schiebt
#      sie beim Uebergang rt===Lt einmalig nach unten.
#
#      GEPRUEFT im Browser, gleiches Deckblatt:
#          karten279  vier Zeilen Serifenlose, Kasten ueber die
#                     volle Spalte, Handschrift klebt an der Kante
#          karten280  vier Zeilen Hand, Kasten mit Rand, Handschrift
#                     frei darunter
#      keine Seitenfehler.

P.append((
 "const zKa=BS_KACHEL.kastenAn===1&&t.folienRolle===\"deckblatt\"&&!tt.istKarte;zKa&&(Qe=(i.typography&&i.typography.bodyFontFamily)||t.bodyFontFamily||\"HelveticaNeueBrand\");",
 "const zKa=BS_KACHEL.kastenAn===1&&t.folienRolle===\"deckblatt\"&&!tt.istKarte;zKa&&(Qe=BS_KACHEL.zweiteFamilie||(i.typography&&i.typography.bodyFontFamily)||t.bodyFontFamily||\"HelveticaNeueBrand\",qe=Math.max(c(12),Math.round(qe*(Number(BS_KACHEL.kastenAnteil)||.72))));",
 "Schreibschrift im Kasten, und die Startgroesse kleiner", 1))

P.append((
 "Qt=r*zbr-(tt.polsterX||0)*2",
 "Qt=r*(zKa&&BS_KACHEL.kastenSpalte?Number(BS_KACHEL.kastenSpalte):zbr)-(tt.polsterX||0)*2",
 "Schmalere Spalte im Kasten, damit er Luft an den Seiten laesst", 1))

P.append((
 "*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)-SR;let rt=0;for(;;){",
 "*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)*(zKa?(Number(BS_KACHEL.kastenAnteil)||.72):1)-SR;let rt=0;for(;;){",
 "Der zweite Hebel: auch das Hoehenbudget schrumpft, sonst holt die Schleife die Groesse zurueck", 1))

P.append((
 "zKa&&Lt>0&&(()=>{const zPx=",
 "const zKaLuft=zKa&&Lt>0?r*((Number(BS_KACHEL.kastenPolsterY)||.045)+(Number(BS_KACHEL.kastenLuft)||.02)):0;zKa&&Lt>0&&(()=>{const zPx=",
 "Abstand unter dem Kasten ausrechnen", 1))

P.append((
 "if(zGT&&rt===Lt){const zU=n*(BS_KACHEL.geteiltUnten||BS_KACHEL.textUnten||.86)",
 "if(zKa&&rt===Lt)De+=zKaLuft;if(zGT&&rt===Lt){const zU=n*(BS_KACHEL.geteiltUnten||BS_KACHEL.textUnten||.86)",
 "Die Handschrift beginnt unter dem Kasten, nicht auf seiner Kante", 1))

P.append((
 "kastenAn:1,kastenPolsterX:.055",
 "kastenAn:1,kastenAnteil:.72,kastenSpalte:.72,kastenLuft:.02,kastenPolsterX:.055",
 "Groesse, Spaltenbreite und Abstand des Kastens", 1))

# 219  Noch kleiner - und die Handschrift wieder gross
#
#      "Kleiner. Die Handschrift darunter ist zu klein."
#
#      Das zweite war eine Nebenwirkung des ersten, aus 218. qe2, die
#      Groesse der Handschrift, wird aus qe abgeleitet:
#
#          qe2 = qe * zweitAnteil * handGroesse
#
#      Als der Kasten qe mal kastenAnteil genommen hat, ist die
#      Handschrift lautlos mitgeschrumpft. Sie war nie gemeint.
#
#      Jetzt haengt sie nicht mehr daran:
#
#          * (zKa ? kastenHand / kastenAnteil : 1)
#
#      Die Division holt genau den Faktor wieder heraus, den der
#      Kasten abgezogen hat. kastenHand 1 waere die Groesse von vor
#      218; 1.12 ist etwas darueber, weil sie sie zu klein fand.
#      Wichtig dabei: die Handschrift bleibt gleich gross, egal wie
#      klein der Kasten noch wird.
#
#      Kasten: kastenAnteil .72 -> .60, kastenSpalte .72 -> .64.
#
#      GEPRUEFT im Browser, gleiches Deckblatt: Kasten schmaler und
#      niedriger als in karten280, Handschrift darunter deutlich
#      groesser. Keine Seitenfehler.

P.append((
 "qe2=$e?Math.round(qe*((zVS&&BS_KACHEL.versalZweitAnteil)||BS_KACHEL.zweitAnteil||1)*((zVS||BS_KACHEL.folgeZweitHand||!(t.folienRolle&&t.folienRolle!==\"deckblatt\"))?(Number(BS_KACHEL.handGroesse)||1):1)):qe,",
 "qe2=$e?Math.round(qe*((zVS&&BS_KACHEL.versalZweitAnteil)||BS_KACHEL.zweitAnteil||1)*((zVS||BS_KACHEL.folgeZweitHand||!(t.folienRolle&&t.folienRolle!==\"deckblatt\"))?(Number(BS_KACHEL.handGroesse)||1):1)*(zKa?(Number(BS_KACHEL.kastenHand)||1)/(Number(BS_KACHEL.kastenAnteil)||.72):1)):qe,",
 "Die Handschrift haengt nicht mehr an der verkleinerten Kastenschrift", 1))

P.append((
 "kastenAn:1,kastenAnteil:.72,kastenSpalte:.72,kastenLuft:.02",
 "kastenAn:1,kastenAnteil:.60,kastenSpalte:.64,kastenHand:1.12,kastenLuft:.02",
 "Kasten nochmal kleiner, Handschrift eigene Groesse", 1))

# 220  Beere statt Schwarz im Kasten
#
#      "Vielleicht die Schrift im Kasten besser rot rosa probiere es
#       hier gerendert bitte" - dann: "4".
#
#      Vier Toene gerendert, nichts davon veroeffentlicht:
#          1  #FF3A2E  ihr Akzentrot aus der Marke
#          2  #E8836B  Koralle, der Ton des Namenszugs
#          3  #D9566B  Rose
#          4  #B03A5B  Beere      <- gewaehlt
#
#      Die helleren Toene sind auf der duennen Schreibschrift schwer
#      zu lesen: die Striche sind nur wenige Pixel breit, und je
#      heller der Ton auf Weiss, desto mehr flimmert er. Beere traegt
#      Farbe und bleibt am Handy lesbar.
#
#      Die Farbe haengt an BS_KACHEL.kastenFarbe. Faellt der Schluessel
#      weg, ist die Schrift wieder schwarz - der alte Stand bleibt also
#      als Rueckfalltuer erhalten.
#
#      GEPRUEFT: das gerenderte Deckblatt ist BYTEWEISE dasselbe Bild
#      wie die Probe, die sie gewaehlt hat. Keine Seitenfehler.

P.append((
 "fill:rr?tt.highlight:zKa&&Ve?\"#000000\":",
 "fill:rr?tt.highlight:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):",
 "Kastenfarbe fuer hervorgehobene Einzelwoerter", 1))

P.append((
 "fill:zKa&&Ve?\"#000000\":",
 "fill:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):",
 "Kastenfarbe fuer die ganze Zeile", 1))

P.append((
 "kastenAn:1,kastenAnteil:.60",
 "kastenAn:1,kastenFarbe:\"#B03A5B\",kastenAnteil:.60",
 "Beere als Schriftfarbe im Kasten", 1))

# 221  Playfair zurueck in den Kasten
#
#      "Hm kann man nicht gut lesen aber Playfair mit Kasten und in
#       der Farbe?"
#
#      Sie hat recht, und der Grund ist die Strichstaerke. "Nothing
#      You Could Do" zieht Linien von wenigen Pixeln. In Schwarz auf
#      Weiss traegt das noch; sobald Farbe dazukommt, sinkt der
#      Kontrast an jeder Kante und die Schrift franst aus. Playfair
#      hat kraeftige Grundstriche - dieselbe Farbe haelt dort.
#
#      Also: Kasten bleibt, Beere bleibt, Groesse bleibt (.60, von ihr
#      zweimal nachjustiert). Nur die Schrift geht zurueck auf
#      Playfair Display.
#
#      Dafuer ein eigener Schluessel kastenSchrift, statt die alte
#      Zeile umzuschreiben. Damit stehen jetzt drei Wege offen, ohne
#      Eingriff in den Zeichner:
#          kastenSchrift gesetzt   diese Schrift
#          nicht gesetzt           zweiteFamilie, also die Hand
#          kastenAn 0              gar kein Kasten
#
#      GEPRUEFT: das gerenderte Deckblatt ist BYTEWEISE dasselbe Bild
#      wie die Probe. Keine Seitenfehler.

P.append((
 "zKa&&(Qe=BS_KACHEL.zweiteFamilie||(i.typography&&i.typography.bodyFontFamily)||t.bodyFontFamily||\"HelveticaNeueBrand\"",
 "zKa&&(Qe=BS_KACHEL.kastenSchrift||BS_KACHEL.zweiteFamilie||(i.typography&&i.typography.bodyFontFamily)||t.bodyFontFamily||\"HelveticaNeueBrand\"",
 "Eigene Schrift fuer den Kasten, faellt sonst auf die Hand zurueck", 1))

P.append((
 "kastenAn:1,kastenFarbe:\"#B03A5B\",kastenAnteil:.60",
 "kastenAn:1,kastenFarbe:\"#B03A5B\",kastenSchrift:\"Playfair Display\",kastenAnteil:.60",
 "Playfair im Kasten", 1))

# 222  Kasten eine Stufe groesser
#
#      "Ja groesser."
#
#      kastenAnteil .60 -> .70. Sonst nichts. Mit Playfair vertraegt
#      der Kasten mehr als mit der duennen Hand, deshalb war das
#      Verkleinern aus 219 an die alte Schrift gebunden, nicht an ihren
#      Geschmack.
#
#      Die Handschrift darunter bleibt unveraendert gross - genau
#      dafuer steht die Division kastenHand/kastenAnteil aus 219. Sie
#      haelt beide Groessen auseinander, in beide Richtungen.
#
#      MERKE fuer den naechsten Bildvergleich: die Probe pf70 hiess
#      beim Pruefen schon nicht mehr so, und index-B5karten282.js war
#      zu dem Zeitpunkt bereits eine Weiterleitung. Ein Nachbau aus
#      der Datei im Arbeitsverzeichnis vergleicht dann 338 Byte Stub
#      gegen das echte Bundle und meldet falschen Alarm. Die alten
#      Staende stehen in git, nicht mehr auf der Platte:
#          git show <commit>:site/assets/index-B5karten282.js
#      So verglichen: Probe und karten284 sind identisch.

P.append((
 "kastenSchrift:\"Playfair Display\",kastenAnteil:.60",
 "kastenSchrift:\"Playfair Display\",kastenAnteil:.70",
 "Kasten eine Stufe groesser", 1))

# 223  Kasten aus, Deckblatt in Sandorange
#
#      "Zurueck zu nur Playfair in weiss oder vielleicht hellorange"
#      - dann: "Sandorange mal".
#
#      Drei Proben gerendert, nichts davon veroeffentlicht, bis die
#      Wahl feststand:
#          weiss     der Stand vor dem ganzen Kasten
#          #F2A26B   Hellorange
#          #E8A87C   Sandorange   <- gewaehlt
#
#      Der Kasten geht ueber kastenAn:0 aus. Der ganze Apparat aus
#      217 bis 222 bleibt im Bundle liegen - Kasten, Rahmen, Farben,
#      Masse, die Entkopplung der Handschrift. Eine 1 holt ihn zurueck.
#
#      Neu ist nur zDf: eine Schriftfarbe fuer das Deckblatt, die auch
#      OHNE Kasten greift.
#
#          zDf = t.folienRolle==="deckblatt" && !tt.istKarte
#                && BS_KACHEL.deckblattFarbe
#
#      Karten und Folgefolien bleiben aussen vor, wie beim Kasten.
#      Ohne den Schluessel ist alles wie vorher - die Farbe faellt auf
#      tt.schriftFarbe zurueck, also Weiss.
#
#      ZU BEDENKEN, falls sie das Thema nochmal aufmacht: ohne Kasten
#      steht die Schrift direkt auf dem Foto, und der Untergrund
#      wechselt von Bild zu Bild. Weiss traegt auf jedem Foto, Orange
#      nur auf dunklen. Der Schlagschatten bleibt aktiv und faengt
#      einiges ab, aber auf einem hellen oder sandfarbenen Bild wird
#      es eng. Genau dafuer gab es den Kasten.
#
#      GEPRUEFT: das gerenderte Deckblatt ist BYTEWEISE dasselbe Bild
#      wie Probe 3. Keine Seitenfehler.

P.append((
 "const zKa=BS_KACHEL.kastenAn===1&&t.folienRolle===\"deckblatt\"&&!tt.istKarte;",
 "const zKa=BS_KACHEL.kastenAn===1&&t.folienRolle===\"deckblatt\"&&!tt.istKarte;const zDf=(t.folienRolle===\"deckblatt\"&&!tt.istKarte&&BS_KACHEL.deckblattFarbe)||\"\";",
 "zDf: eigene Schriftfarbe fuer das Deckblatt, auch ohne Kasten", 1))

P.append((
 "fill:rr?tt.highlight:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):",
 "fill:rr?tt.highlight:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):zDf&&Ve?zDf:",
 "Deckblattfarbe fuer hervorgehobene Einzelwoerter", 1))

P.append((
 "fill:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):",
 "fill:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):zDf&&Ve?zDf:",
 "Deckblattfarbe fuer die ganze Zeile", 1))

P.append((
 "kastenAn:1,kastenFarbe:\"#B03A5B\"",
 "kastenAn:0,deckblattFarbe:\"#E8A87C\",kastenFarbe:\"#B03A5B\"",
 "Kasten aus, Deckblatt in Sandorange", 1))

# 224  Deckblatt wieder weiss - und der Akzent ist nirgends
#
#      "Ok nein weiss ich find meinen Akzent nicht."
#
#      deckblattFarbe faellt weg, damit greift zDf nicht mehr und die
#      Farbe faellt auf tt.schriftFarbe zurueck, also Weiss. Der
#      Schluessel selbst bleibt im Zeichner - ein Wert genuegt, um
#      wieder einzufaerben.
#
#      NACHGESEHEN, warum sie ihren Akzent nicht findet: sie wird ihn
#      auch nicht finden. Im Feed-Zweig, 45 KB lang, kommt
#      accentColor NULL MAL vor. Ihre Marke fuehrt
#      colors.accent "#FF3A2E", der Zeichner liest das an keiner
#      Stelle.
#
#      Farbe kann auf einer Feed-Kachel nur ueber tt.highlight
#      kommen, also ueber Woerter in *Sternchen*. Auch das ist keine
#      Markenfarbe: in allen Fassungen steht dort eine feste
#      Konstante -
#          wa = "#F3E5AB"   ein blasses Gelb
#          E1 = wa
#          oder "#FFFFFF", "#000000", null
#
#      Ihr Akzent ist also nicht falsch gesetzt oder ueberschrieben,
#      er ist im Kachelzeichner schlicht nicht angeschlossen. Wenn
#      sie ihn sehen will, ist das eine Aenderung, keine Einstellung.

P.append((
 "kastenAn:0,deckblattFarbe:\"#E8A87C\",kastenFarbe:\"#B03A5B\"",
 "kastenAn:0,kastenFarbe:\"#B03A5B\"",
 "Deckblatt wieder weiss - der Schluessel faellt weg, zDf greift nicht mehr", 1))

# 225  Deckblatt in Knochen
#
#      "Ich meine ich finde geschmacklich keinen der mir gefaellt."
#      Also nicht mehr einzeln vorschlagen, sondern zwoelf Toene auf
#      EINEM Blatt, gleiche Kachel, gleicher Text, gleiches Foto.
#      Gewaehlt: Nr 2, Knochen #E7DDCF.
#
#      WIE DIE TAFEL ENTSTAND, falls sie nochmal gebraucht wird:
#      eine Probefassung, in der zDf zuerst t.probeFarbe liest,
#      danach zwoelf Tage mit je einem Ton gesaet. So stehen alle
#      Varianten in EINEM Browserlauf nebeneinander statt in zwoelf.
#      Die Einzelbilder danach mit einem kleinen Node-Skript zu einem
#      Raster zusammengesetzt - reines zlib und PNG von Hand, es ist
#      keine Bildbibliothek im Container.
#
#      STOLPERSTELLE: die Kacheln 10 bis 12 lagen beim ersten Lauf
#      unter der klebenden Kopfleiste und kamen halb als Werkzeugleiste
#      heraus. scrollIntoViewIfNeeded genuegt nicht, es braucht danach
#      noch ein Stueck Radabwaerts, sonst deckt die Leiste die obere
#      Kante ab.

P.append((
 "kastenAn:0,kastenFarbe:\"#B03A5B\"",
 "kastenAn:0,deckblattFarbe:\"#E7DDCF\",kastenFarbe:\"#B03A5B\"",
 "Deckblatt in Knochen", 1))

# 226  Deckblatt wieder weiss - und dabei bleibt es
#
#      "Hm nein weiss."
#
#      deckblattFarbe faellt wieder weg. Nachgerechnet: der Stand ist
#      danach byteweise wieder karten286.
#
#      DAMIT IST DIE FARBRUNDE DURCH. Gesehen und verworfen wurden:
#      Beere im Kasten, Beere als Flaeche mit weisser Schrift in drei
#      Rahmenfassungen, Hellorange, Sandorange, Knochen, und die Tafel
#      mit zwoelf Toenen. Jedes Mal zurueck auf Weiss.
#
#      Das ist keine Unentschlossenheit, sondern ein Befund: die
#      Ueberschrift ist nicht die Stelle fuer Farbe. Sie steht auf
#      wechselnden Fotos, also muss sie auf jedem Untergrund tragen,
#      und das kann nur Weiss. Wer hier das naechste Mal Farbe
#      vorschlaegt, schlaegt dasselbe nochmal vor.
#
#      Was NICHT probiert wurde und offen steht, falls das Thema
#      wiederkommt: die Handschriftzeile, der Namenszug unten
#      (nameFarbe), das Schild ueber der Ueberschrift, oder das
#      Sternchen-Highlight - also Farbe an einer NEBENstelle statt an
#      der Hauptzeile.
#
#      Die Schluessel deckblattFarbe, kastenAn und der ganze
#      Kastenapparat bleiben im Bundle. Ein Wert genuegt jeweils.

P.append((
 "kastenAn:0,deckblattFarbe:\"#E7DDCF\",kastenFarbe:\"#B03A5B\"",
 "kastenAn:0,kastenFarbe:\"#B03A5B\"",
 "Deckblatt wieder weiss", 1))

# 227  Story-Deckblaetter wie Posts - fuer Reels-Cover
#
#      "Ich brauche Reels Cover also bitte die Stories exakt so
#       branden wie die Posts."
#
#      Die Stories liefen schon durch den Feed-Zeichner (zStoryFeed
#      setzt format 9:16, textBands, folienRolle). Der einzige
#      Unterschied war storyAnteil .60 aus 207 - sie hatte die
#      Story-Schrift damals um 40 Prozent verkleinert.
#
#      Das gilt jetzt nur noch fuer FOLGEfolien. Deckblaetter
#      bekommen die volle Postgroesse, ueber beide Hebel: Startgroesse
#      und Hoehenbudget. Nur einer davon waere wirkungslos, siehe 218.
#
#      WARUM GETEILT statt ueberall: ihr Wunsch von damals galt den
#      Text-Folien im Story-Menue, der von heute gilt dem Cover. Beide
#      bleiben so erfuellt. Wenn sie es doch ueberall will, faellt die
#      Bedingung folienRolle!=="deckblatt" wieder weg.
#
#      GEPRUEFT: 4:5-Post und 9:16-Deckblatt mit demselben Text
#      nebeneinander - gleiche Schrift, gleiche Groessenverhaeltnisse,
#      Handschrift und Namenszug an derselben Stelle. Die Story bricht
#      in mehr Zeilen um, das liegt am schmaleren Format.
#
#      ZUM GITTER: Instagram schneidet ein Reels-Cover fuers Profil
#      mittig auf 4:5 zu, also etwa 15 bis 85 Prozent der Hoehe. Der
#      Textblock liegt bei 17 bis 80 Prozent und ueberlebt den
#      Zuschnitt. Wer hier die Lage aendert, sollte das nachrechnen.

P.append((
 "t.format===\"9:16\"&&BS_KACHEL.storyAnteil&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.storyAnteil))))",
 "t.format===\"9:16\"&&BS_KACHEL.storyAnteil&&t.folienRolle!==\"deckblatt\"&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.storyAnteil))))",
 "Story-Deckblaetter in voller Postgroesse (Startgroesse)", 1))

P.append((
 "(t.format===\"9:16\"&&BS_KACHEL.storyAnteil?Number(BS_KACHEL.storyAnteil):1)",
 "(t.format===\"9:16\"&&BS_KACHEL.storyAnteil&&t.folienRolle!==\"deckblatt\"?Number(BS_KACHEL.storyAnteil):1)",
 "Dasselbe beim Hoehenbudget, sonst schrumpft die Schleife es zurueck", 1))

# 228  Der Editor bekam die Story-Folien roh
#
#      "Achtung sobald ich bearbeite aendert es sich in ein altes
#       Branding."
#
#      Die Story-Folien tragen ihre Feed-Merkmale nicht im Plan. Sie
#      bekommen sie erst beim Zeichnen, durch zStoryFeed:
#          format 9:16, textBands, folienRolle, _tag
#
#      Das lief an ZWEI Stellen - im Raster und beim Ausgeben. Der
#      Editor war die dritte und hatte es nicht:
#
#          M = E => n("/editor", {state:{slides:i, ...}})
#
#      i sind die ROHEN Folien. Ohne textBands faellt der Zeichner in
#      das alte Layout - weisse Kachel, schwarze Serifenschrift, kein
#      Namenszug. Genau das hat sie gesehen.
#
#      Jetzt geht dieselbe Abbildung auch in den Editor.
#
#      NACHGESTELLT im Browser, Story-Planer oeffnen, Kachel
#      anklicken:
#          karten289  weisse Kachel, schwarze Serifenschrift
#          karten290  dunkle Feed-Kachel mit Namenszug, 9:16
#
#      MERKE: textBands ist die Weiche zwischen Feed-Zeichner und
#      altem Layout. Wer eine vierte Stelle baut, die Story-Folien
#      irgendwohin reicht, muss zStoryFeed mitgeben - sonst faellt
#      genau dort das Branding wieder heraus.

P.append((
 "M=E=>{n(\"/editor\",{state:{slides:i,initialSlideIndex:E,dayTitle:\"Story Sequence\"}})}",
 "M=E=>{n(\"/editor\",{state:{slides:(i||[]).map((zs,zi)=>zStoryFeed(zs,zi)),initialSlideIndex:E,dayTitle:\"Story Sequence\"}})}",
 "Der Editor bekommt die Story-Folien mit Feed-Merkmalen statt roh", 1))

# 229  Die zwanzig Layouts sind wieder da
#
#      "Bring mir alle zurueck."
#
#      Ihre zwanzig Layouts lagen vollstaendig im Bundle: die
#      Tabelle lr mit drei Grundformen (gradient, frame, plate) und
#      die Auswahl TT im Editor unter LAYOUT. Nur gewaehlt wurden sie
#      nie - der Feed-Zweig kommt im Zeichner VOR der Layouttabelle,
#      und er greift, sobald textBands gesetzt ist. Also lief jede
#      Kachel in denselben Look.
#
#      zLay(index, folie) waehlt jetzt reihum aus layoutReihe. Eine
#      Folie mit eigenem brand_-Layout behaelt ihres.
#
#      DIE STOLPERSTELLE, die mich zwei Anlaeufe gekostet hat:
#      im Eigenschaftsobjekt steht 1737 Zeichen NACH textBands
#      nochmal layout:Br,layoutId:... - und beim Objektliteral
#      gewinnt der LETZTE Schluessel. Meine erste Zuweisung wurde
#      lautlos ueberschrieben; am Zeichner kamen layout UND textBands
#      leer an. Gefunden durch Protokollieren im Zeichner, nicht durch
#      Lesen. Dazu gibt es das Objekt ZWEIMAL, fuer beide Zweige des
#      Ternaers - deshalb Anzahl 2.
#
#      NAMENSZUG: die Layout-Zweige zeichnen ihn nicht, und es gibt
#      16 Ausstiege - zu viele zum Einzelpatchen. Stattdessen haengt
#      sich Ca einmal in e.renderAll ein und zieht den Zug bei JEDEM
#      Aufruf nach. Nicht nur beim ersten: manche Zweige rufen
#      renderAll mehrfach und raeumen die Flaeche zwischendurch - bei
#      den Rahmen-Layouts fehlte er dadurch. Der Haken ist eng
#      gefasst: nur ohne textBands und nur bei brand_-Layouts, sonst
#      stuende er im Feed doppelt.
#
#      GEPRUEFT: neun aufeinanderfolgende Tage zeichnen neun
#      verschiedene Layouts, Namenszug auf allen, keine Seitenfehler.
#      layoutAn 0 stellt den alten Zustand her.

P.append((
 "Ca=async(e,t,r,n,i={})=>{let zGrundTon=\"\";",
 "Ca=async(e,t,r,n,i={})=>{let zGrundTon=\"\";try{if(BS_KACHEL.nameZeigen!==0&&t&&t.textBands!==!0&&String(t.layout||\"\").indexOf(\"brand_\")===0){const zRA=e.renderAll.bind(e);let zNo=null;e.renderAll=function(){try{if(!zNo||!e._objects||e._objects.indexOf(zNo)<0){zNo=new Pe.fabric.Text(\"carinaannaprav\",{left:r*.09,top:n*(BS_KACHEL.nameUnten||.945),originX:\"left\",originY:\"center\",fontSize:Math.round(r*(BS_KACHEL.nameAnteil||.042)),fontFamily:BS_KACHEL.nameSchrift||\"OpenSansBrand\",fontWeight:(BS_KACHEL.nameGewicht||\"400\"),charSpacing:(BS_KACHEL.nameLaufweite==null?150:BS_KACHEL.nameLaufweite),fill:BS_KACHEL.nameFarbe||\"#FFFFFF\",opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1,evented:!1});e.add(zNo)}else if(e.bringToFront)e.bringToFront(zNo)}catch(zy){}return zRA.apply(e,arguments)}}}catch(zz){}",
 "Namenszug auf den Layout-Kacheln, bei jedem renderAll nachgezogen", 1))

P.append((
 "aS=e=>{const t=Math.max(0,Number(e)||0);",
 "zLay=(zi,zs)=>{try{const ze=zs&&zs.layout;if(ze&&String(ze).indexOf(\"brand_\")===0)return ze;if(BS_KACHEL.layoutAn!==1)return \"\";const zl=String(BS_KACHEL.layoutReihe||\"\").split(\"|\").filter(Boolean);if(!zl.length)return \"\";return zl[(Number(zi)||0)%zl.length]}catch(zz){return \"\"}},aS=e=>{const t=Math.max(0,Number(e)||0);",
 "zLay: welches Layout ein Tag bekommt; eine eigene Wahl der Folie gewinnt", 1))

P.append((
 "textBands:ot.bandStyle===\"none\"?void 0:!0,",
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0,",
 "Mit Layout kein textBands - sonst kommt der Zeichner nie zur Layouttabelle", 1))

P.append((
 "layout:Br,layoutId:Mt?Br:sn?\"auto\":rt.layoutId||Br,",
 "layout:zLay(dt,rt)||Br,layoutId:zLay(dt,rt)||(Mt?Br:sn?\"auto\":rt.layoutId||Br),",
 "Beide Zweige des Eigenschaftsbaus - der letzte Schluessel gewinnt", 2))

P.append((
 "kastenAn:0,kastenFarbe:\"#B03A5B\"",
 "kastenAn:0,layoutAn:1,layoutReihe:\"brand_photo_gradient|brand_photo_bottom_left|brand_photo_top|brand_photo_center|brand_photo_bigword|brand_photo_quote|brand_photo_bottom_serif|brand_photo_frame|brand_frame_top_text|brand_frame_left|brand_frame_polaroid|brand_text_plate|brand_text_plate_top|brand_text_left|brand_text_bigword|brand_text_quote|brand_text_statement|brand_text_kicker_lead|brand_text_minimal|brand_text_bold_top\",kastenFarbe:\"#B03A5B\"",
 "Alle zwanzig Layouts in der Reihe, und der Schalter dafuer", 1))

# 230  Rotation wieder aus - sie kostet zu viel
#
#      "Aber wieso ist Handschrift und Playfair weg und auch die
#       folgeslides anders?"
#
#      Alle drei Beobachtungen haben DIESELBE Ursache: die zwanzig
#      Layouts sind ein ANDERER Zeichnerzweig. Er holt seine Schrift
#      ueber Ct() aus typography.fontFamily - bei ihr Petrona, nicht
#      Playfair - und er kennt die zweite Zeile in Handschrift
#      ueberhaupt nicht. Die steckt allein im Feed-Zweig, zusammen mit
#      Groessenlogik, Lage und Namenszug.
#
#      Und die Rotation lief ueber den GLOBALEN Folienindex, nicht
#      ueber den Tag. Damit bekam jede Folgefolie eines Karussells ihr
#      eigenes Layout - deshalb waren auch die anders.
#
#      Also layoutAn wieder 0. NACHGEMESSEN: drei Kacheln aus
#      verschiedenen Zeilen sind danach BYTEWEISE dieselben Bilder wie
#      vor der Rotation.
#
#      Der Apparat bleibt liegen: zLay, layoutReihe, der Namenshaken
#      in renderAll. Eine 1 schaltet ihn wieder ein.
#
#      WAS SIE WIRKLICH WILL, aus derselben Nachricht: vier Varianten
#      - der heutige Stand, Foto gerahmt, Text gerahmt, reiner Text.
#      Der heutige Stand und der reine Text existieren bereits, sie
#      wechseln ueber textJede. Neu sind nur die zwei GERAHMTEN.
#
#      DER RICHTIGE WEG DAFUER ist NICHT der Layout-Zweig, sondern ein
#      Rahmen IM Feed-Zeichner: dort bleiben Playfair, Handschrift,
#      Namenszug, Groessen und Folienrollen erhalten. Ein Rahmen ist
#      ein Rechteck - dieselbe Technik wie der Kasten aus 217.
#      Zusaetzlich muss die Wahl am TAG haengen, nicht am Folienindex.

P.append((
 "kastenAn:0,layoutAn:1,layoutReihe:",
 "kastenAn:0,layoutAn:0,layoutReihe:",
 "Rotation aus - sie kostet Playfair, Handschrift und die Folgefolien", 1))

# 231  Farbauswahl ueber dem Feed, einklappbar
#
#      "Bei der Farbauswahl bitte einklappbar damit ich nicht so lange
#       scrolle und am besten ueber dem Feed weil dann sehe ich das
#       Ergebnis sofort."
#
#      Die Auswahl in den Markeneinstellungen gibt es zwar, aber der
#      Zeichner liest sie nicht - siehe 224. Eine zweite Auswahl mit
#      demselben Problem waere sinnlos gewesen. Deshalb hier BEIDES:
#      die Leiste UND die Verdrahtung.
#
#      VIER ROLLEN, weil sie vier Farben wollte:
#          text      die Ueberschrift auf dem Foto
#          hand      die Handschriftzeile
#          name      der Namenszug unten
#          flaeche   der Grund der reinen Textkacheln
#
#      Gespeichert wird in localStorage unter BS_PALETTE, und beide
#      index.html holen sie VOR dem Modul nach window.BS_PALETTE -
#      genau wie BS_SCHWARZ_TAG, aus demselben Grund: der Zeichner
#      liest sie schon bei der ersten Kachel.
#
#      Nichts gesetzt heisst: alles bleibt wie im Bundle. Jede Rolle
#      laesst sich einzeln wieder loeschen (x), oder alle auf einmal.
#
#      WARUM EIN KNOPF ZUM NEUZEICHNEN: die Kacheln sind gemerkt und
#      zeichnen nicht neu, nur weil sich localStorage aendert. Ein
#      Neuladen ist ehrlicher als eine halbe Aktualisierung, und der
#      Plan liegt ohnehin in der Datenbank.
#
#      Die Leiste haengt in der Werkzeugzeile hinter dem Pinnable-
#      Knopf und ist w-full, bricht also in eine eigene Zeile um -
#      direkt ueber dem Raster, ohne Scrollen.
#
#      GEPRUEFT im Browser: Leiste da, vier Farbfelder, aufklappbar.
#      Mit text/hand/name gesetzt zeichnet die Kachel Ueberschrift,
#      Handschrift und Namenszug in den gewaehlten Toenen. Keine
#      Seitenfehler.

P.append((
 "zLay=(zi,zs)=>{try{",
 "zFarbLeiste=()=>{const[zAuf,zSetzAuf]=ce.useState(!1);const zLies=()=>{try{return JSON.parse(localStorage.getItem(\"BS_PALETTE\")||\"{}\")||{}}catch(zz){return{}}};const[zP,zSetzP]=ce.useState(zLies);const zRollen=[[\"text\",\"Überschrift\",\"#FFFFFF\"],[\"hand\",\"Handschrift\",\"#FFFFFF\"],[\"name\",\"Namenszug\",\"#E8836B\"],[\"flaeche\",\"Textfläche\",\"#0C0C0D\"]];const zSchreib=zn=>{zSetzP(zn);try{localStorage.setItem(\"BS_PALETTE\",JSON.stringify(zn));window.BS_PALETTE=zn}catch(zz){}};const zAend=(zk,zv)=>zSchreib({...zP,[zk]:zv});const zWeg=zk=>{const zn={...zP};delete zn[zk];zSchreib(zn)};const zAlles=()=>{try{localStorage.removeItem(\"BS_PALETTE\");window.BS_PALETTE=null}catch(zz){}zSetzP({})};return v.jsxs(\"div\",{className:\"w-full\",children:[v.jsxs(\"button\",{onClick:()=>zSetzAuf(!zAuf),className:\"w-full flex items-center justify-between px-3 py-2 rounded-lg border border-gray-200 bg-white text-[11px] font-bold text-gray-700 hover:bg-gray-50 transition-colors\",children:[v.jsxs(\"span\",{className:\"flex items-center gap-2\",children:[\"Farben\",v.jsx(\"span\",{className:\"flex gap-1\",children:zRollen.map(zr=>v.jsx(\"span\",{className:\"inline-block w-3 h-3 rounded-full border border-gray-300\",style:{background:zP[zr[0]]||zr[2]}},zr[0]))})]}),v.jsx(\"span\",{className:\"text-gray-400\",children:zAuf?\"Zuklappen\":\"Aufklappen\"})]}),zAuf?v.jsxs(\"div\",{className:\"mt-2 p-3 rounded-lg border border-gray-200 bg-gray-50/70\",children:[v.jsx(\"div\",{className:\"grid grid-cols-2 gap-2\",children:zRollen.map(zr=>v.jsxs(\"label\",{className:\"flex items-center gap-2 bg-white rounded-lg border border-gray-200 px-2 py-1.5\",children:[v.jsx(\"input\",{type:\"color\",value:zP[zr[0]]||zr[2],onChange:zE=>zAend(zr[0],zE.target.value),className:\"w-7 h-7 rounded cursor-pointer border-0 bg-transparent p-0\"}),v.jsx(\"span\",{className:\"text-[11px] font-bold text-gray-700 flex-1\",children:zr[1]}),zP[zr[0]]?v.jsx(\"button\",{onClick:zE=>{zE.preventDefault();zWeg(zr[0])},className:\"text-[10px] text-gray-400 hover:text-gray-700\",children:\"x\"}):null]},zr[0]))}),v.jsxs(\"div\",{className:\"flex items-center gap-2 mt-2\",children:[v.jsx(\"button\",{onClick:()=>{try{location.reload()}catch(zz){}},className:\"flex-1 px-3 py-2 rounded-lg bg-gray-900 text-white text-[11px] font-bold hover:bg-black transition-colors\",children:\"Anwenden und neu zeichnen\"}),v.jsx(\"button\",{onClick:zAlles,className:\"px-3 py-2 rounded-lg border border-gray-200 bg-white text-[11px] font-bold text-gray-600 hover:bg-gray-50\",children:\"Alles zurück\"})]}),v.jsx(\"p\",{className:\"text-[10px] text-gray-400 mt-2 leading-snug\",children:\"Die Auswahl ist gespeichert. Erst nach \\u201eAnwenden\\u201c zeichnet der Feed sie neu.\"})]}):null]})},zLay=(zi,zs)=>{try{",
 "Platzhalter fuer die Farbleiste im selben const-Block", 1))

P.append((
 "Ca=async(e,t,r,n,i={})=>{let zGrundTon=\"\";",
 "Ca=async(e,t,r,n,i={})=>{let zGrundTon=\"\";const zPal=(()=>{try{return(typeof window<\"u\"&&window.BS_PALETTE)||{}}catch(zz){return{}}})();",
 "Die gespeicherte Farbauswahl einmal je Kachel lesen", 1))

P.append((
 "fill:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):zDf&&Ve?zDf:(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":tt.schriftFarbe||\"#FFFFFF\",selectable:!1,stroke:",
 "fill:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):zDf&&Ve?zDf:(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":((Ve?zPal.text:zPal.hand)||tt.schriftFarbe||\"#FFFFFF\"),selectable:!1,stroke:",
 "Ueberschrift und Handschrift aus der Farbauswahl (ganze Zeile)", 1))

P.append((
 "fill:rr?tt.highlight:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):zDf&&Ve?zDf:(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":tt.schriftFarbe||\"#FFFFFF\",selectable:!1,shadow:",
 "fill:rr?tt.highlight:zKa&&Ve?(BS_KACHEL.kastenFarbe||\"#000000\"):zDf&&Ve?zDf:(!ge&&(tt.platten||Ve&&!tt.ohnePlatteErste))?tt.bandSchriftFarbe||\"#000000\":((Ve?zPal.text:zPal.hand)||tt.schriftFarbe||\"#FFFFFF\"),selectable:!1,shadow:",
 "Dasselbe fuer hervorgehobene Einzelwoerter", 1))

P.append((
 "fill:tt.platten?(tt.bandSchriftFarbe||tt.schriftFarbe||\"#241C16\"):(BS_KACHEL.nameFarbe||\"#FFFFFF\")",
 "fill:tt.platten?(tt.bandSchriftFarbe||tt.schriftFarbe||\"#241C16\"):(zPal.name||BS_KACHEL.nameFarbe||\"#FFFFFF\")",
 "Namenszug aus der Farbauswahl", 1))

P.append((
 "if(!t){const h=UV(u);return{platten:!1,istKarte:!0,grundFarbe:h.grund,",
 "if(!t){const h=UV(u);const zpf=(()=>{try{return(typeof window<\"u\"&&window.BS_PALETTE&&window.BS_PALETTE.flaeche)||\"\"}catch(zz){return\"\"}})();return{platten:!1,istKarte:!0,grundFarbe:zpf||h.grund,",
 "Textflaeche aus der Farbauswahl", 1))

P.append((
 "v.jsxs(\"button\",{onClick:pinAnlegen,className:\"px-2.5 py-1.5 bg-white text-emerald-700 border border-emerald-200 rounded-lg font-bold hover:bg-emerald-50 transition-colors flex items-center whitespace-nowrap text-[11px]\",children:[v.jsx(ke,{icon:AS,className:\"mr-2\"}),\"Pinnable\"]}),",
 "v.jsxs(\"button\",{onClick:pinAnlegen,className:\"px-2.5 py-1.5 bg-white text-emerald-700 border border-emerald-200 rounded-lg font-bold hover:bg-emerald-50 transition-colors flex items-center whitespace-nowrap text-[11px]\",children:[v.jsx(ke,{icon:AS,className:\"mr-2\"}),\"Pinnable\"]}),v.jsx(zFarbLeiste,{}),",
 "Die Farbleiste in die Werkzeugzeile, also direkt ueber dem Raster", 1))

# 232  Screenshot-Folie: der Abstand zur Hookzeile
#
#      "Zuviel Abstand."
#
#      Die Hookzeile stand fest bei n*.10, und der Screenshot wurde in
#      der RESTFLAECHE darunter zentriert:
#          zOben = n*.10 + Hoehe der Zeile + n*.045
#          Qt    = zOben + zH/2        mit zH bis n*.865
#      Bei einem kleinen Screenshot - eine kurze Sprechblase - klafft
#      dadurch ein Loch von einem Drittel der Kachel zwischen Zeile
#      und Bild. Je kleiner der Screenshot, desto groesser das Loch.
#
#      Jetzt werden Zeile und Bild als EINE GRUPPE mittig gesetzt:
#      Gesamthoehe = Zeilenhoehe + ssLuft + Bildhoehe, davon die Mitte
#      auf die Mitte des Bandes [.10, .865] gelegt, und die Zeile wird
#      nachtraeglich dorthin geschoben. Dafuer musste zTb ueber zTbO
#      aus dem if-Block heraus sichtbar werden.
#
#      Passt auch bei grossen Screenshots: zTop ist nach unten auf
#      zU-zGes geklemmt, das Bild laeuft also nie unter n*.865.
#
#      GEPRUEFT im Browser, gleiche Folie mit kurzer Sprechblase:
#          karten293  Zeile oben, Bild in der Mitte, Loch dazwischen
#          karten294  Zeile und Bild zusammen, gemeinsam mittig
#      keine Seitenfehler. ssLuft .035 regelt den Abstand.

P.append((
 "let zOben=n*.115;if(zHk){const zTb=new Pe.fabric.Textbox(zHk,{left:r/2,top:n*.10,",
 "let zOben=n*.115,zTbO=null;if(zHk){const zTb=new Pe.fabric.Textbox(zHk,{left:r/2,top:n*.10,",
 "Die Hookzeile merken, damit sie nachher mitwandern kann", 1))

P.append((
 "e.add(zTb),zOben=n*.10+zTb.height+n*.045}",
 "e.add(zTb),zTbO=zTb,zOben=n*.10+zTb.height+n*.045}",
 "Dasselbe - die Zeile festhalten", 1))

P.append((
 "Qt=zOben+zH/2+(typeof t.overlayImageY==\"number\"?t.overlayImageY:0)*d;",
 "Qt=(()=>{try{const zG=n*(Number(BS_KACHEL.ssLuft)||.035),zHh=zTbO?zTbO.height:0,zBox=wt+Wt*2,zGes=zHh+(zHh?zG:0)+zBox,zO=n*.10,zU=n*.865,zTop=Math.max(zO,Math.min((zO+zU)/2-zGes/2,zU-zGes));if(zTbO)zTbO.set({top:zTop});return zTop+zHh+(zHh?zG:0)+zBox/2}catch(zz){return zOben+zH/2}})()+(typeof t.overlayImageY==\"number\"?t.overlayImageY:0)*d;",
 "Hook und Screenshot als eine Gruppe mittig setzen statt den Screenshot in der Restflaeche", 1))

P.append((
 "kastenAn:0,layoutAn:0",
 "kastenAn:0,ssLuft:.035,layoutAn:0",
 "Der Abstand zwischen Hookzeile und Screenshot", 1))

# 233  Text wirklich mittig
#
#      "Die folgeslides wie gehabt - zentriert und Playfair und
#       Handschrift gemischt."
#
#      NACHGESEHEN, bevor ich etwas anfasse: Playfair und Handschrift
#      sind bei den Folgefolien bereits gemischt, und zwar ueber zwei
#      Schluessel, die zusammenspielen:
#          folgeFamilie   "Playfair Display"  -> Hauptzeilen
#          folgeZweitHand 1                    -> QeZ faellt auf
#                                                 zweiteFamilie, also
#                                                 die Handschrift
#      Da war also nichts zu tun. Gut, dass ich erst gerendert habe.
#
#      NICHT in Ordnung war die Lage: textMitte stand auf .58, und
#      textImmerMitte===1 setzt De genau darauf. Der Block sass also
#      acht Prozent unter der Mitte - oben ein Loch, unten drueckte
#      die Handschrift fast auf den Namenszug.
#
#      .58 war mein eigener Wert aus 205, als sie "Text immer mittig,
#      nicht so weit unten" verlangt hat. Ich bin damals von .7 nur
#      bis .58 gegangen statt bis zur Mitte. Jetzt .50.
#
#      GILT FUER ALLE KACHELN, nicht nur fuer Folgefolien - eine
#      getrennte Lage fuer Deckblatt und Folge waere eine zweite
#      Wahrheit ueber dieselbe Regel gewesen.
#
#      GEPRUEFT: drei Kacheln gerendert, zwei davon byteweise gleich
#      der Probe, die dritte 17 Byte daneben - dieselbe Schwankung im
#      geblurrten Foto wie in 222. Derselbe Bundle zweimal gerendert
#      ist byteweise identisch, es liegt also nicht an der Aenderung.

P.append((
 "textMitte:.58",
 "textMitte:.50",
 "Text wirklich mittig statt auf 58 Prozent", 1))

# 234  Der Schalter wurde umgangen
#
#      "Wir haben nun wieder eine 2. Schrift als Playfair bei den
#       neuen Layouts."
#
#      Die Rotation steht seit 230 auf 0. Trotzdem landeten Kacheln im
#      Layout-Zweig, weil zLay in DIESER Reihenfolge fragte:
#
#          1. hat die Folie ein brand_-Layout?  -> nimm es
#          2. ist layoutAn 1?                   -> sonst nichts
#
#      Punkt 1 stand VOR dem Schalter. Und Folien bringen so ein
#      Layout mit: ein Normalisierungspfad stempelt
#          layout: Ve.layout || Ve.layoutId || "brand_text_plate"
#      auf jede Folie, die keins hat. Jede so normalisierte Kachel
#      ging damit am ausgeschalteten Schalter vorbei - in den
#      Layout-Zweig, wo die Schrift ueber Ct() aus
#      typography.fontFamily kommt, also Petrona, und wo es die
#      Handschriftzeile nicht gibt.
#
#      Jetzt fragt zLay zuerst den Schalter. Ein eigenes Layout an der
#      Folie zaehlt nur noch, wenn die Rotation ueberhaupt an ist.
#
#      NACHGESTELLT mit layout:"brand_text_plate" an der Folie:
#          karten295  schmale Serife, keine Handschrift, kein Foto
#          karten296  Playfair, Handschrift, Foto - wie im Feed
#
#      LEHRE: ein Schalter, der erst an zweiter Stelle gefragt wird,
#      ist kein Schalter. Beim Zurueckdrehen in 230 habe ich nur
#      geprueft, ob der Feed wieder stimmt - nicht, ob es einen Weg
#      daran vorbei gibt.

P.append((
 "zLay=(zi,zs)=>{try{const ze=zs&&zs.layout;if(ze&&String(ze).indexOf(\"brand_\")===0)return ze;if(BS_KACHEL.layoutAn!==1)return \"\";",
 "zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";const ze=zs&&zs.layout;if(ze&&String(ze).indexOf(\"brand_\")===0)return ze;",
 "Erst den Schalter fragen, dann das Layout an der Folie", 1))

# 235  Die zwei gerahmten Varianten
#
#      "Ja bau die zwei Rahmen."
#
#      NICHT ueber die Layout-Tabelle, sondern IM Feed-Zeichner - das
#      war die Lehre aus 229/230. Der Rahmen ist reine ZUSATZ-
#      zeichnung; Schrift, Groessen, Lage, Handschrift und Namenszug
#      laufen unveraendert weiter. Der Fehler von damals kann hier
#      nicht passieren, weil kein anderer Zweig betreten wird.
#
#      zRah(tag) liest rahmenReihe, Vorgabe "0|0|1|0|0|2|0":
#          0  kein Rahmen
#          1  Foto gerahmt - ein Rand in Kachelfarbe ueber die
#             Bildkanten, dazu die Linie. Das Bild wird nicht
#             verschoben, es wird nur beschnitten; deshalb bleibt
#             die Zuteilung der Fotos unberuehrt.
#          2  Text gerahmt - nur die Linie.
#
#      NUR DAS DECKBLATT: _rah wird nur bei ta==="deckblatt" gesetzt.
#      Die Folgefolien bleiben, wie sie sind - genau ihr Einwand von
#      vorgestern.
#
#      Im Rahmen wird die Textspalte auf rahmenSpalte .74 verengt,
#      sonst stoesst der Text an die Linie (Spalte sonst .86 bei
#      einem Rahmen bei .88 innen).
#
#      GEPRUEFT im Browser, sieben aufeinanderfolgende Tage:
#          Tag 1  unveraendert, Playfair und Handschrift
#          Tag 3  Foto gerahmt
#          Tag 6  Text gerahmt
#      keine Seitenfehler. rahmenReihe "0" schaltet alles ab.

P.append((
 "zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";",
 "zRah=zd=>{try{const zl=String(BS_KACHEL.rahmenReihe||\"\").split(\"|\").filter(zx=>zx!==\"\");if(!zl.length)return 0;return Number(zl[(Math.max(1,Number(zd)||1)-1)%zl.length])||0}catch(zz){return 0}},zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";",
 "zRah: welche Rahmenfassung ein Tag bekommt, 0 keine, 1 Foto, 2 Text", 1))

P.append((
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0,",
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0,_rah:(ta===\"deckblatt\"?zRah(ot.day):0),",
 "Nur das Deckblatt bekommt einen Rahmen - die Folgefolien bleiben unberuehrt", 1))

P.append((
 "const $e=!!t.background;let qe=t.sizeLocked&&typeof t.fontSize==\"number\"",
 "const $e=!!t.background;(()=>{try{const zR=Number(t._rah)||0;if(!zR)return;const zM=r*(Number(BS_KACHEL.rahmenRand)||.06),zLn=Math.max(1,r*(Number(BS_KACHEL.rahmenLinie)||.0045));if(zR===1){const zG=BS_KACHEL.rahmenGrund||\"#0C0C0D\";[[0,0,r,zM],[0,n-zM,r,zM],[0,0,zM,n],[r-zM,0,zM,n]].forEach(zb=>e.add(new Pe.fabric.Rect({left:zb[0],top:zb[1],width:zb[2],height:zb[3],fill:zG,selectable:!1,evented:!1})))}e.add(new Pe.fabric.Rect({left:zM+zLn/2,top:zM+zLn/2,width:Math.max(1,r-2*zM-zLn),height:Math.max(1,n-2*zM-zLn),fill:\"transparent\",stroke:BS_KACHEL.rahmenFarbe||\"#F6F1E6\",strokeWidth:zLn,opacity:(BS_KACHEL.rahmenDeckkraft==null?.5:Number(BS_KACHEL.rahmenDeckkraft)),selectable:!1,evented:!1}))}catch(zz){}})();let qe=t.sizeLocked&&typeof t.fontSize==\"number\"",
 "Den Rahmen zeichnen: bei 1 zusaetzlich ein Rand in Kachelfarbe ueber die Bildkanten", 1))

P.append((
 "Qt=r*(zKa&&BS_KACHEL.kastenSpalte?Number(BS_KACHEL.kastenSpalte):zbr)-(tt.polsterX||0)*2",
 "Qt=r*(zKa&&BS_KACHEL.kastenSpalte?Number(BS_KACHEL.kastenSpalte):(t._rah&&BS_KACHEL.rahmenSpalte?Number(BS_KACHEL.rahmenSpalte):zbr))-(tt.polsterX||0)*2",
 "Im Rahmen eine schmalere Spalte, damit der Text nicht an die Linie stoesst", 1))

P.append((
 "kastenAn:0,ssLuft:.035",
 "kastenAn:0,rahmenReihe:\"0|0|1|0|0|2|0\",rahmenRand:.06,rahmenLinie:.0045,rahmenSpalte:.74,rahmenFarbe:\"#F6F1E6\",rahmenDeckkraft:.5,rahmenGrund:\"#0C0C0D\",ssLuft:.035",
 "Die Rahmenreihe und ihre Masse", 1))

# 236  Die vier Varianten aufeinander ausgerichtet
#
#      "Welche 4 Layout baust du nun?"
#
#      Beim Beantworten nachgerechnet - und dabei gemerkt, dass eine
#      der vier gar nicht vorkam.
#
#      ZWEI RHYTHMEN, die nichts voneinander wussten:
#          textJede 7     -> (ut%7)!==0 heisst Foto. Also sind die
#                            Tage 1, 8, 15 die reinen Textkacheln.
#          rahmenReihe    -> greift ueber (tag-1)%7, derselbe Takt.
#
#      Mit "0|0|1|0|0|2|0" lag die 2 auf Position 5, also auf Tag 6 -
#      einem FOTO-Tag. "Text gerahmt" war damit nie ein gerahmter
#      Textslide, sondern ein zweites gerahmtes Foto. Und die
#      Textkachel auf Position 0 bekam nie einen Rahmen.
#
#      Jetzt "2|0|1|0|0|0|0": die 2 auf Position 0, also genau auf
#      den Textkacheltag. Die 1 bleibt auf Position 2, einem Fototag.
#
#      DAMIT STEHEN DIE VIER:
#          Tag 1, 8, 15   Text gerahmt   (Textkachel + Linie)
#          Tag 3, 10, 17  Foto gerahmt
#          Tag 2,4,5,...  Foto mit Text  (der Standard)
#          - reine Textkachel ohne Rahmen kommt nicht mehr vor,
#            weil Position 0 jetzt belegt ist. Wer sie zurueck will,
#            nimmt textJede auf 5 oder die Reihe auf 14 Stellen.
#
#      MERKE: die beiden Reihen teilen denselben Takt 7. Aendert man
#      textJede, verschiebt sich, worauf die Rahmen fallen.

P.append((
 "rahmenReihe:\"0|0|1|0|0|2|0\"",
 "rahmenReihe:\"2|0|1|0|0|0|0\"",
 "Text gerahmt auf den Textkacheltag legen, Foto gerahmt auf einen Fototag", 1))

# 237  Die Rahmen waren bei Rastergroesse unsichtbar
#
#      "Ich seh nicht viel davon."
#
#      Stimmt, und der Grund ist ein Massstabsfehler von mir. Alle
#      Rahmenmasse haengen an der Kachelbreite r, und geprueft habe
#      ich an EINZELNEN Kacheln von 565 Pixeln. Dort war
#      rahmenLinie .0045 eine feine Linie. Im Raster ist eine Kachel
#      auf dem Handy aber nur rund 120 Pixel breit - dieselbe Linie
#      ist dort unter einem Pixel, und bei Deckkraft .5 verschwindet
#      sie ganz.
#
#      Dazu kam: rahmenGrund #0C0C0D auf einem dunklen Foto ist
#      derselbe Ton. Der Rand des gerahmten Fotos war also auch nicht
#      zu sehen.
#
#      Jetzt: Linie .0045 -> .014, Deckkraft .5 -> 1, Rand .06 ->
#      .09, Spalte .74 -> .72.
#
#      GEPRUEFT: diesmal NICHT an einer Einzelkachel, sondern am
#      Raster bei 402 Pixeln Breite mit dreifacher Aufloesung, also
#      so, wie sie es am Telefon sieht. Zwei Staerken gerendert und
#      verglichen; die leisere (.075/.009/.85) liegt als s1 in der
#      Geschichte, falls es zu viel ist.
#
#      MERKE: Kachelmasse am RASTER pruefen, nicht an der Einzel-
#      kachel. Was bei 565 Pixeln fein wirkt, ist bei 120 nicht da.

P.append((
 "rahmenRand:.06,rahmenLinie:.0045,rahmenSpalte:.74,rahmenFarbe:\"#F6F1E6\",rahmenDeckkraft:.5",
 "rahmenRand:.09,rahmenLinie:.014,rahmenSpalte:.72,rahmenFarbe:\"#F6F1E6\",rahmenDeckkraft:1",
 "Rahmen kraeftiger - bei Rastergroesse war die Haarlinie unsichtbar", 1))

# 238  Die Layouts zurueck - diesmal nur auf dem Deckblatt
#
#      "Du hattest es vorher bei der falschen Petrona-Schrift
#       besser" - "geh zurueck zu der Art vor der Umstellung zurueck
#       auf Playfair, mit den Layouts."
#
#      Also layoutAn wieder 1. Aber NICHT so wie in 229: ihr Einwand
#      von damals war berechtigt und bleibt eingebaut.
#
#      ZWEI UNTERSCHIEDE ZU 229:
#        1. Gewaehlt wird nach TAG, nicht nach Folienindex. Ein
#           Karussell haette sonst pro Folie ein anderes Layout.
#        2. Nur das Deckblatt bekommt ueberhaupt eins. Folgefolien
#           rufen zLay mit -1, und zLay gibt bei negativem Index
#           sofort "" zurueck - VOR der Abfrage des Layouts an der
#           Folie. Sonst haette der brand_text_plate-Stempel aus dem
#           Normalisierer sie doch wieder hineingezogen, genau wie
#           in 234.
#
#      BELEGT, nicht vermutet: die Eigenschaften je Folie eines
#      Karussells protokolliert -
#          Folie 1  deckblatt  layout brand_photo_bottom_left
#          Folie 2  inhalt     kein layout, textBands true
#          Folie 3  abschluss  kein layout, textBands true
#
#      WAS DAS KOSTET, auf den DECKBLAETTERN: Playfair weicht Petrona
#      (der Layout-Zweig holt die Schrift aus typography.fontFamily),
#      und die Handschriftzeile gibt es dort nicht. Genau das hat ihr
#      besser gefallen. Auf den Folgefolien bleibt beides.
#
#      Die Rahmen aus 235-237 liegen damit auf Deckblaettern brach -
#      sie werden im Feed-Zweig gezeichnet, den ein Deckblatt jetzt
#      nicht mehr betritt. Der Layoutsatz hat eigene gerahmte
#      Fassungen. Bei layoutAn 0 sind die Rahmen sofort wieder da.
#
#      FEHLVERSUCH BEIM PRUEFEN, zum Merken: ein Tag mit EINER Folie
#      taugt nicht als Test fuer Folgefolien. ta kommt aus
#      CG(index, anzahl) - bei einer einzigen Folie ist sie immer
#      "deckblatt", egal was man als folienRolle hineinschreibt.

P.append((
 "zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";const ze=zs&&zs.layout;",
 "zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";if((Number(zi)||0)<0)return \"\";const ze=zs&&zs.layout;",
 "Ein negativer Index heisst: diese Folie bekommt kein Layout", 1))

P.append((
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0,_rah:(ta===\"deckblatt\"?zRah(ot.day):0),",
 "textBands:(zLay(ta===\"deckblatt\"?ot.day:-1,rt)||ot.bandStyle===\"none\")?void 0:!0,_rah:(ta===\"deckblatt\"?zRah(ot.day):0),",
 "Layout nur auf dem Deckblatt, und nach TAG gewaehlt statt nach Folienindex", 1))

P.append((
 "layout:zLay(dt,rt)||Br,layoutId:zLay(dt,rt)||(Mt?Br:sn?\"auto\":rt.layoutId||Br),",
 "layout:zLay(ta===\"deckblatt\"?ot.day:-1,rt)||Br,layoutId:zLay(ta===\"deckblatt\"?ot.day:-1,rt)||(Mt?Br:sn?\"auto\":rt.layoutId||Br),",
 "Dasselbe an beiden Stellen des Eigenschaftsbaus", 2))

P.append((
 "layoutAn:0",
 "layoutAn:1",
 "Die Layouts wieder an", 1))

# 239  Zurueck auf den Stand von 292 - und die Folgefolien kleiner
#
#      "Mach zurueck zu Karten 292 und aendere nur, dass die
#       Folgefolien schriftmaessig kleiner sind und man die Farben
#       eben anpassen kann."
#
#      Also raus, was nach 292 an OPTIK dazugekommen ist und was sie
#      nicht bestellt hatte:
#        - die Layoutrotation aus 238 (layoutAn wieder 0)
#        - die zwei gerahmten Varianten aus 235-237 (rahmenReihe "0")
#      Beides bleibt als Code im Bundle - nur die Schalter stehen auf
#      aus. Ein Wort von ihr und sie sind wieder da.
#
#      DRIN BLEIBT, was sie nach 292 AUSDRUECKLICH verlangt hat:
#        293  die Farbleiste (genau das "Farben anpassen" hier)
#        294  die Screenshot-Gruppe mittig statt mit Luecke
#             ("Zuviel Abstand")
#        295  textMitte .50, die Folgefolien wirklich zentriert
#        296  zLay fragt den Schalter ZUERST - ohne das waere
#             layoutAn:0 wirkungslos, weil der Normalisierer jeder
#             Folie brand_text_plate anstempelt
#
#      DIE FOLGEFOLIEN KLEINER: wieder beide Hebel, sonst passiert
#      nichts. qe ist die Startgroesse, Je das Hoehenbudget. Setzt man
#      nur qe herunter, holt die Schrumpfschleife die Groesse aus dem
#      Budget zurueck - der Anteil verpufft. Dasselbe Muster wie schon
#      bei pinnAnteil und kastenAnteil.
#
#      GEMESSEN, nicht geschaetzt: eine Folie mit folienRolle
#      "inhalt" durch den Zeichner geschickt und qe protokolliert -
#          ohne folgeAnteil   qe 102.56
#          mit  folgeAnteil   qe 84.0      = -18 %
#      Das Raster zeichnet nur das Deckblatt, deshalb war dafuer eine
#      Sonde noetig statt eines Blicks aufs Bild.
#
#      Deckblaetter bleiben unberuehrt: die Bedingung fragt
#      folienRolle && folienRolle !== "deckblatt".

P.append((
 "layoutAn:1",
 "layoutAn:0",
 "Layouts wieder aus - zurueck auf den Stand von karten292", 1))

P.append((
 "rahmenReihe:\"2|0|1|0|0|0|0\"",
 "rahmenReihe:\"0\"",
 "Rahmen aus - ebenfalls nach 292 dazugekommen", 1))

P.append((
 "t.bigHeadline===!0&&BS_KACHEL.pinnAnteil&&(qe=Math.roun",
 "t.folienRolle&&t.folienRolle!==\"deckblatt\"&&BS_KACHEL.folgeAnteil&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.folgeAnteil))));t.bigHeadline===!0&&BS_KACHEL.pinnAnteil&&(qe=Math.roun",
 "Folgefolien kleiner: Startgroesse", 1))

P.append((
 "*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)*(zKa?(Number(BS_KACHEL.kastenAnteil)||.72):1)-SR;",
 "*(t.folienRolle&&t.folienRolle!==\"deckblatt\"&&BS_KACHEL.folgeAnteil?Number(BS_KACHEL.folgeAnteil):1)*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)*(zKa?(Number(BS_KACHEL.kastenAnteil)||.72):1)-SR;",
 "Und das Hoehenbudget - sonst holt die Schrumpfschleife es zurueck", 1))

P.append((
 "kastenAn:0,rahmenReihe:",
 "kastenAn:0,folgeAnteil:.82,rahmenReihe:",
 "Wie stark die Folgefolien kleiner werden", 1))

# 240  Die Layouts wieder an - auf JEDER Folie, wie bei karten291
#
#      "Nein, da waren die Layouts!??"
#
#      DER ZAHLENDREHER, zum Merken: karten291 und karten292
#      unterscheiden sich in GENAU ZWEI ZEICHEN -
#          291:  layoutAn:1
#          292:  layoutAn:0
#      (byteweise verglichen, sonst sind die Dateien identisch).
#      Sie hat "zurueck zu 292" gesagt und die Variation gemeint. 292
#      ist aber genau der Stand OHNE sie. 239 hat die Nummer befolgt
#      statt die Absicht. Bei einer genannten Versionsnummer also
#      erst nachsehen, was drinsteht, dann bauen.
#
#      Ausgewaehlt hat sie danach aus vier gerenderten Rastern:
#      291 (Layouts ueberall), 300 (nur Deckblatt), 301 (keine).
#      Ihre Wahl: 291.
#
#      Also die Einschraenkung aus 238 wieder heraus - zLay bekommt
#      den Folienindex statt "Deckblatt oder -1". Der Rest von 239
#      bleibt: Farbleiste, ssLuft, textMitte, Rahmen aus.
#
#      WAS DAS KOSTET, ehrlich notiert: mit layoutAn 1 liefert zLay
#      fuer JEDE Folie ein Layout (erst das brand_-Layout der Folie,
#      sonst eines aus layoutReihe). Damit ist textBands undefined,
#      der Feed-Zweig wird gar nicht erst betreten - und folgeAnteil
#      aus 239 laeuft ins Leere, weil qe dort gesetzt wird. Die
#      Layoutfolien zeichnen ihre Schrift ohnehin kleiner. Will sie
#      die Folgefolien AUCH innerhalb der Layouts kleiner, braucht es
#      einen eigenen Hebel im Layout-Zeichner. folgeAnteil bleibt
#      stehen, damit es bei layoutAn 0 sofort wieder greift.

P.append((
 "layoutAn:0",
 "layoutAn:1",
 "Die zwanzig Layouts wieder an - wie bei karten291", 1))

P.append((
 "textBands:(zLay(ta===\"deckblatt\"?ot.day:-1,rt)||ot.bandStyle===\"none\")?void 0:!0",
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0",
 "Layout wieder auf jeder Folie, nicht nur auf dem Deckblatt", 1))

P.append((
 "layout:zLay(ta===\"deckblatt\"?ot.day:-1,rt)||Br,layoutId:zLay(ta===\"deckblatt\"?ot.day:-1,rt)||",
 "layout:zLay(dt,rt)||Br,layoutId:zLay(dt,rt)||",
 "Dasselbe an beiden Stellen des Eigenschaftsbaus", 2))

# 241  Screenshot-Folien: zwei Zeichner haben uebereinander gemalt
#
#      "Besser aufteilen." Dazu ein Screenshot vom Handy: die Headline
#      liegt quer ueber dem kleinen Foto, darunter der weisse
#      Screenshot-Kasten, das untere Drittel leer.
#
#      URSACHE, zwei Dinge gleichzeitig - seit 240 ist layoutAn 1, und
#      zLay liefert fuer JEDE Folie ein Layout, auch fuer eine
#      Screenshot-Folie. Damit malen zwei Zweige unabhaengig
#      voneinander auf dieselbe Kachel:
#        - der Layout-Zweig ein Foto-Inlay plus die Headline
#        - der Overlay-Zweig (t.overlayIsScreenshot) den weissen
#          Kasten, mittig zwischen .10 und .865
#      Keiner der beiden weiss vom anderen. Das Ergebnis ist der
#      Ueberlapp oben und die Leere unten.
#
#      Dazu kommt: die Gruppenmitte aus 294 rechnet nur mit
#      overlayHook. Steht die Zeile stattdessen in text - weil sie im
#      Editor getippt wurde statt vom Screenshot-Setzer uebernommen -
#      kennt die Rechnung sie nicht und zentriert nur den Kasten.
#
#      ZWEI AENDERUNGEN:
#        1. zLay gibt fuer Screenshot-Folien "" zurueck. Die Abfrage
#           steht VOR dem brand_-Layout der Folie, sonst zieht der
#           Normalisierer sie doch wieder hinein (dieselbe Falle wie
#           in 234 und 296).
#        2. Im Eigenschaftsbau wandert der Text einer Screenshot-
#           Folie nach overlayHook und text wird geleert - genau das,
#           was zSsLegen beim Setzen ohnehin tut. Damit zeichnet nur
#           noch ein Zweig, und Hookzeile und Kasten stehen als eine
#           Gruppe mittig.
#
#      GEPRUEFT: Screenshot-Folie gerendert, vorher und nachher. Das
#      Raster mit den Layouts ist unveraendert - die Aenderung fasst
#      nur Folien mit overlayIsScreenshot an.
#
#      WAS DAS KOSTET: das dekorative Foto auf einer Screenshot-Folie
#      faellt weg, weil es aus dem Layout kam. Headline plus Kasten
#      auf ruhigem Grund - die Aufteilung aus 294.

P.append((
 "zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";",
 "zLay=(zi,zs)=>{try{if(BS_KACHEL.layoutAn!==1)return \"\";if(zs&&(zs.overlayIsScreenshot===!0||zs._wasScreenshot===!0))return \"\";",
 "Screenshot-Folien bekommen kein Layout", 1))

P.append((
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0,",
 "textBands:(zLay(dt,rt)||ot.bandStyle===\"none\")?void 0:!0,...(rt.overlayIsScreenshot===!0&&!String(rt.overlayHook||\"\").trim()&&String(Ir||\"\").trim()?{overlayHook:String(Ir).replace(/\\*/g,\" \").replace(/\\s+/g,\" \").trim(),text:\"\"}:{}),",
 "Headline einer Screenshot-Folie wird zur Hookzeile - sonst zeichnen zwei Zweige nebeneinander", 1))

# 242  Screenshot-Folie: Text, Foto und Screenshot untereinander
#
#      "Es haette eh gepasst, aber Screenshot und Bild und Text
#       besser aufteilen, damit sie nicht uebereinander stehen."
#
#      241 hatte das Foto geopfert, um den Ueberlapp loszuwerden. Das
#      war einer zu viel: sie will alle drei, nur ordentlich gesetzt.
#
#      Der Screenshot-Zweig zeichnet jetzt einen STAPEL und zentriert
#      ihn als Ganzes im Band .10 bis .865 -
#          Hookzeile
#          Foto (Inlay, hoechstens ssFotoAnteil der Restflaeche)
#          Screenshot-Kasten (der Rest)
#      mit ssLuft als Abstand zwischen den Teilen. Erst werden alle
#      drei Hoehen gerechnet, dann die Gesamthoehe, dann der obere
#      Rand - deshalb kann nichts mehr uebereinander liegen.
#
#      WOHER DAS FOTO KOMMT: im Eigenschaftsbau wandert das Tagesbild
#      nach zSsFoto und background wird geleert. Sonst laege dasselbe
#      Bild zusaetzlich vollflaechig darunter.
#
#      DER GRUND WURDE DABEI WEISS, und das war die eigentliche
#      Arbeit. Drei Fehlversuche, jeder mit einer Sonde widerlegt:
#        - backgroundColor setzen: kommt an, faerbt aber nichts.
#        - plateOverride setzen: kommt gar nicht erst an, wird
#          unterwegs ueberschrieben.
#        - karte "dunkel" im Eigenschaftsbau: wird ebenfalls
#          ueberschrieben, die Sonde meldet weiter karte "hell".
#      Gefaerbt wird von T1({hatFoto,karte}).grundFarbe, gemessen:
#          karte "hell"    #FFFFFF
#          karte "dunkel"  #2B211A
#      Ohne Foto greift immer der Plattenzweig. Deshalb liegt die
#      Entscheidung jetzt im Zeichner, wo t.overlayIsScreenshot
#      nachweislich ankommt, und nicht im Eigenschaftsbau. ssGrund
#      setzt den Ton danach auf Schwarz statt auf das Braun der
#      dunklen Karte.
#
#      GEPRUEFT: Screenshot-Folie gerendert, Raster mit den Layouts
#      danebengelegt - unveraendert.

P.append((
 r"""if(t.overlayIsScreenshot){const zHk=String(t.overlayHook||"").replace(/\*/g,"").trim(),zBg=String(zGrundTon||t.plateOverride||t.backgroundColor||"#000000"),zTint=w(zBg)>150?"#241C16":"#F6F1E6",zRd=r*.09,Wt=10*d;let zOben=n*.115,zTbO=null;if(zHk){const zTb=new Pe.fabric.Textbox(zHk,{left:r/2,top:n*.10,originX:"center",originY:"top",width:r-zRd*2,fontSize:Math.round(r*(BS_KACHEL.hakenAnteil||.055)),fontFamily:BS_KACHEL.deckblattFamilie||"Playfair Display",fontWeight:"400",fill:zTint,textAlign:"center",lineHeight:1.18,selectable:!1,evented:!1});for(let zi=0;zi<4&&zTb.height>n*.30;zi+=1)zTb.set({fontSize:Math.round(zTb.fontSize*.88)});e.add(zTb),zTbO=zTb,zOben=n*.10+zTb.height+n*.045}const zUnten=n*.865,zH=Math.max(n*.24,zUnten-zOben),zF=typeof t.overlayImageScale=="number"?Math.max(.3,Math.min(1,t.overlayImageScale/.8)):1,et=Math.min((r-zRd*2-Wt*2)/me.width,(zH-Wt*2)/me.height)*zF,lt=me.width*et,wt=me.height*et,tt=r/2+(typeof t.overlayImageX=="number"?t.overlayImageX:0)*d,Qt=(()=>{try{const zG=n*(Number(BS_KACHEL.ssLuft)||.035),zHh=zTbO?zTbO.height:0,zBox=wt+Wt*2,zGes=zHh+(zHh?zG:0)+zBox,zO=n*.10,zU=n*.865,zTop=Math.max(zO,Math.min((zO+zU)/2-zGes/2,zU-zGes));if(zTbO)zTbO.set({top:zTop});return zTop+zHh+(zHh?zG:0)+zBox/2}catch(zz){return zOben+zH/2}})()+(typeof t.overlayImageY=="number"?t.overlayImageY:0)*d;e.add(new Pe.fabric.Rect({left:tt,top:Qt,originX:"center",originY:"center",width:lt+Wt*2,height:wt+Wt*2,rx:12*d,ry:12*d,fill:F,selectable:!1,shadow:"rgba(0,0,0,0.22) 0px 10px 30px"})),me.set({originX:"center",originY:"center",left:tt,top:Qt,scaleX:et,scaleY:et,selectable:!1,clipPath:new Pe.fabric.Rect({width:me.width,height:me.height,rx:6/et,ry:6/et,originX:"center",originY:"center"})}),e.add(me),Fe(!0);return}""",
 r"""if(t.overlayIsScreenshot){const zHk=String(t.overlayHook||"").replace(/\*/g,"").trim(),zBg=String(zGrundTon||t.plateOverride||t.backgroundColor||"#000000"),zTint=w(zBg)>150?"#241C16":"#F6F1E6",zRd=r*.09,Wt=10*d,zO=n*.10,zU=n*.865,zG=n*(Number(BS_KACHEL.ssLuft)||.035),zBr=r-zRd*2;const zSetz=zFo=>{try{let zTbO=null,zHh=0;if(zHk){const zTb=new Pe.fabric.Textbox(zHk,{left:r/2,top:zO,originX:"center",originY:"top",width:zBr,fontSize:Math.round(r*(BS_KACHEL.hakenAnteil||.055)),fontFamily:BS_KACHEL.deckblattFamilie||"Playfair Display",fontWeight:"400",fill:zTint,textAlign:"center",lineHeight:1.18,selectable:!1,evented:!1});for(let zi=0;zi<4&&zTb.height>n*.26;zi+=1)zTb.set({fontSize:Math.round(zTb.fontSize*.88)});zTbO=zTb,zHh=zTb.height}const zRest=Math.max(n*.24,zU-zO-zHh-zG*(zFo?2:zHh?1:0));const zFoMax=zFo?zRest*(Number(BS_KACHEL.ssFotoAnteil)||.42):0;let zFs=0,zFh=0;if(zFo){zFs=Math.min(zBr/zFo.width,zFoMax/zFo.height),zFh=zFo.height*zFs}const zBoxMax=Math.max(n*.12,zRest-zFh),zF=typeof t.overlayImageScale=="number"?Math.max(.3,Math.min(1,t.overlayImageScale/.8)):1,et=Math.min((zBr-Wt*2)/me.width,(zBoxMax-Wt*2)/me.height)*zF,lt=me.width*et,wt=me.height*et,zBox=wt+Wt*2,zGes=zHh+(zHh?zG:0)+zFh+(zFh?zG:0)+zBox;let zTop=Math.max(zO,Math.min((zO+zU)/2-zGes/2,zU-zGes));if(zTbO)zTbO.set({top:zTop}),e.add(zTbO),zTop+=zHh+zG;const tt=r/2+(typeof t.overlayImageX=="number"?t.overlayImageX:0)*d;if(zFo)zFo.set({originX:"center",originY:"top",left:r/2,top:zTop,scaleX:zFs,scaleY:zFs,selectable:!1,evented:!1,clipPath:new Pe.fabric.Rect({width:zFo.width,height:zFo.height,rx:10/zFs,ry:10/zFs,originX:"center",originY:"center"})}),e.add(zFo),zTop+=zFh+zG;const Qt=zTop+zBox/2+(typeof t.overlayImageY=="number"?t.overlayImageY:0)*d;e.add(new Pe.fabric.Rect({left:tt,top:Qt,originX:"center",originY:"center",width:lt+Wt*2,height:wt+Wt*2,rx:12*d,ry:12*d,fill:F,selectable:!1,shadow:"rgba(0,0,0,0.22) 0px 10px 30px"})),me.set({originX:"center",originY:"center",left:tt,top:Qt,scaleX:et,scaleY:et,selectable:!1,clipPath:new Pe.fabric.Rect({width:me.width,height:me.height,rx:6/et,ry:6/et,originX:"center",originY:"center"})}),e.add(me),Fe(!0)}catch(zz){Fe(!1)}};const zFot=String(t.zSsFoto||"");if(zFot.length>5)try{Pe.fabric.Image.fromURL(zFot,zi=>zSetz(zi&&zi.width>0?zi:null),{crossOrigin:"anonymous"})}catch(zz){zSetz(null)}else zSetz(null);return}""",
 'Screenshot-Folie als Stapel: Hookzeile, Foto, Kasten - als Gruppe mittig', 1))

P.append((
 r"""...(rt.overlayIsScreenshot===!0&&!String(rt.overlayHook||"").trim()&&String(Ir||"").trim()?{overlayHook:String(Ir).replace(/\*/g," ").replace(/\s+/g," ").trim(),text:""}:{}),""",
 r"""...(rt.overlayIsScreenshot===!0&&!String(rt.overlayHook||"").trim()&&String(Ir||"").trim()?{overlayHook:String(Ir).replace(/\*/g," ").replace(/\s+/g," ").trim(),text:""}:{}),...(rt.overlayIsScreenshot===!0?{zSsFoto:((e.tagBilder||{})[ot.day]||rt.background||""),background:"",karte:"dunkel"}:{}),""",
 'Das Tagesbild wandert nach zSsFoto, damit es nicht doppelt liegt', 1))

P.append((
 r"""ssLuft:.035,""",
 r"""ssLuft:.035,ssFotoAnteil:.42,ssGrund:"#141210",""",
 'Wie viel Hoehe das Foto bekommt, und der Grundton', 1))

P.append((
 r"""Ye=T1({hatFoto:$e,karte:t.karte||"dunkel"})""",
 r"""Ye=(()=>{const zY=T1({hatFoto:$e,karte:t.overlayIsScreenshot===!0?"dunkel":t.karte||"dunkel"});try{if(t.overlayIsScreenshot===!0&&BS_KACHEL.ssGrund)zY.grundFarbe=String(BS_KACHEL.ssGrund)}catch(zz){}return zY})()""",
 'Der Grund der Screenshot-Folie wird im Zeichner entschieden, nicht im Eigenschaftsbau', 1))

# 243  Foto auf der Screenshot-Folie groesser und zugeschnitten
#
#      "Foto groesser und lieber zugeschnitten, also das war nicht
#       schlecht vorher."
#
#      242 hat das Foto EINGEPASST (Math.min) - es wurde also so
#      klein, dass es ganz hineinpasste, und liess seitlich Luft.
#      Jetzt wird es FORMATFUELLEND skaliert (Math.max) und der
#      Ueberstand weggeschnitten: volle Spaltenbreite, Hoehe nach
#      Mass, Ausschnitt mittig ueber einen clipPath.
#
#      Der Unterschied steckt in zwei Zeichen:
#          Math.min -> einpassen, Raender bleiben frei
#          Math.max -> fuellen, Ueberstand wird abgeschnitten
#      Dazu muss der clipPath die ZIELmasse bekommen (zFw/zFs mal
#      zFh/zFs), nicht die Bildmasse - sonst schneidet er nichts ab.
#      Und das Bild haengt an originY "center" mit top zTop+zFh/2,
#      weil der clipPath um den Objektmittelpunkt herum rechnet.
#
#      ssFotoAnteil von .42 auf .52: das Foto bekommt gut die Haelfte
#      der Flaeche, die nach der Hookzeile uebrig ist. ssFotoBreite
#      ist der Anteil der Spaltenbreite, 1 heisst ganze Breite.
#
#      GEPRUEFT: Folie gerendert. Raster Pixel fuer Pixel gegen 304
#      gehalten - Unterschied nur die letzte Ziffer im Versionsschild
#      und 15 Pixel mit hoechstens 8 von 255 Helligkeitsunterschied
#      im Weichzeichner. Zwei Laeufe desselben Bundles sind
#      identisch, das Rendern ist also verlaesslich.

P.append((
 "let zFs=0,zFh=0;if(zFo){zFs=Math.min(zBr/zFo.width,zFoMax/zFo.height),zFh=zFo.height*zFs}",
 "let zFs=0,zFh=0,zFw=0;if(zFo){zFw=zBr*(Number(BS_KACHEL.ssFotoBreite)||1),zFh=zFoMax,zFs=Math.max(zFw/zFo.width,zFh/zFo.height)}",
 "Foto wird formatfuellend skaliert statt eingepasst", 1))

P.append((
 'if(zFo)zFo.set({originX:"center",originY:"top",left:r/2,top:zTop,scaleX:zFs,scaleY:zFs,selectable:!1,evented:!1,clipPath:new Pe.fabric.Rect({width:zFo.width,height:zFo.height,rx:10/zFs,ry:10/zFs,originX:"center",originY:"center"})}),e.add(zFo),zTop+=zFh+zG;',
 'if(zFo)zFo.set({originX:"center",originY:"center",left:r/2,top:zTop+zFh/2,scaleX:zFs,scaleY:zFs,selectable:!1,evented:!1,clipPath:new Pe.fabric.Rect({width:zFw/zFs,height:zFh/zFs,rx:10/zFs,ry:10/zFs,originX:"center",originY:"center"})}),e.add(zFo),zTop+=zFh+zG;',
 "Ausschnitt mittig, auf die Zielmasse beschnitten", 1))

P.append((
 "ssFotoAnteil:.42,",
 "ssFotoAnteil:.52,ssFotoBreite:1,",
 "Foto groesser: gut die Haelfte der Restflaeche, volle Spaltenbreite", 1))

# 244  Das Foto wieder halbbreit - die Aufteilung von 302, ohne Ueberlapp
#
#      "Nein, so wie das, nur Abstaende besser." Dazu nochmal ihr
#      Screenshot von karten302.
#
#      Sie wollte also NICHT das Foto ueber die ganze Spalte (das war
#      243), sondern die Anordnung, die sie auf dem alten Bild sah:
#      ein halbbreites Inlay, Text darueber, Screenshot darunter.
#      Kaputt war daran nur, dass die Zeile auf dem Foto lag.
#
#      Genau das ist seit 242 geloest - der Stapel wird als Ganzes
#      gerechnet. Es fehlte nur die Breite. ssFotoBreite von 1 auf
#      .52 zurueck.
#
#      NACHGEMESSEN an ihrem Screenshot: das Foto lief dort von x 245
#      bis 670 bei 920 Bildbreite, also 46 Prozent, und war etwa 31
#      Prozent der Kachelhoehe hoch. Mit ssFotoBreite .52 und
#      ssFotoAnteil .52 kommt der Zeichner auf dieselbe Groessen-
#      ordnung - deshalb diese zwei Werte und nicht geschaetzte.

P.append((
 "ssFotoAnteil:.52,ssFotoBreite:1,",
 "ssFotoAnteil:.52,ssFotoBreite:.52,",
 "Foto halbbreit als Inlay statt ueber die ganze Spalte", 1))

# 245  Zwei Woerter der Hookzeile in Beere
#
#      "Vielleicht machst du bei der Hook immer 2 Woerter so magenta
#       berry?"
#
#      Die Farbe ist nicht neu erfunden: #B03A5B ist ihr eigener
#      Beerenton, der schon als kastenFarbe in der Konfiguration
#      steht. Damit bleibt es eine Marke und keine zweite.
#
#      GEMACHT ueber fabric-Textstile, nicht ueber zwei Textboxen.
#      Eine Textbox traegt styles[Zeile][Zeichen] - und zwar auf den
#      UNGEBROCHENEN Text bezogen, nicht auf die umbrochenen Zeilen.
#      Die Hookzeile hat kein \n, also ist alles Zeile 0 und der
#      Zeichenindex laeuft durch den ganzen Satz. Deshalb reicht ein
#      Bereich von zVon bis zBis, egal wo fabric spaeter umbricht.
#      Zwei getrennte Textboxen haetten den Umbruch zerschossen.
#
#      Die Stile werden VOR der Schrumpfschleife gesetzt und
#      ueberleben sie - set({fontSize}) fasst styles nicht an.
#
#      DREI STELLSCHRAUBEN:
#        hakenAkzentFarbe   leer heisst aus
#        hakenAkzent        "ende" (Vorgabe) oder "anfang"
#        hakenAkzentWoerter wie viele Woerter, Vorgabe 2
#      Bei bis zu zwei Woertern passiert nichts - sonst waere die
#      ganze Zeile farbig.

P.append((
 "for(let zi=0;zi<4&&zTb.height>n*.26;zi+=1)zTb.set({fontSize:Math.round(zTb.fontSize*.88)});",
 "try{const zAk=String(BS_KACHEL.hakenAkzentFarbe||\"\").trim(),zAnz=Number(BS_KACHEL.hakenAkzentWoerter)||2;if(zAk&&zHk.indexOf(\" \")>0){const zW=zHk.split(/\\s+/);if(zW.length>zAnz){const zEnde=BS_KACHEL.hakenAkzent!==\"anfang\",zTeil=zEnde?zW.slice(-zAnz).join(\" \"):zW.slice(0,zAnz).join(\" \"),zVon=zEnde?zHk.length-zTeil.length:0,zBis=zVon+zTeil.length,zSt={};for(let zi=zVon;zi<zBis;zi+=1)zSt[zi]={fill:zAk};zTb.set({styles:{0:zSt}})}}}catch(zz){}for(let zi=0;zi<4&&zTb.height>n*.26;zi+=1)zTb.set({fontSize:Math.round(zTb.fontSize*.88)});",
 "Zwei Woerter der Hookzeile bekommen den Beerenton", 1))

P.append((
 "ssFotoAnteil:.52,ssFotoBreite:.52,",
 "ssFotoAnteil:.52,ssFotoBreite:.52,hakenAkzentFarbe:\"#B03A5B\",hakenAkzent:\"ende\",hakenAkzentWoerter:2,",
 "Farbe, Seite und Anzahl der betonten Woerter", 1))

# 246  Das Beere heller
#
#      "Heller das Berry."
#
#      hakenAkzentFarbe von #B03A5B auf #D6467A. Auf dem fast
#      schwarzen Grund der Screenshot-Folie stand der dunkle Beerenton
#      zu nah am Umfeld - der hellere setzt sich ab, ohne bunt zu
#      werden.
#
#      Beide Toene lagen ihr gerendert vor, sie hat den helleren
#      gewaehlt. kastenFarbe bleibt unveraendert bei #B03A5B, das ist
#      ein anderer Ort.

P.append((
 'hakenAkzentFarbe:"#B03A5B",',
 'hakenAkzentFarbe:"#D6467A",',
 "Der Beerenton der zwei betonten Woerter wird heller", 1))

# 247  Die betonten Woerter in Hellgelb
#
#      "Vielleicht besser in hellgelb."
#
#      hakenAkzentFarbe von #D6467A auf #F3E5AB - und das ist kein
#      neuer Ton: dieses Vanillegelb steckt schon als fest
#      verdrahtetes wa="#F3E5AB" im Bundle, mit dem die App
#      Markierungen setzt. Also wieder eine Farbwelt statt einer
#      zweiten.
#
#      IHR GESAGT, weil es an der Sache liegt und nicht am Geschmack:
#      die Hookzeile steht in Knochenweiss (#F6F1E6). Hellgelb liegt
#      so nah daran, dass die Betonung auf dem Handy kaum auffaellt.
#      Zwei kraeftigere Gelbtoene (#F0CE5A, #E8B93C) lagen ihr
#      gerendert daneben vor. Gebaut ist, was sie verlangt hat.

P.append((
 'hakenAkzentFarbe:"#D6467A",',
 'hakenAkzentFarbe:"#F3E5AB",',
 "Die zwei betonten Woerter in Hellgelb statt Beere", 1))

# 248  Petrona gegen Playfair getauscht - in den Layouts
#
#      "Die Folgeslides sind wieder falsch und du nutzt wieder Prato
#       oder wie die Schrift heisst." Dann, nach meinem Vorschlag,
#       die Layouts aufs Deckblatt zu beschraenken: "Nein, lass es
#       wie es ist und hole nur Playfair fuer den Austausch mit
#       Prato."
#
#      Also NICHT die Rotation einschraenken. Nur die Schrift.
#
#      DER TAUSCH ALLEIN REICHT NICHT, und das war der eigentliche
#      Fund. Setzt man die Familie auf Playfair, laufen die Zeilen
#      ineinander und die Woerter kleben zusammen. Zwei Stellen im
#      Layout-Zweig sind daran schuld:
#
#        Un()  prueft /playfair/i auf der Familie und setzt dann die
#              Zeilenhoehe um -.34 herunter. Das ist fuer die grosse
#              Deckblattzeile im Feed-Zweig gedacht, nicht fuer die
#              kleine Layoutschrift.
#        Fr()  misst ueber Rt() die optischen Seitenraender der
#              Schrift mit measureText und leitet daraus eine
#              NEGATIVE Laufweite ab. Bei Playfair faellt diese
#              Rechnung so scharf aus, dass die Wortabstaende
#              verschwinden.
#
#      BELEGT durch einen Vergleich mit drei Ersatzschriften:
#          Lora              sauber
#          Fraunces          sauber
#          Playfair Display  zusammengequetscht
#      Es liegt also nicht am Tausch an sich, sondern an diesen zwei
#      Playfair-Sonderfaellen. Beide werden jetzt uebersprungen, wenn
#      die Folie den Tausch traegt (t._petronaTausch). Wo Playfair
#      echt konfiguriert ist, bleiben sie unveraendert.
#
#      petronaErsatz steuert das Ganze - leer heisst: alles bleibt
#      bei Petrona.

P.append((
 r"""const zPal=(()=>{try{return(typeof window<"u"&&window.BS_PALETTE)||{}}catch(zz){return{}}})();""",
 r"""const zPal=(()=>{try{return(typeof window<"u"&&window.BS_PALETTE)||{}}catch(zz){return{}}})();try{const zEr=String(BS_KACHEL.petronaErsatz||"");if(zEr&&t&&/Petrona/.test(String(t.fontFamily||"")))t.fontFamily=zEr,t._petronaTausch=!0}catch(zz){}""",
 'Petrona wird durch die Ersatzschrift getauscht', 1))

P.append((
 r"""Un=()=>/playfair/i.test(String(t.fontFamily||"")),""",
 r"""Un=()=>t._petronaTausch!==!0&&/playfair/i.test(String(t.fontFamily||"")),""",
 'Die Playfair-Zeilenhoehe des Feed-Zweigs gilt nicht fuer getauschte Layouts', 1))

P.append((
 r"""Fr=(ge,Fe,me)=>{const $e=Rt(Fe||"HelveticaNeueBrand",me||"400",ge);if(!$e)return 0;""",
 r"""Fr=(ge,Fe,me)=>{if(t._petronaTausch===!0&&String(Fe||"")===String(BS_KACHEL.petronaErsatz||""))return 0;const $e=Rt(Fe||"HelveticaNeueBrand",me||"400",ge);if(!$e)return 0;""",
 'Keine optische Laufweitenkorrektur fuer die getauschte Schrift', 1))

P.append((
 r"""hakenAkzentFarbe:"#F3E5AB",""",
 r"""hakenAkzentFarbe:"#F3E5AB",petronaErsatz:"Playfair Display",""",
 'Welche Schrift Petrona ersetzt', 1))

# 249  Die Folgefolien holten sich die Fliesstextschrift
#
#      "Aber Layouts auch auf den Folgefolien."
#
#      Sie HATTEN welche. Nachgestellt mit einem Karussell aus drei
#      Folien und dem Vorschaufenster abfotografiert:
#          Folie 1  Playfair, mittig      - Layout, Tausch griff
#          Folie 2  fette Grotesk, unten links - Layout, Tausch griff NICHT
#      Es fehlte also nicht das Layout, sondern die Schrift. Ohne
#      dieses Bild haette ich weiter an der Rotation gedreht.
#
#      GRUND: im Eigenschaftsbau steht
#          Tt = ct || (Ve===0 ? He.fontFamily||Vt : He.bodyFontFamily||"Montserrat")
#      Nur die ERSTE Folie bekommt die Headline-Schrift. Alle
#      weiteren bekommen die Fliesstextschrift - und die ist keine
#      Petrona, also lief der Tausch aus 248 an ihnen vorbei.
#
#      Die Bedingung fasst jetzt auch Layoutfolien, deren Familie
#      nicht Petrona ist. Ausgenommen bleibt eine ausdruecklich
#      gewaehlte Headline-Schrift (headlineFontChosen) - wer im
#      Editor eine Schrift setzt, behaelt sie.
#
#      GEPRUEFT: Karussell neu gerendert, alle drei Folien in
#      Playfair mit jeweils eigenem Layout. Das Raster unterscheidet
#      sich nur in den Zeilen des Versionsschilds.

P.append((
 r"""try{const zEr=String(BS_KACHEL.petronaErsatz||"");if(zEr&&t&&/Petrona/.test(String(t.fontFamily||"")))t.fontFamily=zEr,t._petronaTausch=!0}catch(zz){}""",
 r"""try{const zEr=String(BS_KACHEL.petronaErsatz||"");if(zEr&&t){const zLay=String(t.layout||"").indexOf("brand_")===0,zPet=/Petrona/.test(String(t.fontFamily||""));if(zPet||zLay&&t.headlineFontChosen!==!0&&String(t.fontFamily||"")!==zEr)t.fontFamily=zEr,t._petronaTausch=!0}}catch(zz){}""",
 'Auch Folgefolien im Layout bekommen die Headline-Schrift statt der Fliesstextschrift', 1))

# 250  Sandton statt Schwarz - und vier widerlegte Hebel davor
#
#      "Versuche statt schwarz mal die" - dazu ein Foto von nassem
#      Sand mit Schaum.
#
#      VIER HEBEL PROBIERT UND JEDEN GEMESSEN WIDERLEGT, bevor der
#      richtige gefunden war. Der Mittelwert der Kachelflaeche ist
#      jeweils ueber das halbe Raster gerechnet:
#          tonReihe / tonNeutral braun      45,42,39 -> 46,42,39
#          waerme bis .55, Ton aus dem Bild 45,42,39 -> 46,42,39
#          tiefeOben/Mitte/Unten eingeschaltet, braun
#                                           45,42,39 -> 46,42,39
#          Rottest auf rgba(${dr},0.32) im Layoutzweig: kein Rot
#      Ein Punkt Unterschied ist nichts. Diese Regler gehoeren zum
#      FEED-Zweig - und seit die Layouts auf allen Folien laufen,
#      betritt kaum eine Kachel diesen Zweig noch. Sie liefen ins
#      Leere.
#
#      DER TESTFEHLER, der das lange verdeckt hat: mein Testbild war
#      selbst fast schwarz. Damit laesst sich kein Farbton
#      beurteilen. Erst mit einem neutralen Graubild (/tmp/an/grau.b64,
#      selbst erzeugt) wurde sichtbar, was die Kacheln wirklich
#      schwarz macht: nicht ein Farbregler, sondern
#      t.backgroundColor - reines #000000 - als Grund unter dem
#      Foto-Inlay.
#
#      Also wird genau der getauscht: Gruende, deren Helligkeit unter
#      46 liegt, bekommen sandGrund. Die Schwelle laesst helle
#      Karten unberuehrt. Gemessen am Grund von Tag 9:
#          vorher  0,0,0
#          nachher 58,36,23
#
#      Was das NICHT aendert: Kacheln mit vollflaechigem Foto. Deren
#      Ton kommt aus dem Bild selbst. Wer die warm haben will,
#      braucht warme Fotos oder einen echten Farbschleier darueber -
#      das waere eine eigene Arbeit.

P.append((
 r"""const zPal=(()=>{try{return(typeof window<"u"&&window.BS_PALETTE)||{}}catch(zz){return{}}})();""",
 r"""const zPal=(()=>{try{return(typeof window<"u"&&window.BS_PALETTE)||{}}catch(zz){return{}}})();try{const zSd=String(BS_KACHEL.sandGrund||"");if(zSd&&t){const zD=zy=>{const zh=String(zy||"").trim();if(!/^#[0-9a-fA-F]{6}$/.test(zh))return!1;const zr=parseInt(zh.slice(1,3),16),zg=parseInt(zh.slice(3,5),16),zb=parseInt(zh.slice(5,7),16);return .2126*zr+.7152*zg+.0722*zb<46};zD(t.backgroundColor)&&(t.backgroundColor=zSd);zD(t.plateOverride)&&(t.plateOverride=zSd);zD(t.darkPlate)&&(t.darkPlate=zSd)}}catch(zz){}""",
 'Fast schwarze Kachelgruende bekommen den Sandton', 1))

P.append((
 r"""ssGrund:"#141210",""",
 r"""ssGrund:"#3A2418",sandGrund:"#3A2418",""",
 'Der Sandton, auch fuer die Screenshot-Folie', 1))

# 251  Layouts variieren jetzt auch INNERHALB des Karussells
#
#      "Layouts die variieren sollen bitte auf die Folgefolien."
#
#      NACHGEMESSEN statt vermutet: eine Sonde im Eigenschaftsbau hat
#      fuer ein Karussell aus drei Folien protokolliert -
#          Folie 1  deckblatt  brand_photo_gradient
#          Folie 2  inhalt     brand_photo_gradient
#          Folie 3  abschluss  brand_photo_gradient
#      Alle drei dasselbe. Grund: zLay bekam dt, und dt ist der
#      TAGESindex. Ein Tag, ein Layout, egal wie viele Folien.
#      Was ich vorher fuer Variation gehalten hatte, waren nur die
#      Textpositionsregeln INNERHALB desselben Layouts.
#
#      Die Folienposition steht in Ve - dieselbe Zahl, aus der CG()
#      die Rolle ableitet. Der Index ist jetzt
#          Deckblatt      dt
#          Folgefolien    dt + Ve * layoutSchritt
#      Das Deckblatt bleibt damit bei seinem bisherigen Layout, der
#      Feed im Raster aendert sich nicht. layoutSchritt 7 ist
#      teilerfremd zu den 20 Eintraegen der Reihe, deshalb wiederholt
#      sich innerhalb eines Karussells nichts.
#
#      GEPRUEFT am Karussell: Folie 1 mittig auf Foto, Folie 2 unten
#      links, Folie 3 eine reine Textfolie. Dass auf Folie 3 das Foto
#      verschwindet, liegt am Textlayout und ist Teil der Variation.

P.append((
 r"""textBands:(zLay(dt,rt)||ot.bandStyle==="none")?void 0:!0,""",
 r"""textBands:(zLay(Ve===0?dt:dt+Ve*(Number(BS_KACHEL.layoutSchritt)||7),rt)||ot.bandStyle==="none")?void 0:!0,""",
 'Folgefolien waehlen ihr Layout nach der Folienposition', 1))

P.append((
 r"""layout:zLay(dt,rt)||Br,layoutId:zLay(dt,rt)||""",
 r"""layout:zLay(Ve===0?dt:dt+Ve*(Number(BS_KACHEL.layoutSchritt)||7),rt)||Br,layoutId:zLay(Ve===0?dt:dt+Ve*(Number(BS_KACHEL.layoutSchritt)||7),rt)||""",
 'Dasselbe an beiden Stellen des Eigenschaftsbaus', 2))

P.append((
 r"""sandGrund:"#3A2418",""",
 r"""sandGrund:"#3A2418",layoutSchritt:7,""",
 'Wie weit die Folgefolien in der Layoutreihe weiterspringen', 1))

# 252  Zurueck zum Schwarz
#
#      "Zurueck zum schwarz."
#
#      sandGrund wird geleert. Der Tauschcode aus 250 bleibt drin und
#      tut bei leerem Wert nichts - ein Farbwert genuegt, und der Ton
#      ist sofort wieder da. ssGrund geht auf #141210 zurueck, damit
#      die Screenshot-Folie zum Rest passt.
#
#      NACHGEMESSEN am Grund von Tag 9, mit dem neutralen Graubild:
#          vor 250   0,0,0
#          mit 250   58,36,23
#          jetzt     0,0,0
#      Also punktgenau der alte Zustand, nicht nur ungefaehr.
#
#      Die Layoutvariation aus 251 und alles andere bleibt.

P.append((
 r"""ssGrund:"#3A2418",sandGrund:"#3A2418",""",
 r"""ssGrund:"#141210",sandGrund:"",""",
 'Sandton wieder aus - der Grund ist wieder schwarz', 1))

# 253  Deckblattschrift groesser, und kein fettes Playfair mehr
#
#      "Schrift groesser auf Cover und kein Fettes Playfair."
#
#      ZWEI FEHLGRIFFE VORHER, beide durch Messen aufgeflogen:
#        1. Ich habe die Obergrenze r*(128/1080) in der Routine jt()
#           angehoben. Eine Sonde dort hat NIE gefeuert - jt() zeichnet
#           die Deckblaetter gar nicht.
#        2. Danach eine Sonde auf e.add, die jedes Textobjekt
#           protokolliert. Die hat die Wahrheit gezeigt:
#               Playfair Display 700  brand_frame_top_text, brand_photo_frame
#               Playfair Display 400  alle uebrigen
#               Groessen 53, 62, 74, 90
#           Gezeichnet wird in Pt(), einer ganz anderen Routine.
#
#      DAS FETTE kam aus tt, der Gewichtskette in Pt(). Sie endet auf
#      Xt(Ye,tt); direkt danach wird jetzt auf layoutGewicht gesetzt,
#      wenn die Familie Playfair ist. Nach dem Ende der Kette, nicht
#      davor - sonst haette Xt() es wieder ueberschrieben.
#
#      DIE GROESSE haengt an _t, der Startgroesse aus der
#      Layoutvorgabe mal jt (bei Playfair .82). Deckblaetter bekommen
#      dort jetzt deckblattGroesser dazu. Folgefolien nicht - die
#      Bedingung fragt folienRolle.
#
#      GEMESSEN, vorher gegen nachher:
#          Gewicht  700 -> 400 (bei den zwei Rahmenlayouts)
#          Groesse   53 -> 69,  74 -> 96,  62 -> 64,  90 -> 91
#      Dass zwei Werte kaum steigen, ist richtig so: dort begrenzt
#      die Einpassprobe in Pt(), nicht der Faktor. Nichts laeuft
#      ueber.

P.append((
 r"""tt=Xt(Ye,tt);const Qt=$e,""",
 r"""tt=Xt(Ye,tt);try{if(BS_KACHEL.layoutGewicht&&/Playfair/i.test(String(Ye)))tt=String(BS_KACHEL.layoutGewicht)}catch(zz){}const Qt=$e,""",
 'Playfair im Layout bekommt ein festes Gewicht, kein Fettes mehr', 1))

P.append((
 r"""let _t=Math.round((ht?me.fontSize*1.35:me.fontSize)*jt);""",
 r"""let _t=Math.round((ht?me.fontSize*1.35:me.fontSize)*jt*(!t.folienRolle||t.folienRolle==="deckblatt"?Number(BS_KACHEL.deckblattGroesser)||1:1));""",
 'Deckblaetter duerfen groesser starten', 1))

P.append((
 r"""layoutSchritt:7,""",
 r"""layoutSchritt:7,layoutGewicht:"400",deckblattGroesser:1.3,""",
 'Gewicht und Groessenfaktor fuers Deckblatt', 1))

# 254  Der Zuschnitt kann Gesichter - er wurde nur nie benutzt
#
#      "Schau wirklich, dass du Fotos nimmst, wo ich direkt in die
#       Kamera schaue, und schneide sie so."
#
#      GEFUNDEN statt gebaut: im Zeichner steht laengst eine Tabelle
#      von Zuschnitten, und die Haelfte davon rechnet mit dem
#      Gesicht -
#          full  [.5,  .5,  1  ]   Bildmitte, kein Zoom
#          wide  [.5,  .55, 1.35]  Bildmitte
#          face  [qe,  ht,  2.3 ]  GESICHTSmitte
#          bust  [qe,  ht+.22,1.7]  GESICHTSmitte
#          close [qe,  ht+.06,1.85] GESICHTSmitte
#      qe und ht kommen aus t._autoImage.faceZones, also aus dem
#      tinyFaceDetector, den die App schon laedt.
#
#      deckblattSchnitte stand auf "full|full|wide|full|wide|full" -
#      ausschliesslich die zwei Zuschnitte, die das Gesicht NICHT
#      benutzen. Deshalb sass der Ausschnitt immer auf der Bildmitte,
#      egal wo sie im Bild ist. Jetzt: "bust|face|bust|close|bust|face".
#
#      WAS DAMIT NICHT GELOEST IST, ausdruecklich: welches Foto
#      GENOMMEN wird. Der Detektor findet, DASS ein Gesicht da ist -
#      nicht, wohin sie schaut. In site/models liegt nur
#      tiny_face_detector, keine Landmarken. Ohne die laesst sich
#      frontal nicht von Profil unterscheiden.
#      Die Auswahl laeuft ueber xo(), das nach imageMeta[url].priority
#      sortiert - das Feld, das im Bilder-Reiter als Hoch/Normal/
#      Niedrig editierbar ist. Von Hand gesetzt wirkt es sofort.
#
#      GEPRUEFT: Raster gerendert, die Kacheln zoomen sichtbar naeher.
#      NICHT geprueft, weil hier kein echtes Portraet liegt: ob der
#      Detektor auf ihren Fotos anschlaegt. Ohne Treffer faellt der
#      Zuschnitt auf qe .5 / ht .34 zurueck - also oberes Drittel,
#      was fuer Portraets immer noch besser sitzt als die Mitte.

P.append((
 'deckblattSchnitte:"full|full|wide|full|wide|full"',
 'deckblattSchnitte:"bust|face|bust|close|bust|face"',
 'Deckblaetter schneiden aufs Gesicht statt auf die Bildmitte', 1))

# 255  Fuenfzehn Prozent weniger Schwarzweiss
#
#      "15% weniger schwarz weiss."
#
#      ZWEI SACKGASSEN, beide gemessen statt geglaubt:
#
#      1. saettigungReihe von "-1|0.1" auf "-0.85|0.1". Klingt nach
#         15 Prozent weniger. Gemessen am Farbabstand der Kacheln
#         (max(r,g,b) minus min(r,g,b), Mittel ueber drei Kacheln):
#             -1      4.31
#             -0.85  36.87
#         Also kein bisschen weniger, sondern VOLLE Farbe.
#
#      2. Ein Suchlauf ueber -0.999, -0.995, -0.99, -0.98 zeigte
#         einen SPRUNG statt eines Verlaufs:
#             -0.999  4.31
#             -0.995  4.31
#             -0.99   4.31
#             -0.98  36.87
#         Ein Sprung ist kein Filter. Also lag es nicht an der
#         Saettigung.
#
#      GEFUNDEN: drei Stellen im Zeichner haengen an der harten
#      Schwelle zSat<=-.99. Die entscheidende ist swBleibt - eine
#      graue Flaeche #808080 im Mischmodus "saturation" ueber dem
#      Foto. Die ist ganz an oder ganz aus, und SIE macht das
#      Schwarzweiss, nicht der Saettigungsfilter.
#
#      Der richtige Hebel ist also die DECKKRAFT dieser Flaeche.
#      Eingekreist, weil auch das nicht linear ist:
#          Deckkraft .85  ->  7.65  = 10.3 Prozent Farbe
#          Deckkraft .80  ->  9.28  = 15.3 Prozent Farbe
#          Deckkraft .78  ->  9.90  = 17.2 Prozent Farbe
#      Gesetzt ist .80. Bezugspunkte: 4.31 ist ganz schwarzweiss,
#      36.87 ist volle Farbe.
#
#      swStaerke fehlt oder ist keine Zahl -> Deckkraft 1, also
#      genau der alte Zustand.

P.append((
 'BS_KACHEL.swBleibt===1&&zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));',
 'BS_KACHEL.swBleibt===1&&zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",opacity:(typeof BS_KACHEL.swStaerke=="number"?Math.max(0,Math.min(1,BS_KACHEL.swStaerke)):1),selectable:!1,evented:!1}));',
 'Die Schwarzweiss-Flaeche bekommt eine Deckkraft', 1))

P.append((
 'swBleibt:1',
 'swBleibt:1,swStaerke:.8',
 '80 Prozent Schwarzweiss - gemessen bleiben 15,3 Prozent Farbe', 1))

# 256  Missverstaendnis: nicht die Saettigung, die ANZAHL
#
#      "Stop - schwarzweisse Bilder nicht weniger schwarzweiss in der
#       Saettigung." Dazu: "Jetzt noch das Gelb in der Schrift weg."
#
#      MEIN FEHLER in 255. "15% weniger schwarz weiss" habe ich als
#      "weniger stark entsaettigt" gelesen. Gemeint war: WENIGER
#      schwarzweisse Bilder. Die Kacheln, die schwarzweiss sind,
#      sollen es ganz sein.
#
#      Also swStaerke zurueck auf 1 - der Code aus 255 bleibt stehen
#      und tut bei 1 nichts.
#
#      Die Anzahl steuert saettigungReihe zusammen mit
#      saettigungWechsel: die Kachel nimmt den Eintrag an Position
#      _tag modulo Laenge. Bei "-1|0.1" war das jede zweite, also
#      50 Prozent. Neu: 40 Eintraege, davon 17 auf -1.
#          50,0 % -> 42,5 %  = 15,0 Prozent weniger
#      Die 17 sind gleichmaessig ueber die 40 verteilt (nach
#      floor(i*17/40)), damit nicht drei schwarzweisse Tage
#      aufeinander folgen.
#
#      GEPRUEFT am Raster mit Farbtestbild, Kachel fuer Kachel
#      gemessen: die schwarzweissen sitzen auf den Tagen 3 und 5,
#      genau auf den Positionen, an denen die Reihe -1 stehen hat.
#      Tag 8 traegt ein Rahmenlayout und laedt sein Bild ueber einen
#      anderen Weg, der die Schwarzweiss-Flaeche nicht bekommt - das
#      war schon vorher so.
#
#      hakenAkzentFarbe wird geleert. Der Code aus 245 bleibt, ein
#      Farbwert genuegt und die Betonung ist wieder da.

P.append((
 'swBleibt:1,swStaerke:.8',
 'swBleibt:1,swStaerke:1',
 'Schwarzweiss wieder voll - die Saettigung war nicht gemeint', 1))

P.append((
 'saettigungReihe:"-1|0.1"',
 'saettigungReihe:"-1|0.1|0.1|-1|0.1|-1|0.1|0.1|-1|0.1|-1|0.1|-1|0.1|0.1|-1|0.1|-1|0.1|-1|0.1|0.1|-1|0.1|-1|0.1|-1|0.1|0.1|-1|0.1|-1|0.1|-1|0.1|0.1|-1|0.1|-1|0.1"',
 'Statt jeder zweiten Kachel nur noch 17 von 40 in Schwarzweiss', 1))

P.append((
 'hakenAkzentFarbe:"#F3E5AB",',
 'hakenAkzentFarbe:"",',
 'Das Gelb in der Hookzeile wieder aus', 1))

# 257  Text unter den Screenshot - und der zweite Weg im Eigenschaftsbau
#
#      "Bei sowas lege den Text unter den Screenshot." Dazu ihr
#      Screenshot: die Zeile liegt quer ueber dem Foto, obwohl der
#      Stapel aus 242 genau das verhindern soll.
#
#      MEIN TEST ZEIGTE DEN FEHLER NICHT. Nachgestellt mit Hookzeile
#      und Foto sitzt der Stapel sauber. Der Unterschied liegt im
#      Eigenschaftsbau: der hat ZWEI Zweige, und 242 hat nur einen
#      gefasst.
#          rt._colorOverride ? { ...rt, ... }      <- nicht gefasst
#                            : { ...rt, text:Ir }  <- gefasst
#      Im ersten Zweig blieb overlayHook leer und der Text stehen -
#      also zeichnete ihn der Feed-Zweig ueber das Foto, waehrend der
#      Stapel oben eine leere Zeile liess. Die Umschichtung steht
#      jetzt in beiden Zweigen.
#
#      DIE REIHENFOLGE: ssTextUnten haengt die Hookzeile hinter den
#      Kasten statt davor. Der Stapel ist dann
#          Foto - Screenshot - Text
#      Gerechnet wird wie gehabt erst die Gesamthoehe, dann der obere
#      Rand, deshalb bleibt die Gruppe mittig.
#
#      GEPRUEFT: beide Faelle gerendert - Folie mit overlayHook und
#      Folie, deren Text erst umgeschichtet wird. Beide sehen gleich
#      aus, Reihenfolge stimmt, nichts ueberlappt.

P.append((
 'editorialDark:Mt?!1:_e.editorialDark===!0||_e.ruleSet==="editorial_dark"}',
 'editorialDark:Mt?!1:_e.editorialDark===!0||_e.ruleSet==="editorial_dark",...(rt.overlayIsScreenshot===!0&&!String(rt.overlayHook||"").trim()&&String(rt.text||"").trim()?{overlayHook:String(rt.text).replace(/\\*/g," ").replace(/\\s+/g," ").trim(),text:""}:{})}',
 'Auch der Farb-Zweig des Eigenschaftsbaus schiebt den Text in die Hookzeile', 1))

P.append((
 'if(zTbO)zTbO.set({top:zTop}),e.add(zTbO),zTop+=zHh+zG;',
 'const zTU=BS_KACHEL.ssTextUnten===1;if(zTbO&&!zTU)zTbO.set({top:zTop}),e.add(zTbO),zTop+=zHh+zG;',
 'Die Hookzeile oben nur noch, wenn sie nicht unten stehen soll', 1))

P.append((
 'e.add(me),Fe(!0)}catch(zz){Fe(!1)}};const zFot=String(t.zSsFoto||"");',
 'e.add(me),zTbO&&zTU&&(zTop+=zBox+zG,zTbO.set({top:zTop}),e.add(zTbO)),Fe(!0)}catch(zz){Fe(!1)}};const zFot=String(t.zSsFoto||"");',
 'Und sonst unter den Screenshot-Kasten', 1))

P.append((
 'ssFotoAnteil:.52,',
 'ssFotoAnteil:.52,ssTextUnten:1,',
 'Text unter dem Screenshot', 1))

# 258  Sechs Anordnungen fuer die Screenshot-Folie
#
#      "So, jetzt hast du alle so gebaut und es ist fad."
#
#      Stimmt. 242 bis 257 haben EINE Anordnung immer besser
#      gemacht, und damit sahen alle gleich aus. Die Layouts
#      variieren, die Screenshot-Folien nicht.
#
#      Jetzt waehlt ssReihe nach _tag aus sechs Bauarten. Jede ist
#      ein Tripel [Text unten?, Fotobreite, Fotohoehe-Anteil]:
#          A  1, .52, .52   Foto hoch, Kasten, Text unten
#          B  0, .52, .52   Text oben, Foto, Kasten
#          C  1, 1,   .42   Foto ueber die ganze Spalte, Text unten
#          D  0, 0,   0     ohne Foto: Text oben, Kasten
#          E  1, .4,  .62   schmales hohes Foto, Text unten
#          F  0, 1,   .34   Text oben, flaches breites Foto
#      Ist ssReihe leer, gilt wieder die feste Reihenfolge aus 257.
#
#      NEBENBEFUND beim Durchsehen der acht gerenderten Kacheln: eine
#      hatte einen dicken ROTEN Rahmen um den Screenshot. Der Rand
#      des Kastens war fill:F, und F ist t.backgroundColor - die
#      Farbe der Kachel. Auf den meisten Kacheln ist die hell, auf
#      dieser war sie rot. Das war schon vor 258 so, faellt aber nur
#      auf, wenn man mehrere Kacheln nebeneinander sieht. Der Kasten
#      hat jetzt mit ssKastenFarbe eine eigene Farbe.
#
#      GEPRUEFT: acht Folien gerendert, sechs verschiedene
#      Anordnungen sichtbar, kein roter Rahmen mehr.

P.append((
 'const zSetz=zFo=>{try{let zTbO=null,zHh=0;',
 'const zSetz=zFo=>{try{const zVa=(()=>{try{const zl=String(BS_KACHEL.ssReihe||"").split("|").filter(Boolean);if(!zl.length)return null;const zn=typeof t._tag=="number"?t._tag:String(zHk||"").length;return zl[((zn%zl.length)+zl.length)%zl.length]}catch(zz){return null}})(),zTab={A:[1,.52,.52],B:[0,.52,.52],C:[1,1,.42],D:[0,0,0],E:[1,.4,.62],F:[0,1,.34]},zVv=zTab[zVa]||null,zTU=zVv?zVv[0]===1:BS_KACHEL.ssTextUnten===1,zFB=zVv?zVv[1]:(Number(BS_KACHEL.ssFotoBreite)||1),zFA=zVv?zVv[2]:(Number(BS_KACHEL.ssFotoAnteil)||.42);if(!(zFA>0))zFo=null;let zTbO=null,zHh=0;',
 'Sechs Anordnungen fuer die Screenshot-Folie, gewaehlt nach Tag', 1))

P.append((
 'const zFoMax=zFo?zRest*(Number(BS_KACHEL.ssFotoAnteil)||.42):0;',
 'const zFoMax=zFo?zRest*zFA:0;',
 'Die Foto-Hoehe kommt aus der Anordnung', 1))

P.append((
 'zFw=zBr*(Number(BS_KACHEL.ssFotoBreite)||1)',
 'zFw=zBr*zFB',
 'Die Foto-Breite ebenso', 1))

P.append((
 'const zTU=BS_KACHEL.ssTextUnten===1;',
 '',
 'Die alte feste Reihenfolge entfaellt', 1))

P.append((
 'ssTextUnten:1,',
 'ssTextUnten:1,ssReihe:"A|D|B|C|A|E|D|F",',
 'Die Reihe der Anordnungen', 1))

P.append((
 'width:lt+Wt*2,height:wt+Wt*2,rx:12*d,ry:12*d,fill:F,selectable:!1,shadow:"rgba(0,0,0,0.22) 0px 10px 30px"',
 'width:lt+Wt*2,height:wt+Wt*2,rx:12*d,ry:12*d,fill:(BS_KACHEL.ssKastenFarbe||F),selectable:!1,shadow:"rgba(0,0,0,0.22) 0px 10px 30px"',
 'Der Rand um den Screenshot bekommt eine eigene Farbe statt der Kachelfarbe', 1))

P.append((
 'ssReihe:"A|D|B|C|A|E|D|F",',
 'ssReihe:"A|D|B|C|A|E|D|F",ssKastenFarbe:"#FFFFFF",',
 'Weiss, damit der Screenshot wie eine Karte liegt', 1))

# 259  Rueckstellpunkt: karten321 IST karten292
#
#      "Bitte zurueck zu 292, ich weiss nicht wie's ..."
#
#      Diesmal KEIN Nachbau und kein Paar. karten321 ist die Datei
#      aus Commit 75cb3ba, Byte fuer Byte - verglichen, es
#      unterscheiden sich genau 3 Zeichen, und das ist das
#      Versionsschild.
#
#      WICHTIG FUER DIE WARTUNG: alles ab Abschnitt 293 steckt NICHT
#      in dieser Datei. Die Paare weiter oben in diesem Skript passen
#      deshalb nicht mehr auf das laufende Bundle. Verloren ist
#      nichts - jeder Abschnitt steht hier und laesst sich einzeln
#      wieder auftragen.
#
#      WAS DAMIT WEG IST, damit es beim Suchen nicht verwundert:
#          293  die Farbleiste ueber dem Feed
#          294  Screenshot-Gruppe mittig
#          295  Folgefolien zentriert
#          297-299, 235-238  Rahmen und Layoutrotation
#          302-320  Layouts ueberall, Playfair statt Petrona,
#                   Deckblattgroesse, Gesichtszuschnitt,
#                   Schwarzweiss-Anteil, der Screenshot-Stapel und
#                   seine sechs Anordnungen
#
#      WAS DA IST: der schwarze Feed mit Playfair und Handschrift,
#      wie am Anfang.

# 260  karten322 IST karten291
#
#      "Nein nein nein, das war anders." - nach dem Rueckstellen auf
#      292. Also zum dritten Mal dieselbe Nummer, dieselbe Luecke
#      zwischen Nummer und Absicht.
#
#      DIESMAL NICHT GERATEN: drei Raster gerendert und vorgelegt -
#      292 wie es lief, 292 mit eingeschaltetem Layoutschalter
#      (= 291), und dasselbe mit Playfair statt Petrona. Ihre Wahl:
#      das mittlere.
#
#      karten322 ist deshalb die Datei karten291 aus Commit f2524c8,
#      byteweise verglichen: 3 Zeichen Unterschied, gleiche Laenge -
#      das Versionsschild.
#
#      SIE HAT PETRONA GEWAEHLT, obwohl sie sich frueher darueber
#      beschwert hat. Auf Deckblaettern gibt es damit auch keine
#      Handschriftzeile. Das ist so gewollt, nicht uebersehen - die
#      Playfair-Fassung lag daneben und sie hat die andere genommen.
#
#      Zur Wartung gilt wie bei 259: alles ab 293 steckt nicht in
#      dieser Datei, die Paare oben passen nicht darauf, und
#      verloren ist trotzdem nichts.

# 261  Abstand zwischen Hookzeile und Screenshot
#
#      "Ok, Abstand zwischen Text und Bild naeher."
#
#      karten322 ist der Stand von 291 und hat deshalb den ALTEN
#      Screenshot-Zweig: die Hookzeile sitzt fest bei n*.10, und der
#      Kasten wird in der gesamten Restflaeche darunter zentriert -
#          Qt = zOben + zH/2
#      Bei kurzem Screenshot klafft dazwischen eine Luecke, die mit
#      der Bildhoehe schwankt.
#
#      Eingebaut ist jetzt genau die Rechnung aus 294, mehr nicht:
#      Hoehe der Zeile plus ssLuft plus Kastenhoehe ergibt die
#      Gesamthoehe, daraus der obere Rand, und die Zeile wird
#      nachtraeglich dorthin gesetzt. Damit ist der Abstand
#      IMMER ssLuft, unabhaengig vom Screenshot.
#
#      NICHT mitgenommen: das Foto im Stapel (242), die sechs
#      Anordnungen (258), der Text unter dem Kasten (257). Nur der
#      Abstand, um den sie gebeten hat.
#
#      GEPRUEFT: dieselbe Folie vor und nach der Aenderung gerendert.

P.append((
 'zRd=r*.09,Wt=10*d;let zOben=n*.115;if(zHk){',
 'zRd=r*.09,Wt=10*d;let zOben=n*.115,zTbO=null;if(zHk){',
 'Die Hookzeile merken, um sie nachher noch verschieben zu koennen', 1))

P.append((
 'e.add(zTb),zOben=n*.10+zTb.height+n*.045}',
 'e.add(zTb),zTbO=zTb,zOben=n*.10+zTb.height+n*.045}',
 'Dasselbe', 1))

P.append((
 'Qt=zOben+zH/2+(typeof t.overlayImageY=="number"?t.overlayImageY:0)*d;',
 'Qt=(()=>{try{const zG=n*(Number(BS_KACHEL.ssLuft)||.035),zHh=zTbO?zTbO.height:0,zBox=wt+Wt*2,zGes=zHh+(zHh?zG:0)+zBox,zO=n*.10,zU=n*.865,zTop=Math.max(zO,Math.min((zO+zU)/2-zGes/2,zU-zGes));if(zTbO)zTbO.set({top:zTop});return zTop+zHh+(zHh?zG:0)+zBox/2}catch(zz){return zOben+zH/2}})()+(typeof t.overlayImageY=="number"?t.overlayImageY:0)*d;',
 'Hookzeile und Kasten stehen als eine Gruppe mittig, Abstand ist ssLuft', 1))

P.append((
 'kastenAn:0,',
 'kastenAn:0,ssLuft:.035,',
 'Der Abstand zwischen Text und Screenshot', 1))

# 262  Nur noch jede vierte Kachel in Schwarzweiss
#
#      "Ich treffe zu oft auf schwarzweisse Bilder und sie passen
#       stimmungstechnisch nicht."
#
#      saettigungReihe hatte zwei Eintraege, "-1|0.1", und
#      saettigungWechsel waehlt nach _tag modulo Laenge - also jede
#      zweite Kachel. Neu: 40 Eintraege, davon 10 auf -1, gleichmaessig
#      verteilt. 50 Prozent -> 25 Prozent.
#
#      EIN FEHLALARM BEIM PRUEFEN, zum Merken: mein Zaehlskript meldete
#      0 von 9 schwarzweiss. Die Regionen darin waren auf einen
#      frueheren Seitenumbruch geeicht und lagen daneben. Zwei
#      Gegenproben haben das geklaert -
#        - Reihe auf "-1" gesetzt: 8 von 9 Kacheln wurden grau, der
#          Mechanismus greift also.
#        - Eine Sonde auf zSat protokolliert: _tag ist eine Zahl, und
#          Tag 4 und Tag 8 bekommen -1.
#      Im Bild sind genau diese zwei grau. Die Aenderung stimmte, die
#      Messung nicht. Beim naechsten Mal zuerst ins Bild schauen.

P.append((
 'saettigungReihe:"-1|0.1"',
 'saettigungReihe:"-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1"',
 'Nur noch jede vierte Kachel schwarzweiss statt jeder zweiten', 1))

# 263  Gesichtsausdruck je Foto - Schritt eins der Stimmungswahl
#
#      "Kannst du schauen, wo mein Gesicht zu welcher Aussage passt?
#       Wahrscheinlich nicht." - "Ok."
#
#      DOCH, ZUR HAELFTE. Die App laedt face-api mit tinyFaceDetector.
#      Dieselbe Bibliothek kann Mimik (faceExpressionNet), im Bundle
#      ist der Code dafuer drin - nur die Gewichte fehlten. CDNs
#      sind hier gesperrt, npm nicht: aus @vladmandic/face-api 1.7.15
#      kommen face_expression_model.bin und das Manifest nach
#      site/models. Die Detektor-Gewichte des Pakets sind byteweise
#      identisch mit den vorhandenen, also dieselbe Modellfamilie.
#
#      WAS ES TUT: im Bilder-Reiter wird jedes Foto ohne Etikett
#      einmal durch Detektor + Ausdrucksnetz geschickt, das Ergebnis
#      landet in imageMeta[url].ausdruck (froehlich, ernst, neutral,
#      ueberrascht, kein Gesicht) und steht als antippbares Etikett
#      unter der Prioritaet. Antippen wechselt froehlich -> ernst ->
#      neutral. Die Handkorrektur ist damit dasselbe Feld wie das
#      Ergebnis - keine zweite Wahrheit.
#
#      DREI FEHLER AUF DEM WEG, alle im Test gefunden:
#        1. "Assignment to constant variable" - die Hilfsvariablen
#           haengen in einer const-Kette hinter HV. Zustand lebt
#           jetzt in Behaeltern ({p:null}, Set, Map), die man
#           veraendern statt zuweisen kann.
#        2. Ein Foto blieb dauerhaft auf "liest...". Mit einer Sonde:
#           BEIDE Erkennungen lieferten korrekt n:0 - verloren ging
#           das Speichern. Jede Kachel schreibt mit dem imageMeta-
#           Schnappschuss ihres Renders; die letzte ueberschreibt die
#           frueheren. Jetzt sammelt zAusdruckErg alle Ergebnisse und
#           jede Schreibung traegt alle zusammen ein.
#        3. Das Etikett sass auf der Unterkante und verdeckte "Als
#           CTA-Foto" - jetzt top-8 unter dem Prioritaets-Etikett.
#
#      Ladefehler werden NICHT gespeichert (nur echte Ergebnisse),
#      damit ein Geraet ohne WebGL es beim naechsten Oeffnen erneut
#      versucht. Die Erkennungen laufen streng nacheinander -
#      schonender fuer 40 Fotos auf dem Handy.
#
#      TESTBEDINGUNG, ehrlich: der Test-Browser hat WebGL nur per
#      --use-angle=swiftshader (Software). Damit ist belegt: Modell
#      laedt, Inferenz laeuft, Ergebnis wird fuer alle Kacheln
#      gespeichert und angezeigt. NICHT belegt, weil hier kein echtes
#      Portraet liegt: wie gut der Ausdruck auf ihren Fotos gelesen
#      wird. Das beurteilt sie im Bilder-Reiter.
#
#      Schritt zwei (Ton je Post beim Bulk Import ueber das Gemini-
#      Backend, Abgleich beim Zeichnen) folgt getrennt.

P.append((
 'for(let B=w;B<=b;B++)for(let k=m;k<=y;k++)B>=0&&B<t&&k>=0&&k<t&&r.add(B*t+k)}}catch{}return r},',
 'for(let B=w;B<=b;B++)for(let k=m;k<=y;k++)B>=0&&B<t&&k>=0&&k<t&&r.add(B*t+k)}}catch{}return r},zAusdruckLauft=new Set,zAusdruckNetz={p:null},zAusdruckKette={p:Promise.resolve()},zAusdruckErg=new Map,zAusdruckWort={happy:"fr\\u00f6hlich",neutral:"neutral",sad:"ernst",angry:"ernst",fearful:"ernst",disgusted:"ernst",surprised:"\\u00fcberrascht"},zAusdruck=async zu=>{try{if(!await QV()||!Zh||!Zh.nets||!Zh.nets.faceExpressionNet)return null;zAusdruckNetz.p||(zAusdruckNetz.p=Zh.nets.faceExpressionNet.loadFromUri(MV).then(()=>!0).catch(ze=>(console.warn("Ausdrucksmodell nicht geladen:",ze&&ze.message||ze),!1)));if(!await zAusdruckNetz.p)return null;const zi=await new Promise((ok,no)=>{const im=new Image;im.crossOrigin="anonymous";im.onload=()=>ok(im);im.onerror=()=>no(new Error("Bild"));im.src=zu});const zr=await Zh.detectAllFaces(zi,new Zh.TinyFaceDetectorOptions({inputSize:416,scoreThreshold:.4})).withFaceExpressions();if(!zr||!zr.length)return"kein Gesicht";zr.sort((a,b)=>b.detection.box.width*b.detection.box.height-a.detection.box.width*a.detection.box.height);const ze=zr[0].expressions||{},zk=Object.keys(ze).sort((a,b)=>ze[b]-ze[a])[0];return zAusdruckWort[zk]||zk||null}catch(zz){console.warn("Ausdruck:",zz&&zz.message||zz);return null}},',
 'Gesichtsausdruck je Foto erkennen: face-api mit faceExpressionNet aus /models', 1))

P.append((
 'Z=W=>{const G={...e.imageMeta||{},[U]:{...E,...W}};t({imageMeta:G})},re=Y===2?"Hoch":Y===0?"Niedrig":"Normal",',
 'Z=W=>{const G={...e.imageMeta||{},[U]:{...E,...W}};t({imageMeta:G})},zAE=(()=>{try{if(E.ausdruck===void 0&&!zAusdruckLauft.has(U)){zAusdruckLauft.add(U);zAusdruckKette.p=zAusdruckKette.p.then(()=>zAusdruck(U)).then(za=>{if(za){zAusdruckErg.set(U,za);const G={...e.imageMeta||{}};zAusdruckErg.forEach((zv,zk)=>{G[zk]={...G[zk]||{},ausdruck:zv}});t({imageMeta:G})}}).catch(()=>{})}}catch(zz){}return E.ausdruck!==void 0?E.ausdruck:zAusdruckErg.get(U)})(),zAEnext={"fr\\u00f6hlich":"ernst",ernst:"neutral",neutral:"fr\\u00f6hlich"},re=Y===2?"Hoch":Y===0?"Niedrig":"Normal",',
 'Erkennung je Kachel einmal anstossen, nacheinander; Ergebnisse in einer Tabelle sammeln und beim Speichern alle zusammen in imageMeta schreiben, damit kein veralteter Schnappschuss ein frueheres Ergebnis ueberschreibt', 1))

P.append((
 '((ue=e.currentBrandConfig)==null?void 0:ue.ctaImage)===U&&v.jsx("span",{className:"absolute top-1.5 right-1.5 bg-emerald-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow",children:"CTA"})]})',
 '((ue=e.currentBrandConfig)==null?void 0:ue.ctaImage)===U&&v.jsx("span",{className:"absolute top-1.5 right-1.5 bg-emerald-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow",children:"CTA"}),v.jsx("button",{onClick:W=>{W.preventDefault(),Z({ausdruck:zAEnext[zAE]||"fr\\u00f6hlich"})},className:`absolute top-8 left-1.5 text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow ${zAE===void 0?"bg-white/70 text-gray-500":zAE==="fr\\u00f6hlich"?"bg-amber-100 text-amber-800":zAE==="ernst"?"bg-slate-700 text-white":"bg-white/90 text-gray-700"}`,title:"Erkannter Gesichtsausdruck \\u2013 antippen zum \\u00c4ndern",children:zAE===void 0?"liest\\u2026":zAE})]})',
 'Etikett unter dem Prioritaets-Etikett oben links auf der Bildkachel, antippbar zum Korrigieren', 1))

# 264  Ausdruecke lesen nur noch auf Knopfdruck
#
#      "Ich habe ausserdem gerade 168 Fotos und jetzt dauert das Post
#       erstellen ultralange, bitte beschleunigen."
#
#      URSACHE, mit hoher Wahrscheinlichkeit 263: die Erkennung
#      startete beim Rendern der Bildkachel von selbst. Die Kette
#      laeuft dann alle 168 Fotos durch - auch wenn sie den Reiter
#      laengst verlassen hat und Posts baut. Detektor und
#      Ausdrucksnetz rechnen auf derselben Grafikeinheit wie der
#      Post-Zeichner. Minuten Konkurrenz.
#
#      JETZT: kein Autostart. Neben "Duplikate entfernen" steht
#      "Ausdruecke lesen (N offen)". Gedrueckt liest die App
#      nacheinander alle Fotos ohne Etikett, mit 200 ms Pause je
#      Foto, zeigt den Fortschritt (i/n) und laesst sich mit
#      demselben Knopf stoppen. Ungelesene Fotos zeigen "offen".
#      Ergebnisse werden weiter gesammelt und gemeinsam geschrieben
#      (263, Fehler 2), Ladefehler werden nicht gespeichert.
#
#      GEPRUEFT im Test-Browser mit Software-WebGL:
#          vor dem Klick, 8 s gewartet:  offen, offen  (nichts laeuft)
#          Knopf zeigt:                  Ausdruecke lesen (2 offen)
#          nach dem Klick, 10 s:         kein Gesicht, kein Gesicht
#          Konsole leer, keine Fehler.
#
#      OFFEN GEHALTEN, ehrlich: 168 Fotos liegen als volle Data-URLs
#      im Speicher und jede Kachel zieht sie in Originalgroesse. Wenn
#      das Posten nach 264 immer noch traege ist, liegt es daran und
#      nicht an der Erkennung - dann waeren Vorschaubilder der
#      naechste Schritt.

P.append((
 'zAusdruckKette={p:Promise.resolve()},zAusdruckErg=new Map,',
 'zAusdruckKette={p:Promise.resolve()},zAusdruckErg=new Map,zAusdruckLauft2={l:!1,stopp:!1,n:0,i:0},',
 'Laufzustand fuer den Leseknopf', 1))

P.append((
 'zAE=(()=>{try{if(E.ausdruck===void 0&&!zAusdruckLauft.has(U)){zAusdruckLauft.add(U);zAusdruckKette.p=zAusdruckKette.p.then(()=>zAusdruck(U)).then(za=>{if(za){zAusdruckErg.set(U,za);const G={...e.imageMeta||{}};zAusdruckErg.forEach((zv,zk)=>{G[zk]={...G[zk]||{},ausdruck:zv}});t({imageMeta:G})}}).catch(()=>{})}}catch(zz){}return E.ausdruck!==void 0?E.ausdruck:zAusdruckErg.get(U)})(),',
 'zAE=E.ausdruck!==void 0?E.ausdruck:zAusdruckErg.get(U),',
 'Kein Autostart mehr beim Rendern der Kachel - nur noch anzeigen, was bekannt ist', 1))

P.append((
 'children:zAE===void 0?"liest\\u2026":zAE})]})',
 'children:zAE===void 0?"offen":zAE})]})',
 "Ungelesene Fotos zeigen 'offen' statt 'liest...'", 1))

P.append((
 'title:"Doppelte Bilder entfernen",children:"Duplikate entfernen"}),',
 'title:"Doppelte Bilder entfernen",children:"Duplikate entfernen"}),v.jsx("button",{onClick:()=>{if(zAusdruckLauft2.l){zAusdruckLauft2.stopp=!0;return}const zO=(e.brandImages||[]).filter(zu=>((e.imageMeta||{})[zu]||{}).ausdruck===void 0&&!zAusdruckErg.has(zu));if(!zO.length)return;zAusdruckLauft2.l=!0,zAusdruckLauft2.stopp=!1,zAusdruckLauft2.n=zO.length,zAusdruckLauft2.i=0;t({imageMeta:{...e.imageMeta||{}}});(async()=>{try{for(const zu of zO){if(zAusdruckLauft2.stopp)break;const za=await zAusdruck(zu);zAusdruckLauft2.i+=1;if(za){zAusdruckErg.set(zu,za);const G={...e.imageMeta||{}};zAusdruckErg.forEach((zv,zk)=>{G[zk]={...G[zk]||{},ausdruck:zv}});t({imageMeta:G})}else t({imageMeta:{...e.imageMeta||{}}});await new Promise(zr=>setTimeout(zr,200))}}catch(zz){}zAusdruckLauft2.l=!1;const G={...e.imageMeta||{}};zAusdruckErg.forEach((zv,zk)=>{G[zk]={...G[zk]||{},ausdruck:zv}});t({imageMeta:G});B(zAusdruckLauft2.stopp?"Lesen gestoppt.":"Ausdr\\u00fccke gelesen.");setTimeout(()=>B(""),3e3)})()},className:`text-xs px-2 py-1 rounded border ${zAusdruckLauft2.l?"border-amber-300 bg-amber-50 text-amber-800":"border-gray-200 text-gray-600 hover:bg-gray-50"}`,title:"Gesichtsausdruck aller noch ungelesenen Fotos erkennen \\u2013 l\\u00e4uft nur, solange du hier bist, und l\\u00e4sst sich stoppen",children:zAusdruckLauft2.l?`Stoppen (${zAusdruckLauft2.i}/${zAusdruckLauft2.n})`:`Ausdr\\u00fccke lesen (${(e.brandImages||[]).filter(zu=>((e.imageMeta||{})[zu]||{}).ausdruck===void 0&&!zAusdruckErg.has(zu)).length} offen)`}),',
 "Knopf 'Ausdruecke lesen (N offen)' neben 'Duplikate entfernen', mit Stopp und Fortschritt, 200 ms Pause je Foto", 1))

# 265  Dunkle Fotos auf Helligkeit bringen - je Foto gemessen
#
#      "Ich hab nun neue Bilder geladen, aber sie sind zu dunkel
#       insgesamt und durch die dunkle Farbe unter der Schrift viel
#       zu dunkel. Kannst du sie auf die Helligkeit bringen wie alle
#       anderen?"
#
#      Der vorhandene Hub (bildHeben / hellBoost, ColorMatrix) liegt
#      hinter warmEditorial und steht bei ihr auf 0 - unbrauchbar als
#      Grundlage. Neu, direkt nach dem Laden jedes Fotos im Lader u():
#      das Bild wird auf 16x16 gezeichnet, die mittlere Luminanz
#      gemessen (t._hellMittel), und liegt sie unter hellZiel, kommt
#      ein Gamma-Filter dazu. Gamma statt Aufhellen per Addition,
#      damit die Mitteltoene steigen und Schwarz Schwarz bleibt - so
#      behaelt der Verlauf unter der Schrift seinen Kontrast.
#
#      FEHLGRIFF, gemessen erwischt: fabric rechnet Gamma UMGEKEHRT
#      zur ueblichen Lesart - Werte ueber 1 hellen auf. Mit meiner
#      ersten Kurve (unter 1) wurde das dunkle Raster DUNKLER:
#          dunkles Testfoto   53.2 -> 40.2   (falsch herum)
#      Kurve umgedreht:
#          dunkles Testfoto   53.2 -> 70.4   (+32 %)
#          graues Testfoto   101.9 -> 101.9  (unveraendert, wie es soll)
#      Gemessen als mittlere Luminanz ueber den Rasterbereich, also
#      inklusive Text und Zwischenraeumen - die Fotos selbst steigen
#      staerker als die Zahl zeigt.
#
#      REGLER: hellZiel 105 (Zielmittel; nur DUNKLERE Fotos werden
#      angefasst), hellGammaMax 1.7 (Deckel), hellKraft .8 (Kurve).
#      "Wie alle anderen" ist damit ein fester Zielwert, nicht der
#      Durchschnitt ihres Pools - bewusst, weil ein gleitender
#      Durchschnitt bei jedem neuen Foto alle anderen mitziehen wuerde.
#
#      NICHT erfasst: die Rahmenlayouts (E=true), die ihr Bild an u()
#      vorbei laden - wie bei Schwarzweiss (256) und Zuschnitt (254).

P.append((
 'me.setElement(Ze)}}catch{}const Oe=Math.max(r/me.width,n/me.height),Qe=i.slideIndex||0,',
 'me.setElement(Ze)}}catch{}try{const zZiel=Number(BS_KACHEL.hellZiel)||0;if(zZiel>0&&Pe.fabric.Image.filters&&Pe.fabric.Image.filters.Gamma){const zel=me.getElement&&me.getElement();if(zel&&zel.width){const zc=document.createElement("canvas");zc.width=zc.height=16;const zx=zc.getContext("2d");zx.drawImage(zel,0,0,16,16);const zd=zx.getImageData(0,0,16,16).data;let zs=0;for(let zi=0;zi<zd.length;zi+=4)zs+=.2126*zd[zi]+.7152*zd[zi+1]+.0722*zd[zi+2];const zm=zs/(zd.length/4);t._hellMittel=Math.round(zm);const zMax=Number(BS_KACHEL.hellGammaMax)||1.7,zg=Math.min(zMax,Math.max(1,Math.pow(zZiel/Math.max(1,zm),Number(BS_KACHEL.hellKraft)||.8)));if(zg>1.015){me.filters=(me.filters||[]).concat([new Pe.fabric.Image.filters.Gamma({gamma:[zg,zg,zg]})]);me.applyFilters()}}}}catch(zz){}const Oe=Math.max(r/me.width,n/me.height),Qe=i.slideIndex||0,',
 'Jedes Foto wird nach dem Laden gemessen; liegt sein Mittel unter hellZiel, hebt ein Gamma-Filter die Mitteltoene an (fabric: Gamma ueber 1 hellt auf) - Schwarz bleibt Schwarz', 1))

P.append((
 'bildHeben:0,',
 'bildHeben:0,hellZiel:105,hellGammaMax:1.7,hellKraft:.8,',
 'Zielhelligkeit, staerkste erlaubte Anhebung, Kurve', 1))

# 266  Drei Reparaturen, die der 291-Linie fehlten
#
#      Ihr Raster mit zwei rot durchgestrichenen Kacheln (Tag 81, 76):
#      "Die Kompositionen wuerde ich so nicht posten, und die
#       Folgefolien, die jetzt anscheinend nur mehr Montserrat haben
#       statt meiner Playfair und Handschrift, haben zu grossen Text."
#
#      karten322 ist byteweise 291. In dieser Linie fehlen drei
#      Dinge, die in der anderen Linie laengst repariert waren:
#
#      1. SCREENSHOT-FOLIEN BEKOMMEN KEIN LAYOUT (aus 241). Ohne die
#         Sperre malen zwei Zweige auf dieselbe Folie: das Layout ein
#         Foto-Inlay plus Headline, der Overlay-Zweig Hookzeile plus
#         Kasten. Das sind die durchgestrichenen Kacheln. Dazu die
#         Umschichtung text -> overlayHook in BEIDEN Zweigen des
#         Eigenschaftsbaus (aus 257), mit rt.text statt Ir, damit sie
#         in beiden Literalen gleich lautet.
#
#      2. LAYOUTS NUR AUF DEM DECKBLATT (aus 238). zLay(Ve===0?dt:-1)
#         an allen drei Stellen, und zLay gibt bei negativem Index ""
#         zurueck. Damit gehen Folgefolien durch den Feed-Zweig - der
#         einzige, der Playfair PLUS die Handschriftzeile kann. Im
#         Layout-Zweig holen sich Folgefolien die Fliesstextschrift
#         (249), daher das Montserrat.
#
#      3. FOLGEFOLIEN KLEINER (aus 239): folgeAnteil .82 auf beide
#         Hebel, Startgroesse qe und Hoehenbudget Je.
#
#      GEPRUEFT am gerenderten Karussell mit zweisaetzigem Text -
#         322: Folie 2 fette Grotesk, ein Block
#         328: Folie 2 Playfair-Headline, zweiter Satz in Handschrift,
#              zentriert
#      Screenshot-Folie mit Foto: kein Inlay mehr, Hookzeile und
#      Kasten als Gruppe mittig. Raster: Deckblatt-Layouts unveraendert.
#
#      FEHLVERSUCH beim Messen, zum Merken: eine e.add-Sonde vor
#      zSat faengt im Editor-Vorschaufenster nichts - dort haengt der
#      Zeichner an einem anderen Canvas. Ein Pixel-Scan auf hellen
#      Zeilen scheitert an weisser Seitenflaeche und hellem Foto.
#      Entschieden hat der Blick auf die vier Bilder.
#
#      OFFEN GELASSEN: die Folge-Headline steht in folgeGewicht 700,
#      wie im Stand 292. Sie hat fuer Deckblaetter "kein fettes
#      Playfair" gesagt (253), fuer Folgefolien nur "zu gross". Das
#      Gewicht ist eine Zahl, wenn sie es leichter will.

P.append((
 'zLay=(zi,zs)=>{try{const ze=zs&&zs.layout;',
 'zLay=(zi,zs)=>{try{if((Number(zi)||0)<0)return "";if(zs&&(zs.overlayIsScreenshot===!0||zs._wasScreenshot===!0))return "";const ze=zs&&zs.layout;',
 'zLay: negativer Index heisst kein Layout; Screenshot-Folien bekommen nie eines', 1))

P.append((
 'textBands:(zLay(dt,rt)||ot.bandStyle==="none")?void 0:!0,',
 'textBands:(zLay(Ve===0?dt:-1,rt)||ot.bandStyle==="none")?void 0:!0,...(rt.overlayIsScreenshot===!0&&!String(rt.overlayHook||"").trim()&&String(rt.text||"").trim()?{overlayHook:String(rt.text).replace(/\\*/g," ").replace(/\\s+/g," ").trim(),text:""}:{}),',
 'Layout nur auf dem Deckblatt (Ve===0); Text einer Screenshot-Folie wandert in die Hookzeile', 1))

P.append((
 'layout:zLay(dt,rt)||Br,layoutId:zLay(dt,rt)||',
 'layout:zLay(Ve===0?dt:-1,rt)||Br,layoutId:zLay(Ve===0?dt:-1,rt)||',
 'Dasselbe an beiden Stellen des Eigenschaftsbaus', 2))

P.append((
 'editorialDark:Mt?!1:_e.editorialDark===!0||_e.ruleSet==="editorial_dark"}',
 'editorialDark:Mt?!1:_e.editorialDark===!0||_e.ruleSet==="editorial_dark",...(rt.overlayIsScreenshot===!0&&!String(rt.overlayHook||"").trim()&&String(rt.text||"").trim()?{overlayHook:String(rt.text).replace(/\\*/g," ").replace(/\\s+/g," ").trim(),text:""}:{})}',
 'Auch im Farb-Zweig des Eigenschaftsbaus', 1))

P.append((
 't.bigHeadline===!0&&BS_KACHEL.pinnAnteil&&(qe=Math.roun',
 't.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeAnteil&&(qe=Math.max(c(12),Math.round(qe*Number(BS_KACHEL.folgeAnteil))));t.bigHeadline===!0&&BS_KACHEL.pinnAnteil&&(qe=Math.roun',
 'Folgefolien kleiner: Startgroesse', 1))

P.append((
 '*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)*(zKa?(Number(BS_KACHEL.kastenAnteil)||.72):1)-SR;',
 '*(t.folienRolle&&t.folienRolle!=="deckblatt"&&BS_KACHEL.folgeAnteil?Number(BS_KACHEL.folgeAnteil):1)*(t.bigHeadline===!0&&BS_KACHEL.pinnAnteil?Number(BS_KACHEL.pinnAnteil):1)*(zKa?(Number(BS_KACHEL.kastenAnteil)||.72):1)-SR;',
 'Und das Hoehenbudget, sonst holt die Schrumpfschleife es zurueck', 1))

P.append((
 'kastenAn:0,ssLuft:.035,',
 'kastenAn:0,ssLuft:.035,folgeAnteil:.82,',
 'Wie stark die Folgefolien kleiner werden', 1))

# 267  Der Balken hinter der Schrift richtet sich nach dem Foto
#
#      Ihr Deckblatt Tag 109: helles Foto auf dem Sofa, dahinter ein
#      dunkler Balken quer durch Gesicht und Oberkoerper. "Hier ist
#      der Balken zu stark - manchmal passt das, aber so nicht."
#
#      WAS DER BALKEN IST, nach drei Fehlgriffen: KEINER der
#      wortwoertlichen rgba-Kandidaten (dr/0.32, 0,0,0/0.55,
#      20,18,16/0.70) - ein farbcodierter Test faerbte nichts. Der
#      Balken ist die Glocke jr(st) im gradient-Zweig des
#      Layout-Zeichners:
#          Qe = t.overlayStrength ?? Yt.scrim ?? (serif .44 | warm .26 | .78)
#          pr = min(Qe + .12, .95)          Spitze in der Textmitte
#          Flanken bei st +- .15 mit Qe * .72, Null bei st +- .34
#      Layouts ohne eigenen scrim-Wert landen bei Qe .78, Spitze .90.
#      Das ist ihr Balken.
#
#      JETZT haengt Qe an der Helligkeit des Fotos GENAU hinter dem
#      Text. Dafuer zwei Zutaten im Lader u():
#        - die Messung aus 327 behaelt ihr 16x16-Netz (t._hellNetz)
#        - nach dem Platzieren wird jede der 16 Kachelzeilen auf die
#          zugehoerige Bildzeile abgebildet (me.top, me.height*jt),
#          also inklusive Zoom und Versatz der Gesichtszuschnitte -
#          t._hellZeilen
#      Im gradient-Zweig: mittlere Helligkeit der Zeilen im Band
#      er +- .15, daraus
#          zF = clamp((L - bandDunkel) / (bandHell - bandDunkel), 0, 1)
#          zQ = Qe * (bandMin + (1 - bandMin) * zF) * bandStaerke
#      Spitze und Flanken nutzen zQ. Regler: bandDunkel 70, bandHell
#      170, bandMin .35, bandStaerke .85.
#
#      GEMESSEN am Helligkeitsprofil von Tag 5, oben nach unten:
#        helles Foto   Minimum in der Balkenmitte 55 -> 69
#                      (Balken bleibt als Lesehilfe, weicher)
#        dunkles Foto  Minimum 47 -> 60, Zeilen um den Text 56 -> 86
#                      (Balken praktisch weg, Foto kommt durch)
#      Beide Bilder gesichtet: Schrift ueberall lesbar.
#
#      Ihr Fall (helle Haut, weisses Top, Sofa: L etwa 120-140) liegt
#      dazwischen: Spitze etwa .61 statt .90, gut ein Drittel weniger.

P.append((
 'const zm=zs/(zd.length/4);t._hellMittel=Math.round(zm);',
 'const zm=zs/(zd.length/4);t._hellMittel=Math.round(zm);t._hellNetz=(()=>{const zN=[];for(let zy=0;zy<16;zy++){const zR=[];for(let zx=0;zx<16;zx++){const zi=(zy*16+zx)*4;zR.push(.2126*zd[zi]+.7152*zd[zi+1]+.0722*zd[zi+2])}zN.push(zR)}return zN})();',
 'Die Messung aus 327 behaelt das 16x16-Helligkeitsnetz des Fotos', 1))

P.append((
 'me.set({originX:"center",originY:"center",left:r/2+pr,top:n/2+jr,scaleX:jt,scaleY:jt,selectable:!1});',
 'me.set({originX:"center",originY:"center",left:r/2+pr,top:n/2+jr,scaleX:jt,scaleY:jt,selectable:!1});try{const zN=t._hellNetz;if(zN&&zN.length===16){const zHb=me.height*jt,zOb=n/2+jr-zHb/2,zZ=[];for(let zk=0;zk<16;zk++){const zy=(zk+.5)/16*n,zq=Math.max(0,Math.min(15,Math.floor((zy-zOb)/zHb*16))),zR=zN[zq];zZ.push(zR.reduce((za,zb)=>za+zb,0)/zR.length)}t._hellZeilen=zZ}}catch(zz){}',
 'Nach dem Platzieren: Helligkeit je Kachelzeile, mit Zoom und Versatz abgebildet', 1))

P.append((
 'const er=$t?.72:Math.min(Math.max(jt/n,.08),.92),pr=Math.min(Qe+.12,.95),jr=st=>{',
 'const er=$t?.72:Math.min(Math.max(jt/n,.08),.92),zQ=(()=>{try{const zZ=t._hellZeilen;if(!zZ||zZ.length!==16)return Qe;const za=Math.max(0,Math.min(15,Math.floor((er-.15)*16))),zb=Math.max(za,Math.min(15,Math.ceil((er+.15)*16)));let zs=0,zk=0;for(let zi=za;zi<=zb;zi++){zs+=zZ[zi];zk++}const zL=zs/Math.max(1,zk),zD=Number(BS_KACHEL.bandDunkel)||70,zH=Number(BS_KACHEL.bandHell)||170,zMn=Number(BS_KACHEL.bandMin)||.35,zSt=Number(BS_KACHEL.bandStaerke)||1;const zF=Math.max(0,Math.min(1,(zL-zD)/Math.max(1,zH-zD)));t._bandLum=Math.round(zL);return Qe*(zMn+(1-zMn)*zF)*zSt}catch(zz){return Qe}})(),pr=Math.min(zQ+.12,.95),jr=st=>{',
 'Balken nur so stark, wie das Foto hinter dem Text hell ist', 1))

P.append((
 'Je(st-.15,Qe*.72),Je(st,pr),Je(st+.15,Qe*.72)',
 'Je(st-.15,zQ*.72),Je(st,pr),Je(st+.15,zQ*.72)',
 'Die Flanken der Glocke folgen demselben Wert', 1))

P.append((
 'hellKraft:.8,',
 'hellKraft:.8,bandDunkel:70,bandHell:170,bandMin:.35,bandStaerke:.85,',
 'Regler: ab welcher Helligkeit der Balken voll wird, Rest bei dunklem Foto, globale Staerke', 1))

# 268  Wie Lisa.contentdesign es bauen wuerde
#
#      "kannst du bitte so bauen also die Layouts die Folien, alles wie
#      wenn Lisa.contentdesign es bauen wuerde, sie wuerde vielleicht
#      auch Farben aendern oder so bitte mach es einfach wie sie wuerde"
#
#      VORLAGE: zwei Profil-Screenshots von lisa.contentdesign (Uploads
#      38d53864 und 367b7445). Was dort steht:
#        - Farben: Schokobraun (#2B1E17) statt Schwarz, Creme (#E9E3DA)
#          statt Weiss/Hellgrau, Schrift creme auf dunkel und braun auf
#          hell. Kein Rot, kein Gelb, keine Akzentfarbe.
#        - Schrift: enge, kontrastreiche Serife in Regular, grosse
#          Zeilen, Kursiv fuer Betonung, dazu kleine Versalzeilen mit
#          weiter Laufweite. Hier: Playfair Display 400 (liegt lokal),
#          Zeilenabstand .9, Laufweite -40, Betonung kursiv ohne Farbe.
#        - Fotos: alle warm-braun getont, kein Schwarzweiss.
#        - Layouts: Foto mit Text unten/oben/links, Creme-Karte mit
#          doppeltem duennem Rahmen, dunkle Flaeche mit grossem Wort und
#          kleinem Hochformat-Foto in der Mitte ("Seit wann" / "Nein,").
#        - Hierarchie: erster Satz gross, Rest klein darunter.
#
#      UMGESETZT in der 291-Linie (329 -> 330):
#        Stil-Objekt G2 und Kachelaufbau tragen die Toene; die drei
#        Zeichen-Zweige (gradient/plate/frame) erzwingen sie zusaetzlich
#        ueber zGrund()/zFarbe(), damit ein gespeicherter Stil mit
#        Schwarz/Weiss nicht durchschlaegt. Creme nur ueber plateColor
#        in der Layout-Tabelle (plate, plate_top, quote, kicker_lead,
#        minimal); alles andere schokobraun.
#        zTeilen() trennt am ersten Satzende (ohne Lookbehind, damit
#        aeltere Safari nicht am Regex sterben); zUnter() setzt den Rest
#        als Versalzeile (bis 42 Zeichen) oder Playfair-Zeile darunter.
#        Inset (brand_frame_top_text): Foto .42 breit, 1.22 hoch, ab
#        .27; grosses Wort davor (2 Woerter oder bis zum ersten Komma),
#        Rest unter dem Foto.
#        Toenung: Rect #6E4B36 mit globalCompositeOperation "color",
#        Deckkraft .8, ueber jedem Foto (auch im Inset). Schwarzweiss
#        ist damit aus (saettigungReihe "0.05").
#        Deckblatt-Schrift x 1.3 (lisaGroesse), Folgefolien unveraendert
#        (Playfair + Handschrift aus der 291-Linie).
#
#      REGLER (BS_DUNKEL): lisaGrund, lisaCreme, lisaHell, lisaDunkel,
#        lisaGroesse 1.3, lisaZeile -.12, lisaLaufweite -40, lisaTeilen 1,
#        lisaKapitel .0145, lisaUnter .03, lisaUnterGross .042,
#        lisaInsetBreite .42, lisaInsetUnten .056, bildTonung "#6E4B36",
#        bildTonungKraft .8, nameFarbeHell.
#
#      GESICHTET: Raster mit dunklem und buntem Testfoto, Karussell
#      (Deckblatt mit Versal-Unterzeile, Folgefolien wie zuvor),
#      Screenshot-Folie. Keine Konsolenfehler.

P.append((
 'colors:{primary:"#FFFFFF",secondary:"#000000",tertiary:"#8E8E92",accent:"#FF3A2E",neutral:"#000000",background:"#000000",darkPlate:"#000000"},typography:{fontFamily:"Petrona",plateFontFamily:"Petrona",signatureFontFamily:"OpenSansBrand",accentFontFamily:"OpenSansBrand",bodyFontFamily:"OpenSansBrand",fontWeight:"400"},fotoSchriften:[BS_KACHEL.fotoSchrift],textSchrift:"Petrona",layout:"brand_photo_gradient",warmEditorial:!1,headlineTracking:-15,headlineLineHeight:1,textTileLight:"#FFFFFF",textTileDark:"#000000"',
 'colors:{primary:"#F1EBE3",secondary:"#2B1E17",tertiary:"#9C8B7C",accent:"#F1EBE3",neutral:"#2B1E17",background:"#2B1E17",darkPlate:"#2B1E17"},typography:{fontFamily:"Playfair Display",plateFontFamily:"Playfair Display",signatureFontFamily:"OpenSansBrand",accentFontFamily:"Playfair Display",bodyFontFamily:"Playfair Display",fontWeight:"400"},fotoSchriften:[BS_KACHEL.fotoSchrift],textSchrift:"Playfair Display",layout:"brand_photo_gradient",warmEditorial:!1,headlineTracking:(Number(BS_KACHEL.lisaLaufweite)||-40),headlineLineHeight:1,textTileLight:"#E9E3DA",textTileDark:"#2B1E17"',
 'Stil-Objekt: Schokobraun, Creme, Playfair Display statt Petrona, Akzent ohne Farbe', 1))

P.append((
 'Ro=$r,ci="#FFFFFF",Wi=ve.background}else if(_e.warmEditorial)Wi="#000000",ci="#FFFFFF";else if(_e.textTileLight||_e.textTileDark){const $r=_e.textTileLight||"#E8E8E8";Wi=_e.textTileDark||"#000000",ci=$r}else Wi="#000000",ci="#E8E8E8";return Mt&&!Ta&&(ci=Ft(Wi)?"#FFFFFF":"#1A1512")',
 'Ro=$r,ci="#F1EBE3",Wi=ve.background}else if(_e.warmEditorial)Wi="#000000",ci="#FFFFFF";else if(_e.textTileLight||_e.textTileDark){const $r=_e.textTileLight||"#E8E8E8";Wi=_e.textTileDark||"#000000",ci=$r}else Wi="#000000",ci="#E8E8E8";return Mt&&!Ta&&(ci=Ft(Wi)?"#F1EBE3":"#2B1E17")',
 'Kachelaufbau: Schrift creme auf dunkel, schokobraun auf hell', 1))

P.append((
 '"#1A1612":"#F2EDE6"',
 '"#2B1E17":"#F1EBE3"',
 'Kontrastwahl X(): dieselben zwei Toene', 1))

P.append((
 'Un()?-.34:0',
 'Un()?(Number(BS_KACHEL.lisaZeile)||-.12):0',
 'Playfair: Zeilenabstand -.12 statt -.34 (Regler lisaZeile)', 1))

P.append((
 'Un()?.82:1',
 '1',
 'Playfair: keine Verkleinerung auf .82 mehr', 1))

P.append((
 'Un()?-135:0',
 'Un()?-40:0',
 'Playfair: Laufweite -40 statt -135, wenn kein Wert gesetzt', 1))

P.append((
 'const er=Fr($t,Ye,tt),pr=typeof t.headlineTracking',
 'const er=Un()?0:Fr($t,Ye,tt),pr=typeof t.headlineTracking',
 'Playfair: optische Engstellung Fr() aus, nur noch headlineTracking', 1))

P.append((
 'fontWeight:t.fontWeight||(ge.bigWord?"700":"600")',
 'fontWeight:"400"',
 'Deckblatt-Schrift regular statt 600/700 (gradient + plate)', 2))

P.append((
 'me.fontWeight||"600"',
 'me.fontWeight||"400"',
 'Pt(): Vorgabe 400 statt 600', 1))

P.append((
 'fontWeight:t.fontWeight||"600"',
 'fontWeight:"400"',
 'Folgefolien der Layouts: regular statt 600', 2))

P.append((
 'fontFamily:"Montserrat",fontWeight:"600",fill:Oe,charSpacing:ht',
 'fontFamily:"Montserrat",fontWeight:"500",fill:Oe,charSpacing:ht',
 'Versalzeile Te(): Gewicht 500', 1))

P.append((
 'let qe=c(15),ht=400;const Ye=r*.88',
 'let qe=c(14),ht=300;const Ye=r*.88',
 'Versalzeile Te(): kleiner, Laufweite 300', 1))

P.append((
 'fontFamily:"Montserrat",fontWeight:"600",fill:Oe,charSpacing:400',
 'fontFamily:"Montserrat",fontWeight:"500",fill:Oe,charSpacing:300',
 'Versalzeile Se(): Gewicht 500, Laufweite 300', 1))

P.append((
 'lr={brand_photo_gradient:{base:"gradient",textPos:"bottom",align:"center"},brand_photo_bottom_left:{base:"gradient",textPos:"bottom",align:"left"},brand_photo_top:{base:"gradient",textPos:"top",align:"center"},brand_photo_center:{base:"gradient",textPos:"center",align:"center"},brand_photo_bigword:{base:"gradient",textPos:"center",align:"center",bigWord:!0},brand_photo_quote:{base:"gradient",textPos:"center",align:"center",kicker:"top"},brand_photo_bottom_serif:{base:"gradient",textPos:"bottom",align:"center",kicker:"bottom"},brand_photo_frame:{base:"frame",textPos:"below",align:"center"},brand_frame_top_text:{base:"frame",textPos:"above",align:"center"},brand_frame_left:{base:"frame",framePos:"left",textPos:"below",align:"center"},brand_frame_polaroid:{base:"frame",polaroid:!0,textPos:"below",align:"center"},brand_text_plate:{base:"plate",textPos:"center",align:"center",rule:!0},brand_text_plate_top:{base:"plate",textPos:"top",align:"center",rule:!0},brand_text_left:{base:"plate",textPos:"center",align:"left",rule:!1},brand_text_bigword:{base:"plate",textPos:"center",align:"center",bigWord:!0},brand_text_quote:{base:"plate",textPos:"center",align:"center",kicker:"top",rule:!0},brand_text_statement:{base:"plate",textPos:"center",align:"center",kicker:"bottom"},brand_text_kicker_lead:{base:"plate",textPos:"center",align:"center",kicker:"top"},brand_text_minimal:{base:"plate",textPos:"center",align:"center"},brand_text_bold_top:{base:"plate",textPos:"top",align:"left",bigWord:!0},',
 'zGrund=zg=>{try{const zl=w(zg);if(BS_KACHEL.lisaGrund&&zl<45)return BS_KACHEL.lisaGrund;if(BS_KACHEL.lisaCreme&&zl>205)return BS_KACHEL.lisaCreme;return zg}catch(zz){return zg}},zFarbe=zg=>ee(zg)?(BS_KACHEL.lisaHell||"#F1EBE3"):(BS_KACHEL.lisaDunkel||"#2B1E17"),zTeilen=(zx,zKurz)=>{try{const zs=String(zx||"").replace(/\\s+/g," ").trim();if(!zs)return null;const zp=zs.match(/^(.*?[.!?\\u2026])\\s+([A-ZÄÖÜ\\u201E\\u201C"].*)$/);if(zp){const zo=zp[1],zu=zp[2];if(zo.replace(/\\*/g,"").length<=90&&zu.replace(/\\*/g,"").length<=160&&zu.replace(/\\*/g,"").length>=3)return{oben:zo,unten:zu}}if(!zKurz)return null;const zk=zs.match(/^([^,]{2,18}),\\s+(.{8,})$/);if(zk)return{oben:zk[1]+",",unten:zk[2]};const zw=zs.split(" ");if(zw.length>=4){const zo=zw.slice(0,2).join(" ");if(zo.replace(/\\*/g,"").length<=18)return{oben:zo,unten:zw.slice(2).join(" ")}}return null}catch(zz){return null}},zUnter=(zH,zx,zF,zLinks,zLeft,zGross)=>{try{if(!zH||!zx)return;const zs=String(zx).replace(/\\*/g,"").trim();if(!zs)return;const zb=zH.originY==="center"?zH.top+(zH.height||0)/2:zH.originY==="bottom"?zH.top:zH.top+(zH.height||0);const zy=zb+n*.028;const zKap=!zGross&&zs.length<=42&&!/[.!?]\\s/.test(zs);if(zKap){let zg=Math.round(r*(Number(BS_KACHEL.lisaKapitel)||.0145)),zc=300;const zm=()=>new Pe.fabric.Text(zs.toUpperCase(),{left:zLinks?zLeft:r/2,top:zy,originX:zLinks?"left":"center",originY:"top",fontSize:zg,fontFamily:"Montserrat",fontWeight:"500",fill:G(zF,.85),charSpacing:zc,selectable:!1});let zt=zm();for(;zt.width>r*.84&&zc>80;)zc-=60,zt=zm();for(;zt.width>r*.84&&zg>8;)zg-=1,zt=zm();e.add(zt);return}const zg=Math.round(r*(zGross?(Number(BS_KACHEL.lisaUnterGross)||.042):(Number(BS_KACHEL.lisaUnter)||.03))),zw=Math.max(zH.width||0,r*.5),zt=new Pe.fabric.Textbox(zs,{left:zLinks?zLeft:r/2-zw/2,top:zy,originX:"left",originY:"top",width:zw,fontSize:zg,fontFamily:"Playfair Display",fontWeight:"400",fill:G(zF,.92),textAlign:zLinks?"left":"center",lineHeight:1.18,charSpacing:-20,selectable:!1});for(let zi=0;zi<24&&zy+zt.height>n*.88&&zt.fontSize>10;zi+=1)zt.set({fontSize:zt.fontSize-1});e.add(zt)}catch(zz){}},lr={brand_photo_gradient:{base:"gradient",textPos:"bottom",align:"center",scrim:.6},brand_photo_bottom_left:{base:"gradient",textPos:"bottom",align:"left",scrim:.6},brand_photo_top:{base:"gradient",textPos:"top",align:"center",scrim:.55},brand_photo_center:{base:"gradient",textPos:"center",align:"center",scrim:.55},brand_photo_bigword:{base:"gradient",textPos:"center",align:"center",bigWord:!0,scrim:.55},brand_photo_quote:{base:"gradient",textPos:"center",align:"center",kicker:"top",scrim:.55},brand_photo_bottom_serif:{base:"gradient",textPos:"bottom",align:"center",kicker:"bottom",scrim:.6},brand_photo_frame:{base:"frame",textPos:"below",align:"center"},brand_frame_top_text:{base:"frame",textPos:"above",align:"center",inset:!0},brand_frame_left:{base:"frame",framePos:"left",textPos:"below",align:"center"},brand_frame_polaroid:{base:"frame",polaroid:!0,textPos:"below",align:"center"},brand_text_plate:{base:"plate",textPos:"center",align:"center",rule:!0,plateColor:"#E9E3DA"},brand_text_plate_top:{base:"plate",textPos:"top",align:"center",rule:!0,plateColor:"#E9E3DA"},brand_text_left:{base:"plate",textPos:"center",align:"left",rule:!1},brand_text_bigword:{base:"plate",textPos:"center",align:"center",bigWord:!0},brand_text_quote:{base:"plate",textPos:"center",align:"center",kicker:"top",rule:!0,plateColor:"#E9E3DA"},brand_text_statement:{base:"plate",textPos:"center",align:"center",kicker:"bottom"},brand_text_kicker_lead:{base:"plate",textPos:"center",align:"center",kicker:"top",plateColor:"#E9E3DA"},brand_text_minimal:{base:"plate",textPos:"center",align:"center",plateColor:"#E9E3DA"},brand_text_bold_top:{base:"plate",textPos:"top",align:"left",bigWord:!0},',
 'Layout-Tabelle: Helfer zGrund/zFarbe/zTeilen/zUnter, scrim je Fotolayout, Creme-Flaechen, Inset-Rahmen', 1))

P.append((
 'if(e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1})),ge.rule&&ee(me)){const br=r*.08;e.add(new Pe.fabric.Rect({left:br,top:br,width:r-br*2,height:n-br*2,fill:"transparent",stroke:G(me,.35),strokeWidth:1.5*d,selectable:!1}))}',
 'if(e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1})),ge.rule&&ee(me)){const br=r*.062,br2=r*.076;e.add(new Pe.fabric.Rect({left:br,top:br,width:r-br*2,height:n-br*2,fill:"transparent",stroke:G(me,.5),strokeWidth:1.4*d,selectable:!1}));e.add(new Pe.fabric.Rect({left:br2,top:br2,width:r-br2*2,height:n-br2*2,fill:"transparent",stroke:G(me,.3),strokeWidth:1*d,selectable:!1}))}',
 'Doppelrahmen auf der Creme-Flaeche (6.2 % und 7.6 %)', 1))

P.append((
 'if(Pt(ht,qe,{left:br,top:ae,originX:sr,originY:De,width:r*(Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),maxWidth:Qt?void 0:Ze?r*dt:void 0,fontSize:Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k():t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),minFontSize:Ze?T():void 0,goldOk:ur,fill:me,accentFill:Oe,textAlign:Ht,lineHeight:ge.bigWord?.98:t.warmEditorial?1.04:1.12,fontWeight:"400",shadow:se(),maxBottom:Ke}),',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!Qt&&!Ye&&!ge.bigWord&&!t.secondaryText&&!kt?zTeilen($e?$e.rest:t.text,!1):null,zOb=zSp?ye(zSp.oben):null,zHt=Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,top:ae,originX:sr,originY:De,width:r*(Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),maxWidth:Qt?void 0:Ze?r*dt:void 0,fontSize:Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k()*(Number(BS_KACHEL.lisaGroesse)||1):t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),minFontSize:Ze?T()*(Number(BS_KACHEL.lisaGroesse)||1):void 0,goldOk:ur,fill:me,accentFill:Oe,textAlign:Ht,lineHeight:ge.bigWord?.98:t.warmEditorial?1.04:1.12,fontWeight:"400",shadow:se(),maxBottom:zSp?Ke-n*.1:Ke});if(zSp&&zUnter(zHt,zSp.unten,me,Ht==="left",br),',
 'gradient-Zweig: erster Satz gross, Rest als Versal- oder Serifen-Unterzeile; Groesse x lisaGroesse', 1))

P.append((
 'if(Pt(qe,$e,{left:Ye,top:tt,originX:et,originY:Qt,width:r*(kt?.78:ge.exactWidth||(ht?.8:.74)),maxWidth:kt?r*.82:void 0,fontSize:t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):kt?r*(ar/1080):t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(jt),goldOk:_t,minFontSize:kt?r*(56/1080):void 0,fill:me,accentFill:Oe,textAlign:lt,lineHeight:ge.bigWord?.98:kt?1.16:t.warmEditorial?1.04:1.14,fontWeight:"400",shadow:se(),maxBottom:kt?n*.72:Ke}),',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&(i.slideIndex||0)===0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null,zOb=zSp?ye(zSp.oben):null,zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:Ye,top:tt,originX:et,originY:Qt,width:r*(kt?.78:ge.exactWidth||(ht?.8:.74)),maxWidth:kt?r*.82:void 0,fontSize:t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):kt?r*(ar/1080):t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(jt)*(Number(BS_KACHEL.lisaGroesse)||1),goldOk:_t,minFontSize:kt?r*(56/1080):void 0,fill:me,accentFill:Oe,textAlign:lt,lineHeight:ge.bigWord?.98:kt?1.16:t.warmEditorial?1.04:1.14,fontWeight:"400",shadow:se(),maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});if(zSp&&zUnter(zHt,zSp.unten,me,lt==="left",Ye),',
 'plate-Zweig: dieselbe Aufteilung; Groesse x lisaGroesse', 1))

P.append((
 'const{plain:Qe,segments:$e}=ye(t.text),qe=ge.textPos==="above",ht=ge.polaroid?r*.5:r*.58,Ye=ht*(ge.polaroid?1:1.12),et=(r-ht)/2,lt=ge.polaroid?r*.028:0,wt=ge.polaroid?lt*4:0,tt=qe?n*.46:n*.13,Qt=tt+Ye+wt;if(t.secondaryText&&!qe&&Se(t.secondaryText,r/2,n*.07,G(me,.7),"top"),qe&&Pt($e,Qe,{left:r/2,top:n*.22,originX:"center",originY:"center",width:r*.82,fontSize:c(t.fontSize||46),fill:me,accentFill:Oe,textAlign:"center",lineHeight:t.warmEditorial?1.04:1.12,shadow:se(),maxBottom:Ke}),',
 'const zIn=ge.inset===!0&&$&&(i.slideIndex||0)===0,zSp=zIn?zTeilen(t.text,!0):null,zOb=zSp?ye(zSp.oben):null,{plain:Qe,segments:$e}=zOb||ye(t.text),qe=ge.textPos==="above",ht=zIn?r*(Number(BS_KACHEL.lisaInsetBreite)||.40):ge.polaroid?r*.5:r*.58,Ye=ht*(zIn?1.22:ge.polaroid?1:1.12),et=(r-ht)/2,lt=ge.polaroid?r*.028:0,wt=ge.polaroid?lt*4:0,tt=zIn?n*(zSp?.27:.34):qe?n*.46:n*.13,Qt=tt+Ye+wt;if(t.secondaryText&&!qe&&Se(t.secondaryText,r/2,n*.07,G(me,.7),"top"),qe){const zHt=Pt($e,Qe,{left:r/2,top:zIn?(zSp?n*.155:n*.21):n*.22,originX:"center",originY:"center",width:r*.86,fontSize:c(zIn?(zSp&&Qe.length<=16?118:zSp?76:52):t.fontSize||46),fill:me,accentFill:Oe,textAlign:"center",lineHeight:zIn?.98:t.warmEditorial?1.04:1.12,shadow:se(),maxBottom:zIn?tt-n*.02:Ke});zIn&&zSp&&(zHt.set({top:tt-n*.03-(zHt.height||0)/2}),zHt.setCoords&&zHt.setCoords())}if(',
 'frame-Zweig: Inset - kleines Hochformat-Foto, grosses Wort oben, Rest unten', 1))

P.append((
 'e.add(ar),!ge.polaroid&&ee(me)&&e.add(new Pe.fabric.Rect({left:et,top:tt,width:ht,height:Ye,fill:"transparent",stroke:G(me,.25),strokeWidth:1.5*d,selectable:!1})),_t()},{crossOrigin:"anonymous"})}),!qe){',
 'e.add(ar),(()=>{try{const zT=String(BS_KACHEL.bildTonung||""),zK=Number(BS_KACHEL.bildTonungKraft)||0;zT&&zK>0&&BS_FARBMISCH&&e.add(new Pe.fabric.Rect({left:et,top:tt,width:ht,height:Ye,fill:zT,opacity:zK,globalCompositeOperation:"color",selectable:!1,evented:!1}))}catch(zz){}})(),!ge.polaroid&&!zIn&&ee(me)&&e.add(new Pe.fabric.Rect({left:et,top:tt,width:ht,height:Ye,fill:"transparent",stroke:G(me,.25),strokeWidth:1.5*d,selectable:!1})),_t()},{crossOrigin:"anonymous"})}),zIn&&zSp){const zW=r*.8,zt=new Pe.fabric.Textbox(String(zSp.unten).replace(/\\*/g,"").trim(),{left:r/2-zW/2,top:Qt+n*.035,originX:"left",originY:"top",width:zW,fontSize:Math.round(r*(Number(BS_KACHEL.lisaInsetUnten)||.046)),fontFamily:"Playfair Display",fontWeight:"400",fill:me,textAlign:"center",lineHeight:1.06,charSpacing:-30,selectable:!1});for(let zi=0;zi<30&&Qt+n*.035+zt.height>n*.88&&zt.fontSize>12;zi+=1)zt.set({fontSize:zt.fontSize-1});e.add(zt)}if(!qe){',
 'frame-Zweig: Toenung auch auf dem Inset-Foto, Unterzeile unter dem Foto', 1))

P.append((
 'BS_KACHEL.swBleibt===1&&zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));',
 'BS_KACHEL.swBleibt===1&&zSat<=-.99&&BS_MISCHBAR&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"#808080",globalCompositeOperation:"saturation",selectable:!1,evented:!1}));(()=>{try{const zT=String(BS_KACHEL.bildTonung||""),zK=Number(BS_KACHEL.bildTonungKraft)||0;if(!zT||!(zK>0)||!BS_FARBMISCH||zSat<=-.99||!t.background)return;e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:zT,opacity:zK,globalCompositeOperation:"color",selectable:!1,evented:!1}))}catch(zz){}})();',
 'Lader u(): warme Toenung (Composite "color", Regler bildTonung/bildTonungKraft)', 1))

P.append((
 'layoutReihe:"brand_photo_gradient|brand_photo_bottom_left|brand_photo_top|brand_photo_center|brand_photo_bigword|brand_photo_quote|brand_photo_bottom_serif|brand_photo_frame|brand_frame_top_text|brand_frame_left|brand_frame_polaroid|brand_text_plate|brand_text_plate_top|brand_text_left|brand_text_bigword|brand_text_quote|brand_text_statement|brand_text_kicker_lead|brand_text_minimal|brand_text_bold_top",',
 'layoutReihe:"brand_photo_bottom_left|brand_text_quote|brand_frame_top_text|brand_photo_top|brand_text_left|brand_photo_gradient|brand_photo_center|brand_text_plate|brand_photo_bottom_serif|brand_frame_top_text|brand_photo_bigword|brand_text_statement|brand_photo_quote|brand_frame_left|brand_text_plate_top|brand_photo_bottom_left|brand_text_bigword|brand_photo_frame|brand_text_minimal|brand_photo_top",bildTonung:"#6E4B36",bildTonungKraft:.8,lisaTeilen:1,lisaGrund:"#2B1E17",lisaCreme:"#E9E3DA",lisaHell:"#F1EBE3",lisaDunkel:"#2B1E17",lisaGroesse:1.3,nameFarbeHell:"rgba(43,30,23,0.5)",lisaLaufweite:-40,lisaZeile:-.12,lisaKapitel:.0145,lisaUnter:.03,lisaUnterGross:.042,lisaInsetBreite:.42,lisaInsetUnten:.056,',
 'Regler in BS_DUNKEL: neue layoutReihe, bildTonung, lisa*-Regler', 1))

P.append((
 'saettigungReihe:"-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1",',
 'saettigungReihe:"0.05",',
 'Kein Schwarzweiss mehr: saettigungReihe "0.05"', 1))

P.append((
 'if(Yt&&Yt.base==="gradient"){const ge=Yt,Fe=t.overlayColor||"#1A1512",me=X(t.color,$,Fe),Oe=t.accentColor||me,',
 'if(Yt&&Yt.base==="gradient"){const ge=Yt,Fe=zGrund(t.overlayColor||"#1A1512"),me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=me,',
 'Farben erzwingen im gradient-Zweig, unabhaengig vom gespeicherten Stil', 1))

P.append((
 'Fe=t.plateOverride||ge&&ge.plateColor||t.backgroundColor||"#E8E8E8",me=X(t.color,!1,Fe),Oe=t.accentColor||me;',
 'Fe=ge&&ge.plateColor?ge.plateColor:(BS_KACHEL.lisaGrund||zGrund(t.plateOverride||t.backgroundColor||"#E8E8E8")),me=zFarbe(Fe),Oe=me;',
 'Farben erzwingen in plate- und frame-Zweig: Creme nur per plateColor, sonst lisaGrund', 2))

P.append((
 'fill:BS_KACHEL.nameFarbe||"#FFFFFF",opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1,evented:!1});e.add(zNo)}else if(e.bringToFront)e.bringToFront(zNo)}',
 'fill:zFill(),opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1,evented:!1});e.add(zNo)}else{try{zNo.set("fill",zFill())}catch(zy){}if(e.bringToFront)e.bringToFront(zNo)}}',
 'Name auf hellen Flaechen dunkel (zFill bei jedem renderAll)', 1))

P.append((
 'const zRA=e.renderAll.bind(e);let zNo=null;e.renderAll=function(){',
 'const zRA=e.renderAll.bind(e);let zNo=null;const zFill=()=>{try{const zo=(e._objects||[]).filter(zx=>zx&&zx.type==="rect"&&typeof zx.fill=="string"&&zx.width>=r*.98&&zx.height>=n*.98&&(!zx.globalCompositeOperation||zx.globalCompositeOperation==="source-over")&&zx.fill!=="transparent").pop();if(zo){let zl=-1;const zf=String(zo.fill).trim();if(zf.charAt(0)==="#"){let zh=zf.slice(1);zh.length===3&&(zh=zh.split("").map(zq=>zq+zq).join(""));zl=.2126*parseInt(zh.slice(0,2),16)+.7152*parseInt(zh.slice(2,4),16)+.0722*parseInt(zh.slice(4,6),16)}else{const zm=zf.match(/rgba?\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)/);zm&&(zl=.2126*zm[1]+.7152*zm[2]+.0722*zm[3])}if(zl>150)return BS_KACHEL.nameFarbeHell||"rgba(43,30,23,0.5)"}}catch(zz){}return BS_KACHEL.nameFarbe||"#FFFFFF"};e.renderAll=function(){',
 'zFill(): letzte volle Flaeche ohne Composite bestimmt die Namensfarbe', 1))

# 269  Lisas Handwerk, Carinas Branding
#
#      "Wieso sind die Fotos getoent - es soll so sein als wuerde sie
#      mein Branding entwerfen, nicht ihres bauen."
#
#      330 hatte Lisas Palette mitgenommen: Schokobraun, Creme, warm
#      getonte Fotos, kein Schwarzweiss. Das war zu viel Lisa. Bleiben
#      soll nur das Handwerk - Layouts, Playfair regular, erster Satz
#      gross und Rest klein, Doppelrahmen, Inset. Farben und Fotos
#      wieder ihre: Schwarz, Weiss, Off-White #F2EFE9 (ihr Schildgrund),
#      Fotos ungetont, jedes vierte Schwarzweiss wie vor 330.
#      Alle 330-Regler bleiben, nur die Werte wechseln
#      (bildTonungKraft 0, lisaGrund #000000, lisaCreme #F2EFE9).

P.append((
 'colors:{primary:"#F1EBE3",secondary:"#2B1E17",tertiary:"#9C8B7C",accent:"#F1EBE3",neutral:"#2B1E17",background:"#2B1E17",darkPlate:"#2B1E17"}',
 'colors:{primary:"#FFFFFF",secondary:"#000000",tertiary:"#8E8E92",accent:"#FFFFFF",neutral:"#000000",background:"#000000",darkPlate:"#000000"}',
 'Stil-Objekt: zurueck auf Schwarz/Weiss, Playfair bleibt', 1))

P.append((
 'textTileLight:"#E9E3DA",textTileDark:"#2B1E17"',
 'textTileLight:"#F2EFE9",textTileDark:"#000000"',
 'Textflaechen: Off-White #F2EFE9 und Schwarz', 1))

P.append((
 'Ro=$r,ci="#F1EBE3",Wi=ve.background',
 'Ro=$r,ci="#FFFFFF",Wi=ve.background',
 'Kachelaufbau: Schrift weiss auf Foto', 1))

P.append((
 'return Mt&&!Ta&&(ci=Ft(Wi)?"#F1EBE3":"#2B1E17")',
 'return Mt&&!Ta&&(ci=Ft(Wi)?"#FFFFFF":"#111111")',
 'Kachelaufbau: weiss auf dunkel, fast-schwarz auf hell', 1))

P.append((
 '"#2B1E17":"#F1EBE3"',
 '"#111111":"#F2EFE9"',
 'Kontrastwahl X(): #111111 / #F2EFE9', 1))

P.append((
 'zFarbe=zg=>ee(zg)?(BS_KACHEL.lisaHell||"#F1EBE3"):(BS_KACHEL.lisaDunkel||"#2B1E17")',
 'zFarbe=zg=>ee(zg)?(BS_KACHEL.lisaHell||"#FFFFFF"):(BS_KACHEL.lisaDunkel||"#111111")',
 'zFarbe(): Vorgaben weiss / fast-schwarz', 1))

P.append((
 'return BS_KACHEL.nameFarbeHell||"rgba(43,30,23,0.5)"',
 'return BS_KACHEL.nameFarbeHell||"rgba(17,17,17,0.5)"',
 'zFill(): Name auf hellen Flaechen dunkelgrau', 1))

P.append((
 'plateColor:"#E9E3DA"',
 'plateColor:"#F2EFE9"',
 'Helle Flaechen der Layout-Tabelle: Off-White statt Creme', 5))

P.append((
 'bildTonung:"#6E4B36",bildTonungKraft:.8,lisaTeilen:1,lisaGrund:"#2B1E17",lisaCreme:"#E9E3DA",lisaHell:"#F1EBE3",lisaDunkel:"#2B1E17",lisaGroesse:1.3,nameFarbeHell:"rgba(43,30,23,0.5)",',
 'bildTonung:"",bildTonungKraft:0,lisaTeilen:1,lisaGrund:"#000000",lisaCreme:"#F2EFE9",lisaHell:"#FFFFFF",lisaDunkel:"#111111",lisaGroesse:1.3,nameFarbeHell:"rgba(17,17,17,0.5)",',
 'Regler: Toenung aus, lisaGrund schwarz, lisaCreme Off-White', 1))

P.append((
 'saettigungReihe:"0.05",',
 'saettigungReihe:"-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1",',
 'Schwarzweiss-Anteil wie vor 330 (jedes vierte Foto)', 1))

# 270  Name repariert, Layouts auf den Folgefolien
#
#      Screenshot Folie 7/13: "Name ist kaputt und mir fehlt das Layout
#      auf den Folge Folien."
#
#      NAME: die Einblendung aus 291 wickelte e.renderAll bei JEDEM
#      Aufruf des Zeichners neu ein. Jede Huelle hatte ihr eigenes
#      Textobjekt und zeichnete es nach e.clear() wieder - mit den
#      Massen ihres Aufrufs. Auf Schwarz fiel das nie auf, weil die
#      Kopien hell waren; seit 331 zFill() sie auf hellem Grund dunkel
#      faerbt, standen sie sichtbar uebereinander. Jetzt ein Haken pro
#      Leinwand (e.__zNameHook), Masse/Farbe/An-aus werden je Aufruf
#      gesetzt; bei Band-Folien (textBands) entfernt der Haken sein
#      Objekt, weil der Band-Zweig den Namen selbst zeichnet.
#
#      FOLGEFOLIEN: 328 hatte die Layouts aufs Deckblatt beschraenkt.
#      zLayF(dt, Ve, rt, foto) waehlt jetzt je Folie: Deckblatt wie
#      bisher aus layoutReihe[dt]; Folgefolie mit Foto aus
#      layoutReihe[dt + Ve*layoutSchritt]; Folgefolie ohne Foto aus
#      folgeReihe[dt + Ve - 1] (hell/dunkel im Wechsel). Gespeicherte
#      Layouts der Folgefolien werden dabei uebergangen. Im Zeichner
#      faellt die Vereinheitlichung (plate/gradient links, followUp)
#      weg, Satzaufteilung und Inset gelten auch dort, Schrift x .82.
#
#      GESICHTET: 5 Folien (Foto-Deckblatt, Creme/Schwarz im Wechsel,
#      erster Satz gross, Rest klein), Name einmal, korrekt gefaerbt.

P.append((
 'try{if(BS_KACHEL.nameZeigen!==0&&t&&t.textBands!==!0&&String(t.layout||"").indexOf("brand_")===0){const zRA=e.renderAll.bind(e);let zNo=null;const zFill=()=>{try{const zo=(e._objects||[]).filter(zx=>zx&&zx.type==="rect"&&typeof zx.fill=="string"&&zx.width>=r*.98&&zx.height>=n*.98&&(!zx.globalCompositeOperation||zx.globalCompositeOperation==="source-over")&&zx.fill!=="transparent").pop();if(zo){let zl=-1;const zf=String(zo.fill).trim();if(zf.charAt(0)==="#"){let zh=zf.slice(1);zh.length===3&&(zh=zh.split("").map(zq=>zq+zq).join(""));zl=.2126*parseInt(zh.slice(0,2),16)+.7152*parseInt(zh.slice(2,4),16)+.0722*parseInt(zh.slice(4,6),16)}else{const zm=zf.match(/rgba?\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)/);zm&&(zl=.2126*zm[1]+.7152*zm[2]+.0722*zm[3])}if(zl>150)return BS_KACHEL.nameFarbeHell||"rgba(17,17,17,0.5)"}}catch(zz){}return BS_KACHEL.nameFarbe||"#FFFFFF"};e.renderAll=function(){try{if(!zNo||!e._objects||e._objects.indexOf(zNo)<0){zNo=new Pe.fabric.Text("carinaannaprav",{left:r*.09,top:n*(BS_KACHEL.nameUnten||.945),originX:"left",originY:"center",fontSize:Math.round(r*(BS_KACHEL.nameAnteil||.042)),fontFamily:BS_KACHEL.nameSchrift||"OpenSansBrand",fontWeight:(BS_KACHEL.nameGewicht||"400"),charSpacing:(BS_KACHEL.nameLaufweite==null?150:BS_KACHEL.nameLaufweite),fill:zFill(),opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1,evented:!1});e.add(zNo)}else{try{zNo.set("fill",zFill())}catch(zy){}if(e.bringToFront)e.bringToFront(zNo)}}catch(zy){}return zRA.apply(e,arguments)}}}catch(zz){}',
 'try{const zAn=BS_KACHEL.nameZeigen!==0&&t&&t.textBands!==!0&&String(t.layout||"").indexOf("brand_")===0;const zH=e.__zNameHook||(e.__zNameHook={an:!1,r:0,n:0,no:null,installed:!1});zH.an=zAn;zH.r=r;zH.n=n;if(!zH.installed){zH.installed=!0;const zRA=e.renderAll.bind(e);const zFill=()=>{try{const zo=(e._objects||[]).filter(zx=>zx&&zx.type==="rect"&&typeof zx.fill=="string"&&zx.width>=zH.r*.98&&zx.height>=zH.n*.98&&(!zx.globalCompositeOperation||zx.globalCompositeOperation==="source-over")&&zx.fill!=="transparent").pop();if(zo){let zl=-1;const zf=String(zo.fill).trim();if(zf.charAt(0)==="#"){let zh=zf.slice(1);zh.length===3&&(zh=zh.split("").map(zq=>zq+zq).join(""));zl=.2126*parseInt(zh.slice(0,2),16)+.7152*parseInt(zh.slice(2,4),16)+.0722*parseInt(zh.slice(4,6),16)}else{const zm=zf.match(/rgba?\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)/);zm&&(zl=.2126*zm[1]+.7152*zm[2]+.0722*zm[3])}if(zl>150)return BS_KACHEL.nameFarbeHell||"rgba(17,17,17,0.5)"}}catch(zz){}return BS_KACHEL.nameFarbe||"#FFFFFF"};const zMass=()=>({left:zH.r*.09,top:zH.n*(BS_KACHEL.nameUnten||.945),fontSize:Math.round(zH.r*(BS_KACHEL.nameAnteil||.042)),fill:zFill()});e.renderAll=function(){try{const zDa=zH.no&&e._objects&&e._objects.indexOf(zH.no)>=0;if(!zH.an){if(zDa)e.remove(zH.no);zH.no=null}else if(!zDa){zH.no=new Pe.fabric.Text("carinaannaprav",Object.assign({originX:"left",originY:"center",fontFamily:BS_KACHEL.nameSchrift||"OpenSansBrand",fontWeight:(BS_KACHEL.nameGewicht||"400"),charSpacing:(BS_KACHEL.nameLaufweite==null?150:BS_KACHEL.nameLaufweite),opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1,evented:!1},zMass()));e.add(zH.no)}else{try{zH.no.set(zMass())}catch(zy){}if(e.bringToFront)e.bringToFront(zH.no)}}catch(zy){}return zRA.apply(e,arguments)}}}catch(zz){}',
 'Namens-Einblendung: ein Haken je Leinwand, Masse und Farbe je Aufruf, weg bei Band-Folien', 1))

P.append((
 '},aS=e=>{const t=Math.max(0,Number(e)||0);',
 '},zLayF=(dt,Ve,rt,ea)=>{try{const zF=BS_KACHEL.folgeLayouts===1,zV=Number(Ve)||0;if(zV>0&&!zF)return "";const zS=zV>0?{...(rt||{}),layout:void 0}:rt;let L=zLay((Number(dt)||0)+zV*(Number(BS_KACHEL.layoutSchritt)||7),zS);if(L&&zV>0&&!(typeof ea=="string"&&ea.length>5)){const zR=String(BS_KACHEL.folgeReihe||"").split("|").filter(Boolean);if(zR.length)L=zR[((Number(dt)||0)+zV-1)%zR.length]}return L||""}catch(zz){return ""}},aS=e=>{const t=Math.max(0,Number(e)||0);',
 'zLayF(): Layout je Folie, Folgefolien ohne Foto aus folgeReihe', 1))

P.append((
 'isCtaSlide:Ea,layout:zLay(Ve===0?dt:-1,rt)||Br,layoutId:zLay(Ve===0?dt:-1,rt)||',
 'isCtaSlide:Ea,layout:zLayF(dt,Ve,rt,ea)||Br,layoutId:zLayF(dt,Ve,rt,ea)||',
 'Kachelaufbau (Farbueberschreibung): Layout ueber zLayF', 1))

P.append((
 'textBands:(zLay(Ve===0?dt:-1,rt)||ot.bandStyle==="none")',
 'textBands:(zLayF(dt,Ve,rt,(e.tagBilder||{})[ot.day]||rt.background)||ot.bandStyle==="none")',
 'Kachelaufbau: Band-Entscheidung ueber zLayF', 1))

P.append((
 'visualElements:_e.visualElements||[],layout:zLay(Ve===0?dt:-1,rt)||Br,layoutId:zLay(Ve===0?dt:-1,rt)||',
 'visualElements:_e.visualElements||[],layout:zLayF(dt,Ve,rt,(e.tagBilder||{})[ot.day]||rt.background)||Br,layoutId:zLayF(dt,Ve,rt,(e.tagBilder||{})[ot.day]||rt.background)||',
 'Kachelaufbau: Layout ueber zLayF', 1))

P.append((
 'let Yt=lr[D];const Tr=.62,Qr=67,rn=.72;if(Yt&&typeof i.slideIndex=="number"&&i.slideIndex>0){',
 'let Yt=lr[D];const Tr=.62,Qr=67,rn=.72;if(Yt&&typeof i.slideIndex=="number"&&i.slideIndex>0&&BS_KACHEL.folgeLayouts!==1){',
 'Zeichner: keine Vereinheitlichung der Folgefolien, wenn folgeLayouts an', 1))

P.append((
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!Qt&&!Ye&&!ge.bigWord&&!t.secondaryText&&!kt?zTeilen($e?$e.rest:t.text,!1):null',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!Ye&&!ge.bigWord&&!t.secondaryText&&!kt?zTeilen($e?$e.rest:t.text,!1):null',
 'gradient-Zweig: Satzaufteilung auch auf Folgefolien', 1))

P.append((
 'const zSp=BS_KACHEL.lisaTeilen!==0&&(i.slideIndex||0)===0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null',
 'plate-Zweig: Satzaufteilung auch auf Folgefolien', 1))

P.append((
 'const zIn=ge.inset===!0&&$&&(i.slideIndex||0)===0,',
 'const zIn=ge.inset===!0&&$,',
 'frame-Zweig: Inset auch auf Folgefolien', 1))

P.append((
 '(Number(BS_KACHEL.lisaGroesse)||1)',
 'zGr()',
 'Groesse ueber zGr() (Folgefolien x folgeLayoutAnteil)', 3))

P.append((
 'zTeilen=(zx,zKurz)=>{',
 'zGr=()=>(Number(BS_KACHEL.lisaGroesse)||1)*((i.slideIndex||0)>0?(Number(BS_KACHEL.folgeLayoutAnteil)||.82):1),zTeilen=(zx,zKurz)=>{',
 'zGr() definiert', 1))

P.append((
 'lisaGroesse:1.3,nameFarbeHell:',
 'lisaGroesse:1.3,folgeLayouts:1,layoutSchritt:3,folgeReihe:"brand_text_quote|brand_text_left|brand_text_plate_top|brand_text_statement|brand_text_minimal|brand_text_bigword|brand_text_kicker_lead|brand_text_bold_top",folgeLayoutAnteil:.82,nameFarbeHell:',
 'Regler: folgeLayouts 1, layoutSchritt 3, folgeReihe, folgeLayoutAnteil .82', 1))

# 271  Schwarz-Weiss statt Creme, Text runter, Playfair erzwungen
#
#      Folie 3/10 (weisse Karte mit Doppelrahmen, Text oben, in
#      Montserrat): "nicht mittig oder tief genug. Orientiere nur bei
#      Bildern manchmal nach oben (wenn das Gesicht unten ist), sonst
#      immer runter. Dieses Layout finde ich am unpassendsten, meine
#      Farben sind wirklich eher schwarz-weiss - zeig mir mal, was das
#      bedeutet."
#
#      SCHRIFT: die Folgefolien nahmen t.fontFamily aus ihrem
#      gespeicherten Stil (bodyFontFamily -> Montserrat). Pt() setzt
#      jetzt BS_KACHEL.lisaSchrift (Playfair Display) fuer alle
#      Layout-Kacheln; Un() erkennt das mit.
#
#      LAGE: Flaechen (plate) und fotolose gradient-Kacheln zentrieren
#      den Textblock bei .58 statt oben (.24) oder mitte (.5). Fotos
#      blieben schon vorher unten (.64), ausser die Gesichtszonen liegen
#      im unteren Drittel - dann oben. Regler lisaUnten 1, lisaTextMitte.
#
#      FARBE: helle Karte reines Weiss, Text Schwarz; Doppelrahmen aus
#      (lisaRahmen 0). Damit sind die Flaechen wieder ihr Schwarz/Weiss.
#
#      GESICHTET: 5 Folien (Foto, Weiss, Schwarz, Weiss, Schwarz), Raster.

P.append((
 'Un=()=>/playfair/i.test(String(t.fontFamily||""))',
 'Un=()=>/playfair/i.test(String(BS_KACHEL.lisaSchrift||t.fontFamily||""))',
 'Un(): Playfair-Erkennung auch ueber lisaSchrift', 1))

P.append((
 'Oe&&Qe===2?Ye="Montserrat":Ye=qe?"Montserrat":m,',
 'Oe&&Qe===2?Ye="Montserrat":Ye=qe?"Montserrat":(BS_KACHEL.lisaSchrift||m),',
 'Pt(): Schrift in den Layouts immer lisaSchrift (Playfair), egal was der gespeicherte Stil sagt', 1))

P.append((
 'textTileLight:"#F2EFE9",textTileDark:"#000000"',
 'textTileLight:"#FFFFFF",textTileDark:"#000000"',
 'Textflaechen: reines Weiss', 1))

P.append((
 'return Mt&&!Ta&&(ci=Ft(Wi)?"#FFFFFF":"#111111")',
 'return Mt&&!Ta&&(ci=Ft(Wi)?"#FFFFFF":"#000000")',
 'Kachelaufbau: Schwarz auf hell', 1))

P.append((
 '"#111111":"#F2EFE9"',
 '"#000000":"#FFFFFF"',
 'Kontrastwahl X(): Schwarz / Weiss', 1))

P.append((
 'zFarbe=zg=>ee(zg)?(BS_KACHEL.lisaHell||"#FFFFFF"):(BS_KACHEL.lisaDunkel||"#111111")',
 'zFarbe=zg=>ee(zg)?(BS_KACHEL.lisaHell||"#FFFFFF"):(BS_KACHEL.lisaDunkel||"#000000")',
 'zFarbe(): Vorgaben Weiss / Schwarz', 1))

P.append((
 'plateColor:"#F2EFE9"',
 'plateColor:"#FFFFFF"',
 'Helle Flaechen der Layout-Tabelle: Weiss', 5))

P.append((
 'lisaCreme:"#F2EFE9",lisaHell:"#FFFFFF",lisaDunkel:"#111111",',
 'lisaCreme:"#FFFFFF",lisaHell:"#FFFFFF",lisaDunkel:"#000000",lisaRahmen:0,lisaUnten:1,lisaTextMitte:.58,lisaSchrift:"Playfair Display",',
 'Regler: lisaCreme weiss, lisaDunkel schwarz, lisaRahmen 0, lisaUnten 1, lisaTextMitte .58, lisaSchrift', 1))

P.append((
 'nameFarbeHell:"rgba(17,17,17,0.5)"',
 'nameFarbeHell:"rgba(0,0,0,0.5)"',
 'Name auf hellen Flaechen: halbtransparentes Schwarz', 1))

P.append((
 'ge.rule&&ee(me)){const br=r*.062,br2=r*.076;',
 'ge.rule&&ee(me)&&BS_KACHEL.lisaRahmen!==0){const br=r*.062,br2=r*.076;',
 'Doppelrahmen abschaltbar (lisaRahmen 0 = aus)', 1))

P.append((
 'let tt=ge.exactY!=null?n*ge.exactY:ge.textPos==="top"?n*.24:n*.5;const Qt=ge.textPos==="top"?"top":"center";',
 'let tt=ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?n*(Number(BS_KACHEL.lisaTextMitte)||.58):ge.textPos==="top"?n*.24:n*.5;const Qt=ge.textPos==="top"&&BS_KACHEL.lisaUnten!==1?"top":"center";',
 'plate-Zweig: Text mittig-tief bei .58 statt oben/mitte', 1))

P.append((
 'wt??($?n*.64:ge.textPos==="top"?n*.14:ge.textPos==="center"?n*.4:n*.64)',
 'wt??($?n*.64:BS_KACHEL.lisaUnten===1?n*(Number(BS_KACHEL.lisaTextMitte)||.58):ge.textPos==="top"?n*.14:ge.textPos==="center"?n*.4:n*.64)',
 'gradient-Zweig ohne Foto: Text mittig-tief bei .58', 1))

# 272  Versalzeile 50 Prozent groesser
#
#      "eins noch: die All-Caps-Schrift bitte 50 % groesser."
#      lisaKapitel .0145 -> .022 (die Unterzeile aus zUnter), dazu die
#      beiden Versal-Helfer Te() und Se() von 14/15 auf 21/22.

P.append((
 'lisaKapitel:.0145,',
 'lisaKapitel:.022,',
 'Versal-Unterzeile (zUnter): .022 statt .0145 der Breite, also plus 50 Prozent', 1))

P.append((
 'let qe=c(14),ht=300;const Ye=r*.88',
 'let qe=c(21),ht=300;const Ye=r*.88',
 'Versalzeile Te(): 21 statt 14', 1))

P.append((
 'originY:Qe,fontSize:c(15),fontFamily:"Montserrat",fontWeight:"500",fill:Oe,charSpacing:300',
 'originY:Qe,fontSize:c(22),fontFamily:"Montserrat",fontWeight:"500",fill:Oe,charSpacing:300',
 'Versalzeile Se(): 22 statt 15', 1))

# 273  Versalzeile nochmal 50 Prozent groesser
#
#      "Ok nochmal 50 % groesser." lisaKapitel .022 -> .033, Te() 21 -> 32,
#      Se() 22 -> 33. Gegenueber 333 also das 2,25-fache.

P.append((
 'lisaKapitel:.022,',
 'lisaKapitel:.033,',
 'Versal-Unterzeile (zUnter): .033 der Breite', 1))

P.append((
 'let qe=c(21),ht=300;const Ye=r*.88',
 'let qe=c(32),ht=300;const Ye=r*.88',
 'Versalzeile Te(): 32', 1))

P.append((
 'originY:Qe,fontSize:c(22),fontFamily:"Montserrat",fontWeight:"500",fill:Oe,charSpacing:300',
 'originY:Qe,fontSize:c(33),fontFamily:"Montserrat",fontWeight:"500",fill:Oe,charSpacing:300',
 'Versalzeile Se(): 33', 1))

# 274  Screenshot-Folie auf Weiss: Name war weiss
#
#      "Weisse Posts erhalten am Cover eine weisse Schrift, wenn sie mit
#      Screenshot sind." Screenshot-Folien laufen durch den Band-Zweig,
#      der den Namen fest in nameFarbe (helles Creme, .55) zeichnet -
#      auf weissem Grund unsichtbar bzw. weiss. Die Hook-Zeile selbst war
#      schon grundabhaengig (zTint). Jetzt: ohne Foto und Grund heller
#      als 150 -> nameFarbeHell (halbtransparentes Schwarz), sonst wie
#      bisher. Nachgestellt: Screenshot ohne Foto (weiss) und mit Foto.

P.append((
 'fill:tt.platten?(tt.bandSchriftFarbe||tt.schriftFarbe||"#241C16"):(BS_KACHEL.nameFarbe||"#FFFFFF"),opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1}))',
 'fill:tt.platten?(tt.bandSchriftFarbe||tt.schriftFarbe||"#241C16"):(!$e&&w(String(zGrundTon||"#000000"))>150?(BS_KACHEL.nameFarbeHell||"rgba(0,0,0,0.5)"):(BS_KACHEL.nameFarbe||"#FFFFFF")),opacity:(BS_KACHEL.nameDeckkraft||.55),selectable:!1}))',
 'Band-Zweig: Name auf hellem Grund ohne Foto dunkel (Screenshot-Folien auf Weiss)', 1))

# 275  Reine Textfolien zeigen sie trotzdem: blurred oder klein
#
#      "Ich wuerde gerne bei den reinen Textposts dennoch mich zeigen,
#      blurred im Hintergrund oder einfach klein ausgeschnitten als
#      Bild - ohne was ist das nix."
#
#      WOHER DAS FOTO: Folgefolien tragen kein Foto. Beim Zeichnen
#      einer Folie MIT Foto merkt sich Ca das Foto je Tag
#      (window.__bsTagFoto[_tag], Deckblatt hat Vorrang). Textflaechen
#      ohne eigenes Foto nehmen das Foto ihres Tages; fehlt auch das,
#      ein Foto aus window.__bsBilder nach Text-Hash. Nichts wird im
#      Plan gespeichert (Fotos sind Data-URLs, das wuerde den Speicher
#      vervielfachen).
#
#      ZWEI FASSUNGEN im Wechsel ((_tag + slideIndex) % 2):
#        blur   Foto vollflaechig, auf 720 px verkleinert, Blur .45,
#               darueber die Flaeche mit Deckkraft .8 - auf Weiss ein
#               heller Schleier, auf Schwarz ein dunkler.
#        inset  Flaeche deckend, darueber ein Hochformat-Ausschnitt
#               .28 breit (1:1.25) ab .10, Zuschnitt nach oben
#               versetzt (bias .35, Gesichter). Die Headline rueckt bei
#               Bedarf kleiner oder tiefer, damit sie nicht ins Foto
#               laeuft.
#      Screenshot-Folien bleiben ohne.
#
#      GESICHTET: 5 Folien (Weiss blur, Schwarz inset, Weiss blur,
#      Schwarz inset), Raster mit buntem Testfoto.

P.append((
 'try{if(typeof window<"u"&&typeof t.background=="string"&&t.background){const zL=window.__bsBilder=window.__bsBilder||[];if(zL.indexOf(t.background)<0)zL.push(t.background)}}catch(zz){}',
 'try{if(typeof window<"u"&&typeof t.background=="string"&&t.background){const zL=window.__bsBilder=window.__bsBilder||[];if(zL.indexOf(t.background)<0)zL.push(t.background);if(typeof t._tag=="number"&&((i.slideIndex||0)===0||!(window.__bsTagFoto||{})[String(t._tag)])){const zT=window.__bsTagFoto=window.__bsTagFoto||{};zT[String(t._tag)]=t.background}}}catch(zz){}',
 'Merkliste window.__bsTagFoto: Foto je Tag beim Zeichnen einer Folie mit Foto', 1))

P.append((
 'if(Yt&&Yt.base==="plate"){const ge=Yt,Fe=ge&&ge.plateColor?ge.plateColor:(BS_KACHEL.lisaGrund||zGrund(t.plateOverride||t.backgroundColor||"#E8E8E8")),me=zFarbe(Fe),Oe=me;if(e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1})),',
 'if(Yt&&Yt.base==="plate"){const ge=Yt,Fe=ge&&ge.plateColor?ge.plateColor:(BS_KACHEL.lisaGrund||zGrund(t.plateOverride||t.backgroundColor||"#E8E8E8")),me=zFarbe(Fe),Oe=me;const zTF=(()=>{try{if(!BS_KACHEL.textFoto||t.overlayIsScreenshot===!0)return null;const zL=String(BS_KACHEL.textFoto).split("|").filter(Boolean);if(!zL.length)return null;const zReg=(typeof window<"u"&&window.__bsTagFoto)||{};let zF=$?t.background:(zReg[String(t._tag)]||"");if(!zF){const zB=(typeof window<"u"&&window.__bsBilder)||[];if(zB.length){let zh=0;const zs=String(t.text||"");for(let zi=0;zi<zs.length;zi++)zh=(zh*31+zs.charCodeAt(zi))%99991;zF=zB[zh%zB.length]}}if(!zF)return null;const zArt=zL[((Number(t._tag)||0)+(i.slideIndex||0))%zL.length];return zArt&&zArt!=="keins"?{url:zF,art:zArt}:null}catch(zz){return null}})(),zLadeFoto=(zu,zo)=>new Promise(zr=>{let zd=!1;const zf=()=>{zd||(zd=!0,zr())};setTimeout(zf,6e3);try{Pe.fabric.Image.fromURL(zu,zim=>{if(!zim)return zf();try{const zel=zim.getElement&&zim.getElement(),zMax=zo.blur?720:1400;if(zel&&zel.width&&Math.max(zel.width,zel.height)>zMax){const zs=zMax/Math.max(zel.width,zel.height),zc=document.createElement("canvas");zc.width=Math.round(zel.width*zs);zc.height=Math.round(zel.height*zs);zc.getContext("2d").drawImage(zel,0,0,zc.width,zc.height);zim.setElement(zc)}const zk=Math.max(zo.w/zim.width,zo.h/zim.height),zUeb=zim.height*zk-zo.h,zBias=typeof zo.bias=="number"?zo.bias:0;zim.set({originX:"center",originY:"center",left:zo.x+zo.w/2,top:zo.y+zo.h/2+zUeb*zBias,scaleX:zk,scaleY:zk,selectable:!1,evented:!1});if(zo.clip)zim.clipPath=new Pe.fabric.Rect({left:zo.x,top:zo.y,width:zo.w,height:zo.h,absolutePositioned:!0});if(zo.blur&&Pe.fabric.Image.filters&&Pe.fabric.Image.filters.Blur){zim.filters=[new Pe.fabric.Image.filters.Blur({blur:zo.blur})];try{zim.applyFilters()}catch(zz){zim.filters=[]}}e.add(zim);zf()}catch(zz){zf()}},{crossOrigin:"anonymous"})}catch(zz){zf()}});let zInsetUnten=0;if(zTF&&zTF.art==="blur")await zLadeFoto(zTF.url,{x:0,y:0,w:r,h:n,blur:Number(BS_KACHEL.textFotoBlur)||.45,bias:.15});if(e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:zTF&&zTF.art==="blur"?G(Fe,Number(BS_KACHEL.textFotoDeck)||.8):Fe,selectable:!1})),zTF&&zTF.art==="inset"){const zW=r*(Number(BS_KACHEL.textFotoBreite)||.28),zH=zW*1.25,zY=n*(Number(BS_KACHEL.textFotoOben)||.10);await zLadeFoto(zTF.url,{x:r/2-zW/2,y:zY,w:zW,h:zH,clip:!0,bias:.35});zInsetUnten=zY+zH}if(',
 'plate-Zweig: zTF waehlt blur oder inset, zLadeFoto() zeichnet das Foto (blurred hinter der Flaeche oder klein ausgeschnitten oben)', 1))

P.append((
 'maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});if(zSp&&zUnter(zHt,zSp.unten,me,lt==="left",Ye),',
 'maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});try{if(zInsetUnten>0&&zHt&&zHt.originY==="center"){const zGr2=zInsetUnten+n*.035;let zi2=0;for(;zHt.top-(zHt.height||0)/2<zGr2&&zHt.fontSize>12&&zi2<80;zi2+=1)zHt.set("fontSize",zHt.fontSize-1),zHt.initDimensions&&zHt.initDimensions();if(zHt.top-(zHt.height||0)/2<zGr2){zHt.set("top",zGr2+(zHt.height||0)/2);zHt.setCoords&&zHt.setCoords()}}}catch(zz){}if(zSp&&zUnter(zHt,zSp.unten,me,lt==="left",Ye),',
 'plate-Zweig: Headline weicht dem Inset aus (kleiner, sonst tiefer)', 1))

P.append((
 'lisaSchrift:"Playfair Display",',
 'lisaSchrift:"Playfair Display",textFoto:"blur|inset",textFotoDeck:.8,textFotoBlur:.45,textFotoBreite:.28,textFotoOben:.10,',
 'Regler: textFoto "blur|inset", textFotoDeck .8, textFotoBlur .45, textFotoBreite .28, textFotoOben .10', 1))

# 276  CTA-Foto auch am Ende der Textposts
#
#      "Geht das CTA-Foto noch? Ich will auch am Ende der Textposts mein
#      CTA-Bild."
#
#      BISHER haengt das CTA-Foto (Brand-Einstellungen, "Wird immer auf
#      der letzten Slide verwendet") an Rt(): beim Normalisieren des
#      Plans bekommt die letzte Folie background = ctaImage. Wird das
#      Foto spaeter gesetzt oder der Plan nicht neu normalisiert, fehlt
#      es. Und seit 332 waehlte zLayF fuer Folgefolien ohne Foto ein
#      Textlayout - die Flaeche deckte das CTA-Foto zu.
#
#      JETZT zweigleisig:
#        - Rt(): zLayF bekommt Ea (CTA-Kennzeichen) und liefert dann
#          brand_photo_gradient.
#        - Zeichner: die Aufrufer (Editor-Vorschau XV, drei Exporte)
#          geben ctaImage aus currentBrandConfig in den Optionen mit.
#          Ist die Folie die letzte von mehreren, hat kein Foto, ist
#          kein Screenshot und kein Ablauf, setzt Ca background =
#          ctaImage, Fotolayout, kein Band. Damit klappt es ohne
#          Neu-Normalisieren, auch bei reinen Textposts.
#      Das Raster zeigt nur Deckblaetter und ist nicht betroffen.
#
#      GESICHTET: 5 Folien mit gesetztem CTA-Foto (grau): Folie 5 zeigt
#      es mit Text unten. Ohne CTA-Foto unveraendert.

P.append((
 'zLayF=(dt,Ve,rt,ea)=>{try{const zF=BS_KACHEL.folgeLayouts===1,zV=Number(Ve)||0;if(zV>0&&!zF)return "";',
 'zLayF=(dt,Ve,rt,ea,zCta)=>{try{const zF=BS_KACHEL.folgeLayouts===1,zV=Number(Ve)||0;if(zV>0&&!zF)return "";if(zCta===!0&&zF&&typeof ea=="string"&&ea.length>5)return "brand_photo_gradient";',
 'zLayF(): CTA-Folie bekommt ein Fotolayout (brand_photo_gradient)', 1))

P.append((
 'zLayF(dt,Ve,rt,ea)',
 'zLayF(dt,Ve,rt,ea,Ea)',
 'Kachelaufbau: zLayF bekommt das CTA-Kennzeichen mit', 2))

P.append((
 'if(typeof t._tag=="number"&&((i.slideIndex||0)===0||!(window.__bsTagFoto||{})[String(t._tag)])){const zT=window.__bsTagFoto=window.__bsTagFoto||{};zT[String(t._tag)]=t.background}}}catch(zz){}',
 'if(typeof t._tag=="number"&&((i.slideIndex||0)===0||!(window.__bsTagFoto||{})[String(t._tag)])){const zT=window.__bsTagFoto=window.__bsTagFoto||{};zT[String(t._tag)]=t.background}}}catch(zz){}try{if(i&&typeof i.ctaImage=="string"&&i.ctaImage.length>5&&(Number(i.totalSlides)||1)>1&&(i.slideIndex||0)===(Number(i.totalSlides)||1)-1&&!(typeof t.background=="string"&&t.background.length>5)&&t.overlayIsScreenshot!==!0&&t.karte!=="ablauf"){const zL=String(t.layout||"");t={...t,background:i.ctaImage,isCtaSlide:!0,textBands:zL.indexOf("brand_")===0?void 0:t.textBands,layout:zL.indexOf("brand_")===0&&!/photo|frame/.test(zL)?"brand_photo_gradient":t.layout,layoutId:zL.indexOf("brand_")===0&&!/photo|frame/.test(zL)?"brand_photo_gradient":t.layoutId}}}catch(zz){}',
 'Zeichner: letzte Folie ohne Foto nimmt das CTA-Foto aus den Optionen (Fotolayout, kein Band)', 1))

P.append((
 'typography:(b=l==null?void 0:l.currentBrandConfig)==null?void 0:b.typography})}finally{zFrei()}',
 'typography:(b=l==null?void 0:l.currentBrandConfig)==null?void 0:b.typography,ctaImage:(b=l==null?void 0:l.currentBrandConfig)==null?void 0:b.ctaImage})}finally{zFrei()}',
 'Editor-Vorschau (XV): CTA-Foto aus dem Stil mitgeben', 1))

P.append((
 'typography:We==null?void 0:We.typography});',
 'typography:We==null?void 0:We.typography,ctaImage:We==null?void 0:We.ctaImage});',
 'Exporte: CTA-Foto aus dem Stil mitgeben', 3))

# 277  CTA-Foto immer ueber die ganze Seite
#
#      "Hm, find ich nicht gut - und das CTA ueber die ganze Seite immer."
#
#      338 setzte das CTA-Foto nur, wenn die letzte Folie KEIN Foto hatte,
#      und liess das Layout aus der Reihe stehen. Bei ihr kam die letzte
#      Folie mit einem anderen Foto und einem Textlayout an - das
#      CTA-Bild lag dann als Schleier oder kleiner Ausschnitt hinter
#      der Flaeche. Jetzt: ist ein CTA-Foto gesetzt, bekommt die letzte
#      von mehreren Folien IMMER dieses Foto als Hintergrund und das
#      Layout brand_photo_gradient (Regler ctaLayout), egal was im Plan
#      steht. Ohne CTA-Foto, aber isCtaSlide mit Foto: ebenfalls
#      vollflaechig. Screenshot- und Ablauf-Folien bleiben ausgenommen.
#
#      GESICHTET: 7 Folien, die letzte waere ein Textlayout gewesen -
#      zeigt jetzt das Test-CTA (grau) ueber die ganze Seite.

P.append((
 'try{if(i&&typeof i.ctaImage=="string"&&i.ctaImage.length>5&&(Number(i.totalSlides)||1)>1&&(i.slideIndex||0)===(Number(i.totalSlides)||1)-1&&!(typeof t.background=="string"&&t.background.length>5)&&t.overlayIsScreenshot!==!0&&t.karte!=="ablauf"){const zL=String(t.layout||"");t={...t,background:i.ctaImage,isCtaSlide:!0,textBands:zL.indexOf("brand_")===0?void 0:t.textBands,layout:zL.indexOf("brand_")===0&&!/photo|frame/.test(zL)?"brand_photo_gradient":t.layout,layoutId:zL.indexOf("brand_")===0&&!/photo|frame/.test(zL)?"brand_photo_gradient":t.layoutId}}}catch(zz){}',
 'try{const zCtaBild=i&&typeof i.ctaImage=="string"&&i.ctaImage.length>5?i.ctaImage:"",zLetzte=(Number(i.totalSlides)||1)>1&&(i.slideIndex||0)===(Number(i.totalSlides)||1)-1,zHatBg=typeof t.background=="string"&&t.background.length>5;if(zLetzte&&t.overlayIsScreenshot!==!0&&t.karte!=="ablauf"&&(zCtaBild||(t.isCtaSlide===!0&&zHatBg))){const zL=String(t.layout||""),zBrand=zL.indexOf("brand_")===0||BS_KACHEL.folgeLayouts===1,zLay2=BS_KACHEL.ctaLayout||"brand_photo_gradient";t={...t,background:zCtaBild||t.background,isCtaSlide:!0,textBands:zBrand?void 0:t.textBands,layout:zBrand?zLay2:t.layout,layoutId:zBrand?zLay2:t.layoutId}}}catch(zz){}',
 'Zeichner: letzte Folie traegt immer das CTA-Foto vollflaechig (Fotolayout, kein Band), wenn eines gesetzt ist', 1))

# 278  Textkachel: Deckblatt ohne Foto
#
#      "Die erste Slide ohne Foto beim Textkachel." Das Foto aus 337
#      (blurred dahinter / klein ausgeschnitten) gilt nur noch fuer
#      Folgefolien; das Deckblatt einer Textkachel bleibt reine Flaeche.
#      Regler textFotoDeckblatt 1 schaltet es dort wieder ein.

P.append((
 'const zTF=(()=>{try{if(!BS_KACHEL.textFoto||t.overlayIsScreenshot===!0)return null;',
 'const zTF=(()=>{try{if(!BS_KACHEL.textFoto||t.overlayIsScreenshot===!0)return null;if((i.slideIndex||0)===0&&BS_KACHEL.textFotoDeckblatt!==1)return null;',
 'plate-Zweig: kein Foto (blur/inset) auf dem Deckblatt, nur Folgefolien', 1))

P.append((
 'textFoto:"blur|inset",',
 'textFoto:"blur|inset",textFotoDeckblatt:0,',
 'Regler textFotoDeckblatt 0', 1))

# 279  Inset ueberarbeitet: groesser, mittig, heller, Text darunter
#
#      Folie 3/16: "Cover mehr mittig zentriert, diese Groesse ist
#      irgendwie lame, das Foto zu dunkel - ueberarbeiten."
#
#      Das Foto der Textflaechen war .28 breit, oben mittig, der Text
#      darunter links (Layout brand_text_left) und die Aufhellung aus
#      327 fehlte, weil zLadeFoto() am Lader u() vorbeigeht. Jetzt:
#      Foto .5 breit, 1:1.2, ab .10 (bis etwa .58), Gamma-Aufhellung
#      auf hellZiel x 1.1 wie beim Deckblatt, darunter der Text mittig
#      mit .05 Luft, Headline .84 breit, Unterzeile ebenfalls mittig.
#      Die Blur-Fassung bekommt dieselbe Aufhellung.

P.append((
 'const zk=Math.max(zo.w/zim.width,zo.h/zim.height),zUeb=zim.height*zk-zo.h,zBias=typeof zo.bias=="number"?zo.bias:0;',
 'try{const zZ=Number(BS_KACHEL.hellZiel)||0,zel2=zim.getElement&&zim.getElement();if(zZ>0&&zel2&&zel2.width&&Pe.fabric.Image.filters&&Pe.fabric.Image.filters.Gamma){const zc2=document.createElement("canvas");zc2.width=zc2.height=16;const zx2=zc2.getContext("2d");zx2.drawImage(zel2,0,0,16,16);const zd2=zx2.getImageData(0,0,16,16).data;let zs2=0;for(let zi=0;zi<zd2.length;zi+=4)zs2+=.2126*zd2[zi]+.7152*zd2[zi+1]+.0722*zd2[zi+2];const zm2=zs2/(zd2.length/4),zg2=Math.min(Number(BS_KACHEL.hellGammaMax)||1.7,Math.max(1,Math.pow((zZ*(Number(BS_KACHEL.textFotoHell)||1))/Math.max(1,zm2),Number(BS_KACHEL.hellKraft)||.8)));if(zg2>1.015){zim.filters=(zim.filters||[]).concat([new Pe.fabric.Image.filters.Gamma({gamma:[zg2,zg2,zg2]})]);zim.applyFilters()}}}catch(zz){}const zk=Math.max(zo.w/zim.width,zo.h/zim.height),zUeb=zim.height*zk-zo.h,zBias=typeof zo.bias=="number"?zo.bias:0;',
 'zLadeFoto(): Aufhellung per Gamma auf hellZiel x textFotoHell, wie im Deckblatt-Lader', 1))

P.append((
 'const zW=r*(Number(BS_KACHEL.textFotoBreite)||.28),zH=zW*1.25,zY=n*(Number(BS_KACHEL.textFotoOben)||.10);',
 'const zW=r*(Number(BS_KACHEL.textFotoBreite)||.5),zH=zW*(Number(BS_KACHEL.textFotoHoehe)||1.2),zY=n*(Number(BS_KACHEL.textFotoOben)||.10);',
 'Inset: Breite .5 statt .28, Hoehe per textFotoHoehe', 1))

P.append((
 'let tt=ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?n*(Number(BS_KACHEL.lisaTextMitte)||.58):ge.textPos==="top"?n*.24:n*.5;const Qt=ge.textPos==="top"&&BS_KACHEL.lisaUnten!==1?"top":"center";',
 'let tt=zInsetUnten>0?zInsetUnten+n*(Number(BS_KACHEL.textFotoLuft)||.05):ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?n*(Number(BS_KACHEL.lisaTextMitte)||.58):ge.textPos==="top"?n*.24:n*.5;const Qt=zInsetUnten>0?"top":ge.textPos==="top"&&BS_KACHEL.lisaUnten!==1?"top":"center";',
 'plate-Zweig: Text unter dem Inset (originY top, Luft textFotoLuft)', 1))

P.append((
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:Ye,top:tt,originX:et,originY:Qt,width:r*(kt?.78:ge.exactWidth||(ht?.8:.74)),maxWidth:kt?r*.82:void 0,',
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,top:tt,originX:zInsetUnten>0?"center":et,originY:Qt,width:r*(zInsetUnten>0?.84:kt?.78:ge.exactWidth||(ht?.8:.74)),maxWidth:kt?r*.82:void 0,',
 'plate-Zweig: Headline unter dem Inset mittig, Breite .84', 1))

P.append((
 'goldOk:_t,minFontSize:kt?r*(56/1080):void 0,fill:me,accentFill:Oe,textAlign:lt,lineHeight:',
 'goldOk:_t,minFontSize:kt?r*(56/1080):void 0,fill:me,accentFill:Oe,textAlign:zInsetUnten>0?"center":lt,lineHeight:',
 'plate-Zweig: Headline unter dem Inset zentriert', 1))

P.append((
 'if(zSp&&zUnter(zHt,zSp.unten,me,lt==="left",Ye),',
 'if(zSp&&zUnter(zHt,zSp.unten,me,zInsetUnten>0?!1:lt==="left",Ye),',
 'plate-Zweig: Unterzeile unter dem Inset zentriert', 1))

P.append((
 'textFotoBreite:.28,textFotoOben:.10,',
 'textFotoBreite:.5,textFotoHoehe:1.2,textFotoOben:.10,textFotoLuft:.05,textFotoHell:1.1,',
 'Regler: textFotoBreite .5, textFotoHoehe 1.2, textFotoLuft .05, textFotoHell 1.1', 1))

# 280  Inset-Aufhellung: Person statt Fenster messen
#
#      "Findest du es heller?" - kaum: 109 -> 114 im Mittel. Ihr Foto
#      ist Gegenlicht: helles Fenster, sie selbst dunkel. Die Messung
#      ueber das ganze Bild sah keinen Bedarf (Gamma 1,01). Jetzt
#      werden nur die Bildmitte (x 25-75 %, ab y 25 %) und dort die
#      dunkleren 40 % der Proben gemittelt; Ziel hellZiel x .9 dafuer.
#      Cap bleibt hellGammaMax 1.7, Kraft hellKraft .8.
#
#      GEMESSEN an einem synthetischen Gegenlicht-Portraet (nacheinander
#      gerendert - parallele Laeufe mit verschiedenen Bundles sind
#      ungueltig, sie schreiben dieselbe index.html um):
#        Person   69 -> 113      Inset-Mittel 173 -> 197
#      Fenster bleibt hell, ohne auszubrennen.

P.append((
 'const zd2=zx2.getImageData(0,0,16,16).data;let zs2=0;for(let zi=0;zi<zd2.length;zi+=4)zs2+=.2126*zd2[zi]+.7152*zd2[zi+1]+.0722*zd2[zi+2];const zm2=zs2/(zd2.length/4),zg2=Math.min(Number(BS_KACHEL.hellGammaMax)||1.7,Math.max(1,Math.pow((zZ*(Number(BS_KACHEL.textFotoHell)||1))/Math.max(1,zm2),Number(BS_KACHEL.hellKraft)||.8)));',
 'const zd2=zx2.getImageData(0,0,16,16).data,zL2=[];for(let zy=0;zy<16;zy++)for(let zx=0;zx<16;zx++){if(zx<4||zx>=12||zy<4)continue;const zi=(zy*16+zx)*4;zL2.push(.2126*zd2[zi]+.7152*zd2[zi+1]+.0722*zd2[zi+2])}zL2.sort((za,zb)=>za-zb);const zN2=Math.max(1,Math.round(zL2.length*(Number(BS_KACHEL.textFotoAnteil)||.4)));let zs2=0;for(let zi=0;zi<zN2;zi++)zs2+=zL2[zi];const zm2=zs2/zN2,zg2=Math.min(Number(BS_KACHEL.hellGammaMax)||1.7,Math.max(1,Math.pow((zZ*(Number(BS_KACHEL.textFotoHell)||1))/Math.max(1,zm2),Number(BS_KACHEL.hellKraft)||.8)));',
 'zLadeFoto(): Aufhellung misst die dunkleren 40 % der Bildmitte (Person im Gegenlicht), nicht das ganze Bild', 1))

P.append((
 'textFotoHell:1.1,',
 'textFotoHell:.9,textFotoAnteil:.4,',
 'Regler textFotoHell .9, textFotoAnteil .4', 1))

# 281  Textkachel-Deckblatt mittig
#
#      "Gut - und Cover jetzt mehr mittig." Der Textblock der
#      Textflaechen stand seit 333 bei .58 (auf ihren Wunsch "immer
#      runter"). Fuer das Deckblatt gilt jetzt .5, und wenn eine
#      Unterzeile folgt, rueckt die Headline um .045 hoch, damit der
#      ganze Block mittig sitzt. Folgefolien bleiben bei .58. Dafuer
#      wird die Satzaufteilung vor der Lage berechnet.

P.append((
 'let tt=zInsetUnten>0?zInsetUnten+n*(Number(BS_KACHEL.textFotoLuft)||.05):ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?n*(Number(BS_KACHEL.lisaTextMitte)||.58):',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null;let tt=zInsetUnten>0?zInsetUnten+n*(Number(BS_KACHEL.textFotoLuft)||.05):ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?((i.slideIndex||0)===0?n*(Number(BS_KACHEL.lisaDeckMitte)||.5)-(zSp?n*(Number(BS_KACHEL.lisaDeckHub)||.045):0):n*(Number(BS_KACHEL.lisaTextMitte)||.58)):',
 'plate-Zweig: Aufteilung vor der Lage berechnen; Deckblatt-Block mittig (.5, bei Unterzeile .045 hoeher), Folgefolien bleiben .58', 1))

P.append((
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null,zOb=zSp?ye(zSp.oben):null,zHt=Pt(',
 'const zOb=zSp?ye(zSp.oben):null,zHt=Pt(',
 'plate-Zweig: zOb/zHt nutzen die vorgezogene Aufteilung', 1))

P.append((
 'lisaTextMitte:.58,',
 'lisaTextMitte:.58,lisaDeckMitte:.5,lisaDeckHub:.045,',
 'Regler lisaDeckMitte .5, lisaDeckHub .045', 1))

# 282  Dunkles Lila statt Schwarz
#
#      "Koennen wir statt schwarz ein dunkles Lila machen?"
#      Grundton #1E1436 (tiefes Violett, Leuchtdichte etwa 22). Er geht
#      ueberall hin, wo bisher Schwarz stand: dunkle Textflaechen,
#      Rahmen-Layouts, Folgefolien, Schleier hinter den Fotos (zGrund
#      faengt alles unter Leuchtdichte 45), Screenshot-Folien im
#      Band-Zweig und der Leinwandgrund. Weiss und Off-White bleiben.
#      Ein Regler: lisaGrund - zurueck zu Schwarz mit "#000000".
#
#      GESICHTET: Raster (Tag 5 und 3 lila, Fotos mit leichtem
#      Lila-Schleier), Karussell, Screenshot-Folie.

P.append((
 'lisaGrund:"#000000",',
 'lisaGrund:"#1E1436",',
 'Regler lisaGrund: dunkles Lila #1E1436', 1))

P.append((
 'colors:{primary:"#FFFFFF",secondary:"#000000",tertiary:"#8E8E92",accent:"#FFFFFF",neutral:"#000000",background:"#000000",darkPlate:"#000000"}',
 'colors:{primary:"#FFFFFF",secondary:"#1E1436",tertiary:"#8E8E92",accent:"#FFFFFF",neutral:"#1E1436",background:"#1E1436",darkPlate:"#1E1436"}',
 'Stil-Objekt G2: Grund, Sekundaer, Neutral, darkPlate im Lila', 1))

P.append((
 'textTileLight:"#FFFFFF",textTileDark:"#000000"',
 'textTileLight:"#FFFFFF",textTileDark:"#1E1436"',
 'Textflaechen dunkel: Lila', 1))

P.append((
 'et=!$e&&Ye.grundFarbe?Ye.grundFarbe:String(t.plateOverride||t.backgroundColor||"#000000"),lt=(zGrundTon=et,!_C(et))',
 'et=(zx=>{try{return BS_KACHEL.lisaGrund&&w(zx)<45?BS_KACHEL.lisaGrund:zx}catch(zz){return zx}})(!$e&&Ye.grundFarbe?Ye.grundFarbe:String(t.plateOverride||t.backgroundColor||"#000000")),lt=(zGrundTon=et,!_C(et))',
 'Band-Zweig (Screenshot-Folien): fast-schwarzer Grund -> Lila', 1))

P.append((
 'e.clear(),e.setBackgroundColor(t.backgroundColor||"#ffffff",()=>{',
 'e.clear(),e.setBackgroundColor((zx=>{try{let zh=String(zx).replace("#","");if(zh.length===3)zh=zh.split("").map(zq=>zq+zq).join("");const zl=.2126*parseInt(zh.slice(0,2),16)+.7152*parseInt(zh.slice(2,4),16)+.0722*parseInt(zh.slice(4,6),16);return BS_KACHEL.lisaGrund&&zl<45?BS_KACHEL.lisaGrund:zx}catch(zz){return zx}})(t.backgroundColor||"#ffffff"),()=>{',
 'Leinwandgrund: fast-schwarz -> Lila', 1))

# 283  Schwarz bleibt, Betonungen leuchtend lila
#
#      "Ok, lass schwarz - mach aber Worte leuchtend lila."
#      Grund wieder #000000 (344 war ein Tag lang lila). Die Betonung
#      in den Layouts - kursiv, bisher in Textfarbe - bekommt jetzt
#      lisaAkzent #A855F7. Sie greift bei *markierten* Woertern und,
#      wenn nichts markiert ist, automatisch bei den letzten zwei
#      Woertern der Headline samt Satzzeichen (zAkz, Regler
#      lisaAkzentAuto 1 / lisaAkzentWorte 2). Headlines mit weniger
#      als drei Woertern bleiben ohne. Kursiv ist synthetisch, weil
#      Playfair nur als Regular liegt.
#
#      GESICHTET: Raster und Karussell - letzte zwei Woerter lila
#      kursiv auf Schwarz, Weiss und Foto.

P.append((
 'lisaGrund:"#1E1436",',
 'lisaGrund:"#000000",lisaAkzent:"#A855F7",lisaAkzentAuto:1,lisaAkzentWorte:2,',
 'Regler: lisaGrund zurueck auf Schwarz, lisaAkzent #A855F7, lisaAkzentAuto 1, lisaAkzentWorte 2', 1))

P.append((
 'colors:{primary:"#FFFFFF",secondary:"#1E1436",tertiary:"#8E8E92",accent:"#FFFFFF",neutral:"#1E1436",background:"#1E1436",darkPlate:"#1E1436"}',
 'colors:{primary:"#FFFFFF",secondary:"#000000",tertiary:"#8E8E92",accent:"#A855F7",neutral:"#000000",background:"#000000",darkPlate:"#000000"}',
 'Stil-Objekt G2: Schwarz zurueck, accent lila', 1))

P.append((
 'textTileLight:"#FFFFFF",textTileDark:"#1E1436"',
 'textTileLight:"#FFFFFF",textTileDark:"#000000"',
 'Textflaechen dunkel: Schwarz', 1))

P.append((
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=me,',
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me,',
 'gradient-Zweig: Akzentfarbe lisaAkzent', 1))

P.append((
 'me=zFarbe(Fe),Oe=me;',
 'me=zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me;',
 'plate- und frame-Zweig: Akzentfarbe lisaAkzent', 2))

P.append((
 'zTeilen=(zx,zKurz)=>{',
 'zAkz=zs=>{try{if(BS_KACHEL.lisaAkzentAuto!==1||!Array.isArray(zs)||!zs.length||zs.some(zq=>zq&&(zq.accent||zq.bold||zq.gold||zq.big)))return zs;const zt=zs.map(zq=>zq.text||"").join("");const zw=zt.split(/(\\s+)/);const zWo=zw.filter((zq,zi)=>zi%2===0&&zq);if(zWo.length<3)return zs;const zn=Math.max(1,Math.min(Number(BS_KACHEL.lisaAkzentWorte)||2,zWo.length-1));let zc=0,zIdx=zw.length;for(let zi=zw.length-1;zi>=0;zi--){if(zi%2===0&&zw[zi]){zc++;if(zc===zn){zIdx=zi;break}}}const zHead=zw.slice(0,zIdx).join(""),zRest=zw.slice(zIdx).join("");if(!zRest.trim())return zs;const zOut=[];zHead&&zOut.push({text:zHead,accent:!1,bold:!1});zOut.push({text:zRest,accent:!0,bold:!1});return zOut.map(zq=>zq.text).join("")===zt?zOut:zs}catch(zz){return zs}},zTeilen=(zx,zKurz)=>{',
 'zAkz(): ohne Markierung die letzten zwei Woerter (samt Satzzeichen) als Akzent', 1))

P.append((
 'zHt=Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,',
 'zHt=Pt(zAkz(zOb?zOb.segments:ht),zOb?zOb.plain:qe,{left:br,',
 'gradient-Zweig: Headline durch zAkz', 1))

P.append((
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'zHt=Pt(zAkz(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'plate-Zweig: Headline durch zAkz', 1))

P.append((
 'const zHt=Pt($e,Qe,{left:r/2,top:zIn?',
 'const zHt=Pt(zAkz($e),Qe,{left:r/2,top:zIn?',
 'frame-Zweig: Headline durch zAkz', 1))

# 284  Lila-Akzent wieder weg
#
#      "Nimm es wieder weg und schalte einen Designer Agent ein, der
#      entscheidet, welche Farbe besser waere." Genau die fuenf
#      Aenderungen aus 283 rueckgaengig: Akzentfarbe wieder Textfarbe,
#      zAkz() nicht mehr aufgerufen (bleibt als tote Funktion stehen),
#      die drei lisaAkzent*-Regler weg. Schwarzer Grund aus 345 bleibt.
#      Naechster Schritt: ein Subagent bekommt den Marken-Kontext und
#      entscheidet ueber eine Akzentfarbe.

P.append((
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me,',
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=me,',
 'gradient-Zweig: Akzentfarbe zurueck auf Textfarbe', 1))

P.append((
 'me=zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me;',
 'me=zFarbe(Fe),Oe=me;',
 'plate- und frame-Zweig: Akzentfarbe zurueck auf Textfarbe', 2))

P.append((
 'zHt=Pt(zAkz(zOb?zOb.segments:ht),zOb?zOb.plain:qe,{left:br,',
 'zHt=Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,',
 'gradient-Zweig: zAkz()-Aufruf entfernt', 1))

P.append((
 'zHt=Pt(zAkz(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'plate-Zweig: zAkz()-Aufruf entfernt', 1))

P.append((
 'const zHt=Pt(zAkz($e),Qe,{left:r/2,top:zIn?',
 'const zHt=Pt($e,Qe,{left:r/2,top:zIn?',
 'frame-Zweig: zAkz()-Aufruf entfernt', 1))

P.append((
 'lisaGrund:"#000000",lisaAkzent:"#A855F7",lisaAkzentAuto:1,lisaAkzentWorte:2,',
 'lisaGrund:"#000000",',
 'Regler lisaAkzent/lisaAkzentAuto/lisaAkzentWorte entfernt', 1))

# 285  Akzentfarbe per Design-Subagent: Clay Rust statt Lila
#
#      "Nimm es wieder weg und schalte einen Designer Agent ein, der
#      entscheidet, welche Farbe besser waere." 284 hat das Lila
#      entfernt (zAkz() blieb als tote Funktion stehen). Ein Subagent
#      (general-purpose, als Brand-/Grafikdesigner gebrieft) hat die
#      Referenzbilder gesichtet - ihren eigenen Feed, lisa.contentdesign
#      (die sie nicht kopieren will) und juliaknauber_coaching (ihr
#      genanntes Vorbild) - und sich fuer GENAU EINE Farbe entschieden:
#
#        "Clay Rust" #B5622C - gebranntes Terrakotta/Rostrot.
#
#      Begruendung des Agenten: Kontrast ~5.5:1 auf Schwarz und ~3.8:1
#      auf Weiss (WCAG-AA fuer grosse/fette Schrift), warm statt
#      "AI-generic" wie das Lila, harmoniert mit den warmen Hauttoenen
#      ihrer Fotos, klar unterscheidbar von Lisas Schokobraun/Creme
#      (dort Flaechenfarbe, hier nur punktueller Akzent). Auf Fotos
#      empfahl der Agent einen leichten Schatten - die bestehende
#      Scrim-Abdunklung hinter der Schrift (gradient-Zweig) uebernimmt
#      diese Aufgabe bereits, kein zusaetzlicher Schatten noetig.
#
#      UMSETZUNG: dieselben fuenf Stellen wie in 283, nur der
#      Farbwert getauscht; zAkz() (Auto-Betonung letzte 1-2 Woerter,
#      Regler lisaAkzentAuto/lisaAkzentWorte) unveraendert aus 283/346.
#
#      GESICHTET: Raster und Karussell - Rostrot auf Schwarz, Weiss
#      und Foto.

P.append((
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=me,',
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me,',
 'gradient-Zweig: Akzentfarbe lisaAkzent', 1))

P.append((
 'me=zFarbe(Fe),Oe=me;',
 'me=zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me;',
 'plate- und frame-Zweig: Akzentfarbe lisaAkzent', 2))

P.append((
 'zHt=Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,',
 'zHt=Pt(zAkz(zOb?zOb.segments:ht),zOb?zOb.plain:qe,{left:br,',
 'gradient-Zweig: Headline durch zAkz', 1))

P.append((
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'zHt=Pt(zAkz(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'plate-Zweig: Headline durch zAkz', 1))

P.append((
 'const zHt=Pt($e,Qe,{left:r/2,top:zIn?',
 'const zHt=Pt(zAkz($e),Qe,{left:r/2,top:zIn?',
 'frame-Zweig: Headline durch zAkz', 1))

P.append((
 'lisaGrund:"#000000",',
 'lisaGrund:"#000000",lisaAkzent:"#B5622C",lisaAkzentAuto:1,lisaAkzentWorte:2,',
 'Regler lisaAkzent Clay Rust #B5622C, lisaAkzentAuto 1, lisaAkzentWorte 2', 1))

# 286  Lila doch richtig - ihre Videos nutzen es schon
#
#      "Ich hab aber bei meinen Videos lila im Hintergrund." Der
#      Design-Agent aus 285 kannte diesen Teil ihrer Marke nicht - fuer
#      ihn war Lila nur "ein getestetes Neon ohne erkennbaren Grund".
#      Mit dieser Information ist Lila kein Zufallston, sondern
#      bestehende Markenfarbe. Zurueck auf #A855F7, sonst nichts
#      geaendert (zAkz-Mechanik, Kontrast-Ueberlegungen von 283/285
#      gelten unveraendert weiter).

P.append((
 'lisaAkzent:"#B5622C",',
 'lisaAkzent:"#A855F7",',
 'Regler lisaAkzent: zurueck auf Lila #A855F7', 1))

# 287  Lila an ihr Video angeglichen
#
#      Screenshot vom Videohintergrund geschickt. Gemessen: der
#      gedimmte Streifen links im Bild liegt bei #55199E (gemittelt)
#      bis #7323D1 (Spitze), Farbton ~267 Grad - fast identisch mit
#      dem bisherigen Akzent #A855F7 (Farbton ~271 Grad). Gleiche
#      Lila-Familie, ihr Video nur dunkler, weil Umgebungslicht statt
#      Textfarbe. #9142F0 nimmt denselben Farbton, angehoben auf
#      Kontrast 4.24:1 (Schwarz) / 4.95:1 (Weiss) - kraeftiger/naeher
#      am Video als #A855F7 (5.31 / 3.96), beide bestehen WCAG-AA fuer
#      grosse Schrift.

P.append((
 'lisaAkzent:"#A855F7",',
 'lisaAkzent:"#9142F0",',
 'Regler lisaAkzent: an ihr Video angeglichen #9142F0', 1))

# 288  Kein Farbakzent - schwarz-weiss
#
#      "Nein keine, lass es schwarz weiss." Nach zwei Anlaeufen (Lila
#      A855F7, dann an ihr Video angeglichen 9142F0) will sie doch
#      keine Akzentfarbe. Gleicher Rueckbau wie in 284: Akzentfarbe
#      wieder Textfarbe, zAkz() nicht mehr aufgerufen (bleibt tot
#      stehen), die drei lisaAkzent*-Regler weg. Betonte Woerter sind
#      wieder schlicht kursiv in Textfarbe.

P.append((
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me,',
 'me=$?(BS_KACHEL.lisaHell||X(t.color,$,Fe)):zFarbe(Fe),Oe=me,',
 'gradient-Zweig: Akzentfarbe zurueck auf Textfarbe', 1))

P.append((
 'me=zFarbe(Fe),Oe=BS_KACHEL.lisaAkzent||me;',
 'me=zFarbe(Fe),Oe=me;',
 'plate- und frame-Zweig: Akzentfarbe zurueck auf Textfarbe', 2))

P.append((
 'zHt=Pt(zAkz(zOb?zOb.segments:ht),zOb?zOb.plain:qe,{left:br,',
 'zHt=Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,',
 'gradient-Zweig: zAkz()-Aufruf entfernt', 1))

P.append((
 'zHt=Pt(zAkz(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'plate-Zweig: zAkz()-Aufruf entfernt', 1))

P.append((
 'const zHt=Pt(zAkz($e),Qe,{left:r/2,top:zIn?',
 'const zHt=Pt($e,Qe,{left:r/2,top:zIn?',
 'frame-Zweig: zAkz()-Aufruf entfernt', 1))

P.append((
 'lisaGrund:"#000000",lisaAkzent:"#9142F0",lisaAkzentAuto:1,lisaAkzentWorte:2,',
 'lisaGrund:"#000000",',
 'Regler lisaAkzent/lisaAkzentAuto/lisaAkzentWorte entfernt', 1))

# 289  Lila Licht von links oben
#
#      "Koenntest du aeh wie so ein lila Licht auf der linken Seite
#      oder linken oberen Seite machen?" - meint das Umgebungslicht
#      aus ihrem Video (Screenshot 40671fb3, dieselbe Aufnahme, aus
#      der 287 die Akzentfarbe massa). Kein Textakzent mehr (288 nahm
#      den zurueck), sondern ein weicher Lichtschein im Bild selbst:
#      radialer Verlauf, Mittelpunkt knapp links ausserhalb der Karte
#      und im oberen Drittel (x -.15, y .30 relativ), Radius .85 der
#      groesseren Kante, Farbe #7323D1 (die hellere der beiden
#      gemessenen Video-Werte, hier als Licht statt als Textfarbe -
#      darf kraeftiger sein), Staerke .42 in der Mitte, nach aussen
#      auf 0.
#
#      NUR auf dunklem Grund (w(Fe)<60) - auf Weiss waere es ein
#      Farbfleck statt Licht. NUR auf Karten ohne eigenes Foto in der
#      Ecke (plate-Zweig: nicht wenn zTF gesetzt ist) - sonst haette
#      das Licht das Foto eingefaerbt. Foto-Deckblaetter (gradient-
#      Zweig) und Screenshot-Folien bleiben unberuehrt.
#
#      GESICHTET: Raster (Tag 5 schwarze Textkarte, Tag 3 Rahmen-Layout
#      mit kleinem Foto - beide mit Licht; Tag 8/2 weiss und die
#      Foto-Deckblaetter unveraendert) und Karussell.

P.append((
 'e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1}));const zIn=ge.inset===!0&&$,',
 'e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1}));(()=>{try{if(!BS_KACHEL.lisaLicht||!1||w(Fe)>=60)return;const zCx=r*(Number(BS_KACHEL.lisaLichtX)??-.15),zCy=n*(Number(BS_KACHEL.lisaLichtY)??.30),zR=r*(Number(BS_KACHEL.lisaLichtRadius)||.85),zSt=Number(BS_KACHEL.lisaLichtStaerke)||.42;e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"radial",coords:{x1:zCx,y1:zCy,r1:0,x2:zCx,y2:zCy,r2:zR},colorStops:[{offset:0,color:G(BS_KACHEL.lisaLicht,zSt)},{offset:1,color:G(BS_KACHEL.lisaLicht,0)}]})}))}catch(zz){}})();const zIn=ge.inset===!0&&$,',
 'frame-Zweig: lila Licht von links oben, direkt nach der Grundflaeche', 1))

P.append((
 'zInsetUnten=zY+zH}if(ge.rule&&ee(me)&&BS_KACHEL.lisaRahmen!==0){',
 'zInsetUnten=zY+zH}(()=>{try{if(!BS_KACHEL.lisaLicht||zTF||w(Fe)>=60)return;const zCx=r*(Number(BS_KACHEL.lisaLichtX)??-.15),zCy=n*(Number(BS_KACHEL.lisaLichtY)??.30),zR=r*(Number(BS_KACHEL.lisaLichtRadius)||.85),zSt=Number(BS_KACHEL.lisaLichtStaerke)||.42;e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"radial",coords:{x1:zCx,y1:zCy,r1:0,x2:zCx,y2:zCy,r2:zR},colorStops:[{offset:0,color:G(BS_KACHEL.lisaLicht,zSt)},{offset:1,color:G(BS_KACHEL.lisaLicht,0)}]})}))}catch(zz){}})();if(ge.rule&&ee(me)&&BS_KACHEL.lisaRahmen!==0){',
 'plate-Zweig: lila Licht von links oben, nach dem optionalen Foto (nur ohne eigenes Kartenfoto)', 1))

P.append((
 'lisaGrund:"#000000",',
 'lisaGrund:"#000000",lisaLicht:"#7323D1",lisaLichtStaerke:.42,lisaLichtRadius:.85,lisaLichtX:-.15,lisaLichtY:.30,',
 'Regler lisaLicht/-Staerke/-Radius/-X/-Y', 1))

# 290  Serifenlos, Licht ueberall und variiert, gelegentlich Lila-Karten
#
#      "Aendere bitte die Schrift in ein Non-Serif, Helvetica oder
#      Inter. Mach bitte auch bei den weissen Slides das lila Licht
#      und auch bei den Fotoslides. Variier ein bisschen, wo du das
#      Licht setzt. Mach bitte manchmal auch eine, ein dunkleres Lila
#      als das Lila fuers Licht als Hintergrund, und dann Lila und
#      weisse Schrift."
#
#      VIER AENDERUNGEN IN EINEM SCHRITT:
#
#      1. SCHRIFT: Playfair Display raus, HelveticaNeueBrand rein - an
#         allen Stellen, die tatsaechlich im aktiven Pfad liegen
#         (lisaSchrift-Regler, Screenshot-Hook, Fotoschrift, alte
#         Kachel-Folgefolien, Ablauf-Titel, Kasten, sowie zwei fest
#         verdrahtete Stellen: die Versal-Unterzeile aus 279 und die
#         Inset-Unterzeile aus 281 folgen jetzt ebenfalls lisaSchrift
#         statt eines eigenen Playfair-Literals). Ad-Vorlagen (separate
#         te==="ad_*"-Zweige) und die boldMode-Sonderfassung in Pt()
#         bleiben unberuehrt - fuer ihre normalen Slides nie erreicht.
#
#      2. LICHT UEBERALL, VARIIERT: zLichtZeichnen() ersetzt die beiden
#         IIFEs aus 289. Es zeichnet jetzt auch auf hellem Grund
#         (eigene, schwaechere Staerke lisaLichtStaerkeHell .16 statt
#         .42) und im gradient-Zweig (Foto-Deckblaetter), direkt nach
#         der Verlaufsflaeche/Foto. Position kommt aus zLichtPos() -
#         ein Hash aus Tag, Folienindex und Textanfang waehlt einen von
#         vier Punkten (links oben, links mitte, ganz oben links eng,
#         links unten) - je Karte fest, aber uebers Set verteilt.
#
#      3. GELEGENTLICH LILA-KARTEN: zGrundWahl() ersetzt in plate- und
#         frame-Zweig die feste lisaGrund-Grundfarbe. Mit Anteil
#         lisaGrundDunkelAnteil (.28, per-Karte-Hash) wird statt
#         Schwarz die tiefere Farbe lisaGrundDunkel (#2A1150) verwendet
#         - deutlich dunkler als das Licht-Lila #7323D1. zFarbe() liest
#         diese Karten automatisch als dunkel und setzt weisse Schrift
#         von selbst. Nur auf diesen Karten (zVar=Fe===lisaGrundDunkel)
#         wird zAkz() wieder aufgerufen und Oe auf lisaAkzent2 (#C4B5FD,
#         helles Flieder, Kontrast 8.8:1 auf #2A1150) gesetzt - die
#         letzten ein bis zwei Woerter der Headline stehen dort lila.
#         Weisse und Foto-Karten bleiben unveraendert (kein zVar).
#
#      GEPRUEFT (Kontrastrechner): lisaGrundDunkel #2A1150 gegen Weiss
#      16.2:1; lisaAkzent2 #C4B5FD gegen lisaGrundDunkel 8.8:1.
#
#      GESICHTET: Raster (Foto-Deckblaetter und Weiss jetzt auch mit
#      Licht, an unterschiedlichen Stellen), ein erzwungenes
#      brand_text_left mit vorberechnetem Hash-Treffer (Tag 4:
#      Flieder-Grund, weisser Fliesstext, "Denken." in Lila-Kursiv),
#      Karussell, Screenshot-Folie (Schrift sans, kein Licht - wie
#      zuvor unberuehrt).

P.append((
 'deckblattFamilie:"Playfair Display",fotoSchrift:"Playfair Display",',
 'deckblattFamilie:"HelveticaNeueBrand",fotoSchrift:"HelveticaNeueBrand",',
 'Schrift: Screenshot-Hook und Fotoschrift von Playfair auf Helvetica', 1))

P.append((
 'folgeFamilie:"Playfair Display",ablaufTitel:"Playfair Display",',
 'folgeFamilie:"HelveticaNeueBrand",ablaufTitel:"HelveticaNeueBrand",',
 'Schrift: Folgefolien-Familie (alte Kachel) und Ablauf-Titel auf Helvetica', 1))

P.append((
 'lisaSchrift:"Playfair Display",',
 'lisaSchrift:"HelveticaNeueBrand",',
 'Schrift: lisaSchrift-Regler auf Helvetica', 1))

P.append((
 'kastenSchrift:"Playfair Display"',
 'kastenSchrift:"HelveticaNeueBrand"',
 'Schrift: Kasten-Schrift auf Helvetica', 1))

P.append((
 'fontSize:zg,fontFamily:"Playfair Display",fontWeight:"400",fill:G(zF,.92)',
 'fontSize:zg,fontFamily:BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",fontWeight:"400",fill:G(zF,.92)',
 'Schrift: Versal-Unterzeile (zUnter) folgt lisaSchrift statt Playfair', 1))

P.append((
 'fontSize:Math.round(r*(Number(BS_KACHEL.lisaInsetUnten)||.046)),fontFamily:"Playfair Display",fontWeight:"400",fill:me,textAlign:"center"',
 'fontSize:Math.round(r*(Number(BS_KACHEL.lisaInsetUnten)||.046)),fontFamily:BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",fontWeight:"400",fill:me,textAlign:"center"',
 'Schrift: Inset-Unterzeile (frame-Zweig) folgt lisaSchrift statt Playfair', 1))

P.append((
 'zGrund=zg=>{',
 'zGrundWahl=()=>{try{const zA=Number(BS_KACHEL.lisaGrundDunkelAnteil)||0,zG=BS_KACHEL.lisaGrund||"#000000";if(!(zA>0))return zG;const zS=String(t._tag)+"|"+String(i.slideIndex||0)+"|"+String(t.text||"").slice(0,16)+"|g";let zh=0;for(let zi=0;zi<zS.length;zi++)zh=(zh*31+zS.charCodeAt(zi))%99991;return (zh%1000)/1000<zA?(BS_KACHEL.lisaGrundDunkel||"#2A1150"):zG}catch(zz){return BS_KACHEL.lisaGrund||"#000000"}},zLichtPos=()=>{try{const zS=String(t._tag)+"|"+String(i.slideIndex||0)+"|"+String(t.text||"").slice(0,16)+"|l";let zh=0;for(let zi=0;zi<zS.length;zi++)zh=(zh*31+zS.charCodeAt(zi))%99991;const zP=[[-.15,.18,.85],[-.20,.46,.80],[-.08,.06,.75],[-.18,.66,.90]];return zP[zh%zP.length]}catch(zz){return[-.15,.30,.85]}},zLichtZeichnen=(zFarbGrund,zAus)=>{try{if(!BS_KACHEL.lisaLicht||zAus)return;const zHell=w(zFarbGrund)>=60,zSt=zHell?(Number(BS_KACHEL.lisaLichtStaerkeHell)??.16):(Number(BS_KACHEL.lisaLichtStaerke)||.42);if(!(zSt>0))return;const zPk=zLichtPos(),zCx=r*zPk[0],zCy=n*zPk[1],zR=r*(zPk[2]||.85);e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"radial",coords:{x1:zCx,y1:zCy,r1:0,x2:zCx,y2:zCy,r2:zR},colorStops:[{offset:0,color:G(BS_KACHEL.lisaLicht,zSt)},{offset:1,color:G(BS_KACHEL.lisaLicht,0)}]})}))}catch(zz){}},zGrund=zg=>{',
 'Helfer zGrundWahl/zLichtPos/zLichtZeichnen definiert', 1))

P.append((
 'Fe=ge&&ge.plateColor?ge.plateColor:(BS_KACHEL.lisaGrund||zGrund(t.plateOverride||t.backgroundColor||"#E8E8E8")),me=zFarbe(Fe),Oe=me;',
 'Fe=ge&&ge.plateColor?ge.plateColor:zGrundWahl(),me=zFarbe(Fe),zVar=Fe===(BS_KACHEL.lisaGrundDunkel||"#2A1150"),Oe=zVar?(BS_KACHEL.lisaAkzent2||"#C4B5FD"):me;',
 'plate- und frame-Zweig: Grundfarbe ueber zGrundWahl, Betonungsfarbe/-Variante ueber zVar', 2))

P.append((
 '(()=>{try{if(!BS_KACHEL.lisaLicht||!1||w(Fe)>=60)return;const zCx=r*(Number(BS_KACHEL.lisaLichtX)??-.15),zCy=n*(Number(BS_KACHEL.lisaLichtY)??.30),zR=r*(Number(BS_KACHEL.lisaLichtRadius)||.85),zSt=Number(BS_KACHEL.lisaLichtStaerke)||.42;e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"radial",coords:{x1:zCx,y1:zCy,r1:0,x2:zCx,y2:zCy,r2:zR},colorStops:[{offset:0,color:G(BS_KACHEL.lisaLicht,zSt)},{offset:1,color:G(BS_KACHEL.lisaLicht,0)}]})}))}catch(zz){}})();',
 'zLichtZeichnen(Fe,!1);',
 'frame-Zweig: Licht ueber zLichtZeichnen (variierte Position, auch auf Weiss/Foto)', 1))

P.append((
 'zInsetUnten=zY+zH}(()=>{try{if(!BS_KACHEL.lisaLicht||zTF||w(Fe)>=60)return;const zCx=r*(Number(BS_KACHEL.lisaLichtX)??-.15),zCy=n*(Number(BS_KACHEL.lisaLichtY)??.30),zR=r*(Number(BS_KACHEL.lisaLichtRadius)||.85),zSt=Number(BS_KACHEL.lisaLichtStaerke)||.42;e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"radial",coords:{x1:zCx,y1:zCy,r1:0,x2:zCx,y2:zCy,r2:zR},colorStops:[{offset:0,color:G(BS_KACHEL.lisaLicht,zSt)},{offset:1,color:G(BS_KACHEL.lisaLicht,0)}]})}))}catch(zz){}})();',
 'zInsetUnten=zY+zH}zLichtZeichnen(Fe,!!zTF);',
 'plate-Zweig: Licht ueber zLichtZeichnen (kein Licht wenn eigenes Kartenfoto)', 1))

P.append((
 'colorStops:jr(er)})}))):e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1}));const dr=t._autoImage',
 'colorStops:jr(er)})}))):e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:Fe,selectable:!1}));zLichtZeichnen(Fe,!1);const dr=t._autoImage',
 'gradient-Zweig (Foto-Deckblaetter): Licht dazu', 1))

P.append((
 'zHt=Pt(zOb?zOb.segments:qe,zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'zHt=Pt(zVar?zAkz(zOb?zOb.segments:qe):(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,',
 'gradient-Zweig: Headline durch zAkz nur auf der Lila-Karten-Variante', 1))

P.append((
 'const zHt=Pt($e,Qe,{left:r/2,top:zIn?',
 'const zHt=Pt(zVar?zAkz($e):$e,Qe,{left:r/2,top:zIn?',
 'plate-Zweig: Headline durch zAkz nur auf der Lila-Karten-Variante', 1))

P.append((
 'lisaLicht:"#7323D1",lisaLichtStaerke:.42,lisaLichtRadius:.85,lisaLichtX:-.15,lisaLichtY:.30,',
 'lisaLicht:"#7323D1",lisaLichtStaerke:.42,lisaLichtStaerkeHell:.16,lisaGrundDunkel:"#2A1150",lisaGrundDunkelAnteil:.28,lisaAkzent2:"#C4B5FD",',
 'Regler: lisaLichtStaerkeHell, lisaGrundDunkel, lisaGrundDunkelAnteil, lisaAkzent2 (lisaLichtX/Y/Radius entfallen, Position kommt aus zLichtPos)', 1))

# 291  Fettes Helvetica, keine Lila-Flaechen mehr
#
#      "Lieber fettes Helvetica und bitte keine lila Flaechen, nur
#      schwarz mit lila Licht und weiss mit lila Licht."
#
#      Die Lila-Karten-Variante aus 290 (zGrundWahl/zVar/lisaAkzent2)
#      bleibt als Mechanik stehen, wird aber ueber lisaGrundDunkelAnteil
#      0 abgeschaltet - zGrundWahl liefert dann immer lisaGrund
#      (Schwarz), zVar ist nie wahr, der Lila-Textakzent kommt nicht
#      mehr vor. Licht (289/290) bleibt unveraendert auf Schwarz, Weiss
#      und Fotos.
#
#      Headline-Gewicht in allen drei Zeichen-Zweigen auf 700 (vorher
#      400 in gradient/plate, im frame-Zweig war gar kein Gewicht
#      gesetzt - Pt()s eigene Vorgabe griff dort mit 600).
#
#      GESICHTET: Raster - alle dunklen Karten schwarz mit Licht, alle
#      Ueberschriften fett.

P.append((
 'lisaGrundDunkelAnteil:.28,',
 'lisaGrundDunkelAnteil:0,',
 'Regler lisaGrundDunkelAnteil auf 0 - keine Lila-Flaechen mehr', 1))

P.append((
 'lineHeight:ge.bigWord?.98:t.warmEditorial?1.04:1.12,fontWeight:"400",shadow:se(),maxBottom:zSp?Ke-n*.1:Ke});',
 'lineHeight:ge.bigWord?.98:t.warmEditorial?1.04:1.12,fontWeight:"700",shadow:se(),maxBottom:zSp?Ke-n*.1:Ke});',
 'gradient-Zweig: Headline fett (700)', 1))

P.append((
 'lineHeight:ge.bigWord?.98:kt?1.16:t.warmEditorial?1.04:1.14,fontWeight:"400",shadow:se(),maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});',
 'lineHeight:ge.bigWord?.98:kt?1.16:t.warmEditorial?1.04:1.14,fontWeight:"700",shadow:se(),maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});',
 'plate-Zweig Hauptfall: Headline fett (700)', 1))

P.append((
 'textAlign:t.warmEditorial?"center":"left",lineHeight:1.2,fontWeight:"400",shadow:se(),maxBottom:Me-n*.01}),',
 'textAlign:t.warmEditorial?"center":"left",lineHeight:1.2,fontWeight:"700",shadow:se(),maxBottom:Me-n*.01}),',
 'plate-Zweig Folgefolien-Sonderfall: Headline fett (700)', 1))

P.append((
 'lineHeight:zIn?.98:t.warmEditorial?1.04:1.12,shadow:se(),maxBottom:zIn?tt-n*.02:Ke});zIn&&zSp',
 'lineHeight:zIn?.98:t.warmEditorial?1.04:1.12,fontWeight:"700",shadow:se(),maxBottom:zIn?tt-n*.02:Ke});zIn&&zSp',
 'frame-Zweig: Headline fett (700), vorher gar kein Gewicht gesetzt (Vorgabe war 600)', 1))

# 292  Zentriert sieht bei Listentext nicht gut aus - Design-Agent gefragt
#
#      "Bei einem solchen Text sieht immer zentriert nicht gut aus.
#      Mach mit einem Design Agent einen Vorschlag." Dazu 30 Tage
#      Content geschickt: nummerierte Schritte ("01 - HEADLINE") und
#      kurze, unterschiedlich lange Zeilen mit bewussten Umbruechen
#      (Pacing-Stil).
#
#      EIN SUBAGENT (als Editorial-/Typedesigner gebrieft, mit fuenf
#      Beispiel-Folien aus ihrem Text) hat eine Regel vorgeschlagen:
#      linksbuendig, wenn der Text (an den ORIGINAL-Zeilenumbruechen
#      gezaehlt) in mindestens drei Zeilen zerfaellt UND die kuerzeste
#      weniger als halb so lang ist wie die laengste - sonst bleibt es
#      zentriert. Ein Nummern-Praefix ("01 -", "02 -") erzwingt immer
#      linksbuendig, auch bei nur einer Zeile, damit eine ganze
#      Schrittfolge nicht mitten in der Serie die Anmutung wechselt.
#      Manuell gesetzte Ausrichtung (alignLocked) hat weiterhin Vorrang.
#
#      UMGESETZT in gradient- und plate-Zweig (die beiden, die ihren
#      Text-Content tragen); der frame-Zweig (kleines Foto + grosses
#      Wort) bleibt bewusst zentriert, dafuer gebaut.
#
#      NICHT umgesetzt: der zweite Teil des Vorschlags, die Nummer als
#      eigene kleinere, abgesetzte Kicker-Zeile ueber dem Rest zu
#      ziehen - dafuer muesste die Kopfzeile aus dem Fliesstext
#      herausgeloest und separat platziert werden. Naechster Schritt,
#      falls gewuenscht.
#
#      GESICHTET: vier Beispiel-Folien aus ihrem eigenen Text - drei
#      erkannt und linksbuendig (Schrittfolge, Einzeiler mit Nummer,
#      Kontrast-Dialog), ein kurzer Zweisaetzer blieb zentriert.

P.append((
 'zGrund=zg=>{',
 'zAusrichtung=zx=>{try{const zL=String(zx||"").split(/\\r?\\n/).map(zq=>zq.trim()).filter(Boolean);const zN=zL.length;if(/^\\d{1,2}\\s*[\\u2014\\u2013-]/.test(zL[0]||""))return{left:!0};if(zN<3)return{left:!1};const zLens=zL.map(zq=>zq.replace(/\\*/g,"").length);const zMax=Math.max.apply(null,zLens),zMin=Math.min.apply(null,zLens);if(!(zMax>0))return{left:!1};return{left:zMin/zMax<.5}}catch(zz){return{left:!1}}},zGrund=zg=>{',
 'Helfer zAusrichtung(): erkennt Listen-/Schrittfolgen-Text', 1))

P.append((
 '_t=ge.align==="left",ar=!Qt&&',
 '_t=ge.align==="left"||(!t.alignLocked&&zAusrichtung(t.text).left),ar=!Qt&&',
 'gradient-Zweig: Linksbuendigkeit auch bei erkanntem Listentext', 1))

P.append((
 'ht=t.alignLocked&&t.textAlign?t.textAlign==="left":ge.align==="left"&&!(t.warmEditorial&&(i.slideIndex||0)===0),Ye=ht?r*.1:r/2',
 'ht=t.alignLocked&&t.textAlign?t.textAlign==="left":(ge.align==="left"&&!(t.warmEditorial&&(i.slideIndex||0)===0))||(!t.alignLocked&&zAusrichtung(t.text).left),Ye=ht?r*.1:r/2',
 'plate-Zweig: Linksbuendigkeit auch bei erkanntem Listentext', 1))


# --- karten355: strukturierter Mehrzeilen-Text statt einer verschmelzenden
#     Textbox (Reaktion auf "Es tut mir leid das ist haesslich. Ein
#     generelles Design hinterfragen waere es gewesen.") -----------------
#
#     karten354 hat nur die AUSRICHTUNG von Listen-/Schrittfolgen-Text auf
#     links umgestellt, aber weiterhin per Pt() eine einzige automatisch
#     umbrechende Textbox gezeichnet - die von ihr gesetzten Zeilenumbrueche
#     wurden dabei verschluckt und alles floss zu einem Absatz zusammen.
#     Das war der eigentliche Fehler, nicht nur die Ausrichtung.
#
#     Neu: zRolle() klassifiziert den Text (Schrittfolge mit fuehrender
#     Nummer / Liste mit stark wechselnder Zeilenlaenge / normal) und
#     zStapel() zeichnet Schrittfolgen und Listen als eigene, gestapelte
#     Bloecke statt einer verschmelzenden Textbox:
#      - Schrittfolge: Nummer als grosses eigenes Element, Label darunter,
#        jede weitere Zeile eigener Block; "Nicht ..."-Zeilen gedimmt,
#        "Sondern ..."-Zeilen betont.
#      - Liste (z.B. Fragenkaskade): jede Zeile eigener Block mit kleinem
#        Gedankenstrich davor, gleichmaessiges Gewicht.
#      - Automatische Schriftgroessen-Schrumpfung, falls der Text auch
#        gestapelt nicht in die Karte passt.
#     Die Schriftwahl repliziert exakt Pt()s eigene Logik (zFont()), damit
#     der Text nicht versehentlich auf die serifige Deckblatt-Schrift
#     zurueckfaellt statt der serifenlosen Textkachel-Schrift.
#
#     UMGESETZT in gradient- und plate-Zweig, jeweils auch fuers Deckblatt
#     (Slide 0) - der Inhalt entscheidet, nicht die Folienposition. Der
#     frame-Zweig (kleines Foto + grosses Wort) bleibt unveraendert.
#
#     GESICHTET: die Schrittfolge aus karten354s eigenem Test (grosse
#     Nummer, gedimmte "Nicht"-Zeilen, passt ohne Ueberlauf in die Karte)
#     sowie eine vierzeilige Fragenkaskade ohne Nummer (Gedankenstrich-
#     Liste). Kurze normale Saetze laufen unveraendert ueber Pt().

P.append((
 'return{left:zMin/zMax<.5}}catch(zz){return{left:!1}}},zGrund=zg=>{',
 'return{left:zMin/zMax<.5}}catch(zz){return{left:!1}}},zRolle=zx=>{try{const zL=String(zx||"").split(/\\r?\\n/).map(zq=>zq.trim()).filter(Boolean);const zN=zL.length;if(zN>=2&&/^\\d{1,2}\\s*[\\u2014\\u2013.)-]/.test(zL[0]||""))return"schritt";if(zN<3)return"normal";const zLens=zL.map(zq=>zq.replace(/\\*/g,"").length);const zMax=Math.max.apply(null,zLens),zMin=Math.min.apply(null,zLens);if(!(zMax>0))return"normal";return zMin/zMax<.5?"liste":"normal"}catch(zz){return"normal"}},zGrund=zg=>{',
 'Helfer zAusrichtung() um zRolle() ergaenzt: erkennt Nummerierte-Schritt- und Listen-Text zusaetzlich zur reinen Links/Zentriert-Frage', 1))

P.append((
 'e.add(zt)}catch(zz){}},lr={brand_photo_gradient:',
 'e.add(zt)}catch(zz){}},zFont=(zHatFoto)=>{try{if(t.warmEditorial){let zY=Ct();if(t.isTextTile===!0&&!zHatFoto){const zP=t.plateFont||(i.typography&&i.typography.plateFontFamily)||"HelveticaNeueBrand";if(t.headlineFontChosen===!0||Bt(zP))zY=zP}return zY}const zQe=t.serifHeadline===!1||(t.boldMode===!0&&(typeof t.boldStyle=="number"?t.boldStyle:-1)===0);return zQe?"Montserrat":(BS_KACHEL.lisaSchrift||m)}catch(zz){return BS_KACHEL.lisaSchrift||"HelveticaNeueBrand"}},zStapel=(zRl,zText,zOpt)=>{try{const zL=String(zText||"").split(/\\r?\\n/).map(zq=>zq.trim()).filter(Boolean);if(!zL.length)return null;const zFam=zOpt.fontFamily||Ct(),zLeft=zOpt.left,zW=zOpt.width,zFill=zOpt.fill,zAcc=zOpt.accentFill||zFill,zBase=zOpt.fontSize,zTop=zOpt.top,zMax=zOpt.maxBottom||n*.92,zClean=zq=>zq.replace(/\\*/g,"");const zNumM=zRl==="schritt"?/^(\\d{1,2})\\s*[\\u2014\\u2013.)-]?\\s*(.*)$/.exec(zL[0]):null;const zSpecs=[];let zRest=zL;if(zNumM){zSpecs.push({txt:zNumM[1],sz:2.5,wt:"700",fill:zAcc,gap:0});const zLabel=zClean(zNumM[2]||"").trim();zLabel&&zSpecs.push({txt:zLabel,sz:.92,wt:"700",fill:zFill,gap:.16});zRest=zL.slice(1)}zRest.forEach((zln,zi)=>{let zf=zFill,zwt="600";/^(nicht|kein|keine)\\b/i.test(zln)?(zf=G(zFill,.5),zwt="500"):/^(sondern|stattdessen)\\b/i.test(zln)&&(zf=zAcc,zwt="700");const zsz=zRl==="schritt"?.54:.64,ztxt=zRl==="liste"?"\\u2014  "+zln:zln;zSpecs.push({txt:ztxt,sz:zsz,wt:zwt,fill:zf,gap:zi===0?(zNumM?.22:.18):.15})});const zBauen=zScale=>{let zY=zTop;const zBx=[];for(const zs of zSpecs){zY+=zs.gap*zBase*zScale;const zt=new Pe.fabric.Textbox(zClean(zs.txt),{left:zLeft,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zs.sz*zBase*zScale),fontFamily:zFam,fontWeight:Xt(zFam,zs.wt),fill:zs.fill,lineHeight:1.1,shadow:zOpt.shadow,selectable:!1});zY+=zt.height||0,zBx.push(zt)}return{bx:zBx,bottom:zY}};let zScale=1,zErg=zBauen(zScale);for(let zi=0;zi<45&&zErg.bottom>zMax&&zScale>.2;zi+=1)zScale-=.02,zErg=zBauen(zScale);zErg.bx.forEach(zt=>e.add(zt));return{top:zTop,height:zErg.bottom-zTop,originY:"top",originX:"left",bottom:zErg.bottom}}catch(zz){return null}},lr={brand_photo_gradient:',
 'Helfer zFont() (repliziert Pt()s Schriftwahl) und zStapel() (zeichnet mehrzeiligen Text als eigene, nicht verschmolzene Bloecke statt einer auto-umbrechenden Textbox) ergaenzt', 1))

P.append((
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!Ye&&!ge.bigWord&&!t.secondaryText&&!kt?zTeilen($e?$e.rest:t.text,!1):null,zOb=zSp?ye(zSp.oben):null,zHt=Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,top:ae,originX:sr,originY:De,width:r*(Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),maxWidth:Qt?void 0:Ze?r*dt:void 0,fontSize:Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k()*zGr():t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),minFontSize:Ze?T()*zGr():void 0,goldOk:ur,fill:me,accentFill:Oe,textAlign:Ht,lineHeight:ge.bigWord?.98:t.warmEditorial?1.04:1.12,fontWeight:"700",shadow:se(),maxBottom:zSp?Ke-n*.1:Ke});if(zSp&&zUnter(zHt,zSp.unten,me,Ht==="left",br),ge.kicker==="bottom"',
 'const zRlG=kt?"normal":zRolle(t.text),zSp=zRlG==="normal"&&BS_KACHEL.lisaTeilen!==0&&!Ye&&!ge.bigWord&&!t.secondaryText&&!kt?zTeilen($e?$e.rest:t.text,!1):null,zOb=zRlG==="normal"&&zSp?ye(zSp.oben):null,zHt=zRlG==="schritt"||zRlG==="liste"?zStapel(zRlG,t.text,{left:br,top:ae,width:r*(Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),fill:me,accentFill:Oe,fontSize:Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k()*zGr():t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),shadow:se(),maxBottom:Ke,fontFamily:zFont($)}):Pt(zOb?zOb.segments:ht,zOb?zOb.plain:qe,{left:br,top:ae,originX:sr,originY:De,width:r*(Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),maxWidth:Qt?void 0:Ze?r*dt:void 0,fontSize:Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k()*zGr():t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),minFontSize:Ze?T()*zGr():void 0,goldOk:ur,fill:me,accentFill:Oe,textAlign:Ht,lineHeight:ge.bigWord?.98:t.warmEditorial?1.04:1.12,fontWeight:"700",shadow:se(),maxBottom:zSp?Ke-n*.1:Ke});if(zRlG==="normal"&&zSp&&zUnter(zHt,zSp.unten,me,Ht==="left",br),ge.kicker==="bottom"',
 'gradient-Zweig: bei erkanntem Schritt-/Listentext zStapel() statt Pt() verwenden (grosse Nummer als eigenes Element, jede Original-Zeile eigener Block, Nicht/Sondern-Kontrast gedimmt/betont)', 1))

P.append((
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null;let tt=zInsetUnten>0?zInsetUnten+n*(Number(BS_KACHEL.textFotoLuft)||.05):ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?((i.slideIndex||0)===0?n*(Number(BS_KACHEL.lisaDeckMitte)||.5)-(zSp?n*(Number(BS_KACHEL.lisaDeckHub)||.045):0):n*(Number(BS_KACHEL.lisaTextMitte)||.58)):ge.textPos==="top"?n*.24:n*.5;const Qt=zInsetUnten>0?"top":ge.textPos==="top"&&BS_KACHEL.lisaUnten!==1?"top":"center";ge.kicker==="top"&&t.secondaryText?Te(t.secondaryText,Ye,tt-n*.14,G(me,.7),et,"center"):t.secondaryText&&ge.textPos!=="top"&&Te(t.secondaryText,Ye,n*.3,G(me,.7),et,"center");const jt=ge.bigWord?t.fontSize||110:t.warmEditorial&&ge.exactFont?ge.exactFont:t.fontSize||ge.exactFont||(t.warmEditorial?46:58),_t=I(w(Fe)),ar=116,kt=t.warmEditorial&&!ge.bigWord&&(i.slideIndex||0)===0;const zOb=zSp?ye(zSp.oben):null,zHt=Pt(zVar?zAkz(zOb?zOb.segments:qe):(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,top:tt,originX:zInsetUnten>0?"center":et,originY:Qt,width:r*(zInsetUnten>0?.84:kt?.78:ge.exactWidth||(ht?.8:.74)),maxWidth:kt?r*.82:void 0,fontSize:t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):kt?r*(ar/1080):t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(jt)*zGr(),goldOk:_t,minFontSize:kt?r*(56/1080):void 0,fill:me,accentFill:Oe,textAlign:zInsetUnten>0?"center":lt,lineHeight:ge.bigWord?.98:kt?1.16:t.warmEditorial?1.04:1.14,fontWeight:"700",shadow:se(),maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});try{if(zInsetUnten>0&&zHt&&zHt.originY==="center"){const zGr2=zInsetUnten+n*.035;let zi2=0;for(;zHt.top-(zHt.height||0)/2<zGr2&&zHt.fontSize>12&&zi2<80;zi2+=1)zHt.set("fontSize",zHt.fontSize-1),zHt.initDimensions&&zHt.initDimensions();if(zHt.top-(zHt.height||0)/2<zGr2){zHt.set("top",zGr2+(zHt.height||0)/2);zHt.setCoords&&zHt.setCoords()}}}catch(zz){}if(zSp&&zUnter(zHt,zSp.unten,me,zInsetUnten>0?!1:lt==="left",Ye),ge.kicker==="bottom"',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null;let tt=zInsetUnten>0?zInsetUnten+n*(Number(BS_KACHEL.textFotoLuft)||.05):ge.exactY!=null?n*ge.exactY:BS_KACHEL.lisaUnten===1?((i.slideIndex||0)===0?n*(Number(BS_KACHEL.lisaDeckMitte)||.5)-(zSp?n*(Number(BS_KACHEL.lisaDeckHub)||.045):0):n*(Number(BS_KACHEL.lisaTextMitte)||.58)):ge.textPos==="top"?n*.24:n*.5;const Qt=zInsetUnten>0?"top":ge.textPos==="top"&&BS_KACHEL.lisaUnten!==1?"top":"center";ge.kicker==="top"&&t.secondaryText?Te(t.secondaryText,Ye,tt-n*.14,G(me,.7),et,"center"):t.secondaryText&&ge.textPos!=="top"&&Te(t.secondaryText,Ye,n*.3,G(me,.7),et,"center");const jt=ge.bigWord?t.fontSize||110:t.warmEditorial&&ge.exactFont?ge.exactFont:t.fontSize||ge.exactFont||(t.warmEditorial?46:58),_t=I(w(Fe)),ar=116,kt=t.warmEditorial&&!ge.bigWord&&(i.slideIndex||0)===0;const zRl=zInsetUnten<=0?zRolle(t.text):"normal";const zOb=zRl==="normal"&&zSp?ye(zSp.oben):null;const zHt=zRl==="schritt"||zRl==="liste"?zStapel(zRl,t.text,{left:Ye,top:tt,width:r*(kt?.78:ge.exactWidth||.8),fill:me,accentFill:Oe,fontSize:t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):kt?r*(ar/1080):t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(jt)*zGr(),shadow:se(),maxBottom:Ke,fontFamily:zFont($)}):Pt(zVar?zAkz(zOb?zOb.segments:qe):(zOb?zOb.segments:qe),zOb?zOb.plain:$e,{left:zInsetUnten>0?r/2:Ye,top:tt,originX:zInsetUnten>0?"center":et,originY:Qt,width:r*(zInsetUnten>0?.84:kt?.78:ge.exactWidth||(ht?.8:.74)),maxWidth:kt?r*.82:void 0,fontSize:t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):kt?r*(ar/1080):t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(jt)*zGr(),goldOk:_t,minFontSize:kt?r*(56/1080):void 0,fill:me,accentFill:Oe,textAlign:zInsetUnten>0?"center":lt,lineHeight:ge.bigWord?.98:kt?1.16:t.warmEditorial?1.04:1.14,fontWeight:"700",shadow:se(),maxBottom:zSp?(kt?n*.72:Ke)-n*.1:kt?n*.72:Ke});try{if(zInsetUnten>0&&zHt&&zHt.originY==="center"){const zGr2=zInsetUnten+n*.035;let zi2=0;for(;zHt.top-(zHt.height||0)/2<zGr2&&zHt.fontSize>12&&zi2<80;zi2+=1)zHt.set("fontSize",zHt.fontSize-1),zHt.initDimensions&&zHt.initDimensions();if(zHt.top-(zHt.height||0)/2<zGr2){zHt.set("top",zGr2+(zHt.height||0)/2);zHt.setCoords&&zHt.setCoords()}}}catch(zz){}if(zRl==="normal"&&zSp&&zUnter(zHt,zSp.unten,me,zInsetUnten>0?!1:lt==="left",Ye),ge.kicker==="bottom"',
 'plate-Zweig: dieselbe zStapel()-Weiche wie im gradient-Zweig, inklusive Deckblatt (Inhalt statt Folienposition entscheidet)', 1))


# --- karten356: Foto-Highlight-Layout (lila Header, weisser Text, Marker
#     hinter *Wort*) als eigenes, waehlbares Layout ------------------------
#
#     Reaktion auf einen Referenz-Screenshot (Instagram-Account, dunkler
#     Foto-Hintergrund, fetter weisser Text, lila Zwischenueberschriften,
#     lila Marker-Hervorhebung hinter Kernsaetzen). Erst als Mockup-Artifact
#     gezeigt (Poppins, dann auf ihren Wunsch Playfair Display, damit es nicht
#     wie eine Kopie des fremden Accounts aussieht), dann als neues Layout
#     eingebettet: "Mir hat das Lisa Design ja sehr gefallen mit den Layouts"
#     - also nicht als globaler Stil-Wechsel, sondern als weitere, manuell
#     waehlbare Karte im bestehenden Layout-System.
#
#     Neuer Helfer zAbschnitte(): trennt den Text an Leerzeilen in Bloecke;
#     ein Block mit 2+ Zeilen wird zu Kopfzeile (Playfair kursiv, lila) plus
#     Absatz (Playfair, weiss, fliesst natuerlich um); ein Block mit nur
#     einer Zeile bleibt reiner Absatz ohne Kopfzeile. Die Hervorhebung nutzt
#     ihr eigenes, bereits vorhandenes *Wort*-Feature (Editor-Tipp "Nutze
#     *Wort* fuer Farben") - keine neue Eingabe noetig, nur die Darstellung
#     ist neu: statt Kursiv/Akzentfarbe zeichnet sie jetzt einen lila
#     Marker-Hintergrund hinter der markierten Phrase (Fabric Textbox
#     per-Zeichen textBackgroundColor). Automatische Schrumpfung wie bei
#     zStapel, falls der Text nicht passt.
#
#     Neues Layout brand_photo_highlight in der lr-Tabelle (gradient-Zweig,
#     linksbuendig) UND im manuellen Layout-Waehler der Bearbeitungsseite
#     ("Foto Highlight") - taucht dort neben den anderen Foto-Layouts auf,
#     genau wie sie es von den Lisa-Layouts kennt. Nicht in die automatische
#     layoutReihe-Rotation aufgenommen: die Textstruktur (Kopfzeile + Absatz)
#     passt nicht zu ihren Schrittfolgen/Listen, deshalb bewusst nur manuell
#     waehlbar statt automatisch gemischt.
#
#     GESICHTET: zwei Abschnitte (Kopfzeile + Absatz) mit je einer markierten
#     Kernphrase, echte App-Daten ueber den Layout-Waehler ausgewaehlt -
#     beide Marker sichtbar, Playfair kursiv/weiss/lila korrekt, passt ohne
#     Ueberlauf in die Karte.

P.append((
 'return{top:zTop,height:zErg.bottom-zTop,originY:"top",originX:"left",bottom:zErg.bottom}}catch(zz){return null}},lr={brand_photo_gradient:',
 'return{top:zTop,height:zErg.bottom-zTop,originY:"top",originX:"left",bottom:zErg.bottom}}catch(zz){return null}},zAbschnitte=(zText,zOpt)=>{try{const zBloecke=String(zText||"").split(/\\n\\s*\\n+/).map(zb=>zb.split(/\\r?\\n/).map(zq=>zq.trim()).filter(Boolean)).filter(zb=>zb.length);if(!zBloecke.length)return null;const zFam=BS_KACHEL.lisaHighlightSchrift||"Playfair Display",zHeadFarbe=BS_KACHEL.lisaHighlightHeader||"#B9A3E8",zMarker=BS_KACHEL.lisaHighlightMarker||"#3F2F66",zLeft=zOpt.left,zW=zOpt.width,zTop=zOpt.top,zMax=zOpt.maxBottom||n*.92,zHeadSz=r*(Number(BS_KACHEL.lisaHighlightHeaderGroesse)||.048),zKoerperSz=r*(Number(BS_KACHEL.lisaHighlightGroesse)||.039);const zAkzentSeg=zx=>String(zx||"").split(/(\\*[^*]+\\*)/g).filter(Boolean).map(zp=>{const zAcc=zp.length>2&&zp.startsWith("*")&&zp.endsWith("*");return{text:zAcc?zp.slice(1,-1):zp,accent:zAcc}});const zSpecs=zBloecke.map(zL=>zL.length>=2?{header:zL[0],body:zL.slice(1).join(" ")}:{header:null,body:zL[0]});const zBauen=zScale=>{let zY=zTop;const zBx=[];for(const zs of zSpecs){if(zs.header){const zh=new Pe.fabric.Text(zs.header.replace(/\\*/g,""),{left:zLeft,top:zY,originX:"left",originY:"top",fontSize:Math.max(10,zHeadSz*zScale),fontFamily:zFam,fontWeight:"700",fontStyle:"italic",fill:zHeadFarbe,shadow:zOpt.shadow,selectable:!1});zY+=(zh.height||0)+zKoerperSz*zScale*.22;zBx.push(zh)}const zSeg=zAkzentSeg(zs.body),zPlain=zSeg.map(zq=>zq.text).join("");const zKt=new Pe.fabric.Textbox(zPlain,{left:zLeft,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zKoerperSz*zScale),fontFamily:zFam,fontWeight:"600",fill:"#FFFFFF",textAlign:"left",lineHeight:1.32,shadow:zOpt.shadow,selectable:!1});let zPos=0;zSeg.forEach(zq=>{if(zq.accent)zKt.setSelectionStyles({fill:"#FFFFFF",textBackgroundColor:zMarker},zPos,zPos+zq.text.length);zPos+=zq.text.length});zY+=(zKt.height||0)+zKoerperSz*zScale*.55;zBx.push(zKt)}return{bx:zBx,bottom:zY}};let zScale=1,zErg=zBauen(zScale);for(let zi=0;zi<45&&zErg.bottom>zMax&&zScale>.35;zi+=1)zScale-=.02,zErg=zBauen(zScale);zErg.bx.forEach(zt=>e.add(zt));return{top:zTop,bottom:zErg.bottom}}catch(zz){return null}},lr={brand_photo_gradient:',
 'insert zAbschnitte', 1))

P.append((
 'we_plate_cream_left:{base:"plate",textPos:"center",align:"left",exactY:.5,exactFont:58,exactWidth:.72,plateColor:"#E8E8E8"}};',
 'we_plate_cream_left:{base:"plate",textPos:"center",align:"left",exactY:.5,exactFont:58,exactWidth:.72,plateColor:"#E8E8E8"},brand_photo_highlight:{base:"gradient",textPos:"top",align:"left",highlight:!0}};',
 'add lr.brand_photo_highlight', 1))

P.append((
 'const zRlG=kt?"normal":zRolle(t.text),',
 'if(ge.highlight===!0){zAbschnitte(t.text,{left:r*.09,top:n*(Number(BS_KACHEL.lisaHighlightOben)||.14),width:r*(ge.exactWidth||.82),maxBottom:Ke,shadow:se()});if(ge.kicker==="bottom"&&(t.footerText||t.secondaryText)&&Te(t.footerText||t.secondaryText,r*.09,n*.8,"rgba(255,255,255,0.7)","left","center"),i.globalBrandName,t.overlayImage)try{await Ae(t.overlayImage)}catch{}$e&&be($e.label),Le(),e.renderAll();return}const zRlG=kt?"normal":zRolle(t.text),',
 'wire highlight branch into gradient', 1))

P.append((
 '{id:"brand_photo_bottom_left",name:"Foto unten links",icon:CA,description:"Text unten links"},',
 '{id:"brand_photo_bottom_left",name:"Foto unten links",icon:CA,description:"Text unten links"},{id:"brand_photo_highlight",name:"Foto Highlight",icon:Xh,description:"Weißer Text, lila Highlight"},',
 'add layout picker UI entry', 1))


# --- karten357: gezielt auf Playfair Display warten, bevor das Foto-
#     Highlight-Layout zeichnet ----------------------------------------
#
#     Rueckmeldung nach dem Live-Test von 356: "356 aber kein Playfair"
#     - das Layout kam an, aber die Schrift fiel auf die Fallback-Schrift
#     zurueck. Im eigenen Testlauf war das nicht nachzustellen (Playfair
#     Display war durch den Testablauf laengst geladen), darum ist das
#     hier eine gezielte Absicherung, kein bestaetigter Fund.
#
#     Verdacht: der App-weite Font-Preload laedt rund 15 Schriftfamilien
#     mit je 6 Schnitten parallel und bricht nach 4 Sekunden ab (Promise.
#     race gegen einen Timeout), egal ob alles fertig ist. Bei einer
#     langsameren Verbindung kann Playfair Display dieses Rennen verlieren
#     - das Highlight-Layout zeichnet dann mit der Fallback-Schrift und
#     bleibt dabei, weil eine Canvas-Zeichnung sich nicht von selbst neu
#     zeichnet, wenn eine Schrift erst spaeter eintrudelt.
#
#     Deshalb wartet der Highlight-Zweig jetzt zusaetzlich und gezielt auf
#     genau die Playfair-Schnitte, die zAbschnitte() braucht (400/600/700,
#     kursiv 400/700), mit eigenem, grosszuegigerem Timeout (8 Sekunden) -
#     unabhaengig vom Ausgang des allgemeinen Preload-Rennens.

P.append((
 'if(ge.highlight===!0){zAbschnitte(t.text,{left:r*.09,top:n*(Number(BS_KACHEL.lisaHighlightOben)||.14),width:r*(ge.exactWidth||.82),maxBottom:Ke,shadow:se()});',
 'if(ge.highlight===!0){try{typeof document<"u"&&document.fonts&&document.fonts.load&&await Promise.race([Promise.all(["italic 400","italic 700","400","600","700"].map(zw=>document.fonts.load(`${zw} 44px "Playfair Display"`).catch(()=>{}))),new Promise(zr=>setTimeout(zr,8e3))])}catch(zz){}zAbschnitte(t.text,{left:r*.09,top:n*(Number(BS_KACHEL.lisaHighlightOben)||.14),width:r*(ge.exactWidth||.82),maxBottom:Ke,shadow:se()});',
 'Highlight-Layout: gezielt auf Playfair Display warten, statt sich auf das allgemeine 4s-Rennen zu verlassen', 1))

P.append((
 'title:"Geladene Datei",children:"karten356"',
 'title:"Geladene Datei",children:"karten357"',
 'Versionsschild auf karten357', 1))


# --- karten358: Lila Licht weg, Folgefolien direkt auf Foto (Aufbau +
#     fette Pointe) statt Karte, Cover-Feedback bestaetigt ------------------
#
#     Sie schickte vier Screenshots ihres eigenen Content-Plans plus einen
#     Referenz-Account (marina.persano) und schrieb: "Ich lieb Tag 15 Style
#     Cover und Tag 1 bei Fotos das Lila licht weg, und der Style der Folge
#     slides eher so wie Bild 3&4 vom Schriftbild und Größe und so."
#
#     Drei Teile:
#      1. Tag 15 als Cover-Stil (schwarz, kein Foto, fetter weisser Text) -
#         keine Aenderung noetig, das ist bereits der bestehende plate-Zweig
#         ohne Foto; nur als Bestaetigung/Praeferenz vermerkt.
#      2. `lisaLicht` global auf leer gesetzt: das lila Umgebungslicht
#         (zLichtZeichnen, seit 290/291) zeichnet nirgends mehr.
#      3. Neuer Helfer zSetupPayoff(): fuer Folgefolien (slideIndex>0) mit
#         Foto, deren Text sich an einer Satzgrenze in Aufbau+Pointe teilen
#         laesst (zTeilen, dieselbe Erkennung wie beim Kicker-Feature), wird
#         jetzt direkt auf dem Foto gezeichnet statt in einer Karte: der
#         Aufbausatz normal/kleiner, die Pointe fett/groesser, beides
#         zentriert mit Schlagschatten - wie im Referenz-Screenshot (Bild
#         3&4). Nur wenn sich der Text wirklich teilen laesst und noch nicht
#         als Schrittfolge/Liste erkannt wurde (zRolle); sonst unveraendert.

P.append((
 'lisaLicht:"#7323D1"',
 'lisaLicht:""',
 'lisaLicht global abgeschaltet', 1))

P.append((
 'return{top:zTop,bottom:zErg.bottom}}catch(zz){return null}},lr={brand_photo_gradient:',
 'return{top:zTop,bottom:zErg.bottom}}catch(zz){return null}},zSetupPayoff=(zOben,zUnten,zOpt)=>{try{const zW=zOpt.width,zTop=zOpt.top,zMax=zOpt.maxBottom||n*.92,zFam=BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",zSetupSz=r*(Number(BS_KACHEL.lisaPayoffSetupGroesse)||.032),zPayoffSz=r*(Number(BS_KACHEL.lisaPayoffGroesse)||.058);const zBauen=zScale=>{let zY=zTop;const zSe=new Pe.fabric.Textbox(String(zOben||"").replace(/\\*/g,""),{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fill:"#FFFFFF",textAlign:"center",lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});zY+=(zSe.height||0)+zPayoffSz*zScale*.3;const zPa=new Pe.fabric.Textbox(String(zUnten||"").replace(/\\*/g,""),{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zPayoffSz*zScale),fontFamily:zFam,fontWeight:"700",fill:"#FFFFFF",textAlign:"center",lineHeight:1.14,shadow:zOpt.shadow,selectable:!1});zY+=(zPa.height||0);return{bx:[zSe,zPa],bottom:zY}};let zScale=1,zErg=zBauen(zScale);for(let zi=0;zi<40&&zErg.bottom>zMax&&zScale>.3;zi+=1)zScale-=.02,zErg=zBauen(zScale);zErg.bx.forEach(zt=>e.add(zt));return{top:zTop,bottom:zErg.bottom}}catch(zz){return null}},lr={brand_photo_gradient:',
 'insert zSetupPayoff', 1))

P.append((
 'const zRlG=kt?"normal":zRolle(t.text),',
 'if((i.slideIndex||0)>0&&!kt&&!Ye&&!ge.bigWord&&!t.secondaryText&&BS_KACHEL.lisaTeilen!==0&&zRolle(t.text)==="normal"){const zSp2=zTeilen($e?$e.rest:t.text,!1);if(zSp2){zSetupPayoff(zSp2.oben,zSp2.unten,{width:r*(ge.exactWidth||.82),top:ae,maxBottom:Ke,shadow:se()});if(ge.kicker==="bottom"&&(t.footerText||t.secondaryText)&&Te(t.footerText||t.secondaryText,br,n*.8,G(me,.7),sr,"center"),i.globalBrandName,t.overlayImage)try{await Ae(t.overlayImage)}catch{}$e&&be($e.label),Le(),e.renderAll();return}}const zRlG=kt?"normal":zRolle(t.text),',
 'wire setup+payoff into gradient follow-up slides', 1))

P.append((
 'title:"Geladene Datei",children:"karten357"',
 'title:"Geladene Datei",children:"karten358"',
 'Versionsschild auf karten358', 1))


# --- karten359: Folgefolien immer Foto + dunkles Overlay + Aufbau/Pointe,
#     keine Layout-Rotation mehr ---------------------------------------------
#
#     Nach 358: "Also da sind immer noch die Layouts, es sollte aber so sein:
#     bei denen die ich gut fand bleibt das Licht bei den Fotos weg. Bei den
#     Folgeslides auch der Text slides gehoert ein Foto, dunkles Overlay und
#     Text wie auf den Bildern vorher 3&4 von Marina Persano, bei dem
#     Fotoslides generell auch so."
#
#     Die Folgefolien liefen weiter durch die Rotation aus layoutReihe/
#     folgeReihe (zLayF): Text-Plates, Rahmen, Bigword usw. Jetzt:
#      1. zLayF gibt fuer jede Folgefolie (ausser Screenshot-Hook und CTA)
#         dasselbe Layout brand_photo_folge zurueck (gradient, zentriert).
#      2. Folgefolien ohne eigenes Foto bekommen in Ca() eins injiziert:
#         bevorzugt das Foto des Tages (__bsTagFoto - dasselbe Bild ueber
#         das ganze Karussell, wie in der Referenz), sonst ein pro Tag
#         festes Bild aus dem Pool (__bsBilder). Das Cover (Folie 0) bleibt
#         ohne Foto - Tag-15-Stil.
#      3. Im gradient-Zweig legt das Folge-Layout ein gleichmaessiges dunkles
#         Overlay (folgeOverlay .38) ueber das Foto und zeichnet den Text
#         immer als Aufbau (klein, 500) + Pointe (fett, gross), oder nur als
#         Pointe, wenn sich der Satz nicht teilen laesst. Der Block wird um
#         folgeMitte (.6 der Hoehe) zentriert statt ab einer Oberkante.
#         Schrittfolgen/Listen laufen weiter ueber zStapel (mit Overlay).
#     Regler: folgeFoto (1=an), folgeOverlay, folgeMitte, folgeLayout.
#
#     GESICHTET: Tag mit Cover (schwarz, kein Foto), reiner Textfolie (bekam
#     Tagesfoto + Overlay + Aufbau/Pointe), Fotofolie mit Zweisatz und
#     Einzelsatz-Folie (nur Pointe). Alle ohne Karte, ohne Lila-Licht.

P.append((
 'lisaGroesse:1.3,folgeLayouts:1,layoutSchritt:3,',
 'lisaGroesse:1.3,folgeLayouts:1,folgeFoto:1,folgeOverlay:.38,folgeMitte:.6,layoutSchritt:3,',
 'Regler folgeFoto/folgeOverlay/folgeMitte', 1))

P.append((
 't={...t,background:zB[zh%zB.length]}}}catch(zz){}})();const zSat=(()=>{',
 't={...t,background:zB[zh%zB.length]}}}catch(zz){}})();(()=>{try{if(t.background||t.karte==="ablauf"||t.overlayIsScreenshot===!0||BS_KACHEL.folgeFoto!==1||(i.slideIndex||0)===0)return;const zReg=(typeof window<"u"&&window.__bsTagFoto)||{},zB=(typeof window<"u"&&window.__bsBilder)||[];let zF=typeof t._tag=="number"?(zReg[String(t._tag)]||""):"";if(!zF&&zB.length){const zs="tag|"+String(typeof t._tag=="number"?t._tag:0);let zh=0;for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;zF=zB[zh%zB.length]}if(zF)t={...t,background:zF,_folgeFoto:!0}}catch(zz){}})();const zSat=(()=>{',
 'Foto-Injektion fuer Folgefolien', 1))

P.append((
 'if(zCta===!0&&zF&&typeof ea=="string"&&ea.length>5)return "brand_photo_gradient";',
 'if(zCta===!0&&zF&&typeof ea=="string"&&ea.length>5)return "brand_photo_gradient";if(zV>0&&zF&&BS_KACHEL.folgeFoto===1&&!(rt&&(rt.overlayIsScreenshot===!0||rt._wasScreenshot===!0)))return BS_KACHEL.folgeLayout||"brand_photo_folge";',
 'zLayF: ein Layout fuer alle Folgefolien', 1))

P.append((
 'brand_photo_highlight:{base:"gradient",textPos:"top",align:"left",highlight:!0}};',
 'brand_photo_highlight:{base:"gradient",textPos:"top",align:"left",highlight:!0},brand_photo_folge:{base:"gradient",textPos:"center",align:"center",scrim:.5,folge:!0}};',
 'lr.brand_photo_folge', 1))

P.append((
 'zSetupPayoff=(zOben,zUnten,zOpt)=>{try{const zW=zOpt.width,zTop=zOpt.top,zMax=zOpt.maxBottom||n*.92,zFam=BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",zSetupSz=r*(Number(BS_KACHEL.lisaPayoffSetupGroesse)||.032),zPayoffSz=r*(Number(BS_KACHEL.lisaPayoffGroesse)||.058);const zBauen=zScale=>{let zY=zTop;const zSe=new Pe.fabric.Textbox(String(zOben||"").replace(/\\*/g,""),{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fill:"#FFFFFF",textAlign:"center",lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});zY+=(zSe.height||0)+zPayoffSz*zScale*.3;const zPa=new Pe.fabric.Textbox(String(zUnten||"").replace(/\\*/g,""),{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zPayoffSz*zScale),fontFamily:zFam,fontWeight:"700",fill:"#FFFFFF",textAlign:"center",lineHeight:1.14,shadow:zOpt.shadow,selectable:!1});zY+=(zPa.height||0);return{bx:[zSe,zPa],bottom:zY}};let zScale=1,zErg=zBauen(zScale);for(let zi=0;zi<40&&zErg.bottom>zMax&&zScale>.3;zi+=1)zScale-=.02,zErg=zBauen(zScale);zErg.bx.forEach(zt=>e.add(zt));return{top:zTop,bottom:zErg.bottom}}catch(zz){return null}},',
 'zSetupPayoff=(zOben,zUnten,zOpt)=>{try{const zW=zOpt.width,zMax=zOpt.maxBottom||n*.92,zMin=typeof zOpt.minTop=="number"?zOpt.minTop:n*.1,zFam=BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",zSetupSz=r*(Number(BS_KACHEL.lisaPayoffSetupGroesse)||.032),zPayoffSz=r*(Number(BS_KACHEL.lisaPayoffGroesse)||.058),zO=String(zOben||"").replace(/\\*/g,"").trim(),zU=String(zUnten||"").replace(/\\*/g,"").trim();if(!zU)return null;const zBauen=zScale=>{let zY=0;const zBx=[];if(zO){const zSe=new Pe.fabric.Textbox(zO,{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fill:"#FFFFFF",textAlign:"center",lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});zY+=(zSe.height||0)+zPayoffSz*zScale*.3;zBx.push(zSe)}const zPa=new Pe.fabric.Textbox(zU,{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zPayoffSz*zScale),fontFamily:zFam,fontWeight:"700",fill:"#FFFFFF",textAlign:"center",lineHeight:1.14,shadow:zOpt.shadow,selectable:!1});zY+=(zPa.height||0);zBx.push(zPa);return{bx:zBx,h:zY}};const zRaum=zMax-zMin;let zScale=1,zErg=zBauen(zScale);for(let zi=0;zi<40&&zErg.h>zRaum&&zScale>.3;zi+=1)zScale-=.02,zErg=zBauen(zScale);let zTop=typeof zOpt.mitte=="number"?zOpt.mitte-zErg.h/2:zOpt.top;zTop=Math.max(zMin,Math.min(zTop,zMax-zErg.h));zErg.bx.forEach(zt=>{zt.set("top",zt.top+zTop);zt.setCoords&&zt.setCoords();e.add(zt)});return{top:zTop,bottom:zTop+zErg.h}}catch(zz){return null}},',
 'zSetupPayoff: leerer Aufbau, zentriert um Mitte', 1))

P.append((
 'if((i.slideIndex||0)>0&&!kt&&!Ye&&!ge.bigWord&&!t.secondaryText&&BS_KACHEL.lisaTeilen!==0&&zRolle(t.text)==="normal"){const zSp2=zTeilen($e?$e.rest:t.text,!1);if(zSp2){zSetupPayoff(zSp2.oben,zSp2.unten,{width:r*(ge.exactWidth||.82),top:ae,maxBottom:Ke,shadow:se()});if(ge.kicker==="bottom"&&(t.footerText||t.secondaryText)&&Te(t.footerText||t.secondaryText,br,n*.8,G(me,.7),sr,"center"),i.globalBrandName,t.overlayImage)try{await Ae(t.overlayImage)}catch{}$e&&be($e.label),Le(),e.renderAll();return}}',
 'ge.folge===!0&&(Number(BS_KACHEL.folgeOverlay)||0)>0&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"rgba(0,0,0,"+(Number(BS_KACHEL.folgeOverlay)||.38)+")",selectable:!1,evented:!1}));if((i.slideIndex||0)>0&&!Ye&&!ge.bigWord&&!t.secondaryText&&zRolle(t.text)==="normal"&&(ge.folge===!0||!kt)){const zSp2=BS_KACHEL.lisaTeilen!==0?zTeilen($e?$e.rest:t.text,!1):null;if(zSp2||ge.folge===!0){zSetupPayoff(zSp2?zSp2.oben:"",zSp2?zSp2.unten:($e?$e.rest:t.text),{width:r*(ge.exactWidth||.82),top:ae,mitte:ge.folge===!0?n*(Number(BS_KACHEL.folgeMitte)||.6):void 0,minTop:n*.1,maxBottom:Ke,shadow:se()});if(ge.kicker==="bottom"&&(t.footerText||t.secondaryText)&&Te(t.footerText||t.secondaryText,br,n*.8,G(me,.7),sr,"center"),i.globalBrandName,t.overlayImage)try{await Ae(t.overlayImage)}catch{}$e&&be($e.label),Le(),e.renderAll();return}}',
 'Gradient-Zweig: Folge-Overlay + Aufbau/Pointe fuer alle Folgefolien', 1))

P.append((
 'title:"Geladene Datei",children:"karten358"',
 'title:"Geladene Datei",children:"karten359"',
 'Versionsschild auf karten359', 1))


# --- karten360: Lila Licht wieder an (nur nicht auf Fotos), Folgefolien-
#     Text deutlich groesser --------------------------------------------------
#
#     Nach 359 (Screenshot einer Schrittfolge auf Foto, winzig unten links):
#     "Lila Licht soll an ausser bei den Fotos ???, die folgeslides sind viel
#     zu klein vom Schrift Bild"
#
#     358 hatte das Licht global abgeschaltet - gemeint war nur: nicht auf
#     Fotos. lisaLicht steht wieder auf #7323D1, zLichtZeichnen bricht
#     zusaetzlich ab, sobald die Folie ein Foto hat ($) - also auch bei
#     injizierten Tagesfotos. Cover ohne Foto leuchten wieder.
#
#     Zu klein: der Stapel (zStapel) startete im gradient-Zweig an der
#     Text-Oberkante ae = 64 % Hoehe und musste bis Ke (85 %) passen - nur
#     21 % Hoehe Raum, die Schrumpfschleife druecke ihn auf ~40 %. Jetzt:
#      - zStapel kann optional um eine Mitte zentrieren (mitte/minTop): er
#        misst ab 0, nutzt den vollen Raum minTop..maxBottom und setzt den
#        Block dann mittig. Ohne mitte verhaelt er sich wie bisher (Cover).
#      - Im Folge-Layout: mitte = folgeMitte (60 %), minTop 10 %, Grundgroesse
#        mindestens folgeStapelBasis (.062 der Breite), linker Rand 9 %,
#        Breite 82 %. Zeilen im Stapel .6/.68 statt .54/.64 der Grundgroesse.
#      - Aufbau/Pointe etwas groesser (.036 / .064 der Breite).
#
#     GESICHTET: Cover (schwarz, Licht wieder da), Schrittfolge "06 - HOER
#     AUF ..." auf injiziertem Tagesfoto (gross, lesbar, mittig, kein Licht),
#     Fotofolie mit Aufbau/Pointe (kein Licht).

P.append((
 'lisaLicht:"",',
 'lisaLicht:"#7323D1",',
 'lisaLicht wieder an', 1))

P.append((
 'zLichtZeichnen=(zFarbGrund,zAus)=>{try{if(!BS_KACHEL.lisaLicht||zAus)return;',
 'zLichtZeichnen=(zFarbGrund,zAus)=>{try{if(!BS_KACHEL.lisaLicht||zAus||$)return;',
 'zLichtZeichnen: kein Licht auf Fotos', 1))

P.append((
 'zTop=zOpt.top,zMax=zOpt.maxBottom||n*.92,zClean=zq=>zq.replace(/\\*/g,"");const zNumM=',
 'zTop=zOpt.top,zMax=zOpt.maxBottom||n*.92,zMitte=typeof zOpt.mitte=="number",zMin=typeof zOpt.minTop=="number"?zOpt.minTop:n*.1,zClean=zq=>zq.replace(/\\*/g,"");const zNumM=',
 'zStapel: mitte/minTop lesen', 1))

P.append((
 'const zsz=zRl==="schritt"?.54:.64,ztxt=',
 'const zsz=zRl==="schritt"?.6:.68,ztxt=',
 'zStapel: Zeilen groesser', 1))

P.append((
 'const zBauen=zScale=>{let zY=zTop;const zBx=[];for(const zs of zSpecs){zY+=zs.gap*zBase*zScale;',
 'const zBauen=zScale=>{let zY=zMitte?0:zTop;const zBx=[];for(const zs of zSpecs){zY+=zs.gap*zBase*zScale;',
 'zStapel: bei Mitte ab 0 messen', 1))

P.append((
 'for(let zi=0;zi<45&&zErg.bottom>zMax&&zScale>.2;zi+=1)zScale-=.02,zErg=zBauen(zScale);zErg.bx.forEach(zt=>e.add(zt));return{top:zTop,height:zErg.bottom-zTop,originY:"top",originX:"left",bottom:zErg.bottom}}catch(zz){return null}},',
 'const zRaum=zMitte?zMax-zMin:zMax;for(let zi=0;zi<45&&zErg.bottom>zRaum&&zScale>.2;zi+=1)zScale-=.02,zErg=zBauen(zScale);let zOff=0;zMitte&&(zOff=Math.max(zMin,Math.min(zOpt.mitte-zErg.bottom/2,zMax-zErg.bottom)));zErg.bx.forEach(zt=>{zOff&&(zt.set("top",zt.top+zOff),zt.setCoords&&zt.setCoords());e.add(zt)});return zMitte?{top:zOff,height:zErg.bottom,originY:"top",originX:"left",bottom:zOff+zErg.bottom}:{top:zTop,height:zErg.bottom-zTop,originY:"top",originX:"left",bottom:zErg.bottom}}catch(zz){return null}},',
 'zStapel: um Mitte platzieren, Raum = minTop..maxBottom', 1))

P.append((
 'zHt=zRlG==="schritt"||zRlG==="liste"?zStapel(zRlG,t.text,{left:br,top:ae,width:r*(Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),fill:me,accentFill:Oe,fontSize:Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k()*zGr():t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),shadow:se(),maxBottom:Ke,fontFamily:zFont($)}):',
 'zHt=zRlG==="schritt"||zRlG==="liste"?zStapel(zRlG,t.text,{left:ge.folge===!0?r*.09:br,top:ae,width:r*(ge.folge===!0?.82:Ze?ot:kt?.46:ge.exactWidth||(_t?.82:.86)),fill:me,accentFill:Oe,fontSize:ge.folge===!0?Math.max(r*(Number(BS_KACHEL.folgeStapelBasis)||.062),c(ve)):Qt&&t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):Ze?k()*zGr():t.warmEditorial&&ge.exactFont?r*(ge.exactFont/1080):c(ve),mitte:ge.folge===!0?n*(Number(BS_KACHEL.folgeMitte)||.6):void 0,minTop:n*.1,shadow:se(),maxBottom:Ke,fontFamily:zFont($)}):',
 'Gradient-Zweig: Folge-Stapel groesser und zentriert', 1))

P.append((
 'lisaPayoffSetupGroesse)||.032',
 'lisaPayoffSetupGroesse)||.036',
 'Aufbausatz groesser', 1))

P.append((
 'lisaPayoffGroesse)||.058',
 'lisaPayoffGroesse)||.064',
 'Pointe groesser', 1))

P.append((
 'title:"Geladene Datei",children:"karten359"',
 'title:"Geladene Datei",children:"karten360"',
 'Versionsschild auf karten360', 1))


# --- karten361: Folgefolien in Montserrat; Variable-Font-Gewichte richtig
#     erkennen ----------------------------------------------------------------
#
#     "Welche sans serif ist das?" - Helvetica Neue. "Bitte lieber Montserrat."
#     Neuer Regler folgeSchrift ("Montserrat"), gilt fuer Aufbau/Pointe
#     (zSetupPayoff) und den Stapel im Folge-Layout. Cover bleibt Helvetica.
#
#     Dabei aufgefallen: Montserrat liegt als Variable Font vor (@font-face
#     font-weight "100 900"). At() las nur die erste Zahl und meldete als
#     einziges verfuegbares Gewicht 100 - Xt() schnappte deshalb jedes
#     gewuenschte Gewicht auf 100, der Stapel kam hauchduenn heraus (die
#     Aufbau/Pointe-Zeilen nicht, sie gehen nicht durch Xt). At() loest
#     Bereiche jetzt in 100er-Schritte auf; Einzelgewichte wie bei
#     HelveticaNeueBrand bleiben unveraendert.
#
#     GESICHTET: Stapel "06 - HOER AUF ..." in Montserrat Bold/Semibold,
#     Aufbau/Pointe in Montserrat, Cover unveraendert (Helvetica, Licht).

P.append((
 'folgeFoto:1,folgeOverlay:.38,folgeMitte:.6,',
 'folgeFoto:1,folgeOverlay:.38,folgeMitte:.6,folgeSchrift:"Montserrat",',
 'Regler folgeSchrift', 1))

P.append((
 'zFam=BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",zSetupSz=',
 'zFam=BS_KACHEL.folgeSchrift||BS_KACHEL.lisaSchrift||"HelveticaNeueBrand",zSetupSz=',
 'Aufbau/Pointe in folgeSchrift', 1))

P.append((
 'mitte:ge.folge===!0?n*(Number(BS_KACHEL.folgeMitte)||.6):void 0,minTop:n*.1,shadow:se(),maxBottom:Ke,fontFamily:zFont($)}):',
 'mitte:ge.folge===!0?n*(Number(BS_KACHEL.folgeMitte)||.6):void 0,minTop:n*.1,shadow:se(),maxBottom:Ke,fontFamily:ge.folge===!0?(BS_KACHEL.folgeSchrift||zFont($)):zFont($)}):',
 'Folge-Stapel in folgeSchrift', 1))

P.append((
 'At=ge=>{const Fe=[];try{document.fonts.forEach(me=>{if(me.family===ge||me.family===`"${ge}"`){const Oe=parseInt(String(me.weight).split(" ")[0],10);Number.isNaN(Oe)||Fe.push(Oe)}})}catch{}return Fe},',
 'At=ge=>{const Fe=[];try{document.fonts.forEach(me=>{if(me.family===ge||me.family===`"${ge}"`){const zW=String(me.weight).trim().split(/\\s+/),Oe=parseInt(zW[0],10),zB=zW.length>1?parseInt(zW[1],10):NaN;if(!Number.isNaN(Oe)&&!Number.isNaN(zB)){for(let zw=Math.min(Oe,zB);zw<=Math.max(Oe,zB);zw+=100)Fe.push(zw)}else Number.isNaN(Oe)||Fe.push(Oe)}})}catch{}return Fe},',
 'At(): Variable-Font-Gewichtsbereiche (z.B. 100 900) in Einzelgewichte aufloesen', 1))

P.append((
 'title:"Geladene Datei",children:"karten360"',
 'title:"Geladene Datei",children:"karten361"',
 'Versionsschild auf karten361', 1))


# --- karten362/363: "Das ist nicht Montserrat" - statische Montserrat-Schnitte
#     unter eigenem Namen, gezieltes Warten auf die Folge-Schrift ---------------
#
#     Nach 361 auf dem iPhone: "Das ist nicht Montserrat stell das ein". Im
#     Chromium-Test war es Montserrat; auf iOS offenbar nicht. Befund: die
#     einzige Montserrat-Datei im Projekt ist ein Variable Font (wght 100-900,
#     Default-Instanz Thin). Safari zeichnet Variable Fonts im Canvas nicht
#     zuverlaessig (Fallback bzw. Default-Instanz), Chromium schon - daher
#     der Unterschied zwischen Test und Handy.
#
#     Loesung (nicht im Bundle, sondern in site/): aus der Variable-Datei mit
#     fontTools vier statische Schnitte erzeugt (site/fonts/MontserratBrand-
#     400/500/600/700.woff2, je ~16 KB) und in site/index.html sowie
#     site/dunkel/index.html als @font-face "MontserratBrand" mit je EINEM
#     Gewicht eingetragen - dasselbe Muster wie HelveticaNeueBrand.
#
#     Im Bundle: folgeSchrift zeigt auf "MontserratBrand", die Familie steht
#     im allgemeinen Font-Preload, und das Folge-Layout wartet vor dem
#     Zeichnen gezielt (8 s) auf die Schnitte 500/600/700 der Folge-Schrift,
#     statt sich auf das 4-s-Preload-Rennen zu verlassen (362).
#
#     GESICHTET (Chromium): Stapel und Aufbau/Pointe in MontserratBrand
#     Bold/Semibold/Medium; auf iOS muss sie es bestaetigen.

P.append((
 'ge.folge===!0&&(Number(BS_KACHEL.folgeOverlay)||0)>0&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"rgba(0,0,0,"+(Number(BS_KACHEL.folgeOverlay)||.38)+")",selectable:!1,evented:!1}));',
 'if(ge.folge===!0){try{const zFS=BS_KACHEL.folgeSchrift||BS_KACHEL.lisaSchrift||"HelveticaNeueBrand";typeof document<"u"&&document.fonts&&document.fonts.load&&await Promise.race([Promise.all(["500","600","700"].map(zw=>document.fonts.load(`${zw} 44px "${zFS}"`).catch(()=>{}))),new Promise(zr=>setTimeout(zr,8e3))])}catch(zz){}}ge.folge===!0&&(Number(BS_KACHEL.folgeOverlay)||0)>0&&e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:"rgba(0,0,0,"+(Number(BS_KACHEL.folgeOverlay)||.38)+")",selectable:!1,evented:!1}));',
 'Folge-Layout: gezielt auf folgeSchrift warten, bevor gezeichnet wird', 1))

P.append((
 'title:"Geladene Datei",children:"karten361"',
 'title:"Geladene Datei",children:"karten362"',
 'Versionsschild auf karten362', 1))

P.append((
 'folgeSchrift:"Montserrat",',
 'folgeSchrift:"MontserratBrand",',
 'folgeSchrift -> MontserratBrand (statische Schnitte)', 1))

P.append((
 '"Anton","Montserrat","Playfair Display"',
 '"Anton","Montserrat","MontserratBrand","Playfair Display"',
 'MontserratBrand in den Font-Preload', 1))

P.append((
 'title:"Geladene Datei",children:"karten362"',
 'title:"Geladene Datei",children:"karten363"',
 'Versionsschild auf karten363', 1))


# --- karten364: lange Mehrzeilen-Texte sind Prosa, keine Liste ---------------
#
#     Screenshot ihrer Schlussfolie (9/9): ~20 kurze Zeilen, jede mit
#     Gedankenstrich als Listenpunkt gesetzt. "Loest du das so auf?" - nein.
#     Die Listen-Erkennung aus 292 (ab drei Zeilen mit stark wechselnder
#     Laenge) traf auch fliessende Schlusstexte, deren Zeilenumbrueche Pausen
#     sind, keine Aufzaehlung.
#
#     zRolle liefert ab 8 Zeilen "prosa". Im Folge-Layout laeuft Prosa ueber
#     zSetupPayoff im Prosa-Modus: Zeilenumbrueche bleiben (eine Textbox mit
#     \n), keine Striche, linksbuendig, Gewicht 500, folgeProsaGroesse (.04
#     der Breite), Zeilenabstand 1.3, um folgeMitte zentriert mit
#     Auto-Schrumpfung. Ohne Satzteilung (Aufbau/Pointe greift nicht).
#     Im plate-Zweig (Cover) faellt "prosa" wie "normal" auf Pt() zurueck.
#
#     GESICHTET: ihr Schlusstext (18 Zeilen) auf Tagesfoto - alles lesbar,
#     keine Bullets, passt in die Karte.

P.append((
 'return"schritt";if(zN<3)return"normal";const zLens=',
 'return"schritt";if(zN<3)return"normal";if(zN>7)return"prosa";const zLens=',
 'zRolle: >7 Zeilen = prosa', 1))

P.append((
 'const zPa=new Pe.fabric.Textbox(zU,{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zPayoffSz*zScale),fontFamily:zFam,fontWeight:"700",fill:"#FFFFFF",textAlign:"center",lineHeight:1.14,shadow:zOpt.shadow,selectable:!1});',
 'const zPr=zOpt.prosa===!0,zPa=new Pe.fabric.Textbox(zU,{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,(zPr?r*(Number(BS_KACHEL.folgeProsaGroesse)||.04):zPayoffSz)*zScale),fontFamily:zFam,fontWeight:zPr?"500":"700",fill:"#FFFFFF",textAlign:zPr?"left":"center",lineHeight:zPr?1.3:1.14,shadow:zOpt.shadow,selectable:!1});',
 'zSetupPayoff: Prosa-Modus', 1))

P.append((
 'if((i.slideIndex||0)>0&&!Ye&&!ge.bigWord&&!t.secondaryText&&zRolle(t.text)==="normal"&&(ge.folge===!0||!kt)){const zSp2=BS_KACHEL.lisaTeilen!==0?zTeilen($e?$e.rest:t.text,!1):null;if(zSp2||ge.folge===!0){zSetupPayoff(zSp2?zSp2.oben:"",zSp2?zSp2.unten:($e?$e.rest:t.text),{width:r*(ge.exactWidth||.82),top:ae,',
 'const zRo=zRolle(t.text);if((i.slideIndex||0)>0&&!Ye&&!ge.bigWord&&!t.secondaryText&&(zRo==="normal"||zRo==="prosa")&&(ge.folge===!0||!kt)){const zSp2=zRo!=="prosa"&&BS_KACHEL.lisaTeilen!==0?zTeilen($e?$e.rest:t.text,!1):null;if(zSp2||ge.folge===!0){zSetupPayoff(zSp2?zSp2.oben:"",zSp2?zSp2.unten:($e?$e.rest:t.text),{prosa:zRo==="prosa",width:r*(ge.exactWidth||.82),top:ae,',
 'Gradient-Zweig: Prosa ueber zSetupPayoff', 1))

P.append((
 'title:"Geladene Datei",children:"karten363"',
 'title:"Geladene Datei",children:"karten364"',
 'Versionsschild auf karten364', 1))


# --- karten365: Rahmen-Layouts raus, Layout-Waehler auf das Verwendete
#     reduziert ----------------------------------------------------------------
#
#     "Rahmen Layout raus und Layouts generell die wir nicht verwenden loeschen"
#
#     Drei Stellen:
#      1. Cover-Rotation layoutReihe: nur noch Foto Verlauf/unten links/oben/
#         Mitte und die vier Text-Flaechen (hell, dunkel-links, oben, minimal).
#         Raus: alle brand_frame_*, brand_photo_frame, Bigword, Zitat, Serif,
#         Statement, Kicker-Lead, Bold-oben. folgeReihe (nur noch Fallback,
#         falls folgeFoto aus) ebenso bereinigt.
#      2. Gespeicherte Rahmen-Layouts (Tag 17, 14, 9, 6, 4 im Plan) werden
#         beim Zeichnen auf brand_photo_gradient umgeleitet - direkt bei D,
#         damit auch die E-Liste (Rahmen-Layouts laden das Foto nicht ueber
#         u()) nicht mehr greift. Die lr-Eintraege bleiben stehen, sind aber
#         unerreichbar.
#      3. Layout-Waehler (TT): statt ~30 Eintraegen zehn - vier Foto-Cover,
#         Foto Folgefolie, Foto Highlight, vier Text-Flaechen. Die alten
#         Nicht-brand-Layouts (editorial_classic, cover_* usw.) sind raus.
#
#     GESICHTET: Cover mit gespeichertem brand_frame_left + Foto rendert
#     als volles Foto mit Text, kein Rahmen.

P.append((
 'layoutReihe:"brand_photo_bottom_left|brand_text_quote|brand_frame_top_text|brand_photo_top|brand_text_left|brand_photo_gradient|brand_photo_center|brand_text_plate|brand_photo_bottom_serif|brand_frame_top_text|brand_photo_bigword|brand_text_statement|brand_photo_quote|brand_frame_left|brand_text_plate_top|brand_photo_bottom_left|brand_text_bigword|brand_photo_frame|brand_text_minimal|brand_photo_top"',
 'layoutReihe:"brand_photo_bottom_left|brand_text_plate|brand_photo_top|brand_text_left|brand_photo_gradient|brand_photo_center|brand_text_plate_top|brand_text_minimal"',
 'layoutReihe bereinigt', 1))

P.append((
 'folgeReihe:"brand_text_quote|brand_text_left|brand_text_plate_top|brand_text_statement|brand_text_minimal|brand_text_bigword|brand_text_kicker_lead|brand_text_bold_top"',
 'folgeReihe:"brand_text_left|brand_text_plate_top|brand_text_minimal|brand_text_plate"',
 'folgeReihe bereinigt', 1))

P.append((
 'let D=t.layout||"centered_focus";',
 'let D=t.layout||"centered_focus";/^brand_(frame_|photo_frame)/.test(D)&&(D="brand_photo_gradient");',
 'Rahmen-Layouts -> Foto Verlauf', 1))

P.append((
 'TT=({currentLayout:e,onUpdate:t})=>{const r=[{id:"brand_photo_gradient",name:"Foto Verlauf",icon:Bu,description:"Text unten auf Foto"},{id:"brand_photo_bottom_left",name:"Foto unten links",icon:CA,description:"Text unten links"},{id:"brand_photo_highlight",name:"Foto Highlight",icon:Xh,description:"Weißer Text, lila Highlight"},{id:"brand_photo_top",name:"Foto oben",icon:CA,description:"Text oben auf Foto"},{id:"brand_photo_center",name:"Foto Mitte",icon:vo,description:"Text mittig auf Foto"},{id:"brand_photo_bigword",name:"Foto Big-Word",icon:vo,description:"Riesenwort auf Foto"},{id:"brand_photo_quote",name:"Foto Zitat",icon:Xh,description:"Kicker + Zitat"},{id:"brand_photo_bottom_serif",name:"Foto Serif",icon:xc,description:"Serif unten + Fuß"},{id:"brand_photo_frame",name:"Foto gerahmt",icon:P2,description:"Foto im Rahmen"},{id:"brand_frame_top_text",name:"Rahmen Text oben",icon:P2,description:"Text über Rahmen"},{id:"brand_frame_left",name:"Rahmen links",icon:_3,description:"Rahmen versetzt"},{id:"brand_frame_polaroid",name:"Polaroid",icon:XA,description:"Foto wie Polaroid"},{id:"brand_text_plate",name:"Text-Fläche",icon:XA,description:"Text mittig, Rahmen"},{id:"brand_text_plate_top",name:"Fläche oben",icon:CA,description:"Text oben"},{id:"brand_text_left",name:"Fläche links",icon:CA,description:"Text linksbündig"},{id:"brand_text_bigword",name:"Big-Word",icon:vo,description:"Riesenwort-Statement"},{id:"brand_text_quote",name:"Zitat-Fläche",icon:Xh,description:"Kicker + Zitat"},{id:"brand_text_statement",name:"Statement",icon:xc,description:"Aussage + Fußzeile"},{id:"brand_text_kicker_lead",name:"Kicker-Lead",icon:xc,description:"Kicker führt ein"},{id:"brand_text_minimal",name:"Minimal",icon:XA,description:"Nur Text, ruhig"},{id:"brand_text_bold_top",name:"Bold oben links",icon:vo,description:"Großer Text oben links"},{id:"editorial_classic",name:"Classic Center",icon:XA,description:"Klarer, zentrierter Text"},{id:"minimal_quote",name:"Quote Focus",icon:Xh,description:"Zitat-Stil, ruhig"},{id:"maximized_bold",name:"Impact Text",icon:vo,description:"Großer Aussage-Text"},{id:"paper_box",name:"Paper Box",icon:xc,description:"Text auf ruhiger Fläche"},{id:"cover_top_center",name:"Cover Oben",icon:CA,description:"Titel oben auf Foto"},{id:"cover_center_hero",name:"Cover Mitte",icon:vo,description:"Großer Titel mittig"},{id:"cover_bottom_center",name:"Cover Unten",icon:L3,description:"Titel unten zentriert"},{id:"cover_top_left",name:"Cover Oben Links",icon:T3,description:"Titel oben links"},{id:"cover_bottom_left",name:"Cover Unten Links",icon:N3,description:"Titel unten links"}];',
 'TT=({currentLayout:e,onUpdate:t})=>{const r=[{id:"brand_photo_gradient",name:"Foto Verlauf",icon:Bu,description:"Text unten auf Foto"},{id:"brand_photo_bottom_left",name:"Foto unten links",icon:CA,description:"Text unten links"},{id:"brand_photo_top",name:"Foto oben",icon:CA,description:"Text oben auf Foto"},{id:"brand_photo_center",name:"Foto Mitte",icon:vo,description:"Text mittig auf Foto"},{id:"brand_photo_folge",name:"Foto Folgefolie",icon:vo,description:"Aufbau + Pointe auf Foto"},{id:"brand_photo_highlight",name:"Foto Highlight",icon:Xh,description:"Weißer Text, lila Highlight"},{id:"brand_text_plate",name:"Text-Fläche hell",icon:XA,description:"Text mittig, weißer Grund"},{id:"brand_text_left",name:"Text-Fläche dunkel",icon:CA,description:"Text linksbündig, schwarzer Grund"},{id:"brand_text_plate_top",name:"Fläche oben",icon:CA,description:"Text oben, weißer Grund"},{id:"brand_text_minimal",name:"Minimal",icon:XA,description:"Nur Text, ruhig"}];',
 'Layout-Waehler auf verwendete Layouts reduziert', 1))

P.append((
 'title:"Geladene Datei",children:"karten364"',
 'title:"Geladene Datei",children:"karten365"',
 'Versionsschild auf karten365', 1))


# --- karten366/367: Position/Ausrichtung der Folgefolien variiert ("zu statisch"),
#     Grundschrift jetzt Montserrat auch aufs Cover ----------------------------
#
#     "Ich finde den Stil irgendwie fad" -> Nachfrage, was genau: "Zu statisch/
#     ruhig, keine Energie". Jede Folgefolie sass immer exakt gleich (Aufbau
#     klein + Pointe fett, immer bei 60% Hoehe, immer zentriert).
#
#     Neuer Helfer zFolgeVar(): liest folgeMitteReihe/folgeAusrichtungReihe
#     (Pipe-Listen, gleiches Prinzip wie saettigungReihe/tonReihe) und waehlt
#     ueber einen Hash aus Tag+Folienindex+Textanfang eine feste, aber
#     zwischen Tagen wechselnde vertikale Position und Ausrichtung (zentriert
#     oder linksbuendig). zSetupPayoff() kennt jetzt einen align-Parameter
#     (center/links, linksbuendig ab r*.09) statt immer zentriert zu
#     zeichnen; der Stapel im Folge-Layout uebernimmt dieselbe Mitte.
#
#     Danach: "Montserrat auch vorne" - Ct() (Basis-Schriftwahl, auch fuers
#     Cover) fiel bisher hart auf HelveticaNeueBrand zurueck statt den Regler
#     zu lesen. Jetzt liest sie lisaSchrift; lisaSchrift steht auf
#     MontserratBrand, damit Cover und alles ohne spezifischere Schrift-
#     Vorgabe (Highlight-Layout bleibt Playfair, Folge behaelt folgeSchrift)
#     einheitlich Montserrat zeigen.
#
#     GESICHTET: vier Tage mit identischem Folgetext, unterschiedliche
#     Tag-Nummern - jeweils andere vertikale Position, einer davon
#     linksbuendig statt zentriert (per Debug-Log bestaetigt: zFolgeVar()
#     liefert korrekt wechselnde Werte). Cover + Schrittfolge auf Foto
#     beide in Montserrat.

P.append((
 'folgeFoto:1,folgeOverlay:.38,folgeMitte:.6,folgeSchrift:"MontserratBrand",',
 'folgeFoto:1,folgeOverlay:.38,folgeMitte:.6,folgeMitteReihe:".38|.48|.6|.72",folgeAusrichtungReihe:"center|left|center|left",folgeSchrift:"MontserratBrand",',
 'Regler folgeMitteReihe/folgeAusrichtungReihe', 1))

P.append((
 'zSetupPayoff=(zOben,zUnten,zOpt)=>{try{',
 'zFolgeVar=()=>{try{const zS=String(t._tag)+"|"+String(i.slideIndex||0)+"|"+String(t.text||"").slice(0,24)+"|fv";let zh=0;for(let zi=0;zi<zS.length;zi+=1)zh=(zh*31+zS.charCodeAt(zi))%99991;const zM=String(BS_KACHEL.folgeMitteReihe||"").split("|").map(Number).filter(zq=>!isNaN(zq)),zA=String(BS_KACHEL.folgeAusrichtungReihe||"").split("|").filter(Boolean);return{mitte:zM.length?zM[zh%zM.length]:(Number(BS_KACHEL.folgeMitte)||.6),align:zA.length?zA[(zh*7)%zA.length]:"center"}}catch(zz){return{mitte:Number(BS_KACHEL.folgeMitte)||.6,align:"center"}}},zSetupPayoff=(zOben,zUnten,zOpt)=>{try{',
 'Helfer zFolgeVar()', 1))

P.append((
 'if(!zU)return null;const zBauen=zScale=>{let zY=0;const zBx=[];if(zO){const zSe=new Pe.fabric.Textbox(zO,{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fill:"#FFFFFF",textAlign:"center",lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});zY+=(zSe.height||0)+zPayoffSz*zScale*.3;zBx.push(zSe)}const zPr=zOpt.prosa===!0,zPa=new Pe.fabric.Textbox(zU,{left:r/2-zW/2,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,(zPr?r*(Number(BS_KACHEL.folgeProsaGroesse)||.04):zPayoffSz)*zScale),fontFamily:zFam,fontWeight:zPr?"500":"700",fill:"#FFFFFF",textAlign:zPr?"left":"center",lineHeight:zPr?1.3:1.14,shadow:zOpt.shadow,selectable:!1});zY+=(zPa.height||0);zBx.push(zPa);return{bx:zBx,h:zY}};',
 'if(!zU)return null;const zAlignBase=zOpt.prosa===!0?"left":(zOpt.align||"center"),zLeft=zAlignBase==="left"?(typeof zOpt.leftMargin=="number"?zOpt.leftMargin:r*.09):r/2-zW/2,zTA=zAlignBase==="left"?"left":"center";const zBauen=zScale=>{let zY=0;const zBx=[];if(zO){const zSe=new Pe.fabric.Textbox(zO,{left:zLeft,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fill:"#FFFFFF",textAlign:zTA,lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});zY+=(zSe.height||0)+zPayoffSz*zScale*.3;zBx.push(zSe)}const zPr=zOpt.prosa===!0,zPa=new Pe.fabric.Textbox(zU,{left:zLeft,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,(zPr?r*(Number(BS_KACHEL.folgeProsaGroesse)||.04):zPayoffSz)*zScale),fontFamily:zFam,fontWeight:zPr?"500":"700",fill:"#FFFFFF",textAlign:zTA,lineHeight:zPr?1.3:1.14,shadow:zOpt.shadow,selectable:!1});zY+=(zPa.height||0);zBx.push(zPa);return{bx:zBx,h:zY}};',
 'zSetupPayoff: align-Parameter (center/left)', 1))

P.append((
 'if(zSp2||ge.folge===!0){zSetupPayoff(zSp2?zSp2.oben:"",zSp2?zSp2.unten:($e?$e.rest:t.text),{prosa:zRo==="prosa",width:r*(ge.exactWidth||.82),top:ae,mitte:ge.folge===!0?n*(Number(BS_KACHEL.folgeMitte)||.6):void 0,minTop:n*.1,maxBottom:Ke,shadow:se()});',
 'if(zSp2||ge.folge===!0){const zFV=ge.folge===!0?zFolgeVar():null;zSetupPayoff(zSp2?zSp2.oben:"",zSp2?zSp2.unten:($e?$e.rest:t.text),{prosa:zRo==="prosa",align:zFV?zFV.align:void 0,width:r*(ge.exactWidth||.82),top:ae,mitte:zFV?n*zFV.mitte:void 0,minTop:n*.1,maxBottom:Ke,shadow:se()});',
 'Aufruf zSetupPayoff mit zFolgeVar()', 1))

P.append((
 'mitte:ge.folge===!0?n*(Number(BS_KACHEL.folgeMitte)||.6):void 0,minTop:n*.1,shadow:se(),maxBottom:Ke,fontFamily:ge.folge===!0?(BS_KACHEL.folgeSchrift||zFont($)):zFont($)}):P',
 'mitte:ge.folge===!0?n*zFolgeVar().mitte:void 0,minTop:n*.1,shadow:se(),maxBottom:Ke,fontFamily:ge.folge===!0?(BS_KACHEL.folgeSchrift||zFont($)):zFont($)}):P',
 'Stapel im Folge-Layout: Mitte ueber zFolgeVar()', 1))

P.append((
 'title:"Geladene Datei",children:"karten365"',
 'title:"Geladene Datei",children:"karten366"',
 'Versionsschild auf karten366', 1))

P.append((
 'return Ft.has(Fe)||t.headlineFontChosen===!0&&Fe?Fe:!Fe||We.has(Fe)?"HelveticaNeueBrand":Bt(Fe)?Fe:(console.warn(`[BrandStudio] Schrift "${Fe}" ist nicht geladen — es wird HelveticaNeueBrand gesetzt.`),"HelveticaNeueBrand")},',
 'const zDef=BS_KACHEL.lisaSchrift||"HelveticaNeueBrand";return Ft.has(Fe)||t.headlineFontChosen===!0&&Fe?Fe:!Fe||We.has(Fe)?zDef:Bt(Fe)?Fe:(console.warn(`[BrandStudio] Schrift "${Fe}" ist nicht geladen — es wird ${zDef} gesetzt.`),zDef)},',
 'Ct(): Grundschrift-Fallback liest lisaSchrift', 1))

P.append((
 'lisaSchrift:"HelveticaNeueBrand"',
 'lisaSchrift:"MontserratBrand"',
 'lisaSchrift -> MontserratBrand (Cover + Grundschrift)', 1))

P.append((
 'title:"Geladene Datei",children:"karten366"',
 'title:"Geladene Datei",children:"karten367"',
 'Versionsschild auf karten367', 1))

# 368 — Screenshot ihres Instagram-Rasters: "Bitte Bau wieder das und
# halte mich ab es umzubauen". Der Stil dort (Serifen-Headline + kursive
# kleine Zeile darunter) ist genau das, was 302 aus der Rotation nahm.
# DM Serif Display liegt bereits selbst gehostet mit echtem Kursiv-Schnitt
# vor (site/index.html) - kein neuer Font-Import noetig.

P.append((
 'lisaSchrift:"MontserratBrand"',
 'lisaSchrift:"DM Serif Display"',
 'Cover-Schrift -> DM Serif Display', 1))

P.append((
 'folgeSchrift:"MontserratBrand"',
 'folgeSchrift:"DM Serif Display"',
 'Folgefolien-Schrift -> DM Serif Display', 1))

P.append((
 'const zSe=new Pe.fabric.Textbox(zO,{left:zLeft,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fill:"#FFFFFF",textAlign:zTA,lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});',
 'const zSe=new Pe.fabric.Textbox(zO,{left:zLeft,top:zY,originX:"left",originY:"top",width:zW,fontSize:Math.max(10,zSetupSz*zScale),fontFamily:zFam,fontWeight:"500",fontStyle:"italic",fill:"#FFFFFF",textAlign:zTA,lineHeight:1.24,shadow:zOpt.shadow,selectable:!1});',
 'Aufbau-Zeile kursiv', 1))

P.append((
 'await Promise.race([Promise.all(Fe),new Promise(me=>setTimeout(me,4e3))])}}catch{}try{e.clear(),',
 'await Promise.race([Promise.all(Fe),new Promise(me=>setTimeout(me,4e3))])}}catch{}'
 'try{const zLF=new Set([BS_KACHEL.lisaSchrift,BS_KACHEL.folgeSchrift].filter(Boolean));'
 'zLF.size&&typeof document<"u"&&document.fonts&&document.fonts.load&&'
 'await Promise.race([Promise.all([...zLF].flatMap(zf=>["400","500","600","700","italic 400"].map(zw=>document.fonts.load(`${zw} 44px "${zf}"`).catch(()=>{})))),'
 'new Promise(zr=>setTimeout(zr,8e3))])}catch(zz){}'
 'try{e.clear(),',
 'gezielt auf lisaSchrift/folgeSchrift warten (normal + kursiv)', 1))

P.append((
 'title:"Geladene Datei",children:"karten367"',
 'title:"Geladene Datei",children:"karten368"',
 'Versionsschild auf karten368', 1))


# 369 — "Exakt wie am Bild": eigener Raster-Zeichner (Regler rasterStil).
# Playfair Display 400 zentriert, auf Foto darunter Handschrift "Nothing You
# Could Do" (erster Satz/erste Zeile gross, Rest Handschrift, ~Zeilen und
# Subtext immer Handschrift); ohne Foto weisse Flaeche, alles Playfair schwarz.

P.append((
 'lisaSchrift:"DM Serif Display"',
 'lisaSchrift:"Playfair Display",rasterStil:1,rasterSerif:"Playfair Display",rasterHand:"Nothing You Could Do",rasterHandMax:120,rasterMitte:.57,rasterMitteFlaeche:.5,rasterDunkel:1,rasterGrund:"#FFFFFF",rasterTinte:"#111111"',
 'Regler rasterStil + Schriften wie im Instagram-Raster', 1))

P.append((
 'folgeSchrift:"DM Serif Display"',
 'folgeSchrift:"Playfair Display"',
 'folgeSchrift -> Playfair Display', 1))

P.append((
 'if(t.tileMode==="xpost"){',
 'if(Number(BS_KACHEL.rasterStil)===1&&t.tileMode!=="xpost"&&t.textBands!==!0&&t.isCtaSlide!==!0){const zRS=BS_KACHEL.rasterSerif||"Playfair Display",zRH=BS_KACHEL.rasterHand||"Nothing You Could Do";try{typeof document<"u"&&document.fonts&&document.fonts.load&&await Promise.race([Promise.all([`400 44px "${zRS}"`,`400 44px "${zRH}"`].map(zw=>document.fonts.load(zw).catch(()=>{}))),new Promise(zr=>setTimeout(zr,8e3))])}catch(zz){}const zRL=Be(t.text),zRT=String(zRL?zRL.rest:(t.text||"")).replace(/\\*/g,"").replace(/\\r/g,"").trim();let zKopf=zRT,zHand=String(t.secondaryText||"").replace(/\\*/g,"").trim();const zZl=zRT.split("\\n").map(zq=>zq.trim()).filter(Boolean),zTil=zZl.filter(zq=>zq[0]==="~"),zHM=Number(BS_KACHEL.rasterHandMax)||120;if(zTil.length){zKopf=zZl.filter(zq=>zq[0]!=="~").join("\\n");zHand=[zHand,...zTil.map(zq=>zq.slice(1).trim())].filter(Boolean).join(" ")}else if(!zHand&&$){if(zZl.length>1){const zR=zZl.slice(1).join(" ");zR.length<=zHM&&zZl.length<=4&&(zKopf=zZl[0],zHand=zR)}else{const zSz=(zRT.match(/[^.!?…]+[.!?…]+["“”„]*|[^.!?…]+$/g)||[]).map(zq=>zq.trim()).filter(Boolean);if(zSz.length>1){const zR=zSz.slice(1).join(" ");zR.length<=zHM&&(zKopf=zSz[0],zHand=zR)}}}const zFg=$?"#FFFFFF":(BS_KACHEL.rasterTinte||"#111111"),zDk=Number(BS_KACHEL.rasterDunkel);const zDm=isNaN(zDk)?1:zDk;if($){e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:n},colorStops:[{offset:0,color:"rgba(0,0,0,"+Math.min(.9,.16*zDm)+")"},{offset:.45,color:"rgba(0,0,0,"+Math.min(.9,.34*zDm)+")"},{offset:1,color:"rgba(0,0,0,"+Math.min(.9,.5*zDm)+")"}]})}))}else e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:BS_KACHEL.rasterGrund||"#FFFFFF",selectable:!1,evented:!1}));const zSh=$?new Pe.fabric.Shadow({color:"rgba(0,0,0,0.35)",blur:r*.012,offsetX:0,offsetY:r*.002}):null;const zBox=(zTx,zFam,zSz0,zMin,zW,zMaxH,zLH,zCs)=>{let zSz=zSz0,zB=null;for(let zi=0;zi<80;zi++){zB=new Pe.fabric.Textbox(zTx,{left:r/2,top:0,originX:"center",originY:"top",width:zW,fontSize:zSz,fontFamily:zFam,fontWeight:"400",fill:zFg,textAlign:"center",lineHeight:zLH,charSpacing:zCs,shadow:zSh,selectable:!1});zB.initDimensions&&zB.initDimensions();if((zB.width||0)<=zW+1&&(zB.height||0)<=zMaxH||zSz<=zMin)break;zSz=Math.max(zMin,zSz*.96)}return zB};const zBx=[],zGap=r*.035;let zH=0;if(zKopf){const zK=zBox(zKopf,zRS,r*($?(zHand?.098:.118):.085),r*.04,r*($?.8:.84),n*($?(zHand?.34:.56):.6),$?1.08:1.06,-10);zBx.push(zK);zH+=zK.height||0}if(zHand){const zHd=zBox(zHand,zRH,r*.056,r*.032,r*(zHand.length>60?.6:.5),n*.26,1.2,0);zBx.length&&(zH+=zGap);zBx.push(zHd);zH+=zHd.height||0}const zMit=n*($?(Number(BS_KACHEL.rasterMitte)||.57):(Number(BS_KACHEL.rasterMitteFlaeche)||.5));let zTop=Math.max(n*.08,Math.min(zMit-zH/2,Ke-zH));zBx.forEach(zb=>{zb.set("top",zTop);zb.setCoords&&zb.setCoords();e.add(zb);zTop+=(zb.height||0)+zGap});if(t.overlayImage)try{await Ae(t.overlayImage)}catch{}zRL&&be(zRL.label),Le(),e.renderAll();return}if(t.tileMode==="xpost"){',
 'Raster-Zeichner (Playfair + Handschrift, wie Instagram-Raster)', 1))

P.append((
 'title:"Geladene Datei",children:"karten368"',
 'title:"Geladene Datei",children:"karten369"',
 'Versionsschild auf karten369', 1))


# 370 — "Sei genauer und suche in dem Chat nach Handschrift und Aufteilung":
# ihr Raster stammt aus dem Feed-Zeichner (Stand karten292-296), nicht aus einem
# Layout. Dessen Regler zurueck (Playfair statt Helvetica, layoutAn 0, textMitte .5,
# folgeLayouts 0), der Nachbau rasterStil aus. Dazu Helligkeit beidseitig angleichen.

P.append((
 ',fotoSchrift:"HelveticaNeueBrand"',
 ',fotoSchrift:"Playfair Display"',
 'fotoSchrift -> Playfair Display', 1))

P.append((
 ',deckblattFamilie:"HelveticaNeueBrand"',
 ',deckblattFamilie:"Playfair Display"',
 'deckblattFamilie -> Playfair Display', 1))

P.append((
 ',folgeFamilie:"HelveticaNeueBrand"',
 ',folgeFamilie:"Playfair Display"',
 'folgeFamilie -> Playfair Display', 1))

P.append((
 ',ablaufTitel:"HelveticaNeueBrand"',
 ',ablaufTitel:"Playfair Display"',
 'ablaufTitel -> Playfair Display', 1))

P.append((
 ',kastenSchrift:"HelveticaNeueBrand"',
 ',kastenSchrift:"Playfair Display"',
 'kastenSchrift -> Playfair Display', 1))

P.append((
 ',layoutAn:1,',
 ',layoutAn:0,',
 'layoutAn aus', 1))

P.append((
 ',textMitte:.58,',
 ',textMitte:.5,',
 'textMitte .5', 1))

P.append((
 ',folgeLayouts:1,',
 ',folgeLayouts:0,',
 'folgeLayouts aus', 1))

P.append((
 ',rasterStil:1,',
 ',rasterStil:0,',
 'Nachbau rasterStil aus', 1))

P.append((
 ',hellKraft:.8,',
 ',hellKraft:.8,hellAngleich:1,hellDunkelMin:.5,hellAngleichMax:2,',
 'Regler hellAngleich/hellDunkelMin/hellAngleichMax', 1))

P.append((
 'zg=Math.min(zMax,Math.max(1,Math.pow(zZiel/Math.max(1,zm),Number(BS_KACHEL.hellKraft)||.8)));if(zg>1.015){',
 'zg=Number(BS_KACHEL.hellAngleich)===1?Math.min(Number(BS_KACHEL.hellAngleichMax)||2,Math.max(1,Math.log(Math.min(.98,Math.max(.02,zm/255)))/Math.log(Math.min(.98,Math.max(.02,zZiel/255))))):Math.min(zMax,Math.max(1,Math.pow(zZiel/Math.max(1,zm),Number(BS_KACHEL.hellKraft)||.8)));if(Number(BS_KACHEL.hellAngleich)===1&&zm>zZiel+2&&Pe.fabric.Image.filters.BlendColor){const zk=Math.max(Number(BS_KACHEL.hellDunkelMin)||.5,zZiel/zm),zgr=Math.round(255*zk).toString(16).padStart(2,"0");me.filters=(me.filters||[]).concat([new Pe.fabric.Image.filters.BlendColor({color:"#"+zgr+zgr+zgr,mode:"multiply",alpha:1})]);me.applyFilters()}if(zg>1.015){',
 'Helligkeit angleichen: dunkle per Gamma rauf, helle linear runter', 1))

P.append((
 'title:"Geladene Datei",children:"karten369"',
 'title:"Geladene Datei",children:"karten370"',
 'Versionsschild auf karten370', 1))


# 371 — "Mit * und hinter dem letzten Wort * werden alle Worte dazwischen
# handschriftlich": *...* setzt im Feed-Zeichner Handschrift statt kursiv.

P.append((
 ',rasterStil:0,',
 ',rasterStil:0,sternHand:1,',
 'Regler sternHand', 1))

P.append((
 'rt.push({w:ct,kursiv:zk,fett:zf,hand:zh})',
 'rt.push({w:ct,kursiv:zk&&BS_KACHEL.sternHand!==1,fett:zf,hand:zh||zk&&BS_KACHEL.sternHand===1})',
 '*...* setzt Handschrift statt kursiv', 1))

P.append((
 '"Tipp: Wörter in *Sternchen* werden hervorgehoben."',
 '"Tipp: *vor dem ersten und nach dem letzten Wort* – alles dazwischen wird Handschrift."',
 'Editor-Tipp', 1))

P.append((
 'title:"Wort markieren für Highlights",children:[v.jsx(ke,{icon:oK,className:"mr-1"})," Highlight (*Wort*)"]',
 'title:"Wörter in Handschrift setzen",children:[v.jsx(ke,{icon:oK,className:"mr-1"})," Handschrift (*…*)"]',
 'Editor-Knopf', 1))

P.append((
 'title:"Geladene Datei",children:"karten370"',
 'title:"Geladene Datei",children:"karten371"',
 'Versionsschild auf karten371', 1))


# 372 — "Mit _ vor dem ersten und hinter dem letzten Wort_ wird alles dazwischen
# 10% groesser in der Playfair Schrift". Dazu Wortabstaende in der zweiten Zeile
# (Zeichnen und Zentrieren) je Wort in dessen eigener Schrift und Groesse.

P.append((
 ',sternHand:1,',
 ',sternHand:1,strichGross:1,grossAnteil:1.1,',
 'Regler strichGross/grossAnteil', 1))

P.append((
 'rt.push({w:ct,kursiv:zk&&BS_KACHEL.sternHand!==1,fett:zf,hand:zh||zk&&BS_KACHEL.sternHand===1})',
 'rt.push({w:ct,kursiv:zk&&BS_KACHEL.sternHand!==1,fett:zf,hand:zh&&BS_KACHEL.strichGross!==1||zk&&BS_KACHEL.sternHand===1,gross:zh&&BS_KACHEL.strichGross===1})',
 '_..._ setzt Playfair +10% statt Handschrift', 1))

P.append((
 'sr=Je=>Je.some(rt=>rt.kursiv||rt.fett||rt.hand),zwf=(xt,zg)=>xt&&xt.hand?(BS_KACHEL.handFamilie||BS_KACHEL.zweiteFamilie||zg):zg,',
 'sr=Je=>Je.some(rt=>rt.kursiv||rt.fett||rt.hand||rt.gross),zwf=(xt,zg)=>xt&&xt.gross?(BS_KACHEL.grossFamilie||Qe):xt&&xt.hand?(BS_KACHEL.handFamilie||BS_KACHEL.zweiteFamilie||zg):zg,',
 'zwf: grosse Woerter in der Hauptschrift', 1))

P.append((
 'zws=(xt,zg)=>xt&&xt.hand?zg*(BS_KACHEL.handAnteil||1):zg,',
 'zws=(xt,zg)=>xt&&xt.gross?zg*(Number(BS_KACHEL.grossAnteil)||1.1):xt&&xt.hand?zg*(BS_KACHEL.handAnteil||1):zg,',
 'zws: grosse Woerter +10%', 1))

P.append((
 'e.add(Ut),Vt+=Ut.width+ot})',
 'e.add(Ut),Vt+=Ut.width+(Ve?ot:(()=>{const zo={fontSize:Ut.fontSize,fontFamily:Ut.fontFamily,fontWeight:Ut.fontWeight},zp=new Pe.fabric.Text("M M",zo).width-new Pe.fabric.Text("MM",zo).width;return zp>0&&zp<Ut.fontSize?zp:Ut.fontSize*.25})())})',
 'Wortabstand in der zweiten Zeile', 1))

P.append((
 'return Je.reduce((Vt,Tt)=>Vt+new Pe.fabric.Text(Tt.w,{...pt,fontFamily:zwf(Tt,pt.fontFamily),fontWeight:zwg(Tt,pt.fontWeight),fontSize:zws(Tt,pt.fontSize),fontStyle:Tt.kursiv?"italic":"normal"}).width,0)+ct*Math.max(0,Je.length-1)}',
 'if(!Ve)return Je.reduce((Vt,Tt,Ti)=>{const zo={...pt,fontFamily:zwf(Tt,pt.fontFamily),fontWeight:zwg(Tt,pt.fontWeight),fontSize:zws(Tt,pt.fontSize),fontStyle:Tt.kursiv?"italic":"normal"},zsp=new Pe.fabric.Text("M M",zo).width-new Pe.fabric.Text("MM",zo).width;return Vt+new Pe.fabric.Text(Tt.w,zo).width+(Ti<Je.length-1?(zsp>0&&zsp<zo.fontSize?zsp:zo.fontSize*.25):0)},0);return Je.reduce((Vt,Tt)=>Vt+new Pe.fabric.Text(Tt.w,{...pt,fontFamily:zwf(Tt,pt.fontFamily),fontWeight:zwg(Tt,pt.fontWeight),fontSize:zws(Tt,pt.fontSize),fontStyle:Tt.kursiv?"italic":"normal"}).width,0)+ct*Math.max(0,Je.length-1)}',
 'Zentrieren misst Wortabstaende wie beim Zeichnen', 1))

P.append((
 'title:"Geladene Datei",children:"karten371"',
 'title:"Geladene Datei",children:"karten372"',
 'Versionsschild auf karten372', 1))


# 373 — "Jetzt ist es kursiv aber nicht Playfair bei * * und die Textkacheln
# ploetzlich mit lila Licht": zLay fragt den Schalter wieder vor dem
# gespeicherten Layout (wie 234), Lila-Licht aus, Textkachel versteht *...* und _..._.

P.append((
 'const ze=zs&&zs.layout;if(ze&&String(ze).indexOf("brand_")===0)return ze;if(BS_KACHEL.layoutAn!==1)return "";',
 'if(BS_KACHEL.layoutAn!==1)return "";const ze=zs&&zs.layout;if(ze&&String(ze).indexOf("brand_")===0)return ze;',
 'zLay: Schalter vor gespeichertem Layout', 1))

P.append((
 'lisaLichtStaerke:.42',
 'lisaLichtStaerke:0',
 'Lila-Licht aus', 1))

P.append((
 'lisaLichtStaerkeHell:.16',
 'lisaLichtStaerkeHell:0',
 'Lila-Licht (hell) aus', 1))

P.append((
 'const B0=ROH.replace(/\\*/g,"").split(/\\n\\s*\\n/).map(x=>x.trim()).filter(Boolean);',
 'const B0=ROH.replace(BS_KACHEL.strichGross===1?/[*_]/g:/\\*/g,"").split(/\\n\\s*\\n/).map(x=>x.trim()).filter(Boolean);const zHW=(()=>{if(BS_KACHEL.sternHand!==1&&BS_KACHEL.strichGross!==1)return null;const zo=[];let zS=!1,zU=!1,zcur="",zm="";const zpu=()=>{zcur&&zo.push({w:zcur,m:zm});zcur="";zm=""};for(const zc of String(ROH||"")){if(zc==="*"&&BS_KACHEL.sternHand===1){zS=!zS;continue}if(zc==="*"){continue}if(zc==="_"&&BS_KACHEL.strichGross===1){zU=!zU;continue}if(/\\s/.test(zc)){zpu();continue}zcur+=zc;zS?zm="h":zU&&!zm&&(zm="g")}zpu();return zo.some(zq=>zq.m)?zo:null})();let zHP=0;',
 'Textkachel: markierte Woerter merken (* Handschrift, _ Playfair gross)', 1))

P.append((
 'ZL.forEach((blk,ix)=>{const g2=GRO(ix,gr);\nblk.forEach(z=>{txt(z,{left:LI?r*K.rand:r/2,top:y,originX:LI?"left":"center",originY:"center",\nfontSize:g2,fontFamily:FAM(ix),fontWeight:GEW(ix),fill:SCH,\ncharSpacing:LW,maxB:MESS});\ny+=g2*K.zeile});',
 'ZL.forEach((blk,ix)=>{const g2=GRO(ix,gr);\nblk.forEach(z=>{const zWs=String(z).split(/\\s+/).filter(Boolean),zFl=zHW?zWs.map(zw=>{const zq=zHW[zHP++];return zq&&zq.w===zw?zq.m:""}):[];if(zFl.some(Boolean)){const zHF=K.handFamilie||K.zweiteFamilie||"Nothing You Could Do",zGF=K.grossFamilie||"Playfair Display",zHS=g2*(Number(K.handAnteil)||1),zGS=g2*(Number(K.grossAnteil)||1.1),zmk=(zw,zf,zq)=>new Pe.fabric.Text(zw,{fontSize:(zf==="h"?zHS:zf==="g"?zGS:g2)*zq,fontFamily:zf==="h"?zHF:zf==="g"?zGF:FAM(ix),fontWeight:zf?"400":GEW(ix),charSpacing:zf==="h"?0:LW,fill:SCH,originX:"left",originY:"center",selectable:!1,evented:!1}),zsm=(zz,zf2)=>{const zo={fontSize:zz,fontFamily:zf2,fontWeight:"400"},zp=new Pe.fabric.Text("M M",zo).width-new Pe.fabric.Text("MM",zo).width;return zp>0&&zp<zz?zp:zz*.28},zsp=zsm(g2,FAM(ix)),zspH=zsm(zHS,zHF),zGp=zi=>zFl[zi]==="h"&&zFl[zi+1]==="h"?zspH:zsp;let zk=1,zTs=zWs.map((zw,zi)=>zmk(zw,zFl[zi],1)),zGs=zWs.slice(0,-1).reduce((za,zw,zi)=>za+zGp(zi),0),zB=zTs.reduce((za,zt)=>za+zt.width,0)+zGs;if(zB>MESS){zk=MESS/zB;zTs=zWs.map((zw,zi)=>zmk(zw,zFl[zi],zk));zB=zTs.reduce((za,zt)=>za+zt.width,0)+zGs*zk}let zx=LI?r*K.rand:r/2-zB/2;zTs.forEach((zt,zi)=>{zt.set({left:zx,top:y});add(zt);zx+=zt.width+zGp(zi)*zk});zFl.includes("g")&&(y+=(zGS*zk-g2)*K.zeile)}else txt(z,{left:LI?r*K.rand:r/2,top:y,originX:LI?"left":"center",originY:"center",\nfontSize:g2,fontFamily:FAM(ix),fontWeight:GEW(ix),fill:SCH,\ncharSpacing:LW,maxB:MESS});\ny+=g2*K.zeile});',
 'Textkachel: Zeilen mit markierten Woertern Wort fuer Wort', 1))

P.append((
 'title:"Geladene Datei",children:"karten372"',
 'title:"Geladene Datei",children:"karten373"',
 'Versionsschild auf karten373', 1))


# 374 — Julia-Stil (juliaknauber_coaching): enger Satz, **...** fett-kursiv,
# ein Block ohne automatische Teilung (Handschrift nur bei *...*), Zuschnitt
# nach Gesicht mit Text auf der freien Seite, Textkachel versteht Umbrueche und **.

P.append((
 'fotoLaufweite:-20',
 'fotoLaufweite:-45',
 'Laufweite Foto -45', 1))

P.append((
 'fotoZeile:0.98',
 'fotoZeile:0.88',
 'Zeilenabstand Foto .88', 1))

P.append((
 'spalteBreit:.93',
 'spalteBreit:.84',
 'Textspalte .84', 1))

P.append((
 'geteilt:1,',
 'geteilt:0,zuschnittTextfrei:1,zuschnittZoom:1.12,textSeiteGrenze:.55,gesichtOben:.3,gesichtUnten:.64,textUntenMitte:.7,textObenMitte:.27,fettKursiv:1,',
 'Regler Zuschnitt/Textseite/fettKursiv, geteilte Kachel aus', 1))

P.append((
 'fontStyle:tt.kursiv||xt.kursiv&&!tt.highlight?"italic":"normal"',
 'fontStyle:tt.kursiv||xt.kursiv&&!tt.highlight||xt.fett&&BS_KACHEL.fettKursiv===1?"italic":"normal"',
 '**...** fett-kursiv (zeichnen)', 1))

P.append((
 'fontStyle:Tt.kursiv?"italic":"normal"',
 'fontStyle:Tt.kursiv||Tt.fett&&BS_KACHEL.fettKursiv===1?"italic":"normal"',
 '**...** fett-kursiv (messen)', 2))

P.append((
 'if(t.background)try{await u(t.background)}catch{}const $e=!!t.background;',
 'if(t.background&&BS_KACHEL.zuschnittTextfrei===1&&!(t._autoImage&&t._autoImage.faceZones&&t._autoImage.faceZones.length))try{const zA=await Promise.race([AK([t.background]),new Promise(zr=>setTimeout(()=>zr(null),6e3))]);zA&&zA[0]&&(t._zGes=zA[0].faceZones||[],t._zSpot=zA[0].textSpot||null)}catch(zz){}if(t.background)try{await u(t.background)}catch{}const $e=!!t.background;',
 'Gesichtslage vor dem Zuschnitt holen', 1))

P.append((
 '$e=t._autoImage&&t._autoImage.faceZones||[];let qe=.5,ht=.34;',
 '$e=t._zGes&&t._zGes.length?t._zGes:t._autoImage&&t._autoImage.faceZones||[];let qe=.5,ht=.34;',
 'Zuschnitt nutzt die geholte Gesichtslage', 1))

P.append((
 'lt=Ye[Qe===0?zDS:et[Qe%et.length]],[wt,tt,Qt]=lt,',
 'lt=BS_KACHEL.zuschnittTextfrei===1&&t.textBands===!0&&!t.imageLocked?(()=>{const zHat=$e.length>0;if(!zHat){const zSp=t._zSpot;t._textSeite=zSp&&typeof zSp.y=="number"&&zSp.y<.45?"oben":"unten";t._zGy=null;return[.5,.5,1]}const zFy=ht,zZ=zFy<.3?1:Number(BS_KACHEL.zuschnittZoom)||1.12,zU=zFy<=(Number(BS_KACHEL.textSeiteGrenze)||.55);t._textSeite=zU?"unten":"oben";t._zGy=zFy;const zTy=zU?(Number(BS_KACHEL.gesichtOben)||.3):(Number(BS_KACHEL.gesichtUnten)||.64),zAr=me.height*Oe*zZ;return[qe,zFy-(zTy*n-n/2)/zAr,zZ]})():Ye[Qe===0?zDS:et[Qe%et.length]],[wt,tt,Qt]=lt,',
 'Zuschnitt: Gesicht auf die textfreie Seite', 1))

P.append((
 'me.set({originX:"center",originY:"center",left:r/2+pr,top:n/2+jr,scaleX:jt,scaleY:jt,selectable:!1});',
 'me.set({originX:"center",originY:"center",left:r/2+pr,top:n/2+jr,scaleX:jt,scaleY:jt,selectable:!1});typeof t._zGy=="number"&&(t._gesichtY=(n/2+jr+(t._zGy-.5)*ar)/n);',
 'tatsaechliche Gesichtshoehe nach dem Zuschnitt merken', 1))

P.append((
 'BS_KACHEL.textImmerMitte===1&&(De=n*(Number(BS_KACHEL.textMitte)||.5)-ae/2+Et/2);',
 'BS_KACHEL.textImmerMitte===1&&(De=n*(Number(BS_KACHEL.textMitte)||.5)-ae/2+Et/2);BS_KACHEL.zuschnittTextfrei===1&&$e&&t._textSeite&&(()=>{const zS=typeof t._gesichtY=="number"?(t._gesichtY<.5?"unten":"oben"):t._textSeite;t._textSeiteEnd=zS;De=n*(zS==="oben"?(Number(BS_KACHEL.textObenMitte)||.27):(Number(BS_KACHEL.textUntenMitte)||.7))-ae/2+Et/2})();',
 'Text auf die textfreie Seite', 1))

P.append((
 'if(tt.nurErsteZeilePlatte){const zl=String(pr).split(/\\r?\\n/);',
 'if(tt.nurErsteZeilePlatte&&BS_KACHEL.einBlock===1){er=pr;pr=""}else if(tt.nurErsteZeilePlatte){const zl=String(pr).split(/\\r?\\n/);',
 'einBlock: keine automatische Teilung', 1))

P.append((
 'folgeGewicht:"700"',
 'folgeGewicht:"400"',
 'Folgefolien normal statt fett', 1))

P.append((
 'fettKursiv:1,',
 'fettKursiv:1,einBlock:1,',
 'Regler einBlock', 1))

P.append((
 'ae=dr.reduce((zs,zz,ii)=>zs+(zz.length?(tt.nurErsteZeilePlatte&&ii>=Lt?Et2:Et)*zF:(tt.engZeilen?qe*.92:Et)*zF),0)',
 'zHZ=zz=>zz&&zz.length&&zz.every(zx=>zx.hand)?(Number(BS_KACHEL.handZeile)||1.3):1,ae=dr.reduce((zs,zz,ii)=>zs+(zz.length?(tt.nurErsteZeilePlatte&&ii>=Lt?Et2:Et)*zF*Math.max(zHZ(zz),zHZ(dr[ii+1])):(tt.engZeilen?qe*.92:Et)*zF),0)',
 'Handschrift-Zeilen: mehr Abstand (messen)', 1))

P.append((
 'De+=(Ve?Et:Et2)*zF',
 'De+=(Ve?Et:Et2)*zF*Math.max(zHZ(Je),zHZ(dr[rt+1]))',
 'Handschrift-Zeilen: mehr Abstand (setzen)', 1))

P.append((
 'const B0=ROH.replace(BS_KACHEL.strichGross===1?/[*_]/g:/\\*/g,"").split(/\\n\\s*\\n/)',
 'const B0=ROH.replace(BS_KACHEL.strichGross===1?/[*_]/g:/\\*/g,"").split(BS_KACHEL.einBlock===1?/\\n/:/\\n\\s*\\n/)',
 'Textkachel: jeder Zeilenumbruch zaehlt', 1))

P.append((
 'for(const zc of String(ROH||"")){if(zc==="*"&&BS_KACHEL.sternHand===1){zS=!zS;continue}if(zc==="*"){continue}if(zc==="_"&&BS_KACHEL.strichGross===1){zU=!zU;continue}if(/\\s/.test(zc)){zpu();continue}zcur+=zc;zS?zm="h":zU&&!zm&&(zm="g")}',
 'let zBo=!1;const zRR=String(ROH||"");for(let zi=0;zi<zRR.length;zi++){const zc=zRR[zi];if(zc==="*"&&zRR[zi+1]==="*"){zBo=!zBo;zi++;continue}if(zc==="*"&&BS_KACHEL.sternHand===1){zS=!zS;continue}if(zc==="*"){continue}if(zc==="_"&&BS_KACHEL.strichGross===1){zU=!zU;continue}if(/\\s/.test(zc)){zpu();continue}zcur+=zc;if(zS)zm="h";else if(zU&&!zm)zm="g";else if(zBo&&!zm)zm="f"}',
 'Textkachel: **...** erkennen', 1))

P.append((
 'zmk=(zw,zf,zq)=>new Pe.fabric.Text(zw,{fontSize:(zf==="h"?zHS:zf==="g"?zGS:g2)*zq,fontFamily:zf==="h"?zHF:zf==="g"?zGF:FAM(ix),fontWeight:zf?"400":GEW(ix),charSpacing:zf==="h"?0:LW,',
 'zmk=(zw,zf,zq)=>new Pe.fabric.Text(zw,{fontSize:(zf==="h"?zHS:zf==="g"?zGS:g2)*zq,fontFamily:zf==="h"?zHF:zf==="g"?zGF:zf==="f"?(K.fettFamilie||"Playfair Display"):FAM(ix),fontWeight:zf==="f"?(K.betontGewicht||"700"):zf?"400":GEW(ix),fontStyle:zf==="f"&&K.fettKursiv===1?"italic":"normal",charSpacing:zf==="h"?0:LW,',
 'Textkachel: **...** Playfair fett-kursiv', 1))

P.append((
 '(BS_KACHEL.textHoehe||.74)',
 '(BS_KACHEL.zuschnittTextfrei===1&&$e&&t.textBands===!0?(Number(BS_KACHEL.textHoeheTextfrei)||.4):(BS_KACHEL.textHoehe||.74))',
 'Texthoehe auf Fotokacheln begrenzen', 1))

P.append((
 'fettKursiv:1,einBlock:1,',
 'fettKursiv:1,einBlock:1,textHoeheTextfrei:.4,handZeile:1.3,',
 'Regler textHoeheTextfrei/handZeile', 1))

P.append((
 'title:"Geladene Datei",children:"karten373"',
 'title:"Geladene Datei",children:"karten374"',
 'Versionsschild auf karten374', 1))


# 375 — Geteilt-Folie: ohne weisse Plaettchen, Schrift fett und weiss mit
# Schatten, Texthaelfte leicht abgedunkelt; versteht *...*, **...**, _..._ und Umbrueche.

P.append((
 'fettKursiv:1,einBlock:1,',
 'fettKursiv:1,einBlock:1,splitPlatten:0,splitGewicht:"700",splitFarbe:"#FFFFFF",splitDunkel:.22,',
 'Regler Geteilt-Folie', 1))

P.append((
 'Qe=(et,lt)=>{if(!et)return;const wt=i.typography&&i.typography.bodyFontFamily||t.bodyFontFamily||"HelveticaNeueBrand";let tt=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c(22);const Qt=r*.8,Wt=String(et).split(/(\\*[^*]+\\*)/).filter(Boolean),jt=[];Wt.forEach(Lt=>{const St=/^\\*[^*]+\\*$/.test(Lt);String(St?Lt.slice(1,-1):Lt).split(/\\s+/).filter(Boolean).forEach(Zt=>jt.push({w:Zt,kursiv:St}))});const _t=(()=>{const Lt={fontSize:tt,fontFamily:wt,fontWeight:"400"},St=new Pe.fabric.Text("M M",Lt).width-new Pe.fabric.Text("MM",Lt).width;return St>0&&St<tt?St:tt*.25})(),ar=Lt=>Lt.some(St=>St.kursiv)?Lt.reduce((St,Zt)=>St+new Pe.fabric.Text(Zt.w,{fontSize:tt,fontFamily:wt,fontStyle:Zt.kursiv?"italic":"normal",fontWeight:"400"}).width,0)+_t*Math.max(0,Lt.length-1):new Pe.fabric.Text(Lt.map(St=>St.w).join(" "),{fontSize:tt,fontFamily:wt,fontWeight:"400"}).width,kt=[];let br=[];jt.forEach(Lt=>{const St=[...br,Lt];ar(St)<=Qt-c(40)||br.length===0?br=St:(kt.push(br),br=[Lt])}),br.length&&kt.push(br);const sr=tt*1.42,Ht=kt.length*sr,$t=n*.34,er=n*.86;let jr=(lt==="oben"?$t:er)-Ht+sr/2;const dr=T1({schrift:wt,hatFoto:!0,dunkel:me,groesse:tt});kt.forEach(Lt=>{const St=ar(Lt),Zt=St+dr.polsterX*2;e.add(new Pe.fabric.Rect({left:r/2,top:jr,width:Zt,height:sr*.98,originX:"center",originY:"center",fill:dr.plattenFarbe,rx:dr.rundung,ry:dr.rundung,selectable:!1}));let Et=r/2-St/2;Lt.some(ur=>ur.kursiv)?Lt.forEach(ur=>{const ae=new Pe.fabric.Text(ur.w,{left:Et,top:jr,originX:"left",originY:"center",fontSize:tt,fontFamily:wt,fontStyle:ur.kursiv?"italic":"normal",fontWeight:"400",fill:Oe,selectable:!1});e.add(ae),Et+=ae.width+_t}):e.add(new Pe.fabric.Text(Lt.map(ur=>ur.w).join(" "),{left:Et,top:jr,originX:"left",originY:"center",fontSize:tt,fontFamily:wt,fontWeight:"400",fill:Oe,selectable:!1})),jr+=sr})}',
 'Qe=(et,lt)=>{if(!et)return;const wt=BS_KACHEL.splitSchrift||i.typography&&i.typography.bodyFontFamily||t.bodyFontFamily||"HelveticaNeueBrand",zPl=BS_KACHEL.splitPlatten===1,zGw=zPl?"400":(BS_KACHEL.splitGewicht||"700"),zFa=zPl?Oe:(BS_KACHEL.splitFarbe||"#FFFFFF"),zHF=BS_KACHEL.handFamilie||BS_KACHEL.zweiteFamilie||"Nothing You Could Do";let tt=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c(22);const Qt=r*.8,jt=[];String(et).split(/(\\*\\*[^*]+\\*\\*|\\*[^*]+\\*|_[^_\\n]+_)/).filter(Boolean).forEach(Lt=>{const zf=/^\\*\\*[^*]+\\*\\*$/.test(Lt),zk=!zf&&/^\\*[^*]+\\*$/.test(Lt),zu=/^_[^_\\n]+_$/.test(Lt),zx=zf?Lt.slice(2,-2):zk||zu?Lt.slice(1,-1):Lt;zx.split(/\\r?\\n/).forEach((zl,zli)=>{zli>0&&jt.push({br:!0});zl.split(/\\s+/).filter(Boolean).forEach(Zt=>jt.push({w:Zt,m:zf?"f":zk?(BS_KACHEL.sternHand===1?"h":"k"):zu?(BS_KACHEL.strichGross===1?"g":"h"):""}))})});const zo=Zt=>({fontSize:Zt.m==="h"?tt*(Number(BS_KACHEL.handAnteil)||1.15):Zt.m==="g"?tt*(Number(BS_KACHEL.grossAnteil)||1.1):tt,fontFamily:Zt.m==="h"?zHF:Zt.m==="g"?(BS_KACHEL.grossFamilie||"Playfair Display"):wt,fontWeight:Zt.m==="h"?"400":Zt.m==="f"?"700":zGw,fontStyle:Zt.m==="f"&&BS_KACHEL.fettKursiv===1||Zt.m==="k"?"italic":"normal"});const _t=(()=>{const Lt={fontSize:tt,fontFamily:wt,fontWeight:zGw},St=new Pe.fabric.Text("M M",Lt).width-new Pe.fabric.Text("MM",Lt).width;return St>0&&St<tt?St:tt*.25})(),zHs=(()=>{const Lt=zo({m:"h"}),St=new Pe.fabric.Text("M M",Lt).width-new Pe.fabric.Text("MM",Lt).width;return St>0&&St<Lt.fontSize?St:Lt.fontSize*.3})(),zGp=(Lt,zi)=>Lt[zi].m==="h"&&Lt[zi+1]&&Lt[zi+1].m==="h"?zHs:_t,ar=Lt=>Lt.reduce((St,Zt,zi)=>St+new Pe.fabric.Text(Zt.w,zo(Zt)).width+(zi<Lt.length-1?zGp(Lt,zi):0),0),kt=[];let br=[];jt.forEach(Lt=>{if(Lt.br){br.length&&kt.push(br);br=[];return}const St=[...br,Lt];ar(St)<=Qt-c(40)||br.length===0?br=St:(kt.push(br),br=[Lt])}),br.length&&kt.push(br);const sr=tt*(zPl?1.42:1.22),Ht=kt.length*sr,$t=n*.34,er=n*.86;let jr=(lt==="oben"?$t:er)-Ht+sr/2;const dr=T1({schrift:wt,hatFoto:!0,dunkel:me,groesse:tt}),zSh=zPl?void 0:new Pe.fabric.Shadow({color:"rgba(0,0,0,0.55)",blur:c(10),offsetX:0,offsetY:c(2)});!zPl&&(Number(BS_KACHEL.splitDunkel)||0)>0&&e.add(new Pe.fabric.Rect({left:0,top:lt==="oben"?0:ge,width:r,height:ge,fill:"rgba(0,0,0,"+Number(BS_KACHEL.splitDunkel)+")",selectable:!1,evented:!1}));kt.forEach(Lt=>{const St=ar(Lt),Zt=St+dr.polsterX*2;zPl&&e.add(new Pe.fabric.Rect({left:r/2,top:jr,width:Zt,height:sr*.98,originX:"center",originY:"center",fill:dr.plattenFarbe,rx:dr.rundung,ry:dr.rundung,selectable:!1}));let Et=r/2-St/2;Lt.forEach((ur,zi)=>{const ae=new Pe.fabric.Text(ur.w,{left:Et,top:jr,originX:"left",originY:"center",...zo(ur),fill:zFa,shadow:zSh,selectable:!1});e.add(ae),Et+=ae.width+(zi<Lt.length-1?zGp(Lt,zi):0)}),jr+=sr})}',
 'Geteilt-Folie: ohne Plaettchen, fett weiss, Zeichen', 1))

P.append((
 'title:"Geladene Datei",children:"karten374"',
 'title:"Geladene Datei",children:"karten375"',
 'Versionsschild auf karten375', 1))


# 376 — "Bilder teilweise zu dunkel, wenn dunkel mit Schwarz und nicht mehr
# Saettigung oder was auch immer": Toenung, Schwarzpunkt, Vignette, Schleier, Kanten,
# Saettigungsanhebung aus; nur noch ein reinschwarzer Verlauf; Helligkeitsziel 115.

P.append((
 'bildSchwarzpunkt:.07',
 'bildSchwarzpunkt:0',
 'Schwarzpunkt aus', 1))

P.append((
 'bildVignette:.6',
 'bildVignette:0',
 'Vignette aus', 1))

P.append((
 'bildSchleier:.06',
 'bildSchleier:0',
 'Schleier aus', 1))

P.append((
 'tonReihe:"14,13,12|26,20,16|12,16,20|22,14,20"',
 'tonReihe:"0,0,0"',
 'Toenung: reines Schwarz', 1))

P.append((
 'tonNeutral:"13,13,13"',
 'tonNeutral:"0,0,0"',
 'Toenung SW: reines Schwarz', 1))

P.append((
 'bildTon:"14,13,12"',
 'bildTon:"0,0,0"',
 'Bildton: reines Schwarz', 1))

P.append((
 'auflageReihe:"1|0.2|0.65|0.35"',
 'auflageReihe:"1"',
 'Abdunklung auf jeder Kachel gleich', 1))

P.append((
 'vignetteReihe:"1|0|0.55|0.25"',
 'vignetteReihe:"0"',
 'Vignettenreihe aus', 1))

P.append((
 'tiefeOben:.55',
 'tiefeOben:.3',
 'Verlauf oben .30', 1))

P.append((
 'tiefeMitte:.08',
 'tiefeMitte:.1',
 'Verlauf Mitte .10', 1))

P.append((
 'tiefeUnten:.85',
 'tiefeUnten:.45',
 'Verlauf unten .45', 1))

P.append((
 'kanteOben:.34',
 'kanteOben:0',
 'Kante oben aus', 1))

P.append((
 'kanteUnten:.40',
 'kanteUnten:0',
 'Kante unten aus', 1))

P.append((
 'hellZiel:105',
 'hellZiel:115',
 'Helligkeitsziel 115', 1))

P.append((
 'saettigungReihe:"-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1"',
 'saettigungReihe:"-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0"',
 'keine Saettigungsanhebung (jede vierte SW bleibt)', 1))

P.append((
 'e.add(Ut),Vt+=Ut.width+(Ve?ot:',
 'e.add(Ut),Vt+=Ut.width+(Ve&&!(xt.hand&&Je[Je.indexOf(xt)+1]&&Je[Je.indexOf(xt)+1].hand)?ot:',
 'Handschrift-Abstand Ueberschrift (setzen)', 1))

P.append((
 '.width,0)+ct*Math.max(0,Je.length-1)}',
 '.width,0)+Je.slice(0,-1).reduce((zs,zq,zi)=>zs+(zq.hand&&Je[zi+1].hand?(()=>{const zo={fontSize:zws({hand:1},rt),fontFamily:zwf({hand:1},Qe)},zp=new Pe.fabric.Text("M M",zo).width-new Pe.fabric.Text("MM",zo).width;return zp>0?zp:rt*.3})():ct),0)}',
 'Handschrift-Abstand Ueberschrift (messen)', 1))

P.append((
 'title:"Geladene Datei",children:"karten375"',
 'title:"Geladene Datei",children:"karten376"',
 'Versionsschild auf karten376', 1))


# 377 — "Wieso wird der Text nicht um mein Gesicht herum gebaut?": face-api
# faellt ohne WebGL auf wasm (Dateien fehlen) -> keine Gesichter. Jetzt WebGL,
# sonst CPU; laenger warten; etwas empfindlicher.

P.append((
 'Zh=await Rd(()=>import("./face-api.esm-CT-VR31B.js"),[],import.meta.url),await Zh.nets.tinyFaceDetector.loadFromUri(MV)',
 'Zh=await Rd(()=>import("./face-api.esm-CT-VR31B.js"),[],import.meta.url),await(async()=>{try{const zT=Zh.tf;let zok=!1;try{zok=await zT.setBackend("webgl")}catch(zz){}zok||await zT.setBackend("cpu");await zT.ready()}catch(zz){}})(),await Zh.nets.tinyFaceDetector.loadFromUri(MV)',
 'Gesichtserkennung: WebGL, sonst CPU', 1))

P.append((
 'new Promise(zr=>setTimeout(()=>zr(null),6e3))',
 'new Promise(zr=>setTimeout(()=>zr(null),Number(BS_KACHEL.gesichtWarten)||12e3))',
 'beim ersten Mal laenger auf die Erkennung warten', 1))

P.append((
 'fettKursiv:1,einBlock:1,',
 'fettKursiv:1,einBlock:1,gesichtWarten:12000,',
 'Regler gesichtWarten', 1))

P.append((
 'new Zh.TinyFaceDetectorOptions({inputSize:320,scoreThreshold:.5})',
 'new Zh.TinyFaceDetectorOptions({inputSize:416,scoreThreshold:.4})',
 'Gesichtserkennung etwas empfindlicher', 1))

P.append((
 'title:"Geladene Datei",children:"karten376"',
 'title:"Geladene Datei",children:"karten377"',
 'Versionsschild auf karten377', 1))


# 378 — "Zu grau, viel staerkeres Schwarz, Saettigung darf nicht steigen":
# Tonwertkurve nur auf der Helligkeit (Schwarzpunkt aus den dunkelsten 2 %, Kontrast
# um die Bildhelligkeit), lineares Angleichen, Farbabstand nie groesser; Verlauf kraeftiger.

P.append((
 'try{const zZiel=Number(BS_KACHEL.hellZiel)||0;if(zZiel>0&&Pe.fabric.Image.filters&&Pe.fabric.Image.filters.Gamma){',
 'try{const zZiel=Number(BS_KACHEL.hellZiel)||0;if(BS_KACHEL.schwarzKurve===1&&zZiel>0){const zel=me.getElement&&me.getElement();if(zel&&zel.width){const zc=document.createElement("canvas");zc.width=zel.width;zc.height=zel.height;const zx=zc.getContext("2d");zx.drawImage(zel,0,0);const zid=zx.getImageData(0,0,zc.width,zc.height),zd=zid.data,zKo=Number(BS_KACHEL.schwarzKontrast)||1,zH=new Array(256).fill(0);let zn=0;for(let zi=0;zi<zd.length;zi+=4*29){zH[Math.min(255,Math.round(.2126*zd[zi]+.7152*zd[zi+1]+.0722*zd[zi+2]))]++;zn++}let zP=0,zAcc=0;const zQ=zn*(Number(BS_KACHEL.schwarzAnteil)||.02);for(;zP<255&&zAcc+zH[zP]<=zQ;zP++)zAcc+=zH[zP];const zBp=Math.min(zP,Math.max(0,Math.min(.4,Number(BS_KACHEL.schwarzTiefe)||0))*255),zLv=zL=>Math.max(0,(zL-zBp)/(255-zBp))*255;let zs1=0;for(let zb=0;zb<256;zb++)zs1+=zH[zb]*zLv(zb);const zM1=zs1/Math.max(1,zn);const zCu=zL=>{let zv=zLv(zL);zv=zM1+(zv-zM1)*zKo;return zv<0?0:zv>255?255:zv};let zs=0;for(let zb=0;zb<256;zb++)zs+=zH[zb]*zCu(zb);const zm=zs/Math.max(1,zn),zG=Math.max(Number(BS_KACHEL.hellDunkelMin)||.5,Math.min(Number(BS_KACHEL.hellAngleichMax)||2,zZiel/Math.max(1,zm)));for(let zi=0;zi<zd.length;zi+=4){const zr=zd[zi],zg=zd[zi+1],zb=zd[zi+2],zL=.2126*zr+.7152*zg+.0722*zb;if(zL<=.5){zd[zi]=zd[zi+1]=zd[zi+2]=0;continue}const zL2=zCu(zL)*zG,zc=Math.min(1,zL2/zL)*(Number(BS_KACHEL.schwarzFarbe)||1),zk=(zv)=>{const zw=zL2+(zv-zL)*zc;return zw<0?0:zw>255?255:zw};zd[zi]=zk(zr);zd[zi+1]=zk(zg);zd[zi+2]=zk(zb)}zx.putImageData(zid,0,0);me.setElement(zc);const zc2=document.createElement("canvas");zc2.width=zc2.height=16;const zx2=zc2.getContext("2d");zx2.drawImage(zc,0,0,16,16);const zd2=zx2.getImageData(0,0,16,16).data;let zs2=0;const zN=[];for(let zy=0;zy<16;zy++){const zR=[];for(let zq=0;zq<16;zq++){const zi=(zy*16+zq)*4,zl=.2126*zd2[zi]+.7152*zd2[zi+1]+.0722*zd2[zi+2];zR.push(zl);zs2+=zl}zN.push(zR)}t._hellNetz=zN;t._hellMittel=Math.round(zs2/256)}}else if(zZiel>0&&Pe.fabric.Image.filters&&Pe.fabric.Image.filters.Gamma){',
 'Tonwertkurve auf der Helligkeit statt Gamma (Saettigung bleibt)', 1))

P.append((
 'fettKursiv:1,einBlock:1,',
 'fettKursiv:1,einBlock:1,schwarzKurve:1,schwarzTiefe:.1,schwarzAnteil:.02,schwarzKontrast:1.12,schwarzFarbe:.85,',
 'Regler schwarzKurve/schwarzTiefe/schwarzKontrast', 1))

P.append((
 'hellZiel:115',
 'hellZiel:108',
 'Helligkeitsziel 108', 1))

P.append((
 'tiefeOben:.3',
 'tiefeOben:.35',
 'Verlauf oben .35', 1))

P.append((
 'tiefeMitte:.1',
 'tiefeMitte:.12',
 'Verlauf Mitte .12', 1))

P.append((
 'tiefeUnten:.45',
 'tiefeUnten:.55',
 'Verlauf unten .55', 1))

P.append((
 'title:"Geladene Datei",children:"karten377"',
 'title:"Geladene Datei",children:"karten378"',
 'Versionsschild auf karten378', 1))


# 379 — Satzzeichen direkt hinter einer Markierung ("**bold**.") ohne Luecke.

P.append((
 ':String(nr).split(/\\r?\\n/).forEach(',
 ':String((()=>{let zv=nr;const zlw=rt[rt.length-1];if(zlw&&!zlw.br&&/^\\S/.test(zv)&&(zlw.kursiv||zlw.fett||zlw.hand||zlw.gross)){const zm=zv.match(/^\\S+/)[0];zlw.w+=zm;zv=zv.slice(zm.length)}return zv})()).split(/\\r?\\n/).forEach(',
 'Satzzeichen hinter Markierung ohne Luecke', 1))

P.append((
 'title:"Geladene Datei",children:"karten378"',
 'title:"Geladene Datei",children:"karten379"',
 'Versionsschild auf karten379', 1))


# 380 — "So wie bei dir im Bild sieht das nicht aus": Text ueber den Kopf ab
# Gesichtshoehe .4; helle Fotos bekommen mehr echtes Schwarz (Ziel 96, Schwarzpunkt
# bis .20 aus den dunkelsten 5 %, Kontrast 1.22).

P.append((
 'textSeiteGrenze:.55',
 'textSeiteGrenze:.4',
 'Text oben ab Gesichtshoehe .4', 1))

P.append((
 'hellZiel:108',
 'hellZiel:96',
 'Helligkeitsziel 96', 1))

P.append((
 'schwarzTiefe:.1',
 'schwarzTiefe:.2',
 'Schwarzpunkt bis .20', 1))

P.append((
 'schwarzAnteil:.02',
 'schwarzAnteil:.05',
 'dunkelste 5 % werden Schwarz', 1))

P.append((
 'schwarzKontrast:1.12',
 'schwarzKontrast:1.22',
 'Kontrast 1.22', 1))

P.append((
 'title:"Geladene Datei",children:"karten379"',
 'title:"Geladene Datei",children:"karten380"',
 'Versionsschild auf karten380', 1))


# 381 — "Es ist zu grau": Tonwerte spreizen (Schwarz-/Weisspunkt, Mitteltoene per
# Gamma auf hellZiel), schwarze Schichten zurueck (Verlauf .15/0/.30, Balken max 1.25).

P.append((
 'const zid=zx.getImageData(0,0,zc.width,zc.height),zd=zid.data,zKo=Number(BS_KACHEL.schwarzKontrast)||1,zH=new Array(256).fill(0);let zn=0;for(let zi=0;zi<zd.length;zi+=4*29){zH[Math.min(255,Math.round(.2126*zd[zi]+.7152*zd[zi+1]+.0722*zd[zi+2]))]++;zn++}let zP=0,zAcc=0;const zQ=zn*(Number(BS_KACHEL.schwarzAnteil)||.02);for(;zP<255&&zAcc+zH[zP]<=zQ;zP++)zAcc+=zH[zP];const zBp=Math.min(zP,Math.max(0,Math.min(.4,Number(BS_KACHEL.schwarzTiefe)||0))*255),zLv=zL=>Math.max(0,(zL-zBp)/(255-zBp))*255;let zs1=0;for(let zb=0;zb<256;zb++)zs1+=zH[zb]*zLv(zb);const zM1=zs1/Math.max(1,zn);const zCu=zL=>{let zv=zLv(zL);zv=zM1+(zv-zM1)*zKo;return zv<0?0:zv>255?255:zv};let zs=0;for(let zb=0;zb<256;zb++)zs+=zH[zb]*zCu(zb);const zm=zs/Math.max(1,zn),zG=Math.max(Number(BS_KACHEL.hellDunkelMin)||.5,Math.min(Number(BS_KACHEL.hellAngleichMax)||2,zZiel/Math.max(1,zm)));for(let zi=0;zi<zd.length;zi+=4){const zr=zd[zi],zg=zd[zi+1],zb=zd[zi+2],zL=.2126*zr+.7152*zg+.0722*zb;if(zL<=.5){zd[zi]=zd[zi+1]=zd[zi+2]=0;continue}const zL2=zCu(zL)*zG,zc=Math.min(1,zL2/zL)*(Number(BS_KACHEL.schwarzFarbe)||1),zk=(zv)=>{const zw=zL2+(zv-zL)*zc;return zw<0?0:zw>255?255:zw};zd[zi]=zk(zr);zd[zi+1]=zk(zg);zd[zi+2]=zk(zb)}',
 'const zid=zx.getImageData(0,0,zc.width,zc.height),zd=zid.data,zH=new Array(256).fill(0);let zn=0;for(let zi=0;zi<zd.length;zi+=4*29){zH[Math.min(255,Math.round(.2126*zd[zi]+.7152*zd[zi+1]+.0722*zd[zi+2]))]++;zn++}const zPz=zq=>{let zA=0,zp=0;const zQ=zn*zq;for(;zp<255&&zA+zH[zp]<=zQ;zp++)zA+=zH[zp];return zp};const zBp=Math.min(zPz(Number(BS_KACHEL.schwarzAnteil)||.04),Math.max(0,Math.min(.4,Number(BS_KACHEL.schwarzTiefe)||.2))*255),zWp=Math.max(zBp+40,zPz(1-(Number(BS_KACHEL.weissAnteil)||.01))),zLv=zL=>{const zv=(zL-zBp)/(zWp-zBp);return zv<0?0:zv>1?1:zv};const zMit=zg=>{let zs=0;for(let zb=0;zb<256;zb++)zs+=zH[zb]*Math.pow(zLv(zb),zg)*255;return zs/Math.max(1,zn)};let zlo=Number(BS_KACHEL.gammaMin)||.7,zhi=Number(BS_KACHEL.gammaMax)||2.4;for(let zk=0;zk<24;zk++){const zmid=(zlo+zhi)/2;zMit(zmid)>zZiel?zlo=zmid:zhi=zmid}const zGm=(zlo+zhi)/2;for(let zi=0;zi<zd.length;zi+=4){const zr=zd[zi],zg=zd[zi+1],zb=zd[zi+2],zL=.2126*zr+.7152*zg+.0722*zb;if(zL<=.5){zd[zi]=zd[zi+1]=zd[zi+2]=0;continue}const zL2=255*Math.pow(zLv(zL),zGm),zc3=Math.min(1,zL2/zL)*(Number(BS_KACHEL.schwarzFarbe)||1),zk=(zv)=>{const zw=zL2+(zv-zL)*zc3;return zw<0?0:zw>255?255:zw};zd[zi]=zk(zr);zd[zi+1]=zk(zg);zd[zi+2]=zk(zb)}',
 'Tonwerte spreizen: Schwarz- und Weisspunkt, Mitteltoene per Gamma', 1))

P.append((
 'schwarzAnteil:.05,',
 'schwarzAnteil:.04,weissAnteil:.01,gammaMin:.7,gammaMax:2.4,',
 'Regler Weisspunkt/Gamma', 1))

P.append((
 'tiefeOben:.35',
 'tiefeOben:.15',
 'Verlauf oben .15', 1))

P.append((
 'tiefeMitte:.12',
 'tiefeMitte:0',
 'Verlauf Mitte 0', 1))

P.append((
 'tiefeUnten:.55',
 'tiefeUnten:.3',
 'Verlauf unten .30', 1))

P.append((
 'textGrundMax:1.8',
 'textGrundMax:1.25',
 'Balken hinter der Schrift hoechstens 1.25-fach', 1))

P.append((
 'title:"Geladene Datei",children:"karten380"',
 'title:"Geladene Datei",children:"karten381"',
 'Versionsschild auf karten381', 1))


# 382 — "Katastrophe, die Bilder sollten aussehen wie das" (Exporte vom 16.09. =
# karten276): Bildbearbeitung exakt auf 276 zurueck, Kurve/Ausgleich aus; Gesichtslage
# vor dem ERSTEN Laden des Fotos (sonst Zuschnitt ohne Gesicht + Doppelschatten).

P.append((
 'bildSchleier:0,',
 'bildSchleier:.06,',
 'Schleier wie 276', 1))

P.append((
 'bildTon:"0,0,0"',
 'bildTon:"14,13,12"',
 'Bildton wie 276', 1))

P.append((
 'tonReihe:"0,0,0"',
 'tonReihe:"14,13,12|26,20,16|12,16,20|22,14,20"',
 'Toenung wie 276', 1))

P.append((
 'tonNeutral:"0,0,0"',
 'tonNeutral:"13,13,13"',
 'Toenung SW wie 276', 1))

P.append((
 'bildSchwarzpunkt:0,',
 'bildSchwarzpunkt:.07,',
 'Schwarzpunkt wie 276', 1))

P.append((
 'bildVignette:0,',
 'bildVignette:.6,',
 'Vignette wie 276', 1))

P.append((
 'textGrundMax:1.25',
 'textGrundMax:1.8',
 'Balken wie 276', 1))

P.append((
 'auflageReihe:"1"',
 'auflageReihe:"1|0.2|0.65|0.35"',
 'Auflage wie 276', 1))

P.append((
 'vignetteReihe:"0"',
 'vignetteReihe:"1|0|0.55|0.25"',
 'Vignettenreihe wie 276', 1))

P.append((
 'tiefeOben:.15,tiefeKnickOben:.16,tiefeMitte:0,tiefeKnick:.60,tiefeKnickUnten:.999,tiefeUnten:.3,',
 'tiefeOben:.55,tiefeKnickOben:.16,tiefeMitte:.08,tiefeKnick:.60,tiefeKnickUnten:.999,tiefeUnten:.85,',
 'Tiefenverlauf wie 276', 1))

P.append((
 'saettigungReihe:"-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0|-1|0|0|0"',
 'saettigungReihe:"-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1|-1|0.1|0.1|0.1"',
 'Saettigung wie 276 (+0.1), jede vierte SW bleibt', 1))

P.append((
 'schwarzKurve:1,',
 'schwarzKurve:0,',
 'Tonwertkurve aus', 1))

P.append((
 'hellZiel:96',
 'hellZiel:0',
 'Helligkeitsausgleich aus (gab es am 16.09. nicht)', 1))

P.append((
 'textSeiteGrenze:.4',
 'textSeiteGrenze:.55',
 'Text oben erst ab Gesichtshoehe .55', 1))

P.append((
 'if($&&!E)try{await u(t.background)}catch{}',
 'if($&&!E&&t.textBands===!0&&BS_KACHEL.zuschnittTextfrei===1&&!(t._autoImage&&t._autoImage.faceZones&&t._autoImage.faceZones.length))try{const zA=await Promise.race([AK([t.background]),new Promise(zr=>setTimeout(()=>zr(null),Number(BS_KACHEL.gesichtWarten)||12e3))]);zA&&zA[0]&&(t._zGes=zA[0].faceZones||[],t._zSpot=zA[0].textSpot||null)}catch(zz){}if($&&!E)try{await u(t.background)}catch{}',
 'Gesichtslage vor dem ersten Laden des Fotos', 1))

P.append((
 'title:"Geladene Datei",children:"karten381"',
 'title:"Geladene Datei",children:"karten382"',
 'Versionsschild auf karten382', 1))


# 383 — "Die dunkleren Fotos grundsaetzlich aufhellen auf die Tageslicht-Fotos":
# nur aufhellen, Ziel 118, linear mit weicher Schulter, Farbabstand gleich.

P.append((
 'try{const zZiel=Number(BS_KACHEL.hellZiel)||0;if(BS_KACHEL.schwarzKurve===1&&zZiel>0){',
 'try{const zZiel=Number(BS_KACHEL.hellZiel)||0;if(BS_KACHEL.aufhellModus===1&&zZiel>0){const zel=me.getElement&&me.getElement();if(zel&&zel.width){const zc=document.createElement("canvas");zc.width=zel.width;zc.height=zel.height;const zx=zc.getContext("2d");zx.drawImage(zel,0,0);const zid=zx.getImageData(0,0,zc.width,zc.height),zd=zid.data;let zs=0,zn=0;for(let zi=0;zi<zd.length;zi+=4*29){zs+=.2126*zd[zi]+.7152*zd[zi+1]+.0722*zd[zi+2];zn++}const zm=zs/Math.max(1,zn),zG=Math.min(Number(BS_KACHEL.hellGammaMax)||2.2,zZiel/Math.max(1,zm));if(zG>1.02){const zT=Number(BS_KACHEL.aufhellSchulter)||.8,zSc=zL=>{const zv=zL*zG/255;return 255*(zv<=zT?zv:zT+(1-zT)*(1-Math.exp(-(zv-zT)/(1-zT))))};for(let zi=0;zi<zd.length;zi+=4){const zr=zd[zi],zg=zd[zi+1],zb=zd[zi+2],zL=.2126*zr+.7152*zg+.0722*zb;if(zL<=.5)continue;const zL2=zSc(zL),zk=(zv)=>{const zw=zL2+(zv-zL);return zw<0?0:zw>255?255:zw};zd[zi]=zk(zr);zd[zi+1]=zk(zg);zd[zi+2]=zk(zb)}zx.putImageData(zid,0,0);me.setElement(zc)}const zc2=document.createElement("canvas");zc2.width=zc2.height=16;const zx2=zc2.getContext("2d");zx2.drawImage(me.getElement(),0,0,16,16);const zd2=zx2.getImageData(0,0,16,16).data;let zs2=0;const zN=[];for(let zy=0;zy<16;zy++){const zR=[];for(let zq=0;zq<16;zq++){const zi=(zy*16+zq)*4,zl=.2126*zd2[zi]+.7152*zd2[zi+1]+.0722*zd2[zi+2];zR.push(zl);zs2+=zl}zN.push(zR)}t._hellNetz=zN;t._hellMittel=Math.round(zs2/256)}}else if(BS_KACHEL.schwarzKurve===1&&zZiel>0){',
 'Aufhellen auf Tageslicht: linear mit Schulter, nur nach oben', 1))

P.append((
 'hellZiel:0',
 'hellZiel:118',
 'Ziel: Tageslicht-Niveau 118', 1))

P.append((
 'hellGammaMax:1.7',
 'hellGammaMax:2.2',
 'sehr dunkle Fotos bis 2.2-fach', 1))

P.append((
 'schwarzKurve:0,',
 'schwarzKurve:0,aufhellModus:1,aufhellSchulter:.8,',
 'Regler aufhellModus/aufhellSchulter', 1))

P.append((
 'title:"Geladene Datei",children:"karten382"',
 'title:"Geladene Datei",children:"karten383"',
 'Versionsschild auf karten383', 1))


# 384 — "Unlogisch wo der Text landet und wieso kein handschriftlicher Teil":
# echter Gesichtsrahmen, Text ins freie Band ueber/unter dem Gesicht, ohne Zeichen
# automatischer Handschrift-Nachsatz, Zufalls-Teilung aus.

P.append((
 'const u=a.box||a._box||a,d=.15,',
 'const u=a.box||a._box||a;{const zx0=u.x/l,zy0=u.y/o,zx1=(u.x+u.width)/l,zy1=(u.y+u.height)/o;r.box=r.box?{x0:Math.min(r.box.x0,zx0),y0:Math.min(r.box.y0,zy0),x1:Math.max(r.box.x1,zx1),y1:Math.max(r.box.y1,zy1)}:{x0:zx0,y0:zy0,x1:zx1,y1:zy1}}const d=.15,',
 'face-api: Gesichtsrahmen merken', 1))

P.append((
 'faceZones:Array.from(j),hasFace:j.size>0,',
 'faceZones:Array.from(j),faceBox:j.box||null,hasFace:j.size>0,',
 'Gesichtsrahmen ins Analyse-Ergebnis', 1))

P.append((
 'zA&&zA[0]&&(t._zGes=zA[0].faceZones||[],t._zSpot=zA[0].textSpot||null)',
 'zA&&zA[0]&&(t._zGes=zA[0].faceZones||[],t._zSpot=zA[0].textSpot||null,t._zBox=zA[0].faceBox||null)',
 'Gesichtsrahmen an die Folie', 2))

P.append((
 'const zFy=ht,',
 'const zBx=t._zBox,zFy=zBx?(zBx.y0+zBx.y1)/2:ht,',
 'Zuschnitt: Gesichtsmitte aus Rahmen', 1))

P.append((
 'return[qe,zFy-(zTy*n-n/2)/zAr,zZ]',
 'return[zBx?(zBx.x0+zBx.x1)/2:qe,zFy-(zTy*n-n/2)/zAr,zZ]',
 'Zuschnitt: waagrecht aus Rahmen', 1))

P.append((
 'textSeiteGrenze:.55',
 'textSeiteGrenze:.3',
 'Text ueber dem Kopf, ausser Gesicht ganz oben', 1))

P.append((
 'typeof t._zGy=="number"&&(t._gesichtY=(n/2+jr+(t._zGy-.5)*ar)/n);',
 'typeof t._zGy=="number"&&(t._gesichtY=(n/2+jr+(t._zGy-.5)*ar)/n);t._freiBand=null;try{if(BS_KACHEL.zuschnittTextfrei===1&&t.textBands===!0){const zY=zv=>(n/2+jr+(zv-.5)*ar)/n,zo=.08,zu=.9,zm=Number(BS_KACHEL.gesichtAbstand)||.035;let zT=null,zU=null;if(t._zBox){zT=zY(t._zBox.y0);zU=zY(t._zBox.y1)}else if($e.length){const zr=$e.map(zq=>Math.floor(zq/3));zT=zY(Math.min(...zr)/3);zU=zY((Math.max(...zr)+1)/3)}if(zT!=null){const zA=[zo,zT-zm],zB=[zU+zm,zu],zhA=zA[1]-zA[0],zhB=zB[1]-zB[0];t._freiBand=zhA>=(Number(BS_KACHEL.bandMinOben)||.2)||zhA>=zhB?zA:zB}else if(t._zSpot&&typeof t._zSpot.y=="number"){const zc=Math.max(zo+.18,Math.min(zu-.18,zY(t._zSpot.y)));t._freiBand=[zc-.18,zc+.18]}}}catch(zz){}',
 'freies Band neben dem Gesicht berechnen', 1))

P.append((
 '(Number(BS_KACHEL.textHoeheTextfrei)||.4)',
 '(t._freiBand?Math.max(.12,Math.min(Number(BS_KACHEL.textHoeheTextfrei)||.4,(t._freiBand[1]-t._freiBand[0])*.9)):(Number(BS_KACHEL.textHoeheTextfrei)||.4))',
 'Texthoehe = freies Band', 1))

P.append((
 'BS_KACHEL.zuschnittTextfrei===1&&$e&&t._textSeite&&(()=>{',
 'BS_KACHEL.zuschnittTextfrei===1&&$e&&t._freiBand?(De=n*(t._freiBand[0]+t._freiBand[1])/2-ae/2+Et/2):BS_KACHEL.zuschnittTextfrei===1&&$e&&t._textSeite&&(()=>{',
 'Text mittig ins freie Band', 1))

P.append((
 'if(tt.nurErsteZeilePlatte&&BS_KACHEL.einBlock===1){er=pr;pr=""}',
 'if(tt.nurErsteZeilePlatte&&BS_KACHEL.einBlock===1&&/[*_]/.test(String(pr))){er=pr;pr=""}',
 'ohne Zeichen: automatischer Handschrift-Nachsatz', 1))

P.append((
 'fettKursiv:1,einBlock:1,',
 'fettKursiv:1,einBlock:1,gesichtAbstand:.035,bandMinOben:.28,',
 'Regler gesichtAbstand/bandMinOben', 1))

P.append((
 'geteiltAnteil:25',
 'geteiltAnteil:0',
 'Zufalls-Teilung (erste Zeile ganz oben) aus', 1))

P.append((
 'title:"Geladene Datei",children:"karten383"',
 'title:"Geladene Datei",children:"karten384"',
 'Versionsschild auf karten384', 1))


# 385 — Sara-Noir-Look als Testversion unter /noir/ (BS_STIL "noir", BS_NOIR).
# Alle Eingriffe sind ohne die BS_NOIR-Regler wirkungslos.

P.append((
 'const BS_DUNKEL={',
 'const BS_NOIR={fotoSchrift:"Bodoni Moda",deckblattFamilie:"Bodoni Moda",folgeFamilie:"Bodoni Moda",kastenSchrift:"Bodoni Moda",lisaSchrift:"Bodoni Moda",folgeSchrift:"Bodoni Moda",ablaufTitel:"Bodoni Moda",deckblattGewicht:"400",gewicht:"400",folgeGewicht:"400",fotoLaufweite:30,fotoZeile:1.08,deckblattGroesse:72,fotoGroesse:58,textHoeheTextfrei:.3,spalteBreit:.8,sternHand:0,immerEinBlock:1,akzentAuto:1,akzentFarbe:"#C9A27E",zweiteFamilie:"MontserratBrand",kickerAn:1,fliessSchrift:"MontserratBrand",fliessGroesse:.024,nameMitte:1,nameText:"CARINA ANNA PRAV",nameSchrift:"Bodoni Moda",nameGewicht:"400",nameLaufweite:260,nameAnteil:.02,nameUnten:.95,nameFarbe:"rgba(255,255,255,0.9)",nameDeckkraft:1,obenLinks:1,dunkelText:1,dunkelTextAb:120,dunkelFarbe:"#2B1F18",akzentFarbeDunkel:"#9C7452",tonReihe:"30,20,14",tonNeutral:"30,20,14",bildTon:"30,20,14",saettigungReihe:"-0.1",bildTonung:"#8B6A4F",bildTonungKraft:.16,tiefeOben:.12,tiefeMitte:.04,tiefeUnten:.92,tiefeKnick:.55,auflageReihe:"1",vignetteReihe:"0.4",grundA:"#241A14",grundB:"#241A14",schriftA:"#F3ECE4",schriftB:"#F3ECE4"};const BS_DUNKEL={',
 'BS_NOIR-Regler', 1))

P.append((
 'if(typeof window<"u"&&window.BS_STIL==="dunkel")Object.assign(BS_KACHEL,BS_DUNKEL);',
 'if(typeof window<"u"&&(window.BS_STIL==="dunkel"||window.BS_STIL==="noir"))Object.assign(BS_KACHEL,BS_DUNKEL);if(typeof window<"u"&&window.BS_STIL==="noir")Object.assign(BS_KACHEL,BS_NOIR);',
 'Stil noir aktivieren', 1))

P.append((
 'let er="",pr=jt(t.text),jr="";',
 'let er="",pr=jt((()=>{t._kicker="";const zl=String(t.text||"").split(/\\r?\\n/);if(BS_KACHEL.kickerAn===1&&zl.length>1&&/^[A-ZÄÖÜ0-9 &\\-.:#]{2,24}$/.test(zl[0].trim())){t._kicker=zl[0].trim();return zl.slice(1).join("\\n")}return t.text})()),jr="";',
 'Kicker aus der ersten Zeile', 1))

P.append((
 'BS_KACHEL.einBlock===1&&/[*_]/.test(String(pr))',
 'BS_KACHEL.einBlock===1&&(BS_KACHEL.immerEinBlock===1||/[*_]/.test(String(pr)))',
 'noir: immer ein Block', 1))

P.append((
 '}),rt};let kt=',
 '}),BS_KACHEL.akzentAuto===1&&Je===er&&!rt.some(zq=>zq.kursiv||zq.fett||zq.hand||zq.gross)&&(()=>{for(let zi=rt.length-1;zi>=0;zi--)if(rt[zi].w){rt[zi].kursiv=!0;break}})(),rt};let kt=',
 'Akzent automatisch aufs letzte Wort', 1))

P.append((
 'const rr=xt.kursiv&&tt.highlight,Ut=',
 'const rr=xt.kursiv&&(BS_KACHEL.akzentFarbe||tt.highlight),Ut=',
 'Akzent Farbe (1)', 1))

P.append((
 'fill:rr?tt.highlight:',
 'fill:rr?(BS_KACHEL.akzentFarbe||tt.highlight):',
 'Akzent Farbe (2)', 1))

P.append((
 'xt.kursiv&&!tt.highlight',
 'xt.kursiv&&(BS_KACHEL.akzentFarbe||!tt.highlight)',
 'Akzent kursiv', 1))

P.append((
 'St=qe*.86,',
 'St=BS_KACHEL.fliessSchrift?r*(Number(BS_KACHEL.fliessGroesse)||.024):qe*.86,',
 'Fliesstext Groesse', 1))

P.append((
 'fontSize:St,fontFamily:Qe,',
 'fontSize:St,fontFamily:BS_KACHEL.fliessSchrift||Qe,',
 'Fliesstext Schrift', 2))

P.append((
 'dr.forEach((Je,rt)=>{if(zGT&&rt===0)',
 'dr.forEach((Je,rt)=>{rt===0&&(t._blockTop=De-Et*zF/2);if(zGT&&rt===0)',
 'Blockoberkante merken', 1))

P.append((
 'BS_KACHEL.nameZeigen===0||e.add(new Pe.fabric.Text(Ze,{left:_e+(Ye&&Ye.istKarte&&Ye.monogrammFarbe?c(42):0),top:n*(BS_KACHEL.nameUnten||.945),originX:"left",',
 't._kicker&&typeof t._blockTop=="number"&&e.add(new Pe.fabric.Text(String(t._kicker).toUpperCase(),{left:tt.ausrichtung==="links"?_e:r/2,top:t._blockTop-r*.03,originX:tt.ausrichtung==="links"?"left":"center",originY:"bottom",fontSize:Math.round(r*.019),fontFamily:BS_KACHEL.fliessSchrift||"MontserratBrand",fontWeight:"600",charSpacing:500,fill:"rgba(255,255,255,0.82)",selectable:!1})),BS_KACHEL.nameZeigen===0||e.add(new Pe.fabric.Text(BS_KACHEL.nameText||Ze,{left:BS_KACHEL.nameMitte===1?r/2:_e+(Ye&&Ye.istKarte&&Ye.monogrammFarbe?c(42):0),top:n*(BS_KACHEL.nameUnten||.945),originX:BS_KACHEL.nameMitte===1?"center":"left",',
 'Kicker zeichnen, Name mittig', 1))

P.append((
 'BS_KACHEL.zuschnittTextfrei===1&&$e&&t._freiBand?(De=',
 'BS_KACHEL.obenLinks===1&&$e&&t._freiBand&&(tt.ausrichtung=t._freiBand[0]<.2?"links":"mitte"),BS_KACHEL.zuschnittTextfrei===1&&$e&&t._freiBand?(De=',
 'oben links, unten mittig', 1))

P.append((
 'BS_KACHEL.obenLinks===1&&$e&&t._freiBand&&(tt.ausrichtung=',
 't._dunkelSchrift=!1,BS_KACHEL.dunkelText===1&&$e&&t._freiBand&&t._hellZeilen&&(()=>{const zZ=t._hellZeilen,za=Math.max(0,Math.floor(t._freiBand[0]*16)),zb=Math.min(15,Math.ceil(t._freiBand[1]*16)-1);let zs=0,zk=0;for(let zi=za;zi<=zb;zi++){zs+=zZ[zi];zk++}if(zs/Math.max(1,zk)>(Number(BS_KACHEL.dunkelTextAb)||145)){tt.schriftFarbe=BS_KACHEL.dunkelFarbe||"#2B1F18";t._dunkelSchrift=!0}})(),BS_KACHEL.obenLinks===1&&$e&&t._freiBand&&(tt.ausrichtung=',
 'dunkle Schrift auf heller Flaeche', 1))

P.append((
 'shadow:zKa&&Ve?void 0:((ge||!tt.platten)&&!lt?me():void 0)',
 'shadow:zKa&&Ve||t._dunkelSchrift?void 0:((ge||!tt.platten)&&!lt?me():void 0)',
 'kein Schatten bei dunkler Schrift (1)', 1))

P.append((
 'shadow:zKa&&Ve?void 0:((ge||!tt.platten&&(!Ve||tt.ohnePlatteErste))&&!lt?me():void 0)',
 'shadow:zKa&&Ve||t._dunkelSchrift?void 0:((ge||!tt.platten&&(!Ve||tt.ohnePlatteErste))&&!lt?me():void 0)',
 'kein Schatten bei dunkler Schrift (2)', 1))

P.append((
 'fill:rr?(BS_KACHEL.akzentFarbe||tt.highlight):',
 'fill:rr?(t._dunkelSchrift&&BS_KACHEL.akzentFarbeDunkel||BS_KACHEL.akzentFarbe||tt.highlight):',
 'Akzent dunkler auf hell', 1))

P.append((
 'fill:"rgba(255,255,255,0.82)",selectable:!1})),',
 'fill:t._dunkelSchrift?"rgba(43,31,24,0.75)":"rgba(255,255,255,0.82)",selectable:!1})),',
 'Kicker dunkel auf hell', 1))

P.append((
 'fontFamily:BS_KACHEL.fliessSchrift||Qe,fontWeight:"400",fontStyle:pt.kursiv?"italic":"normal",fill:"#FFFFFF",selectable:!1,shadow:new Pe.fabric.Shadow({color:"rgba(0,0,0,0.55)",blur:c(10),offsetX:0,offsetY:c(2)})',
 'fontFamily:BS_KACHEL.fliessSchrift||Qe,fontWeight:"400",fontStyle:pt.kursiv?"italic":"normal",fill:t._dunkelSchrift?"rgba(43,31,24,0.85)":"#FFFFFF",selectable:!1,shadow:t._dunkelSchrift?void 0:new Pe.fabric.Shadow({color:"rgba(0,0,0,0.55)",blur:c(10),offsetX:0,offsetY:c(2)})',
 'Fliesstext dunkel auf hell (1)', 1))

P.append((
 'fontFamily:BS_KACHEL.fliessSchrift||Qe,fontWeight:"400",fill:"#FFFFFF",selectable:!1,shadow:Ve',
 'fontFamily:BS_KACHEL.fliessSchrift||Qe,fontWeight:"400",fill:t._dunkelSchrift?"rgba(43,31,24,0.85)":"#FFFFFF",selectable:!1,shadow:t._dunkelSchrift?void 0:Ve',
 'Fliesstext dunkel auf hell (2)', 1))

P.append((
 'title:"Geladene Datei",children:"karten384"',
 'title:"Geladene Datei",children:"karten385"',
 'Versionsschild auf karten385', 1))


# 386 — /noir/: "nichts gut lesbar, zu klein, klassische Designregeln": Text am Rand
# verankert, Verlauf genau hinter dem Text nach gemessener Helligkeit, groesser,
# Gesicht oberes Drittel / Text unteres Drittel. Nur mit BS_NOIR-Reglern aktiv.

P.append((
 'const zY=zv=>(n/2+jr+(zv-.5)*ar)/n,zo=.08,zu=.9,',
 'const zY=zv=>(n/2+jr+(zv-.5)*ar)/n,zo=Number(BS_KACHEL.randOben)||.08,zu=Number(BS_KACHEL.randUnten)||.9,',
 'Raender als Regler', 1))

P.append((
 'BS_KACHEL.zuschnittTextfrei===1&&$e&&t._freiBand?(De=n*(t._freiBand[0]+t._freiBand[1])/2-ae/2+Et/2)',
 'BS_KACHEL.zuschnittTextfrei===1&&$e&&t._freiBand?(De=BS_KACHEL.randAnker===1?(t._freiBand[0]<.3?n*t._freiBand[0]+(t._kicker?r*.05:0)+Et/2:n*t._freiBand[1]-ae+Et/2):n*(t._freiBand[0]+t._freiBand[1])/2-ae/2+Et/2)',
 'Text am Rand verankern', 1))

P.append((
 'const Ze="carinaannaprav",',
 'BS_KACHEL.textScrim===1&&$e&&t._freiBand&&(()=>{try{const zT=(De-Et/2)/n,zB=(De-Et/2+ae)/n,zOb=t._freiBand[0]<.3,zZ=t._hellZeilen||[];let zs=0,zk=0;for(let zi=Math.max(0,Math.floor(zT*16));zi<=Math.min(15,Math.ceil(zB*16)-1);zi++){zs+=zZ[zi]||0;zk++}const zL=zk?zs/zk:128,zA=Math.max(Number(BS_KACHEL.scrimMin)||.25,Math.min(Number(BS_KACHEL.scrimMax)||.82,1-(Number(BS_KACHEL.scrimZiel)||70)/Math.max(1,zL))),zC=BS_KACHEL.bildTon||"0,0,0",zF=Number(BS_KACHEL.scrimAuslauf)||.14;if(zOb){const zE=Math.min(1,zB+zF);e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n*zE,selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:n*zE},colorStops:[{offset:0,color:`rgba(${zC},${zA})`},{offset:Math.min(.95,zB/zE),color:`rgba(${zC},${zA*.8})`},{offset:1,color:`rgba(${zC},0)`}]})}))}else{const zS=Math.max(0,zT-zF);e.add(new Pe.fabric.Rect({left:0,top:n*zS,width:r,height:n*(1-zS),selectable:!1,evented:!1,fill:new Pe.fabric.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:n*(1-zS)},colorStops:[{offset:0,color:`rgba(${zC},0)`},{offset:Math.min(.95,(zT-zS)/(1-zS)),color:`rgba(${zC},${zA*.8})`},{offset:1,color:`rgba(${zC},${zA})`}]})}))}}catch(zz){}})();const Ze="carinaannaprav",',
 'Verlauf hinter dem Text', 1))

P.append((
 'deckblattGroesse:72,fotoGroesse:58,textHoeheTextfrei:.3,',
 'deckblattGroesse:104,fotoGroesse:80,textHoeheTextfrei:.46,',
 'noir: Schrift groesser', 1))

P.append((
 'obenLinks:1,dunkelText:1,',
 'obenLinks:1,randAnker:1,textScrim:1,scrimZiel:70,scrimMin:.25,scrimMax:.82,scrimAuslauf:.14,randOben:.1,randUnten:.86,gesichtAbstand:.06,bandMinOben:.38,textSeiteGrenze:1,gesichtOben:.28,dunkelText:0,',
 'noir: Raender, Verlauf, immer weiss', 1))

P.append((
 'title:"Geladene Datei",children:"karten385"',
 'title:"Geladene Datei",children:"karten386"',
 'Versionsschild auf karten386', 1))


# 387 — /noir/: "Die Bilder aber wieder diese Farbwelt" (Exporte 16.09.): Fotolook aus BS_NOIR
# entfernt, es gilt die Bildbearbeitung aus BS_DUNKEL (karten276-Stand).

P.append((
 'tonReihe:"30,20,14",tonNeutral:"30,20,14",bildTon:"30,20,14",saettigungReihe:"-0.1",bildTonung:"#8B6A4F",bildTonungKraft:.16,tiefeOben:.12,tiefeMitte:.04,tiefeUnten:.92,tiefeKnick:.55,auflageReihe:"1",vignetteReihe:"0.4",',
 '',
 'noir: Fotolook wie 16.09. (BS_DUNKEL)', 1))

P.append((
 'title:"Geladene Datei",children:"karten386"',
 'title:"Geladene Datei",children:"karten387"',
 'Versionsschild auf karten387', 1))


# 388 — Versuch 3 unter /v3/ (BS_STIL "v3" = DUNKEL + NOIR + V3): Workbook-Schriften
# und -Farben, helle warme Fotos. Ohne BS_V3/BS_NOIR wirkungslos.

P.append((
 'const BS_NOIR={',
 'const BS_V3={fotoSchrift:"CormorantV3",deckblattFamilie:"CormorantV3",folgeFamilie:"CormorantV3",kastenSchrift:"CormorantV3",lisaSchrift:"CormorantV3",folgeSchrift:"CormorantV3",ablaufTitel:"CormorantV3",deckblattGewicht:"500",gewicht:"500",folgeGewicht:"500",fotoLaufweite:0,fotoZeile:1.0,deckblattGroesse:124,fotoGroesse:96,akzentFarbe:"#FFFFFF",akzentFarbeDunkel:"#231F20",akzentGewicht:"700",fliessSchrift:"HelveticaNeueBrand",fliessGroesse:.026,fliessVersal:1,nameText:"Carina",nameSchrift:"CaveatV3",nameGewicht:"500",nameLaufweite:0,nameAnteil:.05,nameUnten:.935,nameFarbe:"#FFFFFF",nameDeckkraft:.95,dunkelFarbe:"#231F20",grundA:"#FFFFFF",grundB:"#E0DCD9",schriftA:"#231F20",schriftB:"#231F20",schriftart:"CormorantV3",unterSchrift:"CormorantV3",tonReihe:"89,77,64",tonNeutral:"89,77,64",bildTon:"89,77,64",saettigungReihe:"-0.2",bildTonung:"#8A7663",bildTonungKraft:.1,tiefeOben:.08,tiefeMitte:0,tiefeUnten:.28,auflageReihe:"1",vignetteReihe:"0",bildVignette:0,bildSchleier:0,bildSchwarzpunkt:.03,textGrundMax:1,hellZiel:132,hellGammaMax:2.2,scrimZiel:82,scrimMin:.2,scrimMax:.7};const BS_NOIR={',
 'BS_V3-Regler', 1))

P.append((
 'if(typeof window<"u"&&(window.BS_STIL==="dunkel"||window.BS_STIL==="noir"))Object.assign(BS_KACHEL,BS_DUNKEL);if(typeof window<"u"&&window.BS_STIL==="noir")Object.assign(BS_KACHEL,BS_NOIR);',
 'if(typeof window<"u"&&(window.BS_STIL==="dunkel"||window.BS_STIL==="noir"||window.BS_STIL==="v3"))Object.assign(BS_KACHEL,BS_DUNKEL);if(typeof window<"u"&&(window.BS_STIL==="noir"||window.BS_STIL==="v3"))Object.assign(BS_KACHEL,BS_NOIR);if(typeof window<"u"&&window.BS_STIL==="v3")Object.assign(BS_KACHEL,BS_V3);',
 'Stil v3 aktivieren', 1))

P.append((
 'zwg=(xt,zg)=>xt&&xt.fett?',
 'zwg=(xt,zg)=>xt&&xt.kursiv&&BS_KACHEL.akzentGewicht?BS_KACHEL.akzentGewicht:xt&&xt.fett?',
 'Akzent fett-kursiv', 1))

P.append((
 '"400","500","600","700","italic 400"',
 '"400","500","600","700","italic 400","italic 700"',
 'Kursiv fett vorladen', 1))

P.append((
 'new Set([BS_KACHEL.lisaSchrift,BS_KACHEL.folgeSchrift]',
 'new Set([BS_KACHEL.lisaSchrift,BS_KACHEL.folgeSchrift,BS_KACHEL.nameSchrift,BS_KACHEL.fliessSchrift]',
 'Name-/Fliesstextschrift vorladen', 1))

P.append((
 'fontFamily:BS_KACHEL.fliessSchrift||Qe,fontWeight:"400",fontStyle:pt.kursiv?"italic":"normal"',
 'fontFamily:BS_KACHEL.fliessSchrift||Qe,fontWeight:pt.fett?"700":"400",fontStyle:pt.kursiv?"italic":"normal"',
 'Fliesstext: **fett**', 1))

P.append((
 'Zt=t.secondaryText?$t(_t(t.secondaryText),St,!1):[]',
 'Zt=t.secondaryText?$t(_t(BS_KACHEL.fliessVersal===1&&(i.slideIndex||0)===0?String(t.secondaryText).toUpperCase():t.secondaryText),St,!1):[]',
 'Subline auf dem Cover in Versalien', 1))

P.append((
 'title:"Geladene Datei",children:"karten387"',
 'title:"Geladene Datei",children:"karten388"',
 'Versionsschild auf karten388', 1))


# 389 — "Ueberall heller": Helligkeit aus /v3/ in BS_DUNKEL (/, /dunkel/, /noir/),
# Verlauf hinter dem Text auch in der normalen App. Alle Adressen auf karten389.

P.append((
 'tiefeOben:.55,',
 'tiefeOben:.08,',
 'Verlauf oben .08', 1))

P.append((
 'tiefeMitte:.08,',
 'tiefeMitte:0,',
 'Verlauf Mitte 0', 1))

P.append((
 'tiefeUnten:.85,',
 'tiefeUnten:.28,',
 'Verlauf unten .28', 1))

P.append((
 'bildVignette:.6,',
 'bildVignette:0,',
 'keine Vignette', 1))

P.append((
 'vignetteReihe:"1|0|0.55|0.25"',
 'vignetteReihe:"0"',
 'keine Vignettenreihe', 1))

P.append((
 'bildSchleier:.06,',
 'bildSchleier:0,',
 'kein Schleier', 1))

P.append((
 'bildSchwarzpunkt:.07,',
 'bildSchwarzpunkt:.03,',
 'Schwarzpunkt .03', 1))

P.append((
 'textGrundMax:1.8,',
 'textGrundMax:1,',
 'Balken hoechstens 1-fach', 1))

P.append((
 'hellZiel:118,',
 'hellZiel:132,textScrim:1,scrimZiel:82,scrimMin:.2,scrimMax:.7,scrimAuslauf:.14,',
 'Aufhellen auf 132, Verlauf hinter dem Text', 1))

P.append((
 'title:"Geladene Datei",children:"karten388"',
 'title:"Geladene Datei",children:"karten389"',
 'Versionsschild auf karten389', 1))


# 390 — "V3 ist zu hell, diese Nuance fuer alle" (Referenz-Story im Jeans-Overall):
# Verlauf oben/unten wie das Referenzbild, auf jeder Kachel gleich stark; v3 ohne
# eigene Bildwerte. Dazu "Schriften von v3 groesser". Alle Adressen auf karten390.

P.append((
 'tonReihe:"89,77,64",tonNeutral:"89,77,64",bildTon:"89,77,64",saettigungReihe:"-0.2",bildTonung:"#8A7663",bildTonungKraft:.1,',
 '',
 'v3: Farbwerte raus', 1))

P.append((
 'tiefeOben:.08,tiefeMitte:0,tiefeUnten:.28,auflageReihe:"1",vignetteReihe:"0",bildVignette:0,bildSchleier:0,bildSchwarzpunkt:.03,textGrundMax:1,hellZiel:132,hellGammaMax:2.2,scrimZiel:82,scrimMin:.2,scrimMax:.7',
 'scrimZiel:82',
 'v3: Helligkeitswerte raus', 1))

P.append((
 'bildSpreizung:.28,tiefeOben:.08,tiefeKnickOben:.16,tiefeMitte:0,tiefeKnick:.60,tiefeKnickUnten:.999,tiefeUnten:.28,',
 'bildSpreizung:.28,tiefeOben:.38,tiefeKnickOben:.16,tiefeMitte:.03,tiefeKnick:.60,tiefeKnickUnten:.999,tiefeUnten:.85,',
 'Verlauf wie ihr Referenzbild: oben .38, Mitte .03, unten .85', 1))

P.append((
 'bildHeben:0,hellZiel:132,',
 'bildHeben:0,hellZiel:118,',
 'Aufhellen auf 118', 1))

P.append((
 'auflageReihe:"1|0.2|0.65|0.35"',
 'auflageReihe:"1"',
 'Verlauf auf jeder Kachel gleich stark', 1))

P.append((
 'deckblattGroesse:124,fotoGroesse:96,',
 'deckblattGroesse:150,fotoGroesse:116,textHoeheTextfrei:.56,kickerGroesse:.024,',
 'v3: Titel groesser', 1))

P.append((
 'fliessGroesse:.026,',
 'fliessGroesse:.032,',
 'v3: Fliesstext groesser', 1))

P.append((
 'nameAnteil:.05,',
 'nameAnteil:.06,',
 'v3: Name groesser', 1))

P.append((
 'fontSize:Math.round(r*.019)',
 'fontSize:Math.round(r*(Number(BS_KACHEL.kickerGroesse)||.019))',
 'Kicker-Groesse per Regler', 1))

P.append((
 'title:"Geladene Datei",children:"karten389"',
 'title:"Geladene Datei",children:"karten390"',
 'Versionsschild auf karten390', 1))


# 391 — Textaufteilung wie ihre Testbilder: in v3 steht der Text unten (Band unter
# dem Gesicht zuerst; ohne Gesicht unten statt am ruhigsten Fleck). SW bleibt.

P.append((
 'nameText:"Carina",nameSchrift:"CaveatV3"',
 'bandUnten:1,bandMinUnten:.28,nameText:"Carina",nameSchrift:"CaveatV3"',
 'v3: Text bevorzugt unten', 1))

P.append((
 't._freiBand=zhA>=(Number(BS_KACHEL.bandMinOben)||.2)||zhA>=zhB?zA:zB}',
 't._freiBand=BS_KACHEL.bandUnten===1?(zhB>=(Number(BS_KACHEL.bandMinUnten)||.28)||zhB>=zhA?zB:zA):zhA>=(Number(BS_KACHEL.bandMinOben)||.2)||zhA>=zhB?zA:zB}',
 'Band: unten zuerst, wenn bandUnten', 1))

P.append((
 'else if(t._zSpot&&typeof t._zSpot.y=="number"){',
 'else if(BS_KACHEL.bandUnten===1){t._freiBand=[Math.max(.4,zu-.46),zu]}else if(t._zSpot&&typeof t._zSpot.y=="number"){',
 'ohne Gesicht: Text unten statt am ruhigsten Fleck', 1))

P.append((
 'title:"Geladene Datei",children:"karten390"',
 'title:"Geladene Datei",children:"karten391"',
 'Versionsschild auf karten391', 1))


# 392 — Textaufteilung wie ihre Testbilder: ein langer Text ohne Unterzeile wird in v3
# geteilt - erste Saetze (mind. 20 Zeichen) gross, der Rest als kleine Zeile in Versalien.

P.append((
 'pr=jt((()=>{t._kicker="";const zl=String(t.text||"").split(/\\r?\\n/);if(BS_KACHEL.kickerAn===1&&zl.length>1&&/^[A-ZÄÖÜ0-9 &\\-.:#]{2,24}$/.test(zl[0].trim())){t._kicker=zl[0].trim();return zl.slice(1).join("\\n")}return t.text})())',
 'pr=jt((()=>{t._autoUnter="";const zB=(()=>{t._kicker="";const zl=String(t.text||"").split(/\\r?\\n/);if(BS_KACHEL.kickerAn===1&&zl.length>1&&/^[A-ZÄÖÜ0-9 &\\-.:#]{2,24}$/.test(zl[0].trim())){t._kicker=zl[0].trim();return zl.slice(1).join("\\n")}return t.text})();try{if(BS_KACHEL.autoUnter===1&&!t.secondaryText&&!/\\n/.test(String(zB||""))){const zS=(String(zB||"").match(/[^.!?…]+[.!?…]+["“”„*_]*|[^.!?…]+$/g)||[]).map(zq=>zq.trim()).filter(Boolean);if(zS.length>1){let zh=zS[0],zk=1;const zMin=Number(BS_KACHEL.autoKopfMin)||20;while(zk<zS.length&&zh.length<zMin){zh+=" "+zS[zk];zk++}const zR=zS.slice(zk).join(" ");if(zR.length>=12&&zh.length<=(Number(BS_KACHEL.autoKopfMax)||80)){t._autoUnter=zR.replace(/(^|[^*])\\*(?!\\*)/g,"$1").replace(/(^|\\s)_|_(?=\\s|$|[.,!?…])/g,"$1");return zh}}}}catch(zz){}return zB})())',
 'v3: langer Text -> Kopfzeile + kleine Zeile darunter (autoUnter)', 1))

P.append((
 'Zt=t.secondaryText?$t(_t(BS_KACHEL.fliessVersal===1&&(i.slideIndex||0)===0?String(t.secondaryText).toUpperCase():t.secondaryText),St,!1):[]',
 'Zt=(t.secondaryText||t._autoUnter)?$t(_t(BS_KACHEL.fliessVersal===1&&(i.slideIndex||0)===0?String(t.secondaryText||t._autoUnter).toUpperCase():(t.secondaryText||t._autoUnter)),St,!1):[]',
 'kleine Zeile auch aus autoUnter', 1))

P.append((
 'bandUnten:1,bandMinUnten:.28,',
 'bandUnten:1,bandMinUnten:.28,autoUnter:1,',
 'v3: autoUnter an', 1))

P.append((
 'title:"Geladene Datei",children:"karten391"',
 'title:"Geladene Datei",children:"karten392"',
 'Versionsschild auf karten392', 1))


# 393 — Ihr Satz bleibt ganz gross. Die kleine Zeile darunter kommt nur aus Zeilen,
# die mit / anfangen (Kicker wie bisher: erste Zeile in GROSSBUCHSTABEN).

P.append((
 'try{if(BS_KACHEL.autoUnter===1&&!t.secondaryText&&!/\\n/.test(String(zB||""))){const zS=(String(zB||"").match(/[^.!?…]+[.!?…]+["“”„*_]*|[^.!?…]+$/g)||[]).map(zq=>zq.trim()).filter(Boolean);if(zS.length>1){let zh=zS[0],zk=1;const zMin=Number(BS_KACHEL.autoKopfMin)||20;while(zk<zS.length&&zh.length<zMin){zh+=" "+zS[zk];zk++}const zR=zS.slice(zk).join(" ");if(zR.length>=12&&zh.length<=(Number(BS_KACHEL.autoKopfMax)||80)){t._autoUnter=zR.replace(/(^|[^*])\\*(?!\\*)/g,"$1").replace(/(^|\\s)_|_(?=\\s|$|[.,!?…])/g,"$1");return zh}}}}',
 'try{if(BS_KACHEL.autoUnter===1&&!t.secondaryText){const zL=String(zB||"").split(/\\r?\\n/),zU=zL.filter(zq=>/^\\s*\\//.test(zq)).map(zq=>zq.replace(/^\\s*\\/\\s*/,"").trim()).filter(Boolean);if(zU.length){t._autoUnter=zU.join(" ");return zL.filter(zq=>!/^\\s*\\//.test(zq)).join("\\n")}}}',
 'v3: Satz bleibt ganz; kleine Zeile nur aus Zeilen mit / am Anfang', 1))

P.append((
 'title:"Geladene Datei",children:"karten392"',
 'title:"Geladene Datei",children:"karten393"',
 'Versionsschild auf karten393', 1))


# 394 — /noir/: Schrift groesser und enger gesetzt, mehr Hoehe fuer den Text;
# / -Zeile auch in Noir als kleine Zeile.

P.append((
 'fotoLaufweite:30,fotoZeile:1.08,deckblattGroesse:104,fotoGroesse:80,textHoeheTextfrei:.46,',
 'fotoLaufweite:-15,fotoZeile:1.02,deckblattGroesse:132,fotoGroesse:104,textHoeheTextfrei:.56,autoUnter:1,',
 'Noir: Schrift groesser, enger gesetzt; / -Zeile als kleine Zeile', 1))

P.append((
 'randUnten:.86,gesichtAbstand:.06,',
 'randUnten:.885,gesichtAbstand:.025,',
 'Noir: mehr Hoehe fuer den Text (naeher ans Kinn, etwas tiefer)', 1))

P.append((
 'title:"Geladene Datei",children:"karten393"',
 'title:"Geladene Datei",children:"karten394"',
 'Versionsschild auf karten394', 1))


# 395 — Textkacheln (Setzer 'marke' und plate) verstehen Kicker + /-Zeile;
# Hauptadresse (v3): Schrift groesser, enger, mehr Hoehe unter dem Gesicht.

P.append((
 'const Qe=Be(t.text),{plain:$e,segments:qe}=ye(Qe?Qe.rest:t.text)',
 'const zPL=(()=>{try{if(BS_KACHEL.autoUnter!==1||t.secondaryText)return null;const zl=String(t.text||"").split(/\\r?\\n/);let zk="";if(BS_KACHEL.kickerAn===1&&zl.length>1&&/^[A-ZÄÖÜ0-9 &\\-.:#]{2,24}$/.test(zl[0].trim()))zk=zl.shift().trim();const zu=zl.filter(zq=>/^\\s*\\//.test(zq)).map(zq=>zq.replace(/^\\s*\\/\\s*/,"").trim()).filter(Boolean);if(!zk&&!zu.length)return null;return{k:zk,u:zu.join(" "),text:zl.filter(zq=>!/^\\s*\\//.test(zq)).join("\\n")}}catch(zz){return null}})(),zPTx=zPL?zPL.text:t.text;const Qe=Be(zPTx),{plain:$e,segments:qe}=ye(Qe?Qe.rest:zPTx)',
 'Textkachel: Kicker und /-Zeile aus dem Text loesen', 1))

P.append((
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText?zTeilen(Qe?Qe.rest:t.text,!1):null;',
 'const zSp=BS_KACHEL.lisaTeilen!==0&&!ge.bigWord&&!t.secondaryText&&!(zPL&&zPL.u)?zTeilen(Qe?Qe.rest:zPTx,!1):null;',
 'Textkachel: nicht selbst teilen, wenn /-Zeile da', 1))

P.append((
 'const zRl=zInsetUnten<=0?zRolle(t.text):"normal";',
 'const zRl=zInsetUnten<=0?zRolle(zPTx):"normal";',
 'Textkachel: Rolle aus dem Satz ohne Zusatzzeilen', 1))

P.append((
 '}catch(zz){}if(zRl==="normal"&&zSp&&zUnter(zHt,zSp.unten,me,zInsetUnten>0?!1:lt==="left",Ye)',
 '}catch(zz){}try{if(zPL&&zHt){zHt.initDimensions&&zHt.initDimensions();const zFS=BS_KACHEL.fliessSchrift||"MontserratBrand",zX=zHt.left,zOX=zHt.originX||"center",zW=r*.74,zG=n*.035;let zU=null,zK=null;if(zPL.u){zU=new Pe.fabric.Textbox(zPL.u.toUpperCase(),{left:zX,top:0,originX:zOX,originY:"top",width:zW,fontSize:r*(Number(BS_KACHEL.fliessGroesse)||.026),fontFamily:zFS,fontWeight:"400",fill:G(me,.85),textAlign:et,lineHeight:1.3,selectable:!1});zU.initDimensions&&zU.initDimensions()}if(zPL.k){zK=new Pe.fabric.Text(zPL.k.toUpperCase(),{left:zX,top:0,originX:zOX,originY:"bottom",fontSize:Math.round(r*(Number(BS_KACHEL.kickerGroesse)||.019)),fontFamily:zFS,fontWeight:"400",charSpacing:400,fill:G(me,.8),selectable:!1})}const zH=zHt.height||0,zUH=zU?(zU.height||0)+zG:0,zKH=zK?(zK.height||0)+zG*.7:0;let zTp=(zHt.originY==="center"?zHt.top-zH/2:zHt.top)-(zUH-zKH)/2;zHt.set("top",zHt.originY==="center"?zTp+zH/2:zTp);zHt.setCoords&&zHt.setCoords();zK&&(zK.set("top",zTp-zG*.7),e.add(zK));zU&&(zU.set("top",zTp+zH+zG),e.add(zU))}}catch(zz){}if(zRl==="normal"&&zSp&&zUnter(zHt,zSp.unten,me,zInsetUnten>0?!1:lt==="left",Ye)',
 'Textkachel: kleines Wort oben, kleine Zeile unten', 1))

P.append((
 'const K=BS_KACHEL;',
 'const K=BS_KACHEL;let zMK="",zMU="",ROH2=ROH;try{if(K.autoUnter===1){const zl=String(ROH).split(/\\r?\\n/);if(K.kickerAn===1&&zl.length>1&&/^[A-ZÄÖÜ0-9 &\\-.:#]{2,24}$/.test(zl[0].trim()))zMK=zl.shift().trim();zMU=zl.filter(zq=>/^\\s*\\//.test(zq)).map(zq=>zq.replace(/^\\s*\\/\\s*/,"").trim()).filter(Boolean).join(" ");if(zMK||zMU)ROH2=zl.filter(zq=>!/^\\s*\\//.test(zq)).join(" ")}}catch(zz){}',
 'Textkachel (marke): Kicker und /-Zeile loesen', 1))

P.append((
 'const B0=ROH.replace(',
 'const B0=ROH2.replace(',
 'marke: Satz ohne Zusatzzeilen', 1))

P.append((
 'const zRR=String(ROH||"")',
 'const zRR=String(ROH2||"")',
 'marke: Markierungen aus dem Satz', 1))

P.append((
 'let y=n*K.mitte-M.h/2+GRO(0,gr)*.5;',
 'const zMG=n*.035,zMUb=zMU?new Pe.fabric.Textbox(zMU.toLocaleUpperCase("de-DE"),{left:LI?r*K.rand:r/2,top:0,originX:LI?"left":"center",originY:"top",width:MAXB*.9,fontSize:r*(Number(K.fliessGroesse)||.026),fontFamily:K.fliessSchrift||GLATT,fontWeight:"400",fill:SCH,opacity:.85,textAlign:LI?"left":"center",lineHeight:1.3,selectable:!1,evented:!1}):null;zMUb&&zMUb.initDimensions&&zMUb.initDimensions();const zMKt=zMK?new Pe.fabric.Text(zMK.toLocaleUpperCase("de-DE"),{left:LI?r*K.rand:r/2,top:0,originX:LI?"left":"center",originY:"bottom",fontSize:Math.round(r*(Number(K.kickerGroesse)||.019)),fontFamily:K.fliessSchrift||GLATT,fontWeight:"400",charSpacing:400,fill:SCH,opacity:.8,selectable:!1,evented:!1}):null;const zMV=((zMUb?(zMUb.height||0)+zMG:0)-(zMKt?(zMKt.height||0)+zMG*.7:0))/2,zMTop=n*K.mitte-M.h/2-zMV,zMBot=zMTop+M.h-(NA?gr*K.nameAbstand:0);let y=n*K.mitte-M.h/2+GRO(0,gr)*.5-zMV;zMKt&&(zMKt.set("top",zMTop-zMG*.7),add(zMKt));zMUb&&(zMUb.set("top",zMBot+zMG),add(zMUb));',
 'marke: kleines Wort oben, kleine Zeile unten', 1))

P.append((
 'fotoLaufweite:0,fotoZeile:1.0,deckblattGroesse:150,fotoGroesse:116,textHoeheTextfrei:.56,',
 'fotoLaufweite:-15,fotoZeile:.98,deckblattGroesse:172,fotoGroesse:136,textHoeheTextfrei:.64,bandNutzung:.98,randUnten:.9,',
 'v3: Schrift groesser, enger gesetzt, mehr Hoehe', 1))

P.append((
 '(t._freiBand[1]-t._freiBand[0])*.9)',
 '(t._freiBand[1]-t._freiBand[0])*(Number(BS_KACHEL.bandNutzung)||.9))',
 'Band-Ausnutzung per Regler', 1))

P.append((
 'title:"Geladene Datei",children:"karten394"',
 'title:"Geladene Datei",children:"karten395"',
 'Versionsschild auf karten395', 1))


# 396 — Lesbar im Feed: Groessenanpassung rechnet mit dem echten Zeilenabstand
# (zeileEcht), Mindestgroesse auf Fotos (fotoMin); Noir kleine Zeile/Kicker groesser.

P.append((
 'if(((Ve.length+pt.length)*qe*1.3<=Je&&',
 'if(((Ve.length+pt.length)*qe*(BS_KACHEL.zeileEcht===1&&$e?(Number(BS_KACHEL.fotoZeile)||1.3)*1.04:1.3)<=Je&&',
 'Groessenanpassung rechnet mit dem echten Zeilenabstand', 1))

P.append((
 '||qe<=c(16)||rt++>60)break;',
 '||qe<=Math.max(c(16),$e?r*(Number(BS_KACHEL.fotoMin)||0):0)||rt++>60)break;',
 'Mindestgroesse auf Fotos (fotoMin)', 1))

P.append((
 'fliessGroesse:.024,',
 'fliessGroesse:.032,kickerGroesse:.024,',
 'Noir: kleine Zeile und Kicker groesser', 1))

P.append((
 'autoUnter:1,',
 'autoUnter:1,zeileEcht:1,fotoMin:.062,',
 'Noir: echter Zeilenabstand, Mindestgroesse fuer den Feed', 1))

P.append((
 'title:"Geladene Datei",children:"karten395"',
 'title:"Geladene Datei",children:"karten396"',
 'Versionsschild auf karten396', 1))


# 397 — v3 (Hauptadresse): Playfair Display normal + kursiv statt Cormorant, enger gesetzt.

P.append((
 'const BS_V3={fotoSchrift:"CormorantV3",deckblattFamilie:"CormorantV3",folgeFamilie:"CormorantV3",kastenSchrift:"CormorantV3",lisaSchrift:"CormorantV3",folgeSchrift:"CormorantV3",ablaufTitel:"CormorantV3",deckblattGewicht:"500",gewicht:"500",folgeGewicht:"500",fotoLaufweite:-15,fotoZeile:.98,deckblattGroesse:172,fotoGroesse:136,textHoeheTextfrei:.64,bandNutzung:.98,randUnten:.9,kickerGroesse:.024,akzentFarbe:"#FFFFFF",akzentFarbeDunkel:"#231F20",akzentGewicht:"700",fliessSchrift:"HelveticaNeueBrand",fliessGroesse:.032,fliessVersal:1,bandUnten:1,bandMinUnten:.28,autoUnter:1,nameText:"Carina",nameSchrift:"CaveatV3",nameGewicht:"500",nameLaufweite:0,nameAnteil:.06,nameUnten:.935,nameFarbe:"#FFFFFF",nameDeckkraft:.95,dunkelFarbe:"#231F20",grundA:"#FFFFFF",grundB:"#E0DCD9",schriftA:"#231F20",schriftB:"#231F20",schriftart:"CormorantV3",unterSchrift:"CormorantV3",scrimZiel:82',
 'const BS_V3={fotoSchrift:"Playfair Display",deckblattFamilie:"Playfair Display",folgeFamilie:"Playfair Display",kastenSchrift:"Playfair Display",lisaSchrift:"Playfair Display",folgeSchrift:"Playfair Display",ablaufTitel:"Playfair Display",deckblattGewicht:"400",gewicht:"400",folgeGewicht:"400",fotoLaufweite:-25,fotoZeile:.96,deckblattGroesse:172,fotoGroesse:136,textHoeheTextfrei:.64,bandNutzung:.98,randUnten:.9,kickerGroesse:.024,akzentFarbe:"#FFFFFF",akzentFarbeDunkel:"#231F20",akzentGewicht:"500",fliessSchrift:"HelveticaNeueBrand",fliessGroesse:.032,fliessVersal:1,bandUnten:1,bandMinUnten:.28,autoUnter:1,nameText:"Carina",nameSchrift:"CaveatV3",nameGewicht:"500",nameLaufweite:0,nameAnteil:.06,nameUnten:.935,nameFarbe:"#FFFFFF",nameDeckkraft:.95,dunkelFarbe:"#231F20",grundA:"#FFFFFF",grundB:"#E0DCD9",schriftA:"#231F20",schriftB:"#231F20",schriftart:"Playfair Display",unterSchrift:"Playfair Display",scrimZiel:82',
 'v3: Playfair Display (normal + kursiv), enger gesetzt', 1))

P.append((
 'title:"Geladene Datei",children:"karten396"',
 'title:"Geladene Datei",children:"karten397"',
 'Versionsschild auf karten397', 1))


# 398 — v3: carinaannaprav in Playfair statt Carina (Fotos und Textkacheln).

P.append((
 'nameText:"Carina",nameSchrift:"CaveatV3",nameGewicht:"500",nameLaufweite:0,nameAnteil:.06,',
 'nameText:"carinaannaprav",nameSchrift:"Playfair Display",nameGewicht:"400",nameLaufweite:60,nameAnteil:.034,handleSchrift:"Playfair Display",',
 'v3: carinaannaprav in Playfair statt Carina', 1))

P.append((
 'fontSize:c(14),fontFamily:FETT,fontWeight:"700",charSpacing:140,',
 'fontSize:BS_KACHEL.handleSchrift?c(17):c(14),fontFamily:BS_KACHEL.handleSchrift||FETT,fontWeight:BS_KACHEL.handleSchrift?"400":"700",charSpacing:BS_KACHEL.handleSchrift?60:140,',
 'Textkacheln: Name in handleSchrift', 1))

P.append((
 'title:"Geladene Datei",children:"karten397"',
 'title:"Geladene Datei",children:"karten398"',
 'Versionsschild auf karten398', 1))


# 399 — Folgefolien/Textfolien ohne Foto dunkel wie Noir (Farben aus BS_NOIR), Playfair bleibt.

P.append((
 'grundA:"#FFFFFF",grundB:"#E0DCD9",schriftA:"#231F20",schriftB:"#231F20",',
 '',
 'v3: Textfolien dunkel wie Noir (Farben von BS_NOIR)', 1))

P.append((
 'title:"Geladene Datei",children:"karten398"',
 'title:"Geladene Datei",children:"karten399"',
 'Versionsschild auf karten399', 1))


# 400 — Folgefolien wie das fruehe Noir: Text linksbuendig ins Eck (folgeEck), Titelbild bleibt mittig.

P.append((
 'BS_KACHEL.obenLinks===1&&$e&&t._freiBand&&(tt.ausrichtung=t._freiBand[0]<.2?"links":"mitte"),',
 'BS_KACHEL.obenLinks===1&&$e&&t._freiBand&&(tt.ausrichtung=t._freiBand[0]<.2?"links":"mitte"),BS_KACHEL.folgeEck===1&&$e&&t.folienRolle&&t.folienRolle!=="deckblatt"&&(tt.ausrichtung="links"),',
 'Folgefolien auf Foto: Text linksbuendig ins Eck (folgeEck)', 1))

P.append((
 'bandUnten:1,',
 'bandUnten:1,folgeEck:1,folgeAusrichtung:"links",',
 'v3: Folgefolien ins Eck, Textfolien linksbuendig', 1))

P.append((
 'title:"Geladene Datei",children:"karten399"',
 'title:"Geladene Datei",children:"karten400"',
 'Versionsschild auf karten400', 1))


# 401 — Look-Schalter: BS_MARKEN (bordeaux, bordeauxgloock, creme) ueber v3, gewaehlt per window.BS_MARKE
# (marken-schalter.js / ?look=). Mehr Schriften vorladen.

P.append((
 'if(typeof window<"u"&&window.BS_STIL==="v3")Object.assign(BS_KACHEL,BS_V3);',
 'if(typeof window<"u"&&window.BS_STIL==="v3")Object.assign(BS_KACHEL,BS_V3);const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"}};try{if(typeof window<"u"&&window.BS_STIL==="v3"&&window.BS_MARKE&&BS_MARKEN[window.BS_MARKE])Object.assign(BS_KACHEL,BS_MARKEN[window.BS_MARKE])}catch(zz){}',
 'Look-Schalter: BS_MARKEN ueber v3 legen (window.BS_MARKE)', 1))

P.append((
 'new Set([BS_KACHEL.lisaSchrift,BS_KACHEL.folgeSchrift,BS_KACHEL.nameSchrift,BS_KACHEL.fliessSchrift].filter(Boolean))',
 'new Set([BS_KACHEL.lisaSchrift,BS_KACHEL.folgeSchrift,BS_KACHEL.nameSchrift,BS_KACHEL.fliessSchrift,BS_KACHEL.handleSchrift,BS_KACHEL.versalFamilie,BS_KACHEL.fotoSchrift,BS_KACHEL.schriftart].filter(Boolean))',
 'auch Namens-, Versal- und Fotoschrift vorladen', 1))

P.append((
 'title:"Geladene Datei",children:"karten400"',
 'title:"Geladene Datei",children:"karten401"',
 'Versionsschild auf karten401', 1))


# 402 — Look bordeauxmix (Textposts Instrument Serif, Fotos Gloock), platteFamilie fuer Textposts,
# v3: Fotoschrift einen Ticken groesser (190/150, fotoMin .07), jeder 3. Tag ein Textpost (textJede 3).

P.append((
 'const FAM=ix=>FOLGE?K.folgeFamilie:(ix===0?K.schriftart:(K.unterSchrift||K.schriftart));',
 'const FAM=ix=>K.platteFamilie?K.platteFamilie:FOLGE?K.folgeFamilie:(ix===0?K.schriftart:(K.unterSchrift||K.schriftart));',
 'Textposts: eigene Schrift (platteFamilie) statt folgeFamilie', 1))

P.append((
 'zFont=(zHatFoto)=>{try{',
 'zFont=(zHatFoto)=>{try{if(!zHatFoto&&BS_KACHEL.platteFamilie)return BS_KACHEL.platteFamilie;',
 'Textkachel-Zweig: platteFamilie', 1))

P.append((
 'deckblattGroesse:172,fotoGroesse:136,',
 'deckblattGroesse:190,fotoGroesse:150,fotoMin:.07,textJede:3,',
 'v3: Schrift auf Fotos einen Ticken groesser, jeder 3. Tag ein Textpost', 1))

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif"}}',
 'Look bordeauxmix: Textposts Instrument Serif, Fotos Gloock', 1))

P.append((
 'BS_KACHEL.fotoSchrift,BS_KACHEL.schriftart].filter(Boolean))',
 'BS_KACHEL.fotoSchrift,BS_KACHEL.schriftart,BS_KACHEL.platteFamilie,BS_KACHEL.deckblattFamilie].filter(Boolean))',
 'Textpost- und Titelschrift vorladen', 1))

P.append((
 'title:"Geladene Datei",children:"karten401"',
 'title:"Geladene Datei",children:"karten402"',
 'Versionsschild auf karten402', 1))


# 403 — Farbueberzug pro Tag (ueberzugReihe); Bordeaux-Looks meist SW / SW mit rotem Ueberzug, wenige farbig;
# jeder 2. Tag ein Textpost (textJede 2).

P.append((
 '(()=>{const zU=Number(BS_KACHEL.bildUeberzug)||0;',
 '(()=>{const zU=(()=>{const zl=String(BS_KACHEL.ueberzugReihe||"").split("|").filter(zx=>zx!=="");if(zl.length&&typeof t._tag=="number"){const zv=parseFloat(zl[((t._tag%zl.length)+zl.length)%zl.length]);return isNaN(zv)?0:zv}return Number(BS_KACHEL.bildUeberzug)||0})();',
 'Farbueberzug pro Tag (ueberzugReihe)', 1))

P.append((
 'textJede:3,',
 'textJede:2,',
 'v3: jeder 2. Tag ein Textpost', 1))

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.2,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif"}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.45|0|0|.45","ueberzugTon":"128,30,26","ueberzugModus":"multiply"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.45|0|0|.45","ueberzugTon":"128,30,26","ueberzugModus":"multiply"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.45|0|0|.45","ueberzugTon":"128,30,26","ueberzugModus":"multiply"}}',
 'Bordeaux-Looks: meist SW, jedes 2. SW-Bild mit rotem Ueberzug, wenige farbig', 1))

P.append((
 'title:"Geladene Datei",children:"karten402"',
 'title:"Geladene Datei",children:"karten403"',
 'Versionsschild auf karten403', 1))


# 404 — roter Ueberzug im Modus color (196,38,26 bei .85) statt multiply: klares Rot statt Mauve.

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.45|0|0|.45","ueberzugTon":"128,30,26","ueberzugModus":"multiply"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.45|0|0|.45","ueberzugTon":"128,30,26","ueberzugModus":"multiply"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.45|0|0|.45","ueberzugTon":"128,30,26","ueberzugModus":"multiply"}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.85|0|0|.85","ueberzugTon":"196,38,26","ueberzugModus":"color"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.85|0|0|.85","ueberzugTon":"196,38,26","ueberzugModus":"color"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.85|0|0|.85","ueberzugTon":"196,38,26","ueberzugModus":"color"}}',
 'Bordeaux-Looks: roter Ueberzug im Modus color (klares Rot statt Mauve)', 1))

P.append((
 'title:"Geladene Datei",children:"karten403"',
 'title:"Geladene Datei",children:"karten404"',
 'Versionsschild auf karten404', 1))


# 405 — roter Overlay ohne Einfaerben: source-over 194,64,28 bei .4 (waermeres Rot).

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.85|0|0|.85","ueberzugTon":"196,38,26","ueberzugModus":"color"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.85|0|0|.85","ueberzugTon":"196,38,26","ueberzugModus":"color"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.85|0|0|.85","ueberzugTon":"196,38,26","ueberzugModus":"color"}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.4|0|0|.4","ueberzugTon":"194,64,28","ueberzugModus":"source-over"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.4|0|0|.4","ueberzugTon":"194,64,28","ueberzugModus":"source-over"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.4|0|0|.4","ueberzugTon":"194,64,28","ueberzugModus":"source-over"}}',
 'Bordeaux-Looks: warmroter Overlay darueber statt Einfaerben', 1))

P.append((
 'title:"Geladene Datei",children:"karten404"',
 'title:"Geladene Datei",children:"karten405"',
 'Versionsschild auf karten405', 1))


# 406 — Overlay-Kacheln bleiben farbig, Overlay im Modus overlay (Schwarz bleibt schwarz), eigener Kontrast.

P.append((
 'if(!(zU>0)||!t.background||!(zSat<=-.99))return;',
 'if(!(zU>0)||!t.background||(!BS_KACHEL.ueberzugReihe&&!(zSat<=-.99)))return;',
 'Overlay auch auf farbigen Fotos, wenn ueberzugReihe gesetzt', 1))

P.append((
 'try{const zK=Number(BS_KACHEL.bildKontrast)||0,zH=Number(BS_KACHEL.bildHelligkeit)||0,zFl=[];',
 'try{const zUe=(()=>{try{const zl=String(BS_KACHEL.ueberzugReihe||"").split("|").filter(zx=>zx!=="");if(!zl.length||typeof t._tag!="number")return 0;const zv=parseFloat(zl[((t._tag%zl.length)+zl.length)%zl.length]);return isNaN(zv)?0:zv}catch(zz){return 0}})(),zK=(Number(BS_KACHEL.bildKontrast)||0)+(zUe>0?(Number(BS_KACHEL.ueberzugKontrast)||0):0),zH=(Number(BS_KACHEL.bildHelligkeit)||0)+(zUe>0?(Number(BS_KACHEL.ueberzugHell)||0):0),zFl=[];',
 'Overlay-Kacheln: eigener Kontrast/Helligkeit (tiefes Schwarz)', 1))

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.4|0|0|.4","ueberzugTon":"194,64,28","ueberzugModus":"source-over"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.4|0|0|.4","ueberzugTon":"194,64,28","ueberzugModus":"source-over"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0.1|-1|-1","saettigungWechsel":1,"ueberzugReihe":"0|.4|0|0|.4","ueberzugTon":"194,64,28","ueberzugModus":"source-over"}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.7|0|0|.7","ueberzugTon":"194,64,28","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.7|0|0|.7","ueberzugTon":"194,64,28","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.7|0|0|.7","ueberzugTon":"194,64,28","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05}}',
 'Bordeaux-Looks: Overlay-Kacheln farbig mit tiefem Schwarz', 1))

P.append((
 'title:"Geladene Datei",children:"karten405"',
 'title:"Geladene Datei",children:"karten406"',
 'Versionsschild auf karten406', 1))


# 407 — Lange Texte laufen nicht mehr ueber: fotoMin nur, solange der Text passt; Versalien nur bis versalMaxZeichen;
# Bordeaux-Looks randUnten .86 (ueber der Handschrift), Overlay waermer/schwaecher.

P.append((
 '||qe<=Math.max(c(16),$e?r*(Number(BS_KACHEL.fotoMin)||0):0)||rt++>60)break;',
 '||qe<=Math.max(c(16),$e&&(Ve.length+pt.length)*qe*1.05<=n*(Number(BS_KACHEL.fotoMinHoehe)||.62)?r*(Number(BS_KACHEL.fotoMin)||0):0)||rt++>60)break;',
 'Mindestgroesse nur, solange der Text dann noch passt (lange Texte werden kleiner)', 1))

P.append((
 'try{if(!$e||!BS_KACHEL.versalAnteil)return!1;',
 'try{if(!$e||!BS_KACHEL.versalAnteil)return!1;if(BS_KACHEL.versalMaxZeichen&&String(t.text||"").replace(/\\s+/g," ").length>BS_KACHEL.versalMaxZeichen)return!1;',
 'Grossbuchstaben nur fuer kurze Texte (versalMaxZeichen)', 1))

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.7|0|0|.7","ueberzugTon":"194,64,28","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.7|0|0|.7","ueberzugTon":"194,64,28","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.7|0|0|.7","ueberzugTon":"194,64,28","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.58|0|0|.58","ueberzugTon":"196,78,26","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05,"randUnten":0.86,"versalMaxZeichen":120},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.58|0|0|.58","ueberzugTon":"196,78,26","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05,"randUnten":0.86},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.58|0|0|.58","ueberzugTon":"196,78,26","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05,"randUnten":0.86}}',
 'Bordeaux-Looks: Text endet ueber der Handschrift-Unterschrift; Versalien nur bis 90 Zeichen', 1))

P.append((
 'title:"Geladene Datei",children:"karten406"',
 'title:"Geladene Datei",children:"karten407"',
 'Versionsschild auf karten407', 1))


# 408 — Bordeaux-Looks: Duoton Bordeaux (duoReihe) im Wechsel mit natuerlicher Farbe; Overlay und Rotstich raus.

P.append((
 'globalCompositeOperation:zM,selectable:!1,evented:!1})),zUeberAn=!0})();',
 'globalCompositeOperation:zM,selectable:!1,evented:!1})),zUeberAn=!0})();(()=>{try{const zl=String(BS_KACHEL.duoReihe||"").split("|").filter(zx=>zx!=="");if(!zl.length||typeof t._tag!="number"||!t.background||!(zSat<=-.99)||!BS_MISCHBAR)return;if(parseFloat(zl[((t._tag%zl.length)+zl.length)%zl.length])!==1)return;const zD=String(BS_KACHEL.duoDunkel||"40,6,8").split(",").map(Number),zL=String(BS_KACHEL.duoHell||"246,228,214").split(",").map(Number);e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgb(${zL.map((zv,zi)=>Math.max(0,zv-zD[zi])).join(",")})`,globalCompositeOperation:"multiply",selectable:!1,evented:!1}));e.add(new Pe.fabric.Rect({left:0,top:0,width:r,height:n,fill:`rgb(${zD.join(",")})`,globalCompositeOperation:"lighter",selectable:!1,evented:!1}))}catch(zz){}})();',
 'Duoton pro Tag (duoReihe): Schatten duoDunkel, Lichter duoHell', 1))

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.58|0|0|.58","ueberzugTon":"196,78,26","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05,"randUnten":0.86,"versalMaxZeichen":120},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.58|0|0|.58","ueberzugTon":"196,78,26","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05,"randUnten":0.86},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0.1,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|0.1|0.1|-1|0.1","saettigungWechsel":1,"ueberzugReihe":"0|.58|0|0|.58","ueberzugTon":"196,78,26","ueberzugModus":"overlay","ueberzugKontrast":0.22,"ueberzugHell":-0.05,"randUnten":0.86}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"versalMaxZeichen":120,"duoReihe":"1|1|0|0","duoDunkel":"40,6,8","duoHell":"246,228,214"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"duoReihe":"1|1|0|0","duoDunkel":"40,6,8","duoHell":"246,228,214"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"duoReihe":"1|1|0|0","duoDunkel":"40,6,8","duoHell":"246,228,214"}}',
 'Bordeaux-Looks: abwechselnd Duoton Bordeaux und natuerliche Farbe, kein Overlay, kein Rotstich', 1))

P.append((
 'title:"Geladene Datei",children:"karten407"',
 'title:"Geladene Datei",children:"karten408"',
 'Versionsschild auf karten408', 1))


# 409 — kleine Zeile wird mit der Fliessschrift gemessen (Umbruch und Zentrierung), nicht mit der Headline-/Zweitschrift.

P.append((
 ',Ht=(Je,rt,Ve)=>{const pt={fontSize:rt,fontFamily:Ve?Qe:((zVS&&BS_KACHEL.versalFamilie)||BS_KACHEL.zweiteFamilie||Qe),fontWeight:Ve?kt:"400",charSpacing:zCS};',
 ',Ht=(Je,rt,Ve)=>{const pt={fontSize:rt,fontFamily:Ve?Qe:(t._zMF?(BS_KACHEL.fliessSchrift||Qe):((zVS&&BS_KACHEL.versalFamilie)||BS_KACHEL.zweiteFamilie||Qe)),fontWeight:Ve?kt:"400",charSpacing:t._zMF&&!Ve?0:zCS};',
 'Messung der kleinen Zeile in der Fliessschrift (t._zMF)', 1))

P.append((
 'Zt=(t.secondaryText||t._autoUnter)?$t(_t(BS_KACHEL.fliessVersal===1&&(i.slideIndex||0)===0?String(t.secondaryText||t._autoUnter).toUpperCase():(t.secondaryText||t._autoUnter)),St,!1):[]',
 'Zt=(()=>{t._zMF=1;try{return (t.secondaryText||t._autoUnter)?$t(_t(BS_KACHEL.fliessVersal===1&&(i.slideIndex||0)===0?String(t.secondaryText||t._autoUnter).toUpperCase():(t.secondaryText||t._autoUnter)),St,!1):[]}finally{t._zMF=0}})()',
 'Umbruch der kleinen Zeile mit der Fliessschrift messen', 1))

P.append((
 'let rt=tt.ausrichtung==="links"?_e:r/2-Ht(Je,St,!1)/2;const Ve=new Pe.fabric.Shadow(',
 'let rt=tt.ausrichtung==="links"?_e:r/2-(()=>{t._zMF=1;try{return Ht(Je,St,!1)}finally{t._zMF=0}})()/2;const Ve=new Pe.fabric.Shadow(',
 'Zentrieren der kleinen Zeile mit der Fliessschrift', 1))

P.append((
 'title:"Geladene Datei",children:"karten408"',
 'title:"Geladene Datei",children:"karten409"',
 'Versionsschild auf karten409', 1))


# 410 — Bordeaux-Looks: Duoton raus, wieder normales Schwarz-Weiss im Wechsel mit natuerlicher Farbe.

P.append((
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"versalMaxZeichen":120,"duoReihe":"1|1|0|0","duoDunkel":"40,6,8","duoHell":"246,228,214"},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"duoReihe":"1|1|0|0","duoDunkel":"40,6,8","duoHell":"246,228,214"},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"duoReihe":"1|1|0|0","duoDunkel":"40,6,8","duoHell":"246,228,214"}}',
 'const BS_MARKEN={"bordeaux":{"fotoSchrift":"Instrument Serif","deckblattFamilie":"Instrument Serif","folgeFamilie":"Instrument Serif","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Instrument Serif","ablaufTitel":"Instrument Serif","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"versalAnteil":100,"versalFamilie":"Instrument Serif","versalLaufweite":0,"versalGroesse":0,"handGroesse":1,"fotoLaufweite":0,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86,"versalMaxZeichen":120},"bordeauxgloock":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Gloock","lisaSchrift":"Gloock","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Gloock","unterSchrift":"Gloock","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86},"creme":{"fotoSchrift":"Bodoni Moda SC","deckblattFamilie":"Bodoni Moda SC","folgeFamilie":"Bodoni Moda SC","kastenSchrift":"Bodoni Moda SC","lisaSchrift":"Bodoni Moda SC","folgeSchrift":"Bodoni Moda SC","ablaufTitel":"Bodoni Moda SC","schriftart":"Bodoni Moda SC","unterSchrift":"Bodoni Moda SC","fotoLaufweite":10,"akzentFarbe":"#F3D6C2","akzentGewicht":"400","grundA":"#F1E9DC","grundB":"#F1E9DC","schriftA":"#2B1D14","schriftB":"#2B1D14","akzentFarbeDunkel":"#8B3A2B","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400"},"bordeauxmix":{"fotoSchrift":"Gloock","deckblattFamilie":"Gloock","folgeFamilie":"Gloock","kastenSchrift":"Instrument Serif","lisaSchrift":"Instrument Serif","folgeSchrift":"Gloock","ablaufTitel":"Gloock","schriftart":"Instrument Serif","unterSchrift":"Instrument Serif","grundA":"#6B1E1A","grundB":"#6B1E1A","schriftA":"#F4EDE1","schriftB":"#F4EDE1","fliessSchrift":"Courier Prime","fliessVersal":0,"fliessGroesse":0.03,"nameText":"carinaannaprav","nameSchrift":"Mrs Saint Delafield","nameAnteil":0.075,"nameLaufweite":0,"nameGewicht":"400","handleSchrift":"Mrs Saint Delafield","gewicht":"400","deckblattGewicht":"400","folgeGewicht":"400","bildTonung":"#6B1E1A","bildTonungKraft":0,"fotoLaufweite":-10,"akzentFarbe":"#F1D9C9","akzentGewicht":"400","platteFamilie":"Instrument Serif","saettigungReihe":"-1|-1|0|0","saettigungWechsel":1,"randUnten":0.86}}',
 'Bordeaux-Looks: Duoton raus, wieder normales Schwarz-Weiss (im Wechsel mit natuerlicher Farbe)', 1))

P.append((
 'title:"Geladene Datei",children:"karten409"',
 'title:"Geladene Datei",children:"karten410"',
 'Versionsschild auf karten410', 1))


# 411 — Absaetze: Import behaelt Leerzeilen innerhalb einer Folie; Textkacheln: Zeilenumbruch = neue Zeile,
# Leerzeile = Absatz mit Luft (absatzEcht, absatzLuft), in die Groessenanpassung eingerechnet.

P.append((
 'zKap=!1}if(!a)return;const u=a.match(/^(?:Tag|Day|Woche)',
 'zKap=!1}if(!a){s.length&&s[s.length-1]!==""&&s.push("");return}const u=a.match(/^(?:Tag|Day|Woche)',
 'Import: Leerzeilen innerhalb einer Folie bleiben als Absatz', 1))

P.append((
 'const umbruch=(x,gr,fam,max,gew)=>{const w=String(x).split(/\\s+/).filter(Boolean),z=[];',
 'const umbruch=(x,gr,fam,max,gew)=>{if(/\\n/.test(String(x)))return String(x).split("\\n").reduce((za,zt)=>za.concat(zt.trim()?umbruch(zt,gr,fam,max,gew):[]),[]);const w=String(x).split(/\\s+/).filter(Boolean),z=[];',
 'Textkacheln: Zeilenumbruch im Text bleibt ein Umbruch', 1))

P.append((
 '.split(BS_KACHEL.einBlock===1?/\\n/:/\\n\\s*\\n/)',
 '.split(BS_KACHEL.absatzEcht===1?/\\n\\s*\\n/:BS_KACHEL.einBlock===1?/\\n/:/\\n\\s*\\n/)',
 'Textkacheln: Leerzeile = Absatz (absatzEcht)', 1))

P.append((
 'if(zMK||zMU)ROH2=zl.filter(zq=>!/^\\s*\\//.test(zq)).join(" ")',
 'if(zMK||zMU)ROH2=zl.filter(zq=>!/^\\s*\\//.test(zq)).join(K.absatzEcht===1?"\\n":" ")',
 'Textkacheln: Umbrueche bleiben auch mit Kicker/Zusatzzeile', 1))

P.append((
 'const BL=BS_KACHEL.kachelSatzUmbruch?B0.reduce((za,zb)=>za.concat(zSatz(zb)),[]):',
 'const zPE=[];const BL=BS_KACHEL.kachelSatzUmbruch?B0.reduce((za,zb)=>{const zq=zSatz(zb);zq.forEach((zx,zi)=>zPE.push(zi===zq.length-1));return za.concat(zq)},[]):',
 'Textkacheln: merken, wo ein Absatz endet', 1))

P.append((
 '+(BL.length-1)*g*K.absatz+(NA?g*K.nameAbstand:0);',
 '+BL.slice(0,-1).reduce((za,zx,zi)=>za+g*(K.absatzEcht===1&&(zPE.length?zPE[zi]:!0)?(Number(K.absatzLuft)||.6):K.absatz),0)+(NA?g*K.nameAbstand:0);',
 'Textkacheln: Absatz-Luft in die Hoehe einrechnen', 1))

P.append((
 'if(ix<ZL.length-1)y+=gr*K.absatz});',
 'if(ix<ZL.length-1)y+=gr*(K.absatzEcht===1&&(zPE.length?zPE[ix]:!0)?(Number(K.absatzLuft)||.6):K.absatz)});',
 'Textkacheln: Luft nur zwischen Absaetzen', 1))

P.append((
 'textJede:2,',
 'textJede:2,absatzEcht:1,',
 'v3: Absaetze echt', 1))

P.append((
 'title:"Geladene Datei",children:"karten410"',
 'title:"Geladene Datei",children:"karten411"',
 'Versionsschild auf karten411', 1))


# 412 — Detail-Ausschnitte zurueck: detailReihe/deckblattDetailReihe waehlen lower/bust/close vor dem Gesichts-Zuschnitt;
# liegt das Gesicht ausserhalb des Ausschnitts, steht der Text unten.

P.append((
 'lt=BS_KACHEL.zuschnittTextfrei===1&&t.textBands===!0&&!t.imageLocked?(()=>{',
 'zDet=(()=>{try{if(t.imageLocked)return null;const zl=String((Qe===0?BS_KACHEL.deckblattDetailReihe:BS_KACHEL.detailReihe)||"").split("|").filter(Boolean);if(!zl.length)return null;const zs=String(t.background||"")+"|"+String(t.text||"");let zh=0;for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;const zm=zl[(zh*7+Qe*3+1)%zl.length];return Ye[zm]?zm:null}catch(zz){return null}})(),lt=zDet?(t._zDetail=zDet,t._zGy=null,(()=>{const zb=t._zBox,zx=zb?(zb.x0+zb.x1)/2:qe,zy=zb?(zb.y0+zb.y1)/2:ht;return zDet==="face"?[zx,zy,2.3]:zDet==="close"?[zx,zy+.06,1.85]:zDet==="bust"?[zx,Math.min(.95,zy+.22),1.7]:Ye[zDet]})()):(t._zDetail=null,BS_KACHEL.zuschnittTextfrei===1&&t.textBands===!0&&!t.imageLocked?(()=>{',
 'Detail-Ausschnitte (detailReihe / deckblattDetailReihe) vor dem Gesichts-Zuschnitt', 1))

P.append((
 ':Ye[Qe===0?zDS:et[Qe%et.length]],[wt,tt,Qt]=lt',
 ':Ye[Qe===0?zDS:et[Qe%et.length]]),[wt,tt,Qt]=lt',
 'Klammer zu', 1))

P.append((
 'if(zT!=null){const zA=[zo,zT-zm],zB=[zU+zm,zu]',
 'if(zT!=null&&(zU<zo+.05||zT>zu-.05)){t._freiBand=[Math.max(.4,zu-.46),zu]}else if(zT!=null){const zA=[zo,zT-zm],zB=[zU+zm,zu]',
 'Gesicht ausserhalb des Ausschnitts: Text unten', 1))

P.append((
 'textJede:2,',
 'textJede:2,detailReihe:"-|lower|-|bust|-|close|lower",deckblattDetailReihe:"-|-|-|bust",',
 'v3: Details auf Folgefolien (lower/bust/close), ab und zu auf dem Titelbild', 1))

P.append((
 'title:"Geladene Datei",children:"karten411"',
 'title:"Geladene Datei",children:"karten412"',
 'Versionsschild auf karten412', 1))

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
