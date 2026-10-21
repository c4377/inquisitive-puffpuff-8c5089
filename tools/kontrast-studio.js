/* Look „Studio“ zum Ausprobieren (Carina 21.10., Pinterest-Vorlage „Herground“): fette, enge Grotesk (Inter 800),
   Weinrot auf Creme, Rost und Schwarz als Flächen, dunkle Fotos mit weißer Schrift, Mikro-Texte in den Ecken
   (Name oben links, CAPS-Wort oben rechts, Unterzeile klein unten links, Pfeil unten rechts). Das *markierte* Wort
   wird schräg und in Rost gesetzt. Typen im Rhythmus magKontrastFeed: hgcreme, hgrost, hgschwarz, hgfoto.
   Eingeschaltet nur über den Look-Schalter (site/look-schalter.js → window.BS_LOOK_K).
   Wird von editorial-look.py vor den Papier-Zweig gesetzt; alle Zeilenumbrüche werden entfernt. */
if(zxTyp.slice(0,2)==="hg"){
const hT=zxTyp.slice(2),hF=K.kontrastHgSchrift||"Inter";
try{await Promise.race([Promise.all([`800 40px "${hF}"`,`700 40px "${hF}"`,`600 40px "${hF}"`,`italic 800 40px "${hF}"`].map(zq=>document.fonts.load(zq).catch(()=>{}))),new Promise(zr=>setTimeout(zr,4e3))])}catch(zz){}
const hFarben={creme:["#F2ECE4","#3A0E0E","#A3321B","#3A0E0E"],rost:["#A3321B","#F6EEE6","#F6EEE6","#F6EEE6"],schwarz:["#151111","#F6EEE6","#D9573A","#F6EEE6"],foto:["#151111","#FFFFFF","#E8694A","#FFFFFF"]},hC=hFarben[hT]||hFarben.creme,hG=hC[0],hInk=hC[1],hAk=hC[2],hMik=hC[3];
const hWort=String(zKickT||"").replace(/\*+/g,"").replace(/[.!?…:,]+$/,"").trim(),hSub=String(zxSub||zxKl||zxSkriptT||"").replace(/\*+/g,"").trim(),hHdl=String(K.kontrastHandle||"@carinaannaprav");
if(hT==="foto"){zxFotoBG(zxSW(zxFoto,1.05,zxHB,zxPK));try{zxFoto&&(zxFoto.width=zxFoto.height=0)}catch(zz){}e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:"rgba(14,9,7,0.38)",...zNo}));e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,...zNo,fill:new zFb.Gradient({type:"linear",coords:{x1:0,y1:0,x2:0,y2:zH},colorStops:[{offset:0,color:"rgba(0,0,0,0.35)"},{offset:.25,color:"rgba(0,0,0,0)"},{offset:.6,color:"rgba(0,0,0,0.25)"},{offset:1,color:"rgba(0,0,0,0.7)"}]})}))}
else e.add(new zFb.Rect({left:0,top:0,width:zW,height:zH,fill:hG,...zNo}));
const hX=zW*.065,hB=zW*.87,hMk=(ztx,zx,zy,zo)=>new zFb.Text(String(ztx).toLocaleUpperCase("de-DE"),{left:zx,top:zy,fontFamily:hF,fontWeight:"700",fontSize:zW*.0165,charSpacing:30,lineHeight:1.05,fill:hMik,...zNo,...(zo||{})});
e.add(hMk("Carina Anna Prav",hX,zH*.045));
hWort&&e.add(hMk(hWort,zW-hX,zH*.045,{originX:"right",textAlign:"right"}));
const hSg=zxSegs(zxTitel,"wort");let hFs=zW*.15,hTb=null;const hMaxH=hT==="foto"?zH*.5:zH*.6;for(let k=0;k<45;k++){const zsty={};Object.keys(hSg.st).forEach(zk=>{zsty[zk]={fontStyle:"italic",fill:hAk}});hTb=new zFb.Textbox(hSg.plain,{left:hX,top:0,width:hB,fontFamily:hF,fontWeight:"800",fontSize:hFs,lineHeight:.86,charSpacing:-55,fill:hInk,textAlign:"left",styles:{0:zsty},...zNo});const zlw=Math.max(0,...hSg.plain.split(/\s+/).filter(Boolean).map(zwd=>new zFb.Text(zwd,{fontFamily:hF,fontWeight:"800",fontSize:hFs,charSpacing:-55}).width||0));if(zlw<=hB*.99&&hTb.height<=hMaxH)break;hFs*=.95}
const hTy=hT==="foto"?Math.max(zH*.2,zH*.8-(hTb.height||0)):zH*.13;hTb.set({top:hTy});e.add(hTb);
if(hSub){const zs=new zFb.Textbox(hSub.toLocaleUpperCase("de-DE"),{left:hX,top:0,width:zW*.52,fontFamily:hF,fontWeight:"600",fontSize:zW*.019,lineHeight:1.12,charSpacing:10,fill:hMik,...zNo});let zk=0;while(zs.textLines&&zs.textLines.length>3&&zk<10){zs.set({fontSize:zs.fontSize*.92});zs.initDimensions();zk++}const zyS=hT==="foto"?Math.min(zH*.905-(zs.height||0),hTy+(hTb.height||0)+zH*.03):zH*.905-(zs.height||0);zs.set({top:zyS});e.add(zs)}
else e.add(hMk(hHdl,hX,zH*.905));
e.add(new zFb.Text("→",{left:zW-hX,top:zH*.885,originX:"right",fontFamily:hF,fontWeight:"400",fontSize:zW*.06,fill:hMik,...zNo}));
t.overlayImage&&await Ae(t.overlayImage).catch(()=>{});e.renderAll();return}
