import { folieZeichnen, schriftenLaden, detailWahl } from "./render/render.js";
import { gesichtFinden } from "./render/faces.js";
import { LOOKS, STANDARD } from "./lib/looks.js";

window.__test = async (bilderDaten, lookName, faelle) => {
  const look = { ...STANDARD, ...LOOKS[lookName] };
  await schriftenLaden(look);
  const bilder = await Promise.all(bilderDaten.map((src) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = src; })));
  const gesichter = [];
  for (const b of bilder) gesichter.push(await gesichtFinden(b));
  const aus = [];
  for (const f of faelle) {
    const c = document.createElement("canvas");
    const bild = f.bild != null ? bilder[f.bild] : null;
    folieZeichnen(c, {
      format: f.format || "feed", look, brand: { handle: "carinaannaprav" },
      folie: { text: f.text }, rolle: f.rolle, bild, gesicht: bild ? gesichter[f.bild] : null,
      fotoModus: f.modus || "farbe", detail: f.detail || null,
    });
    aus.push(c.toDataURL("image/jpeg", 0.85));
  }
  return { aus, gesichter };
};
window.__bereit = true;
