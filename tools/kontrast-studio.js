/* Look „Studio“ zum Ausprobieren (Carina 21.10., Pinterest-Vorlage „Herground“; „bitte 100 %“).
   Wie die Vorlage: Hook in Kleinbuchstaben, sehr fett und eng (Inter 800, Zeilenabstand 0.84, Laufweite −60), so groß,
   dass er die Breite füllt, oben links. Lange Hooks: erster Satz groß, der Rest klein unten links.
   Akzent auf dem *markierten* Wort je nach Kachel: dicke Unterstreichung, schräg, mit Kuli umkreist oder in Rost.
   Mikro-Texte: Name fett oben links, gestapelte Versal-Zeilen oben rechts, Unterzeile in Versalien unten links,
   langer dünner Pfeil unten rechts. Typen im Rhythmus magKontrastFeed:
   hgcreme     Creme, Weinrot-Schrift (Akzent wechselt: unterstrichen, schräg, umkreist)
   hgfoto      warmes dunkles Foto, weiße Schrift, Akzent schräg in Rost
   hgfotorost  helles Foto, Schrift in Rost
   hgrost      Rost-Fläche, Creme-Schrift
   hgschwarz   fast schwarz abgedunkeltes Foto, weiße Schrift, Akzent in hellem Rost
   hgblob      Creme, Foto in organischer Klecks-Form, Schrift weiß darauf, Akzent in Rost
   Eingeschaltet nur über den Look-Schalter (site/look-schalter.js → window.BS_LOOK_K).
   Wird von editorial-look.py vor den Papier-Zweig gesetzt; alle Zeilenumbrüche werden entfernt. */
