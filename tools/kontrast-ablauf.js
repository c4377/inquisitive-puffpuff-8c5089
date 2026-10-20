/* Ablauf-/Zusammenarbeit-Folien im Look von carinaannaprav.at (Carina 20.10.: „leite meine Ablauf-Folien von
   meiner Website ab und brande sie wie die Website“). Weiß, Titel in Playfair Display kursiv, Text in Montserrat,
   Cognac-Etiketten in Versalien, Nummern-Kästchen wie „01“, schwarze Knöpfe; [dunkel] = Schlussfolie in #141414.
   Format pro Folie: #KOPF (zeigt die Marke „Carina Anna Prav“), >ETIKETT, [nr: 01], Titel (erste freie Zeile),
   ~Unterzeile (Playfair kursiv), [liste: a | b], [stationen: a | b], [preis: 249 € | Zusatz], [knopf: Text],
   [dunkel], weitere freie Zeilen = Fließtext. Reihenfolge auf der Folie = Reihenfolge im Text.
   Fotos (Carina 20.10.: „Ablauf mit Fotos bitte“): schwarz-weiß wie auf der Website. Deckblatt ([nr: …]) und
   [dunkel] vollflächig mit dunklem Verlauf und weißer Schrift wie der Website-Hero, alle anderen Folien mit einem
   Fotostreifen oben. [ohne foto] schaltet das Foto für eine Folie ab. Fotos aus den Markenbildern, je Folie ein anderes.
   Wird von editorial-look.py VOR dem Magazin-Zeichner eingesetzt; alle Zeilenumbrüche werden entfernt. */
