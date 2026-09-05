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
DUNKEL = ('const BS_DUNKEL={grundA:"#171512",schriftA:"#F2EFE9",'
 'grundB:"#0E0D0C",schriftB:"#F2EFE9",'
 'deckblattFamilie:"Playfair Display",fotoSchrift:"Playfair Display",'
 'deckblattGewicht:"400",deckblattGroesse:74.8,fotoGroesse:48.4,zweiteFamilie:"Nothing You Could Do",zweitAnteil:.62,'
 'schriftart:"Playfair Display",unterSchrift:"Shadows Into Light",gewicht:"400",'
 'betontGewicht:"700",handAnteil:1.15,handGroesse:1.0909,'
 'unterGewicht:"400",unterVerhaeltnis:.62,laufweite:0,fotoLaufweite:-20,'
 'folgeFamilie:"Playfair Display",ablaufTitel:"Playfair Display",'
 'nameSchrift:"Playfair Display",nameGewicht:"400",nameLaufweite:60,'
 'nameAnteil:.030,folgeAusrichtung:"mitte",textAnteil:0,'
 'geteilt:1,geteiltAnteil:25,geteiltOben:.16,geteiltUnten:.86,geteiltLuft:.05,'
 'deckblattSchnitte:"full|full|wide|full|wide|full",'
 'tonReihe:"14,13,12|26,20,16|12,16,20|22,14,20",tonNeutral:"13,13,13",'
 'versalAnteil:15,versalFamilie:"Shadows Into Light",versalGewicht:"400",'
 'versalLaufweite:20,versalGroesse:.065,versalZweitAnteil:1,'
 'fotoAusrichtung:"mitte",fotoSchriftFarbe:"#FFFFFF",'
 'bildTon:"14,13,12",waerme:0,waermeTon:"14,13,12",'
 'bildSaettigung:-1,saettigungReihe:"-1|0.1",saettigungWechsel:1,'
 'bildSchwarzpunkt:.07,bildVignette:.6,schwarzGrund:.2,textGrundZiel:4,textGrundMax:1.8,auflageReihe:"1|0.2|0.65|0.35",vignetteReihe:"1|0|0.55|0.25",auflageWechsel:1,folgeFuss:.86,lagenReihe:"unten",textMitte:.58,textLageUnten:.80,textMesseOben:.60,nameZeigen:0,'
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
 'if(!t.background&&BS_KACHEL.textAnteil===0&&t.karte!=="ablauf")try{'
 'const zB=(typeof window<"u"&&window.__bsBilder)||[];'
 'if(zB.length){const zs=String(t.text||"")+"|"+String(i.slideIndex||0);let zh=0;'
 'for(let zi=0;zi<zs.length;zi+=1)zh=(zh*31+zs.charCodeAt(zi))%99991;'
 't={...t,background:zB[zh%zB.length]}}}catch(zz){}',
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
