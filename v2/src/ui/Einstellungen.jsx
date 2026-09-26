import { useRef, useState } from "react";
import LookWahl from "./LookWahl.jsx";
import { LOOKS, SCHRIFTEN, wirksamerLook } from "../lib/looks.js";
import { sicherungErstellen, sicherungLesen } from "../lib/export.js";

export default function Einstellungen({ d, onNeuVerteilen, meldung }) {
  const b = d.brand || {};
  const look = wirksamerLook(b);
  const anp = b.anpassung || {};
  const setzeAnp = (patch) => d.brandSetzen({ anpassung: { ...anp, ...patch } });
  const datei = useRef(null);
  const [arbeit, setArbeit] = useState(false);

  const farbe = (k, n) => (
    <label key={k}>
      <input type="color" value={look[k]} onChange={(e) => setzeAnp({ [k]: e.target.value })} />{n}
    </label>
  );
  const schriftWahl = (k, n) => (
    <div className="feld" key={k}>
      <label>{n}</label>
      <select value={look[k]} onChange={(e) => setzeAnp({ [k]: e.target.value })}>
        {SCHRIFTEN.map((s) => <option key={s} value={s} style={{ fontFamily: s }}>{s}</option>)}
      </select>
    </div>
  );

  return (
    <>
      <div className="karte">
        <h2>Deine Marke</h2>
        <div className="feld"><label htmlFor="bn">Name</label>
          <input id="bn" type="text" value={b.name || ""} onChange={(e) => d.brandSetzen({ name: e.target.value })} /></div>
        <div className="feld"><label htmlFor="bh">Instagram-Name</label>
          <input id="bh" type="text" autoCapitalize="none" value={b.handle || ""} onChange={(e) => d.brandSetzen({ handle: e.target.value.replace(/^@/, "") })} /></div>
      </div>

      <div className="karte">
        <h2>Look</h2>
        <LookWahl gewaehlt={b.look} brand={b} foto={d.fotos[0] || null} onWahl={(k) => d.brandSetzen({ look: k, anpassung: {} })} />
      </div>

      <div className="karte">
        <h2>Farben und Schriften</h2>
        <div className="farben" style={{ marginBottom: 14 }}>
          {farbe("grund", "Textpost")}{farbe("schrift", "Schrift")}{farbe("akzent", "Akzent")}
        </div>
        {schriftWahl("fotoSchrift", "Schrift auf Fotos")}
        {schriftWahl("titelSchrift", "Schrift auf Textposts")}
        {schriftWahl("kleinSchrift", "Kleine Zeilen")}
        {schriftWahl("nameSchrift", "Name unten")}
        <div className="feld">
          <label>Kleine Zeilen in GROSSBUCHSTABEN</label>
          <div className="segment">
            <button className={look.kleinVersal ? "an" : ""} onClick={() => setzeAnp({ kleinVersal: true })}>Ja</button>
            <button className={!look.kleinVersal ? "an" : ""} onClick={() => setzeAnp({ kleinVersal: false })}>Nein</button>
          </div>
        </div>
        <div className="feld">
          <label>Schriftgröße ({Math.round((look.schriftFaktor || 1) * 100)} %)</label>
          <input type="range" min="0.8" max="1.3" step="0.05" value={look.schriftFaktor || 1} onChange={(e) => setzeAnp({ schriftFaktor: Number(e.target.value) })} />
        </div>
        <div className="feld">
          <label>Dunkler Verlauf auf Fotos ({Math.round((look.schwarz ?? 0.85) * 100)} %)</label>
          <input type="range" min="0" max="1" step="0.05" value={look.schwarz ?? 0.85} onChange={(e) => setzeAnp({ schwarz: Number(e.target.value) })} />
        </div>
        <button className="knopf klein" onClick={() => d.brandSetzen({ anpassung: {} })}>Auf Vorlage „{LOOKS[b.look]?.name}“ zurücksetzen</button>
      </div>

      <div className="karte">
        <h2>Feed-Mischung</h2>
        <div className="feld">
          <label>Textposts ohne Foto</label>
          <div className="segment">
            {[[0, "nie"], [2, "jeder 2. Tag"], [3, "jeder 3. Tag"], [4, "jeder 4. Tag"]].map(([k, n]) => (
              <button key={k} className={Number(look.textJede) === k ? "an" : ""} onClick={() => setzeAnp({ textJede: k })}>{n}</button>
            ))}
          </div>
        </div>
        <div className="feld">
          <label>Fotos</label>
          <div className="segment">
            {[["farbe|farbe|farbe|sw", "meist Farbe"], ["sw|sw|farbe|farbe", "halb/halb"], ["sw", "nur Schwarz-Weiß"], ["farbe", "nur Farbe"]].map(([k, n]) => (
              <button key={k} className={(look.fotoReihe || []).join("|") === k ? "an" : ""} onClick={() => setzeAnp({ fotoReihe: k.split("|") })}>{n}</button>
            ))}
          </div>
        </div>
        <p className="hinweis">Die Mischung gilt beim nächsten Import. Mit „Neu verteilen“ wendest du sie auf den ganzen Plan an (deine Texte bleiben).</p>
        <button className="knopf klein" onClick={onNeuVerteilen}>Fotos und Textposts neu verteilen</button>
      </div>

      <div className="karte">
        <h2>Sicherung</h2>
        <p className="hinweis" style={{ marginTop: 0 }}>Alles liegt nur in diesem Browser. Sichere regelmäßig, um nichts zu verlieren oder um auf ein anderes Gerät umzuziehen.</p>
        <div className="knopfreihe">
          <button className="knopf" disabled={arbeit} onClick={async () => { setArbeit(true); await sicherungErstellen(d.brand, d.plan, d.fotos); setArbeit(false); }}>Sicherung herunterladen</button>
          <button className="knopf" onClick={() => datei.current?.click()}>Sicherung einspielen</button>
          <input ref={datei} type="file" accept="application/json,.json" hidden onChange={async (e) => {
            const f = e.target.files?.[0];
            e.target.value = "";
            if (!f) return;
            if (!confirm("Die Sicherung ersetzt alles, was gerade in der App ist. Fortfahren?")) return;
            try { await d.sicherungEinspielen(await sicherungLesen(f)); meldung("Sicherung eingespielt"); }
            catch (err) { alert(err.message || "Die Datei konnte nicht gelesen werden."); }
          }} />
        </div>
      </div>

      <div className="karte">
        <h2>Zurücksetzen</h2>
        <button className="knopf gefahr" onClick={() => { if (confirm("Wirklich alles löschen? Marke, Plan und Fotos sind danach weg.")) d.allesZuruecksetzen(); }}>Alles löschen</button>
      </div>

      <p className="hinweis" style={{ textAlign: "center" }}>
        Schriften: SIL Open Font License (Playfair Display, Instrument Serif, Gloock, Bodoni Moda, Inter, Courier Prime, Caveat, Mrs Saint Delafield).
        Gesichtserkennung: face-api (MIT).
      </p>
    </>
  );
}
