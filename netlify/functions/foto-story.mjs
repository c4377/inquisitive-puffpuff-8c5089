// Netlify Function: Foto-Story — aus EINEM echten Foto eine Story-Sequenz mit 7 Slides.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { bild: "data:image/jpeg;base64,…", moment?: "…", variante: 1|2|3 }  ->  { titel, idee, slides: [{ text, sticker }] }
// Die App fragt die drei Varianten parallel an (je eine Storyline), damit keine Anfrage zu lange dauert.
// Zielkundin und Fakten kommen aus dem Story-Studio (gleiche Stimme, gleiche Regeln).
import { HINTERGRUND } from './story-studio.mjs';

const VARIANTEN = {
  1: `STORYLINE „DER MOMENT“
Slide 1 startet bei dem, was auf dem Foto wirklich zu sehen ist (oder was Carina zum Moment geschrieben hat), ganz alltäglich, ohne Anlauf.
Slide 2–3: Was dieser Moment mit der Coachin zu tun hat, die postet und nicht verkauft.
Slide 4: Das große Missverständnis, fair benannt.
Slide 5: Carinas Sicht, begründet (warum, nicht nur was).
Slide 6: Der Frame: ein Satz, den man screenshotten will.
Slide 7: Die Entscheidung, ohne Druck.`,
  2: `STORYLINE „DAS MISSVERSTÄNDNIS“
Das Foto ist nur die Kulisse, die Sequenz geht um ein Verhalten.
Slide 1: Eine klare Aussage gegen ein typisches Verhalten von Coaches, die posten und nicht verkaufen.
Slide 2: Drei kurze Parallelsätze, die das gewohnte Verhalten zeigen.
Slide 3: „Aber …“ – was dabei fehlt.
Slide 4–5: Warum? Die Antwort, Schritt für Schritt, gern 1. 2.
Slide 6: Der neue Standard, harter Abschluss.
Slide 7: Selbst-Selektion: „Wenn du … willst: …“`,
  3: `STORYLINE „FRAG DICH SELBST“
Interaktiv, zum Mitmachen. Das Foto ist die ruhige Kulisse.
Slide 1: Eine direkte Frage an die Leserin, die sie ertappt.
Slide 2: Eine Umfrage dazu (sticker: „📊 Umfrage: … / …“), der Text stellt die Frage.
Slide 3: Was die meisten antworten würden und warum das verständlich ist.
Slide 4–5: Carinas Sicht darauf, begründet.
Slide 6: Der Satz, der hängen bleibt.
Slide 7: Eine Frage zurück, die man per Sticker beantworten kann (sticker: „💬 Fragen-Sticker: …“).`,
};

const PROMPT = `Du bist Story Writer für Carina Anna Prav (Mentorin für Coaches: Content, Angebote, Verkaufen).

AUFGABE
Carina gibt dir ein echtes Foto aus ihrem Alltag. Du schreibst daraus EINE Instagram-Story-Sequenz mit genau 7 Slides, nur Text, der auf diesem Foto steht. Zielgruppe ist ausschließlich die Coachin, die postet und nicht verkauft.

{{VARIANTE}}

DAS FOTO
- Nutze nur, was auf dem Foto klar zu sehen ist, und was Carina selbst dazu schreibt. Erfinde keinen Ort, keine Uhrzeit, keine Personen, keine Handlung, die nicht sichtbar oder genannt ist.
- Wenn unklar ist, was passiert, beschreib nicht, sondern bleib beim Gedanken.
{{MOMENT}}

STIL (Carinas Stimme)
- Ich-Perspektive, du-Ansprache, souverän, warm, klar. Kurze Sätze, Fragmente als Pointe.
- Jede Slide höchstens 120 Zeichen, höchstens 3 kurze Zeilen. Keine Füllslides.
- Denglisch erlaubt, Emojis höchstens eins pro Sequenz.

FESTE REGELN
- Immer Deutsch. Zahlen als Ziffern.
- Nichts erfinden: keine Zahlen, keine Kundinnen-Zitate, keine Erlebnisse. Fakten nur aus der Liste unten und nur, wenn sie wirklich passen.
- Nie „Verkaufslücke“, stattdessen „Funkstille zwischen Like und Anfrage“.
- „Sprachnotiz“ oder „Voice“, nie „Sprachi“.
- Keine Preise. Kurse und Programme nie als Gegner, Gegner ist das Verhalten. Nie Vorwürfe an die Leserin.
- Kein CTA mit Codewort, außer die Storyline verlangt einen Sticker.

${HINTERGRUND}

AUSGABE (technisch, für die App)
Antworte NUR mit JSON, ohne Vorwort, ohne Markdown:
{"titel":"2–4 Wörter","idee":"ein Satz, worum es geht","slides":[{"text":"…","sticker":""}]}
- Genau 7 Einträge in "slides".
- "text": genau so, wie er auf die Story kommt, Zeilen getrennt mit \\n.
- In jedem "text" genau EIN Schlüsselwort mit Sternchen, z. B. „Likes zahlen deine *Miete* nicht.“
- "sticker": nur wenn die Storyline es verlangt, sonst "".`;

