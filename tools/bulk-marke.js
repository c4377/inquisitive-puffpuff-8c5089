/* Marken-Check beim Bulk Import (Carina 22.10.: „ich erstelle immer Posts, die dann das Branding sprengen“, Grund: zu viel Text).
   Läuft einmal beim Klick auf „Plan erstellen“, nach dem Einlesen (JK) und vor dem Anlegen der Posts. Ändert keine Worte,
   verteilt nur an Satzgrenzen um:
   - Cover (Slide 1): Hook (vor dem „&“, ohne [Rubrik] / VERSAL-Einstieg) über BS_BULK_HOOK Zeichen (Grundwert 90) →
     die ersten Sätze bleiben auf dem Cover, der Rest kommt als neue Folie 2. Ein einzelner langer Satz wird am
     Doppelpunkt oder Gedankenstrich geteilt, sonst bleibt er und wird gemeldet. Handschrift-Zeile (nach „&“) über
     BS_BULK_ZEILE Zeichen (80) → nur ihr erster Satz bleibt, der Rest wandert mit auf die neue Folie.
   - Folgefolien über BS_BULK_FOLIE Zeichen (230) → an Absätzen, Zeilen und Sätzen auf gleich volle Folien geteilt.
     Zeilen mit Auszeichnung (#, >, -, →, 1. …) bleiben ganz, eine Zeile mit „:“ am Ende bleibt bei der nächsten.
   - Sonderfolien (Vorher/Nachher, Screenshot, Kennungen S-/T-/W-) bleiben unangetastet.
   Am Ende eine kleine Meldung unten im Bild, was umverteilt wurde (und was zu lang bleibt).
   Wird von editorial-look.py als Ausdruck „__bsMarkeF=…“ eingesetzt; alle Zeilenumbrüche werden entfernt (kein // im Code). */
