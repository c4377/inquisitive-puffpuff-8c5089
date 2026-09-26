// Zentrale Daten der App (Marke, Plan, Fotos) mit Speichern im Browser.
import { useCallback, useEffect, useRef, useState } from "react";
import { kvGet, kvSet, fotoAlle, fotoSpeichern, fotoLoeschen, allesLoeschen, neueId } from "./db.js";
import { gesichtFinden } from "../render/faces.js";
import { vorschauLeeren } from "./zeichnen.js";

function bildLaden(url) {
  return new Promise((ok, fehler) => {
    const img = new Image();
    img.onload = () => ok(img);
    img.onerror = fehler;
    img.src = url;
  });
}

// Grosse Fotos vor dem Speichern verkleinern (lange Seite 1800 px).
async function verkleinern(datei) {
  const url = URL.createObjectURL(datei);
  try {
    const img = await bildLaden(url);
    const max = 1800;
    const s = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
    const c = document.createElement("canvas");
    c.width = Math.round(img.naturalWidth * s);
    c.height = Math.round(img.naturalHeight * s);
    c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
    return await new Promise((ok) => c.toBlob((b) => ok(b), "image/jpeg", 0.9));
  } finally {
    URL.revokeObjectURL(url);
  }
}

async function mitBild(f) {
  const url = URL.createObjectURL(f.blob);
  try {
    return { ...f, url, img: await bildLaden(url) };
  } catch {
    return { ...f, url, img: null };
  }
}

export function useDaten() {
  const [geladen, setGeladen] = useState(false);
  const [brand, setBrand] = useState(null);
  const [plan, setPlan] = useState({ tage: [] });
  const [fotos, setFotos] = useState([]);
  const [rev, setRev] = useState(0);
  const fotosRef = useRef([]);
  fotosRef.current = fotos;

  useEffect(() => {
    (async () => {
      const [b, p, alle] = await Promise.all([kvGet("brand"), kvGet("plan"), fotoAlle()]);
      setBrand(b || null);
      setPlan(p || { tage: [] });
      const sortiert = (alle || []).sort((a, z) => (a.hinzugefuegt || 0) - (z.hinzugefuegt || 0));
      setFotos(await Promise.all(sortiert.map(mitBild)));
      setGeladen(true);
    })();
  }, []);

  // Fotos ohne Gesichtspruefung im Hintergrund nachholen.
  useEffect(() => {
    if (!geladen) return;
    const offen = fotos.filter((f) => !f.gesichtGeprueft && f.img);
    if (!offen.length) return;
    let abbruch = false;
    (async () => {
      for (const f of offen) {
        if (abbruch) return;
        const gesicht = await gesichtFinden(f.img);
        const neu = { id: f.id, name: f.name, blob: f.blob, hinzugefuegt: f.hinzugefuegt, gesicht, gesichtGeprueft: true };
        await fotoSpeichern(neu);
        setFotos((alt) => alt.map((x) => (x.id === f.id ? { ...x, gesicht, gesichtGeprueft: true } : x)));
        vorschauLeeren();
        setRev((r) => r + 1);
      }
    })();
    return () => { abbruch = true; };
  }, [geladen, fotos]);

  const brandSetzen = useCallback(async (patch) => {
    setBrand((alt) => {
      const neu = { ...(alt || {}), ...patch };
      kvSet("brand", neu);
      return neu;
    });
    vorschauLeeren();
    setRev((r) => r + 1);
  }, []);

  const planSetzen = useCallback((fn) => {
    setPlan((alt) => {
      const neu = typeof fn === "function" ? fn(alt) : fn;
      kvSet("plan", neu);
      return neu;
    });
  }, []);

  const fotosHinzufuegen = useCallback(async (dateien, fortschritt) => {
    const neu = [];
    let i = 0;
    for (const d of dateien) {
      i++;
      fortschritt && fortschritt(i, dateien.length);
      const blob = await verkleinern(d);
      const f = { id: neueId(), name: d.name, blob, hinzugefuegt: Date.now() + i, gesicht: null, gesichtGeprueft: false };
      const mb = await mitBild(f);
      if (mb.img) {
        f.gesicht = await gesichtFinden(mb.img);
        f.gesichtGeprueft = true;
      }
      await fotoSpeichern(f);
      neu.push({ ...mb, gesicht: f.gesicht, gesichtGeprueft: f.gesichtGeprueft });
    }
    setFotos((alt) => [...alt, ...neu]);
    return neu;
  }, []);

  const fotoEntfernen = useCallback(async (id) => {
    await fotoLoeschen(id);
    setFotos((alt) => {
      const f = alt.find((x) => x.id === id);
      if (f?.url) URL.revokeObjectURL(f.url);
      return alt.filter((x) => x.id !== id);
    });
    // Folien, die das Foto nutzten, werden zu Textposts
    planSetzen((p) => ({
      ...p,
      tage: (p.tage || []).map((t) => ({
        ...t,
        slides: t.slides.map((s) => (s.fotoId === id ? { ...s, fotoId: null } : s)),
        stories: (t.stories || []).map((s) => (s.fotoId === id ? { ...s, fotoId: null } : s)),
      })),
    }));
    vorschauLeeren();
  }, [planSetzen]);

  const sicherungEinspielen = useCallback(async ({ brand: b, plan: p, fotos: fs }) => {
    await allesLoeschen();
    await kvSet("brand", b);
    await kvSet("plan", p);
    for (const f of fs) await fotoSpeichern(f);
    fotosRef.current.forEach((f) => f.url && URL.revokeObjectURL(f.url));
    setBrand(b);
    setPlan(p);
    setFotos(await Promise.all(fs.map(mitBild)));
    vorschauLeeren();
    setRev((r) => r + 1);
  }, []);

  const allesZuruecksetzen = useCallback(async () => {
    await allesLoeschen();
    fotosRef.current.forEach((f) => f.url && URL.revokeObjectURL(f.url));
    setBrand(null);
    setPlan({ tage: [] });
    setFotos([]);
    vorschauLeeren();
  }, []);

  return {
    geladen, brand, plan, fotos, rev,
    brandSetzen, planSetzen, fotosHinzufuegen, fotoEntfernen, sicherungEinspielen, allesZuruecksetzen,
  };
}
