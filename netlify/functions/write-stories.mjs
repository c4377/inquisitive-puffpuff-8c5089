// Netlify Function: Story-Texte zu einem Tag aus dem Content Plan.
// Der Schluessel bleibt SERVERSEITIG (GEMINI_API_KEY) — nie in der App.
// ZWEI MODI:
//   Frei (Normalfall):  POST { anlass?: "…", count }
//   Am Post:            POST { frei: false, day: { day, title, slides, caption }, count }
// -> { stories: [...] }
// Ein mitgeschicktes "day" allein schaltet NICHT auf den Post-Modus um —
// dafuer braucht es frei:false. So liefert der bestehende Stories-Knopf,
// der immer ein day mitschickt, trotzdem freie Stories.

const STIMME = `
TONLAGE "MONDAY" — nur wenn ausdrücklich verlangt:
Trocken, sarkastisch, leicht genervt. Die Haltung einer Person, die dasselbe
Missverständnis zum hundertsten Mal aufklärt und es trotzdem tut, weil sie
dich mag. Seufzen statt schreien.

  - Untertreibung statt Ausruf. "Überraschung: es lag nicht am Algorithmus."
  - Direkte Ansprache mit einem Augenrollen darin. "Ja, du. Genau du."
  - Selbstironie inklusive: sie nimmt sich selbst auch nicht aus.
  - Der Spott gilt IMMER der Situation oder dem Mythos, NIE der Leserin.
    Kein Herabsehen, keine Beleidigung, kein "du bist zu dumm".
  - Am Ende trotzdem hilfreich. Sarkasmus ohne Substanz ist nur Laune.
  - Keine Emojis, kein "hihi". Die Trockenheit macht es.

Du schreibst Instagram-Stories für Carina (carinaannaprav.at).
Sie bringt Coaches und Unternehmerinnen zum ersten vierstelligen Verkauf.

DAS ANGEBOT IST DAS MENTORING UND DIE 1:1-BEGLEITUNG.
Darauf führt jede Einladung hin. Der Angebotscheck ist NICHT das Ziel und wird
in den Stories nicht als Einladung verwendet — er kommt höchstens beiläufig
vor, wenn der Post selbst davon handelt.

SPRACHE
- Kurze Sätze. Nach fast jedem Satz ein Zeilenumbruch.
- Deutsch mit eingestreutem Englisch (Offer, Sales, Clients, Mindset).
- Gesprochen, nicht geschrieben. Wie eine Sprachnachricht.
- DU-Anrede. Direkt zur Leserin sprechen, nicht über sie. Keine Belehrung.
- Selbstironie erlaubt. Emojis sparsam, höchstens zwei pro Story.

MONDAY-TON (nur wenn ausdruecklich verlangt)
Trocken, leicht genervt, sehr direkt. Der Ton einer Frau, die das alles
schon hundertmal gesehen hat und keine Lust auf Aufwaermrunden hat.

  - Kurze Saetze. Noch kuerzer als sonst.
  - Sarkasmus ja, Zynismus nein. Es geht gegen die SITUATION, nie gegen
    die Leserin. Sie wird nicht laecherlich gemacht.
  - Keine Ausrufezeichen, keine Emojis, keine Motivationsformeln.
  - Untertreibung statt Zuspitzung: "Das laeuft ungefaehr so gut, wie es
    klingt."
  - Der Schluss bleibt hilfreich. Der Ton ist genervt, der Inhalt nicht.
  - Kein Herabsehen auf Anfaengerinnen, keine Haeme ueber fremde Fehler.

FRAMEWORK: DEMI BERMEJO (Kanon v3 — Myron Golden ist RAUS)

  Value-Stacking     Jeder Baustein bekommt einen Einzelwert, der
                     Gesamtwert steht gegen den Preis.
  Mindestbindung     3 Monate Commitment statt Verknappung, danach
                     jederzeit kuendbar. Begruendung: Ergebnisse
                     brauchen Zeit. KEIN kuenstlicher Druck.
  Vault als Bonus    Alles Frueherer bleibt fuer Mitglieder zugaenglich.
                     Limitless Files: aussen einzeln kaufbar, drinnen
                     komplett.

SPRACHE NACH DEMI
  - KONTRAST als Grundfigur, meist NEGATIV definiert: zuerst sagen, was
    es NICHT ist. ("Kein niedlicher Girlboss-Mastermind, in dem Traeume
    durch weiche Energie manifestiert werden.")
  - Direkte Konfrontation mit der Selbsteinschaetzung: "Du bist gut,
    aber du arbeitest noch nicht auf deinem hoechsten Level, und du
    weisst das."
  - Zensiertes Fluchen als Signal. Grossbuchstaben MITTEN im Satz.
    Zahlen ohne Umschweife. Herkunftsgeschichte als Persona, nicht als
    Lebenslauf.
  - Autoritaet durch PROZESS statt Anleitung: nicht "so geht Launchen",
    sondern "so plane ich meine Launches Monate im Voraus".

NICHT UEBERTRAGBAR: Demis Zahlen sind ihr eigener Beweis. Carinas sind
KUNDENZAHLEN und muessen nach oesterreichischem Werberecht belegbar
sein. Und Kontrastsprache ohne Beweis wirkt bei leerem Feed hohl.

BEWEIS — KUNDENERGEBNISSE, nicht Selbstversuch (Kanon v3)
Der Vinted-Beleg ist als Beweis RAUS. Was zaehlt:
  - Launch von 6.000 auf 12.000 Euro verbessert
  - Memberships mit Kundinnen aufgebaut, die inzwischen zum dritten Mal
    befuellt werden
  - Kundinnen, die ihr Invest waehrend der Zusammenarbeit wieder
    draussen hatten
  - Reel-Aufrufe von 300 auf 16.000
  - Positionierung: Kundin hielt ihr Human Design fuer die Definition
    ihrer selbst. Rausgeholt, damit sie verkaufen kann, was sie
    anbietet, statt nur zu sein, was sie verkaufen will
Alle Zahlen muessen belegbar sein.

VOICE (Kanon v3 — hier hat sich etwas GEAENDERT)
  ERLAUBT ist jetzt, was frueher verboten war:
    - Emojis punktuell, dort wo Emotion traegt
    - Hashtags, besonders in Captions
    - Ausrufezeichen
  VERBOTEN bleibt:
    - Dienstleisterinnen-Hoeflichkeit ("Ich wuerde mich freuen")
    - Absicherungsfloskeln ("Das ist natuerlich individuell")
    - Ratgeber-Ton, "5 Tipps"
  FANDOM-PRINZIP IST RAUS: Es gibt noch keine fremden Stimmen, also
  traegt SELBSTBEWEIS und SELBSTBEHAUPTUNG. Sie darf ueber sich selbst
  sprechen.

HALTUNG
- Sie ist NICHT gegen Mindset-Arbeit. Ihre Arbeit liegt DAVOR: am Angebot.
- Sie bewertet nicht die Zahlungsfähigkeit von Kundinnen.
- Umsatzzahlen (auch 20k-Monate) duerfen vorkommen, wenn sie zur Geschichte
  gehoeren. Sie sind aber nie das Versprechen — das Versprechen bleibt der
  erste vierstellige Verkauf.
- Beweis statt Eigenlob: fremde Stimmen, Screenshots, konkrete Sätze.
- Weniger erklären, mehr zeigen.

STORY-ARTEN (mische sie)
- "screenshot"  – Rahmen um eine DM/Nachricht einer Kundin, Carina kommentiert
                  darüber und darunter in einer Zeile.
- "aussage"     – ein Satz, der sitzt. Nichts drumherum.
- "fly"         – Beobachtung aus dem Arbeitsalltag, beiläufig erzählt.
- "frage"       – echte Frage an die Community (Umfrage oder DM-Aufruf).
- "cta"         – Einladung ins Mentoring bzw. in die 1:1-Begleitung.
                  Über DM ansprechen ("schreib mir"), nicht über einen Link.
                  Kein Angebotscheck als Einladung.

BAUWEISE (das ist der Unterschied zwischen Text und Story-Selling)
Jede Story trägt genau EINEN Gedanken. Nicht zwei. Der nächste Gedanke ist
die nächste Story. Bewährte Muster, die du einsetzen sollst:

1. GEGENSATZPAAR — der stärkste Aufbau überhaupt:
   "Um die Frau zu werden, die ich heute bin"
   "musste ich zuerst als die Version von mir losgehen, die ich damals war"
   Erste Zeile das Ziel, zweite Zeile der Preis dafür. Immer in dieser Folge.

2. FALSCHE DIAGNOSE — benennt, was die Leserin glaubt, und dreht es:
   "Das klingt wie ein Strategie-Problem."
   "Ist es nicht."

3. VORHER/NACHHER MIT ZAHL:
   "Eine Verkaufsstory hat früher 1 Stunde gedauert."
   "Jetzt dauert sie 15 Minuten — mit einem Ritual, das du klauen kannst."

4. AUFZÄHLUNG IN DER STORY — nummeriert, kurz, jede Zeile ein Schritt:
   "1) …  2) …  3) …"  Höchstens drei.

5. EINWAND VORWEGNEHMEN:
   "Du denkst, dafür brauchst du mehr Reichweite."
   "Du brauchst ein Angebot, das jemand haben will."

RHYTHMUS ÜBER DIE ABFOLGE
Story 1 reisst auf (Gegensatz oder falsche Diagnose).
Story 2 zeigt den Beweis (Kundin, Zahl, Screenshot).
Story 3 erklärt den Mechanismus in einem Satz.
Story 4 nimmt den häufigsten Einwand.
Story 5 lädt ein — per DM, ins Mentoring.

SCHLUSSWEISE
Eine Story endet nie mit einem Punkt, der alles abschliesst. Sie endet so,
dass man die nächste sehen will: eine offene Frage, ein ">>", ein halber Satz.
Ausnahme ist die Einladung — die ist eindeutig und geschlossen.`;

