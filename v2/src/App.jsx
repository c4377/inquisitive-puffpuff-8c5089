import { useCallback, useEffect, useMemo, useState } from "react";
import { useDaten } from "./lib/store.js";
import { wirksamerLook } from "./lib/looks.js";
import { importUebernehmen, fotosVerteilen, neuerTag } from "./lib/planen.js";
import { tagDateien, teilenOderLaden, alsZip } from "./lib/export.js";
import { schriftenLaden } from "./render/render.js";
import { vorschauLeeren } from "./lib/zeichnen.js";
import Einrichtung from "./ui/Einrichtung.jsx";
import Feed from "./ui/Feed.jsx";
import TagEditor from "./ui/TagEditor.jsx";
import Stories from "./ui/Stories.jsx";
import Captions from "./ui/Captions.jsx";
import Fotos from "./ui/Fotos.jsx";
import Einstellungen from "./ui/Einstellungen.jsx";

const ICONS = {
  feed: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
  stories: "M8 3h8a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z",
  captions: "M4 6h16M4 11h16M4 16h10",
  fotos: "M4 6h16v12H4zM8 14l3-3 3 3 2-2 3 3M9 9.5a1 1 0 1 0 0-.01",
  einstellungen: "M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM4 12h2M18 12h2M12 4v2M12 18v2M6.3 6.3l1.4 1.4M16.3 16.3l1.4 1.4M6.3 17.7l1.4-1.4M16.3 7.7l1.4-1.4",
};
const NAV = [["feed", "Feed"], ["stories", "Stories"], ["captions", "Captions"], ["fotos", "Fotos"], ["einstellungen", "Einstellungen"]];

