// Export: einzelne Folien als PNG, Tage als ZIP, Teilen in die Fotos-App
// (iPhone/Android) und eine Sicherungsdatei, weil es kein Konto gibt.
import { folieAufCanvas } from "./zeichnen.js";

export function folieBlob(opts) {
  const c = folieAufCanvas(document.createElement("canvas"), opts);
  return new Promise((ok) => c.toBlob((b) => ok(b), "image/png"));
}

export function herunterladen(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

const zwei = (n) => String(n).padStart(2, "0");

// Alle Folien eines Tages (oder mehrerer) als Dateien.
export async function tagDateien(tage, optsFuer) {
  const dateien = [];
  for (const tag of tage) {
    for (let i = 0; i < tag.slides.length; i++) {
      const blob = await folieBlob(optsFuer(tag, tag.slides[i], i, false));
      dateien.push({ name: `Tag-${zwei(tag.nr)}_Folie-${zwei(i + 1)}.png`, blob, ordner: `Tag-${zwei(tag.nr)}` });
    }
    for (let i = 0; i < (tag.stories || []).length; i++) {
      const blob = await folieBlob(optsFuer(tag, tag.stories[i], i, true));
      dateien.push({ name: `Tag-${zwei(tag.nr)}_Story-${zwei(i + 1)}.png`, blob, ordner: `Tag-${zwei(tag.nr)}` });
    }
  }
  return dateien;
}

export async function alsZip(dateien, name) {
  const { default: JSZip } = await import("jszip");
  const zip = new JSZip();
  for (const d of dateien) zip.folder(d.ordner).file(d.name, d.blob);
  herunterladen(await zip.generateAsync({ type: "blob" }), name);
}

// Auf dem Handy: Teilen-Menue ("Bilder sichern"). Sonst Download.
export async function teilenOderLaden(dateien) {
  const files = dateien.map((d) => new File([d.blob], d.name, { type: "image/png" }));
  if (navigator.canShare && navigator.canShare({ files })) {
    try {
      await navigator.share({ files });
      return "geteilt";
    } catch (e) {
      if (e && e.name === "AbortError") return "abgebrochen";
    }
  }
  if (dateien.length === 1) herunterladen(dateien[0].blob, dateien[0].name);
  else await alsZip(dateien, "Folien.zip");
  return "geladen";
}

function blobZuDaten(blob) {
  return new Promise((ok, fehler) => {
    const r = new FileReader();
    r.onload = () => ok(r.result);
    r.onerror = fehler;
    r.readAsDataURL(blob);
  });
}

export async function sicherungErstellen(brand, plan, fotos) {
  const daten = {
    app: "feedstudio",
    version: 1,
    erstellt: new Date().toISOString(),
    brand,
    plan,
    fotos: await Promise.all(fotos.map(async (f) => ({
      id: f.id, name: f.name, gesicht: f.gesicht ?? null, hinzugefuegt: f.hinzugefuegt,
      daten: await blobZuDaten(f.blob),
    }))),
  };
  const blob = new Blob([JSON.stringify(daten)], { type: "application/json" });
  herunterladen(blob, `feedstudio-sicherung-${new Date().toISOString().slice(0, 10)}.json`);
}

export async function sicherungLesen(datei) {
  const daten = JSON.parse(await datei.text());
  if (daten.app !== "feedstudio") throw new Error("Das ist keine Feed-Studio-Sicherung.");
  const fotos = await Promise.all((daten.fotos || []).map(async (f) => ({
    id: f.id, name: f.name, gesicht: f.gesicht, gesichtGeprueft: true, hinzugefuegt: f.hinzugefuegt,
    blob: await (await fetch(f.daten)).blob(),
  })));
  return { brand: daten.brand, plan: daten.plan, fotos };
}
