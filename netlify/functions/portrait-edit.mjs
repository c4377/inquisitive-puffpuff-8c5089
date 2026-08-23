// Netlify Function: aus EINEM Ausgangsbild ein neues Motiv machen.
//
// Uebernommen aus der Portrait-App und um zwei Dinge ergaenzt:
//   1. eine Modell-Kaskade — Google benennt Bildmodelle regelmaessig um und
//      schaltet alte ab; ein fest verdrahteter Name legt die Funktion sonst
//      irgendwann still.
//   2. ein optionales Zielformat, damit dasselbe Bild als Pin (2:3),
//      Post (4:5) oder Anzeige (1:1) angefordert werden kann.
//
// POST { prompt, imageBase64, mimeType, format } -> { image: { base64Data, mimeType } }

const MODELLE = ['gemini-3-pro-image', 'gemini-flash-image-latest', 'gemini-2.5-flash-image'];

const FORMATE = {
  pin: 'Vertical 2:3 composition (Pinterest pin), subject placed slightly lower third, generous empty space in the upper half for a headline.',
  post: 'Vertical 4:5 composition (Instagram post), subject centred, calm space around the head.',
  ad: 'Square 1:1 composition, subject centred, even margins.',
  frei: '',
};

export default async (req) => {
  if (req.method !== 'POST') return json({ error: 'Nur POST erlaubt' }, 405);

  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return json({ error: 'GEMINI_API_KEY ist nicht gesetzt (Netlify → Environment variables).' }, 500);
  }

  try {
    const { prompt, imageBase64, mimeType, format } = await req.json();
    if (!prompt || !imageBase64) return json({ error: 'prompt oder Bild fehlt' }, 400);

    const zusatz = FORMATE[format] || '';
    const volltext = zusatz ? `${prompt}\n\nCOMPOSITION: ${zusatz}` : prompt;

    let res = null, data = null, letzterFehler = '';
    for (const modell of MODELLE) {
      res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{
              parts: [
                { inline_data: { mime_type: mimeType || 'image/jpeg', data: imageBase64 } },
                { text: volltext },
              ],
            }],
          }),
        }
      );
      data = await res.json().catch(() => ({}));
      if (res.ok) break;
      letzterFehler = data?.error?.message || `Gemini-Fehler (${res.status})`;
      const modellProblem = res.status === 404
        || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
      if (!modellProblem) break;
    }
    if (!res.ok) return json({ error: letzterFehler }, 502);

    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imagePart = parts.find((p) => p.inline_data || p.inlineData);
    const inline = imagePart?.inline_data || imagePart?.inlineData;
    if (!inline?.data) return json({ error: 'Keine Bilddaten in der Antwort' }, 502);

    return json({
      image: { base64Data: inline.data, mimeType: inline.mime_type || inline.mimeType || 'image/png' },
    });
  } catch (err) {
    return json({ error: `Serverfehler: ${err.message}` }, 500);
  }
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status, headers: { 'Content-Type': 'application/json' },
  });
}
