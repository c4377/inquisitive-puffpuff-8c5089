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

AUFBAU — dieser gilt NUR, wenn unten keine ART vorgegeben ist.
Steht unten eine ART, dann zaehlt AUSSCHLIESSLICH deren Aufbau.

Genau diese Teile, in dieser Reihenfolge:

1) ZEILE 1: Hook, der mit einem DOPPELPUNKT endet. Immer.
   Kein Satz ohne Cliffhanger. Danach eine LEERZEILE.
   Beispiel: "Der wahre Grund, warum deine beste Kundenstimme noch immer
   ungehört in deinem Handy liegt:"

2) NUMMERIERTE LISTE, 5 bis 7 Punkte, je EINE Zeile.
   Jeder Punkt beginnt mit "Du" und benennt etwas, das die Leserin gerade
   tut oder glaubt. Kein Ratschlag, keine Lösung — die Liste diagnostiziert.
   Die Punkte steigern sich: der letzte ist der teuerste.
   Danach eine LEERZEILE.

3) FRÜHER — ein Satz, eigener Absatz, danach eine LEERZEILE.
   HEUTE — ein Satz, eigener Absatz. Beide stehen GETRENNT, nicht
   untereinander im selben Block.

4) CTA als FRAGE auf die Liste:
   "Was davon triggert dich am meisten? 1–7 in die Kommentare."
   Die Zahlenspanne passt sich der Anzahl der Punkte an.
   NUR wenn ein CTA-Wort vorgegeben ist, stattdessen: "Kommentiere WORT".

KEIN Philosophie-Satz in Grossbuchstaben. Der Post endet mit dem CTA.

FORM
- 800 bis 1200 Zeichen. Nie länger.
- Du-Form, Präsens.
- Jeder Punkt eine eigene Zeile. Zwischen den Bloecken eine Leerzeile.
- Die Listenzeilen sind kurz genug zum Scannen — höchstens rund 90 Zeichen.
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

FRAMEWORK: DEMI BERMEJO (Kanon v3 — Myron Golden ist RAUS)

  Value-Stacking     Jeder Baustein bekommt einen Einzelwert, der
                     Gesamtwert steht gegen den Preis.
  Ergebnis statt     Wo bei Demi die Vertragsdetails stehen, steht
  Kleingedrucktes    bei uns das Danach. Siehe unten, DER LETZTE
                     SCHLAG. Bindung, Laufzeit, Kuendigung, Vault:
                     kommen nicht vor. Kein Wort davon.

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

const MONEYROOM = `
DAS ANGEBOT — THE MONEY ROOM
97 Euro im Monat. Kein Lernprogramm. Ein Umsetzungsraum.
Die Kundin bringt mit, was gerade auf dem Tisch liegt.
Ziel: in den naechsten Tagen 2.000 Euro mehr machen.

DER MECHANISMUS — JEDER POST HAT EINEN JOB
Die fuenf Jobs sind:
  Bin ich gemeint?   Was hab ich danach?   Warum du?
  Was kostet es?     Was, wenn ich nichts tue?
Ein Post, der keinen dieser Jobs schliesst, ist Leerlauf.

DER LETZTE SCHLAG — direkt nach dem Angebot, vor der Qualifizierung

Hier steht KEIN Kleingedrucktes. Nicht die Laufzeit, nicht die
Bindung, nicht die Kuendigungsfrist, kein "danach jederzeit", kein
Vault, kein Archiv, keine Liste, was alles enthalten ist. Nichts,
was nach Vertrag klingt. Kein Wort ueber die Dauer.

Stattdessen EIN Ergebnis. Was sie hinterher kann, was sie vorher
nicht konnte. Der Moment, in dem sie es merkt — nicht das Gefuehl
danach, sondern die Szene. So konkret, dass sie sich selbst darin
sieht:

  gut   "In zwei Wochen tippst du einen Post und weisst schon beim
         Schreiben, welchen Job er erledigt. Das ist der ganze
         Unterschied zwischen posten und verkaufen."
  gut   "Dein naechster Launch wird nicht groesser. Er wird mit
         denselben Leuten gemacht und mit den richtigen ersten drei
         Saetzen."
  mies  "Du wirst endlich sichtbar und ziehst deine Traumkundinnen an."
  mies  "Mehr Umsatz, mehr Klarheit, mehr Leichtigkeit."

Regeln fuer diese Zeile:
  - Eine Zeile, hoechstens zwei. Sie steht allein.
  - Ihre Sprache, ihr Alltag, ihre Handgriffe. Kein Marketingwort.
  - Ein KOENNEN, kein Gefuehl. "Du weisst", "du schreibst", "du
    siehst" — nicht "du fuehlst dich".
  - Kein Superlativ, kein Ausrufezeichen, keine Garantie.
  - Zahlen nur, wenn sie belegbar sind, und nie als Versprechen.

Das ist das Letzte, was haengen bleibt, bevor die Qualifizierung und
der CTA kommen. Wenn diese Zeile nicht sitzt, sitzt die Caption nicht.

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
`;

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

