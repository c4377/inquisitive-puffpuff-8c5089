// Liest den Bulk-Import im Format
//
//   Tag 1: Titel
//   Slide 1: erster Satz …
//   (weitere Zeilen und Leerzeilen gehoeren zur selben Folie)
//   Slide 2: …
//   Caption: Bildunterschrift, darf mehrzeilig sein
//   Story 1: Text fuer eine Story (9:16)
//
// "Folie" statt "Slide" und "Day" statt "Tag" gehen auch. Alles zwischen zwei
// Markern gehoert zum vorherigen Eintrag, Leerzeilen bleiben als Absatz.
import { neueId } from "./db.js";

const TAG = /^(?:tag|day)\s*(\d+)\s*(?:[:.\-–—]\s*(.*))?$/i;
const SLIDE = /^(?:slide|folie)\s*\d+\s*(?:[:.\-–—]\s*)?(.*)$/i;
const STORY = /^story\s*\d+\s*(?:[:.\-–—]\s*)?(.*)$/i;
const CAPTION = /^caption\s*:\s*(.*)$/i;

export function parseImport(input) {
  const tage = [];
  let tag = null;
  let ziel = null; // { art: "slide"|"story"|"caption", zeilen: [] }

  const abschliessen = () => {
    if (!ziel || !tag) return;
    const text = ziel.zeilen.join("\n").replace(/\n{3,}/g, "\n\n").trim();
    if (text) {
      if (ziel.art === "slide") tag.slides.push({ id: neueId(), text });
      else if (ziel.art === "story") tag.stories.push({ id: neueId(), text });
      else tag.caption = text;
    }
    ziel = null;
  };
  const neuerTag = (nr, titel) => {
    abschliessen();
    tag = { id: neueId(), nr, titel: titel || `Tag ${nr}`, caption: "", slides: [], stories: [] };
    tage.push(tag);
  };

  for (const roh of String(input || "").replace(/\r/g, "").split("\n")) {
    const zeile = roh.trim();
    let m;
    if ((m = zeile.match(TAG))) { neuerTag(Number(m[1]), (m[2] || "").trim()); continue; }
    if ((m = zeile.match(SLIDE)) || (m = zeile.match(STORY)) || (m = zeile.match(CAPTION))) {
      if (!tag) neuerTag(1, "");
      abschliessen();
      const art = SLIDE.test(zeile) ? "slide" : STORY.test(zeile) ? "story" : "caption";
      ziel = { art, zeilen: m[1] ? [m[1].trim()] : [] };
      continue;
    }
    if (!tag) neuerTag(1, "");
    if (!ziel) ziel = { art: "slide", zeilen: [] };
    // Leerzeilen am Anfang einer Folie ignorieren, sonst als Absatz behalten
    if (!zeile && !ziel.zeilen.length) continue;
    ziel.zeilen.push(zeile);
  }
  abschliessen();
  return tage.filter((t) => t.slides.length || t.stories.length || t.caption);
}

// Zerlegt den Text einer Folie in ihre Teile:
//   kicker  — kurze erste Zeile in GROSSBUCHSTABEN (klein ueber dem Satz)
//   unter   — Zeilen, die mit "/" beginnen (kleine Zeile darunter)
//   haupt   — der Rest, mit Zeilenumbruechen und Absaetzen
export function teileFolie(text) {
  const zeilen = String(text || "").replace(/\r/g, "").split("\n");
  let kicker = "";
  const erste = zeilen.findIndex((z) => z.trim());
  if (erste >= 0 && zeilen.length - erste > 1) {
    const z = zeilen[erste].trim();
    if (/^[A-ZÄÖÜ0-9 &\-.:#!?]{2,24}$/.test(z) && /[A-ZÄÖÜ]/.test(z)) {
      kicker = z;
      zeilen.splice(erste, 1);
    }
  }
  const unter = [];
  const rest = [];
  for (const z of zeilen) {
    if (/^\s*\//.test(z)) unter.push(z.replace(/^\s*\/\s*/, "").trim());
    else rest.push(z);
  }
  const haupt = rest.join("\n").replace(/^\s+|\s+$/g, "").replace(/\n{3,}/g, "\n\n");
  return { kicker, haupt, unter: unter.filter(Boolean).join(" ") };
}

// Markierungen im Satz:  *Wort* = Akzent (kursiv),  **Wort** = fett.
// Ergebnis: Absaetze -> Zeilen -> Woerter mit Stil. Ein Absatz ist durch
// eine Leerzeile getrennt, eine Zeile durch einen einfachen Umbruch.
export function markierungen(text) {
  const absaetze = String(text || "").split(/\n\s*\n/);
  let akzentGesehen = false;
  const ergebnis = absaetze.map((absatz) =>
    absatz.split("\n").map((zeile) => {
      const woerter = [];
      let fett = false, akzent = false;
      const teile = zeile.split(/(\*\*|\*)/);
      let puffer = "";
      const flush = () => {
        for (const w of puffer.split(/\s+/)) if (w) woerter.push({ w, fett, akzent });
        puffer = "";
      };
      for (const t of teile) {
        if (t === "**") { flush(); fett = !fett; continue; }
        if (t === "*") { flush(); akzent = !akzent; if (akzent) akzentGesehen = true; continue; }
        // Satzzeichen direkt hinter einer Markierung haengt am Wort davor
        if (/^[.,!?;:…"“”»«)]/.test(t) && woerter.length && !puffer) {
          const m = t.match(/^([.,!?;:…"“”»«)]+)(.*)$/s);
          woerter[woerter.length - 1].w += m[1];
          puffer = m[2];
          continue;
        }
        puffer += t;
      }
      flush();
      return woerter;
    }).filter((z, i, a) => z.length || a.length === 1)
  );
  return { absaetze: ergebnis, akzentGesehen };
}
