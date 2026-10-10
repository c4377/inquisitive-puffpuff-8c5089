/* Look „Foto & Serif“ (magFotoSerifFeed), nach Carinas Explore-Referenz: Foto in Farbe, leicht abgedunkelt,
   Hook in weißer Instrument Serif zentriert, erster Satz als eigener Absatz, Rest darunter.
   Kursiv: *Sternchen*, sonst das erste du/dein/dich/dir…, sonst das längste Wort. Text nach „&“ entfällt.
   Folgefolien: warmes Dunkel mit heller Schrift.
   Wird von editorial-look.py eingesetzt; alle Zeilenumbrüche werden entfernt. */
if(K.magFotoSerifFeed){const zFS=K.fotoSerifSchrift||"Instrument Serif";
if(!zCover){e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:K.fotoSerifGrund||"#1E1915",...zNo}));TXT="#F5EFE6";AK=K.fotoSerifAkzent||"#D9B99B";zkKeinSchatten=!0;zkObenA=0}
else{
try{await Promise.race([Promise.all([`400 40px "${zFS}"`,`italic 400 40px "${zFS}"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
e.getObjects().forEach(zo=>{zo.type!=="image"&&(zo.visible=!1)});
e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"rgba(12,8,6,0.3)",...zNo}));
e.add(new zFb.Rect({left:0,top:zH*.3,width:zW,height:zH*.6,...zNo,fill:new zFb.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:zH*.6},colorStops:[{offset:0,color:"rgba(12,8,6,0)"},{offset:.5,color:"rgba(12,8,6,0.22)"},{offset:1,color:"rgba(12,8,6,0)"}]})}));
const zFRaw=String(zRoh||t.text||"").split(/\n/).map(q=>q.trim()).filter(Boolean).join(" "),zFAi=zFRaw.search(/(^|\s)&\s/);
const zFTitel=(zFAi>=0?zFRaw.slice(0,zFAi):zFRaw).replace(/__/g,"").trim();
let zFPlain="";const zFK=new Set();zFTitel.split(/(\*[^*]+\*)/).filter(Boolean).forEach(zp=>{const zk=/^\*.*\*$/.test(zp),ztx=zk?zp.slice(1,-1):zp;for(let k=0;k<ztx.length;k++)zk&&zFK.add(zFPlain.length+k);zFPlain+=ztx});
if(!zFK.size){const zm=/(^|[^A-Za-zÄÖÜäöüß])(du|dein|deine|deinen|deinem|deiner|dich|dir)(?![A-Za-zÄÖÜäöüß])/i.exec(zFPlain);let zi=-1,zl=0;if(zm){zi=zm.index+zm[1].length;zl=zm[2].length}else{const zre=/[A-Za-zÄÖÜäöüß\-]+/g;let zw;while((zw=zre.exec(zFPlain))){zw[0].length>zl&&(zl=zw[0].length,zi=zw.index)}}if(zi>=0)for(let k=zi;k<zi+zl;k++)zFK.add(k)}
const zFSz=zSaetze(zFPlain);let zFBr=-1;if(zFSz.length>1){const zf=zFSz[0].trim(),zp=zFPlain.indexOf(zf);zp>=0&&(zFBr=zp+zf.length)}
const zFTeile=[];if(zFBr>0){const zrest=zFPlain.slice(zFBr).replace(/^\s+/,""),zoff=zFPlain.length-zrest.length,za={},zb={};zFK.forEach(k=>{k<zFBr?za[k]={fontStyle:"italic"}:k>=zoff&&(zb[k-zoff]={fontStyle:"italic"})});zFTeile.push([zFPlain.slice(0,zFBr),za],[zrest,zb])}else{const za={};zFK.forEach(k=>{za[k]={fontStyle:"italic"}});zFTeile.push([zFPlain,za])}
const zFw=zW*.76,zfs0=zFPlain.length>120?zW*.07:zW*.082;let zsk=1,zFBx=[],zFH=0;
for(let k=0;k<40;k++){const zfs=zfs0*zsk;zFBx=zFTeile.map(([ztx,zst])=>new zFb.Textbox(ztx,{width:zFw,fontFamily:zFS,fontWeight:"400",fontSize:zfs,lineHeight:.92,charSpacing:-25,fill:"#FFFFFF",textAlign:"center",styles:{0:zst},shadow:new zFb.Shadow({color:"rgba(0,0,0,0.35)",blur:zW*.02,offsetX:0,offsetY:2}),...zNo}));zFH=zFBx.reduce((za,zo)=>za+zo.height,0)+(zFBx.length-1)*zfs*.55;const zlw=Math.max(0,...zFPlain.split(/\s+/).filter(Boolean).map(zwd=>new zFb.Text(zwd,{fontFamily:zFS,fontSize:zfs,charSpacing:-25}).width||0));if(zlw<=zFw*.98&&zFH<=zH*.5)break;zsk*=.94}
let zFy=Math.min(zH*.62-zFH/2,zH*.9-zFH);zFBx.forEach(zo=>{zo.set({left:(zW-zFw)/2,top:zFy});e.add(zo);zFy+=zo.height+zo.fontSize*.55});
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}}
