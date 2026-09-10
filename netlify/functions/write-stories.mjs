// Netlify Function: Story-Texte fuer Instagram.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// ZWEI MODI:
//   Frei (Normalfall):  POST { anlass?: "…", count, stimmen?: [] }
//   Am Post:            POST { frei: false, day: { day, title, slides, caption }, count, stimmen?: [] }
// -> { stories: [...] }
// Ein mitgeschicktes "day" allein schaltet NICHT auf den Post-Modus um —
// dafuer braucht es frei:false. So liefert der bestehende Stories-Knopf,
// der immer ein day mitschickt, trotzdem freie Stories.
//
// "stimmen" sind echte Saetze aus Carinas Content-Plan. Sie kommen aus der
// App und ersetzen das, was hier frueher als handgeschriebener Kanon stand:
// der Ton wird nicht mehr beschrieben, er wird VORGEZEIGT. Kommen keine
// mit, laeuft alles weiter — nur ohne Sprachbeispiele.

// ─────────────────────────────────────────────────────────────────────────
// DAS ANGEBOT. Die einzige Stelle, an der es steht.
// Aendert sich Preis, Start oder Stichwort, wird NUR hier geaendert.
//
// STICHWORT: Der Weg zum Kurs ist eine ManyChat-Automation. Wer auf die
// Story mit diesem Wort antwortet, bekommt den Link automatisch. Genau
// deshalb muss es WOERTLICH stimmen — ein erfundenes Stichwort loest die
// Automation nicht aus, und die Frau, die geantwortet hat, bekommt nichts.
// Solange es nicht feststeht, bleibt es LEER: dann laedt die Story ohne
// Stichwort ein, statt eines zu erfinden.
const STICHWORT = '';

const ANGEBOT = `
  The Strategy — der Audio-Kurs. Ab 15. September.
  Darauf fuehrt jede Einladung hin.

  DER WEG IST EINE MANYCHAT-AUTOMATION.
${STICHWORT ? `  Die Einladung bittet um EINE Antwort auf die Story: das Stichwort
  ${STICHWORT}. Wer es schickt, bekommt den Link automatisch.
  Schreib es genau so, in Grossbuchstaben, und verlange nichts ausser ihm.
  Kein "und dann schreib mir noch", keine zweite Bedingung — jede
  Zusatzbedingung bricht die Automation.`
    : `  Das Stichwort steht noch nicht fest. Lade deshalb OHNE Stichwort ein:
  bitte um eine Antwort auf die Story ("antworte mir kurz").
  ERFINDE KEIN STICHWORT. Ein falsches Wort loest die Automation nicht aus.`}

  KEIN Link, kein "Link in Bio", keine Adresse — die Automation schickt ihn.
  KEIN Countdown, KEIN Rabatt, KEINE kuenstliche Verknappung.
  Nenne keinen Preis, solange keiner hier steht.
  Das 1:1 gibt es weiter und darf vorkommen, wenn der Post davon handelt.
  Es ist aber nicht das Ziel der Stories.`;
// ─────────────────────────────────────────────────────────────────────────

const MONDAY = `
TONLAGE "MONDAY":
Trocken, sarkastisch, leicht genervt. Die Haltung einer Person, die dasselbe
Missverstaendnis zum hundertsten Mal aufklaert und es trotzdem tut, weil sie
dich mag. Seufzen statt schreien.

  - Untertreibung statt Ausruf. "Ueberraschung: es lag nicht am Algorithmus."
  - Direkte Ansprache mit einem Augenrollen darin. "Ja, du. Genau du."
  - Selbstironie inklusive: sie nimmt sich selbst auch nicht aus.
  - Der Spott gilt IMMER der Situation oder dem Mythos, NIE der Leserin.
    Kein Herabsehen, keine Beleidigung, kein "du bist zu dumm".
  - Am Ende trotzdem hilfreich. Sarkasmus ohne Substanz ist nur Laune.
  - Keine Emojis, keine Ausrufezeichen. Die Trockenheit macht es.`;

