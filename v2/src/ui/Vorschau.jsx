import { useEffect, useState } from "react";
import { vorschau } from "../lib/zeichnen.js";

// Vorschaubilder werden nacheinander gezeichnet, damit die Oberflaeche
// beim Laden eines grossen Plans nicht haengt.
const schlange = [];
let laeuft = false;
function einreihen(aufgabe) {
  schlange.push(aufgabe);
  if (!laeuft) weiter();
}
function weiter() {
  const aufgabe = schlange.shift();
  if (!aufgabe) { laeuft = false; return; }
  laeuft = true;
  setTimeout(() => {
    try { aufgabe(); } finally { weiter(); }
  }, 0);
}

export function schluesselFuer(o) {
  return JSON.stringify({
    l: o.look, h: o.brand?.handle, t: o.folie?.text, f: o.foto?.id, g: o.foto?.gesicht,
    a: o.folie?.ausschnitt, m: o.folie?.modus, i: o.index, n: o.tag?.nr, s: !!o.story,
  });
}

export default function Vorschau({ opts, breite = 360, className, alt = "" }) {
  const schluessel = schluesselFuer(opts) + "|" + breite;
  const [url, setUrl] = useState(null);
  useEffect(() => {
    let ab = false;
    einreihen(() => {
      if (ab) return;
      const u = vorschau(opts, schluessel, breite);
      if (!ab) setUrl(u);
    });
    return () => { ab = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [schluessel]);
  return url ? <img src={url} className={className} alt={alt} /> : <div className={className} style={{ aspectRatio: opts.story ? "9/16" : "4/5" }} />;
}