Diese drei Abschnitte gehen jedem Bauplan vor. Sagt ein Bauplan etwas
anderes über Aufbau, Ton oder Länge, gilt, was hier steht.
`;

const BAUPLAENE = {
  1: {
    name: 'Der Widerspruch',
    bau: `Beginne mit einem Satz, den die Leserin selbst sagt, in
Anfuehrungszeichen. Einen echten, keinen erfundenen.
  "Ich will nicht pushy wirken."
  "Ich warte noch, bis es fertig ist."

Dann eine Zeile, die zeigt, was dieser Satz sie kostet. Nicht moralisch —
rechnerisch oder zeitlich.

Dann der Widerspruch: was sie gleichzeitig will und tut. Zwei Zeilen.

Dann der Ausweg in EINER Handlung, die sie heute machen kann. Nicht
"ueberdenke", sondern "schreib", "streich", "setz".

Angebot, letzter Schlag, Qualifizierung, CTA.`,
  },
  2: {
    name: 'Die Reihenfolge',
    bau: `Fuer alles, was nicht am Aufwand scheitert, sondern an der
Abfolge. Hook: "Du hast kein X-Problem. Du hast ein
Reihenfolge-Problem."

Dann VIER nummerierte Schritte in der falschen Reihenfolge, so wie sie
es gerade macht. Jeder ein Halbsatz.

Dann dieselben vier in der richtigen. Ohne Erklaerung dazwischen — die
Umstellung spricht fuer sich.

Ein Satz, warum die zweite Reihenfolge verkauft und die erste nicht.

Angebot, letzter Schlag, Qualifizierung, CTA.`,
  },
  3: {
    name: 'Die Zahl zuerst',
    bau: `Beginne mit einer belegbaren Zahl aus der Arbeit mit einer
Kundin. Nackt, ohne Aufbau:
  "4.000 Euro in dreissig Tagen. Secondhand-Brautmode."
  "Von 6.000 auf 12.000, geaendert wurden drei Saetze."

Zweite Zeile: was sie NICHT geaendert hat. Das ist der eigentliche
Punkt — kein Rebrand, keine neue Zielgruppe, kein neues Angebot.

Dann der Mechanismus dahinter, in drei bis vier Zeilen. Was genau
gedreht wurde und warum das wirkt.

"Einzelfall, kein Durchschnitt." — dieser Satz MUSS stehen.

Angebot, letzter Schlag, Qualifizierung, CTA.`,
  },
  4: {
    name: 'Was es kostet zu bleiben',
    bau: `Die einzige Fassung, die rechnet. Hook ist eine Frage mit
Zahl: "Was kostet dich ein Monat ohne Angebotsseite?"

Dann die Rechnung, drei bis vier Zeilen, in ihren Groessen. Anfragen
mal Abschlussquote mal Preis. Konservativ schaetzen und das dazusagen.

Dann die Gegenrechnung: was die Umstellung kostet, an Zeit und an Geld.

Kein Druck, kein Countdown, keine Verknappung. Die Zahlen stehen
nebeneinander, die Leserin zieht den Schluss.

Angebot, letzter Schlag, Qualifizierung, CTA.`,
  },
  5: {
    name: 'Die Nachricht',
    bau: `Beginne mit einer echten Nachricht, die Carina bekommen hat,
in Anfuehrungszeichen und als eigener Block. Eine Frage oder ein
Einwand.

Dann die Antwort, die sie tatsaechlich gegeben haette — direkt, ohne
Hoeflichkeitsfloskel, ohne "gute Frage".

Dann eine Zeile, warum diese Frage so oft kommt. Das ist die Stelle,
an der die Leserin sich wiedererkennt.

Diese Fassung bleibt kurz. Hoechstens zwoelf Zeilen bis zum Angebot.

Angebot, letzter Schlag, Qualifizierung, CTA.`,
  },
  6: {
    name: 'Von damals',
    bau: `Carina stand da, wo die Leserin gerade steht. Beginne mit
