import { useState } from "react";
import Vorschau from "./Vorschau.jsx";
import FolienEditor from "./FolienEditor.jsx";
import { neueId } from "../lib/db.js";

export default function Stories({ d, look, fotoVon, onTagAendern, onSichern }) {
  const [offen, setOffen] = useState(null); // { tagId, storyId }
  const tage = [...(d.plan.tage || [])].sort((a, z) => a.nr - z.nr);
  const tag = offen && tage.find((t) => t.id === offen.tagId);
  const story = tag && tag.stories.find((s) => s.id === offen.storyId);

  const neu = (t) => {
    const s = { id: neueId(), text: "Neue Story", fotoId: d.fotos[0]?.id ?? null };
    onTagAendern({ ...t, stories: [...(t.stories || []), s] });
    setOffen({ tagId: t.id, storyId: s.id });
  };

  if (!tage.length) {
    return <div className="leer"><h2>Noch keine Tage</h2><p>Importiere zuerst Texte. Stories schreibst du im Import mit „Story 1:“.</p></div>;
  }

  return (
    <>
      <p className="hinweis" style={{ marginTop: 0 }}>Stories im Format 9:16, pro Tag. Im Import mit „Story 1:“, „Story 2:“ …</p>
      {tage.map((t) => (
        <div className="karte" key={t.id}>
          <div className="zeile" style={{ marginBottom: 10 }}>
            <h2 style={{ margin: 0 }}>Tag {t.nr}{t.titel && t.titel !== `Tag ${t.nr}` ? ` · ${t.titel}` : ""}</h2>
            <div className="knopfreihe" style={{ justifyContent: "flex-end" }}>
              <button className="knopf klein" onClick={() => neu(t)}>+ Story</button>
              {(t.stories || []).length > 0 && <button className="knopf klein" onClick={() => onSichern(t)}>Sichern</button>}
            </div>
          </div>
          {(t.stories || []).length === 0 ? (
            <p className="hinweis" style={{ margin: 0 }}>Keine Stories.</p>
          ) : (
            <div className="streifen">
              {t.stories.map((s, k) => (
                <button key={s.id} style={{ flexBasis: 96 }} onClick={() => setOffen({ tagId: t.id, storyId: s.id })}>
                  <Vorschau opts={{ look, brand: d.brand, tag: t, folie: s, index: k, foto: fotoVon(s.fotoId), story: true }} breite={200} />
                </button>
              ))}
            </div>
          )}
        </div>
      ))}

      {story && (
        <div className="dialog-hg" onClick={() => setOffen(null)}>
          <div className="dialog" onClick={(e) => e.stopPropagation()}>
            <div className="dialog-kopf">
              <h2>Story · Tag {tag.nr}</h2>
              <button className="x" onClick={() => setOffen(null)} aria-label="Schließen">×</button>
            </div>
            <div style={{ maxWidth: 240, margin: "0 auto 12px" }}>
              <Vorschau opts={{ look, brand: d.brand, tag, folie: story, index: 0, foto: fotoVon(story.fotoId), story: true }} breite={480} className="vorschau-gross" />
            </div>
            <FolienEditor story folie={story} fotos={d.fotos}
              onAendern={(neuS) => onTagAendern({ ...tag, stories: tag.stories.map((s) => (s.id === story.id ? neuS : s)) })} />
            <button className="knopf gefahr klein" onClick={() => {
              onTagAendern({ ...tag, stories: tag.stories.filter((s) => s.id !== story.id) });
              setOffen(null);
            }}>Story löschen</button>
          </div>
        </div>
      )}
    </>
  );
}
