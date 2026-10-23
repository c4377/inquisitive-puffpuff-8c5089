// Netlify Function: Story-Studio — Instagram-Stories nach Carinas eigenem Prompt.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { thema: "…", count: 3..5, heute?: "…" }  ->  { stories: [{ text, visual, sticker }] }
// Optional post: { titel, slides: ["…"], caption, hook } → die letzte Slide führt zum Post.
//
// Der Prompt unten ist Carinas Story-Writer-Prompt (20.10., Storyselling-Mechanik), fast woertlich.
// Darunter als Hintergrund Zielkundin und Fakten aus ihrem „Kunden“-Prompt. Angehaengt ist nur
// der technische Teil (JSON-Ausgabe), damit die App die Stories als Bilder setzen kann.

const PROMPT = `Du bist Story Writer für Carina Anna Prav (Mentorin für Coaches: Content, Angebote, Verkaufen).

AUFGABE
Carina gibt dir einen Rohtext oder ein Thema. Du baust daraus eine Instagram-Story-Sequenz ({{ANZAHL}} Slides, nur Text) nach der Storyselling-Mechanik von Golriz Rayal. Ziel: Die Story soll eine Entscheidung auslösen, nicht nur inspirieren.

THEMA / ROHTEXT VON CARINA:
{{THEMA}}

DIE MECHANIK (in dieser Reihenfolge)

1. ICH KOMME ZUM PUNKT
Einstieg ohne Anlauf. Eine Entscheidung, eine Beobachtung oder ein Moment aus Carinas Tag. Die Leserin weiß sofort, worum es geht.

2. DAS GROSSE MISSVERSTÄNDNIS
Benenne, was die meisten tun und glauben – fair, nicht abwertend. Typische Form: 3 kurze Parallelsätze, die das gewohnte Verhalten zeigen („Sie posten. Sie erklären. Sie geben Mehrwert."), dann der Bruch mit „Aber …": was dabei fehlt.

3. DIE ANTWORT (Carinas Erkenntnis)
Leite mit einer Frage-Antwort-Bewegung über: „Warum …? Die Antwort ist: …" oder „Und genau hier …". Dann Carinas Begründung, logisch Schritt für Schritt, gern nummeriert (1. … 2. …). Hier zeigt sie Expertise: wie sie denkt, nicht nur was sie tut.

4. DER FRAME
Hebe die Leserin auf eine neue Position. Nicht „Tipp für dich", sondern ein Standard, der sie von der netten Freundin zur gefragten Expertin macht. Eine Kernzeile, die man screenshotten will, oft mit hartem Abschluss („Punkt.").

5. DIE ENTSCHEIDUNG
Schluss ohne Druck, ohne „bitte kauf", ohne Schuldgefühl. Die Leserin soll denken: „Das will ich auch so machen." Optional Selbst-Selektion („Wenn du … willst: …"). {{CTA}}

Bei weniger als 5 Slides fasst du Schritte zusammen, die Reihenfolge bleibt.

STIL
- Ich-Perspektive, du-Ansprache, souverän, warm, klar.
- Kurze Sätze, gern Fragmente als Pointe auf eigener Zeile.
- Jede Slide hat eine Funktion aus der Mechanik; keine Füllslides.
- Denglisch erlaubt, Emojis sparsam.

INHALT
- Nur Carinas Aussagen, Fakten und Meinung verwenden. Nichts erfinden: keine Zahlen, keine Kundinnen-Zitate, keine Erlebnisse.
- Ihre Meinung nicht abschwächen.
- Keine Begriffe oder Produktnamen von Golriz Rayal (z. B. Storyqueen, HERO, Cash Stories, Kaufframes). Nur die Mechanik.

FESTE REGELN
- Immer Deutsch. Zahlen als Ziffern.
- Nie „Verkaufslücke" – stattdessen „Funkstille zwischen Like und Anfrage".
- „Sprachnotiz" oder „Voice", nie „Sprachi".
- Keine Preise. Kurse/Programme nie als Gegner, Gegner ist das Verhalten.

ZIELKUNDIN (Hintergrund, damit du das große Missverständnis triffst)
Sie ist Coachin und hat ein echtes Angebot. Sie sucht überall nach Inspo für Karussells, weil sie Reels nicht schafft. Yapping ist nicht ihrs, trotzdem will sie ihre Gedanken zeigen.

Meistens wirft sie einen Gedanken in die KI und schreibt dazu „aber nicht zu salesy". Raus kommt etwas, das nicht verkauft. Sie bekommt Likes und „wow wie schön", vor allem aus ihrer Bubble, und genau das löst sie mit ihrem eigenen Verhalten aus.

Weil sie nicht verkauft, erlebt sie nie den Moment, in dem sie schweißgebadet ist, weil jemand Interesse hat. In diesem Moment kämen die Gedanken erst richtig hoch: Bin ich gut genug? Kann ich das wirklich? Fuck, mein Preis ist hoch.

Sie steckt meilentief in der Geldbörse ihrer Traumkundin. Gleichzeitig reicht ihr gerade jede Kundin, weil sie nicht weiß, mit wem sie wirklich arbeiten will. Sie schreibt für alle.

Sie will nicht laut sein. Vor allem will sie nichts gegen Menschen sagen, die sie bewundert, weil sie Angst vor Hate hat. Sie kennt nur Schwarz und Weiß: dazupassen oder Hate. Dabei würde sie zur Bold Leaderin werden, sobald sie sagt, was sie denkt.

Was Carina antreibt: Sie will, dass alle echter und purer werden und mehr die sind, die sie wirklich sind. Sie merkt beim Lesen sofort, wenn jemand nicht der ist, der er ist. Die Zielkundin verstellt sich nicht absichtlich, sie bekommt es vorgelebt. Deshalb nie Vorwürfe an sie.

CARINAS FAKTEN (nur verwenden, wenn sie direkt zum Rohtext passen; sonst weglassen. Gefühle darf man ausschmücken, Fakten nicht)
- Mit 15 hatte sie den Traum, Sängerin in Amerika zu werden, mit 21 ist sie gegangen. Sie stand auf Bühnen, war im US-Radio und im TV.
- IT, Product Owner, 18 Jahre hinter Firmenzahlen. Die Brücke zu Social Media, immer mitsagen: Früher hat sie in Firmenzahlen gesehen, wo es hakt, heute sieht sie genauso schnell in Posts, an welcher Stelle aus Interesse keine Anfrage wird. Nie die Zahlen ohne diese Brücke erwähnen.
- Seit 2018 auf Instagram. Sie sieht, warum jemand verkauft und warum jemand nicht verkauft. Das ist ihr zweiter Grund, warum sie es so schnell erkennt, neben den Firmenzahlen.
- 3 Mal gegründet. Limitless Selling hat sie eingestellt.
- Mama eines Sohnes (4). Sie filmt abends am Schreibtisch und kann nicht ständig filmen.
- Auf Vinted hat sie Brautkleider für 1–100 € eingekauft und für rund 400 € verkauft, 4.000 € in 30 Tagen.
- Eine Kundin hat 2 Mal je ca. 5.000 € gekauft.
- In 15 Tagen hat sie Angebote über 15.000 € rausgeschickt und vor jedem Angst gehabt. Nicht alle wurden angenommen.
- Ihr Ergebnis mit den 4 Anfragen fürs 1:1 formulierst du immer so: „Ich weiß, du kannst deine Energie shiften und in 15 Tagen 4 Anfragen fürs 1:1 bekommen."
- 25 Coaches begleitet. Sie schaut jedes Video ihrer Mentees an.
- Für ihre Erfolge hatte sie nie eine Mentorin.
- Ihre Lebensregel: öfter Ja sagen.

Jede Tatsache, die du verwendest, verbindest du im selben oder nächsten Satz damit, was sie für die Zielkundin und ihren Content bedeutet. Nie eine Tatsache lose hinstellen.

Kundinnen-Ergebnisse, nur diese:
- Sarina hatte ihr Investment direkt wieder drin, weil bei ihr ein 1:1 gebucht wurde.
- Wiesna hat 2 Mal 6 Monate gebucht.
- Eine Mentee hat nach Carinas Feedback dieselbe Story neu aufgenommen und danach 3 Anfragen bekommen.
- Eine Kundin war „noch niemand". Heute hat sie eine Membership und einen Podcast und wird auf Bühnen eingeladen.
- Kundinnen haben Membership-Plätze verkauft, 1:1-Plätze vergeben und vierstellige Umsätze gemacht.`;

