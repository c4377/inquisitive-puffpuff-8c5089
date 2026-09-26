import { useState } from "react";

export default function Captions({ d, onTagAendern }) {
  const [kopiert, setKopiert] = useState(null);
  const tage = [...(d.plan.tage || [])].sort((a, z) => a.nr - z.nr);
  const kopieren = async (t) => {
    try {
      await navigator.clipboard.writeText(t.caption || "");
      setKopiert(t.id);
      setTimeout(() => setKopiert(null), 1500);
    } catch {
      alert("Kopieren ist in diesem Browser nicht erlaubt. Markiere den Text und kopiere ihn von Hand.");
    }
  };
  if (!tage.length) return <div className="leer"><h2>Noch keine Tage</h2><p>Captions kommen mit dem Import („Caption:“) oder du schreibst sie hier.</p></div>;
  return (
    <div className="captions">
      {tage.map((t) => (
        <div className="karte" key={t.id}>
          <div className="zeile" style={{ marginBottom: 8 }}>
            <h2 style={{ margin: 0 }}>Tag {t.nr}{t.titel && t.titel !== `Tag ${t.nr}` ? ` · ${t.titel}` : ""}</h2>
            <div style={{ textAlign: "right" }}>
              <button className="knopf klein" onClick={() => kopieren(t)} disabled={!t.caption}>{kopiert === t.id ? "Kopiert ✓" : "Kopieren"}</button>
            </div>
          </div>
          <textarea value={t.caption || ""} placeholder="Caption für diesen Tag …" onChange={(e) => onTagAendern({ ...t, caption: e.target.value })} />
          <div className="hinweis">{(t.caption || "").length} / 2200 Zeichen</div>
        </div>
      ))}
    </div>
  );
}
