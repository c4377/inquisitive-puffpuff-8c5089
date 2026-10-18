// Netlify Function: Story-Studio — Instagram-Stories nach Carinas eigenem Prompt.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { thema: "…", count: 5..7 }  ->  { stories: [{ text, sticker }] }
// Optional post: { titel, slides: ["…"], caption } → die Stories führen zu diesem Feed-Post hin.
//
// Der Prompt unten ist Carinas Vorlage, woertlich. Geaendert wird er NUR hier.
// Angehaengt ist nur der technische Teil (JSON-Ausgabe), damit die App die
// Stories als Bilder setzen kann.

const PROMPT = `Du schreibst Instagram-Stories für mich, Carina Anna Prav (@carinaannaprav), Business-Mentorin für Coaches. Ich schreibe Coaches Content und Angebote, die verkaufen (Done-for-you). Meine Community sind die „Ja-Sagerinnen": Frauen, die Opportunities sehen, sich weiterbilden, Zeit, Geld und Schweiß in ihren Traum stecken und Ja zu sich sagen.

THEMA HEUTE: {{THEMA}}

FORMAT (jede Story ist gleich aufgebaut, wie ein ruhiges Gespräch unter vier Augen)
- {{ANZAHL}} Stories.
- Story 1 beginnt mit genau diesem Label in einer eigenen Zeile: REAL TALK
  Darunter als großer Satz eine sehr ehrliche Frage, Feststellung oder Meinung, die sie trifft, weil sie stimmt. Kein Weichzeichnen, keine Floskel.
  Kein anderes Label (nicht UNTER UNS, LET'S TALK, KURZ GESAGT usw.).
- Alle anderen Stories haben KEIN Label.
- Jede Story hat den großen Satz: eine klare Aussage von mir als Leaderin, eine ehrliche Feststellung oder eine Frage, die sitzt. Höchstens 25 Wörter, keine Aufzählung.
- KEINE Anführungszeichen um den großen Satz oder den Absatz. „…" nur, wenn wirklich jemand einen Satz wörtlich sagt, und das höchstens einmal in der ganzen Serie.
- Darunter der kleine Absatz, 2–3 ruhige Sätze, höchstens 40 Wörter. Er ordnet ein, bezieht Position oder gibt die Richtung vor.
- Keine erfundenen Situationen aus meinem Alltag (kein „in meinem Call gesagt", kein „eine Kundin hat mir geschrieben"), außer es steht unten bei MEINE GESCHICHTE oder HEUTE BEI MIR. Stattdessen: „Hört man oft", „Sagen viele", „Kennst du den Satz?".
- Ausgabe nur die Texte: „Story 1", „Story 2" … ohne Erklärungen.
- Keine Umfrage-, Quiz- oder Fragesticker vorschlagen. Die Stories stehen für sich.

STIMME
- Kurze, einfache Sätze, aber fließend verbunden („das heißt", „und zwar", „im Endeffekt", „weil", „also"). Keine abgehackten Fragmente.
- Wie ich rede: direkt, warm, ein bisschen rebellisch, große Schwester.
- LEADERIN-TON: Ich führe. Ich sage, was ich denke, und stehe dazu: klare Meinung, klare Richtung, keine Absicherungen („vielleicht", „ein bisschen", „man könnte"), kein Weichspülen, keine Entschuldigungen. Ruhig und souverän statt laut. Ich weiß, wovon ich rede, und muss es nicht beweisen. Denglisch erlaubt (Opportunities, level up, FREAKIN), CAPS für den einen Peak, sparsam Emojis 🔥😉.
- Roter Faden von der ersten bis zur letzten Story, ein wiederkehrender Anker (z. B. „sagt Ja zu sich").
- An EINE Frau schreiben, nicht an ein Publikum. Die fähige Frau ansprechen, nicht die festgefahrene.
- Kalter Einstieg, Story 1 ist Hook. Kein „hier ist die Sache", kein „es ist nicht X, es ist Y".
- Den konkreten Moment beschreiben statt des Gefühls. Lang aufbauen, kurz zuschlagen. Eine screenshot-würdige Zeile.
- Echte Zahlen oder gar keine. Nichts erfinden, keine erfundenen Kundinnen-DMs.
- Kurse und Programme nie als Gegner. Gegner ist das Verhalten: warten aufs Bereitsein, Wissen sammeln ohne Umsetzen, rabattieren, allein rumprobieren.

GEFÜHLE, DIE SIE BEIM LESEN HABEN SOLL
- „Sie kennt meine Wünsche."
- „Sie hält mich nicht für zu viel."
- „Sie hat selbst Scheiße durchlebt."
- „Sie hat ein Kind."
- „Sie judgt nichts, außer wenn ich's nicht umsetze."
Diese Gefühle entstehen über Haltung, Ton und wie genau ich ihre Situation beschreibe, NICHT dadurch, dass ich meine Biografie erzähle.

MEINE GESCHICHTE
{{GESCHICHTE}}

AUSSCHLUSS (wenn passend, vor dem Hauptteil)
Wer nicht passt, wird freundlich, aber klar rausgeschickt, rein über Haltung: wer wartet, bis sie „bereit" ist, wer rabattiert, wer nie umsetzt.

SCHLUSS
Die letzte Zeile vor der CTA ist der schärfste Punkt, keine Zusammenfassung. Dann:
„Schreib mir STARTEN ↓"
Nenne nur Angebote, die es wirklich gibt (Das Intensive, Das 1:1, Done-for-you Content, Offer Incubator).

Bevor du lieferst: Frag dich, was es noch ehrlicher und mutiger machen würde, und schreib es so.`;

