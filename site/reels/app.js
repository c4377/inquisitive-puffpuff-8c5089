// Reel-Werkstatt — laeuft komplett im Browser.
// Ablauf: Video laden -> Ton analysieren (Pausen) -> Whisper transkribiert jeden Satz
// -> optional Claude markiert Versprecher -> Carina hakt ab -> Rendern (WebCodecs) -> MP4.
import {
  Input, BlobSource, ALL_FORMATS, CanvasSink, AudioBufferSink,
  Output, Mp4OutputFormat, BufferTarget, CanvasSource, AudioBufferSource,
  getFirstEncodableAudioCodec, canEncodeVideo,
} from './lib/mediabunny.min.mjs';

const $ = (id) => document.getElementById(id);
const W = 1080, H = 1920;

// ---------------------------------------------------------------- Einstellungen
const SCHRIFTEN = [
  ['Nothing You Could Do', 400, 'Handschrift (wie dein Beispiel)'],
  ['Caveat', 500, 'Handschrift rund'],
  ['Shadows Into Light', 400, 'Handschrift locker'],
  ['Mrs Saint Delafield', 400, 'Schreibschrift elegant'],
  ['Figtree', 700, 'Instagram-Stil fett'],
  ['Poppins', 700, 'Poppins fett'],
  ['Montserrat', 700, 'Montserrat fett'],
  ['Helvetica Neue BS', 700, 'Helvetica fett'],
  ['Archivo Black', 400, 'Archivo Black'],
  ['Anton', 400, 'Anton (schmal, laut)'],
  ['Playfair Display', 600, 'Playfair (Serif)'],
];
const STANDARD = {
  titel: '', titelFont: 'Figtree', titelSize: 74, titelDauer: 2.8, titelY: 14,
  capFont: 'Nothing You Could Do', capSize: 92, capY: 67, capOutline: 2.2, capFarbe: '#ffffff', capMax: 18,
  zoomA: 1.15, zoomB: 1.35, gesichtY: 30, shotLen: 3.3, fx: 0.5, fy: 0.35,
  look: 'warm', lookStaerke: 100, hell: 0, vignette: 35,
  klang: 'maus', klangAbstand: 5, klangLaut: 100,
  padVor: 0.10, padNach: 0.15, pauseMin: 0.3, stille: -38,
  modell: 'onnx-community/whisper-large-v3-turbo', apiKey: '', claudeModell: 'claude-sonnet-5-5',
  bitrate: '4000000',
};
let S = { ...STANDARD };
try { Object.assign(S, JSON.parse(localStorage.getItem('reelWerkstatt') || '{}')); } catch {}
const speichern = () => { try { localStorage.setItem('reelWerkstatt', JSON.stringify(S)); } catch {} };

for (const id of ['s_titelFont', 's_capFont']) {
  $(id).innerHTML = SCHRIFTEN.map(([f, , n]) => `<option value="${f}">${n}</option>`).join('');
}
const FELDER = ['titel', 'titelFont', 'titelSize', 'titelDauer', 'titelY', 'capFont', 'capSize', 'capY', 'capOutline',
  'capFarbe', 'capMax', 'zoomA', 'zoomB', 'gesichtY', 'shotLen', 'look', 'lookStaerke', 'hell', 'vignette', 'klang',
  'klangAbstand', 'klangLaut', 'padVor', 'padNach', 'pauseMin', 'stille', 'modell', 'apiKey', 'claudeModell', 'bitrate'];
function felderFuellen() {
  for (const k of FELDER) {
    const el = $('s_' + k); if (!el) continue;
    el.value = S[k];
    const v = $('v_' + k); if (v) v.textContent = S[k];
  }
}
for (const k of FELDER) {
  const el = $('s_' + k); if (!el) continue;
  el.addEventListener('input', () => {
    S[k] = (el.type === 'range' || el.type === 'number') ? parseFloat(el.value) : el.value;
    const v = $('v_' + k); if (v) v.textContent = S[k];
    speichern(); vorschauBald();
  });
}
$('zuruecksetzen').onclick = () => { const key = S.apiKey; S = { ...STANDARD, apiKey: key }; speichern(); felderFuellen(); vorschauBald(); };
felderFuellen();

const status = (t) => { $('status').textContent = t; };
const fortschritt = (p) => { $('fortschritt').style.width = Math.round(p * 100) + '%'; };
const rStatus = (t) => { $('renderStatus').textContent = t; };
const rFortschritt = (p) => { $('renderFortschritt').style.width = Math.round(p * 100) + '%'; };

// ---------------------------------------------------------------- Zustand
let datei = null, input = null, videoTrack = null, audioTrack = null;
let quelle = { w: 0, h: 0, dauer: 0, fps: 30 };
let ton = null;       // { rate, L, R }  Originalton
let ton16 = null;     // Float32Array 16 kHz mono, normalisiert (nur fuer Analyse)
let saetze = [];      // { id, s, e, text, keep, grund }
let klangDatei = null;

