// Story-Highlight-Cover (Carina 17.10.: „Mach Highlight-Bilder und mach's damit echt zur Boutique“).
// Rendert 1080×1920-Cover in zwei Reihen (hell/dunkel) nach site/highlights/. Aufruf aus dem Projektordner:
//   node tools/highlights.mjs   (braucht den lokalen Server auf Port 8899, der site/ ausliefert)
import {chromium} from '/opt/node22/lib/node_modules/playwright/index.mjs';
const THEMEN=[['Über mich'],['Verkaufs-','lücke'],['Storytelling'],['Vorher','Nachher'],['Stimmen'],['Notizen'],['Buchen']];
const REIHEN={hell:{bg:'#F4F1EC',ink:'#141414',linie:'#C08276',nr:'#8A8A8A',korn:.10},dunkel:{bg:'#141414',ink:'#FFFFFF',linie:'#E7CCC6',nr:'#CFCCC8',korn:.16}};
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const [name,r] of Object.entries(REIHEN)){for(let i=0;i<THEMEN.length;i++){const nr=String(i+1).padStart(2,'0');
await p.goto('http://127.0.0.1:8899/highlights/vorlage.html');
await p.evaluate(({r,w,nr})=>window.zeichne(r,w,nr),{r,w:THEMEN[i],nr});
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:`site/highlights/${name}-${nr}.jpg`,type:'jpeg',quality:92});}}
await b.close();console.log('fertig');
