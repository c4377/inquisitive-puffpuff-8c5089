"""Look „editorial“: jede Folie ist ein Foto, abgedunkelt, darauf Text wie im
Magazin-Karussell (Carinas Vorlage vom 5. Oktober): große Serif-Titel (Fraunces
Light), breite fette Versalien (Syne ExtraBold), schlichter Fließtext (Poppins),
Pfeil-Listen, handgezogene Unterstreichungen, senkrechter Trennstrich, Monogramm
oben rechts.

Aufruf: python3 tools/editorial-look.py <eingabe.js> <ausgabe.js> <version>
Die Eingabe ist das Ergebnis von tools/frech-look.py.

Textauszeichnung pro Folie (jede Zeile eine Rolle, Leerzeile = Absatz):
  # Titel            große Serif (auf dem Deckblatt sehr groß)
  ## Titel           mittlere Serif
  > TEXT             breite fette Versalien
  - Punkt / → Punkt  Pfeil-Aufzählung
  ! Satz             fetter Einleitungssatz
  |                  senkrechter Trennstrich
  [mitte] / [links]  Ausrichtung der Folie
  normaler Text      Fließtext; **fett**, *fett + unterstrichen*, __unterstrichen__
Ohne Auszeichnung teilt der Zeichner selbst auf (Deckblatt: Titel + kurze
Schlusszeile in Versalien; Folgefolien: erster Satz Serif, Rest Fließtext).
"""
import json, sys

A, Z, VERSION = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(A, encoding='utf-8').read()


def ersetze(alt, neu, anzahl=1):
    global s
    n = s.count(alt)
    if n != anzahl:
        sys.exit(f'{n}x statt {anzahl}x: {alt[:80]}')
    s = s.replace(alt, neu)


# Grundlage: der Frech-Look (Fotozuschnitt, Fotostil), alles andere hier drüber
i = s.index('"frech":{') + len('"frech":')
tiefe, j = 0, i
while True:
    if s[j] == '{': tiefe += 1
    elif s[j] == '}':
        tiefe -= 1
        if tiefe == 0: break
    j += 1
look = json.loads(s[i:j + 1])
SER, SANS, BREIT = 'Roxborough CF', 'Poppins', 'Syne Mag'  # Carinas eigene Lizenz (nur ihre App)
look.update({k: SER for k in ['fotoSchrift', 'deckblattFamilie', 'folgeFamilie', 'kastenSchrift', 'lisaSchrift',
                              'folgeSchrift', 'ablaufTitel', 'schriftart', 'unterSchrift']})
look.update({
    'magazin': 1, 'magSerif': SER, 'magSans': SANS, 'magBreit': BREIT, 'magMonogramm': 'cp', 'magCover': 'serif', 'magFeed': 'serif|kringel|flaeche|chat|pop|sticker|band|wortmix|durch|mitte|marker|zettel|zahl', 'magSticker': 'REAL TALK|15 JAHRE BÜHNE|SALES TALK|EHRLICH JETZT|KLAR TEXT', 'magDurchWorte': 'Ertappt.|Kenn ich.|Ups.|Same.|Echt jetzt?', 'magFlaeche': '#CEDF92', 'magFlaecheText': '#1E2B30', 'magFlaecheAkzent': '#3F6E78', 'magBand': 'rgba(18,16,15,0.86)', 'magCoverSerif': 'DMSerif Mag', 'magSerifGewicht': '400', 'magAkzent': '#CEDF92',
    'magDunkel': 0.2, 'magDunkelCover': 0.14, 'magAusrichtung': 'links',
    'versalFamilie': BREIT, 'versalAnteil': 0, 'fliessSchrift': SANS,
    # jede Folie bekommt ein Foto
    'textJede': 0, 'textAnteil': 0,
    # Fotos natürlich, leicht gedämpft, nicht so nah wie Kino
    'kino': 1, 'kinoSaettigung': 1.06, 'kinoHeben': 8, 'kinoKontrast': 1.04, 'kinoWarm': 0.04,
    'kinoSchwarz': 2, 'kinoWeiss': 252, 'kinoGamma': 0.88, 'kinoSplit': 1, 'kinoVignette': 0,
    'kinoBlauAnteil': 2, 'zuschnittZoom': 1.1,
})
AKZENTE = [('pfirsich', '#F6C8A8'), ('himmel', '#BFDDF0'), ('butter', '#F1E3B8')]
weitere = ''.join(',"editorial-' + k + '":' + json.dumps({**look, **v}, ensure_ascii=False, separators=(',', ':')) for k, v in [('b', {'magFeed': ''}), ('pop', {'magFeed': '', 'magCover': 'pop'})]) + ''.join(',"editorial-' + k + '":' + json.dumps({**look, 'magAkzent': f}, ensure_ascii=False, separators=(',', ':')) for k, f in AKZENTE)
ersetze('},"frech":', '},"editorial":' + json.dumps(look, ensure_ascii=False, separators=(',', ':')) + weitere + ',"frech":')

