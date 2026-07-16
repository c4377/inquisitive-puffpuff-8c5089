// Netlify Function: AI ad-background generation via Google Gemini.
// The API key stays SERVER-SIDE (env var GEMINI_API_KEY) — never in the app.
// POST { prompt: string } -> { image: "data:image/png;base64,..." }

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let prompt = '';
  try {
    const body = await req.json();
    prompt = String(body.prompt || '').slice(0, 2000);
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!prompt) return new Response(JSON.stringify({ error: 'prompt fehlt' }), { status: 400 });

  try {
    const r = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=${key}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { responseModalities: ['IMAGE'] },
        }),
      }
    );
    const data = await r.json();
    if (!r.ok) {
      return new Response(JSON.stringify({ error: data?.error?.message || 'Gemini-Fehler' }), { status: 502 });
    }
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imgPart = parts.find((p) => p.inlineData?.data);
    if (!imgPart) {
      return new Response(JSON.stringify({ error: 'Kein Bild in der Antwort' }), { status: 502 });
    }
    const mime = imgPart.inlineData.mimeType || 'image/png';
    return new Response(
      JSON.stringify({ image: `data:${mime};base64,${imgPart.inlineData.data}` }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e.message || e) }), { status: 500 });
  }
};
