/* Look „Untertitel“ (magUntertitelFeed), nach Carinas Reel-Referenz: Foto in Farbe unverändert, Hook in
   fetter Helvetica Neue schwarz auf weißen Zeilen-Kästchen (wie Untertitel), zentriert im unteren Drittel.
   Ein Wort rot: *Sternchen*, sonst das längste Wort. Text nach „&“ wird weggelassen.
   Folgefolien: weiß mit schwarzer Schrift, letzte Folie schwarz mit weißer Schrift, Akzent rot.
   Wird von editorial-look.py eingesetzt; alle Zeilenumbrüche werden entfernt. */
if(K.magUntertitelFeed){const zUR=K.untertitelRot||"#E2262D",zUHN=K.untertitelSans||"HelveticaNeueBrand";
if(!zCover){const zUN=(i&&i.slideIndex)||0,zUTot=(i&&i.totalSlides)||0,zULe=zUTot>1&&zUN>=zUTot-1;e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:zULe?"#111111":"#FFFFFF",...zNo}));TXT=zULe?"#FFFFFF":"#111111";AK=zUR;zkKeinSchatten=!0;zkObenA=0}
else{
try{await Promise.race([Promise.all([`700 40px ${zUHN}`,`500 40px ${zUHN}`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
e.getObjects().forEach(zo=>{zo.type!=="image"&&(zo.visible=!1)});
const zURaw=String(zRoh||t.text||"").split(/\n/).map(q=>q.trim()).filter(Boolean).join(" "),zUAi=zURaw.search(/(^|\s)&\s/);
const zUTitel=(zUAi>=0?zURaw.slice(0,zUAi):zURaw).replace(/__/g,"").trim();
let zUPlain="";const zUSt={};zUTitel.split(/(\*[^*]+\*)/).filter(Boolean).forEach(zp=>{const zk=/^\*.*\*$/.test(zp),ztx=zk?zp.slice(1,-1):zp;for(let k=0;k<ztx.length;k++)zk&&(zUSt[zUPlain.length+k]={fill:zUR});zUPlain+=ztx});
if(!Object.keys(zUSt).length){let zb="",zi=-1;const zre=/[A-Za-zÄÖÜäöüß\-]+/g;let zm;while((zm=zre.exec(zUPlain))){zm[0].length>zb.length&&(zb=zm[0],zi=zm.index)}if(zi>=0)for(let k=zi;k<zi+zb.length;k++)zUSt[k]={fill:zUR}}
const zUw=zW*.84;let zsk=1,ztb=null;const zfs0=zUPlain.length>110?zW*.058:zW*.07;
for(let k=0;k<40;k++){ztb=new zFb.Textbox(zUPlain,{width:zUw,fontFamily:zUHN,fontWeight:"700",fontSize:zfs0*zsk,lineHeight:.98,charSpacing:-25,fill:"#111111",textAlign:"center",styles:{0:zUSt},...zNo});const zlw=Math.max(0,...zUPlain.split(/\s+/).filter(Boolean).map(zwd=>new zFb.Text(zwd,{fontFamily:zUHN,fontWeight:"700",fontSize:zfs0*zsk,charSpacing:-25}).width||0));if(zlw<=zUw*.98&&ztb.height<=zH*.36)break;zsk*=.94}
const zUx=(zW-zUw)/2,zUy=zH*.81-ztb.height,zpad=ztb.fontSize*.22;ztb.set({left:zUx,top:zUy});
let zly=zUy;(ztb.textLines||[]).forEach((zl,k)=>{const zlh=ztb.getHeightOfLine(k),zlw=ztb.getLineWidth(k)||0;zlw>0&&e.add(new zFb.Rect({left:zUx+(zUw-zlw)/2-zpad,top:zly+(k?0:-zpad*.25),width:zlw+zpad*2,height:zlh+(k?0:zpad*.25)+(k===ztb.textLines.length-1?zpad*.35:1),fill:"#FFFFFF",...zNo}));zly+=zlh});
e.add(ztb);
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}}
