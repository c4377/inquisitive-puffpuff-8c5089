// Netlify Function: Caption zu einem Post.
// POST { day: { day, title, slides: [text], caption }, keyword } -> { caption }
// Der Schluessel bleibt serverseitig.

const REGELN = `
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

Du schreibst Instagram-Captions für Carina (carinaannaprav.at).
Sie bringt Coaches und Unternehmerinnen zum ersten vierstelligen Verkauf.
Das Angebot ist das Mentoring / die 1:1-Begleitung.

FORM
- Keine Hashtag-Wolke. Wenn Hashtags, dann höchstens #moneymindset #sheo.
- Zu Emojis gilt der VOICE-Block weiter unten, nicht diese Zeile.

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

GEGENBEISPIEL STATT RATSCHLAG
Wenn die Caption etwas erklaert oder anwendbar macht, geht sie ueber den
FEHLER, nicht ueber den Rat. Nicht "mach X", sondern "du machst Y,
deshalb passiert Z". Ein Ratschlag rauscht durch; ein Fehler, den man
gerade selbst macht, bleibt haengen.

  So: erst das, was sie gerade tut. Dann, was daraus wird. Dann, was
  stattdessen dasteht — konkret genug, dass man es heute aendern kann.

    gut   "Deine Pinnwand heisst 'Inspiration'. Danach sucht keine.
           Nenn sie, wonach gesucht wird."
    mies  "Nutze relevante Keywords fuer mehr Sichtbarkeit."

Der Fehler wird als BEOBACHTUNG benannt, nie als Vorwurf — es geht gegen
die Situation, nie gegen die Leserin. Und: keine Haeme ueber fremde
Fehler, auch nicht ueber die eigenen von frueher.

Setze dabei nichts voraus. Erklaere das Wort, bevor du es benutzt. Nenne
die Zahl statt "regelmaessig". Sie ist keine Anfaengerin im Business —
aber bei dieser Mechanik faengt sie bei null an. Also bei der SACHE bei
null anfangen, bei der PERSON nicht.

ZAHLEN — RECHTLICH
Carinas Zahlen sind KUNDENZAHLEN und muessen nach oesterreichischem
Werberecht belegbar sein. Keine Zahl ohne Beleg, keine Zahl als
Versprechen. Bei Einzelfaellen steht "Einzelfall, kein Durchschnitt"
dabei.

BEWEIS — KUNDENERGEBNISSE, nicht Selbstversuch
Was zaehlt:
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

HALTUNG
- Keine Dienstleisterinnen-Hoeflichkeit ("Ich wuerde mich freuen").
- Keine Absicherungsfloskeln ("Das ist natuerlich individuell").
- Kein Ratgeber-Ton, kein "5 Tipps".
- Sie darf ueber sich selbst sprechen. Selbstbeweis traegt, es gibt
  noch keine fremden Stimmen.
- Nicht gegen Mindset-Arbeit — die Arbeit liegt davor, am Angebot.
- Keine Bewertung der Zahlungsfähigkeit von Kundinnen.
- Umsatzzahlen dürfen vorkommen, sind aber nie das Versprechen.
- Beweis statt Eigenlob. Weniger erklären, mehr zeigen.
`;

