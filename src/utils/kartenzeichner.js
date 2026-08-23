/**
 * REMINDER-FOLIEN — ZEICHNER
 * ==========================
 *
 * Zwei Fassungen, editorial gesetzt:
 *
 *   zitat    heller Grund #F5EFE9, Tinte #141210
 *            zwei bis vier Saetze, Playfair, gemischt geschrieben
 *   aussage  dunkler Grund #16202E, Schrift #F2EBE4
 *            ein bis zwei Saetze, sehr gross
 *
 * Keine Requisiten: kein Rahmen, kein Zettel, kein Klebeband, kein
 * Anfuehrungszeichen, keine Linie. Der Text fuellt die Flaeche, links
 * ausgerichtet, eng gesetzt. Unten mittig die Wortmarke.
 *
 * DAS STERNCHEN traegt die Betonung: *Wort* wird kursiv gesetzt.
 * Deshalb wird Wort fuer Wort gezeichnet statt zeilenweise — nur so
 * kann innerhalb einer Zeile die Schriftlage wechseln.
 *
 * ERWARTET im Gueltigkeitsbereich: fabric, e (Canvas), r (Breite),
 * n (Hoehe), c (Skalierung).
 *
 * WICHTIG: Playfair muss VOR dem Zeichnen geladen sein, kursiv
 * eingeschlossen — sonst misst Fabric mit der Ersatzschrift und die
 * Zeilen laufen ueber den Rand:
 *
 *   await Promise.all([
 *     document.fonts.load('400 40px "Playfair Display"'),
 *     document.fonts.load('italic 400 40px "Playfair Display"'),
 *   ]);
 */

// ---------- Farbtafel ----------
export const kartenFarben = (art) => {
  const TAFEL = {
    zitat: {
      grund: '#F5EFE9', schrift: '#141210', betont: '#141210',
      monogramm: '#141210', absender: 'rgba(20,18,16,0.55)',
      fassung: 'zitat', schriftart: 'Playfair Display',
    },
    aussage: {
      grund: '#16202E', schrift: '#F2EBE4', betont: '#F2EBE4',
      monogramm: '#F2EBE4', absender: 'rgba(242,235,228,0.60)',
      fassung: 'aussage', schriftart: 'Playfair Display',
    },
    // Die schlichten Karten ohne Foto bleiben unveraendert:
    stein: { grund: '#64737B', schrift: '#FFFFFF', betont: '#F6F1E6', monogramm: '#FFFFFF', absender: 'rgba(255,255,255,0.62)' },
    hell:  { grund: '#F6F1E6', schrift: '#141210', betont: '#141210', monogramm: '#6B5238', absender: 'rgba(20,18,16,0.45)' },
  };
  return TAFEL[art] || {
    grund: '#141210', schrift: '#F6F1E6', betont: '#F3E5AB',
    monogramm: '#A88354', absender: 'rgba(246,241,230,0.55)',
  };
};

// ---------- Zeichner ----------
// `thema` ist das Ergebnis von T1({ hatFoto: false, karte }) — also mit
// den Namen schriftFarbe / absenderFarbe / fassung.
// Rueckgabe true = fertig gezeichnet, false = auf schlichte Karte zurueckfallen.
const zeichneKarte = (thema, rohtext) =>{
const ROH=String(rohtext||"").replace(/\s+/g," ").trim();
const FA=thema.fassung;
if(!ROH||!FA)return false;
const SCH=thema.schriftFarbe||"#141210",ABS=thema.absenderFarbe||SCH;
const SERIF="Playfair Display";

/* Sternchen markieren EIN Wort oder eine Wendung kursiv — das ist
   der Kniff, der diesen Folien ihre Betonung gibt. */
const worte=[];
ROH.split(/(\*[^*]+\*)/).filter(Boolean).forEach(st=>{
const ku=/^\*[^*]+\*$/.test(st);
(ku?st.slice(1,-1):st).split(/\s+/).filter(Boolean).forEach(w=>worte.push({w:w,kursiv:ku}))});
if(!worte.length)return false;

const miss=(w,gr,ku)=>new fabric.Text(String(w),{fontSize:gr,fontFamily:SERIF,fontStyle:ku?"italic":"normal"}).width;
const brechen=(gr,maxB)=>{const sp=miss("\u00a0",gr,false)||gr*.26,zeilen=[];let z=[],br=0;
worte.forEach(o=>{const b=miss(o.w,gr,o.kursiv);
if(z.length&&br+sp+b>maxB){zeilen.push({worte:z,breite:br}),z=[],br=0}
br+=(z.length?sp:0)+b,z.push({...o,b:b})});
z.length&&zeilen.push({worte:z,breite:br});
return{zeilen:zeilen,abstand:sp}};

const L=r*.09,MAXB=r*.82,ZH=1.16;
const start=FA==="aussage"?c(74):c(44);
const maxZeilen=FA==="aussage"?5:9;
const maxHoehe=n*.60;
let gr=start,satz=brechen(gr,MAXB);
for(let i=0;i<26;i+=1){
const hoch=satz.zeilen.length*gr*ZH,breit=Math.max(...satz.zeilen.map(z=>z.breite));
if(satz.zeilen.length<=maxZeilen&&hoch<=maxHoehe&&breit<=MAXB)break;
gr*=.94,satz=brechen(gr,MAXB)}

const hoch=satz.zeilen.length*gr*ZH;
let y=n*.46-hoch/2+gr*.5;
satz.zeilen.forEach(z=>{
let x=L;
z.worte.forEach(o=>{
e.add(new fabric.Text(o.w,{left:x,top:y,originX:"left",originY:"center",
fontSize:gr,fontFamily:SERIF,fontStyle:o.kursiv?"italic":"normal",
fill:SCH,selectable:false,evented:false}));
x+=o.b+satz.abstand});
y+=gr*ZH});

e.add(new fabric.Text("carinaannaprav",{left:r/2,top:n*.905,originX:"center",originY:"center",
fontSize:c(17),fontFamily:SERIF,charSpacing:60,fill:ABS,selectable:false,evented:false}));
return true};