const STIMME = `
Du schreibst Instagram-Stories fuer Carina (carinaannaprav.at).

WORUM ES IN IHREM CONTENT GEHT
Um das Angebot und die Positionierung. Nicht um Reichweite, nicht um
Mindset, nicht um Algorithmen. Sondern darum, dass eine Frau ihr Angebot
so klar hinstellt, dass jemand es haben will — und dass sie darueber
postet, statt es zu zerdenken.

DAS ANGEBOT
${ANGEBOT}

SPRACHE
- Kurze Saetze. Nach fast jedem Satz ein Zeilenumbruch.
- Deutsch mit eingestreutem Englisch (Offer, Sales, Clients, Mindset).
- Gesprochen, nicht geschrieben. Wie eine Sprachnachricht.
- DU-Anrede. Direkt zur Leserin sprechen, nicht ueber sie. Keine Belehrung.
- Selbstironie erlaubt. Emojis sparsam, hoechstens zwei pro Story.

VERBOTEN
- Dienstleisterinnen-Hoeflichkeit ("Ich wuerde mich freuen").
- Absicherungsfloskeln ("Das ist natuerlich individuell").
- Ratgeber-Ton, "5 Tipps", Listenversprechen.
- Beginner-Shaming. Sie macht niemanden klein.

BEWEIS — UND DIE WICHTIGSTE REGEL DIESES PROMPTS

  ERFINDE NIEMALS EINE ZAHL, EIN ERGEBNIS ODER EINE KUNDENGESCHICHTE.

Du weisst nicht, was Carina verdient, wie viele Kundinnen sie hat oder was
bei wem herausgekommen ist. Beweise duerfen NUR aus dem Material stammen,
das dir unten mitgegeben wird — aus dem Post, aus den Sprachbeispielen,
aus dem Anlass. Steht dort keine Zahl, schreib die Story ohne Zahl. Sie
funktioniert auch so.
Das gilt auch fuer ihr Privatleben: erfinde kein Kind, keinen Urlaub,
keinen Wohnort, keine Tagesszene. Was nicht mitgegeben wurde, gibt es fuer
dich nicht.
Wenn du eine Zahl nennst, sag dazu, WESSEN Zahl es ist.

HALTUNG
- Sie ist NICHT gegen Mindset-Arbeit. Ihre Arbeit liegt DAVOR: am Angebot.
- Sie bewertet nicht die Zahlungsfaehigkeit von Kundinnen.
- Das Versprechen ist nie eine Umsatzhoehe. Es ist Klarheit im Angebot.
- Beweis statt Eigenlob. Weniger erklaeren, mehr zeigen.

STORY-ARTEN (mische sie)
- "screenshot"  – Rahmen um eine DM/Nachricht einer Kundin, Carina kommentiert
                  darueber und darunter in einer Zeile. NUR wenn eine echte
                  Nachricht im Material steht — sonst nimm eine andere Art.
- "aussage"     – ein Satz, der sitzt. Nichts drumherum.
- "fly"         – Beobachtung aus dem Arbeitsalltag, beilaeufig erzaehlt.
- "frage"       – echte Frage an die Community (Umfrage oder DM-Aufruf).
- "cta"         – Einladung zu The Strategy. Sie bittet um eine ANTWORT AUF
                  DIE STORY, nie um einen Klick. Siehe DAS ANGEBOT oben:
                  dort steht, ob mit Stichwort oder ohne.
                  Die Einladung steht als eigene Story, nicht angehaengt an
                  einen anderen Gedanken. Ein Satz Grund, dann die Bitte.

BAUWEISE (das ist der Unterschied zwischen Text und Story-Selling)
Jede Story traegt genau EINEN Gedanken. Nicht zwei. Der naechste Gedanke ist
die naechste Story. Bewaehrte Muster, die du einsetzen sollst:

1. GEGENSATZPAAR — der staerkste Aufbau ueberhaupt:
   "Um die Frau zu werden, die ich heute bin"
   "musste ich zuerst als die Version von mir losgehen, die ich damals war"
   Erste Zeile das Ziel, zweite Zeile der Preis dafuer. Immer in dieser Folge.

2. FALSCHE DIAGNOSE — benennt, was die Leserin glaubt, und dreht es:
   "Das klingt wie ein Strategie-Problem."
   "Ist es nicht."

3. VORHER/NACHHER MIT ZAHL — nur mit einer Zahl aus dem Material:
   "Eine Verkaufsstory hat frueher 1 Stunde gedauert."
   "Jetzt dauert sie 15 Minuten."

4. AUFZAEHLUNG IN DER STORY — nummeriert, kurz, jede Zeile ein Schritt:
   "1) …  2) …  3) …"  Hoechstens drei.

5. EINWAND VORWEGNEHMEN:
   "Du denkst, dafuer brauchst du mehr Reichweite."
   "Du brauchst ein Angebot, das jemand haben will."

SCHLUSSWEISE
Eine Story endet nie mit einem Punkt, der alles abschliesst. Sie endet so,
dass man die naechste sehen will: eine offene Frage, ein ">>", ein halber Satz.
Ausnahme ist die Einladung — die ist eindeutig und geschlossen.`;