// ---------------------------------------------------------------- Video laden
$('datei').addEventListener('change', async (ev) => {
  const f = ev.target.files[0]; if (!f) return;
  datei = f; saetze = []; zeigeSaetze();
  $('quelle').src = URL.createObjectURL(f);
  $('quelle').muted = true;
  try {
    input = new Input({ source: new BlobSource(f), formats: ALL_FORMATS });
    videoTrack = null; audioTrack = null;
    for (const t of await input.getVideoTracks()) if (await t.canDecode()) { videoTrack = t; break; }
    for (const t of await input.getAudioTracks()) if (await t.canDecode()) { audioTrack = t; break; }
    if (!videoTrack && (await input.getVideoTracks()).length) throw new Error('Dieser Browser kann das Video nicht lesen — bitte Chrome oder Safari auf dem Mac verwenden.');
    if (!videoTrack) throw new Error('Keine Videospur gefunden.');
    if (!audioTrack) throw new Error('Keine Tonspur gefunden.');
    quelle.dauer = await input.computeDuration();
    try { const st = await videoTrack.computePacketStats(100); quelle.fps = Math.round(st.averagePacketRate) || 30; } catch { quelle.fps = 30; }
    vorschauSink = null; vorschauBild = null; vorschauZeit = Math.min(1, quelle.dauer / 2); ton = null; ton16 = null;
    await vorschau();
    status(`Video geladen: ${quelle.dauer.toFixed(1)} Sek. — jetzt „Pausen finden & transkribieren“.`);
    $('analysieren').disabled = false;
  } catch (e) { status('Fehler beim Laden: ' + e.message); }
});
$('scrub').addEventListener('input', () => {
  if (!quelle.dauer) return;
  vorschauZeit = ($('scrub').value / 1000) * quelle.dauer; vorschauBald();
});
$('vorschau').addEventListener('click', (ev) => {
  if (!quelle.w) return;
  const r = ev.target.getBoundingClientRect();
  const u = (ev.clientX - r.left) / r.width, v = (ev.clientY - r.top) / r.height;
  const c = ausschnitt(quelle.w, quelle.h, S.zoomA);
  S.fx = (c.x + u * c.w) / quelle.w;
  S.fy = (c.y + v * c.h) / quelle.h;
  S.gesichtY = Math.round(Math.min(60, Math.max(15, v * 100)));
  felderFuellen(); speichern(); vorschauBald();
});

// ---------------------------------------------------------------- Ton holen
async function tonLaden() {
  if (ton) return ton;
  const sink = new AudioBufferSink(audioTrack);
  const teile = []; let rate = 48000, len = 0;
  for await (const { buffer, timestamp } of sink.buffers()) {
    rate = buffer.sampleRate;
    const L = buffer.getChannelData(0).slice();
    const R = buffer.numberOfChannels > 1 ? buffer.getChannelData(1).slice() : L;
    teile.push({ t: timestamp, L, R }); len = Math.max(len, Math.round(timestamp * rate) + L.length);
    if (teile.length % 50 === 0) status(`Ton wird gelesen … ${timestamp.toFixed(0)} Sek.`);
  }
  const Lg = new Float32Array(len), Rg = new Float32Array(len);
  for (const p of teile) { const o = Math.max(0, Math.round(p.t * rate)); Lg.set(p.L.subarray(0, Math.min(p.L.length, len - o)), o); Rg.set(p.R.subarray(0, Math.min(p.R.length, len - o)), o); }
  ton = { rate, L: Lg, R: Rg };
  // 16 kHz mono fuer Analyse & Whisper
  const mono = new Float32Array(len); for (let i = 0; i < len; i++) mono[i] = 0.5 * (Lg[i] + Rg[i]);
  ton16 = await resample(mono, rate, 16000);
  // normalisieren: lautester Sprachanteil (95. Perzentil) auf -19 dB
  const pegel = []; for (let i = 0; i + 800 <= ton16.length; i += 800) pegel.push(db(ton16, i, 800));
  pegel.sort((a, b) => a - b);
  const p95 = pegel[Math.floor(pegel.length * 0.95)] ?? -30;
  const g = Math.pow(10, (-19 - p95) / 20);
  for (let i = 0; i < ton16.length; i++) ton16[i] *= g;
  return ton;
}
async function resample(data, von, zu) {
  if (von === zu) return data;
  const n = Math.ceil(data.length * zu / von);
  const ctx = new OfflineAudioContext(1, n, zu);
  const b = ctx.createBuffer(1, data.length, von); b.copyToChannel(data, 0);
  const s = ctx.createBufferSource(); s.buffer = b; s.connect(ctx.destination); s.start();
  return (await ctx.startRendering()).getChannelData(0);
}
function db(a, i, n) { let s = 0, e = Math.min(a.length, i + n); for (let k = i; k < e; k++) s += a[k] * a[k]; return 10 * Math.log10(s / Math.max(1, e - i) + 1e-12); }
const dbT = (t, dauer = 0.05) => db(ton16, Math.max(0, Math.round(t * 16000)), Math.round(dauer * 16000));

// ---------------------------------------------------------------- Pausen finden
function sprechstellen() {
  const hop = 160; // 10 ms
  const n = Math.floor(ton16.length / hop);
  const laut = new Uint8Array(n);
  for (let i = 0; i < n; i++) laut[i] = db(ton16, i * hop, 320) > S.stille ? 1 : 0;
  // Stille unter 0,15 s ueberbruecken, Sprache unter 0,05 s ignorieren
  const segs = []; let i = 0;
  while (i < n) {
    if (!laut[i]) { i++; continue; }
    let j = i; while (j < n && laut[j]) j++;
    segs.push([i * 0.01, j * 0.01]); i = j;
  }
  const merged = [];
  for (const s of segs) {
    if (merged.length && s[0] - merged[merged.length - 1][1] < 0.15) merged[merged.length - 1][1] = s[1];
    else merged.push([...s]);
  }
  return merged.filter(([a, b]) => b - a >= 0.05);
}
function zuSaetzen(mikro) {
  // Fenster: neue Zeile bei Pause >= pauseMin; lange Stuecke an leisen Stellen teilen (max ~8 s)
  const fenster = []; let cur = null;
  for (const m of mikro) {
    if (!cur || m[0] - cur[1] >= S.pauseMin) { cur = [m[0], m[1]]; fenster.push(cur); }
    else cur[1] = m[1];
  }
  const out = [];
  for (const [a, b] of fenster) {
    let t = a;
    while (b - t > 8) {
      let best = t + 4.5, bestDb = 99;
      for (let x = t + 4.5; x < Math.min(b - 0.5, t + 7.5); x += 0.02) { const d = dbT(x, 0.06); if (d < bestDb) { bestDb = d; best = x; } }
      out.push([t, best]); t = best;
    }
    out.push([t, b]);
  }
  return out;
}