if((t.karte==="ablauf"||t.reminderArt==="ablauf")&&BS_KACHEL.magKontrastFeed&&BS_KACHEL.kontrastAblauf===1){const zFb=Pe.fabric,K=BS_KACHEL,zW=r,zH=n,zNo={selectable:!1,evented:!1};
const zaPF="Playfair Display",zaMO="Montserrat",zaN=(i&&i.slideIndex)||0,zaTot=(i&&i.totalSlides)||0;
try{await Promise.race([Promise.all([`italic 400 40px "${zaPF}"`,`400 40px "${zaPF}"`,`400 40px ${zaMO}`,`500 40px ${zaMO}`,`600 40px ${zaMO}`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
e.getObjects().forEach(zo=>{zo.visible=!1});
const zaZ=String(t.text||"").split(/\n/).map(q=>q.trim()).filter(Boolean),zaDunkel=zaZ.some(q=>/^\[dunkel\]$/i.test(q));
const zaOhne=zaZ.some(q=>/^\[ohne foto\]$/i.test(q)),zaVollW=zaDunkel||zaZ.some(q=>/^\[nr\s*:/i.test(q)),zaBandH=zH*.38;
const zaBl=window.__bsBilder||[],zaTg=typeof t._tag=="number"?t._tag:(Number(t.day)||0),zaSrc=zaOhne?"":(typeof t.background=="string"&&t.background.length>5?t.background:"")||(zaBl.length?zaBl[(zaN*3+zaTg*5+1)%zaBl.length]:"");
let zaFoto=null;if(zaSrc){try{const zim=await new Promise(zr=>{const zq=new Image();/^https?:/.test(zaSrc)&&(zq.crossOrigin="anonymous");zq.onload=()=>zr(zq);zq.onerror=()=>zr(null);zq.src=zaSrc;setTimeout(()=>zr(null),8e3)});if(zim){const zcw=Math.round(zW),zch=Math.round(zaVollW?zH:zaBandH),zc=document.createElement("canvas");zc.width=zcw;zc.height=zch;const zx=zc.getContext("2d"),zw0=zim.naturalWidth||zim.width,zh0=zim.naturalHeight||zim.height,zsk=Math.max(zcw/zw0,zch/zh0),zdw=zw0*zsk,zdh=zh0*zsk;zx.drawImage(zim,(zcw-zdw)/2,Math.min(0,(zch-zdh)*(zaVollW?.3:.26)),zdw,zdh);try{const zd=zx.getImageData(0,0,zcw,zch),zp=zd.data;for(let k=0;k<zp.length;k+=4){const zy=.299*zp[k]+.587*zp[k+1]+.114*zp[k+2],zv=Math.max(0,Math.min(255,(zy-128)*1.06+128));zp[k]=zp[k+1]=zp[k+2]=zv}zx.putImageData(zd,0,0)}catch(zz){}
if(zaVollW){let zg=zx.createLinearGradient(0,0,0,zch);zg.addColorStop(0,"rgba(10,10,10,0.45)");zg.addColorStop(.3,"rgba(10,10,10,0.18)");zg.addColorStop(.55,"rgba(10,10,10,0.45)");zg.addColorStop(1,"rgba(10,10,10,0.9)");zx.fillStyle=zg;zx.fillRect(0,0,zcw,zch);zaDunkel&&(zx.fillStyle="rgba(10,10,10,0.35)",zx.fillRect(0,0,zcw,zch))}else{let zg=zx.createLinearGradient(0,0,0,zch*.4);zg.addColorStop(0,"rgba(10,10,10,0.42)");zg.addColorStop(1,"rgba(10,10,10,0)");zx.fillStyle=zg;zx.fillRect(0,0,zcw,zch)}
zaFoto=new zFb.Image(zc,{left:0,top:0,scaleX:zW/zcw,scaleY:(zaVollW?zH:zaBandH)/zch,...zNo})}}catch(zz){zaFoto=null}}
const zaVoll=zaVollW&&!!zaFoto,zaBand=!zaVollW&&!!zaFoto,zaHT=zaDunkel||zaVoll;
const zaG=zaDunkel?"#141414":"#FFFFFF",zaS=zaHT?"#FFFFFF":"#141414",zaT=zaHT?"rgba(255,255,255,0.8)":"#4A4A4A",zaA=zaHT?"#D9A479":"#9E5A2C",zaL=zaHT?"rgba(255,255,255,0.62)":"#8A8A8A",zaH=zaHT?"rgba(255,255,255,0.25)":"#E6E2DD",zaPk=zaVoll?"rgba(20,20,20,0.6)":zaG;
e.backgroundColor=zaG;e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zaG,...zNo}));zaFoto&&e.add(zaFoto);
const zaM=zW*.1,zaB=zW-zaM*2,zaTeile=[];let zaKopf=!1,zaTitel=!1;
const zaTB=(zt,zo)=>new zFb.Textbox(zt,{width:zaB,lineHeight:1.5,...zNo,...zo});
zaZ.forEach(zl=>{let zm;
if(/^#/.test(zl)){zaKopf=!0;return}
if(/^\[(dunkel|ohne foto)\]$/i.test(zl))return;
if(/^>/.test(zl)){zaTeile.push({o:zaTB(zl.replace(/^>\s*/,"").toLocaleUpperCase("de-DE"),{fontFamily:zaMO,fontWeight:"600",fontSize:zW*.021,charSpacing:300,fill:zaA}),g:zH*.022});return}
if(zm=/^\[nr\s*:\s*(.*?)\]$/i.exec(zl)){const zs=zW*.078,zr=new zFb.Rect({left:0,top:0,width:zs,height:zs,fill:"rgba(0,0,0,0)",stroke:zaS,strokeWidth:Math.max(1.5,zW*.0018)}),zx=new zFb.Text(zm[1],{left:zs/2,top:zs/2,originX:"center",originY:"center",fontFamily:zaMO,fontWeight:"500",fontSize:zW*.024,charSpacing:80,fill:zaS});zaTeile.push({o:new zFb.Group([zr,zx],{...zNo}),g:zH*.035});return}
if(zm=/^\[(liste|stationen)\s*:\s*(.*?)\]?$/i.exec(zl)){const zp=zm[2].split("|").map(q=>q.trim()).filter(Boolean);if(!zp.length)return;
if(zm[1].toLowerCase()==="liste"){const zobs=[];let zy=0;zp.forEach((zq,k)=>{const ztx=new zFb.Textbox(zq,{left:zW*.045,top:zy,width:zaB-zW*.045,fontFamily:zaMO,fontWeight:"400",fontSize:zW*.03,lineHeight:1.4,fill:zaS});zobs.push(new zFb.Circle({left:zW*.008,top:zy+zW*.03*.62,radius:zW*.0055,originX:"center",originY:"center",fill:zaA}),ztx);zy+=(ztx.height||0)+zW*.026});zaTeile.push({o:new zFb.Group(zobs,{...zNo}),g:zH*.04})}
else{const zn=zp.length,zgap=zaB/Math.max(1,zn-1),zobs=[new zFb.Rect({left:0,top:zW*.012,width:zn>1?zaB:0,height:Math.max(1,zW*.0016),fill:zaH})];zp.forEach((zq,k)=>{const zx=zn>1?k*zgap:zaB/2,zal=k===0&&zn>1?"left":k===zn-1&&zn>1?"right":"center";zobs.push(new zFb.Circle({left:zx,top:zW*.0125,radius:zW*.0105,originX:"center",originY:"center",fill:k===0?zaA:zaPk,stroke:zaA,strokeWidth:Math.max(1.5,zW*.002)}));zobs.push(new zFb.Textbox(zq,{width:Math.min(zgap*.95,zaB*.32),fontFamily:zaMO,fontWeight:"400",fontSize:zW*.022,lineHeight:1.35,fill:zaS,textAlign:zal,originX:zal,left:zal==="left"?zx-zW*.0105:zal==="right"?zx+zW*.0105:zx,top:zW*.05}))});zaTeile.push({o:new zFb.Group(zobs,{...zNo}),g:zH*.045})}return}
if(zm=/^\[preis\s*:\s*(.*?)\]$/i.exec(zl)){const zp=zm[1].split("|").map(q=>q.trim()),zobs=[new zFb.Rect({left:0,top:0,width:zaB,height:Math.max(1,zW*.0014),fill:zaH})],zpr=new zFb.Text(zp[0]||"",{left:0,top:zW*.04,fontFamily:zaPF,fontStyle:"italic",fontWeight:"400",fontSize:zW*.075,fill:zaS});zobs.push(zpr);zp[1]&&zobs.push(new zFb.Textbox(zp[1],{left:0,top:zW*.04+(zpr.height||0)+zW*.008,width:zaB,fontFamily:zaMO,fontWeight:"400",fontSize:zW*.02,fill:zaL}));zaTeile.push({o:new zFb.Group(zobs,{...zNo}),g:zH*.035});return}
if(zm=/^\[knopf\s*:\s*(.*?)\]$/i.exec(zl)){const zkh=zW*.088,zr=new zFb.Rect({left:0,top:0,width:zaB,height:zkh,fill:zaHT?"#FFFFFF":"#141414"}),zx=new zFb.Text(zm[1].toLocaleUpperCase("de-DE"),{left:zaB/2,top:zkh/2,originX:"center",originY:"center",fontFamily:zaMO,fontWeight:"600",fontSize:zW*.021,charSpacing:160,fill:zaHT?"#141414":"#FFFFFF"});zaTeile.push({o:new zFb.Group([zr,zx],{...zNo}),g:zH*.03});return}
if(/^~/.test(zl)){zaTeile.push({o:zaTB(zl.replace(/^~\s*/,""),{fontFamily:zaPF,fontStyle:"italic",fontWeight:"400",fontSize:zW*.038,lineHeight:1.35,fill:zaS}),g:zH*.035});return}
if(!zaTitel){zaTitel=!0;let zfs=zW*.092,ztb=null;for(let k=0;k<20;k++){ztb=zaTB(zl,{fontFamily:zaPF,fontStyle:"italic",fontWeight:"400",fontSize:zfs,lineHeight:1.08,fill:zaS});if(ztb.height<=zH*.24)break;zfs*=.93}zaTeile.push({o:ztb,g:zH*.035});return}
zaTeile.push({o:zaTB(zl,{fontFamily:zaMO,fontWeight:"400",fontSize:zW*.03,lineHeight:1.6,fill:zaT}),g:zH*.03})});
const zaHt=zq=>zq.o.getScaledHeight?zq.o.getScaledHeight():(zq.o.height||0),zaSum=()=>zaTeile.reduce((za,zq,k)=>za+zaHt(zq)+(k<zaTeile.length-1?zq.g:0),0);
const zaOben=zaBand?zaBandH+zH*.06:zH*.15,zaUnten=zaVoll?zH*.87:zH*.9,zaMax=zaVoll?zH*.62:zaUnten-zaOben;
for(let k=0;k<14&&zaSum()>zaMax;k++)zaTeile.forEach(zq=>{zq.o.scale((zq.o.scaleX||1)*.95);zq.g*=.95});
let zaH0=zaSum(),zaY=zaVoll?Math.max(zaOben,zaUnten-zaH0):Math.max(zaOben,(zaBand?(zaOben+zaUnten)/2:zH*.52)-zaH0/2);zaTeile.forEach(zq=>{zq.o.set({left:zaM,top:zaY,originX:"left",originY:"top"});e.add(zq.o);zaY+=zaHt(zq)+zq.g});
if(zaKopf){const zk1=new zFb.Text("Carina Anna ",{left:zaM,top:zH*.055,fontFamily:zaMO,fontWeight:"600",fontSize:zW*.024,fill:zaHT||zaBand?"#FFFFFF":zaS,...zNo});e.add(zk1);e.add(new zFb.Text("Prav",{left:zaM+(zk1.width||0),top:zH*.055-zW*.004,fontFamily:zaPF,fontStyle:"italic",fontWeight:"400",fontSize:zW*.029,fill:zaHT||zaBand?"#FFFFFF":zaS,...zNo}))}
e.add(new zFb.Text(String(K.kontrastHandle||"@carinaannaprav"),{left:zW-zaM,top:zH*.06,originX:"right",fontFamily:zaMO,fontWeight:"500",fontSize:zW*.018,charSpacing:120,fill:zaBand?"rgba(255,255,255,0.85)":zaL,...zNo}));
e.add(new zFb.Rect({left:zaM,top:zH*.925,width:zaB,height:Math.max(1,zW*.0014),fill:zaH,...zNo}));
e.add(new zFb.Text("carinaannaprav.at",{left:zaM,top:zH*.94,fontFamily:zaMO,fontWeight:"500",fontSize:zW*.018,charSpacing:120,fill:zaL,...zNo}));
zaTot>1&&e.add(new zFb.Text(`${String(zaN+1).padStart(2,"0")} / ${String(zaTot).padStart(2,"0")}`,{left:zW-zaM,top:zH*.94,originX:"right",fontFamily:zaMO,fontWeight:"500",fontSize:zW*.018,charSpacing:120,fill:zaL,...zNo}));
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}
