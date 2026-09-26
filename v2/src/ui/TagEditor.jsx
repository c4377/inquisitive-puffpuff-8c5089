import { useState } from "react";
import Vorschau from "./Vorschau.jsx";
import FolienEditor from "./FolienEditor.jsx";
import { neueId } from "../lib/db.js";

export default function TagEditor({ tag, d, look, fotoVon, onAendern, onLoeschen, onSichern }) {
  const [idx, setIdx] = useState(0);
  const i = Math.min(idx, Math.max(0, tag.slides.length - 1));
  const folie = tag.slides[i];

  const folienSetzen = (slides) => onAendern({ ...tag, slides });
  const aendern = (neu) => folienSetzen(tag.slides.map((s, k) => (k === i ? neu : s)));
  const verschieben = (r) => {
    const j = i + r;
    if (j < 0 || j >= tag.slides.length) return;
    const s = [...tag.slides];
    [s[i], s[j]] = [s[j], s[i]];
    folienSetzen(s);
    setIdx(j);
  };
  const hinzufuegen = () => {
    const vorlage = tag.slides[tag.slides.length - 1];
    folienSetzen([...tag.slides, { id: neueId(), text: "Neuer Text", fotoId: vorlage ? vorlage.fotoId : null }]);
    setIdx(tag.slides.length);
  };
  const entfernen = () => {
    if (tag.slides.length <= 1) return;
    folienSetzen(tag.slides.filter((_, k) => k !== i));
    setIdx(Math.max(0, i - 1));
  };
  const opts = (s, k) => ({ look, brand: d.brand, tag, folie: s, index: k, foto: fotoVon(s.fotoId) });

  return (
    <>
      {folie && <Vorschau opts={opts(folie, i)} breite={880} className="vorschau-gross" />}
      <div className="streifen">
        {tag.slides.map((s, k) => (
          <button key={s.id} className={k === i ? "an" : ""} onClick={() => setIdx(k)} aria-label={`Folie ${k + 1}`}>
            <Vorschau opts={opts(s, k)} breite={140} />
          </button>
        ))}
        <button className="plus" onClick={hinzufuegen} aria-label="Folie hinzufügen">+</button>
      </div>

      <div className="knopfreihe" style={{ marginBottom: 14 }}>
        <button className="knopf klein" onClick={() => verschieben(-1)} disabled={i === 0}>← Nach vorn</button>
        <button className="knopf klein" onClick={() => verschieben(1)} disabled={i >= tag.slides.length - 1}>Nach hinten →</button>
        <button className="knopf klein gefahr" onClick={entfernen} disabled={tag.slides.length <= 1}>Folie löschen</button>
      </div>

      {folie && (
        <div className="karte">
          <h2>Folie {i + 1} von {tag.slides.length}</h2>
          <FolienEditor folie={folie} fotos={d.fotos} onAendern={aendern} />
          <div className="knopfreihe">
            <button className="knopf haupt" onClick={() => onSichern([tag], i)}>Diese Folie sichern</button>
            <button className="knopf" onClick={() => onSichern([tag])}>Ganzen Tag sichern</button>
          </div>
        </div>
      )}

      <div className="karte">
        <h2>Tag {tag.nr}</h2>
        <div className="feld">
          <label htmlFor="tagtitel">Thema (nur für dich)</label>
          <input id="tagtitel" type="text" value={tag.titel || ""} onChange={(e) => onAendern({ ...tag, titel: e.target.value })} />
        </div>
        <div className="feld">
          <label htmlFor="tagcaption">Caption</label>
          <textarea id="tagcaption" value={tag.caption || ""} onChange={(e) => onAendern({ ...tag, caption: e.target.value })} />
        </div>
        <button className="knopf klein gefahr" onClick={() => { if (confirm(`Tag ${tag.nr} wirklich löschen?`)) onLoeschen(); }}>Tag löschen</button>
      </div>
    </>
  );
}