// ---------------------------------------------------------------- Whisper
let asr = null;
async function whisperLaden() {
  if (window.__testTranskription) return null;
  if (asr && asr.__modell === S.modell) return asr;
  status('Sprachmodell wird geladen … (beim ersten Mal dauert das einige Minuten, danach ist es im Browser gespeichert)');
  const T = await import('./lib/transformers.bundle.mjs');
  const gpu = !!navigator.gpu && !!(await navigator.gpu.requestAdapter().catch(() => null));
  const dateien = {};
  const progress_callback = (p) => {
    if (p.status === 'progress' && p.total) {
      dateien[p.file] = [p.loaded, p.total];
      let l = 0, t = 0; for (const [a, b] of Object.values(dateien)) { l += a; t += b; }
      status(`Sprachmodell wird geladen … ${(l / 1e6).toFixed(0)} / ${(t / 1e6).toFixed(0)} MB`); fortschritt(l / t);
    }
  };
  // Versuche in dieser Reihenfolge: gewaehltes Modell auf der Grafikkarte, dann ohne Grafikkarte, dann kleineres Modell
  const versuche = [];
  if (gpu) versuche.push([S.modell, { device: 'webgpu', dtype: { encoder_model: 'fp16', decoder_model_merged: 'q4' } }]);
  versuche.push([S.modell, { device: 'wasm', dtype: 'q8' }]);
  if (S.modell !== 'onnx-community/whisper-small') versuche.push(['onnx-community/whisper-small', { device: gpu ? 'webgpu' : 'wasm', dtype: gpu ? 'fp32' : 'q8' }]);
  let fehler = null;
  for (const [modell, opts] of versuche) {
    try {
      asr = await T.pipeline('automatic-speech-recognition', modell, { ...opts, progress_callback });
      asr.__modell = S.modell;
      if (modell !== S.modell) status(`Hinweis: ${S.modell} ließ sich nicht laden, ich nutze ${modell}.`);
      return asr;
    } catch (e) { console.warn('Whisper-Versuch fehlgeschlagen', modell, opts.device, e); fehler = e; }
  }
  throw new Error('Sprachmodell konnte nicht geladen werden: ' + (fehler?.message || fehler));
}
async function transkribiere(a, b) {
  const s = Math.max(0, Math.round((a - 0.1) * 16000)), e = Math.min(ton16.length, Math.round((b + 0.1) * 16000));
  const stueck = ton16.slice(s, e);
  if (window.__testTranskription) return window.__testTranskription(a, b);
  const r = await asr(stueck, { language: 'german', task: 'transcribe', chunk_length_s: 30 });
  return (r.text || '').trim();
}

$('analysieren').onclick = async () => {
  $('analysieren').disabled = true; $('ki').disabled = true; $('rendern').disabled = true;
  try {
    status('Ton wird gelesen …'); fortschritt(0);
    await tonLaden();
    const zeilen = zuSaetzen(sprechstellen());
    status(`${zeilen.length} Sätze gefunden. Transkription startet …`);
    await whisperLaden();
    saetze = [];
    for (let i = 0; i < zeilen.length; i++) {
      const [a, b] = zeilen[i];
      const text = await transkribiere(a, b);
      const leer = !/[A-Za-zÄÖÜäöüß0-9]/.test(text);
      saetze.push({ id: i + 1, s: +a.toFixed(2), e: +b.toFixed(2), text, keep: !leer && b - a > 0.12, grund: leer ? 'kein Wort erkannt' : '' });
      fortschritt((i + 1) / zeilen.length);
      status(`Transkribiere … ${i + 1} / ${zeilen.length}`);
      zeigeSaetze();
    }
    // Anfang pruefen: Geraeusch/Atmer vor dem ersten Wort faellt durch die Stille-Erkennung weg
    status(`Fertig: ${saetze.length} Sätze. Prüfe die Liste${S.apiKey ? ' oder lass Claude Versprecher finden' : ''}, dann „Reel rendern“.`);
    if (!S.titel) { const erster = saetze.find((x) => x.keep); if (erster) { S.titel = kurzTitel(erster.text); felderFuellen(); speichern(); } }
    $('ki').disabled = false; $('rendern').disabled = false;
  } catch (e) { console.error(e); status('Fehler: ' + e.message); }
  $('analysieren').disabled = false;
  vorschauBald();
};
function kurzTitel(t) { const w = t.replace(/[.,!?:;]+$/, '').split(/\s+/).slice(0, 7); const h = Math.ceil(w.length / 2); return w.slice(0, h).join(' ') + '\n' + w.slice(h).join(' '); }

// ---------------------------------------------------------------- Satzliste
function zeigeSaetze() {
  const box = $('saetze');
  box.innerHTML = '';
  for (const z of saetze) {
    const el = document.createElement('div');
    el.className = 'satz' + (z.keep ? '' : ' raus');
    el.innerHTML = `<input type="checkbox" ${z.keep ? 'checked' : ''} title="behalten">
      <button class="play" title="anhören">▶</button>
      <textarea rows="2"></textarea>
      <div class="zeit"><input type="number" step="0.05" value="${z.s}" title="Start (Sek.)"><input type="number" step="0.05" value="${z.e}" title="Ende (Sek.)"></div>
      ${z.grund ? `<div class="grund">${z.grund}</div>` : ''}`;
    const [cb, play, ta, zs, ze] = [el.querySelector('input'), el.querySelector('.play'), el.querySelector('textarea'), ...el.querySelectorAll('.zeit input')];
    ta.value = z.text;
    cb.onchange = () => { z.keep = cb.checked; el.classList.toggle('raus', !z.keep); };
    ta.oninput = () => { z.text = ta.value; };
    zs.onchange = () => { z.s = parseFloat(zs.value); };
    ze.onchange = () => { z.e = parseFloat(ze.value); };
    play.onclick = () => abspielen(z.s, z.e);
    box.appendChild(el);
  }
}
let stopTimer = null;
function abspielen(a, b) {
  const v = $('quelle'); v.muted = false; v.currentTime = a; v.play();
  clearInterval(stopTimer);
  stopTimer = setInterval(() => { if (v.currentTime >= b) { v.pause(); clearInterval(stopTimer); } }, 30);
}