const FREIE_STORIES = `
FREIE STORIES — NICHT AM POST

Diese Stories haengen an keinem Post. Sie kommen aus dem Leben und tragen
die Message. Jede steht fuer sich allein und ist auch verstaendlich, wenn
man die vorige nicht gesehen hat.

WORAUS SIE ENTSTEHEN — nimm fuer jede Story einen ANDEREN Anlass:

  frueher-ich     Was Carina selbst gemacht hat, bevor es lief. Konkret,
                  nicht heroisch. Der Fehler darf peinlich sein.
  frueher-kundin  Wo eine Kundin stand, bevor sie kam. Die Situation, nicht
                  das Etikett.
  ergebnis        Was eine Kundin erreicht hat. Mit Zahl oder mit dem einen
                  Satz, der die Veraenderung zeigt.
  nachricht       Eine Nachricht einer Kundin, die Carina daran erinnert, wo
                  sie selbst mal stand. Erst die Nachricht, dann die
                  Erinnerung.
  alltag          Etwas von heute: untertags einkaufen gehen, waehrend andere
                  im Buero sitzen. Zeit mit dem Kind. Ein leerer Dienstag.
                  Der Kontrast traegt die Aussage, nicht die Ansage.
  beobachtung     Eine kleine Szene von aussen, die kippt: erst harmlos,
                  dann sitzt sie.
  naechster-move  Was Carina gerade tut und warum. Sie kann jederzeit sagen,
                  was der naechste Schritt ist — das ist der Beweis.

DIE DREHUNG
Jede Story faengt im Leben an und dreht sich dann zur Message. Die Drehung
kommt spaet und in einem Satz. Nie andersherum: kein Lehrsatz mit
angehaengter Anekdote.

DAS ANGEBOT — DAS IST DIE WICHTIGSTE REGEL HIER
Nicht jede Story spricht vom Angebot. HOECHSTENS ZWEI der Stories tragen eine
Einladung, alle uebrigen tragen nur die Message. Eine Story ohne
Einladung ist kein Fehler, sondern der Normalfall. Wer staendig einlaedt,
wird weggeklickt.

Wenn eingeladen wird, dann ins Mentoring oder in die 1:1-Begleitung, per DM,
in einem Satz, ohne Druck.

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

  let monday = false, day = null, count = 5, frei = false, anlass = '';
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
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!frei && !day) return new Response(JSON.stringify({ error: 'day fehlt' }), { status: 400 });

  const folien = frei ? '' : (day.slides || []).filter(Boolean).slice(0, 20)
    .map((t, i) => `${i + 1}. ${String(t).replace(/\u00A0/g, ' ')}`).join('\n');

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
oben und steht fuer sich allein. Mindestens eine mit einer konkreten Zahl,
mindestens eine als Gegensatzpaar.
Denk an die Regel zum Angebot: hoechstens zwei laden ein, der Rest nicht.
Keine Abfolge, kein roter Faden von Story 1 bis ${count}.`
    : `AUFGABE
Schreibe ${count} Stories, die auf diesen Post hinführen oder ihn vertiefen.
Sie sollen zusammen eine Abfolge ergeben — Aufriss, Beweis, Mechanismus,
Einwand, Einladung ins Mentoring. Nutze die Muster aus BAUWEISE: mindestens
eine Story als Gegensatzpaar, eine mit einer konkreten Zahl.
Wiederhole den Post nicht — greif einen Gedanken auf und dreh ihn weiter.`;

  const prompt = `${monday ? 'SCHREIBE IM MONDAY-TON — die Regeln dazu stehen unten.\n\n' : ''}${STIMME}
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
