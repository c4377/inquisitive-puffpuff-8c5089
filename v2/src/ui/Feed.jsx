import { useState } from "react";
import Vorschau from "./Vorschau.jsx";
import ImportDialog from "./ImportDialog.jsx";

export default function Feed({ d, look, fotoVon, onTag, onImport, onNeuerTag, onAllesSichern }) {
  const [importOffen, setImportOffen] = useState(false);
  const tage = [...(d.plan.tage || [])].sort((a, z) => z.nr - a.nr);

  return (
    <>
      <div className="knopfreihe" style={{ margin: "4px 0 14px" }}>
        <button className="knopf haupt" onClick={() => setImportOffen(true)}>Texte importieren</button>
        <button className="knopf" onClick={onNeuerTag}>Neuer Tag</button>
        {tage.length > 0 && <button className="knopf" onClick={onAllesSichern}>Alles sichern</button>}
      </div>

      {tage.length === 0 ? (
        <div className="leer">
          <h2>Dein Feed ist noch leer</h2>
          <p>Importiere deine Texte, und die App baut daraus Karussells mit deinen Fotos.</p>
          <button className="knopf haupt" onClick={() => setImportOffen(true)}>Texte importieren</button>
        </div>
      ) : (
        <div className="raster">
          {tage.map((t) => (
            <button key={t.id} className="kachel" onClick={() => onTag(t.id)}>
              {t.slides[0] && (
                <Vorschau opts={{ look, brand: d.brand, tag: t, folie: t.slides[0], index: 0, foto: fotoVon(t.slides[0].fotoId) }} />
              )}
              <span className="marke">Tag {t.nr}</span>
            </button>
          ))}
        </div>
      )}

      {importOffen && (
        <ImportDialog hatPlan={tage.length > 0} onZu={() => setImportOffen(false)}
          onUebernehmen={(neu, modus) => { onImport(neu, modus); setImportOffen(false); }} />
      )}
    </>
  );
}