einer Szene, nicht mit einer Erkenntnis:
  "Zehn Gruendungen. Bei sechs davon habe ich den Preis erst im
  Gespraech genannt."

Dann was daran nicht funktioniert hat. Konkret, ohne Selbstmitleid und
ohne Heldenerzaehlung.

Dann die EINE Sache, die sie geaendert hat. Eine, nicht drei.

Dann was danach anders war. Belegbar oder gar nicht.

Kein "und heute helfe ich Frauen dabei". Die Bruecke zum Angebot
passiert im naechsten Absatz von selbst.

Angebot, letzter Schlag, Qualifizierung, CTA.`,
  },
  7: {
    name: 'Kurz',
    bau: `Fuer Tage, an denen die Folien schon alles sagen. Die
gesamte Caption hat hoechstens acht Zeilen.

Eine Behauptung. Eine Folge. Ein Angebotssatz mit Preis. Ein Ergebnis.
Der CTA.

Keine Erklaerung, kein Beispiel, kein Beweis. Wer mehr will, liest die
Folien. Diese Fassung darf sich unhoeflich kurz anfuehlen.`,
  },
  8: {
    name: 'Serie — ein Schritt von dreissig',
    bau: `Fuer die laufende Serie. Kein Verkauf, keine Qualifizierung.

Erste Zeile: "Schritt X von 30:" und dahinter eine Behauptung, der man
widersprechen moechte. Kein Thema, keine Ueberschrift.
  gut   "Schritt 12 von 30: Der Preis steht im Post. Oder er steht nicht."
  mies  "Schritt 12 von 30: Preiskommunikation"

Dann in drei bis vier Zeilen, was an diesem einen Schritt haengt.
Konkret genug, dass sie ihn heute machen kann, ohne die anderen 29.

Dann Gestern und Morgen, immer inhaltlich, nie "Teil 12 von 30":
  "Gestern ging es darum, warum dein Angebot drei Versprechen gibt
  statt einem. Morgen kommt die Zeile direkt nach dem Preis."
Ist kein Vortag bekannt, nur der Ausblick. Ist kein Folgetag bekannt,
nur der Rueckblick. Nie beides erfinden.

Dann das Ergebnis nach allen dreissig Schritten, als Szene.

Dann: "Kommentiere DABEI, dann bekommst du die naechsten Schritte."
Nichts sonst.`,
  },
};


export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let monday = false, day = null, keyword = '', bauplan = 0, ziel = 2;
  let stilreferenz = '';
  try {
    const body = await req.json();
    day = body.day || null;
    monday = body.monday === true;
    keyword = String(body.keyword || '').trim().slice(0, 24);
    bauplan = [1, 2, 3, 4, 5, 6, 7, 8].includes(Number(body.bauplan)) ? Number(body.bauplan) : 0;
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
    : bauplan
      ? `CTA: "Kommentiere ${ZIELE[ziel].cta}"`
      : 'CTA: die Frage auf die Liste ("Was davon triggert dich am meisten? 1–N in die Kommentare.")';

  const prompt = `${monday ? 'SCHREIBE IM MONDAY-TON — die Regeln dazu stehen unten.\n\n' : ''}${REGELN}
${bauplan ? ZIELE[ziel].block : ''}
${stilreferenz ? `STILREFERENZ — nur die Machart, nie den Inhalt uebernehmen:\n---\n${stilreferenz}\n---` : ''}
${VOICE_BLOCK}
${bauplan ? `DEIN BAUPLAN — ${BAUPLAENE[bauplan].name}\n${BAUPLAENE[bauplan].bau}` : ''}

DER POST — Tag ${day.day}${day.title ? `: ${day.title}` : ''}
${folien}

${ctaZeile}

Schreibe die Caption. Sie muss in den ersten drei Zeilen erkennbar an
einem Satz aus dem Content Piece andocken und danach genau eine Sache
bringen, die dort nicht steht. Keine Zusammenfassung, keine
Wegbeschreibung.
${bauplan && ziel !== 1 && bauplan !== 8 ? 'Die Qualifizierung MUSS vorkommen, und sie geht ueber die Haltung:\nnicht fuer die, die nicht umsetzen, nicht investieren oder an ihrem\nZustand nichts aendern wollen — und nicht fuer die, die glauben, sie\nbekommen das allein hin. Nie daran festmachen, was jemand schon hat.' : ''}

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