// Wofuer die Caption arbeitet. Der Angebotsblock haengt nicht mehr fest
// am Money Room — Carina verkauft mehrere Dinge nebeneinander.
const ZIELE = {
  1: {
    name: 'Angebotsserie',
    cta: 'DABEI',
    block: `
DAS ZIEL — DIE LAUFENDE SERIE
Es geht um Angebote schreiben: ein Paket statt drei, der Preis sichtbar,
der Beleg neben der Behauptung, am Ende eine Aufforderung.

WAS DIE CAPTION LEISTEN MUSS
Sie gehoert zu einer Reihe, die weiterlaeuft. Also ein Satz, der die
naechste Folge ankuendigt oder auf die vorige zeigt. Nicht "Teil 3 von 7",
sondern inhaltlich: was heute drankommt und was als Naechstes kommt.

DER CTA
Kein Verkauf. Wer dabeibleiben will, sagt es — und bekommt die naechste
Folge. Das ist die einzige Aufforderung.

WER CARINA IST — gehoert dazu, aber beilaeufig
Angebotsarchitektin in Wien. Gruenderin von The Money Room. Hat einen
Kurs, The Strategy. Zehn eigene Gruendungen. Das steht als Nebensatz da,
nicht als Vorstellungsrunde.

KEINE Qualifizierung in dieser Fassung. Die Serie ist fuer alle offen.
`,
  },
  2: {
    name: 'The Money Room',
    cta: 'MOVE',
    block: `
DAS ANGEBOT — THE MONEY ROOM
97 Euro im Monat, Starterpreis, solange die Gruppe klein ist.
Kein Lernprogramm, ein Umsetzungsraum. Alle zwei Wochen ein Slot,
dazwischen werden Fragen beantwortet. Alles liegt hochgeladen bereit.
Das Intensive gibt es fuer Mitglieder um 444 statt 888 Euro.

BEWEIS
Launch von 6.000 auf 12.000 Euro, nur durch neue erste drei Saetze.
IMMER dazusagen: Einzelfall, kein Durchschnitt.

QUALIFIZIERUNG — gehoert in JEDE Caption, keine Ausnahme
Sie geht ueber die HALTUNG, nie ueber Voraussetzungen. Niemand wird
daran gemessen, was er schon hat, wie weit er ist oder wo er gerade
steckt. Ausgeschlossen wird, wer nicht bereit ist:

Nicht fuer die, die nicht umsetzen wollen.
Nicht fuer die, die nicht investieren wollen.
Nicht fuer die, die an ihrem jetzigen Zustand nichts aendern wollen.
Nicht fuer die, die glauben, sie bekommen das alles allein hin.
`,
  },
  3: {
    name: 'Mentoring, das 1:1',
    cta: 'MENTORING',
    block: `
DAS ANGEBOT — DAS MENTORING
Zwoelf Monate, acht Plaetze. 15.000 Euro auf einmal oder 1.250 im Monat.
Taeglich auf Telegram, ohne Uhrzeit. Jeder Launch, jedes Angebot, jeder
Sale wird gemacht, nicht besprochen. Acht Etappen ueber das Jahr:
Brainstorm, Strategiesitzung, Zusammenfassung, Testphase, Plan, Pruefen,
Nachschaerfen, Umsatzbooster.

KEIN KAUFKNOPF
Es laeuft nur ueber Anfrage. Carina antwortet mit einem von drei Saetzen:
Platz frei. Platz frei, aber der Money Room passt gerade besser. Oder
kein Platz, du stehst auf der Liste.

QUALIFIZIERUNG
Acht Plaetze, nicht mehr. Nicht fuer Frauen, die sammeln statt umzusetzen.
`,
  },
  4: {
    name: 'Das Intensive',
    cta: 'INTENSIVE',
    block: `
DAS ANGEBOT — DAS INTENSIVE
888 Euro, aus dem Money Room 444. Eine Sitzung, vierzig Minuten, nur ein
Fall. Vorab fuellt sie ein Dokument aus: Angebot, Preis, woran es haengt.
Carina arbeitet es durch, bevor sie sich sehen.
Die Sitzung IST die Ausarbeitung, nicht die Besprechung davon.

DER UNTERSCHIED
Kein Rebrand, keine Positionierungsschleife. Umgebaut wird, was schon
steht: ein Paket statt drei, der Preis sichtbar, der Beleg neben der
Behauptung.

KEIN KAUFKNOPF
Nur auf Anfrage, Antwort innerhalb von zwei Tagen.
`,
  },
  5: {
    name: 'The Strategy',
    cta: 'STRATEGY',
    block: `
DAS ANGEBOT — THE STRATEGY
Der Kurs, mit dem sie auf Instagram verkauft. Startvideo und Voice Notes,
kein Modulberg, den man nachholen muss. Man hoert eine Note und macht
danach etwas.

WAS DIE CAPTION LEISTEN MUSS
Der Unterschied zu einem Kurs, der im Ordner liegt: hier ist nach jeder
Note etwas zu tun. Das ist das Verkaufsargument, nicht der Umfang.

QUALIFIZIERUNG
Nicht fuer Frauen, die sammeln statt umzusetzen.
`,
  },
};


// Die Stilreferenz kommt aus dem Aufruf. Kommt keine, steht hier der
// Ersatz — dann traegt das Regelwerk oben den Ton allein. Sobald Carina
// zwei, drei eigene Captions liefert, gehoeren sie hier hinein.