// ---------------------------------------------------------------- Claude
$('ki').onclick = async () => {
  if (!S.apiKey) { status('Für die Versprecher-Erkennung brauchst du einen Anthropic-API-Key (Einstellungen → Transkription & KI).'); return; }
  $('ki').disabled = true; status('Claude liest die Sätze …');
  try {
    const liste = saetze.map((z, i) => ({ id: z.id, start: z.s, ende: z.e, pause_davor: i ? +(z.s - saetze[i - 1].e).toFixed(2) : 0, text: z.text }));
    const prompt = `Du schneidest ein gesprochenes Instagram-Reel (Deutsch, teils Englisch). Unten stehen die automatisch transkribierten Satzstücke mit Zeiten.

Aufgabe:
1. Finde Stücke, die raus sollen: abgebrochene Satzanfänge, die direkt danach neu begonnen werden (behalte den vollständigen, meist späteren Anlauf), gestotterte Wiederholungen, reine Geräusche oder Füllwörter ohne Inhalt, erkannte Wörter, die offensichtlich Rauschen sind ("Musik", "*", "..."). Bewusste Wiederholungen zur Betonung bleiben drin. Im Zweifel drinlassen.
2. Korrigiere offensichtliche Erkennungsfehler im Text anhand des Zusammenhangs (Rechtschreibung, falsch gehörte Wörter, abgeschnittene Wörter an Stückgrenzen). Formulierung der Sprecherin nicht umschreiben.
3. Schlag einen kurzen Hook-Titel für das Reel vor (max. 6 Wörter, in ihren Worten, aus der Kernaussage).

Antworte NUR mit JSON in genau dieser Form:
{"raus":[{"id":1,"grund":"kurz"}],"text":{"3":"korrigierter Text"},"titel":"...","unsicher":["Stellen, bei denen du dir beim Wortlaut nicht sicher bist"]}

Stücke:
${JSON.stringify(liste)}`;
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': S.apiKey, 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
      body: JSON.stringify({ model: S.claudeModell, max_tokens: 4000, messages: [{ role: 'user', content: prompt }] }),
    });
    const j = await res.json();
    if (!res.ok) throw new Error(j?.error?.message || res.status);
    const txt = j.content.map((c) => c.text || '').join('');
    const antwort = JSON.parse(txt.slice(txt.indexOf('{'), txt.lastIndexOf('}') + 1));
    for (const r of antwort.raus || []) { const z = saetze.find((x) => x.id === +r.id); if (z) { z.keep = false; z.grund = 'Claude: ' + (r.grund || 'raus'); } }
    for (const [id, t] of Object.entries(antwort.text || {})) { const z = saetze.find((x) => x.id === +id); if (z && t) z.text = t; }
    if (antwort.titel) { const w = antwort.titel.split(/\s+/); const h = Math.ceil(w.length / 2); S.titel = w.slice(0, h).join(' ') + '\n' + w.slice(h).join(' '); felderFuellen(); speichern(); }
    zeigeSaetze();
    vorschauBald();
    status(`Claude hat ${(antwort.raus || []).length} Stellen markiert.` + ((antwort.unsicher || []).length ? '\nBitte prüfen: ' + antwort.unsicher.join(' · ') : ''));
  } catch (e) { status('Claude-Fehler: ' + e.message); }
  $('ki').disabled = false;
};

// ---------------------------------------------------------------- Plan: Bereiche, Shots, Untertitel, Klicks
function plan() {
  const alle = [...saetze].sort((a, b) => a.s - b.s);
  const behalten = alle.filter((z) => z.keep && z.e > z.s);
  // zusammenhaengende Saetze (Luecke < 0,35 s und nichts Gestrichenes dazwischen) bilden einen Bereich
  const bereiche = [];
  for (const z of behalten) {
    const idx = alle.indexOf(z);
    const vorher = alle[idx - 1];
    const letzter = bereiche[bereiche.length - 1];
    if (letzter && vorher && vorher.keep && vorher === letzter.zeilen[letzter.zeilen.length - 1] && z.s - vorher.e < 0.35) {
      letzter.e = z.e; letzter.zeilen.push(z);
    } else bereiche.push({ s: z.s, e: z.e, zeilen: [z] });
  }
  // Luft davor/danach, ohne in gestrichene Nachbarn oder den Dateirand zu laufen
  for (const b of bereiche) {
    const i0 = alle.indexOf(b.zeilen[0]), i1 = alle.indexOf(b.zeilen[b.zeilen.length - 1]);
    const vor = alle[i0 - 1], nach = alle[i1 + 1];
    b.a = Math.max(0, b.s - S.padVor, vor ? vor.e + 0.02 : 0);
    b.b = Math.min(quelle.dauer - 0.02, b.e + S.padNach, nach ? nach.s - 0.02 : Infinity);
  }
  // Shots: lange Bereiche an leisen Stellen teilen, Zoom abwechseln
  const shots = []; let o = 0, z = 0;
  for (const b of bereiche) {
    b.o = o;
    const cuts = [b.a]; let t = b.a;
    while (b.b - t > S.shotLen * 1.4) {
      let best = t + S.shotLen, bestDb = 99;
      for (let x = t + S.shotLen * 0.75; x < t + S.shotLen * 1.25 && x < b.b - 1; x += 0.05) { const d = dbT(x); if (d < bestDb) { bestDb = d; best = x; } }
      cuts.push(best); t = best;
    }
    cuts.push(b.b);
    for (let i = 0; i < cuts.length - 1; i++) { shots.push({ s: cuts[i], e: cuts[i + 1], o: o + (cuts[i] - b.a), zoom: z % 2 ? S.zoomB : S.zoomA }); z++; }
    o += b.b - b.a;
  }
  const dauer = o;
  const zuAus = (t) => { for (const b of bereiche) if (t >= b.a - 1e-6 && t <= b.b + 1e-6) return b.o + (t - b.a); return null; };
  // Untertitel: Woerter proportional zur Laenge innerhalb des Satzes
  const caps = [];
  for (const b of bereiche) {
    const woerter = [];
    for (const zl of b.zeilen) {
      const ws = zl.text.split(/\s+/).filter(Boolean); const tot = ws.reduce((s, w) => s + w.length + 1, 0); let acc = 0;
      for (const w of ws) { woerter.push({ t: zuAus(zl.s + (zl.e - zl.s) * acc / tot), w }); acc += w.length + 1; }
    }
    const ende = b.o + (b.b - b.a) - 0.05;
    const gruppen = []; let cur = [];
    for (const w of woerter) {
      cur.push(w); const t = cur.map((x) => x.w).join(' ');
      if (t.length >= S.capMax || (/[.?!,:;]$/.test(w.w) && t.length >= 8) || cur.length >= 5) { gruppen.push(cur); cur = []; }
    }
    if (cur.length) {
      const rest = cur.map((x) => x.w).join(' ');
      if (gruppen.length && rest.length < 7 && (gruppen[gruppen.length - 1].map((x) => x.w).join(' ') + ' ' + rest).length <= S.capMax + 12) gruppen[gruppen.length - 1].push(...cur);
      else gruppen.push(cur);
    }
    gruppen.forEach((g, i) => caps.push({ a: g[0].t, b: i + 1 < gruppen.length ? gruppen[i + 1][0].t : ende, text: g.map((x) => x.w).join(' ') }));
  }
  return { bereiche, shots, caps, dauer };
}
function zweiZeilen(t) {
  if (t.length <= 16 || !t.includes(' ')) return [t];
  const w = t.split(' '); let best = 1, diff = 1e9;
  for (let k = 1; k < w.length; k++) { const d = Math.abs(w.slice(0, k).join(' ').length - w.slice(k).join(' ').length); if (d < diff) { diff = d; best = k; } }
  return [w.slice(0, best).join(' '), w.slice(best).join(' ')];
}

