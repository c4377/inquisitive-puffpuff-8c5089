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
SER, SANS, BREIT = 'Fraunces Mag', 'Poppins', 'Syne Mag'
look.update({k: SER for k in ['fotoSchrift', 'deckblattFamilie', 'folgeFamilie', 'kastenSchrift', 'lisaSchrift',
                              'folgeSchrift', 'ablaufTitel', 'schriftart', 'unterSchrift']})
look.update({
    'magazin': 1, 'magSerif': SER, 'magSans': SANS, 'magBreit': BREIT, 'magMonogramm': 'cp',
    'magDunkel': 0.2, 'magDunkelCover': 0.06, 'magAusrichtung': 'links',
    'versalFamilie': BREIT, 'versalAnteil': 0, 'fliessSchrift': SANS,
    # jede Folie bekommt ein Foto
    'textJede': 0, 'textAnteil': 0,
    # Fotos natürlich, leicht gedämpft, nicht so nah wie Kino
    'kino': 1, 'kinoSaettigung': 0.92, 'kinoHeben': 8, 'kinoKontrast': 1.04, 'kinoWarm': 0.15,
    'kinoSchwarz': 2, 'kinoWeiss': 252, 'kinoGamma': 0.88, 'kinoSplit': 1, 'kinoVignette': 0.1,
    'kinoBlauAnteil': 2, 'zuschnittZoom': 1.1,
})
ersetze('},"frech":', '},"editorial":' + json.dumps(look, ensure_ascii=False, separators=(',', ':')) + ',"frech":')

