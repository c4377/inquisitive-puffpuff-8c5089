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

Respond with ONLY strict, valid JSON (no markdown, no commentary, no ranges — concrete numbers only). Shape, shown here as a filled example:
{"background":{"type":"plate","color":"#F7F5F1","overlay":0},"elements":[{"content":"Der schnellste Weg","x":0.5,"y":0.34,"width":0.8,"align":"center","fontSize":58,"fontWeight":"300","color":"#252220","italic":false,"underline":false,"lineHeight":1.1}],"summary":"light cream plate, text upper third"}
Constraints: background.type must be "${hasImage ? 'photo' : 'plate'}". overlay between 0 and 0.5. x and y are the CENTER of each text block as canvas fractions; y between 0.06 and 0.80. width between 0.5 and 0.9. fontSize between 30 and 120 (canvas 1080 wide). fontWeight one of "300","400","700". Max 4 elements. All post text must be covered by the elements, split naturally. The summary is one line describing bg tone and text position for the next post's rhythm.`;

  try {
    // Model fallback chain: API availability differs per key/region.
    const models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash'];
    let raw = '';
    let lastErr = '';
    for (const model of models) {
      // 2.5 models "think" by default, which can consume the whole output
      // budget and return an EMPTY text part — disable thinking and give a
      // generous output budget.
      const genCfg = {
        temperature: 0.7,
        responseMimeType: 'application/json',
        maxOutputTokens: 4096,
      };
      if (model.startsWith('gemini-2.5')) genCfg.thinkingConfig = { thinkingBudget: 0 };
      const r = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: genCfg,
          }),
        }
      );
      const data = await r.json();
      if (data?.error) { lastErr = `${model}: ${data.error.message || data.error.status}`; continue; }
      // Collect ALL text parts — some responses split JSON across parts.
      const parts = data?.candidates?.[0]?.content?.parts || [];
      raw = parts.map((p) => p?.text || '').join('');
      if (raw) break;
      const finish = data?.candidates?.[0]?.finishReason || 'leer';
      lastErr = `${model}: keine Antwort (${finish})`;
    }
    if (!raw) {
      return new Response(JSON.stringify({ error: `KI nicht erreichbar — ${lastErr}` }), { status: 502 });
    }
    // Tolerant JSON extraction: strip fences and anything around the outermost object.
    let jsonStr = raw.replace(/```json|```/g, '').trim();
    const first = jsonStr.indexOf('{');
    const last = jsonStr.lastIndexOf('}');
    if (first > 0 || last < jsonStr.length - 1) jsonStr = jsonStr.slice(first, last + 1);
    let spec = null;
    try { spec = JSON.parse(jsonStr); } catch { /* below */ }
    if (!spec || !Array.isArray(spec.elements) || spec.elements.length === 0) {
      return new Response(JSON.stringify({ error: `KI-Antwort unbrauchbar: ${raw.slice(0, 200)}` }), { status: 502 });
    }
    return new Response(JSON.stringify({ spec }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};

export const config = { path: '/.netlify/functions/design-post' };
