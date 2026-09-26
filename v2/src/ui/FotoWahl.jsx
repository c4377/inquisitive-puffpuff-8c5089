export default function FotoWahl({ fotos, gewaehlt, onWahl, onZu }) {
  return (
    <div className="dialog-hg" onClick={onZu}>
      <div className="dialog" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-kopf">
          <h2>Foto wählen</h2>
          <button className="x" onClick={onZu} aria-label="Schließen">×</button>
        </div>
        {fotos.length === 0 ? (
          <p className="hinweis">Noch keine Fotos. Lade sie unter „Fotos“ hoch.</p>
        ) : (
          <div className="fotoraster">
            {fotos.map((f) => (
              <button key={f.id} className={"foto" + (f.id === gewaehlt ? " an" : "")} onClick={() => onWahl(f.id)}>
                <img src={f.url} alt="" />
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
