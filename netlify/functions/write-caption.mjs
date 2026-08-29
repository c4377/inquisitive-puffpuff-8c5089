// Der Prompt kommt woertlich von Carina. Was hier steht, ist ihre
// Fassung — nicht meine Zusammenfassung davon.

const USER_KONTEXT = `Business Mentorin, Angebot vierstellig verkaufen, THE STRATEGY (33€ Beta / 88€), THE MONEY ROOM (97€/Monat, 3 Monate Minimum), 1:1 (8 Plätze, kein Kaufknopf)`;

const CTAS = {
  1: {
    name: 'STRATEGY',
    satz: 'Schreib mir STRATEGY. 13 Voice Notes, 33€ im Beta. Danach 88€. Für dich, wenn du umsetzt, diese Woche.',
  },
  2: {
    name: 'MOVE',
    satz: 'Kommentiere MOVE. THE MONEY ROOM. 97€ im Monat, 3 Monate Minimum. Du bringst mit, was auf dem Tisch liegt, du gehst mit einem Move raus.',
  },
  3: {
    name: 'SPEICHERN',
    satz: 'Speicher dir diesen Beitrag. Morgen fangen wir an, und ich zähl mit.',
  },
  4: {
    name: '1:1',
    satz: 'Acht Plätze, kein Kaufknopf: du sagst mir, welcher Weg, und ich melde mich innerhalb von zwei Tagen.',
  },
};

const ANWEISUNG = (postContent, ctaText) => `Du bist der Caption-Schreiber für CARINA | ANNA | PRAV.

VOICE DNA - SO SCHREIBT SIE:
- Kein Motivations-Geschwurbel. Kein "du bist genug". Trocken, direkt, logisch.
- Struktur: Immer "Das Offensichtliche:" als Anker. Dann was wirklich Sache ist.
- Sätze: Kurz. Kein Adjektiv-Bingo. Verben statt Adjektive.
- Kein Storytelling um des Storytellings willen. Jede Slide hat einen Job.
- Humor: Trocken, fast beiläufig. "Überraschung: Es lag nicht an deinen Sternzeichen."
- Haltung: Reihenfolge > Reichweite. Angebot > Branding. Wiederholung > neue Ideen.
- Typische Formulierungen: "Das Offensichtliche:", "Nicht, weil du nichts kannst, sondern weil...", "Zehn Minuten.", "Speicher dir diesen Beitrag.", "Schreib mir, was dich davon abhält."
- Emojis: Gar keine oder maximal 1. Keine Hashtag-Flut.

DEINE AUFGABE:
Du bekommst 3 Inputs:
1. POST_CONTENT: ${postContent} - das ist der Rohtext der Slides / Reel-Transkript
2. USER_KONTEXT: ${USER_KONTEXT} - immer: Business Mentorin, Angebot vierstellig verkaufen, THE STRATEGY (33€ Beta / 88€), THE MONEY ROOM (97€/Monat, 3 Monate Minimum), 1:1 (8 Plätze, kein Kaufknopf)
3. CTA: ${ctaText} - z.B. STRATEGY / MOVE / ACADEMY / Speicher dir / Schreib mir

REGELN FÜR DIE CAPTION:

1. Starte NIEMALS mit einer Zusammenfassung der Slides. Starte mit dem Problem aus dem Post.
2. Aufbau:
   Zeile 1-2: Hook (Provokant, aus dem Post)
   Leerzeile
   Das Offensichtliche: [2-3 Sätze was wirklich passiert]
   Leerzeile
   Was es stattdessen braucht / Was wir machen (aus den Slides)
   Leerzeile
   Konkrete Aufgabe: "Nimm dir zehn Minuten..." / "Geh deine letzten 10 Beiträge durch..."
   Leerzeile
   CTA - exakt wie in ${ctaText} vorgegeben, natürlich eingebaut.

3. Länge: 110-170 Wörter. Kein Roman.
4. Beziehe dich immer auf den Post und auf dich (deine Erfahrung: tausende Cold Calls, früheres Leben, eigene Fehler).
5. Ende: CTA als einzelner Satz. Kein "Link in Bio" wenn CTA "Schreib mir STRATEGY" ist.

Gib NUR die fertige Caption aus.`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let day = null, cta = 2;
  try {
    const body = await req.json();
    day = body.day || null;
    cta = [1, 2, 3, 4].includes(Number(body.cta)) ? Number(body.cta) : 2;
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!day) return new Response(JSON.stringify({ error: 'day fehlt' }), { status: 400 });

  const folien = (day.slides || []).filter(Boolean).slice(0, 20)
    .map((t, i) => `${i + 1}. ${String(t).replace(/\u00A0/g, ' ')}`).join('\n');

  const prompt = ANWEISUNG(folien, CTAS[cta].satz);

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
            generationConfig: { temperature: 0.95 },
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

    // Die Anweisung sagt "Gib NUR die fertige Caption aus" — also kommt
    // reiner Text zurueck. Codezaeune abschneiden, falls das Modell doch
    // welche setzt, sonst nichts anfassen.
    const roh = (data?.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('');
    const caption = roh.replace(/^\s*```[a-z]*\s*/i, '').replace(/```\s*$/, '').trim();
    if (!caption) {
      return new Response(JSON.stringify({ error: 'Keine Caption erhalten. Nochmal versuchen.' }), { status: 502 });
    }
    return new Response(JSON.stringify({ caption, laenge: caption.length }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