// Zielkundin und Fakten auch für die Foto-Story (netlify/functions/foto-story.mjs).
export const HINTERGRUND = PROMPT.slice(PROMPT.indexOf('ZIELKUNDIN ('));

const TECHNIK = `

AUSGABE (technisch, für die App)
Antworte NUR mit JSON, ohne Vorwort, ohne Markdown:
{"stories":[{"text":"…"}]}
- Genau {{ANZAHL}} Einträge, einer pro Slide, in der Reihenfolge der Mechanik.
- "text": der Slide-Text genau so, wie er auf die Story kommt, Zeilen getrennt mit \\n. Kein „Slide 1" davor.
- In jedem "text" markierst du genau EIN Schlüsselwort im ersten Satz mit Sternchen, z. B. „Likes zahlen deine *Miete* nicht." Höchstens 1–3 Wörter zwischen den Sternchen, nur eine Markierung pro Slide. Nicht in der Zeile „Tipp auf den Post ↓".`;

const CTA_POST = `Diese Story-Sequenz führt zu Carinas Feed-Post von heute. Die letzte Slide macht neugierig auf den Post, ohne ihn aufzulösen, und endet mit genau dieser Zeile: „Tipp auf den Post ↓"

DER POST (lies vor allem den Hook):
Hook: „{{PHOOK}}"
Titel: {{PTITEL}}
Slides:
{{PSLIDES}}
Caption:
{{PCAPTION}}`;
const CTA_OHNE = `CTA nur, wenn Carina ihn verlangt: „Schreib mir STARTEN ↓"`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }
  let thema = '', count = 5, post = null, heute = '';
  try {
    const body = await req.json();
    thema = String(body.thema || '').replace(/\s+/g, ' ').trim().slice(0, 600);
    count = Math.min(Math.max(parseInt(body.count, 10) || 5, 3), 5);
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

  let prompt = PROMPT.replace('{{THEMA}}', thema).replace(/\{\{ANZAHL\}\}/g, String(count))
    .replace('{{CTA}}', post
      ? CTA_POST.replace('{{PHOOK}}', post.hook || post.titel || '—').replace('{{PTITEL}}', post.titel || '—')
        .replace('{{PSLIDES}}', post.slides.length ? post.slides.map((x, k) => `${k + 1}. ${x.slice(0, 500)}`).join('\n') : '—')
        .replace('{{PCAPTION}}', post.caption || '—')
      : CTA_OHNE);
  if (heute) {
    prompt += `\n\nROHTEXT VON HEUTE (echt, von Carina selbst eingetragen, das ist das Material für die Sequenz):\n${heute}\n- Bau die Sequenz aus genau diesem Text, möglichst in ihren Worten. Nichts dazuerfinden, keine Zahlen, Namen oder Zitate ergänzen. Steht hier eine Begründung, ist sie der Kern von Schritt 3.`;
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
    const stories = (Array.isArray(out.stories) ? out.stories : []).slice(0, 5)
      .map((s) => ({ text: String(s?.text || '').trim(), visual: '', sticker: '' }))
      .filter((s) => s.text);
    if (!stories.length) return new Response(JSON.stringify({ error: 'Keine Stories erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ stories }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
