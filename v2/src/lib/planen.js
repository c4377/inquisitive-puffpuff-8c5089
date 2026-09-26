// Aus importierten Tagen wird der Plan: Welche Tage sind Textposts, welche
// Folie bekommt welches Foto. Alles laesst sich danach im Editor aendern.
import { neueId } from "./db.js";

export function tagIstText(nr, look) {
  const jede = Number(look.textJede) || 0;
  return jede > 0 && (nr - 1) % jede === 0;
}

// Fotos der Reihe nach verteilen, pro Tag moeglichst ohne Wiederholung.
export function fotosVerteilen(tage, fotoIds, look, start = 0) {
  let zeiger = start;
  return tage.map((tag) => {
    const text = tagIstText(tag.nr, look);
    const benutzt = new Set();
    const nimm = () => {
      if (!fotoIds.length) return null;
      for (let i = 0; i < fotoIds.length; i++) {
        const id = fotoIds[(zeiger + i) % fotoIds.length];
        if (!benutzt.has(id) || benutzt.size >= fotoIds.length) {
          zeiger = (zeiger + i + 1) % fotoIds.length;
          benutzt.add(id);
          return id;
        }
      }
      return null;
    };
    return {
      ...tag,
      slides: tag.slides.map((s) => ({ ...s, fotoId: text ? null : s.fotoId ?? nimm() })),
      stories: (tag.stories || []).map((s) => ({ ...s, fotoId: s.fotoId ?? nimm() })),
    };
  });
}

// Import in den bestehenden Plan uebernehmen.
//   modus "anhaengen": neue Tage hinten anfuegen und weiterzaehlen
//   modus "ersetzen":  den Plan komplett ersetzen
export function importUebernehmen(plan, neueTage, fotoIds, look, modus) {
  const alt = modus === "ersetzen" ? [] : plan.tage || [];
  const letzte = alt.reduce((m, t) => Math.max(m, t.nr), 0);
  const nummeriert = neueTage.map((t, i) => ({
    ...t,
    id: t.id || neueId(),
    nr: modus === "ersetzen" ? t.nr || i + 1 : letzte + i + 1,
  }));
  const verteilt = fotosVerteilen(nummeriert, fotoIds, look, (plan.fotoZeiger || 0) + alt.length);
  return { ...plan, tage: [...alt, ...verteilt], fotoZeiger: (plan.fotoZeiger || 0) + verteilt.length };
}

export function neuerTag(plan) {
  const nr = (plan.tage || []).reduce((m, t) => Math.max(m, t.nr), 0) + 1;
  return { id: neueId(), nr, titel: `Tag ${nr}`, caption: "", slides: [{ id: neueId(), text: "Neuer Text", fotoId: null }], stories: [] };
}