const TECHNIK = `

TECHNISCHE AUSGABE (nur für die App, ändert nichts am Inhalt oben):
Antworte NUR mit JSON, ohne Vorwort, ohne Markdown:
{"stories":[{"text":"…","sticker":""}]}
- "text": der Story-Text genau so, wie er auf die Story kommt: großer Satz\\nkleiner Absatz,
  bei Story 1 davor noch LABEL\\n. Kein „Story 1" davor.
- "sticker": immer "".
  Der Sticker-Text steht NICHT zusätzlich in "text".
- Die CTA „Schreib mir STARTEN ↓" steht als letzte Zeile im "text" der letzten Story.`;

const ZUM_POST = `

STORIES ZUM POST (für diese Serie gilt zusätzlich):
Diese Stories führen zu meinem neuen Feed-Post hin. Der Post ist das Ende der Serie.

DER HOOK DES POSTS (das Wichtigste, lies ihn zuerst und bau alles darauf auf):
„{{PHOOK}}"

AUFBAU ALS BRÜCKE:
1. Steht unten HEUTE BEI MIR, startet Story 1 genau bei diesem echten Moment von heute und die Brücke geht von dort aus. Sonst startet Story 1 bei einem Alltagsgedanken, den sie heute selbst haben könnte: beim Kaffee, beim Scrollen, kurz bevor sie postet, beim Angebot-Überarbeiten, abends nach einem Kundinnen-Call. Als Gedanke oder Frage, die sie kennt, NICHT als erfundenes Erlebnis von mir.
2. Die nächsten Stories bauen die Brücke von diesem Alltagsgedanken zum Hook: denselben Gedanken zu Ende denken, bis der Hook fast ausgesprochen ist. Den Hook nicht wortgleich verraten und die Lösung aus dem Post NICHT vorwegnehmen.
3. Eine Story vor der letzten baut die Brücke zu dem EINEN Angebot von mir, das am besten zum Hook passt (nur: Das Intensive, Das 1:1, Done-for-you Content, Offer Incubator). In ein, zwei Sätzen, als logische Folge des Gedankens, ohne Druck, ohne „STARTEN".
4. Die letzte Story kündigt den Post an und schickt sie hin. Sie endet mit genau dieser Zeile: „Neuer Post ↓"
- STARTEN kommt in dieser Serie nicht vor.

DER POST:
Titel: {{PTITEL}}
Slides:
{{PSLIDES}}
Caption:
{{PCAPTION}}`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }
  let thema = '', count = 6, post = null, heute = '';
  try {
    const body = await req.json();
    thema = String(body.thema || '').replace(/\s+/g, ' ').trim().slice(0, 600);
    count = Math.min(Math.max(parseInt(body.count, 10) || 6, 5), 7);
    heute = String(body.heute || '').replace(/\s+/g, ' ').trim().slice(0, 1200);
    if (body.post && typeof body.post === 'object') {
      const sl = (Array.isArray(body.post.slides) ? body.post.slides : []).map((x) => String(x || '').trim()).filter(Boolean).slice(0, 12);
      post = { titel: String(body.post.titel || '').trim().slice(0, 200), slides: sl, caption: String(body.post.caption || '').trim().slice(0, 3000), hook: String(body.post.hook || '').replace(/\s+/g, ' ').trim().slice(0, 300) };
      if (!post.hook && sl.length) post.hook = sl[0].replace(/^\s*\[[^\]\n]{1,24}\]\s*/, '').split(/\s&\s/)[0].replace(/\*+|__/g, '').replace(/\s+/g, ' ').trim().slice(0, 300);
      if (!post.slides.length && !post.caption) post = null;
    }
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!thema) return new Response(JSON.stringify({ error: 'Bitte ein Thema eintragen.' }), { status: 400 });

  // Meine Geschichte nur sparsam (Carina: „immer nur so 10 %", „als Text, nicht premade"):
  // Bei etwa der Hälfte der Serien gar nicht, sonst EIN Element, zufällig gewählt, in 1–2 Sätzen erzählt.
  const MATERIAL = [
    'Mit 15 der Traum, als Sängerin nach Amerika zu gehen, mit 21 dort. Bühnen-, US-Radio- und TV-Erfahrung.',
    '18 Jahre in Businesses jeder Größe, vom Millionenprojekt bis zum kleinen Business Case.',
    'Zweimal im Business ohne Mentoring gestanden, als Kind keine Mentorin gehabt, Mentoren immer selbst gesucht.',
    'Mama mit Job und Business, Videos entstehen auch mal am Abend.',
    'Hands-on: Ich schau jedes Video meiner Mentees an und sag die Lücke sofort.',
    'Kundinnen: Membership-Plätze verkauft, 1:1-Plätze vergeben, vierstellige Umsätze generiert.',
  ];
  const geschichte = Math.random() < 0.5
    ? '- In DIESER Serie kommt meine Biografie NICHT vor. Keine Erwähnung von Amerika, Singen, meinen Jahren im Business, meinem Kind oder meinen Kundinnen-Ergebnissen. Die Serie lebt nur vom Thema und von ihr.'
    : `- In dieser Serie darf höchstens dieses EINE Element vorkommen, und nur wenn es das Thema wirklich stützt (sonst weglassen):\n  ${MATERIAL[Math.floor(Math.random() * MATERIAL.length)]}\n- Höchstens 1–2 Sätze in der ganzen Serie, das sind etwa 10 % des Texts. Der Rest gehört ihr und dem Thema.\n- Nicht als fertigen Satz übernehmen und nicht aufzählen. Erzähl es als kleinen, konkreten Moment in meinen eigenen Worten, eingewoben in den Gedankengang, so als würde es mir gerade beim Reden einfallen.`;
  let prompt = PROMPT.replace('{{THEMA}}', thema).replace('{{ANZAHL}}', String(count)).replace('{{GESCHICHTE}}', geschichte);
  if (post) {
    prompt += ZUM_POST.replace('{{PHOOK}}', post.hook || post.titel || '—').replace('{{PTITEL}}', post.titel || '—')
      .replace('{{PSLIDES}}', post.slides.length ? post.slides.map((x, k) => `${k + 1}. ${x.slice(0, 500)}`).join('\n') : '—')
      .replace('{{PCAPTION}}', post.caption || '—');
  }
  if (heute) {
    prompt += `\n\nHEUTE BEI MIR (echt, von mir selbst eingetragen):\n${heute}\n- Erzähl diesen Moment in meinen Worten, nur mit den Details, die hier stehen. Nichts dazuerfinden, keine Zahlen, Namen oder Zitate ergänzen.\n- ${post ? 'Von diesem Moment aus baust du die Brücke zur Hook des Posts.' : 'Von diesem Moment aus baust du die Brücke zum Thema.'}`;
  }
  prompt += post ? TECHNIK.replace('Die CTA „Schreib mir STARTEN ↓" steht als letzte Zeile im "text" der letzten Story.', 'Die Zeile „Neuer Post ↓" steht als letzte Zeile im "text" der letzten Story.') : TECHNIK;

  // Wie in write-stories: Modelle der Reihe nach, falls Google eines umbenennt.
  const MODELLE = ['gemini-3.6-flash', 'gemini-3-flash', 'gemini-flash-latest', 'gemini-2.5-flash'];
  try {
    let data = null, r = null, letzterFehler = '';
    for (const modell of MODELLE) {
      r = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { temperature: 0.95, responseMimeType: 'application/json' },
          }),
        }
      );
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
      out = a >= 0 && b > a ? JSON.parse(sauber.slice(a, b + 1)) : { stories: [] };
    }
    const stories = (Array.isArray(out.stories) ? out.stories : []).slice(0, 7)
      .map((s) => ({ text: String(s?.text || '').trim(), sticker: '' }))
      .filter((s) => s.text);
    if (!stories.length) return new Response(JSON.stringify({ error: 'Keine Stories erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ stories }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
