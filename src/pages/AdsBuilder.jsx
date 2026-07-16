import React, { useMemo, useRef, useState } from 'react';
import { useBrand } from '../context/BrandContext';
import Canvas from '../components/Canvas';
import SafeIcon from '../common/SafeIcon';
import * as FiIcons from 'react-icons/fi';
import { getActiveImagePool } from '../utils/smartLayoutGenerator';

const { FiDownload, FiRefreshCw, FiImage, FiTarget, FiList } = FiIcons;

// Builds prefilled ad texts from the strategy stored in brand settings.
// Several hook formulas so "Neu kombinieren" gives fresh variants.
// Dry, observational combinations — no hype phrasing. Each variant only
// recombines what the strategy says; nothing invented.
const firstSentence = (t) => {
  const m = String(t || '').match(/^[^.!?]*[.!?]/);
  return m ? m[0].trim() : String(t || '');
};
// Hook = PROBLEM only. Versprechen/CTA have their own fixed places on the ad,
// so no formula may mix them in — that's what created duplicates.
const hookFormulas = [
  (s) => s.problem || '',
  (s) => firstSentence(s.problem),
  (s) => (s.zielgruppe && s.problem ? `${s.zielgruppe}: ${firstSentence(s.problem)}` : s.problem || ''),
];
const statementFormulas = [
  (s) => s.problem || '',
  (s) => (s.problem && s.versprechen ? `${s.problem} ${s.versprechen}` : s.problem || s.versprechen || ''),
  (s) => (s.versprechen && s.cta ? `${s.versprechen} ${s.cta}` : s.problem || ''),
];

