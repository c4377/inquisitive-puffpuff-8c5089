// Netlify Function: 2 Kommentare zum Kopieren für einen Post (Carinas Stimme).
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { caption, titel, slides: ["…"] }  ->  { kommentare: [{ art, text }, { art, text }] }
// POST { art: "alt", caption, titel, slides } ->  { alttexte: ["…" je Slide] }  (Instagram-Alternativtext)

const PROMPT = `Du schreibst für mich, Carina Anna Prav (@carinaannaprav), Business-Mentorin für Coaches, ZWEI Kommentare, die ich selbst unter meinen eigenen Instagram-Post setze. Meine Community sind die „Ja-Sagerinnen": Frauen, die Opportunities sehen, sich weiterbilden und Ja zu sich sagen.

DER POST
Titel: {{TITEL}}
Slides:
{{SLIDES}}
Caption:
{{CAPTION}}

KOMMENTAR 1 – „Anpinnen": ein Gesprächsstarter zum Thema dieses Posts. Eine Frage, die man in einem Wort, mit A/B oder einem Emoji beantworten kann. Sie soll sich angesprochen fühlen, nicht abgefragt.
KOMMENTAR 2 – „Nachlegen": ein Gedanke, der NICHT schon in Caption oder Slides steht (ein Satz mehr Tiefe, ein ehrlicher Nachsatz), danach ein sanfter nächster Schritt: speichern, einer Freundin schicken oder „Schreib mir STARTEN" per DM. Nur EIN Schritt.

STIMME
- Du-Form, an EINE Frau. Direkt, warm, ein bisschen rebellisch, große Schwester. Denglisch erlaubt, höchstens ein Emoji pro Kommentar, keine Hashtags.
- Kurz: je 1–3 Sätze, höchstens 220 Zeichen. Klingt wie getippt, nicht wie Werbung.
- Kein „hier ist die Sache", kein „es ist nicht X, es ist Y", keine Floskeln wie „Was denkst du?".
- Echte Zahlen oder gar keine. Nichts erfinden, keine erfundenen Kundinnen-Geschichten.
- Angebote nur, wenn es sie wirklich gibt (Das Intensive, Das 1:1, Done-for-you Content, Offer Incubator).

Antworte NUR mit JSON, ohne Vorwort, ohne Markdown:
{"kommentare":[{"art":"Anpinnen","text":"…"},{"art":"Nachlegen","text":"…"}]}`;

const ALT = `Schreib für jede Slide dieses Instagram-Karussells von Carina Anna Prav (@carinaannaprav, Business-Mentorin für Coaches) einen Alternativtext, wie man ihn in Instagram unter „Erweiterte Einstellungen → Alternativtext" einträgt. Zweck: Barrierefreiheit, und Instagram soll den Post thematisch richtig einordnen.

DER POST
Titel: {{TITEL}}
Slides:
{{SLIDES}}
Caption:
{{CAPTION}}

REGELN
- Genau {{ANZAHL}} Alternativtexte, einer pro Slide, in derselben Reihenfolge.
- Je höchstens 100 Zeichen. Deutsch. Keine Hashtags, keine Emojis.
- Sag, was auf der Slide steht: den Kernsatz der Slide in „…" (gekürzt, sinngemäß) und das Thema in natürlichen Suchbegriffen, nach denen Coaches suchen würden (z. B. Angebot verkaufen, Preise, Content für Coaches, Sichtbarkeit, Business aufbauen) – nur was zum Inhalt passt.
- Slide 1 beginnt mit „Carina Anna Prav, Business-Mentorin für Coaches:".
- Beschreibe nichts, was du nicht sicher weißt: keine Farben, Personen, Kleidung oder Fotos erfinden.
- Keine erfundenen Zahlen.

Antworte NUR mit JSON, ohne Vorwort, ohne Markdown:
{"alttexte":["…","…"]}`;

async function gemini(key, prompt, temperature) {
  // Wie in story-studio: Modelle der Reihe nach, falls Google eines umbenennt.
  const MODELLE = ['gemini-3.6-flash', 'gemini-3-flash', 'gemini-flash-latest', 'gemini-2.5-flash'];
  let data = null, r = null, letzterFehler = '';
  for (const modell of MODELLE) {
    r = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature, responseMimeType: 'application/json' },
        }),
      }
    );
    data = await r.json();
    if (r.ok) break;
    letzterFehler = data?.error?.message || `HTTP ${r.status}`;
    const modellProblem = r.status === 404 || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
    if (!modellProblem) break;
  }
  if (!r.ok) throw Object.assign(new Error(letzterFehler || 'Gemini-Fehler'), { status: 502 });
  const roh = (data?.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('').trim();
  const sauber = roh.replace(/^```json\s*|```$/g, '').trim();
  try { return JSON.parse(sauber); } catch {
    const a = sauber.indexOf('{'), b = sauber.lastIndexOf('}');
    return a >= 0 && b > a ? JSON.parse(sauber.slice(a, b + 1)) : {};
  }
}

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }
  let caption = '', titel = '', slides = [], art = '';
  try {
    const body = await req.json();
    art = String(body.art || '');
    caption = String(body.caption || '').trim().slice(0, 3000);
    titel = String(body.titel || '').trim().slice(0, 200);
    slides = (Array.isArray(body.slides) ? body.slides : []).map((x) => String(x || '').trim()).filter(Boolean).slice(0, 12);
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!caption && !slides.length) return new Response(JSON.stringify({ error: 'Erst Caption oder Slides schreiben.' }), { status: 400 });

  const slidesText = slides.length ? slides.map((x, k) => `${k + 1}. ${x.slice(0, 500)}`).join('\n') : '—';
  try {
    if (art === 'alt') {
      const anzahl = Math.max(1, slides.length);
      const prompt = ALT.replace('{{TITEL}}', titel || '—').replace('{{SLIDES}}', slidesText)
        .replace('{{CAPTION}}', caption || '—').replace('{{ANZAHL}}', String(anzahl));
      const out = await gemini(key, prompt, 0.4);
      const alttexte = (Array.isArray(out.alttexte) ? out.alttexte : []).map((x) => String(x || '').replace(/\s+/g, ' ').trim()).filter(Boolean).slice(0, anzahl);
      if (!alttexte.length) return new Response(JSON.stringify({ error: 'Keine Alternativtexte erhalten. Nochmal versuchen.' }), { status: 502 });
      return new Response(JSON.stringify({ alttexte }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
    const prompt = PROMPT.replace('{{TITEL}}', titel || '—').replace('{{SLIDES}}', slidesText).replace('{{CAPTION}}', caption || '—');
    const out = await gemini(key, prompt, 0.9);
    const kommentare = (Array.isArray(out.kommentare) ? out.kommentare : []).slice(0, 2)
      .map((k, i) => ({ art: String(k?.art || (i ? 'Nachlegen' : 'Anpinnen')).trim(), text: String(k?.text || '').trim() }))
      .filter((k) => k.text);
    if (kommentare.length < 2) return new Response(JSON.stringify({ error: 'Keine Kommentare erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ kommentare }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: e?.status || 500 });
  }
};