(zPl)=>{try{if(!Array.isArray(zPl)||window.BS_BULK_AUS===1)return zPl;
const zMaxH=Number(window.BS_BULK_HOOK)||90,zMaxZ=Number(window.BS_BULK_ZEILE)||80,zMaxF=Number(window.BS_BULK_FOLIE)||230,zBer=[];
const zLen=x=>String(x||"").replace(/\*+|_{2}/g,"").replace(/\s+/g," ").trim().length;
const zSonder=x=>/(?:^|[\s:|])[STW]-[A-Z0-9]{4,6}\b|\b(?:Vorher|Nachher|Screenshot)\s*:/i.test(String(x||""));
const zAbk=/\b(z\. ?B|d\. ?h|u\. ?a|bzw|ca|Nr|etc|inkl|evtl|ggf|usw|vs|Dr|Mio|Mrd|Std|Min)\./g;
const zSaetze=x=>{const zs=String(x||"").replace(zAbk,zm=>zm.replace(/\./g,"․")).replace(/(\d)\.(?=\s*\d)/g,"$1․");const zr=zs.match(/[^.!?…]+(?:[.!?…]+[\"“”»«'’)]*|$)\s*/g)||[zs];return zr.map(zq=>zq.replace(/․/g,".").trim()).filter(Boolean)};
const zAusz=zl=>/^\s*(?:#{1,2}\s|>\s|[-→•]\s|\d+[.)]\s|!\s|\||\[(?:mitte|links)\])/i.test(zl);
const zFolgeTeilen=(zTx,zTag,zNr)=>{if(zLen(zTx)<=zMaxF||zSonder(zTx))return[zTx];
const zEin=[];String(zTx).split(/\n\s*\n/).forEach((zAbs,zai)=>{zAbs.split("\n").filter(zl=>zl.trim()).forEach((zl,zli)=>{const zst=zAusz(zl)?[zl.trim()]:zSaetze(zl);zst.forEach((zs,zsi)=>zEin.push({t:zs,a:zai,l:zai+"/"+zli,neuAbs:zli===0&&zsi===0}))})});
for(let k=zEin.length-2;k>=0;k--){if(/:\s*$/.test(zEin[k].t)){const zn=zEin[k+1];zEin[k]={...zEin[k],t:zEin[k].t+(zn.l===zEin[k].l?" ":"\n")+zn.t,l:zn.l,a:zn.a};zEin.splice(k+1,1)}}
const zGes=zEin.reduce((zs,ze)=>zs+zLen(ze.t),0),zAnz=Math.max(2,Math.ceil(zGes/zMaxF)),zZiel=zGes/zAnz,zTeile=[];let zAkt=[],zAktL=0;
zEin.forEach(ze=>{const zL=zLen(ze.t);if(zAkt.length&&(zAktL+zL>zMaxF||(zTeile.length<zAnz-1&&((ze.neuAbs&&zAktL>=zZiel*.5)||(zAktL>=zZiel*.8&&zAktL+zL>zZiel*1.15))))){zTeile.push(zAkt);zAkt=[];zAktL=0}zAkt.push(ze);zAktL+=zL});zAkt.length&&zTeile.push(zAkt);
const zOut=zTeile.map(zg=>zg.reduce((zs,ze,k)=>k===0?ze.t:zs+(ze.a!==zg[k-1].a?"\n\n":ze.l!==zg[k-1].l?"\n":" ")+ze.t,""));
zOut.some(zo=>zLen(zo)>zMaxF*1.15)&&zBer.push("Tag "+zTag+": ein Satz auf Folie "+zNr+" ist allein schon sehr lang, bitte kürzen");
zOut.length>1&&zBer.push("Tag "+zTag+": Folie "+zNr+" auf "+zOut.length+" Folien verteilt");return zOut};
zPl.forEach(zP=>{if(!zP||!Array.isArray(zP.slides)||!zP.slides.length)return;const zTag=zP.day;let zSl=zP.slides.map(zs=>typeof zs=="string"?zs:String((zs&&zs.text)||""));
const zC=zSl[0];if(!zSonder(zC)){let zRest=zC,zVor="";const zRm=/^\s*\[[^\]\n]{2,24}\]\s*/.exec(zRest);zRm&&(zVor=zRm[0],zRest=zRest.slice(zRm[0].length));
if(!zRm){const zKm=/^\s*((?:[A-ZÄÖÜ][A-ZÄÖÜß0-9&\-]*[A-ZÄÖÜß0-9][ \t]*){1,3}[:|·•–—][ \t]*)(?=\S)/.exec(zRest);zKm&&(zVor=zKm[0],zRest=zRest.slice(zKm[0].length))}
const zAi=zRest.search(/\s&\s/);let zHook=zAi>=0?zRest.slice(0,zAi):zRest,zZeile=zAi>=0?zRest.slice(zAi).replace(/^\s*&\s*/,""):"",zWeg=[];
if(zLen(zHook)>zMaxH){const zs=zSaetze(zHook.replace(/\n/g," "));let zBl=[];for(const zq of zs){if(!zBl.length||zLen(zBl.join(" ")+" "+zq)<=zMaxH)zBl.push(zq);else break}
if(zBl.length<zs.length){zWeg=zs.slice(zBl.length);zHook=zBl.join(" ")}
if(zLen(zHook)>zMaxH){const zm=/^(.{25,}?(?::|\s[–—]))\s+(.+)$/.exec(zHook);if(zm&&zLen(zm[1])<=zMaxH){zHook=zm[1];zWeg.unshift(zm[2])}}
zLen(zHook)>zMaxH&&zBer.push("Tag "+zTag+": der Hook ist ein einziger langer Satz ("+zLen(zHook)+" Zeichen), bitte kürzen")}
if(zZeile&&zLen(zZeile)>zMaxZ){const zs=zSaetze(zZeile);if(zLen(zs[0])<=zMaxZ&&zs.length>1){zWeg.push(zs.slice(1).join(" "));zZeile=zs[0]}else{zWeg.push(zZeile);zZeile=""}}
if(zWeg.length){zSl[0]=zVor+zHook.trim()+(zZeile?" & "+zZeile.trim():"");zSl.splice(1,0,zWeg.join(" ").trim());zBer.push("Tag "+zTag+": Cover gekürzt, der Rest steht jetzt auf Folie 2")}}
const zNeu=[zSl[0]];for(let k=1;k<zSl.length;k++){zFolgeTeilen(zSl[k],zTag,zNeu.length+1).forEach(zt=>zNeu.push(zt))}
zNeu.length>20&&zBer.push("Tag "+zTag+": "+zNeu.length+" Folien, Instagram nimmt höchstens 20");
const zOrig=zP.slides;zP.slides=zNeu.map((zt,k)=>{const zo=zOrig[k];return zo&&typeof zo=="object"&&zo.text===zt?zo:zt})});
if(zBer.length){try{const zd=document.createElement("div");zd.setAttribute("role","status");zd.style.cssText="position:fixed;left:12px;right:12px;top:14px;z-index:2147483647;max-width:520px;margin:0 auto;background:#3A2E25;color:#EDE7DD;border-radius:14px;padding:14px 16px 12px;font:13px/1.45 system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.35)";
const zh=document.createElement("div");zh.textContent="Marken-Check: zu viel Text umverteilt";zh.style.cssText="font-weight:700;margin-bottom:6px;color:#fff";zd.appendChild(zh);
zBer.slice(0,8).forEach(zt=>{const zz=document.createElement("div");zz.textContent="· "+zt;zd.appendChild(zz)});zBer.length>8&&zd.appendChild(Object.assign(document.createElement("div"),{textContent:"· und "+(zBer.length-8)+" weitere"}));
const zx=document.createElement("button");zx.textContent="OK";zx.style.cssText="margin-top:10px;background:#B9A68A;color:#3A2E25;border:0;border-radius:8px;padding:6px 14px;font-weight:700";zx.onclick=()=>zd.remove();zd.appendChild(zx);document.body.appendChild(zd);setTimeout(()=>zd.remove(),25e3)}catch(zz){}}
window.__bsBulkBericht=zBer;return zPl}catch(zz){console.warn("Marken-Check",zz);return zPl}}