// ---------------------------------------------------------------- Bild: WebGL-Grading + Text
const gl_canvas = document.createElement('canvas'); gl_canvas.width = W; gl_canvas.height = H;
const gl = gl_canvas.getContext('webgl', { preserveDrawingBuffer: true, premultipliedAlpha: false });
const out = document.createElement('canvas'); out.width = W; out.height = H;
const octx = out.getContext('2d');
const LOOKS = {
  warm:      { mix: [0.95, 0.86, 0.80], con: 1.05, sat: 1.12, lo: 0.02, hi: 0.96, ts: [0, 0, 0], th: [0, 0, 0] },
  cinematic: { mix: [1, 1, 1], con: 1.10, sat: 1.12, lo: 0.0, hi: 1.0, ts: [-0.05, -0.005, 0.06], th: [0.05, 0.02, -0.05] },
  film:      { mix: [1.0, 0.97, 0.92], con: 0.92, sat: 0.90, lo: 0.06, hi: 0.94, ts: [0, 0.01, 0.02], th: [0.03, 0.015, 0] },
  sw:        { mix: [1, 1, 1], con: 1.12, sat: 0, lo: 0.02, hi: 0.97, ts: [0, 0, 0], th: [0, 0, 0] },
  neutral:   { mix: [1, 1, 1], con: 1, sat: 1, lo: 0, hi: 1, ts: [0, 0, 0], th: [0, 0, 0] },
};
const prog = (() => {
  // Hinweis: Textur wird ohne FLIP_Y geladen -> Zeile 0 ist oben; uv.y waechst nach unten.
  const vs = `attribute vec2 p; varying vec2 uv; varying vec2 op; uniform vec4 crop;
    void main(){ vec2 q = p*0.5+0.5; op = vec2(q.x, 1.0-q.y);
      uv = vec2(crop.x + op.x*crop.z, crop.y + op.y*crop.w); gl_Position = vec4(p,0.0,1.0); }`;
  const fs = `precision mediump float; varying vec2 uv; varying vec2 op; uniform sampler2D tex;
    uniform vec3 mixc; uniform vec3 ts; uniform vec3 th;
    uniform float con; uniform float sat; uniform float lo; uniform float hi; uniform float k; uniform float hell; uniform float vig;
    void main(){
      vec3 o = texture2D(tex, uv).rgb; vec3 c = o*mixc;
      c = (c-0.5)*con+0.5;
      float l = dot(c, vec3(0.299,0.587,0.114));
      c = mix(vec3(l), c, sat);
      c += ts*(1.0-l)*(1.0-l) + th*l*l;
      c = lo + c*(hi-lo);
      c = mix(o, c, k) + hell;
      vec2 d = op - 0.5; d.x *= 0.5625; float r = length(d)*1.6;
      c *= 1.0 - vig*smoothstep(0.35, 0.95, r);
      gl_FragColor = vec4(clamp(c,0.0,1.0),1.0);
    }`;
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const p = gl.createProgram();
  gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(p); gl.useProgram(p);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(p, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  const u = {}; for (const n of ['crop', 'mixc', 'ts', 'th', 'con', 'sat', 'lo', 'hi', 'k', 'hell', 'vig']) u[n] = gl.getUniformLocation(p, n);
  return u;
})();

function ausschnitt(sw, sh, zoom) {
  let ch = Math.min(sh, sw * 16 / 9) / zoom, cw = ch * 9 / 16;
  const cx = S.fx * sw, cy = S.fy * sh;
  const x = Math.min(Math.max(0, cx - cw / 2), sw - cw);
  const y = Math.min(Math.max(0, cy - (S.gesichtY / 100) * ch), sh - ch);
  return { x, y, w: cw, h: ch };
}
function bildMalen(src, sw, sh, zoom) {
  const c = ausschnitt(sw, sh, zoom);
  gl.viewport(0, 0, W, H);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
  const L = LOOKS[S.look] || LOOKS.neutral;
  gl.uniform4f(prog.crop, c.x / sw, c.y / sh, c.w / sw, c.h / sh);
  gl.uniform3fv(prog.mixc, L.mix); gl.uniform3fv(prog.ts, L.ts); gl.uniform3fv(prog.th, L.th);
  gl.uniform1f(prog.con, L.con); gl.uniform1f(prog.sat, L.sat); gl.uniform1f(prog.lo, L.lo); gl.uniform1f(prog.hi, L.hi);
  gl.uniform1f(prog.k, S.lookStaerke / 100); gl.uniform1f(prog.hell, S.hell / 250); gl.uniform1f(prog.vig, (S.vignette / 100) * 0.6);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  octx.drawImage(gl_canvas, 0, 0);
}
function schrift(name) { const f = SCHRIFTEN.find((x) => x[0] === name) || SCHRIFTEN[0]; return f; }
function textMalen(zeilen, family, size, weight, yMitte, farbe, kontur, titel) {
  octx.save();
  octx.textAlign = 'center'; octx.textBaseline = 'middle';
  let groesse = size;
  const setze = () => { octx.font = `${weight} ${groesse}px "${family}"`; };
  setze();
  while (groesse > 30 && Math.max(...zeilen.map((z) => octx.measureText(z).width)) > W - 100) { groesse -= 4; setze(); }
  const lh = groesse * (titel ? 1.12 : 1.18);
  const y0 = yMitte - ((zeilen.length - 1) * lh) / 2;
  zeilen.forEach((z, i) => {
    const y = y0 + i * lh;
    if (kontur > 0) { octx.lineJoin = 'round'; octx.lineWidth = kontur * 2; octx.strokeStyle = 'rgba(25,20,18,0.95)'; octx.strokeText(z, W / 2, y); }
    octx.shadowColor = titel ? 'rgba(0,0,0,0.55)' : 'rgba(0,0,0,0.4)'; octx.shadowBlur = titel ? 14 : 6; octx.shadowOffsetY = titel ? 3 : 2;
    octx.fillStyle = farbe; octx.fillText(z, W / 2, y);
    octx.shadowColor = 'transparent';
  });
  octx.restore();
}
function overlay(outT, p) {
  if (S.titel && outT < S.titelDauer) {
    const [fam, wt] = schrift(S.titelFont);
    const zeilen = S.titel.split('\n').map((x) => x.trim()).filter(Boolean);
    textMalen(zeilen, fam, S.titelSize, wt, (S.titelY / 100) * H + (zeilen.length - 1) * S.titelSize * 0.56, '#ffffff', 0, true);
  }
  const cap = p ? p.caps.find((c) => outT >= c.a && outT < c.b) : { text: 'So sehen deine Untertitel aus' };
  if (cap) { const [fam, wt] = schrift(S.capFont); textMalen(zweiZeilen(cap.text), fam, S.capSize, wt, (S.capY / 100) * H, S.capFarbe, S.capOutline, false); }
}

// ---------------------------------------------------------------- Vorschau
let vt = null, vLaeuft = false, vNochmal = false;
const vorschauBald = () => { clearTimeout(vt); vt = setTimeout(async () => { if (vLaeuft) { vNochmal = true; return; } vLaeuft = true; try { await vorschau(); } catch (e) { console.warn(e); } vLaeuft = false; if (vNochmal) { vNochmal = false; vorschauBald(); } }, 60); };
let vorschauSink = null, vorschauBild = null, vorschauZeit = 0;
async function vorschauBildHolen(t) {
  if (!videoTrack) return null;
  if (!vorschauSink) {
    const probe = await new CanvasSink(videoTrack, { poolSize: 1 }).getCanvas(0);
    const f = Math.min(1, 1600 / Math.max(probe.canvas.width, probe.canvas.height));
    quelle.w = Math.round(probe.canvas.width * f / 2) * 2; quelle.h = Math.round(probe.canvas.height * f / 2) * 2;
    vorschauSink = new CanvasSink(videoTrack, { width: quelle.w, height: quelle.h, fit: 'fill', poolSize: 1 });
  }
  const w = await vorschauSink.getCanvas(t);
  return w ? w.canvas : null;
}
let rendertGerade = false;
async function vorschau() {
  if (rendertGerade) return;
  const v = { currentTime: vorschauZeit };
  if (!videoTrack) return;
  await schriftenLaden();
  if (!vorschauBild || vorschauBild.t !== vorschauZeit) { const c = await vorschauBildHolen(vorschauZeit); if (!c) return; vorschauBild = { t: vorschauZeit, c }; }
  bildMalen(vorschauBild.c, quelle.w, quelle.h, S.zoomA);
  let outT = 0.5, p = null;
  if (saetze.length && ton16) { p = plan(); const b = p.bereiche.find((x) => v.currentTime >= x.a && v.currentTime <= x.b); outT = b ? b.o + v.currentTime - b.a : 99; if (!b) p = null; }
  if (!p) outT = Math.min(0.5, S.titelDauer - 0.01);
  overlay(outT, p);
  const pv = $('vorschau').getContext('2d'); pv.drawImage(out, 0, 0, 540, 960);
}
let schriftenOk = null;
function schriftenLaden() {
  if (!schriftenOk) schriftenOk = Promise.all(SCHRIFTEN.map(([f, w]) => document.fonts.load(`${w} 40px "${f}"`).catch(() => null)));
  return schriftenOk;
}

// ---------------------------------------------------------------- Klick-Klaenge
function biquadBP(x, sr, f1, f2) {
  const f0 = Math.sqrt(f1 * f2), Q = f0 / (f2 - f1), w = 2 * Math.PI * f0 / sr, al = Math.sin(w) / (2 * Q);
  const b0 = al, b2 = -al, a0 = 1 + al, a1 = -2 * Math.cos(w), a2 = 1 - al;
  const y = new Float32Array(x.length); let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) { const v = (b0 * x[i] + b2 * x2 - a1 * y1 - a2 * y2) / a0; x2 = x1; x1 = x[i]; y2 = y1; y1 = v; y[i] = v; }
  return y;
}
function klangBauen(art, sr = 48000) {
  const n = Math.round(0.15 * sr), c = new Float32Array(n);
  let seed = 7; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647 * 2 - 1; };
  const rauschen = (dauer, f1, f2, dec, amp, off = 0) => {
    const m = Math.round(dauer * sr), x = new Float32Array(m); for (let i = 0; i < m; i++) x[i] = rnd();
    const y = biquadBP(x, sr, f1, f2); const o = Math.round(off * sr);
    for (let i = 0; i < m && o + i < n; i++) c[o + i] += y[i] * Math.exp(-i / (dec * sr)) * amp * 4;
  };
  const ton = (f, dec, amp, off = 0, f2 = f) => {
    const o = Math.round(off * sr), m = Math.round(Math.min(0.12, dec * 8) * sr); let ph = 0;
    for (let i = 0; i < m && o + i < n; i++) { const fr = f + (f2 - f) * (i / m); ph += 2 * Math.PI * fr / sr; c[o + i] += Math.sin(ph) * Math.exp(-i / (dec * sr)) * amp; }
  };
  if (art === 'maus') { rauschen(0.025, 3500, 11000, 0.0012, 1); ton(4200, 0.003, 0.6); ton(7266, 0.002, 0.25); rauschen(0.025, 3500, 11000, 0.0012, 0.55, 0.075); ton(4700, 0.003, 0.33, 0.075); }
  else if (art === 'tastatur') { rauschen(0.03, 1500, 6000, 0.002, 1); ton(1800, 0.005, 0.5); ton(320, 0.008, 0.5); rauschen(0.03, 2000, 7000, 0.0015, 0.5, 0.09); ton(2100, 0.004, 0.3, 0.09); }
  else if (art === 'schreibmaschine') { rauschen(0.04, 2000, 9000, 0.003, 1); ton(3200, 0.025, 0.35); ton(5100, 0.02, 0.2); ton(150, 0.015, 0.7); }
  else if (art === 'weich') { rauschen(0.03, 1000, 4000, 0.004, 0.8); ton(900, 0.01, 0.5); }
  else if (art === 'tick') { ton(6000, 0.0015, 1); rauschen(0.01, 5000, 12000, 0.0008, 0.6); }
  else if (art === 'pop') { ton(900, 0.03, 1, 0, 300); }
  let m = 0; for (const v of c) m = Math.max(m, Math.abs(v)); if (m) for (let i = 0; i < n; i++) c[i] *= 0.95 / m;
  return c;
}
$('s_klangDatei').addEventListener('change', async (ev) => {
  const f = ev.target.files[0]; if (!f) return;
  const ctx = new OfflineAudioContext(1, 1, 48000);
  const b = await ctx.decodeAudioData(await f.arrayBuffer());
  const mono = new Float32Array(b.length); for (let ch = 0; ch < b.numberOfChannels; ch++) { const d = b.getChannelData(ch); for (let i = 0; i < b.length; i++) mono[i] += d[i] / b.numberOfChannels; }
  klangDatei = await resample(mono, b.sampleRate, 48000);
  S.klang = 'eigen'; felderFuellen(); speichern();
});
async function aktuellerKlang() {
  if (S.klang === 'aus') return null;
  if (S.klang === 'eigen') return klangDatei;
  return klangBauen(S.klang);
}
$('klangTest').onclick = async () => {
  const k = await aktuellerKlang(); if (!k) return;
  const ctx = new AudioContext(); const b = ctx.createBuffer(1, k.length, 48000); b.copyToChannel(k, 0);
  const s = ctx.createBufferSource(); const g = ctx.createGain(); g.gain.value = S.klangLaut / 100 * 0.7; s.buffer = b; s.connect(g).connect(ctx.destination); s.start();
};

