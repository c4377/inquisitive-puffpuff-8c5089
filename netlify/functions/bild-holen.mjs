/**
 * BILD-UMWEG.
 *
 * Fotos, die in der Cloud liegen, lassen sich im Browser nicht immer auf
 * eine Leinwand zeichnen. Der Browser verlangt dafuer eine Erlaubnis vom
 * Speicherort (CORS). Fehlt sie, schlaegt das Laden fehl — und zwar
 * STILL: kein Fehler, kein Hinweis, das Bild ist einfach weg. Genau
 * deshalb kamen in den Pins nur die wenigen Fotos vor, die lokal als
 * base64 gespeichert sind.
 *
 * Auf dem Server gibt es diese Beschraenkung nicht. Diese Funktion holt
 * das Bild also serverseitig und reicht es als Data-URL zurueck.
 *
 * POST { url } -> { image: "data:image/jpeg;base64,…" }
 */
export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Nur POST' }), { status: 405 });
  }

  let url = '';
  try {
    const body = await req.json();
    url = String(body.url || '');
  } catch {
    return new Response(JSON.stringify({ error: 'Kein gültiger Aufruf' }), { status: 400 });
  }

  // NUR https, und keine internen Adressen. Ohne diese Pruefung waere die
  // Funktion ein offener Tuersteher: jemand koennte sie benutzen, um von
  // aussen an Adressen zu kommen, die nur der Server erreicht.
  let ziel;
  try {
    ziel = new URL(url);
  } catch {
    return new Response(JSON.stringify({ error: 'Keine gültige Adresse' }), { status: 400 });
  }
  const verboten = /^(localhost$|127\.|10\.|192\.168\.|169\.254\.|0\.|\[?::1)/i;
  if (ziel.protocol !== 'https:' || verboten.test(ziel.hostname)) {
    return new Response(JSON.stringify({ error: 'Adresse nicht erlaubt' }), { status: 400 });
  }

  try {
    const res = await fetch(ziel.toString(), { signal: AbortSignal.timeout(7000) });
    if (!res.ok) {
      return new Response(JSON.stringify({ error: `Bild antwortete mit ${res.status}` }), { status: 502 });
    }

    const typ = res.headers.get('content-type') || '';
    if (!typ.startsWith('image/')) {
      return new Response(JSON.stringify({ error: 'Das ist kein Bild' }), { status: 415 });
    }

    const roh = await res.arrayBuffer();
    // Obergrenze, damit eine sehr grosse Datei die Funktion nicht sprengt.
    if (roh.byteLength > 8 * 1024 * 1024) {
      return new Response(JSON.stringify({ error: 'Bild zu groß (über 8 MB)' }), { status: 413 });
    }

    const base64 = Buffer.from(roh).toString('base64');
    return new Response(JSON.stringify({ image: `data:${typ};base64,${base64}` }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        // Einen Tag im Zwischenspeicher: dasselbe Foto wird bei jedem
        // Schwung erneut gebraucht, muss aber nicht erneut geholt werden.
        'Cache-Control': 'public, max-age=86400',
      },
    });
  } catch (e) {
    const grund = e?.name === 'TimeoutError'
      ? 'Das Bild hat zu lange gebraucht'
      : (e?.message || 'Bild nicht erreichbar');
    return new Response(JSON.stringify({ error: grund }), { status: 502 });
  }
};
