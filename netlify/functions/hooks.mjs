// Netlify Function: Hook-Generator — Hooks in Carinas Stimme für Feed-Posts (Bulk-Format) oder Reels.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { art: "feed"|"reels", thema?: "…", start?: 1, anzahl: 1..25, winkel?: "…", caption?: true, stil?: "klartext"|"neugier" }
//   stil "neugier" (Carina 24.10.: „Hooks mehr wie eve“): Mechanik von Neugier-Hooks, in Carinas Worten, ohne fremde Sätze.
//   Mit caption: zu jedem Hook eine Caption in Carinas Stimme (Feld "caption").
//   feed  -> { hooks: [{ tag, thema, slide1 }] }   (Slide 1 im Bulk-Format, passend zum Feed-Rhythmus)
//   reels -> { hooks: [{ hook, format }] }
// Die App fragt größere Mengen in Paketen zu 20 parallel an (je ein anderer Winkel), damit keine Anfrage zu lange dauert.
import { HINTERGRUND, STIMME } from './story-studio.mjs';

// Feed-Rhythmus wie in tools/editorial-look.py (magKontrastFeed, Tag % 8).
const PLATZ = ['foto', 'dunkel', 'quote', 'foto', 'oliv', 'kuli', 'fotoquote', 'hell'];
const REGEL = {
  foto: 'Foto-Tag: Hook steht auf ihrem Foto. Zeichen A (~alt|neu~) oder D ({Wort}, [01] …) erlaubt, B und C nicht.',
  dunkel: 'Dunkle Kachel in Versalien: kurz und hart. Alle Zeichen erlaubt.',
  oliv: 'Oliv-Kachel in Versalien, linksbündig: kurz und hart. Alle Zeichen erlaubt.',
  hell: 'Helle Kachel: ruhiger Satz. Alle Zeichen erlaubt.',
  quote: 'Quote-Tag: ein zitierbarer Satz, den man screenshotten will. KEIN Zeichen A–D. Eine [Rubrik] wird zur Handschrift oben, der Text nach „&“ zur Handschrift unten.',
  fotoquote: 'Quote auf Foto: ein zitierbarer Satz. KEIN Zeichen A–D.',
  kuli: 'Kuli-Notiz: klingt wie eine handgeschriebene Notiz an sie, persönlich, 1–2 Sätze. KEIN Zeichen A–D, keine Rubrik.',
};

const GRUND = `Du schreibst Hooks für Carina Anna Prav (Mentorin für Coaches: Content, Angebote, Verkaufen). Zielgruppe ausschließlich: die Coachin, die postet und nicht verkauft.

${STIMME}

FESTE REGELN
- Immer Deutsch, du-Ansprache, Zahlen als Ziffern.
- Nichts erfinden: keine Zahlen, keine Kundinnen, keine Zitate von Kundinnen, keine Erlebnisse. Fakten nur aus der Liste unten, genau so, wie sie dort stehen.
- Nie „Verkaufslücke“, stattdessen „Funkstille zwischen Like und Anfrage“. „Sprachnotiz“ oder „Voice“, nie „Sprachi“.
- Keine Preise. Kurse und Programme nie als Gegner, Gegner ist das Verhalten. Nie Vorwürfe.
- Keine Sätze oder Begriffe anderer Coaches. Jeder Hook anders, keine Wiederholungen.

${HINTERGRUND}`;