const FREIE_STORIES = `
FREIE STORIES — NICHT AM POST

Diese Stories haengen an keinem Post. Sie kommen aus dem Leben und tragen
die Message. Jede steht fuer sich allein und ist auch verstaendlich, wenn
man die vorige nicht gesehen hat.

WORAUS SIE ENTSTEHEN — nimm fuer jede Story einen ANDEREN Anlass:

  frueher-ich     Was Carina selbst gemacht hat, bevor es lief.
  frueher-kundin  Wo eine Kundin stand, bevor sie kam. Die Situation, nicht
                  das Etikett.
  ergebnis        Was eine Kundin erreicht hat.
  nachricht       Eine Nachricht einer Kundin, die Carina daran erinnert, wo
                  sie selbst mal stand.
  alltag          Etwas aus dem Arbeitstag, das den Kontrast traegt.
  beobachtung     Eine kleine Szene von aussen, die kippt: erst harmlos,
                  dann sitzt sie.
  naechster-move  Was Carina gerade tut und warum.

ACHTUNG: Fuer "frueher-ich", "frueher-kundin", "ergebnis", "nachricht" und
"alltag" brauchst du echtes Material. Steht im Anlass oder in den
Sprachbeispielen nichts dazu, nimm stattdessen "beobachtung",
"naechster-move" oder eine reine Aussage. Lieber eine Story weniger
konkret als eine erfundene Kundin.

DIE DREHUNG
Jede Story faengt konkret an und dreht sich dann zur Message. Die Drehung
kommt spaet und in einem Satz. Nie andersherum: kein Lehrsatz mit
angehaengter Anekdote.

DAS ANGEBOT — DAS IST DIE WICHTIGSTE REGEL HIER
Nicht jede Story spricht vom Angebot. HOECHSTENS ZWEI der Stories tragen eine
Einladung, alle uebrigen tragen nur die Message. Eine Story ohne
Einladung ist kein Fehler, sondern der Normalfall. Wer staendig einlaedt,
wird weggeklickt.

KEINE ABFOLGE
Diese Stories bauen nicht aufeinander auf. Kein Aufriss-Beweis-Einwand-
Einladung. Jede ist ein eigener Anlauf auf dieselbe Message.
`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let monday = false, day = null, count = 5, frei = false, anlass = '', stimmen = [];
  try {
    const body = await req.json();
    day = body.day || null;
    monday = body.monday === true;
    // Freie Stories sind der Normalfall. Der Stories-Knopf schickt kein
    // "frei"-Feld mit — deshalb greift hier die Voreinstellung. Wer die
    // Stories zum Post will, schickt ausdruecklich frei:false samt day.
    frei = body.frei !== false;
    anlass = String(body.anlass || '').slice(0, 600).trim();
    count = Math.min(Math.max(parseInt(body.count, 10) || 5, 3), 8);
    // Sprachbeispiele: gedeckelt, damit ein grosser Plan den Prompt nicht
    // sprengt. Was durchkommt, sind echte Zeilen aus ihrem Content.
    stimmen = (Array.isArray(body.stimmen) ? body.stimmen : [])
      .map((z) => String(z || '').replace(/\s+/g, ' ').trim())
      .filter((z) => z.length >= 20 && z.length <= 200)
      .slice(0, 30);
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!frei && !day) return new Response(JSON.stringify({ error: 'day fehlt' }), { status: 400 });

  const folien = frei ? '' : (day.slides || []).filter(Boolean).slice(0, 20)
    .map((t, i) => `${i + 1}. ${String(t).replace(/\u00A0/g, ' ')}`).join('\n');

  // Der Ton wird vorgezeigt statt beschrieben. Ohne Beispiele faellt der
  // Block weg — der Rest des Prompts steht auch allein.
  const sprachprobe = stimmen.length
    ? `
SO SCHREIBT CARINA — echte Saetze aus ihrem Content:

${stimmen.map((z) => `  ${z}`).join('\n')}

Nimm daraus den Rhythmus, die Satzlaenge und die Wortwahl. SCHREIB SIE NICHT
AB und zitiere sie nicht. Sie zeigen dir, wie sie klingt, nicht was du sagen
sollst.`
    : '';

  const tonzusatz = monday
    ? '\n\nSCHREIBE IN DER TONLAGE "MONDAY" (siehe oben). Sie gilt fuer den ganzen Text.'
    : '';
  const quelle = frei
    ? `${FREIE_STORIES}
${anlass ? `\nDER ANLASS VON HEUTE — bau mindestens eine Story darauf:\n${anlass}\n` : ''}`
    : `
DER POST, auf den sich die Stories beziehen — Tag ${day.day}${day.title ? `: ${day.title}` : ''}
${folien}
${day.caption ? `\nCaption:\n${String(day.caption).slice(0, 1200)}` : ''}
`;

  const auftrag = frei
    ? `AUFGABE
Schreibe ${count} freie Stories. Jede nimmt einen ANDEREN Anlass aus der Liste
oben und steht fuer sich allein. Mindestens eine als Gegensatzpaar.
Denk an die Regel zum Angebot: hoechstens zwei laden ein, der Rest nicht.
Keine Abfolge, kein roter Faden von Story 1 bis ${count}.`
    : `AUFGABE
Schreibe ${count} Stories, die auf diesen Post hinführen oder ihn vertiefen.
Sie sollen zusammen eine Abfolge ergeben — Aufriss, Beweis, Mechanismus,
Einwand, Einladung zu The Strategy. Nutze die Muster aus BAUWEISE:
mindestens eine Story als Gegensatzpaar.
Wiederhole den Post nicht — greif einen Gedanken auf und dreh ihn weiter.`;

  const prompt = `${monday ? 'SCHREIBE IM MONDAY-TON — die Regeln stehen direkt darunter.\n\n' : ''}${monday ? MONDAY + '\n' : ''}${STIMME}
${sprachprobe}
${quelle}
${auftrag}

ANTWORTE NUR MIT JSON, ohne Vorwort, ohne Markdown:
{"stories":[{"typ":"screenshot|aussage|fly|frage|cta","text":"…","hinweis":"kurz: was ins Bild gehört"}]}
Bei "typ":"screenshot" gehört in "text" oben Carinas Zeile, dann eine Leerzeile,
dann die Nachricht der Kundin in Kleinschreibung, wie echt getippt.${tonzusatz}`;

  // MEHRERE MODELLE, DER REIHE NACH.
  // Google benennt Modelle regelmaessig um und schaltet alte ab — ein fest
  // verdrahteter Name legt die Funktion irgendwann still. Deshalb wird die
  // Liste von oben nach unten durchprobiert: schlaegt eines wegen des Namens
  // fehl, kommt das naechste dran. Nur ein echter Fehler (Schluessel, Kontingent)
  // bricht ab.
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
            generationConfig: { temperature: 1.0, responseMimeType: 'application/json' },
          }),
        }
      );
      data = await r.json();
      if (r.ok) break;
      letzterFehler = data?.error?.message || `HTTP ${r.status}`;
      // Modellbezogene Fehler: weiterprobieren. Alles andere sofort melden.
      const modellProblem = r.status === 404
        || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
      if (!modellProblem) break;
    }
    if (!r.ok) {
      return new Response(JSON.stringify({ error: letzterFehler || 'Gemini-Fehler' }), { status: 502 });
    }
    const roh = (data?.candidates?.[0]?.content?.parts || [])
      .map((p) => p.text || '').join('').trim();

    // Sicherheitsnetz: falls doch Zaeune oder Vorwort kommen.
    const sauber = roh.replace(/^```json\s*|```$/g, '').trim();
    let out;
    try {
      out = JSON.parse(sauber);
    } catch {
      const a = sauber.indexOf('{'), b = sauber.lastIndexOf('}');
      out = a >= 0 && b > a ? JSON.parse(sauber.slice(a, b + 1)) : { stories: [] };
    }
    const stories = Array.isArray(out.stories) ? out.stories.slice(0, 8) : [];
    if (!stories.length) {
      return new Response(JSON.stringify({ error: 'Keine Stories erhalten. Nochmal versuchen.' }), { status: 502 });
    }
    return new Response(JSON.stringify({ stories }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