const VOICE_BLOCK = `
=== VOICE ===
Sprache: Deutsch mit selbstverständlichem Denglisch (Dream Client,
Offer, Funnel, Test Reel, Social Proof, Win, ready, geil). Nicht
erklären, nicht übersetzen.
Anrede: durchgehend "du", fourth wall, direkt. Sie liest dir Gedanken
vor, die du selbst noch nicht ausgesprochen hast.
Sätze: kurz. Ein Gedanke pro Absatz, Leerzeile dazwischen. Fragmente
als Betonung erlaubt. Absätze von 1–3 Sätzen, nie Blocktext.
Beweis: konkrete Zahlen statt Adjektiven (Monatsumsatz, Follower-
Zuwachs, Reichweite, Zeitraum). Nie eine Behauptung ohne Zahl oder
Beispiel dahinter.
Einwand: den Gegeneinwand offen benennen, kurz gelten lassen
("X kann geil sein, um ..."), dann drehen ("Doch, wenn ...").
Rhetorische Frage im letzten Drittel, die das Reframe trägt.
Kurzer Punch-Satz als Absatzschluss (3–5 Wörter, Aussage, kein Hedging).
Emojis: sparsam, 2–4 pro Caption, immer am Satzende, nie im Satz,
nie zwei nebeneinander. Nie am Anfang einer Zeile außer bei ⬇️ im Hook.
Verboten: Höflichkeitsfloskeln, "Hey ihr Lieben", Hashtag-Wolke,
Tipp-Listen ohne Ich-Bezug, Konjunktiv-Weichmacher ("könnte
vielleicht"), Erklärbär-Ton.

=== BEZUG ===
Jede Caption greift den konkreten Post-Inhalt auf: Aussage, Zahl,
Beispiel, Szene oder Slide-Reihenfolge. Test: Ohne den Post darf die
Caption keinen Sinn ergeben. Wiederhole den Post nicht 1:1 – ergänze
ihn um Kontext, Gegenbeispiel, Konsequenz oder Einordnung.

=== AUFBAU ===
1. Hook (1 Zeile): setzt den Post fort, statt ihn zusammenzufassen.
   Entweder Fortsetzung des Reels ("Auf diese 2 Dinge achte ich
   zusätzlich ⬇️"), harte Behauptung über die Leserin, oder
   Zeitanker mit Ergebnis ("Vor 4 Jahren ... heute ...").
2. Kontext/Problem: was im Post steht, weitergedreht — Konsequenz,
   Gegenbeispiel oder das, was die Leserin insgeheim denkt.
3. Beweis: eigene Zahlen oder Client-Ergebnisse, konkret benannt.
4. Reframe: rhetorische Frage oder Umkehrung des Einwands.
5. Optional eine Zeile Selbstvorstellung, wenn der Post Reichweite
   außerhalb der Community bekommt.
6. CTA: letzte Zeile, ein Satz, locker, ein Emoji. Bei Listenposts
   stattdessen nummeriert (1) / 2) mit je einem erklärenden Satz)
   und CTA darunter.

Diese drei Abschnitte sind bindend. Die Variante der Caption ergibt sich
aus dem Post selbst — aus dem, was in den Folien steht — nicht aus einer
vorgegebenen Fassung.
`;



export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let monday = false, day = null, keyword = '', ziel = 2;
  let stilreferenz = '';
  try {
    const body = await req.json();
    day = body.day || null;
    monday = body.monday === true;
    keyword = String(body.keyword || '').trim().slice(0, 24);
    ziel = [1, 2, 3, 4, 5].includes(Number(body.ziel)) ? Number(body.ziel) : 2;
    stilreferenz = String(body.stilreferenz || '').slice(0, 8000).trim();
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!day) return new Response(JSON.stringify({ error: 'day fehlt' }), { status: 400 });

  const folien = (day.slides || []).filter(Boolean).slice(0, 20)
    .map((t, i) => `${i + 1}. ${String(t).replace(/\u00A0/g, ' ')}`).join('\n');

  const tonzusatz = monday
    ? '\n\nSCHREIBE IN DER TONLAGE "MONDAY" (siehe oben). Sie gilt fuer den ganzen Text.'
    : '';
  const ctaZeile = keyword
    ? `CTA: "Kommentiere ${keyword.toUpperCase()}"`
    : `CTA: "Kommentiere ${ZIELE[ziel].cta}"`;

  const prompt = `${monday ? 'SCHREIBE IM MONDAY-TON — die Regeln dazu stehen unten.\n\n' : ''}${REGELN}
${ZIELE[ziel].block}
${stilreferenz ? `STILREFERENZ — nur die Machart, nie den Inhalt uebernehmen:\n---\n${stilreferenz}\n---` : ''}
${VOICE_BLOCK}

DER POST — Tag ${day.day}${day.title ? `: ${day.title}` : ''}
${folien}

${ctaZeile}

Schreibe die Caption. Sie muss in den ersten drei Zeilen erkennbar an
einem Satz aus dem Content Piece andocken und danach genau eine Sache
bringen, die dort nicht steht. Keine Zusammenfassung, keine
Wegbeschreibung.
${ziel !== 1 ? 'Die Qualifizierung MUSS vorkommen, und sie geht ueber die Haltung:\nnicht fuer die, die nicht umsetzen, nicht investieren oder an ihrem\nZustand nichts aendern wollen — und nicht fuer die, die glauben, sie\nbekommen das allein hin. Nie daran festmachen, was jemand schon hat.' : ''}

ANTWORTE NUR MIT JSON, ohne Vorwort, ohne Markdown:
{"caption":"…"}
Zeilenumbrüche im Text als \\n.${tonzusatz}`;

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
            generationConfig: { temperature: 0.95, responseMimeType: 'application/json' },
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
    let out;
    try {
      out = JSON.parse(sauber);
    } catch {
      const a = sauber.indexOf('{'), b = sauber.lastIndexOf('}');
      out = a >= 0 && b > a ? JSON.parse(sauber.slice(a, b + 1)) : null;
    }
    const caption = out && typeof out.caption === 'string' ? out.caption.trim() : '';
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