const FEED = `

FORMAT FEED (Slide 1 im Bulk-Format)
[Rubrik] Hook mit höchstens einem *Wort* & kurze Zeile
- [Rubrik] optional, 1–3 Wörter, höchstens 24 Zeichen.
- Hook höchstens 90 Zeichen. Zwei kurze Sätze sind okay, wenn der zweite kippt.
- Nach „&“ optional eine Zeile unter 60 Zeichen, die neugierig macht.
- Höchstens EIN Wort in *Sternchen*.

ERKENNUNGSZEICHEN (etwa jeder 3. Hook, nur wo der Tag es erlaubt, pro Hook höchstens eins)
A  Durchgestrichen: „Du musst nicht ~perfekt|echt~ sein.“
B  Was ich lese: „[Was ich lese] „Mehr Infos im Link.“ & Ich trau mich nicht zu fragen.“
C  Tagebuch: „[Tagebuch] Karussells zuerst. Reels *danach*.“
D  Kasten: „[01] Likes zahlen deine {Miete} nicht.“ (Nummern fortlaufend ab {{NR}})

DIE TAGE (genau diese, in dieser Reihenfolge)
{{TAGE}}

AUSGABE: NUR JSON, ohne Vorwort:
{"hooks":[{"tag":1,"thema":"2–4 Wörter","slide1":"…"{{CAPFELD}}}]}`;

const CAPTION = `

CAPTION (zu JEDEM Hook, Feld "caption")
- Ich-Perspektive, du-Ansprache, Carinas Stimme. 4–8 kurze Absätze, zusammen etwa 400–800 Zeichen, Absätze getrennt mit \\n\\n.
- Erster Satz greift den Hook auf, ohne ihn zu wiederholen. Dann der Gedanke dahinter, Carinas Sicht mit Begründung, ein Satz, der hängen bleibt.
- Schluss: eine Frage an die Leserin oder eine ruhige Einladung („Schreib mir, wenn …“). Kein Codewort, keine Preise, keine Hashtags, Emojis höchstens eins.
- Nichts erfinden: keine Erlebnisse, Zahlen oder Kundinnen, die nicht in den Fakten stehen.`;

const NEUGIER = `

STIL „NEUGIER“ (für diese Hooks wichtiger als die ruhigen Pointen oben)
Diese Hooks machen neugierig und lassen etwas offen, damit man weiterwischt. Mechaniken, frei gemischt:
- Offene Schleife mit Doppelpunkt am Ende: „Seit 2018 auf Instagram. Und das hat mir am meisten über Verkaufen gezeigt:“
- Gegenfrage zu einer verbreiteten Annahme: „Ist Mehrwert-Content am Ende?“
- Nummeriertes Versprechen: „3 Fragen, die dir zeigen, ob dein Post je eine Anfrage bringt:“
- Kontrast mit Auflösung später: „Warum mehr Reichweite gut klingt, aber ein klarer Satz das eigentliche Minimum ist.“
- Echte Autorität aus Carinas Fakten als Einstieg: „25 Coaches begleitet, jedes Video selbst angeschaut. Was fast immer fehlt:“
- „POV:“ mit einer Szene aus dem Alltag der Zielkundin (als Szene, nicht als Behauptung über Carina).
- Die Zeile nach „&“ ist eine kurze, lockere Einladung zum Weiterwischen in Carinas Worten, z. B. „& ich erklär's dir →“, „& kurz und ehrlich“, „& eine davon tut weh“.
- Zahlen nur aus Carinas Fakten. Keine erfundenen Umsätze, Kundenzahlen oder Ergebnisse. Keine Sätze, Floskeln oder englischen Kürzel anderer Coaches übernehmen.
- Die Auflösung muss Carina später liefern können: Versprich nichts, was nicht aus ihrer Arbeit oder ihren Fakten kommt.`;

