// Bruecke zwischen Plan und Zeichenmaschine: setzt fuer eine Folie Rolle,
// Foto-Modus (SW/Farbe) und Ausschnitt zusammen und zeichnet sie.
import { folieZeichnen, detailWahl } from "../render/render.js";

export function folienOptionen({ look, brand, tag, folie, index, foto, story = false }) {
  const rolle = story ? "story" : index === 0 ? "titel" : "folge";
  const reihe = look.fotoReihe || ["farbe"];
  const fotoModus = folie.modus || reihe[((tag?.nr || 1) - 1 + reihe.length * 100) % reihe.length];
  let detail = null;
  let hand = null;
  const a = folie.ausschnitt;
  if (a && typeof a === "object") hand = a;
  else if (a && a !== "auto" && a !== "gesicht") detail = a;
  else if (!a || a === "auto") detail = story ? null : detailWahl(look, rolle, folie.text, foto?.id || "", index);
  return {
    format: story ? "story" : "feed",
    look, brand, folie, rolle,
    bild: foto?.img || null,
    gesicht: foto?.gesicht || null,
    fotoModus, detail, hand,
  };
}

export function folieAufCanvas(canvas, opts) {
  folieZeichnen(canvas, folienOptionen(opts));
  return canvas;
}

// Kleines Vorschaubild als Daten-URL, mit Zwischenspeicher.
const cache = new Map();
export function vorschau(opts, schluessel, breite = 360) {
  if (schluessel && cache.has(schluessel)) return cache.get(schluessel);
  const gross = document.createElement("canvas");
  folieAufCanvas(gross, opts);
  const klein = document.createElement("canvas");
  klein.width = breite;
  klein.height = Math.round((gross.height / gross.width) * breite);
  klein.getContext("2d").drawImage(gross, 0, 0, klein.width, klein.height);
  const url = klein.toDataURL("image/jpeg", 0.85);
  if (schluessel) {
    if (cache.size > 400) cache.delete(cache.keys().next().value);
    cache.set(schluessel, url);
  }
  return url;
}

export function vorschauLeeren() {
  cache.clear();
}
