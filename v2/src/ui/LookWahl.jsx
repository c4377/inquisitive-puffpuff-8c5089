import Vorschau from "./Vorschau.jsx";
import { LOOKS, STANDARD } from "../lib/looks.js";

const BEISPIEL = { id: "beispiel", text: "Du wartest auf Sicherheit. Sicherheit kommt *danach.*" };
const BEISPIEL_TEXT = { id: "beispiel2", text: "Dein boldester Satz ist ihr leisester *Gedanke.*" };

export default function LookWahl({ gewaehlt, brand, foto, onWahl }) {
  return (
    <div className="looks">
      {Object.entries(LOOKS).map(([k, l]) => {
        const look = { ...STANDARD, ...l };
        return (
          <button key={k} className={"look" + (gewaehlt === k ? " an" : "")} onClick={() => onWahl(k)}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 4 }}>
              <Vorschau opts={{ look, brand, tag: { nr: 2 }, folie: BEISPIEL, index: 0, foto }} breite={220} />
              <Vorschau opts={{ look, brand, tag: { nr: 1 }, folie: BEISPIEL_TEXT, index: 0, foto: null }} breite={220} />
            </div>
            <b>{l.name}</b>
            <span>{l.beschreibung}</span>
          </button>
        );
      })}
    </div>
  );
}
