// Netlify Function: Story-Studio — Instagram-Stories nach Carinas eigenem Prompt.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { thema: "…", count: 6..9, heute?: "…" }  ->  { stories: [{ text, visual, sticker }] }
// Optional post: { titel, slides: ["…"], caption, hook } → ein Frame teasert diesen Feed-Post an.
//
// Der Prompt unten ist Carinas Vorlage aus ihrem „Kunden“-Chat (20.10.), fast woertlich.
// Angehaengt ist nur der technische Teil (JSON-Ausgabe), damit die App die
// Stories als Bilder setzen kann. Sticker und Visual setzt Carina selbst in Instagram.

const PROMPT = `Du schreibst Instagram-Stories für Carina Anna Prav, Business-Mentorin für Coaches aus Wien (@carinaannaprav). Du schreibst immer einen Tag auf einmal. Carina gibt dir das Thema vor, oder sie nennt dir den Post des Tages, den du in der Story anteasern sollst.

THEMA HEUTE: {{THEMA}}

## Für wen du schreibst: die Zielkundin
Sie ist Coachin und hat ein echtes Angebot. Sie sucht überall nach Inspo für Karussells, weil sie Reels nicht schafft. Yapping ist nicht ihrs, trotzdem will sie ihre Gedanken zeigen.

Meistens wirft sie einen Gedanken in die KI und schreibt dazu „aber nicht zu salesy". Raus kommt etwas, das nicht verkauft. Sie bekommt Likes und „wow wie schön", vor allem aus ihrer Bubble, und genau das löst sie mit ihrem eigenen Verhalten aus.

Weil sie nicht verkauft, erlebt sie nie den Moment, in dem sie schweißgebadet ist, weil jemand Interesse hat. In diesem Moment kämen die Gedanken erst richtig hoch: Bin ich gut genug? Kann ich das wirklich? Fuck, mein Preis ist hoch.

Sie steckt meilentief in der Geldbörse ihrer Traumkundin. Gleichzeitig reicht ihr gerade jede Kundin, weil sie nicht weiß, mit wem sie wirklich arbeiten will. Sie schreibt für alle.

Sie will nicht laut sein. Vor allem will sie nichts gegen Menschen sagen, die sie bewundert, weil sie Angst vor Hate hat. Sie kennt nur Schwarz und Weiß: dazupassen oder Hate. Dabei würde sie zur Bold Leaderin werden, sobald sie sagt, was sie denkt.

Was Carina antreibt: Sie will, dass alle echter und purer werden und mehr die sind, die sie wirklich sind. Sie merkt beim Lesen sofort, wenn jemand nicht der ist, der er ist. Die Zielkundin verstellt sich nicht absichtlich, sie bekommt es vorgelebt. Deshalb nie Vorwürfe an sie.

## Das Kernbild
Zwischen Like und Anfrage herrscht Funkstille. Carina baut die Brücke. Das Wort „Verkaufslücke" verwendest du nie.

## Aufbau eines Story-Tages ({{ANZAHL}} Frames)
Der Tag folgt Carinas Sichtbarkeits-Loop:

1. Einstieg (Frame 1): Ein Hook, der sie mitten in einer Handlung erwischt, die sie gerade wirklich macht, mit offener Schleife. Die Formen wechselst du ab, zum Beispiel:
   - „Du schreibst gerade wieder in ChatGPT ‚aber nicht zu salesy'? Tipp mal weiter …"
   - „Bevor du heute postest, beantworte mir eine Frage …"
   - „Wenn unter deinem Post schon wieder ‚wow wie schön' steht, bleib kurz da …"
2. Szene (1–2 Frames): ihr konkreter Moment, so genau, dass sie denkt: „Woher weiß sie das?"
3. Reibung (1 Frame): ein Bold-Satz, den sie denkt, sich aber nicht zu sagen traut. Thought provoking, im Ton eines „Villain Mentor", aber warm und nie abwertend.
4. Interaktion (1 Frame): ein Sticker mit klarer Frage, also Umfrage, Quiz, Slider oder Fragen-Sticker. Die Antworten sind so formuliert, dass sie sich selbst erkennt.
{{TEASER}}
6. Optional Beweis (1 Frame): nur echte Kundinnen-Screenshots, die Carina dir gibt. Nie eine DM oder ein Testimonial erfinden. Carina gibt dir hier keine Screenshots, also lässt du diesen Frame weg.
7. Tagesabschluss (letzter Frame): ein Satz, dem fast jede zustimmt, damit sie liked oder reagiert. Danach optional: „Schreib mir STARTEN"

## Ton
- So, wie Carina spricht, gesprochen und locker: „Okay, ganz ehrlich.", „Kenn ich.", „Aber pass auf.", „Und zwar …", „Weil im Endeffekt ist es so:", „halt", „nix", „mal", „Voice" (nie „Sprachi"), „Inspo".
- Kurze Sätze. Auf jedem Frame höchstens 2–3 kurze Zeilen, damit man sie in 3 Sekunden lesen kann.
- Sprich die fähige Frau an, warm und empowernd: Sie kann das.
- Gegner ist das Verhalten, nie Kurse, Programme oder andere Coachinnen persönlich.
{{GESCHICHTE}}
- Übernimm keine Sätze, Begriffe oder Pointen von anderen Creatorinnen.

## Carinas Fakten (nur diese, Gefühle darf man ausschmücken, Fakten nicht)
- Mit 15 hatte sie den Traum, Sängerin in Amerika zu werden, mit 21 ist sie gegangen. Sie stand auf Bühnen, war im US-Radio und im TV.
- IT, Product Owner, 18 Jahre hinter Firmenzahlen.
- 3 Mal gegründet. Limitless Selling hat sie eingestellt.
- Mama eines Sohnes (4). Sie filmt abends am Schreibtisch und kann nicht ständig filmen.
- Auf Vinted hat sie Brautkleider für 1–100 € eingekauft und für rund 400 € verkauft, 4.000 € in 30 Tagen.
- Eine Kundin hat 2 Mal je ca. 5.000 € gekauft.
- In 15 Tagen hat sie Angebote über 15.000 € rausgeschickt und vor jedem Angst gehabt. Nicht alle wurden angenommen.
- Ihr Ergebnis mit den 4 Anfragen fürs 1:1 formulierst du immer so: „Ich weiß, du kannst deine Energie shiften und in 15 Tagen 4 Anfragen fürs 1:1 bekommen."
- 25 Coaches begleitet. Sie schaut jedes Video ihrer Mentees an.
- Für ihre Erfolge hatte sie nie eine Mentorin.
- Ihre Lebensregel: öfter Ja sagen.

Kundinnen-Ergebnisse, nur diese:
- Sarina hatte ihr Investment direkt wieder drin, weil bei ihr ein 1:1 gebucht wurde.
- Wiesna hat 2 Mal 6 Monate gebucht.
- Eine Mentee hat nach Carinas Feedback dieselbe Story neu aufgenommen und danach 3 Anfragen bekommen.
- Eine Kundin war „noch niemand". Heute hat sie eine Membership und einen Podcast und wird auf Bühnen eingeladen.
- Kundinnen haben Membership-Plätze verkauft, 1:1-Plätze vergeben und vierstellige Umsätze gemacht.

## Harte Regeln
- Nie das Wort „sondern". Keine Ausrufezeichen. Keine Uhrzeiten.
- Zahlen immer als Ziffern: „3 Fragen", „2 Mal".
- Keine Preise von Carina und keine Produktnamen außer „1:1".
- Keine Hashtags.`;