ZEICHNER = r'''if($e&&BS_KACHEL.magazin===1){const zFb=Pe.fabric,K=BS_KACHEL,zW=r,zH=n;
const SER=K.magSerif||"Fraunces Mag",HAND=K.magHand||"CaveatV3",CSER=K.magCoverSerif||SER,SW=String(K.magSerifGewicht||"300"),SANS=K.magSans||"Poppins",WIDE=K.magBreit||"Syne Mag";
try{await Promise.race([Promise.all([`${SW} 40px "${SER}"`,`400 40px "${CSER}"`,`700 40px "${HAND}"`,`400 40px "${SANS}"`,`600 40px "${SANS}"`,`800 40px "${WIDE}"`,`italic 300 40px "Fraunces Mag"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,5e3))])}catch(zz){}
const zNo={selectable:!1,evented:!1};let AK=K.magAkzent||"#FFFFFF",TXT="#FFFFFF";
const zD=((i&&i.slideIndex)||0)===0?(K.magDunkelCover==null?.06:K.magDunkelCover):(K.magDunkel==null?.2:K.magDunkel);e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:`rgba(0,0,0,${zD})`,...zNo}));
e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,...zNo,fill:new zFb.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:zH},colorStops:[{offset:0,color:"rgba(0,0,0,0.08)"},{offset:.22,color:"rgba(0,0,0,0)"},{offset:.5,color:"rgba(0,0,0,0.04)"},{offset:1,color:`rgba(0,0,0,${((i&&i.slideIndex)||0)===0?.58:.3})`}]})}));
const zCx=document.createElement("canvas").getContext("2d");
const zMs=(zs,zf,zfs,zcs)=>{zCx.font=zf;return zCx.measureText(zs).width+String(zs).length*(zcs||0)*zfs/1e3};
const zCover=((i&&i.slideIndex)||0)===0;
const ST={strike:{fam:CSER,w:"400",fs:.075,lh:1.1,cs:-10,max:3,min:.05},bl:{fam:SANS,w:"400",fs:.042,lh:1.3,cs:0,bub:1},br:{fam:SANS,w:"600",fs:.042,lh:1.3,cs:0,bub:1},zahl:{fam:WIDE,w:"800",fs:.34,lh:.92,cs:-30,max:1,min:.12},wm1:{fam:"Fraunces Mag",w:"300",fs:.13,lh:1.0,cs:-10,max:2,min:.07,it:1},wm2:{fam:CSER,w:"400",fs:.075,lh:1.05,cs:-10,max:3,min:.05},wm3:{fam:WIDE,w:"800",fs:.24,lh:.95,cs:-10,max:1,min:.06,up:1},hand:{fam:HAND,w:"700",fs:.095,lh:.98,cs:0,max:3,min:.062},h1:{fam:SER,w:SW,fs:.15,lh:.93,cs:-20,max:5,min:.085},h2:{fam:SER,w:SW,fs:.08,lh:1.02,cs:-15,max:5},caps:{fam:WIDE,w:"800",fs:.043,lh:1.45,cs:20,up:1},lead:{fam:SANS,w:"600",fs:.035,lh:1.5,cs:0},body:{fam:SANS,w:"400",fs:.035,lh:1.55,cs:0},li:{fam:SANS,w:"400",fs:.036,lh:1.45,cs:0}};
const zFR=String(K.magFeed||"").split("|").filter(Boolean),zTyp0=zFR.length?zFR[((Number(t._tag)||0)%zFR.length+zFR.length)%zFR.length]:"",zTyp={kringel:"serif",durch:"serif",sticker:"serif",zettel:"serif",wortmix:"serif",marker:"pop",chat:"pop",zahl:"pop"}[zTyp0]||zTyp0;let zGim=zCover?zTyp0:"";const zStil=zTyp?(zTyp==="pop"?"pop":"serif"):K.magCover==="pop"||(K.magCover==="wechsel"&&(Number(t._tag)||0)%2===1)?"pop":"serif";if(zStil==="pop")ST.h1={fam:SANS,w:"600",fs:.105,lh:1.04,cs:-25,max:5,min:.075,pop:1};else if(K.magCoverSerif)ST.h1={...ST.h1,fam:CSER,w:String(K.magCoverSerifGewicht||"400"),fs:.13,lh:.98,cs:-10};if(zTyp==="band")ST.h1={...ST.h1,fam:SER,w:SW,fs:.105,lh:1.0,cs:-15,pop:0};if(!zCover){const zH2=zTyp||zStil;if(zH2==="pop")ST.h2={fam:SANS,w:"600",fs:.068,lh:1.08,cs:-20,max:5};else if(zH2!=="band"&&K.magCoverSerif)ST.h2={...ST.h2,fam:CSER,w:String(K.magCoverSerifGewicht||"400"),cs:-10}}if(zTyp==="band")e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:K.magBand||"rgba(18,16,15,0.86)",...zNo}));if(zTyp==="mitte")e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"rgba(0,0,0,0.24)",...zNo}));if(zTyp==="flaeche"){e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:K.magFlaeche||"#CEDF92",...zNo}));TXT=K.magFlaecheText||"#1E2B30";AK=K.magFlaecheAkzent||"#3F6E78"}
const zRuns=zs=>{const zo=[];let zb=!1,zu=!1,zc="";const zp=()=>{zc&&zo.push({t:zc,b:zb||zu,u:zu});zc=""};for(let k=0;k<zs.length;k++){const ch=zs[k];if(ch==="*"&&zs[k+1]==="*"){zp();zb=!zb;k++;continue}if(ch==="_"&&zs[k+1]==="_"){zp();zu=!zu;k++;continue}if(ch==="*"){zp();zu=!zu;continue}zc+=ch}zp();return zo};
const zSaetze=zx=>{const zr=[];let za="";String(zx||"").split(/\s+/).filter(Boolean).forEach(zw=>{za=za?za+" "+zw:zw;if(/[.!?:…]["»”)’]?$/.test(zw)){zr.push(za);za=""}});za&&zr.push(za);return zr};
let zAus=zTyp==="mitte"?"mitte":(K.magAusrichtung||"links");const zBl=[];
const zRoh=String(t.text||"").replace(/\r/g,"");const zZl=zRoh.split("\n");
const zMark=zZl.some(zq=>/^\s*(#{1,2}\s|>\s|[-•→]\s|->\s|!\s|~\s|\|\s*$|\[(mitte|links)\]\s*$)/i.test(zq));
if(zMark){zZl.forEach(zq=>{const z=zq.trim();if(!z){zBl.push({k:"gap"});return}let m;
if(/^\[mitte\]$/i.test(z)){zAus="mitte";return}if(/^\[links\]$/i.test(z)){zAus="links";return}
if(m=/^##\s+(.*)$/.exec(z))return zBl.push({k:"h2",s:m[1]});if(m=/^#\s+(.*)$/.exec(z))return zBl.push({k:zCover?"h1":"h2",s:m[1]});
if(m=/^>\s+(.*)$/.exec(z))return zBl.push({k:"caps",s:m[1]});if(m=/^(?:[-•→]|->)\s+(.*)$/.exec(z))return zBl.push({k:"li",s:m[1]});
if(m=/^~\s+(.*)$/.exec(z))return zBl.push({k:"hand",s:m[1]});if(m=/^!\s+(.*)$/.exec(z))return zBl.push({k:"lead",s:m[1]});if(/^\|$/.test(z))return zBl.push({k:"div"});zBl.push({k:"body",s:z})})}
else{const zP=zRoh.split(/\n/).map(zq=>zq.trim()).filter(Boolean);
if(zCover){const zAll=zP.join(" "),zS=zSaetze(zAll);let zh=zS[0]||"",zr=zS.slice(1),zHand="";if(zh.replace(/\*/g,"").length>50){let zc=-1;const zIn=zx=>{const zv=zh.slice(0,zx);return(zv.match(/[\u201e\u00bb]/g)||[]).length>(zv.match(/[\u201c\u201d\u00ab]/g)||[]).length||((zv.match(/"/g)||[]).length%2===1)};const zk=zh.indexOf(", ",15);if(zk>0&&zk<=60&&!zIn(zk))zc=zk;else{const zm=/\s(und|oder|weil|aber|statt|bis|wenn|obwohl|damit|während|nachdem|sobald)\s/g;let zq;while((zq=zm.exec(zh))){if(zq.index>=18&&zq.index<=60&&!zIn(zq.index)){zc=zq.index;break}}}if(zc>0){zHand=zh.slice(zc).replace(/^[,\s]+/,"");zh=zh.slice(0,zc)}}if(!zHand&&zr.length&&zr[0].replace(/\*/g,"").length<=70)zHand=zr.shift();zBl.push({k:"h1",s:zh});zHand&&zBl.push({k:"hand",s:zHand});zr.length&&zBl.push({k:"body",s:zr.join(" ")})}
else if(zP.length>1){zBl.push({k:zP[0].length>110?"body":"h2",s:zP[0]});zP.slice(1).forEach(zq=>/^\d+[.)]\s+/.test(zq)?zBl.push({k:"li",s:zq.replace(/^\d+[.)]\s+/,"")}):zBl.push({k:"body",s:zq}))}
else{const zS=zSaetze(zP[0]||"");if(zS.length<2||(zS[0]||"").length>110)zBl.push({k:(zP[0]||"").length>140?"body":"h2",s:zP[0]||""});else{zBl.push({k:"h2",s:zS[0]});zBl.push({k:"body",s:zS.slice(1).join(" ")})}}}
while(zBl.length&&zBl[zBl.length-1].k==="gap")zBl.pop();while(zBl.length&&zBl[0].k==="gap")zBl.shift();let zGimZettel="";
const zWahl=(zl,zd)=>{const zq=String(zl||"").split("|").filter(Boolean);return zq.length?zq[((Number(t._tag)||0)%zq.length+zq.length)%zq.length]:zd};
if(zGim&&!zMark){const zI1=zBl.findIndex(zq=>zq.k==="h1"),zIH=zBl.findIndex(zq=>zq.k==="hand");
if(zGim==="zahl"){const zS=zSaetze(zRoh.replace(/\n/g," ")),zIx=zS.findIndex(zq=>/\d/.test(zq));if(zIx<0)zGim="kringel";else{const zm=/\d[\d.,]*(?:\s?(?:%|€|Euro|k))?/.exec(zS[zIx]),zv=zS[zIx].slice(0,zm.index).trim(),zn=zS[zIx].slice(zm.index+zm[0].length).replace(/[.!?:]+$/,"").trim(),zh=zS.slice(zIx+1).find(zq=>zq.length<=70)||"";zBl.length=0;zv&&zBl.push({k:"lead",s:zv});zBl.push({k:"zahl",s:zm[0]});zn&&zBl.push({k:"caps",s:zn.length>34?zn.slice(0,zn.lastIndexOf(" ",34))+" …":zn});zh&&zBl.push({k:"hand",s:zh})}}
if((zGim==="durch"||zGim==="zettel")&&zIH<0)zGim="kringel";
if(zGim==="durch"){zBl[zIH].k="strike";zBl.splice(zIH,0,{k:"hand",s:zWahl(K.magDurchWorte,"Ertappt."),kom:1})}
if(zGim==="zettel"){zGimZettel=zBl[zIH].s;zBl.splice(zIH,1)}
if(zGim==="chat"&&zI1>=0){zBl[zI1].k="bl";zIH>=0&&(zBl[zIH].k="br")}
if(zGim==="wortmix"&&zI1>=0){const zw=String(zBl[zI1].s).replace(/\*+/g,"").trim().split(/\s+/);const zn=[];zw.length>1&&zn.push({k:"wm1",s:zw[0]});zw.length>2&&zn.push({k:"wm2",s:zw.slice(1,-1).join(" ")});zn.push({k:"wm3",s:zw[zw.length-1]});zBl.splice(zI1,1,...zn)}}

const L=zW*.1,MAXW=zW*(zCover?.84:.8),LI=zW*.105;
const zWrap=(zruns,st,fs,mw)=>{const zws=[];zruns.forEach(ru=>String(ru.t).split(/(\s+)/).forEach(zw=>{zw&&zws.push({t:zw,b:ru.b,u:ru.u,c:ru.c,sp:/^\s+$/.test(zw)})}));
const zf=zb=>`${st.it?"italic ":""}${zb&&st.fam===SANS?"600":st.w} ${fs}px "${st.fam}"`;const zl=[];let zc=[],zcw=0;
const zend=()=>{while(zc.length&&zc[zc.length-1].sp)zcw-=zc.pop().w;zc.length&&zl.push({segs:zc,w:zcw});zc=[];zcw=0};
zws.forEach(zd=>{const zw=zMs(zd.t,zf(zd.b),fs,st.cs);if(zd.sp){zc.length&&(zc.push({...zd,w:zw}),zcw+=zw);return}if(zcw+zw>mw&&zc.length)zend();zc.push({...zd,w:zw});zcw+=zw});zend();return zl};
zBl.forEach((zb,zx)=>{zb.k==="caps"&&((zBl[zx-1]||{}).k==="caps"||(zBl[zx+1]||{}).k==="caps")&&(zb.reihe=1)});let zK=1;const zBau0=()=>zBl.map(zb=>{if(zb.k==="gap"||zb.k==="div")return{...zb,h:zb.k==="div"?zH*.095:zH*.012,lines:[]};const st=ST[zb.k];let fs=zW*st.fs*zK;
let txt=String(zb.s||"");if(st.fam!==SANS||zb.k==="h1")txt=txt.replace(/\*+|__/g,"");if(st.up)txt=txt.toLocaleUpperCase("de-DE");
const zr=st.fam===SANS?zRuns(txt):[{t:txt,b:!1,u:!1}];if(zGim==="marker"&&zb.k==="h1"&&zr.length){const zt=zr.map(zq=>zq.t).join("").trim(),zw=zt.split(/\s+/);let zn=1;while(zn<zw.length-1&&zw.slice(-zn).join(" ").length<12)zn++;const zA0=zw.slice(0,-zn).join(" "),zA1=zw.slice(-zn).join(" ");zr.length=0;zA0&&zr.push({t:zA0+" ",b:!1,u:!1});zr.push({t:zA1,b:!1,u:!1,c:1})}else if(st.pop&&zr.length&&!zBl.some(zq=>zq.k==="hand")){const zl0=zr[zr.length-1],zi=zl0.t.trimEnd().lastIndexOf(" ");zi>0?zr.splice(zr.length-1,1,{...zl0,t:zl0.t.slice(0,zi+1)},{...zl0,t:zl0.t.slice(zi+1),c:1}):(zl0.c=1)}const mw=zb.k==="li"?MAXW-LI:st.bub?zW*.6:zb.k==="strike"?MAXW*.92:MAXW;let lines=zWrap(zr,st,fs,mw);
if(st.max)for(let k=0;k<40&&(lines.length>st.max||lines.some(zl=>zl.w>mw))&&!(st.min&&fs<=zW*st.min*zK&&!lines.some(zl=>zl.w>mw));k++){fs*=.94;lines=zWrap(zr,st,fs,mw)}if(zb.reihe)for(let k=0;k<20&&lines.length>1&&fs>zW*.03;k++){fs*=.95;lines=zWrap(zr,st,fs,mw)}
return{...zb,st,fs,lines,h:lines.length*fs*st.lh+(st.bub?fs*1.2:0)}});const zBau=()=>{const zb0=zBau0();const zm=Math.min(...zb0.filter(zq=>zq.reihe).map(zq=>zq.fs),1e9);return zm<1e9?zb0.map(zq=>{if(!zq.reihe||zq.fs===zm)return zq;const lines=zWrap([{t:String(zq.s).replace(/\*+|__/g,"").toLocaleUpperCase("de-DE"),b:!1,u:!1}],zq.st,zm,MAXW);return{...zq,fs:zm,lines,h:lines.length*zm*zq.st.lh}}):zb0};
const zGap=(za,zb)=>za.st&&za.st.bub&&zb.st&&zb.st.bub?zH*.014:/^wm/.test(za.k)&&/^wm/.test(zb.k)?zH*.004:za.k==="hand"&&za.kom?zH*.004:za.k==="zahl"?zH*.012:za.k==="lead"&&zb.k==="zahl"?zH*.004:za.k==="h1"&&zb.k==="hand"?zH*.014:za.k==="hand"?zH*.026:za.k==="caps"&&zb.k==="caps"?zH*.008:za.k==="li"&&zb.k==="li"?zH*.026:zb.k==="div"||za.k==="div"?zH*.03:za.k==="h1"?zH*.03:za.k==="h2"?zH*.038:za.k==="caps"?zH*.03:za.k==="lead"?zH*.02:zH*.028;
let zB=zBau(),zT=0;const zSum=()=>{zT=zB.reduce((za,zb,zx)=>za+zb.h+(zx<zB.length-1?zGap(zb,zB[zx+1]):0),0)};zSum();
for(let k=0;k<30&&zT>zH*.74&&zK>.72;k++){zK*=.94;zB=zBau();zSum()}
let y=zCover?(zTyp==="mitte"||zTyp==="flaeche"||zTyp==="band"?Math.max(zH*.14,zH*.53-zT/2):Math.max(zH*.14,zH*(zTyp==="band"?.9:.86)-zT)):Math.max(zH*.14,zH*.56-zT/2);zCover&&zTyp==="mitte"&&e.add(new zFb.Line([zW/2-zW*.05,y-zH*.045,zW/2+zW*.05,y-zH*.045],{stroke:AK,strokeWidth:Math.max(2,zW*.004),...zNo}));
let zLW=null,zHY=null;const zDurch=[];let zSch=new zFb.Shadow({color:zCover?"rgba(0,0,0,0.42)":"rgba(0,0,0,0.28)",blur:zW*(zCover?.018:.012),offsetX:0,offsetY:0});zTyp==="flaeche"&&(zSch=void 0);
const zStrich=(x1,x2,yy,fs)=>{let zh=0;const zs=String(t.text||"")+x1;for(let k=0;k<zs.length;k++)zh=(zh*31+zs.charCodeAt(k))%9973;const zj=k=>((zh*(k+3))%7-3)/3*fs*.035;const sw=Math.max(1.5,zW*.0032);
e.add(new zFb.Path(`M ${x1} ${yy+zj(1)} Q ${(x1+x2)/2} ${yy+zj(2)+fs*.03} ${x2} ${yy+zj(3)}`,{fill:"",stroke:AK,strokeWidth:sw,strokeLineCap:"round",...zNo}));
e.add(new zFb.Path(`M ${x1+fs*.15} ${yy+fs*.09+zj(4)} Q ${(x1+x2)/2} ${yy+fs*.06+zj(5)} ${x2-fs*.1} ${yy+fs*.1+zj(6)}`,{fill:"",stroke:AK,strokeWidth:sw*.6,strokeLineCap:"round",opacity:.85,...zNo}))};
zB.forEach((zb,zx)=>{if(zb.k==="div"){const xx=zAus==="mitte"?zW/2:L+zW*.01;e.add(new zFb.Line([xx,y,xx,y+zb.h],{stroke:AK,strokeWidth:Math.max(1.5,zW*.0025),...zNo}))}
else if(zb.lines.length){const st=zb.st,fs=zb.fs,lh=fs*st.lh,zPad=st.bub?fs*.6:0,zBw=st.bub?Math.max(...zb.lines.map(zq=>zq.w))+2*zPad:0,zBx=zb.k==="br"?zW-L-zBw:L;st.bub&&e.add(new zFb.Rect({left:zBx,top:y,width:zBw,height:zb.h,rx:fs*.75,ry:fs*.75,fill:zb.k==="br"?AK:"rgba(255,255,255,0.94)",shadow:new zFb.Shadow({color:"rgba(0,0,0,0.18)",blur:zW*.012,offsetX:0,offsetY:zW*.003}),...zNo}));zb.lines.forEach((zl,zi)=>{const yc=y+zPad+lh*zi+lh/2;const x0=st.bub?zBx+zPad:zb.k==="li"?L+LI:zb.k==="hand"&&zb.kom?L+zW*.32:zAus==="mitte"?(zW-zl.w)/2:L;if(zb.k==="h1"&&zi===zb.lines.length-1){const zLt=zl.segs.map(zq=>zq.t).join("").trim(),zLw=zLt.split(/\s+/).pop();const zWw=zMs(zLw,`${st.w} ${fs}px "${st.fam}"`,fs,st.cs);zLW={x:x0+zl.w-zWw,w:zWw,yc,fs}}if(zb.k==="hand"&&zi===0)zHY={x:x0,yc,fs};if(zb.k==="strike"){const zy0=yc+fs*.02,zj=((zi*7+3)%5-2)*fs*.04;zDurch.push(`M ${x0-fs*.15} ${zy0+zj} C ${x0+zl.w*.3} ${zy0-fs*.08}, ${x0+zl.w*.65} ${zy0+fs*.1}, ${x0+zl.w+fs*.15} ${zy0-zj}`)}
if(zb.k==="li"&&zi===0){const ax=L,aw=zW*.058,sw=Math.max(1.5,zW*.0032);e.add(new zFb.Line([ax,yc,ax+aw,yc],{stroke:AK,strokeWidth:sw,strokeLineCap:"round",...zNo}));e.add(new zFb.Polyline([{x:ax+aw-fs*.32,y:yc-fs*.22},{x:ax+aw,y:yc},{x:ax+aw-fs*.32,y:yc+fs*.22}],{fill:"",stroke:AK,strokeWidth:sw,strokeLineCap:"round",strokeLineJoin:"round",...zNo}))}
let xx=x0;const zg=[];zl.segs.forEach(sg=>{const zq=zg[zg.length-1];zq&&zq.b===sg.b&&zq.u===sg.u&&zq.c===sg.c?(zq.t+=sg.t,zq.w+=sg.w):zg.push({...sg})});
zg.forEach(sg=>{const zMk=zGim==="marker"&&zb.k==="h1"&&sg.c,zDk=st.bub||zMk;zMk&&e.add(new zFb.Rect({left:xx-fs*.12,top:yc-fs*.56,width:sg.w-zMs((/\s+$/.exec(sg.t)||[""])[0],`${st.w} ${fs}px "${st.fam}"`,fs,st.cs)+fs*.24,height:fs*1.1,rx:fs*.14,ry:fs*.14,angle:-1,fill:AK,...zNo}));e.add(new zFb.Text(sg.t,{left:xx,top:yc,originX:"left",originY:"center",fontFamily:st.fam,fontWeight:sg.b&&st.fam===SANS?"600":st.w,fontStyle:st.it?"italic":"normal",fontSize:fs,charSpacing:st.cs||0,fill:zb.k==="zahl"?"":zDk?"#1E2B30":(sg.c||zb.k==="caps"||zb.k==="hand"||zb.k==="wm3")?AK:TXT,stroke:zb.k==="zahl"?TXT:void 0,strokeWidth:zb.k==="zahl"?Math.max(2,zW*.004):0,opacity:zb.k==="strike"?.88:1,angle:zb.k==="hand"?(zb.kom?-7:-3):0,shadow:zDk||zb.k==="zahl"?void 0:zSch,...zNo}));
if(sg.u){const tw=sg.w-zMs((/\s+$/.exec(sg.t)||[""])[0],`600 ${fs}px "${st.fam}"`,fs,0);zStrich(xx,xx+tw,yc+fs*.62,fs)}xx+=sg.w})})}
y+=zb.h+(zx<zB.length-1?zGap(zb,zB[zx+1]):0)});
zDurch.forEach(zd=>e.add(new zFb.Path(zd,{fill:"",stroke:AK,strokeWidth:Math.max(3,zW*.0055),strokeLineCap:"round",...zNo})));if(zGim==="kringel"&&zLW){const zs=zLW.fs,cx=zLW.x+zLW.w/2,rx=zLW.w/2+zs*.28,ry=zs*.58,sw=Math.max(2,zW*.0042);e.add(new zFb.Path(`M ${cx-rx*.9} ${zLW.yc+ry*.2} C ${cx-rx*1.05} ${zLW.yc-ry*1.1}, ${cx+rx*.7} ${zLW.yc-ry*1.25}, ${cx+rx} ${zLW.yc-ry*.2} C ${cx+rx*1.2} ${zLW.yc+ry*.9}, ${cx-rx*.2} ${zLW.yc+ry*1.15}, ${cx-rx*.85} ${zLW.yc+ry*.75} C ${cx-rx*1.1} ${zLW.yc+ry*.5}, ${cx-rx*1.0} ${zLW.yc-ry*.6}, ${cx-rx*.55} ${zLW.yc-ry*.85}`,{fill:"",stroke:AK,strokeWidth:sw,strokeLineCap:"round",...zNo}));
if(zHY){const ax=cx-rx*.3,ay=zLW.yc+ry*1.2,bx=Math.max(zHY.x+zHY.fs*2.2,ax+zW*.02),by=zHY.yc-zHY.fs*.75;e.add(new zFb.Path(`M ${ax} ${ay} Q ${ax-zW*.01} ${(ay+by)/2+zW*.02} ${bx} ${by}`,{fill:"",stroke:AK,strokeWidth:sw*.85,strokeLineCap:"round",...zNo}));e.add(new zFb.Polyline([{x:bx-zW*.025,y:by-zW*.008},{x:bx,y:by},{x:bx-zW*.012,y:by+zW*.022}],{fill:"",stroke:AK,strokeWidth:sw*.85,strokeLineCap:"round",strokeLineJoin:"round",...zNo}))}}
const zFbx=t._zBox,zLinks=!!(zFbx&&typeof zFbx.x0==="number"&&(zFbx.x0+zFbx.x1)/2>.55);
if(zGim==="sticker"){const zr2=zW*.15,zcx=zLinks?zW*.22:zW*.78,zcy=zH*.3;e.add(new zFb.Circle({left:zcx,top:zcy,radius:zr2,originX:"center",originY:"center",fill:AK,shadow:new zFb.Shadow({color:"rgba(0,0,0,0.3)",blur:zW*.02,offsetX:0,offsetY:zW*.006}),...zNo}));e.add(new zFb.Text(zWahl(K.magSticker,"REAL TALK").split(" ").join("\n"),{left:zcx,top:zcy,originX:"center",originY:"center",textAlign:"center",fontFamily:WIDE,fontWeight:"800",fontSize:zW*.04,lineHeight:.95,charSpacing:20,fill:"#1E2B30",angle:-14,...zNo}))}
if(zGim==="zettel"&&zGimZettel){const zbw=zW*.48,zfs=zW*.07,zcx=zLinks?zW*.3:zW*.7,zcy=zH*.3,ztb=new zFb.Textbox(zGimZettel,{width:zbw-zW*.07,fontFamily:HAND,fontWeight:"700",fontSize:zfs,lineHeight:.98,fill:"#1E2B30",textAlign:"left",originX:"center",originY:"center",left:zcx,top:zcy,angle:4,...zNo});const zbh=(ztb.height||zfs*3)+zW*.08;e.add(new zFb.Rect({left:zcx,top:zcy,width:zbw,height:zbh,originX:"center",originY:"center",angle:4,fill:"#FBF8F1",shadow:new zFb.Shadow({color:"rgba(0,0,0,0.3)",blur:zW*.025,offsetX:0,offsetY:zW*.008}),...zNo}));e.add(ztb);e.add(new zFb.Rect({left:zcx+Math.sin(4*Math.PI/180)*zbh/2,top:zcy-Math.cos(4*Math.PI/180)*zbh/2,width:zW*.13,height:zW*.04,originX:"center",originY:"center",angle:-4,fill:AK,opacity:.88,...zNo}))}
K.magMonogramm&&e.add(new zFb.Text(String(K.magMonogramm),{left:zW*.905,top:zH*.105,originX:"right",originY:"center",fontFamily:SER,fontWeight:SW,fontSize:zW*.095,charSpacing:-40,fill:TXT,shadow:zSch,...zNo}));
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}'''
ANKER = 'if($e&&(t.karte==="ablauf"||t.reminderArt==="ablauf")){const Ab=T1('
ersetze(ANKER, ZEICHNER.replace('\n', '') + ANKER)
ersetze('title:"Geladene Datei",children:"karten451"', f'title:"Geladene Datei",children:"karten{VERSION}"')
open(Z, 'w', encoding='utf-8').write(s)
print('ok')
