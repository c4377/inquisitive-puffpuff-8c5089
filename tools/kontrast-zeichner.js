/* Look „Oxblood · Kontrast“ (magKontrastFeed): reines Schwarz, Weiß und Oxblood, Fotos in
   hartem Schwarz-Weiß, Instrument Serif aufrecht und kursiv gemischt.
   papier: weißes Papier auf Schwarz, Text schwarz, Akzentwort kursiv Oxblood.
   flaeche: Oxblood-Fläche, große weiße Schrift, erster Satz kursiv.
   fotozeilen: S/W-Foto, Text in schwarzen Zeilen-Kästchen, letzter Satz Oxblood kursiv.
   fotoetikett: wie fotozeilen, darüber weißes Etikett (Kicker oder Rubrik).
   weiss: reinweiß, riesige Schrift, Anfang kursiv Oxblood, Ende schwarz.
   cutwort: reinweiß, letztes Wort riesig kursiv Oxblood hinter einem S/W-Cutout.
   Folgefolien: weiß mit schwarzer Schrift, letzte Folie Oxblood mit weißer Schrift.
   Wird von editorial-look.py eingesetzt; alle Zeilenumbrüche werden entfernt. */
if(K.magKontrastFeed){const zxL=String(K.magKontrastFeed).split("|").filter(Boolean),zxTg=Number(t._tag)||0,zxTyp=zxL[(zxTg%zxL.length+zxL.length)%zxL.length];
const zxOX=K.kontrastOx||"#5E1A21",zxIS=K.magCoverSerif||"Instrument Serif",zxHN="HelveticaNeueBrand";
if(!zCover){const zxN=(i&&i.slideIndex)||0,zxTot=(i&&i.totalSlides)||0,zxLetzte=zxTot>1&&zxN>=zxTot-1;e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zxLetzte?zxOX:"#FFFFFF",...zNo}));TXT=zxLetzte?"#FFFFFF":"#0A0706";AK=zxLetzte?"#FFFFFF":zxOX;zkKeinSchatten=!0;zkObenA=0}
else{
try{await Promise.race([Promise.all([`400 40px "${zxIS}"`,`italic 400 40px "${zxIS}"`,`500 40px "${zxHN}"`,`700 40px "${zxHN}"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
const zxW=(za,zl)=>za[((zl%za.length)+za.length)%za.length],zxI=Math.floor(zxTg/zxL.length);
let zxS=(zxTg*7919+31)%233280;const zxR=()=>(zxS=(zxS*9301+49297)%233280)/233280;
const zxRaw=String(zRoh||t.text||"").split(/\n/).map(q=>q.trim()).filter(Boolean).join(" "),zxAi=zxRaw.search(/(^|\s)&\s/);
const zxTitel=(zxAi>=0?zxRaw.slice(0,zxAi):zxRaw).replace(/__/g,"").trim(),zxSub=zxAi>=0?zxRaw.slice(zxAi).replace(/^\s*&\s*/,"").replace(/\*+|__/g,"").trim():"";
const zxSegs=(zs,zmodus)=>{let zplain="";const zst={};const zstar=/\*[^*]+\*/.test(zs);if(zstar){zs.split(/(\*[^*]+\*)/).filter(Boolean).forEach(zp=>{const zk=/^\*.*\*$/.test(zp),ztx=zk?zp.slice(1,-1):zp;for(let k=0;k<ztx.length;k++)zk&&(zst[zplain.length+k]={fontStyle:"italic",ak:1});zplain+=ztx});return{plain:zplain,st:zst}}
zplain=zs.replace(/\*+/g,"");const zsz=zSaetze(zplain).length?zSaetze(zplain):[zplain];let zpos=0;
zsz.forEach((zsatz,zn)=>{const zi=zplain.indexOf(zsatz,zpos);if(zi<0)return;zpos=zi+zsatz.length;const zw=zsatz.trim();
if(zmodus==="erster"){if(zn===0&&zsz.length>1)for(let k=zi;k<zi+zsatz.length;k++)zst[k]={fontStyle:"italic",ak:1};else if(zsz.length===1){const zl=zw.lastIndexOf(" ");for(let k=zi;k<zi+(zl>0?zl:zw.length);k++)zst[k]={fontStyle:"italic",ak:1}}}
else{const zl=zw.lastIndexOf(" ");const za=zl>0?zi+zl+1:zi;for(let k=za;k<zi+zw.length;k++)zst[k]={fontStyle:"italic",ak:zn===0?1:0}}});return{plain:zplain,st:zst}};
const zxBal=(zo,zw)=>{const zn=(zo.textLines||[]).length;if(zn<2)return;let lo=zw*.5,hi=zw;for(let k=0;k<10;k++){const zm=(lo+hi)/2;zo.set({width:zm});zo.initDimensions();(zo.textLines.length>zn||Math.max(...(zo.__lineWidths||[0]))>zm*1.01)?lo=zm:hi=zm}zo.set({width:hi});zo.initDimensions()};
const zxBox=(zsg,zfs,zw,zmaxH,zfill,zak,zo2)=>{const zop=zo2||{};let zsk=1,ztb=null;for(let k=0;k<45;k++){const zsty={};Object.keys(zsg.st).forEach(zk=>{const zv=zsg.st[zk];zsty[zk]={fontStyle:zv.fontStyle,...(zv.ak?{fill:zak}:{})}});ztb=new zFb.Textbox(zsg.plain,{width:zw,fontFamily:zxIS,fontWeight:"400",fontSize:zfs*zsk,lineHeight:zop.lh||.92,charSpacing:zop.cs==null?-30:zop.cs,fill:zfill,textAlign:zop.align||"center",styles:{0:zsty},...zNo});zxBal(ztb,zw);const zlw=Math.max(0,...zsg.plain.split(/\s+/).filter(Boolean).map(zwd=>new zFb.Text(zwd,{fontFamily:zxIS,fontStyle:"italic",fontSize:zfs*zsk,charSpacing:zop.cs==null?-30:zop.cs}).width||0));if(zlw<=zw*.98&&ztb.height<=zmaxH)break;zsk*=.94}ztb.set({width:zw});ztb.initDimensions();return ztb};
const zxSans=(ztx,zfs,zw,zfill,zgew)=>new zFb.Textbox(ztx,{width:zw,fontFamily:zxHN,fontWeight:zgew||"500",fontSize:zfs,lineHeight:1.4,fill:zfill,textAlign:"center",...zNo});
const zxSW=(zc0,zkon)=>{if(!zc0)return null;const zs=Math.min(1,1200/Math.max(zc0.width,zc0.height)),zc=document.createElement("canvas");zc.width=Math.max(1,Math.round(zc0.width*zs));zc.height=Math.max(1,Math.round(zc0.height*zs));const zx=zc.getContext("2d");zx.drawImage(zc0,0,0,zc.width,zc.height);try{const zd=zx.getImageData(0,0,zc.width,zc.height),zq=zd.data,zk=zkon||1.38;for(let k=0;k<zq.length;k+=4){const v=Math.max(0,Math.min(255,(.3*zq[k]+.59*zq[k+1]+.11*zq[k+2]-128)*zk+136));zq[k]=zq[k+1]=zq[k+2]=v}zx.putImageData(zd,0,0)}catch(zz){}return zc};
const zxSh=(za,zb)=>new zFb.Shadow({color:`rgba(0,0,0,${za})`,blur:zW*(zb||.03),offsetX:0,offsetY:zW*.012});
const zxZeilen=(zsg,zfs,zmaxW,zunten,zakFarbe)=>{const zplain=zsg.plain,zw=zplain.split(/\s+/).filter(Boolean);let zsk=1,zlines=[];const zmess=(ztx,zit,zf)=>{const zo=new zFb.Text(ztx,{fontFamily:zxIS,fontStyle:zit?"italic":"normal",fontSize:zf,charSpacing:-10});return zo.width||0};
const zsz=zSaetze(zplain).length?zSaetze(zplain):[zplain],zletzt=zsz.length>1?zsz[zsz.length-1].trim():"";
for(let k=0;k<30;k++){zlines=[];let zcur="";const zf=zfs*zsk;zw.forEach(zwd=>{const zt=zcur?zcur+" "+zwd:zwd;zmess(zt,0,zf)>zmaxW&&zcur?(zlines.push(zcur),zcur=zwd):zcur=zt});zcur&&zlines.push(zcur);if(zlines.length<=5&&zlines.every(zl=>zmess(zl,0,zf)<=zmaxW*1.01))break;zsk*=.93}
const zf=zfs*zsk,zpadX=zf*.32,zpadY=zf*.1,zlh=zf*1.08;let zakAb=zlines.length-1;if(zletzt){let zacc="";for(let k=zlines.length-1;k>=0;k--){zacc=zlines[k]+(zacc?" "+zacc:"");if(zacc.length>=zletzt.length-1){zakAb=k;break}}}
const zobs=[];let zy=zunten-zlines.length*zlh;zlines.forEach((zl,zk)=>{const zak=zk>=zakAb,ztx=new zFb.Text(zl,{fontFamily:zxIS,fontStyle:zak?"italic":"normal",fontSize:zf,charSpacing:-10,fill:"#FFFFFF",originX:"center",left:zW/2,top:zy+zpadY*.2,...zNo});const zbw=(ztx.width||0)+zpadX*2;zobs.push(new zFb.Rect({left:zW/2-zbw/2,top:zy,width:zbw,height:zlh,fill:zak?zakFarbe:"#000000",...zNo}));zobs.push(ztx);zy+=zlh});zobs.forEach(zo=>e.add(zo));return zunten-zlines.length*zlh};
const zxFotoBG=zc=>{if(!zc){e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"#222222",...zNo}));return}const zs=Math.max(zW/zc.width,zH/zc.height),zfb=t._zBox;let zfx=.5;zfb&&typeof zfb.x0==="number"&&(zfx=(zfb.x0+zfb.x1)/2);const zdw=zc.width*zs,zl=Math.max(zW-zdw,Math.min(0,zW/2-zfx*zdw));e.add(new zFb.Image(zc,{left:zl,top:(zH-zc.height*zs)/2,scaleX:zs,scaleY:zs,...zNo}))};
let zxFoto=null;if(zxTyp==="fotozeilen"||zxTyp==="fotoetikett"){e.getObjects().forEach(zo=>{zo.type!=="image"&&(zo.visible=!1)});try{zxFoto=e.toCanvasElement(1)}catch(zz){}}
e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zxTyp==="papier"?"#000000":zxTyp==="flaeche"?zxOX:"#FFFFFF",...zNo}));
if(zxTyp==="papier"){const zpw=zW*.84,zph=zH*.86,zpc=document.createElement("canvas");zpc.width=420;zpc.height=520;const zpx=zpc.getContext("2d");zpx.fillStyle="#FFFFFF";zpx.fillRect(0,0,420,520);for(let k=0;k<26;k++){const zgx=zxR()*420,zgy=zxR()*520,zgr=40+zxR()*140,zg=zpx.createRadialGradient(zgx,zgy,0,zgx,zgy,zgr);zg.addColorStop(0,`rgba(0,0,0,${.025+zxR()*.03})`);zg.addColorStop(1,"rgba(0,0,0,0)");zpx.fillStyle=zg;zpx.fillRect(0,0,420,520)}
e.add(new zFb.Image(zpc,{left:zW/2,top:zH/2,originX:"center",originY:"center",scaleX:zpw/420,scaleY:zph/520,angle:-.8,shadow:zxSh(.5,.05),...zNo}));
const ztb=zxBox(zxSegs(zxTitel,"wort"),zW*.13,zpw*.8,zph*.62,"#0A0706",zxOX);ztb.set({left:zW/2,top:zH/2-(zxSub?zH*.04:0),originX:"center",originY:"center",angle:-.8});e.add(ztb);
zxSub&&(()=>{const zs=zxSans(zxSub,zW*.024,zpw*.7,"#0A0706","500");zs.set({left:zW/2,top:zH/2+ztb.height/2+zH*.02,originX:"center",angle:-.8});e.add(zs)})()}
else if(zxTyp==="flaeche"){const ztb=zxBox(zxSegs(zxTitel,"erster"),zW*.2,zW*.88,zH*.6,"#FFFFFF","#FFFFFF",{lh:.86});ztb.set({left:zW/2,top:zH*.47,originX:"center",originY:"center"});e.add(ztb);
zxSub&&(()=>{const zs=zxSans(zxSub,zW*.026,zW*.7,"#FFFFFF","500");zs.set({left:zW/2,top:zH*.47+ztb.height/2+zH*.045,originX:"center"});e.add(zs)})()}
else if(zxTyp==="fotozeilen"||zxTyp==="fotoetikett"){zxFotoBG(zxSW(zxFoto,1.38));const zoben=zxZeilen(zxSegs(zxTitel,"wort"),zW*.066,zW*.82,zH*.9-(zxSub?zH*.05:0),zxOX);
zxSub&&(()=>{const zs=zxSans(zxSub,zW*.024,zW*.7,"#FFFFFF","700");zs.set({left:zW/2,top:zH*.9-zH*.03,originX:"center",shadow:new zFb.Shadow({color:"rgba(0,0,0,0.6)",blur:zW*.012,offsetX:0,offsetY:0})});e.add(zs)})();
if(zxTyp==="fotoetikett"){const zkt=String(zKickT||zxW(String(K.magKontrastRubrik||"SALES TALK|REALTALK|KLARTEXT").split("|"),zxI)).toLocaleUpperCase("de-DE"),zt=new zFb.Text(zkt,{fontFamily:zxHN,fontWeight:"700",fontSize:zW*.034,charSpacing:300,fill:"#000000",originX:"center",left:zW/2,...zNo}),zbw=(zt.width||0)+zW*.06,zbh=zW*.034*1.9,zby=zoben-zbh-zH*.03;e.add(new zFb.Rect({left:zW/2-zbw/2,top:zby,width:zbw,height:zbh,fill:"#FFFFFF",...zNo}));zt.set({top:zby+(zbh-(zt.height||0))/2+zW*.002});e.add(zt)}}
else if(zxTyp==="weiss"){const ztb=zxBox(zxSegs(zxTitel,"erster"),zW*.22,zW*.88,zH*.6,"#000000",zxOX,{lh:.84});ztb.set({left:zW/2,top:zH*.46,originX:"center",originY:"center"});e.add(ztb);
zxSub&&(()=>{const zs=zxSans(zxSub,zW*.024,zW*.7,"#000000","500");zs.set({left:zW/2,top:zH*.46+ztb.height/2+zH*.04,originX:"center"});e.add(zs)})()}
else{const zplain=zxTitel.replace(/\*+/g,"").trim(),zwd=(zplain.split(/\s+/).pop()||"Ja.").replace(/^[„"»]+|[“"«]+$/g,"");
const zwo=new zFb.Text(zwd,{fontFamily:zxIS,fontStyle:"italic",fontSize:zW*.6,charSpacing:-40,fill:zxOX,originX:"center",left:zW/2,top:zH*.1,...zNo});const zww=zwo.width||1;zww>zW*.96&&zwo.set({fontSize:zW*.6*zW*.96/zww});e.add(zwo);
const zkop=zxSans(zplain.toLocaleUpperCase("de-DE"),zW*.022,zW*.84,"#000000","700");zkop.set({left:zW/2,top:zH*.045,originX:"center",charSpacing:220});e.add(zkop);
const zcn=zxW(String(K.magKontrastCut||"k3|k2|k7|k4|k5").split("|").filter(Boolean),zxI*3+zxTg),zim=await new Promise(zr=>{const zq=new Image();zq.onload=()=>zr(zq);zq.onerror=()=>zr(null);zq.src="/scrap/"+zcn+".webp"});
if(zim){const zsw=zxSW(zim,1.3),zs=Math.min(zH*.74/zim.height,zW*.8/zim.width),zsc=zs*zim.width/zsw.width;e.add(new zFb.Image(zsw,{left:zW/2,top:zH-zim.height*zs/2,originX:"center",originY:"center",scaleX:zsc,scaleY:zsc,shadow:zxSh(.3,.03),...zNo}))}
zxSub&&(()=>{const zs=zxSans(zxSub,zW*.022,zW*.5,"#FFFFFF","700");zs.set({left:zW/2,top:zH*.93,originX:"center",shadow:new zFb.Shadow({color:"rgba(0,0,0,0.7)",blur:zW*.012,offsetX:0,offsetY:0})});e.add(zs)})()}
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}}