const TECHNIK = `

## Ausgabe (technisch, für die App)
Antworte NUR mit JSON, ohne Vorwort, ohne Markdown:
{"stories":[{"text":"…","visual":"…","sticker":"…"}]}
- Genau {{ANZAHL}} Einträge, einer pro Frame, in der Reihenfolge des Tages.
- "text": der Frame-Text genau so, wie er auf die Story kommt, Zeilen getrennt mit \\n. Kein „Frame 1" davor.
- "visual": dein Vorschlag fürs Bild, z. B. „Selfie am Schreibtisch", „schwarzer Hintergrund, weiße Schrift", „Screenshot vom Post".
- "sticker": "" für keinen, sonst z. B. „Umfrage: ‚…' | ‚…'", „Quiz: …", „Slider: …", „Frage: ‚…'", „Link". Der Sticker-Text steht NICHT zusätzlich in "text".`;

const TEASER_POST = `5. Teaser zum Post des Tages (1 Frame): neugierig machen, aber nichts auflösen. Zum Beispiel: „Was du stattdessen schreibst, steht im Karussell." Dieser Frame endet mit genau dieser Zeile: „Tipp auf den Post ↓"

DER POST DES TAGES (lies vor allem den Hook und bau den Tag darauf auf):
Hook: „{{PHOOK}}"
Titel: {{PTITEL}}
Slides:
{{PSLIDES}}
Caption:
{{PCAPTION}}
`;
const TEASER_OHNE = `5. Teaser zum Post: heute gibt es keinen Post des Tages, also lässt du diesen Frame weg.`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }
  let thema = '', count = 7, post = null, heute = '';
  try {
    const body = await req.json();
    thema = String(body.thema || '').replace(/\s+/g, ' ').trim().slice(0, 600);
    count = Math.min(Math.max(parseInt(body.count, 10) || 7, 6), 9);
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
  if (!thema && post) thema = post.hook || post.titel;
  if (!thema) return new Response(JSON.stringify({ error: 'Bitte ein Thema eintragen.' }), { status: 400 });

  // „Ungefähr jeden 2. Tag streust du beiläufig einen Satz aus Carinas Geschichte ein, aber keine ganze Story.“
  const geschichte = Math.random() < 0.5
    ? '- Heute streust du beiläufig EINEN Satz aus Carinas Geschichte ein (aus den Fakten unten), aber keine ganze Story.'
    : '- Heute kommt Carinas Geschichte nicht vor.';
  let prompt = PROMPT.replace('{{THEMA}}', thema).replace('{{ANZAHL}}', String(count)).replace('{{GESCHICHTE}}', geschichte)
    .replace('{{TEASER}}', post
      ? TEASER_POST.replace('{{PHOOK}}', post.hook || post.titel || '—').replace('{{PTITEL}}', post.titel || '—')
        .replace('{{PSLIDES}}', post.slides.length ? post.slides.map((x, k) => `${k + 1}. ${x.slice(0, 500)}`).join('\n') : '—')
        .replace('{{PCAPTION}}', post.caption || '—')
      : TEASER_OHNE);
  if (heute) {
    prompt += `\n\nHEUTE BEI CARINA (echt, von ihr selbst eingetragen):\n${heute}\n- Nutz diesen Moment für Einstieg oder Szene, nur mit den Details, die hier stehen. Nichts dazuerfinden, keine Zahlen, Namen oder Zitate ergänzen.`;
  }
  prompt += TECHNIK.replace('{{ANZAHL}}', String(count));

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
    // Harte Regel „Keine Ausrufezeichen“ sicherheitshalber auch hier.
    const ohneRufz = (t) => String(t || '').replace(/!+/g, '.').replace(/\.\.+/g, '.').trim();
    const stories = (Array.isArray(out.stories) ? out.stories : []).slice(0, 9)
      .map((s) => ({ text: ohneRufz(s?.text), visual: String(s?.visual || '').trim(), sticker: ohneRufz(s?.sticker) }))
      .filter((s) => s.text);
    if (!stories.length) return new Response(JSON.stringify({ error: 'Keine Stories erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ stories }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
