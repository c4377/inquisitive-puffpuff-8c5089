// Netlify Function: AI post designer. Instead of fixed layout presets, a
// multimodal model designs each post freely — position, size, weight, colour —
// guided by classic design principles (whitespace, hierarchy, contrast), the
// reference feed style, and a summary of the PREVIOUS post for feed rhythm.
// POST { text, isHook, hasImage, prevSummary, palette } -> { spec: {...} }
// The app renders the returned spec directly (specRenderer in canvasRenderer).

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let body = {};
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  const text = String(body.text || '').slice(0, 600);
  const isHook = body.isHook === true;
  const hasImage = body.hasImage === true;
  const prevSummary = String(body.prevSummary || 'none').slice(0, 300);
  const palette = body.palette || {};

  const prompt = `You are a senior editorial graphic designer. Design ONE Instagram feed tile (portrait 4:5, canvas 1080x1350) for a calm premium coach brand, in the style of the reference account marina.persano: warm near-white and khaki-greige plates, Helvetica-style grotesk, centered text blocks, a light/bold word rhythm, one underlined key word, a warm-tan closing clause, generous whitespace, text never in the bottom 15% (reserved footer).

BRAND PALETTE: ${JSON.stringify(palette)}
POST TEXT (must appear, may be split into elements, do not rewrite): "${text}"
SLIDE ROLE: ${isHook ? 'HOOK (first slide, may use one big statement)' : 'FOLLOW-UP (calm, one weight)'}
BACKGROUND: ${hasImage ? 'a portrait PHOTO fills the canvas (you may add a dark overlay 0-0.5 for depth/readability)' : 'a flat colour plate (pick from palette)'}
PREVIOUS POST (for feed rhythm — vary from it): ${prevSummary}

Apply real design judgement: whitespace balance, visual hierarchy, optical centering, contrast. Vary from the previous post (light vs dark, text position high vs low).

Respond with ONLY strict JSON, no markdown, no commentary:
{
 "background": {"type": "${hasImage ? 'photo' : 'plate'}", "color": "#hex (plate colour or overlay tint)", "overlay": 0.0-0.5},
 "elements": [
   {"content":"text part","x":0.0-1.0,"y":0.06-0.82,"width":0.5-0.9,"align":"center|left","fontSize":30-120,"fontWeight":"300|400|700","color":"#hex","italic":false,"underline":false,"lineHeight":1.0-1.3}
 ],
 "summary": "one line describing this design (bg tone, text position) for the next post's rhythm"
}
Rules: x/y are the CENTER of each text block as canvas fractions. All post text must be covered by the elements. Max 4 elements. y+height of text must stay above 0.85.`;

  try {
    const r = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${key}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.7, responseMimeType: 'application/json' },
        }),
      }
    );
    const data = await r.json();
    const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
    let spec = null;
    try { spec = JSON.parse(raw.replace(/```json|```/g, '').trim()); } catch { /* below */ }
    if (!spec || !Array.isArray(spec.elements) || spec.elements.length === 0) {
      return new Response(JSON.stringify({ error: 'KI-Antwort unbrauchbar', raw: raw.slice(0, 300) }), { status: 502 });
    }
    return new Response(JSON.stringify({ spec }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};

export const config = { path: '/.netlify/functions/design-post' };
