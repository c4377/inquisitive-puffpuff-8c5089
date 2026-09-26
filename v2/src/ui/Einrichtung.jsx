import { useRef, useState } from "react";
import LookWahl from "./LookWahl.jsx";
import { sicherungLesen } from "../lib/export.js";

// Erster Start: Name, Handle, Fotos, Look. Danach geht es direkt in den Feed.
export default function Einrichtung({ d, onFertig }) {
  const [schritt, setSchritt] = useState(0);
  const [name, setName] = useState(d.brand?.name || "");
  const [handle, setHandle] = useState(d.brand?.handle || "");
  const [look, setLook] = useState(d.brand?.look || "klassisch");
  const [laden, setLaden] = useState(null);
  const sicherung = useRef(null);

  const hochladen = async (e) => {
    const dateien = [...(e.target.files || [])];
    e.target.value = "";
    if (!dateien.length) return;
    await d.fotosHinzufuegen(dateien, (i, n) => setLaden(`Foto ${i} von ${n} wird vorbereitet …`));
    setLaden(null);
  };
  const brand = { name, handle: handle.replace(/^@/, "").trim() };

  return (
    <div className="app" style={{ paddingTop: 28 }}>
      {schritt === 0 && (
        <div className="karte">
          <div className="schritt">Schritt 1 von 3</div>
          <div className="gross-titel">Willkommen in deinem Feed Studio</div>
          <p className="hinweis">Aus deinen Texten und Fotos entstehen Karussells und Stories in deinem eigenen Look. Alles bleibt auf diesem Gerät, du brauchst kein Konto.</p>
          <div className="feld">
            <label htmlFor="name">Dein Name oder Markenname</label>
            <input id="name" type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="z. B. Anna Beispiel" />
          </div>
          <div className="feld">
            <label htmlFor="handle">Instagram-Name (steht unten auf jeder Folie)</label>
            <input id="handle" type="text" value={handle} onChange={(e) => setHandle(e.target.value)} placeholder="z. B. annabeispiel" autoCapitalize="none" />
          </div>
          <button className="knopf haupt" disabled={!name.trim()} onClick={() => setSchritt(1)}>Weiter</button>
          <p className="hinweis" style={{ marginTop: 18 }}>
            Du hast schon eine Sicherung von einem anderen Gerät?{" "}
            <button className="knopf klein" onClick={() => sicherung.current?.click()}>Sicherung einspielen</button>
          </p>
          <input ref={sicherung} type="file" accept="application/json,.json" hidden onChange={async (e) => {
            const f = e.target.files?.[0];
            e.target.value = "";
            if (!f) return;
            try { await d.sicherungEinspielen(await sicherungLesen(f)); onFertig(); }
            catch (err) { alert(err.message || "Die Datei konnte nicht gelesen werden."); }
          }} />
        </div>
      )}

      {schritt === 1 && (
        <div className="karte">
          <div className="schritt">Schritt 2 von 3</div>
          <div className="gross-titel">Deine Fotos</div>
          <p className="hinweis">Lade 5 bis 30 Fotos von dir hoch, am besten im Hochformat. Du kannst später jederzeit welche ergänzen.</p>
          <label className="knopf haupt" style={{ marginBottom: 12 }}>
            Fotos auswählen
            <input type="file" accept="image/*" multiple hidden onChange={hochladen} />
          </label>
          {laden && <p className="hinweis">{laden}</p>}
          <div className="fotoraster" style={{ margin: "12px 0" }}>
            {d.fotos.map((f) => (
              <div key={f.id} className="foto"><img src={f.url} alt="" />{f.gesicht && <span className="punkt" />}</div>
            ))}
          </div>
          <div className="knopfreihe">
            <button className="knopf" onClick={() => setSchritt(0)}>Zurück</button>
            <button className="knopf haupt" disabled={!!laden} onClick={() => setSchritt(2)}>{d.fotos.length ? "Weiter" : "Ohne Fotos weiter"}</button>
          </div>
        </div>
      )}

      {schritt === 2 && (
        <div className="karte">
          <div className="schritt">Schritt 3 von 3</div>
          <div className="gross-titel">Dein Look</div>
          <p className="hinweis">Wähle eine Vorlage. Farben und Schriften kannst du danach in den Einstellungen anpassen.</p>
          <LookWahl gewaehlt={look} brand={brand} foto={d.fotos[0] || null} onWahl={setLook} />
          <div className="knopfreihe" style={{ marginTop: 14 }}>
            <button className="knopf" onClick={() => setSchritt(1)}>Zurück</button>
            <button className="knopf haupt" onClick={() => { d.brandSetzen({ ...brand, look, anpassung: {}, fertig: true }); onFertig(); }}>Los geht’s</button>
          </div>
        </div>
      )}
    </div>
  );
}