export default function App() {
  const d = useDaten();
  const [ansicht, setAnsicht] = useState("feed");
  const [tagId, setTagId] = useState(null);
  const [meldungText, setMeldungText] = useState(null);
  const [schriftenBereit, setSchriftenBereit] = useState(false);
  const look = useMemo(() => wirksamerLook(d.brand), [d.brand]);

  const meldung = useCallback((t) => {
    setMeldungText(t);
    setTimeout(() => setMeldungText(null), 2400);
  }, []);

  // Schriften laden, bevor irgendetwas gezeichnet wird.
  useEffect(() => {
    let ab = false;
    setSchriftenBereit(false);
    schriftenLaden(look).then(() => {
      if (ab) return;
      vorschauLeeren();
      setSchriftenBereit(true);
    });
    return () => { ab = true; };
  }, [look.titelSchrift, look.fotoSchrift, look.kleinSchrift, look.nameSchrift]); // eslint-disable-line react-hooks/exhaustive-deps

  const fotoMap = useMemo(() => new Map(d.fotos.map((f) => [f.id, f])), [d.fotos]);
  const fotoVon = useCallback((id) => (id ? fotoMap.get(id) || null : null), [fotoMap]);

  const tagAendern = useCallback((neu) => {
    d.planSetzen((p) => ({ ...p, tage: p.tage.map((t) => (t.id === neu.id ? neu : t)) }));
  }, [d]);

  const optsFuer = useCallback((tag, folie, index, story) => ({
    look, brand: d.brand, tag, folie, index, foto: fotoVon(folie.fotoId), story,
  }), [look, d.brand, fotoVon]);

  const sichern = useCallback(async (tage, nurIndex, nurStories) => {
    meldung("Bilder werden erstellt …");
    let dateien = await tagDateien(tage, optsFuer);
    if (nurIndex != null) dateien = dateien.filter((x) => x.name.endsWith(`_Folie-${String(nurIndex + 1).padStart(2, "0")}.png`));
    else if (nurStories) dateien = dateien.filter((x) => x.name.includes("_Story-"));
    else dateien = dateien.filter((x) => tage.length > 1 || x.name.includes("_Folie-"));
    if (tage.length > 1) { await alsZip(dateien, "Feed.zip"); meldung("ZIP heruntergeladen"); return; }
    const r = await teilenOderLaden(dateien);
    if (r === "geladen") meldung("Heruntergeladen");
  }, [optsFuer, meldung]);

  if (!d.geladen) return <div className="leer">Lädt …</div>;
  if (!d.brand?.fertig) return <Einrichtung d={d} onFertig={() => setAnsicht("feed")} />;

  const tag = tagId && d.plan.tage.find((t) => t.id === tagId);
  const fotoIds = d.fotos.map((f) => f.id);

  let inhalt;
  let titel = d.brand.name || "Feed Studio";
  let zurueck = null;
  if (!schriftenBereit) inhalt = <div className="leer">Schriften werden geladen …</div>;
  else if (ansicht === "feed" && tag) {
    titel = `Tag ${tag.nr}`;
    zurueck = () => setTagId(null);
    inhalt = (
      <TagEditor tag={tag} d={d} look={look} fotoVon={fotoVon} onAendern={tagAendern}
        onLoeschen={() => { d.planSetzen((p) => ({ ...p, tage: p.tage.filter((t) => t.id !== tag.id) })); setTagId(null); }}
        onSichern={sichern} />
    );
  } else if (ansicht === "feed") {
    inhalt = (
      <Feed d={d} look={look} fotoVon={fotoVon} onTag={setTagId}
        onImport={(neu, modus) => {
          d.planSetzen((p) => importUebernehmen(p, neu, fotoIds, look, modus));
          meldung(`${neu.length} Tage übernommen`);
        }}
        onNeuerTag={() => {
          const t = neuerTag(d.plan);
          const [verteilt] = fotosVerteilen([t], fotoIds, look, d.plan.tage.length);
          d.planSetzen((p) => ({ ...p, tage: [...p.tage, verteilt] }));
          setTagId(t.id);
        }}
        onAllesSichern={() => sichern(d.plan.tage)} />
    );
  } else if (ansicht === "stories") {
    inhalt = <Stories d={d} look={look} fotoVon={fotoVon} onTagAendern={tagAendern} onSichern={(t) => sichern([t], null, true)} />;
  } else if (ansicht === "captions") {
    inhalt = <Captions d={d} onTagAendern={tagAendern} />;
  } else if (ansicht === "fotos") {
    inhalt = <Fotos d={d} />;
  } else {
    inhalt = (
      <Einstellungen d={d} meldung={meldung}
        onNeuVerteilen={() => {
          if (!confirm("Fotos und Textposts im ganzen Plan neu verteilen? Deine Texte bleiben, von Hand gewählte Fotos werden ersetzt.")) return;
          d.planSetzen((p) => ({
            ...p,
            tage: fotosVerteilen(p.tage.map((t) => ({
              ...t,
              slides: t.slides.map((s) => ({ ...s, fotoId: undefined, ausschnitt: undefined, modus: undefined })),
              stories: (t.stories || []).map((s) => ({ ...s, fotoId: undefined })),
            })), fotoIds, look, 0),
          }));
          meldung("Neu verteilt");
        }} />
    );
  }

  return (
    <>
      <div className="app">
        <header className="kopf">
          {zurueck && <button className="x" onClick={zurueck} aria-label="Zurück">‹</button>}
          <h1>{titel}</h1>
          {!zurueck && d.brand.handle && <span className="klein">@{d.brand.handle}</span>}
        </header>
        {inhalt}
      </div>
      <div className="leiste">
        <nav>
          {NAV.map(([k, n]) => (
            <button key={k} className={ansicht === k ? "an" : ""} onClick={() => { setAnsicht(k); if (k !== "feed") setTagId(null); else if (ansicht === "feed") setTagId(null); }}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d={ICONS[k]} /></svg>
              {n}
            </button>
          ))}
        </nav>
      </div>
      {meldungText && <div className="meldung">{meldungText}</div>}
    </>
  );
}