// ---------------------------------------------------------------- Ton zusammensetzen
async function tonBauen(p) {
  const sr = 48000;
  let L = ton.L, R = ton.R;
  if (ton.rate !== sr) { L = await resample(ton.L, ton.rate, sr); R = ton.R === ton.L ? L : await resample(ton.R, ton.rate, sr); }
  const len = Math.round(p.dauer * sr);
  const oL = new Float32Array(len), oR = new Float32Array(len);
  for (const b of p.bereiche) {
    const a = Math.round(b.a * sr), e = Math.round(b.b * sr), o = Math.round(b.o * sr);
    const n = Math.min(e - a, len - o), fi = Math.round(0.015 * sr), fo = Math.round(0.02 * sr);
    for (let i = 0; i < n; i++) {
      let g = 1; if (i < fi) g = i / fi; if (n - i < fo) g = Math.min(g, (n - i) / fo);
      oL[o + i] = (L[a + i] || 0) * g; oR[o + i] = (R[a + i] || 0) * g;
    }
  }
  // Lautheit: Sprachanteil auf ca. -17 dBFS RMS (entspricht grob -14 LUFS)
  const blk = 2400; const lv = [];
  for (let i = 0; i + blk <= len; i += blk) { let s = 0; for (let k = i; k < i + blk; k++) s += oL[k] * oL[k] + oR[k] * oR[k]; lv.push(10 * Math.log10(s / (2 * blk) + 1e-12)); }
  const sprache = lv.filter((x) => x > -45); const mittel = sprache.length ? 10 * Math.log10(sprache.reduce((s, x) => s + Math.pow(10, x / 10), 0) / sprache.length) : -20;
  const gain = Math.pow(10, (-17 - mittel) / 20);
  for (let i = 0; i < len; i++) { oL[i] *= gain; oR[i] *= gain; }
  // Klicks in die naechste leise Stelle
  const klang = await aktuellerKlang(); const klicks = [];
  if (klang && S.klangAbstand > 0) {
    const vol = (S.klangLaut / 100) * 0.9, such = Math.min(1, S.klangAbstand * 0.4);
    const pegel = (t) => { const i = Math.round(t * sr), m = Math.round(0.08 * sr); let s = 0; for (let k = i; k < i + m && k < len; k++) s += oL[k] * oL[k]; return s; };
    for (let k = S.klangAbstand; k < p.dauer - 0.5; k += S.klangAbstand) {
      let best = k, bv = 1e9; for (let t = k - such; t <= k + such; t += 0.02) { const v = pegel(t); if (v < bv) { bv = v; best = t; } }
      klicks.push(best); const o = Math.round(best * sr);
      for (let i = 0; i < klang.length && o + i < len; i++) { oL[o + i] += klang[i] * vol; oR[o + i] += klang[i] * vol; }
    }
  }
  // Limiter bei -1,5 dBFS (5 ms Vorschau, 80 ms Rueckkehr)
  const ceil = 0.84, la = Math.round(0.005 * sr), rel = Math.exp(-1 / (0.08 * sr));
  const noetig = new Float32Array(len);
  for (let i = 0; i < len; i++) { const m = Math.max(Math.abs(oL[i]), Math.abs(oR[i])); noetig[i] = m > ceil ? ceil / m : 1; }
  let g = 1; const q = []; // gleitendes Minimum
  for (let i = 0; i < len; i++) {
    const j = i + la; if (j < len) { while (q.length && noetig[q[q.length - 1]] >= noetig[j]) q.pop(); q.push(j); }
    while (q.length && q[0] < i) q.shift();
    const ziel = q.length ? Math.min(noetig[q[0]], 1) : 1;
    g = ziel < g ? ziel : ziel - (ziel - g) * rel;
    oL[i] *= g; oR[i] *= g;
  }
  const buf = new AudioBuffer({ length: len, numberOfChannels: 2, sampleRate: sr });
  buf.copyToChannel(oL, 0); buf.copyToChannel(oR, 1);
  return { buf, klicks };
}