if(zxTyp.slice(0,2)==="hg"){
const hT=zxTyp.slice(2),hF=K.kontrastHgSchrift||"Inter",hCr="#F1EBE2",hWr="#3B0B0B",hRo="#9E2A14",hRoH="#E0603F";
try{await Promise.race([Promise.all([`800 40px "${hF}"`,`700 40px "${hF}"`,`italic 800 40px "${hF}"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
const hFoto=hT==="foto"||hT==="fotorost"||hT==="schwarz"||hT==="blob",hInk={creme:hWr,foto:"#FFFFFF",fotorost:hRo,rost:hCr,schwarz:"#FFFFFF",blob:"#FFFFFF"}[hT]||hWr,hMik={creme:hWr,foto:"#FFFFFF",fotorost:hWr,rost:hCr,schwarz:"#FFFFFF",blob:hWr}[hT]||hWr,hAkz={creme:hWr,foto:hRoH,fotorost:hWr,rost:hCr,schwarz:hRoH,blob:hRo}[hT]||hRo;
const hArt=hT==="creme"?["linie","schraeg","kreis"][((zxTg%3)+3)%3]:hT==="rost"?"linie":hT==="fotorost"?"linie":"schraeg";
const hWort=String(zKickT||"").replace(/\*+/g,"").replace(/[.!?…:,]+$/,"").trim();
let hTitel=String(zxTitel||"").replace(/\s+/g," ").trim(),hSub=String(zxSub||zxKl||zxSkriptT||"").replace(/\*+/g,"").trim();
{const zp=hTitel.replace(/\*/g,"");if(zp.length>44){const zm=/^(.{8,}?[.!?…])\s+(.+)$/.exec(hTitel);if(zm){hTitel=zm[1];hSub=hSub||zm[2].replace(/\*+/g,"")}}}
if(!/\*[^*]+\*/.test(hTitel)){const zw=hTitel.replace(/[.!?…„“”"]+$/,"").split(" ");if(zw.length>1){const zl=zw[zw.length-1];hTitel=hTitel.slice(0,hTitel.lastIndexOf(zl))+"*"+zl+"*"+hTitel.slice(hTitel.lastIndexOf(zl)+zl.length)}}
const hRaster=(zfill)=>e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zfill,...zNo}));
if(hT==="blob"){hRaster(hCr)}else if(hFoto){zxFotoBG(zxFoto);
if(hT==="fotorost"){e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"rgba(255,246,236,0.28)",...zNo}))}
else{e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"#B9784B",opacity:.32,globalCompositeOperation:"multiply",...zNo}));e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:hT==="schwarz"?"rgba(12,8,6,0.66)":"rgba(18,10,6,0.34)",...zNo}));e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,...zNo,fill:new zFb.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:zH},colorStops:[{offset:0,color:"rgba(0,0,0,0.38)"},{offset:.45,color:"rgba(0,0,0,0.08)"},{offset:1,color:"rgba(0,0,0,0.45)"}]})}))}}
else hRaster(hT==="rost"?hRo:hCr);
if(hT==="blob"&&zxFoto){try{const zcx=zW*.52,zcy=zH*.6,zr=zW*.43,zn=9,zpt=[];for(let k=0;k<zn;k++){const za=k/zn*Math.PI*2-Math.PI/2,zf=1+.16*Math.sin(k*2.3+zxTg)+.08*Math.cos(k*1.7);zpt.push([zcx+Math.cos(za)*zr*zf,zcy+Math.sin(za)*zr*zf*1.12])}let zd=`M ${zpt[0][0]} ${zpt[0][1]}`;for(let k=0;k<zn;k++){const z0=zpt[(k-1+zn)%zn],z1=zpt[k],z2=zpt[(k+1)%zn],z3=zpt[(k+2)%zn];zd+=` C ${z1[0]+(z2[0]-z0[0])/6} ${z1[1]+(z2[1]-z0[1])/6} ${z2[0]-(z3[0]-z1[0])/6} ${z2[1]-(z3[1]-z1[1])/6} ${z2[0]} ${z2[1]}`}
const zsk=Math.max(zW/zxFoto.width,zH/zxFoto.height),zim=new zFb.Image(zxFoto,{left:(zW-zxFoto.width*zsk)/2,top:(zH-zxFoto.height*zsk)/2,scaleX:zsk,scaleY:zsk,...zNo});zim.clipPath=new zFb.Path(zd,{absolutePositioned:!0});e.add(zim);const zv=new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"rgba(20,10,6,0.32)",...zNo});zv.clipPath=new zFb.Path(zd,{absolutePositioned:!0});e.add(zv)}catch(zz){}}
const hX=zW*.065,hB=zW*.87,hMk=(ztx,zx,zy,zo)=>new zFb.Textbox(String(ztx).toLocaleUpperCase("de-DE"),{left:zx,top:zy,width:zW*.4,fontFamily:hF,fontWeight:"800",fontSize:zW*.0175,charSpacing:-10,lineHeight:1,fill:hMik,...zNo,...(zo||{})});
e.add(new zFb.Text("CARINA ANNA PRAV",{left:hX,top:zH*.042,fontFamily:hF,fontWeight:"800",fontSize:zW*.019,charSpacing:-20,fill:hT==="blob"?hWr:hMik,...zNo}));
const hStapel=hWort?[hWort]:[["CONTENT","ANGEBOTE","VERKAUF"],["MENTORING","FÜR COACHES"],["INTERESSE","→ KAUF"],["SCHREIB MIR","STARTEN"]][((zxTg%4)+4)%4];
e.add(hMk(hStapel.join("\n"),zW-hX,zH*.042,{originX:"right",textAlign:"right",fill:hT==="blob"?hWr:hMik}));
const hSg=zxSegs(hTitel,"wort"),hPl=hSg.plain.toLocaleLowerCase("de-DE"),hIk=Object.keys(hSg.st).map(Number).sort((za,zb)=>za-zb),hBlob=hT==="blob",hBw=hBlob?zW*.7:hB,hMaxH=hBlob?zH*.42:hFoto?zH*.55:zH*.62;
let hFs=zW*.3,hTb=null;for(let k=0;k<60;k++){const zsty={};hIk.forEach(zk=>{zsty[zk]={fill:hAkz,...(hArt==="schraeg"?{fontStyle:"italic"}:{})}});hTb=new zFb.Textbox(hPl,{left:0,top:0,width:hBw,fontFamily:hF,fontWeight:"800",fontSize:hFs,lineHeight:.84,charSpacing:-60,fill:hInk,textAlign:hBlob?"right":"left",styles:{0:zsty},...zNo});const zlw=Math.max(0,...hPl.split(/\s+/).filter(Boolean).map(zwd=>new zFb.Text(zwd,{fontFamily:hF,fontWeight:"800",fontSize:hFs,charSpacing:-60}).width||0));if(zlw<=hBw*.99&&hTb.height<=hMaxH)break;hFs*=.95}
const hTx=hBlob?zW-hX-hBw:hX,hTy=hBlob?zH*.62-(hTb.height||0)/2:hT==="foto"&&zxTg%2?zH*.42-(hTb.height||0)/2+zH*.08:zH*.13;hTb.set({left:hTx,top:hTy});e.add(hTb);
if(hIk.length&&(hArt==="linie"||hArt==="kreis")){try{const zruns=[];hIk.forEach(zq=>{const zr=zruns[zruns.length-1];zr&&zq===zr[1]+1?zr[1]=zq:zruns.push([zq,zq])});zruns.forEach(([za,zb])=>{while(zb>za&&/[\s.,!?…:;“”"]/.test(hPl[zb]))zb--;const zc1=hTb.get2DCursorLocation(za),zc2=hTb.get2DCursorLocation(zb),zlt=zl=>{let zy=0;for(let q=0;q<zl;q++)zy+=hTb.getHeightOfLine(q);return zy};for(let zl=zc1.lineIndex;zl<=zc2.lineIndex;zl++){const zca=zl===zc1.lineIndex?zc1.charIndex:0,zcz=zl===zc2.lineIndex?zc2.charIndex:hTb._textLines[zl].length-1,zlt0=(hTb._textLines[zl]||[]).join(""),zmw=zq=>zq?new zFb.Text(zq,{fontFamily:hF,fontWeight:"800",fontSize:hFs,charSpacing:-60}).width||0:0,zoff=hTx+(hTb._getLineLeftOffset?hTb._getLineLeftOffset(zl)||0:0),zxa=zoff+zmw(zlt0.slice(0,zca)),zxb=zoff+zmw(zlt0.slice(0,zcz+1)),zlh=hTb.getHeightOfLine(zl)/hTb.lineHeight;if(hArt==="linie"){e.add(new zFb.Rect({left:zxa,top:hTy+zlt(zl)+zlh*.86,width:Math.max(1,zxb-zxa),height:Math.max(3,hFs*.055),fill:hInk,...zNo}))}else if(zc1.lineIndex===zc2.lineIndex){e.add(new zFb.Ellipse({left:(zxa+zxb)/2,top:hTy+zlt(zl)+zlh*.5,originX:"center",originY:"center",rx:(zxb-zxa)/2+hFs*.28,ry:zlh*.6,fill:"",stroke:hInk,strokeWidth:Math.max(2.5,hFs*.035),angle:-4,...zNo}))}}})}catch(zz){}}
if(hSub){const zs=new zFb.Textbox(hSub.toLocaleUpperCase("de-DE"),{left:hX,top:0,width:zW*.5,fontFamily:hF,fontWeight:"700",fontSize:zW*.02,lineHeight:1.04,charSpacing:-5,fill:hMik,...zNo});let zk=0;while(zs.textLines&&zs.textLines.length>4&&zk<10){zs.set({fontSize:zs.fontSize*.92});zs.initDimensions();zk++}zs.set({top:zH*.935-(zs.height||0)});e.add(zs)}
const hAy=zH*.915,hAx2=zW-hX,hAx1=hAx2-zW*.1,hSw=Math.max(2,zW*.0032),hAf=hT==="blob"?hWr:hMik;e.add(new zFb.Line([hAx1,hAy,hAx2,hAy],{stroke:hAf,strokeWidth:hSw,...zNo}));e.add(new zFb.Polyline([{x:hAx2-zW*.022,y:hAy-zW*.018},{x:hAx2,y:hAy},{x:hAx2-zW*.022,y:hAy+zW*.018}],{fill:"",stroke:hAf,strokeWidth:hSw,strokeLineCap:"round",strokeLineJoin:"round",...zNo}));
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}