// Für eine Coach-Nische (Carina 24.10.: „eigene Hooks für Hooks, die ich als XY-Coach heute verwenden würde, danach 5 Hooks“):
// zuerst ein Hook über die Hooks in Carinas Stimme, dann N Hooks, die eine Coachin dieser Nische heute posten kann.
const NISCHE = `Du schreibst für Carina Anna Prav (Mentorin für Coaches). Sie zeigt ihrer Community Hooks, die eine Coachin einer bestimmten Nische heute verwenden kann.

${STIMME}

AUFGABE
NISCHE: {{NISCHE}}
1. "titel": EIN Hook in Carinas Stimme, der diese Hooks ankündigt, z. B. „5 Hooks, die du als {{NISCHE}} heute posten kannst.“ Höchstens 90 Zeichen, ein Wort in *Sternchen*.
2. "hooks": genau {{ANZAHL}} Hooks, die eine {{NISCHE}} für IHRE Kundinnen posten kann. Konkret aus deren Alltag, in der Mechanik oben, jeder mit einer anderen Mechanik: Umdeuten („Du brauchst nicht … Du brauchst …“), Zitat der Kundin plus Übersetzung, „nicht … sondern“, kippendes Gegensatzpaar, offene Schleife mit Doppelpunkt, Gegenfrage, nummeriertes Versprechen.
- Jeder Hook höchstens 100 Zeichen, du-Ansprache an die Kundin der Coachin.
- Keine erfundenen Zahlen, Studien, Ergebnisse oder Erfahrungen. Nichts, was eine Coachin dieser Nische nicht ehrlich sagen kann.
- Keine Heilversprechen, keine medizinischen oder rechtlichen Aussagen.
- "mechanik": 1–3 Wörter, welche Mechanik es ist.

AUSGABE: NUR JSON, ohne Vorwort:
{"titel":"…","hooks":[{"hook":"…","mechanik":"…"}]}`;

const REELS = `

FORMAT REELS
- Jeder Hook ist der Satz der ersten 2 Sekunden: gesprochen oder als Text im Bild. Höchstens 100 Zeichen.
- Mische: in die Kamera gesprochen, Text im Bild über ruhigem B-Roll (Kaffee, Schreibtisch, Laptop), Ertappen („Du hast … oder?“), Carinas Geschichte (nur echte Fakten).
- "format": „Kamera“ oder „Text im Bild“.

AUSGABE: NUR JSON, ohne Vorwort:
{"hooks":[{"hook":"…","format":"Kamera"{{CAPFELD}}}]}
Genau {{ANZAHL}} Hooks.`;

// Caption: Absätze behalten, keine Zeile darf wie „Tag 3:“ oder „Slide 2:“ anfangen (würde den Bulk Import zerlegen).
const sauberCaption = (c) => String(c || '').replace(/\r/g, '').split('\n').map((z) => z.trim().replace(/^(Tag|Day|Woche|Slide|Folie|Bild|Page)\s*(\d+)\s*[:.\-–—]/i, '$1 $2,')).join('\n').replace(/\n{3,}/g, '\n\n').trim().slice(0, 2200);