// ---------------------------------------------------------------- Rendern
$('rendern').onclick = rendern;
async function rendern() {
  $('rendern').disabled = true; $('ausgabe').innerHTML = ''; rendertGerade = true;
  const t0 = performance.now();
  try {
    await schriftenLaden(); await tonLaden();
    const p = plan();
    if (!p.shots.length) throw new Error('Keine Sätze ausgewählt.');
    rStatus('Ton wird gemischt …'); rFortschritt(0);
    const { buf, klicks } = await tonBauen(p);
    const vCodec = window.__testVideoCodec || 'avc';
    if (!(await canEncodeVideo(vCodec, { width: W, height: H }))) throw new Error('Dieser Browser kann kein H.264 kodieren — bitte Chrome verwenden.');
    const aCodec = await getFirstEncodableAudioCodec(['aac', 'opus'], { numberOfChannels: 2, sampleRate: 48000 });
    if (!aCodec) throw new Error('Dieser Browser kann keinen Ton kodieren.');
    const output = new Output({ format: new Mp4OutputFormat({ fastStart: 'in-memory' }), target: new BufferTarget() });
    const vSrc = new CanvasSource(out, { codec: vCodec, bitrate: parseInt(S.bitrate, 10), keyFrameInterval: 2 });
    const aSrc = new AudioBufferSource({ codec: aCodec, bitrate: 192000 });
    output.addVideoTrack(vSrc, { frameRate: quelle.fps });
    output.addAudioTrack(aSrc);
    await output.start();
    await aSrc.add(buf);
    aSrc.close();
    // Quellbild in passender Aufloesung dekodieren (Drehung uebernimmt Mediabunny)
    const probe = new CanvasSink(videoTrack, { poolSize: 1 });
    const erstes = await probe.getCanvas(p.shots[0].s);
    const sw0 = erstes.canvas.width, sh0 = erstes.canvas.height;
    const f = Math.min(1, 2560 / Math.max(sw0, sh0));
    const sw = Math.round(sw0 * f / 2) * 2, sh = Math.round(sh0 * f / 2) * 2;
    const sink = new CanvasSink(videoTrack, { width: sw, height: sh, fit: 'fill', poolSize: 2 });
    const fd = 1 / quelle.fps; let letzte = -1, frames = 0;
    for (let si = 0; si < p.shots.length; si++) {
      const sh_ = p.shots[si];
      for await (const w of sink.canvases(sh_.s, sh_.e)) {
        if (w.timestamp < sh_.s - fd / 2 || w.timestamp >= sh_.e) continue;
        const ot = Math.round((sh_.o + (w.timestamp - sh_.s)) / fd) * fd;
        if (ot <= letzte + 1e-6 || ot >= p.dauer) continue;
        bildMalen(w.canvas, sw, sh, sh_.zoom);
        overlay(ot, p);
        await vSrc.add(ot, fd);
        letzte = ot; frames++;
        if (frames % 15 === 0) {
          rFortschritt(ot / p.dauer);
          const verg = (performance.now() - t0) / 1000;
          rStatus(`Rendere … ${ot.toFixed(1)} / ${p.dauer.toFixed(1)} Sek. (noch ca. ${Math.max(0, Math.round(verg / (ot / p.dauer) - verg))} Sek.)`);
          if (frames % 90 === 0) $('vorschau').getContext('2d').drawImage(out, 0, 0, 540, 960);
        }
      }
    }
    vSrc.close();
    await output.finalize();
    const blob = new Blob([output.target.buffer], { type: 'video/mp4' });
    const url = URL.createObjectURL(blob);
    const name = (S.titel || 'reel').replace(/\s+/g, '_').replace(/[^\wäöüÄÖÜß_-]/g, '').slice(0, 40) + '.mp4';
    $('ausgabe').innerHTML = `<video controls playsinline src="${url}"></video><a class="download" href="${url}" download="${name}">⬇ ${name} herunterladen (${(blob.size / 1e6).toFixed(1)} MB)</a>`;
    rFortschritt(1);
    rStatus(`Fertig in ${Math.round((performance.now() - t0) / 1000)} Sek.: ${p.dauer.toFixed(1)} Sek. Reel statt ${quelle.dauer.toFixed(1)} Sek., ${p.shots.length} Schnitte, ${klicks.length} Klicks.`);
    window.__ergebnis = blob;
  } catch (e) { console.error(e); rStatus('Fehler: ' + e.message); }
  $('rendern').disabled = false; rendertGerade = false;
}

// Test-Zugang (fuer automatische Pruefung)
window.__reel = { get S() { return S; }, get saetze() { return saetze; }, set saetze(v) { saetze = v; zeigeSaetze(); }, plan, rendern, tonLaden, sprechstellen, zuSaetzen };
