import { useState } from "react";
import FotoWahl from "./FotoWahl.jsx";

const AUSSCHNITTE = [
  ["auto", "Auto"], ["gesicht", "Gesicht"], ["close", "Nah"], ["bust", "Brust"],
  ["lower", "Unten"], ["full", "Ganz"], ["eigen", "Eigen"],
];

// Bearbeitet eine Folie oder Story: Text, Foto/Textpost, Ausschnitt, Farbe.
export default function FolienEditor({ folie, fotos, onAendern, story = false }) {
  const [wahlOffen, setWahlOffen] = useState(false);
  const setze = (patch) => onAendern({ ...folie, ...patch });
  const eigen = folie.ausschnitt && typeof folie.ausschnitt === "object";
  const aus = eigen ? "eigen" : folie.ausschnitt || "auto";
  const hand = eigen ? folie.ausschnitt : { x: 0.5, y: 0.4, zoom: 1.2 };

  return (
    <div>
      <div className="feld">
        <label htmlFor="folientext">Text</label>
        <textarea id="folientext" value={folie.text} onChange={(e) => setze({ text: e.target.value })} />
        <span className="hinweis">
          Erste Zeile in GROSSBUCHSTABEN = kleines Wort oben · Zeile mit „/“ = kleine Zeile darunter ·
          *Wort* = Akzent · **Wort** = fett · Leerzeile = Absatz
        </span>
      </div>

      {!story && (
        <div className="feld">
          <label>Art</label>
          <div className="segment">
            <button className={folie.fotoId ? "an" : ""} onClick={() => (folie.fotoId ? null : setWahlOffen(true))}>Foto</button>
            <button className={!folie.fotoId ? "an" : ""} onClick={() => setze({ fotoId: null })}>Textpost</button>
          </div>
        </div>
      )}

      {(folie.fotoId || story) && (
        <>
          <div className="feld">
            <label>Foto</label>
            <div className="knopfreihe">
              <button className="knopf klein" onClick={() => setWahlOffen(true)}>{folie.fotoId ? "Foto ändern" : "Foto wählen"}</button>
            </div>
          </div>
          {folie.fotoId && (
            <>
              <div className="feld">
                <label>Ausschnitt</label>
                <div className="segment">
                  {AUSSCHNITTE.map(([k, n]) => (
                    <button key={k} className={aus === k ? "an" : ""}
                      onClick={() => setze({ ausschnitt: k === "eigen" ? hand : k === "auto" ? undefined : k })}>{n}</button>
                  ))}
                </div>
              </div>
              {eigen && (
                <div className="karte" style={{ padding: 12 }}>
                  <div className="feld"><label>Zoom</label>
                    <input type="range" min="1" max="2.6" step="0.02" value={hand.zoom}
                      onChange={(e) => setze({ ausschnitt: { ...hand, zoom: Number(e.target.value) } })} /></div>
                  <div className="feld"><label>Links – rechts</label>
                    <input type="range" min="0" max="1" step="0.01" value={hand.x}
                      onChange={(e) => setze({ ausschnitt: { ...hand, x: Number(e.target.value) } })} /></div>
                  <div className="feld"><label>Oben – unten</label>
                    <input type="range" min="0" max="1" step="0.01" value={hand.y}
                      onChange={(e) => setze({ ausschnitt: { ...hand, y: Number(e.target.value) } })} /></div>
                </div>
              )}
              <div className="feld">
                <label>Farbe</label>
                <div className="segment">
                  {[[undefined, "Auto"], ["farbe", "Farbe"], ["sw", "Schwarz-Weiß"]].map(([k, n]) => (
                    <button key={n} className={folie.modus === k ? "an" : ""} onClick={() => setze({ modus: k })}>{n}</button>
                  ))}
                </div>
              </div>
            </>
          )}
        </>
      )}

      {wahlOffen && (
        <FotoWahl fotos={fotos} gewaehlt={folie.fotoId}
          onWahl={(id) => { setze({ fotoId: id }); setWahlOffen(false); }}
          onZu={() => setWahlOffen(false)} />
      )}
    </div>
  );
}
