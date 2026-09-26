import { useState } from "react";
import { parseImport } from "../lib/importParser.js";

const BEISPIEL = `Tag 1: Sichtbarkeit
Slide 1: INSIGHTS
Du wartest auf Sicherheit. Sicherheit kommt *danach.*
/ Kein Trick, keine Formel.
Slide 2: Die meisten wissen längst, was sie wert sind.

Sie trauen sich nur nicht, es laut zu sagen.
Slide 3: Schreib mir START und ich schick dir den *Plan.*
Caption: Hier steht deine Bildunterschrift.
Story 1: Heute im Feed: warum Sicherheit *danach* kommt.

Tag 2: Preise
Slide 1: Dein boldester Satz ist ihr leisester *Gedanke.*`;

export default function ImportDialog({ onUebernehmen, onZu, hatPlan }) {
  const [text, setText] = useState("");
  const [modus, setModus] = useState("anhaengen");
  const tage = parseImport(text);
  const folien = tage.reduce((n, t) => n + t.slides.length, 0);
  const stories = tage.reduce((n, t) => n + t.stories.length, 0);

  return (
    <div className="dialog-hg" onClick={onZu}>
      <div className="dialog" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-kopf">
          <h2>Texte importieren</h2>
          <button className="x" onClick={onZu} aria-label="Schließen">×</button>
        </div>
        <p className="hinweis">
          Schreib „Tag 1:“ für einen neuen Tag und „Slide 1:“ für jede Folie. Alles bis zum nächsten „Slide“
          gehört zur Folie, auch Absätze. Dazu gehen „Caption:“ und „Story 1:“.
        </p>
        <div className="feld">
          <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Tag 1: …" style={{ minHeight: 240, fontFamily: "ui-monospace, Menlo, monospace", fontSize: 14 }} />
        </div>
        <div className="knopfreihe" style={{ marginBottom: 12 }}>
          <button className="knopf klein" onClick={() => setText(BEISPIEL)}>Beispiel einfügen</button>
          {hatPlan && (
            <div className="segment">
              <button className={modus === "anhaengen" ? "an" : ""} onClick={() => setModus("anhaengen")}>Hinten anhängen</button>
              <button className={modus === "ersetzen" ? "an" : ""} onClick={() => setModus("ersetzen")}>Plan ersetzen</button>
            </div>
          )}
        </div>
        <p className="hinweis">{tage.length} Tage · {folien} Folien · {stories} Stories erkannt</p>
        <button className="knopf haupt" disabled={!tage.length} onClick={() => onUebernehmen(tage, modus)}>Übernehmen</button>
      </div>
    </div>
  );
}
