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

# 19 — Kachelfarben: matte Erdtoene, hell genug fuer Weiss.
#      Vorher lagen die Alltagskacheln auf Hellgrau (hell) und
#      Schiefer (stein) — die beiden waehlt aS(day-1) im Wechsel,
#      sie sind also das, was im Feed wirklich zu sehen ist.
#      Sand und helles Orange trugen weisse Schrift nicht (1,4 bzw.
#      2,1 zu 1). Olive und Gold liegen bei 5,5 und 5,4 zu 1.
#      linie und wieder bekommen dieselben Toene, damit nirgends
#      weisse Schrift auf hellem Grund steht.
P.append(('stein:{grund:SF,schriftGrund:SF,schrift:"#FFFFFF",betont:"#FFFFFF",monogramm:"#FFFFFF",absender:"rgba(255,255,255,0.60)",schriftart:"Playfair Display"}',
 'stein:{grund:"#BEB7A7",schriftGrund:"#BEB7A7",schrift:"#112250",betont:"#112250",monogramm:"#112250",absender:"rgba(17,34,80,0.62)",schriftart:"Playfair Display"}',
 "stein auf Warm Taupe #BEB7A7", 1))
P.append(('hell:{grund:OW,schriftGrund:OW,schrift:OD,betont:OD,monogramm:OD,absender:"rgba(35,40,44,0.55)",schriftart:"Playfair Display"}',
 'hell:{grund:"#E7E2CE",schriftGrund:"#E7E2CE",schrift:"#112250",betont:"#112250",monogramm:"#112250",absender:"rgba(17,34,80,0.58)",schriftart:"Playfair Display"}',
 "hell auf Champagne #E7E2CE", 1))
P.append(('linie:{grund:uA,schrift:hA,betont:hA,monogramm:F1,absender:"rgba(62,80,99,0.55)",fassung:"linie",schriftart:"PoppinsBold"}',
 'linie:{grund:"#BEB7A7",schrift:"#112250",betont:"#112250",monogramm:"#112250",absender:"rgba(17,34,80,0.62)",fassung:"linie",schriftart:"PoppinsBold"}',
 "linie auf Warm Taupe", 1))
P.append(('wieder:{grund:uA,schrift:hA,betont:hA,monogramm:F1,absender:"rgba(62,80,99,0.55)",fassung:"wieder",schriftart:"PoppinsBold"}',
 'wieder:{grund:"#E7E2CE",schrift:"#112250",betont:"#112250",monogramm:"#112250",absender:"rgba(17,34,80,0.58)",fassung:"wieder",schriftart:"PoppinsBold"}',
 "wieder auf Champagne", 1))

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
P.append(('folienRolle:ta,zaehler:"",kachelSchrift:ot.kachelSchrift||(D1(ot.day)?nS(ot.day):BG(rt.kachelSchrift)||"marke")',
 'folienRolle:ta,zaehler:"",kachelSchrift:ta==="deckblatt"?"playfair":(ot.kachelSchrift||(D1(ot.day)?nS(ot.day):BG(rt.kachelSchrift)||"marke"))',
 "Deckblatt in Playfair statt Anton", 1))
P.append(('let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?PV:OV);',
 'let qe=t.sizeLocked&&typeof t.fontSize=="number"?c(t.fontSize):c($e?(t.folienRolle==="deckblatt"?46:PV):OV);',
 "Deckblatt groesser (46 statt 34)", 1))

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
