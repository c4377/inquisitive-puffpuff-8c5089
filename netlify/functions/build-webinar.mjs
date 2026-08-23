// Netlify Function: aus einer Idee ein ganzes Webinar bauen.
// POST { idee, dauer } -> { webinar: {...} }  — Aufbau wie src/constants/webinar.js
// Schluessel bleibt serverseitig.

const STIMME = `
Du baust Webinare für Carina (carinaannaprav.at).
Sie bringt Coaches und Unternehmerinnen zum ersten vierstelligen Verkauf —
ohne Preisleiter.

DAS ANGEBOT IST DAS MENTORING UND DIE 1:1-BEGLEITUNG.
Der letzte Abschnitt lädt IMMER dorthin ein, über DM, nicht über einen Link.
Kein Angebotscheck als Einladung. Kein Countdown, kein Rabatt.

SPRACHE
- Kurze Sätze. Gesprochen, nicht geschrieben.
- Deutsch mit eingestreutem Englisch (Offer, Sales, Clients).
- Sammelanrede. Keine Belehrung, kein Werbeton.
- Konkret statt allgemein: Zahlen, Sätze, Beispiele — keine Prinzipien.

HALTUNG
- Nicht gegen Mindset-Arbeit. Die Arbeit liegt DAVOR, am Angebot.
- Die Preisleiter ist die Falle, nicht die Lösung.
- Keine 20k/30k-Monate. Es geht um die ERSTEN Kundinnen.
- Sie bewertet nicht die Zahlungsfähigkeit von Kundinnen.
- Beweis statt Eigenlob. Weniger erklären, mehr zeigen.
- Der Einstieg ist eine Geschichte, keine Vorstellungsrunde.

AUFBAU
6 Abschnitte über die angegebene Dauer, mit Minutenangaben.
Der Bogen: Einstieg → das eigentliche Problem → die Unterscheidung, auf die
alles hinausläuft → was konkret zu tun ist → wie es in der Praxis klingt →
Einladung ins Mentoring.

ARBEITSBLÄTTER
3 Stück, die IM Webinar ausgefüllt werden. Jedes mit 2 Teilen und je 3–7
Fragen. Fragen sind entscheidbar oder in einem Satz beantwortbar — keine
Reflexionsaufsätze. Mindestens eines soll eine Diagnose ermöglichen
(zwei Spalten, am Ende weiß man, welcher Fall vorliegt).
`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let idee = '', dauer = '60 Minuten';
  try {
    const body = await req.json();
    idee = String(body.idee || '').trim().slice(0, 4000);
    if (body.dauer) dauer = String(body.dauer).slice(0, 40);
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!idee) return new Response(JSON.stringify({ error: 'Keine Idee angegeben.' }), { status: 400 });

  const prompt = `${STIMME}

DIE IDEE FÜR DIESES WEBINAR
${idee}

Dauer: ${dauer}

Bau daraus ein vollständiges Webinar. Nimm die Idee ernst und dreh sie weiter —
gib nicht bloß wieder, was dasteht.

ANTWORTE NUR MIT JSON, ohne Vorwort, ohne Markdown:
{
 "titel": "…",
 "untertitel": "…",
 "dauer": "${dauer}",
 "versprechen": "Was weiß oder kann sie am Ende? Zwei Sätze.",
 "abschnitte": [
   {"id":"kurz-klein","minute":"0–5","titel":"…","ziel":"…",
    "beats":["gesprochener Satz","…"],
    "hinweis":"Regieanweisung für dich",
    "worksheet":"id eines Arbeitsblatts oder weglassen"}
 ],
 "worksheets": [
   {"id":"kurz-klein","titel":"…","zweck":"…","anleitung":"…",
    "teile":[{"titel":"…","fragen":["…"]}]}
 ]
}
6 Abschnitte, je 3–6 beats. 3 Arbeitsblätter.
Die ids sind kleingeschrieben, ohne Leerzeichen und Umlaute.`;

  const MODELLE = ['gemini-3.6-flash', 'gemini-3-flash', 'gemini-flash-latest', 'gemini-2.5-flash'];

  try {
    let r = null, data = null, letzterFehler = '';
    for (const modell of MODELLE) {
      r = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { temperature: 0.9, responseMimeType: 'application/json' },
          }),
        }
      );
      data = await r.json();
      if (r.ok) break;
      letzterFehler = data?.error?.message || `HTTP ${r.status}`;
      const modellProblem = r.status === 404
        || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
      if (!modellProblem) break;
    }
    if (!r.ok) {
      return new Response(JSON.stringify({ error: letzterFehler || 'Gemini-Fehler' }), { status: 502 });
    }

    const roh = (data?.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('').trim();
    const sauber = roh.replace(/^```json\s*|```$/g, '').trim();
    let w;
    try {
      w = JSON.parse(sauber);
    } catch {
      const a = sauber.indexOf('{'), b = sauber.lastIndexOf('}');
      w = a >= 0 && b > a ? JSON.parse(sauber.slice(a, b + 1)) : null;
    }

    // Aufbau pruefen, damit die Ansicht nicht auf halbem Weg abstuerzt.
    const ok = w && Array.isArray(w.abschnitte) && w.abschnitte.length >= 3
      && Array.isArray(w.worksheets);
    if (!ok) {
      return new Response(JSON.stringify({ error: 'Unvollständige Antwort. Nochmal versuchen.' }), { status: 502 });
    }
    w.abschnitte = w.abschnitte.map((a, i) => ({
      id: a.id || `abschnitt-${i + 1}`,
      minute: a.minute || '',
      titel: a.titel || `Abschnitt ${i + 1}`,
      ziel: a.ziel || '',
      beats: Array.isArray(a.beats) ? a.beats.filter(Boolean) : [],
      hinweis: a.hinweis || '',
      worksheet: a.worksheet || undefined,
    }));
    w.worksheets = w.worksheets.map((ws, i) => ({
      id: ws.id || `blatt-${i + 1}`,
      titel: ws.titel || `Arbeitsblatt ${i + 1}`,
      zweck: ws.zweck || '',
      anleitung: ws.anleitung || '',
      teile: (Array.isArray(ws.teile) ? ws.teile : []).map((t, k) => ({
        titel: t.titel || `Teil ${k + 1}`,
        fragen: Array.isArray(t.fragen) ? t.fragen.filter(Boolean) : [],
      })),
    }));

    return new Response(JSON.stringify({ webinar: w }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
