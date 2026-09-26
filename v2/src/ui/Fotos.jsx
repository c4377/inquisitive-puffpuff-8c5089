import { useState } from "react";

export default function Fotos({ d }) {
  const [laden, setLaden] = useState(null);
  const hochladen = async (e) => {
    const dateien = [...(e.target.files || [])];
    e.target.value = "";
    if (!dateien.length) return;
    await d.fotosHinzufuegen(dateien, (i, n) => setLaden(`Foto ${i} von ${n} wird vorbereitet …`));
    setLaden(null);
  };
  return (
    <>
      <div className="karte">
        <h2>Deine Fotos</h2>
        <p className="hinweis" style={{ marginTop: 0 }}>
          Hochformat-Fotos von dir wirken am besten. Die App erkennt dein Gesicht und setzt den Text darunter.
          Ein grüner Punkt heißt: Gesicht gefunden. Die Fotos bleiben nur auf diesem Gerät.
        </p>
        <label className="knopf haupt">
          Fotos hinzufügen
          <input type="file" accept="image/*" multiple hidden onChange={hochladen} />
        </label>
        {laden && <p className="hinweis">{laden}</p>}
      </div>
      <div className="fotoraster">
        {d.fotos.map((f) => (
          <div key={f.id} className="foto">
            <img src={f.url} alt="" />
            {f.gesicht && <span className="punkt" title="Gesicht erkannt" />}
            <button className="weg" aria-label="Foto löschen" onClick={() => { if (confirm("Foto löschen? Folien mit diesem Foto werden zu Textposts.")) d.fotoEntfernen(f.id); }}>×</button>
          </div>
        ))}
      </div>
      {d.fotos.length === 0 && <p className="hinweis">Noch keine Fotos.</p>}
    </>
  );
}
