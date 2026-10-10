/* Look „Statement“ (magStatementFeed): entsättigtes, abgedunkeltes Foto (foto) oder tiefe
   Oxblood-Fläche (flaeche). Zentriert: Einleitung in Montserrat, großes Zitat in Libre Baskerville
   (weiß, Akzentwörter fett in Orange, ein Verneinungswort unterstrichen), Nachsatz in Montserrat
   (Text nach „&“). Dazu ein schräger ovaler Sticker, unten links ein Versal-Satz, oben rechts der
   Absender. Akzent: *Sternchen*-Wörter, sonst bis zu zwei großgeschriebene Wörter (Nomen).
   Folgefolien: Oxblood-Fläche mit weißer Schrift, Akzent Orange.
   Wird von editorial-look.py eingesetzt; alle Zeilenumbrüche werden entfernt. */
if(K.magStatementFeed){const zsL=String(K.magStatementFeed).split("|").filter(Boolean),zsTg=Number(t._tag)||0,zsTyp=zsL[(zsTg%zsL.length+zsL.length)%zsL.length];
const zsOR=K.statementOrange||"#F2603C",zsGR=K.statementGrund||"#3E141B",zsSE=K.statementSerif||"Libre Baskerville",zsSA=K.statementSans||"MontserratBrand",zsPK=K.statementSticker||"#F4A9B8";
if(!zCover){e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zsGR,...zNo}));TXT="#FFFFFF";AK=zsOR;zkKeinSchatten=!0;zkObenA=0}
else{
try{await Promise.race([Promise.all([`400 40px "${zsSE}"`,`700 40px "${zsSE}"`,`400 40px "${zsSA}"`,`700 40px "${zsSA}"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
const zsW=(za,zl)=>za[((zl%za.length)+za.length)%za.length],zsI=Math.floor(zsTg/zsL.length);
const zsRaw=String(zRoh||t.text||"").split(/\n/).map(q=>q.trim()).filter(Boolean).join(" "),zsAi=zsRaw.search(/(^|\s)&\s/);
const zsTitelRoh=(zsAi>=0?zsRaw.slice(0,zsAi):zsRaw).replace(/__/g,"").trim(),zsNachRoh=zsAi>=0?zsRaw.slice(zsAi).replace(/^\s*&\s*/,"").trim():"";
const zsIntro=zKickT?zKickT+":":zsW(String(K.statementIntro||"Ehrlich jetzt …|Hör mal …|Klartext:|Notiz an dich:|Ich sag's dir, wie's ist:").split("|"),zsTg+zsI);
const zsSegs=(zs,zauto)=>{let zplain="";const zst={};const zstar=/\*[^*]+\*/.test(zs);zs.split(/(\*[^*]+\*)/).filter(Boolean).forEach(zp=>{const zk=/^\*.*\*$/.test(zp),ztx=zk?zp.slice(1,-1):zp;for(let k=0;k<ztx.length;k++)zk&&(zst[zplain.length+k]={fontWeight:"700",fill:zsOR});zplain+=ztx});
if(!zstar&&zauto){const zkand=[];const zre=/(^|[\s(])([A-ZÄÖÜ][a-zäöüß\-]{4,}[A-Za-zäöüß]*)/g;let zm;while((zm=zre.exec(zplain))){const zi=zm.index+zm[1].length;if(zi===0)continue;const zvor=zplain.slice(0,zi).trimEnd();if(/[.!?:„"»]$/.test(zvor))continue;zkand.push({i:zi,n:zm[2].length})}zkand.sort((za,zb)=>zb.n-za.n).slice(0,zplain.length>70?2:1).forEach(zc=>{for(let k=zc.i;k<zc.i+zc.n;k++)zst[k]={fontWeight:"700",fill:zsOR}})}
if(zauto){const zre2=/(^|\s)(nicht|kein|keine|nie|niemals|nur|nö)(?=[\s.,!?]|$)/gi;let zm2;while((zm2=zre2.exec(zplain))){const zi=zm2.index+zm2[1].length;if(zst[zi])continue;for(let k=zi;k<zi+zm2[2].length;k++)zst[k]={...(zst[k]||{}),underline:!0};break}}
return{plain:zplain,st:zst}};
const zsBal=(zo,zw)=>{const zn=(zo.textLines||[]).length;if(zn<2)return;let lo=zw*.5,hi=zw;for(let k=0;k<10;k++){const zm=(lo+hi)/2;zo.set({width:zm});zo.initDimensions();(zo.textLines.length>zn||Math.max(...(zo.__lineWidths||[0]))>zm*1.01)?lo=zm:hi=zm}zo.set({width:hi});zo.initDimensions()};
const zsBox=(zsg,zfam,zgew,zfs,zw,zmaxH,zlh,zcs)=>{let zsk=1,ztb=null;for(let k=0;k<45;k++){ztb=new zFb.Textbox(zsg.plain,{width:zw,fontFamily:zfam,fontWeight:zgew,fontSize:zfs*zsk,lineHeight:zlh,charSpacing:zcs,fill:"#FFFFFF",textAlign:"center",styles:{0:zsg.st},...zNo});zsBal(ztb,zw);const zlw=Math.max(0,...zsg.plain.split(/\s+/).filter(Boolean).map(zwd=>new zFb.Text(zwd,{fontFamily:zfam,fontWeight:"700",fontSize:zfs*zsk,charSpacing:zcs}).width||0));if(zlw<=zw*.98&&ztb.height<=zmaxH)break;zsk*=.94}return ztb};
let zsFoto=null;if(zsTyp==="foto"){e.getObjects().forEach(zo=>{zo.type!=="image"&&(zo.visible=!1)});try{zsFoto=e.toCanvasElement(1)}catch(zz){}}
e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zsTyp==="foto"?"#1E1A19":zsGR,...zNo}));
if(zsFoto){const zc=document.createElement("canvas"),zsc=Math.min(1,1400/Math.max(zsFoto.width,zsFoto.height));zc.width=Math.round(zsFoto.width*zsc);zc.height=Math.round(zsFoto.height*zsc);const zx=zc.getContext("2d");zx.drawImage(zsFoto,0,0,zc.width,zc.height);try{const zd=zx.getImageData(0,0,zc.width,zc.height),zq=zd.data,zsat=Number(K.statementSaettigung==null?.25:K.statementSaettigung);for(let k=0;k<zq.length;k+=4){const zl=.3*zq[k]+.59*zq[k+1]+.11*zq[k+2];for(let j=0;j<3;j++){let v=zl+(zq[k+j]-zl)*zsat;v=(v-128)*1.08+122;zq[k+j]=v<0?0:v>255?255:v}}zx.putImageData(zd,0,0)}catch(zz){}e.add(new zFb.Image(zc,{left:0,top:0,scaleX:zW/zc.width,scaleY:zH/zc.height,...zNo}));
e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:`rgba(18,12,11,${Number(K.statementDunkel==null?.5:K.statementDunkel)})`,...zNo}))}
const zsTeile=[];const zsIn=new zFb.Textbox(zsIntro,{width:zW*.8,fontFamily:zsSA,fontWeight:"400",fontSize:zW*.046,lineHeight:1.15,fill:"#FFFFFF",textAlign:"center",...zNo});zsTeile.push(zsIn);
const zsQ=zsBox(zsSegs(zsTitelRoh,!0),zsSE,"400",zW*.092,zW*.86,zH*(zsNachRoh?.36:.46),1.08,-10);zsTeile.push(zsQ);
if(zsNachRoh){const zsg=zsSegs(zsNachRoh,!1);Object.keys(zsg.st).forEach(zk=>{zsg.st[zk].fontWeight="700"});zsTeile.push(zsBox(zsg,zsSA,"400",zW*.048,zW*.74,zH*.16,1.12,0))}
const zsGap=zW*.055;let zsH=0;zsTeile.forEach((zo,k)=>{zsH+=(zo.height||0)+(k?zsGap:0)});let zsY=Math.max(zH*.12,zH*.46-zsH/2);zsTeile.forEach(zo=>{zo.set({left:(zW-zo.width)/2,top:zsY});e.add(zo);zsY+=(zo.height||0)+zsGap});
const zsStT=zsW(String(K.statementStickerText||"SO GEHT'S|LIES WEITER|SWIPE →|ERKLÄR ICH DIR").split("|"),zsTg+zsI*2),zsSt=new zFb.Text(zsStT,{fontFamily:zsSA,fontWeight:"700",fontSize:zW*.05,charSpacing:20,fill:"#141010",originX:"center",originY:"center",...zNo}),zsRx=(zsSt.width||zW*.3)/2+zW*.07,zsRy=zW*.068,zsCx=zW*.63,zsCy=Math.max(zsY+zsRy*.6,zH*.84);
if(zsCy+zsRy<zH*.97){const zg=new zFb.Group([new zFb.Ellipse({rx:zsRx,ry:zsRy,originX:"center",originY:"center",left:0,top:0,fill:zsPK,stroke:"#141010",strokeWidth:Math.max(2,zW*.003)}),new zFb.Ellipse({rx:zsRx*1.01,ry:zsRy*.96,originX:"center",originY:"center",left:zW*.004,top:-zW*.003,fill:"",stroke:"#141010",strokeWidth:Math.max(1.5,zW*.0022),angle:1.5}),zsSt.set({left:0,top:0})],{left:zsCx,top:zsCy,originX:"center",originY:"center",angle:-6,...zNo});e.add(zg)}
e.add(new zFb.Textbox(String(K.statementFuss||"FÜR DIE\nJA-SAGERINNEN."),{width:zW*.3,left:zW*.09,top:zH*.885,fontFamily:zsSA,fontWeight:"500",fontSize:zW*.019,lineHeight:1.15,fill:"#FFFFFF",textAlign:"left",...zNo}));
e.add(new zFb.Text(String(K.statementAbsender||"CARINA ANNA PRAV"),{fontFamily:zsSA,fontWeight:"500",fontSize:zW*.019,charSpacing:60,fill:"#FFFFFF",originX:"right",left:zW*.93,top:zH*.045,...zNo}));
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}}
