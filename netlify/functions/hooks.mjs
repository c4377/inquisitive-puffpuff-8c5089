// Netlify Function: Hook-Generator — Hooks in Carinas Stimme für Feed-Posts (Bulk-Format) oder Reels.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// POST { art: "feed"|"reels", thema?: "…", start?: 1, anzahl: 1..25, winkel?: "…" }
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
{"hooks":[{"tag":1,"thema":"2–4 Wörter","slide1":"…"}]}`;

const REELS = `

FORMAT REELS
- Jeder Hook ist der Satz der ersten 2 Sekunden: gesprochen oder als Text im Bild. Höchstens 100 Zeichen.
- Mische: in die Kamera gesprochen, Text im Bild über ruhigem B-Roll (Kaffee, Schreibtisch, Laptop), Ertappen („Du hast … oder?“), Carinas Geschichte (nur echte Fakten).
- "format": „Kamera“ oder „Text im Bild“.

AUSGABE: NUR JSON, ohne Vorwort:
{"hooks":[{"hook":"…","format":"Kamera"}]}
Genau {{ANZAHL}} Hooks.`;

export default async (req) => {
  if (req.method !== 'POST') return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  const key = process.env.GEMINI_API_KEY;
  if (!key) return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  let art = 'feed', thema = '', start = 1, anzahl = 20, winkel = '', nr = 1;
  try {
    const b = await req.json();
    art = b.art === 'reels' ? 'reels' : 'feed';
    thema = String(b.thema || '').replace(/\s+/g, ' ').trim().slice(0, 400);
    start = Math.max(1, parseInt(b.start, 10) || 1);
    anzahl = Math.min(25, Math.max(1, parseInt(b.anzahl, 10) || 20));
    winkel = String(b.winkel || '').replace(/\s+/g, ' ').trim().slice(0, 200);
    nr = Math.max(1, parseInt(b.nr, 10) || 1);
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  let prompt = GRUND;
  if (art === 'feed') {
    const tage = Array.from({ length: anzahl }, (_, k) => { const t = start + k; return `Tag ${t}: ${REGEL[PLATZ[t % 8]]}`; }).join('\n');
    prompt += FEED.replace('{{TAGE}}', tage).replace('{{NR}}', String(nr).padStart(2, '0'));
  } else {
    prompt += REELS.replace('{{ANZAHL}}', String(anzahl));
  }
  if (thema) prompt += `\n\nTHEMA VON CARINA (alle Hooks drehen sich darum, aus verschiedenen Richtungen): ${thema}`;
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
    if (art === 'feed') {
      hooks = liste.map((h, k) => {
        let s1 = String(h?.slide1 || '').replace(/\s+/g, ' ').trim().replace(/^Slide\s*1\s*:\s*/i, '');
        const m = /^\[([^\]]*)\]\s*/.exec(s1);
        if (m && m[1].length > 24) s1 = s1.slice(m[0].length); // zu lange Rubrik würde sichtbar stehen bleiben
        return { tag: start + k, thema: String(h?.thema || '').replace(/\s+/g, ' ').trim().slice(0, 40) || 'Thema', slide1: s1 };
      }).filter((h) => h.slide1).slice(0, anzahl);
    } else {
      hooks = liste.map((h) => ({ hook: String(h?.hook || '').replace(/\s+/g, ' ').trim(), format: /text/i.test(String(h?.format || '')) ? 'Text im Bild' : 'Kamera' }))
        .filter((h) => h.hook).slice(0, anzahl);
    }
    if (!hooks.length) return new Response(JSON.stringify({ error: 'Keine Hooks erhalten. Nochmal versuchen.' }), { status: 502 });
    return new Response(JSON.stringify({ hooks }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