export default async (req) => {
  if (req.method !== 'POST') return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  const key = process.env.GEMINI_API_KEY;
  if (!key) return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  let bild = '', moment = '', variante = 1;
  try {
    const body = await req.json();
    bild = String(body.bild || '');
    moment = String(body.moment || '').replace(/\s+/g, ' ').trim().slice(0, 800);
    variante = [1, 2, 3].includes(Number(body.variante)) ? Number(body.variante) : 1;
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  const m = /^data:(image\/(?:jpeg|png|webp));base64,([A-Za-z0-9+/=]+)$/.exec(bild);
  if (!m || m[2].length > 6_000_000) return new Response(JSON.stringify({ error: 'Bitte ein Foto (JPEG/PNG) mitschicken.' }), { status: 400 });

  const prompt = PROMPT.replace('{{VARIANTE}}', VARIANTEN[variante])
    .replace('{{MOMENT}}', moment ? `- Carina schreibt zum Moment (echt, das ist dein Material): ${moment}` : '- Carina hat nichts zum Moment geschrieben. Bleib deshalb beim Gedanken und beschreib das Foto höchstens allgemein.');

  const MODELLE = ['gemini-3.6-flash', 'gemini-3-flash', 'gemini-flash-latest', 'gemini-2.5-flash'];
  try {
    let data = null, r = null, letzterFehler = '';
    for (const modell of MODELLE) {
      r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ inline_data: { mime_type: m[1], data: m[2] } }, { text: prompt }] }],
          generationConfig: { temperature: 0.9, responseMimeType: 'application/json' },
        }),
      });
      data = await r.json();
      if (r.ok) break;
      letzterFehler = data?.error?.message || `HTTP ${r.status}`;
      const modellProblem = r.status === 404 || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
      if (!modellProblem) break;
    }
    if (!r.ok) return new Response(JSON.stringify({ error: letzterFehler || 'Gemini-Fehler' }), { status: 502 });
    const roh = (data?.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('').trim();
    const sauber = roh.replace(/^```json\s*|```$/g, '').trim();
    let out;
    try { out = JSON.parse(sauber); } catch {
      const a = sauber.indexOf('{'), b = sauber.lastIndexOf('}');
      out = a >= 0 && b > a ? JSON.parse(sauber.slice(a, b + 1)) : {};
    }
    const slides = (Array.isArray(out.slides) ? out.slides : []).slice(0, 7)
      .map((s) => ({ text: String(s?.text || '').trim(), sticker: String(s?.sticker || '').trim() }))
      .filter((s) => s.text);
    if (slides.length < 5) return new Response(JSON.stringify({ error: 'Keine vollständige Storyline erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ titel: String(out.titel || '').trim().slice(0, 60), idee: String(out.idee || '').trim().slice(0, 200), slides }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