const AdsBuilder = () => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const canvasRef = useRef(null);
  const cfg = brandSettings.currentBrandConfig || {};
  const strategy = cfg.adsStrategy || {};
  const pool = useMemo(() => getActiveImagePool(brandSettings), [brandSettings]);

  const [template, setTemplate] = useState('pins');
  const [variant, setVariant] = useState(0);
  const [background, setBackground] = useState(pool[0] || null);

  // Editable texts, prefilled from the strategy.
  const [hook, setHook] = useState(hookFormulas[0](strategy));
  const [bullets, setBullets] = useState([
    strategy.angebot || '',
    'Direkt umsetzbar',
    '',
  ]);
  const [promise, setPromise] = useState(strategy.versprechen || '');
  const [cta, setCta] = useState(strategy.cta || 'Trag dich für 0 € ein');
  const [statement, setStatement] = useState(statementFormulas[0](strategy));
  const [ctaLine, setCtaLine] = useState(strategy.cta || 'Genug gewartet. Jetzt starten.');

  // --- AI background generation (Netlify function, server-side key) ---
  const [aiStyle, setAiStyle] = useState('collage');
  const [aiBusy, setAiBusy] = useState(false);
  const [aiError, setAiError] = useState('');
  const [aiImages, setAiImages] = useState([]);
  const aiStyles = {
    collage: 'Bold punk collage advertising background, torn paper scraps, tape strips, halftone black-and-white photo cutouts, hand-drawn scribbles and arrows, energetic red backdrop, gritty texture, no text, square format',
    studio: 'Minimal bright studio backdrop for an elegant female coach brand, soft beige tones, clean light, subtle shadows, editorial photography style, no people, no text, square format',
    editorial: 'Moody editorial magazine background, warm dark tones, soft window light, elegant interior blur, cinematic, no text, square format',
  };
  const generateAiImage = async () => {
    setAiBusy(true); setAiError('');
    try {
      const context = [strategy.zielgruppe, strategy.angebot].filter(Boolean).join(', ');
      const prompt = `${aiStyles[aiStyle]}${context ? `. Theme context: ${context}` : ''}`;
      const res = await fetch('/.netlify/functions/generate-ad-image', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      // Robust parsing: on drag&drop deploys the function doesn't exist and
      // the SPA fallback returns HTML — give a clear hint instead of a
      // cryptic Safari parse error.
      const raw = await res.text();
      let data = null;
      try { data = JSON.parse(raw); } catch { /* HTML or empty */ }
      if (!data) {
        throw new Error('KI-Funktion nicht erreichbar. Sie ist nur bei Git-Deploys aktiv (nicht bei Drag-&-Drop) und braucht den GEMINI_API_KEY in Netlify.');
      }
      if (!res.ok || !data.image) throw new Error(data.error || 'Generierung fehlgeschlagen');
      setAiImages((prev) => [data.image, ...prev].slice(0, 6));
      setBackground(data.image);
    } catch (e) {
      setAiError(String(e.message || e));
    } finally {
      setAiBusy(false);
    }
  };

  const reshuffle = () => {
    const v = (variant + 1) % Math.max(hookFormulas.length, statementFormulas.length);
    setVariant(v);
    const h = hookFormulas[v % hookFormulas.length](strategy);
    const st = statementFormulas[v % statementFormulas.length](strategy);
    if (h) setHook(h);
    if (st) setStatement(st);
  };

  // Contrast-aware accent: pick the DARKEST brand color so the CTA button and
  // statement background always carry light text readably. A cream primary
  // (like bordeauxLuxe) used to make buttons invisible.
  const lum = (hex) => {
    if (!hex || typeof hex !== 'string') return 255;
    let h = hex.replace('#', '');
    if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    const r = parseInt(h.slice(0, 2), 16), g = parseInt(h.slice(2, 4), 16), b = parseInt(h.slice(4, 6), 16);
    if ([r, g, b].some(Number.isNaN)) return 255;
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const candidates = [cfg.colors?.primary, cfg.colors?.secondary, cfg.colors?.accent, cfg.colors?.background].filter(Boolean);
  const darkest = candidates.sort((a, b) => lum(a) - lum(b))[0];
  const accent = (darkest && lum(darkest) < 140) ? darkest : '#5C2A2A';
  const brandName = cfg.brandText || brandSettings.website || '';

  const slide = template === 'pins'
    ? {
        layout: 'ad_pins', layoutId: 'ad_pins', format: '4:5',
        background, overlay: 0.15,
        hook,
        bullets: bullets.filter((b) => {
          const t = (b || '').trim();
          return t && t !== (promise || '').trim() && !(hook || '').includes(t);
        }),
        promise: (promise || '').trim() && !(hook || '').includes((promise || '').trim()) ? promise : '',
        cta, accentColor: accent,
        text: hook,
      }
    : {
        layout: 'ad_statement', layoutId: 'ad_statement', format: '4:5',
        background: null, backgroundColor: accent,
        statement, ctaLine, accentColor: accent,
        text: statement,
      };

  const strategyEmpty = !strategy.problem && !strategy.versprechen && !strategy.cta;

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-black text-gray-900 mb-1">Ads-Builder</h1>
      <p className="text-sm text-gray-500 mb-4">Anzeigen aus deiner Strategie — Vorlage wählen, anpassen, exportieren.</p>

      {strategyEmpty && (
        <div className="mb-4 border border-amber-200 bg-amber-50 text-amber-800 rounded-xl px-4 py-3 text-sm">
          Noch keine Ads-Strategie hinterlegt. Fülle sie in den <b>Brand-Einstellungen → Ads-Strategie</b> aus, dann befüllt sich alles hier automatisch.
        </div>
      )}

      {/* Template choice */}
      <div className="flex gap-2 mb-4">
        <button onClick={() => setTemplate('pins')} className={`px-3 py-2 rounded-lg text-xs font-bold border flex items-center gap-1.5 ${template === 'pins' ? 'bg-purple-600 text-white border-purple-600' : 'bg-white text-gray-700 border-gray-200'}`}>
          <SafeIcon icon={FiList} /> Pin-Liste (Foto)
        </button>
        <button onClick={() => setTemplate('statement')} className={`px-3 py-2 rounded-lg text-xs font-bold border flex items-center gap-1.5 ${template === 'statement' ? 'bg-purple-600 text-white border-purple-600' : 'bg-white text-gray-700 border-gray-200'}`}>
          <SafeIcon icon={FiTarget} /> Statement
        </button>
        <button onClick={reshuffle} className="ml-auto px-3 py-2 rounded-lg text-xs font-bold border bg-white text-gray-700 border-gray-200 flex items-center gap-1.5" title="Texte neu aus der Strategie kombinieren">
          <SafeIcon icon={FiRefreshCw} /> Neu kombinieren
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Controls */}
        <div>
          {template === 'pins' && (
            <>
              <label className="block text-[11px] font-bold text-gray-500 mb-1">Hook (oben)</label>
              <textarea value={hook} onChange={(e) => setHook(e.target.value)} rows={2} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 outline-none focus:border-purple-400" />
              {bullets.map((b, i) => (
                <div key={i} className="mb-2">
                  <label className="block text-[11px] font-bold text-gray-500 mb-1">✅ Punkt {i + 1}</label>
                  <input value={b} onChange={(e) => setBullets(bullets.map((x, j) => (j === i ? e.target.value : x)))} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-purple-400" />
                </div>
              ))}
              <label className="block text-[11px] font-bold text-gray-500 mb-1 mt-3">Versprechen (unten)</label>
              <input value={promise} onChange={(e) => setPromise(e.target.value)} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 outline-none focus:border-purple-400" />
              <label className="block text-[11px] font-bold text-gray-500 mb-1">CTA-Button</label>
              <input value={cta} onChange={(e) => setCta(e.target.value)} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 outline-none focus:border-purple-400" />

              <div className="mb-3 border border-gray-200 rounded-xl p-3 bg-gray-50/60">
                <div className="text-[11px] font-bold text-gray-500 mb-2">KI-Hintergrund erstellen</div>
                <div className="flex gap-1.5 mb-2">
                  {[['collage', 'Collage'], ['studio', 'Studio hell'], ['editorial', 'Editorial']].map(([k, l]) => (
                    <button key={k} onClick={() => setAiStyle(k)} className={`px-2.5 py-1.5 rounded-lg text-[11px] font-bold border ${aiStyle === k ? 'bg-gray-900 text-white border-gray-900' : 'bg-white text-gray-600 border-gray-200'}`}>{l}</button>
                  ))}
                </div>
                <button onClick={generateAiImage} disabled={aiBusy} className="w-full bg-gray-900 text-white rounded-lg py-2 text-xs font-bold flex items-center justify-center gap-1.5 disabled:opacity-50">
                  <SafeIcon icon={FiRefreshCw} className={aiBusy ? 'animate-spin' : ''} /> {aiBusy ? 'Wird erstellt…' : 'Bild generieren'}
                </button>
                {aiError && <p className="text-[11px] text-red-600 mt-1.5">{aiError}</p>}
                {aiImages.length > 0 && (
                  <div className="flex gap-2 overflow-x-auto pt-2">
                    {aiImages.map((img, i) => (
                      <button key={i} onClick={() => setBackground(img)} className={`shrink-0 rounded-lg overflow-hidden border-2 ${background === img ? 'border-purple-600' : 'border-transparent'}`}>
                        <img src={img} alt="" className="w-14 h-[70px] object-cover" />
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <div className="text-[11px] font-bold text-gray-500 mb-1 flex items-center gap-1"><SafeIcon icon={FiImage} /> Foto</div>
              <div className="flex gap-2 overflow-x-auto pb-2">
                {pool.length === 0 && <span className="text-xs text-gray-400">Keine Fotos im Pool — lade welche in den Brand-Einstellungen hoch.</span>}
                {pool.map((img) => (
                  <button key={img} onClick={() => setBackground(img)} className={`shrink-0 rounded-lg overflow-hidden border-2 ${background === img ? 'border-purple-600' : 'border-transparent'}`}>
                    <img src={img} alt="" className="w-14 h-[70px] object-cover" />
                  </button>
                ))}
              </div>
            </>
          )}

          {template === 'statement' && (
            <>
              <label className="block text-[11px] font-bold text-gray-500 mb-1">Statement</label>
              <textarea value={statement} onChange={(e) => setStatement(e.target.value)} rows={4} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 outline-none focus:border-purple-400" />
              <label className="block text-[11px] font-bold text-gray-500 mb-1">Handschrift-Zeile (eingekreist)</label>
              <input value={ctaLine} onChange={(e) => setCtaLine(e.target.value)} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 outline-none focus:border-purple-400" />
              <p className="text-[11px] text-gray-400">Hintergrundfarbe kommt aus deiner Brand (Primärfarbe).</p>
            </>
          )}

          <button
            onClick={() => canvasRef.current?.downloadImage?.(`ad-${template}.png`)}
            className="mt-4 w-full bg-purple-600 text-white rounded-xl py-3 text-sm font-bold flex items-center justify-center gap-2 hover:bg-purple-700"
          >
            <SafeIcon icon={FiDownload} /> Als PNG exportieren
          </button>
        </div>

        {/* Preview */}
        <div className="flex items-start justify-center">
          <div className="w-full max-w-[400px] aspect-[4/5] shadow-2xl rounded-sm overflow-hidden bg-white">
            <Canvas ref={canvasRef} data={slide} brandName={brandName} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdsBuilder;