export default async (req) => {
  if (req.method !== 'POST') return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  const key = process.env.GEMINI_API_KEY;
  if (!key) return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  let art = 'feed', thema = '', start = 1, anzahl = 20, winkel = '', nr = 1, mitCaption = false, stil = 'klartext';
  try {
    const b = await req.json();
    art = b.art === 'reels' ? 'reels' : b.art === 'nische' ? 'nische' : 'feed';
    thema = String(b.thema || '').replace(/\s+/g, ' ').trim().slice(0, 400);
    start = Math.max(1, parseInt(b.start, 10) || 1);
    anzahl = Math.min(25, Math.max(1, parseInt(b.anzahl, 10) || 20));
    winkel = String(b.winkel || '').replace(/\s+/g, ' ').trim().slice(0, 200);
    nr = Math.max(1, parseInt(b.nr, 10) || 1);
    mitCaption = b.caption === true;
    stil = b.stil === 'neugier' ? 'neugier' : 'klartext';
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (art === 'nische' && !thema) return new Response(JSON.stringify({ error: 'Bitte eine Nische eintragen, z. B. Ernährungscoach.' }), { status: 400 });
  let prompt = art === 'nische' ? NISCHE.replace(/\{\{NISCHE\}\}/g, thema).replace('{{ANZAHL}}', String(anzahl)) : GRUND;
  if (art === 'feed') {
    const tage = Array.from({ length: anzahl }, (_, k) => { const t = start + k; return `Tag ${t}: ${REGEL[PLATZ[t % 8]]}`; }).join('\n');
    prompt += FEED.replace('{{TAGE}}', tage).replace('{{NR}}', String(nr).padStart(2, '0'));
  } else if (art === 'reels') {
    prompt += REELS.replace('{{ANZAHL}}', String(anzahl));
  }
  if (stil === 'neugier' && art !== 'nische') prompt += NEUGIER;
  if (mitCaption && art !== 'nische') prompt += CAPTION;
  prompt = prompt.replace('{{CAPFELD}}', mitCaption ? ',"caption":"…"' : '');
  if (thema && art !== 'nische') prompt += `\n\nTHEMA VON CARINA (alle Hooks drehen sich darum, aus verschiedenen Richtungen): ${thema}`;
  if (winkel) prompt += `\n\nSCHWERPUNKT DIESES PAKETS (damit sich die Pakete nicht wiederholen): ${winkel}`;

  const MODELLE = ['gemini-3.6-flash', 'gemini-3-flash', 'gemini-flash-latest', 'gemini-2.5-flash'];
  try {
    let data = null, r = null, letzterFehler = '';
    for (const modell of MODELLE) {
      r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { temperature: 1.0, responseMimeType: 'application/json' } }),
      });
      data = await r.json();
      if (r.ok) break;
      letzterFehler = data?.error?.message || `HTTP ${r.status}`;
      const modellProblem = r.status === 404 || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
      if (!modellProblem) break;
    }
    if (!r.ok) return new Response(JSON.stringify({ error: letzterFehler || 'Gemini-Fehler' }), { status: 502 });
    const roh = (data?.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('').trim().replace(/^```json\s*|```$/g, '').trim();
    let out;
    try { out = JSON.parse(roh); } catch {
      const a = roh.indexOf('{'), b = roh.lastIndexOf('}');
      out = a >= 0 && b > a ? JSON.parse(roh.slice(a, b + 1)) : {};
    }
    const liste = Array.isArray(out.hooks) ? out.hooks : [];
    let hooks;
    if (art === 'nische') {
      hooks = liste.map((h) => ({ hook: String(h?.hook || '').replace(/\s+/g, ' ').trim(), format: String(h?.mechanik || '').replace(/\s+/g, ' ').trim().slice(0, 30) || 'Hook', caption: '' })).filter((h) => h.hook).slice(0, anzahl);
      if (hooks.length && out.titel) hooks.unshift({ hook: String(out.titel).replace(/\s+/g, ' ').trim(), format: 'Hook über die Hooks', caption: '', titel: true });
    } else if (art === 'feed') {
      hooks = liste.map((h, k) => {
        let s1 = String(h?.slide1 || '').replace(/\s+/g, ' ').trim().replace(/^Slide\s*1\s*:\s*/i, '');
        const m = /^\[([^\]]*)\]\s*/.exec(s1);
        if (m && m[1].length > 24) s1 = s1.slice(m[0].length); // zu lange Rubrik würde sichtbar stehen bleiben
        return { tag: start + k, thema: String(h?.thema || '').replace(/\s+/g, ' ').trim().slice(0, 40) || 'Thema', slide1: s1, caption: mitCaption ? sauberCaption(h?.caption) : '' };
      }).filter((h) => h.slide1).slice(0, anzahl);
    } else {
      hooks = liste.map((h) => ({ hook: String(h?.hook || '').replace(/\s+/g, ' ').trim(), format: /text/i.test(String(h?.format || '')) ? 'Text im Bild' : 'Kamera', caption: mitCaption ? sauberCaption(h?.caption) : '' }))
        .filter((h) => h.hook).slice(0, anzahl);
    }
    if (!hooks.length) return new Response(JSON.stringify({ error: 'Keine Hooks erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ hooks }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