ZEICHNER = r'''if($e&&BS_KACHEL.magazin===1){const zFb=Pe.fabric,K=BS_KACHEL,zW=r,zH=n;
const SER=K.magSerif||"Fraunces Mag",SANS=K.magSans||"Poppins",WIDE=K.magBreit||"Syne Mag";
try{await Promise.race([Promise.all([`300 40px "${SER}"`,`400 40px "${SANS}"`,`600 40px "${SANS}"`,`800 40px "${WIDE}"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,5e3))])}catch(zz){}
const zNo={selectable:!1,evented:!1};
const zD=((i&&i.slideIndex)||0)===0?(K.magDunkelCover==null?.06:K.magDunkelCover):(K.magDunkel==null?.2:K.magDunkel);e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:`rgba(0,0,0,${zD})`,...zNo}));
e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,...zNo,fill:new zFb.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:zH},colorStops:[{offset:0,color:"rgba(0,0,0,0.12)"},{offset:.22,color:"rgba(0,0,0,0)"},{offset:.5,color:"rgba(0,0,0,0.04)"},{offset:1,color:`rgba(0,0,0,${((i&&i.slideIndex)||0)===0?.5:.3})`}]})}));
const zCx=document.createElement("canvas").getContext("2d");
const zMs=(zs,zf,zfs,zcs)=>{zCx.font=zf;return zCx.measureText(zs).width+String(zs).length*(zcs||0)*zfs/1e3};
const zCover=((i&&i.slideIndex)||0)===0;
const ST={h1:{fam:SER,w:"300",fs:.145,lh:.98,cs:-20,max:5,min:.085},h2:{fam:SER,w:"300",fs:.08,lh:1.05,cs:-15,max:5},caps:{fam:WIDE,w:"800",fs:.043,lh:1.45,cs:20,up:1},lead:{fam:SANS,w:"600",fs:.035,lh:1.5,cs:0},body:{fam:SANS,w:"400",fs:.035,lh:1.55,cs:0},li:{fam:SANS,w:"400",fs:.036,lh:1.45,cs:0}};
const zRuns=zs=>{const zo=[];let zb=!1,zu=!1,zc="";const zp=()=>{zc&&zo.push({t:zc,b:zb||zu,u:zu});zc=""};for(let k=0;k<zs.length;k++){const ch=zs[k];if(ch==="*"&&zs[k+1]==="*"){zp();zb=!zb;k++;continue}if(ch==="_"&&zs[k+1]==="_"){zp();zu=!zu;k++;continue}if(ch==="*"){zp();zu=!zu;continue}zc+=ch}zp();return zo};
const zSaetze=zx=>{const zr=[];let za="";String(zx||"").split(/\s+/).filter(Boolean).forEach(zw=>{za=za?za+" "+zw:zw;if(/[.!?:…]["»”)’]?$/.test(zw)){zr.push(za);za=""}});za&&zr.push(za);return zr};
let zAus=K.magAusrichtung||"links";const zBl=[];
const zRoh=String(t.text||"").replace(/\r/g,"");const zZl=zRoh.split("\n");
const zMark=zZl.some(zq=>/^\s*(#{1,2}\s|>\s|[-•→]\s|->\s|!\s|\|\s*$|\[(mitte|links)\]\s*$)/i.test(zq));
if(zMark){zZl.forEach(zq=>{const z=zq.trim();if(!z){zBl.push({k:"gap"});return}let m;
if(/^\[mitte\]$/i.test(z)){zAus="mitte";return}if(/^\[links\]$/i.test(z)){zAus="links";return}
if(m=/^##\s+(.*)$/.exec(z))return zBl.push({k:"h2",s:m[1]});if(m=/^#\s+(.*)$/.exec(z))return zBl.push({k:zCover?"h1":"h2",s:m[1]});
if(m=/^>\s+(.*)$/.exec(z))return zBl.push({k:"caps",s:m[1]});if(m=/^(?:[-•→]|->)\s+(.*)$/.exec(z))return zBl.push({k:"li",s:m[1]});
if(m=/^!\s+(.*)$/.exec(z))return zBl.push({k:"lead",s:m[1]});if(/^\|$/.test(z))return zBl.push({k:"div"});zBl.push({k:"body",s:z})})}
else{const zP=zRoh.split(/\n/).map(zq=>zq.trim()).filter(Boolean);
if(zCover){const zAll=zP.join(" "),zS=zSaetze(zAll),zL=(zS[zS.length-1]||"").replace(/\*/g,"");if(zAll.replace(/\*/g,"").length<=70&&!(zS.length>1&&zL.length<=48))zBl.push({k:"h1",s:zAll});else{let zh=zS[0]||"",zr=zS.slice(1);if(zh.length>90){const zc=zh.indexOf(",",30);if(zc>0&&zc<90){zr=[zh.slice(zc+1).trim(),...zr];zh=zh.slice(0,zc+1)}}zBl.push({k:"h1",s:zh});let zcap="";zr.length&&zr[zr.length-1].replace(/\*/g,"").length<=48&&(zcap=zr.pop());zr.length&&zBl.push({k:"body",s:zr.join(" ")});zcap&&zBl.push({k:"caps",s:zcap})}}
else if(zP.length>1){zBl.push({k:zP[0].length>110?"body":"h2",s:zP[0]});zP.slice(1).forEach(zq=>/^\d+[.)]\s+/.test(zq)?zBl.push({k:"li",s:zq.replace(/^\d+[.)]\s+/,"")}):zBl.push({k:"body",s:zq}))}
else{const zS=zSaetze(zP[0]||"");if(zS.length<2||(zS[0]||"").length>110)zBl.push({k:(zP[0]||"").length>140?"body":"h2",s:zP[0]||""});else{zBl.push({k:"h2",s:zS[0]});zBl.push({k:"body",s:zS.slice(1).join(" ")})}}}
while(zBl.length&&zBl[zBl.length-1].k==="gap")zBl.pop();while(zBl.length&&zBl[0].k==="gap")zBl.shift();
const L=zW*.1,MAXW=zW*(zCover?.84:.8),LI=zW*.105;
const zWrap=(zruns,st,fs,mw)=>{const zws=[];zruns.forEach(ru=>String(ru.t).split(/(\s+)/).forEach(zw=>{zw&&zws.push({t:zw,b:ru.b,u:ru.u,sp:/^\s+$/.test(zw)})}));
const zf=zb=>`${zb&&st.fam===SANS?"600":st.w} ${fs}px "${st.fam}"`;const zl=[];let zc=[],zcw=0;
const zend=()=>{while(zc.length&&zc[zc.length-1].sp)zcw-=zc.pop().w;zc.length&&zl.push({segs:zc,w:zcw});zc=[];zcw=0};
zws.forEach(zd=>{const zw=zMs(zd.t,zf(zd.b),fs,st.cs);if(zd.sp){zc.length&&(zc.push({...zd,w:zw}),zcw+=zw);return}if(zcw+zw>mw&&zc.length)zend();zc.push({...zd,w:zw});zcw+=zw});zend();return zl};
zBl.forEach((zb,zx)=>{zb.k==="caps"&&((zBl[zx-1]||{}).k==="caps"||(zBl[zx+1]||{}).k==="caps")&&(zb.reihe=1)});let zK=1;const zBau0=()=>zBl.map(zb=>{if(zb.k==="gap"||zb.k==="div")return{...zb,h:zb.k==="div"?zH*.095:zH*.012,lines:[]};const st=ST[zb.k];let fs=zW*st.fs*zK;
let txt=String(zb.s||"");if(st.fam!==SANS)txt=txt.replace(/\*+|__/g,"");if(st.up)txt=txt.toLocaleUpperCase("de-DE");
const zr=st.fam===SANS?zRuns(txt):[{t:txt,b:!1,u:!1}];const mw=zb.k==="li"?MAXW-LI:MAXW;let lines=zWrap(zr,st,fs,mw);
if(st.max)for(let k=0;k<40&&(lines.length>st.max||lines.some(zl=>zl.w>mw))&&!(st.min&&fs<=zW*st.min*zK&&!lines.some(zl=>zl.w>mw));k++){fs*=.94;lines=zWrap(zr,st,fs,mw)}if(zb.reihe)for(let k=0;k<20&&lines.length>1&&fs>zW*.03;k++){fs*=.95;lines=zWrap(zr,st,fs,mw)}
return{...zb,st,fs,lines,h:lines.length*fs*st.lh}});const zBau=()=>{const zb0=zBau0();const zm=Math.min(...zb0.filter(zq=>zq.reihe).map(zq=>zq.fs),1e9);return zm<1e9?zb0.map(zq=>{if(!zq.reihe||zq.fs===zm)return zq;const lines=zWrap([{t:String(zq.s).replace(/\*+|__/g,"").toLocaleUpperCase("de-DE"),b:!1,u:!1}],zq.st,zm,MAXW);return{...zq,fs:zm,lines,h:lines.length*zm*zq.st.lh}}):zb0};
const zGap=(za,zb)=>za.k==="caps"&&zb.k==="caps"?zH*.008:za.k==="li"&&zb.k==="li"?zH*.026:zb.k==="div"||za.k==="div"?zH*.03:za.k==="h1"?zH*.03:za.k==="h2"?zH*.038:za.k==="caps"?zH*.03:za.k==="lead"?zH*.02:zH*.028;
let zB=zBau(),zT=0;const zSum=()=>{zT=zB.reduce((za,zb,zx)=>za+zb.h+(zx<zB.length-1?zGap(zb,zB[zx+1]):0),0)};zSum();
for(let k=0;k<30&&zT>zH*.74&&zK>.72;k++){zK*=.94;zB=zBau();zSum()}
let y=zCover?Math.max(zH*.14,zH*.885-zT):Math.max(zH*.14,zH*.56-zT/2);
const zSch=new zFb.Shadow({color:"rgba(0,0,0,0.28)",blur:zW*.012,offsetX:0,offsetY:0});
const zStrich=(x1,x2,yy,fs)=>{let zh=0;const zs=String(t.text||"")+x1;for(let k=0;k<zs.length;k++)zh=(zh*31+zs.charCodeAt(k))%9973;const zj=k=>((zh*(k+3))%7-3)/3*fs*.035;const sw=Math.max(1.5,zW*.0032);
e.add(new zFb.Path(`M ${x1} ${yy+zj(1)} Q ${(x1+x2)/2} ${yy+zj(2)+fs*.03} ${x2} ${yy+zj(3)}`,{fill:"",stroke:"#FFFFFF",strokeWidth:sw,strokeLineCap:"round",...zNo}));
e.add(new zFb.Path(`M ${x1+fs*.15} ${yy+fs*.09+zj(4)} Q ${(x1+x2)/2} ${yy+fs*.06+zj(5)} ${x2-fs*.1} ${yy+fs*.1+zj(6)}`,{fill:"",stroke:"#FFFFFF",strokeWidth:sw*.6,strokeLineCap:"round",opacity:.85,...zNo}))};
zB.forEach((zb,zx)=>{if(zb.k==="div"){const xx=zAus==="mitte"?zW/2:L+zW*.01;e.add(new zFb.Line([xx,y,xx,y+zb.h],{stroke:"#FFFFFF",strokeWidth:Math.max(1.5,zW*.0025),...zNo}))}
else if(zb.lines.length){const st=zb.st,fs=zb.fs,lh=fs*st.lh;zb.lines.forEach((zl,zi)=>{const yc=y+lh*zi+lh/2;const x0=zb.k==="li"?L+LI:zAus==="mitte"?(zW-zl.w)/2:L;
if(zb.k==="li"&&zi===0){const ax=L,aw=zW*.058,sw=Math.max(1.5,zW*.0032);e.add(new zFb.Line([ax,yc,ax+aw,yc],{stroke:"#FFFFFF",strokeWidth:sw,strokeLineCap:"round",...zNo}));e.add(new zFb.Polyline([{x:ax+aw-fs*.32,y:yc-fs*.22},{x:ax+aw,y:yc},{x:ax+aw-fs*.32,y:yc+fs*.22}],{fill:"",stroke:"#FFFFFF",strokeWidth:sw,strokeLineCap:"round",strokeLineJoin:"round",...zNo}))}
let xx=x0;const zg=[];zl.segs.forEach(sg=>{const zq=zg[zg.length-1];zq&&zq.b===sg.b&&zq.u===sg.u?(zq.t+=sg.t,zq.w+=sg.w):zg.push({...sg})});
zg.forEach(sg=>{e.add(new zFb.Text(sg.t,{left:xx,top:yc,originX:"left",originY:"center",fontFamily:st.fam,fontWeight:sg.b&&st.fam===SANS?"600":st.w,fontSize:fs,charSpacing:st.cs||0,fill:"#FFFFFF",shadow:zSch,...zNo}));
if(sg.u){const tw=sg.w-zMs((/\s+$/.exec(sg.t)||[""])[0],`600 ${fs}px "${st.fam}"`,fs,0);zStrich(xx,xx+tw,yc+fs*.62,fs)}xx+=sg.w})})}
y+=zb.h+(zx<zB.length-1?zGap(zb,zB[zx+1]):0)});
K.magMonogramm&&e.add(new zFb.Text(String(K.magMonogramm),{left:zW*.905,top:zH*.105,originX:"right",originY:"center",fontFamily:SER,fontWeight:"300",fontSize:zW*.095,charSpacing:-40,fill:"#FFFFFF",shadow:zSch,...zNo}));
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}'''
ANKER = 'if($e&&(t.karte==="ablauf"||t.reminderArt==="ablauf")){const Ab=T1('
ersetze(ANKER, ZEICHNER.replace('\n', '') + ANKER)
ersetze('title:"Geladene Datei",children:"karten451"', f'title:"Geladene Datei",children:"karten{VERSION}"')
open(Z, 'w', encoding='utf-8').write(s)
print('ok')
