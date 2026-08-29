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
- Keine Hashtags und keine Emojis. Nur wenn ausdrücklich verlangt:
  höchstens #moneymindset #sheo, Emojis dann ganz am Ende.

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

const ARTEN = {
  1: `
ART 1 — CARINA ORIGINAL, DIRECT CALL-OUT

Hook: der erste Satz aus dem Carousel, konfrontativ, in Versalien.
      Beispiel: SIE SAGT: GENAU MEIN THEMA. DANN KAUFT SIE WOANDERS.

Aufbau, in dieser Reihenfolge:
  Hook
  Warum sie nicht kauft — drei bis vier harte Wahrheiten, je eine Zeile
  Der Mechanismus — ein Post, ein Job
  Das Angebot — 97 Euro im Monat, was sie mitbringt, was sie bekommt
  Der letzte Schlag — ein Ergebnis, kein Kleingedrucktes
  Qualifizierung — fuer wen es NICHT ist
  CTA — Schreib mir MOVE

Sprache: Du, aktiv, Praesens. Saetze wie "Das haelt dich in der
Kategorie Option-fuer-spaeter." oder "Du erklaerst zu Tode."
Verboten: "In diesem Post zeige ich dir", Aufzaehlungen mit Emojis,
Zusammenfassungen des Carousels. Verdichten, nicht nacherzaehlen.
Keine Hashtags.`,

  2: `
ART 2 — LISA BISSCHOP, SOFT EDUCATIONAL

Hook als Frage:
  "Warum schreibt dir deine Traumkundin 'total mein Thema' und bucht
   dann woanders?"

Framing: Das ist ein Content-Problem, kein Charakterproblem. Sie kann
verkaufen. Ihre Posts schliessen nur keinen Job.

Aufbau:
  Relatable Intro — "Das sehe ich gerade bei vielen ..."
  Drei bis fuenf Punkte aus dem Carousel als Liste
  Die Loesung als Konzept — jeder Post hat einen Job
  Weiches Angebot
  Community-CTA — "Speicher dir das ab. Welcher Punkt trifft dich?"

Sprache: wir, weicher, erklaerend, einladend. Mehr Erklaerung als in
Art 1. Kein DM-Druck. Hoechstens drei Hashtags am Ende.`,

  3: `
ART 3 — US-SALES, KURZ UND PITCH

Hook in Versalien, englisch oder denglisch:
  YOUR CONTENT IS NOT THE PROBLEM. YOUR MESSAGE IS.

Aufbau:
  Hook
  Drei Fehler als Liste, jeder Punkt beginnt mit einem Kreuz-Zeichen
  Ein Satz Mechanismus
  Mini-Case — 6k auf 12k, Einzelfall
  CTA mit Keyword

Sprache: sehr kurz, punchy, viel Zeilenumbruch. Denglisch erlaubt.`,
};

const STORY_ANLEITUNG = `
FUENF STORIES ZUM POST — immer genau diese fuenf, in dieser Reihenfolge:

1  Call-Out
   Schwarzer Grund, weisse Schrift. EIN Satz aus Folie 1.
   Dazu eine Umfrage: Ertappt? Ja / Nein

2  Mechanismus
   Erklaere "ein Post, ein Job" an EINER Frage, zum Beispiel
   "Bin ich gemeint?", und zeige an einem Beispiel, wie ein Post sie
   schliesst. Sticker: Frag mich.

3  Behind / Mindset
   Kurze persoenliche Anekdote zum Gedanken aus Folie 3. Nahbar,
   konkrete Uhrzeit, konkrete Situation.

4  Beweis
   "Gleiches Angebot. Neue erste drei Saetze. 6k auf 12k."
   Platzhalter fuer den Screenshot mitschreiben. Disclaimer nicht
   vergessen: Einzelfall, kein Durchschnitt.

5  Sales
   Die letzten beiden Folien direkt. The Money Room, 97 Euro im Monat,
   was sie mitbringt, was sie bekommt, fuer wen ja und fuer wen nicht.
   Schreib MOVE.

Jede Story hoechstens 300 Zeichen. Zeilenumbrueche sind erwuenscht.
`;

const VOICE = {
  1: {
    name: 'Preis-Pause',
    bau: `Hook: "Der Grund, warum du deinen Umsatz fuer ein Persoenlichkeitsproblem haeltst:"
Dann VIER nummerierte Gewohnheiten, jede beginnt mit "Du" und beschreibt
eine Handlung, keine Eigenschaft.
Dann der Dreh: "Du musst nicht X werden. Du musst aufhoeren, Y."
Dann das Angebot mit Preis, der Beweis mit Einzelfall-Hinweis,
dann die Qualifizierung, dann der CTA.`,
  },
  2: {
    name: 'Geboren zum Verkaufen',
    bau: `Hook: "Du bist nicht 'nicht der Verkaufstyp'. Du hast vier Angewohnheiten,
die dich so aussehen lassen."
Vier nummerierte Punkte, jeder eine Handlung.
Dann: "Vierstellig verkaufst du nicht mit neuem Charakter. Sondern wenn du
aufhoerst, Verkaufen fuer Magie zu halten."
Kurzes Angebot, CTA. Diese Fassung bleibt knapp.`,
  },
  3: {
    name: 'Ehrlich',
    bau: `Beginnt mit dem alten Glaubenssatz: "Frueher dachtest du: Ich muss erst
extrovertierter, disziplinierter, schlagfertiger werden."
Dann eine Zeile allein: "Bullshit."
Dann "Du musst:" und VIER Spiegelstriche, jeder beginnt mit "Aufhoeren, ...".
Dann: "Das ist kein Charakter. Das sind vier Gewohnheiten. Und Gewohnheiten
tauscht man aus."
Angebot, Qualifizierung, CTA.`,
  },
  4: {
    name: 'Kurz und fies',
    bau: `Hook: "Du hast kein Mindset-Problem. Du hast ein Gewohnheits-Problem."
Dann "Solange du:" und vier Zeilen in Kleinschreibung, mit Komma getrennt,
die letzte endet auf drei Punkte.
Dann: "wirst du weiter denken, du bist falsch."
Dann zwei kurze Saetze: "Bist du nicht. Du bist nur untrainiert."
Angebot in einer Zeile, CTA. Die kuerzeste Fassung, keine Fuellsaetze.`,
  },
  5: {
    name: 'Launch',
    bau: `Beginnt mit einer Zahl aus ihrem Alltag: "6.000 Euro Launch fuehlt sich
nicht nach 'Ich bin halt introvertiert' an. Es fuehlt sich nach vier falschen
Moves an, die du jeden Tag wiederholst."
Dann der Beweis als Erzaehlung: Kundin dachte, sie muesse ihre Persoenlichkeit
aendern, ging von 6k auf 12k, nachdem EINE Gewohnheit getauscht wurde.
Einzelfall, kein Durchschnitt — dieser Satz MUSS dabeistehen.
Angebot, Qualifizierung, CTA.`,
  },
  6: {
    name: 'Persoenlichkeits-Luege',
    bau: `Hook: "Der teuerste Satz in deinem Business: 'Ich bin halt so.'"
Dann: "Du bist nicht so. Du MACHST so." — das MACHST in Versalien.
Dann vier Zeilen, jede beginnt mit "Du machst ...", von der konkreten
Handlung bis zur letzten: "Du machst aus vier Gewohnheiten eine Identitaet."
Dann: "In THE MONEY ROOM entkoppeln wir das." Preis, CTA.`,
  },
  7: {
    name: 'Alles schon probiert',
    bau: `Drei Zeilen "Du brauchst kein ...", die aufzaehlen, was sie schon
gekauft hat: neues Branding, neues Reading, neuer Charakter.
Dann: "Du brauchst jemanden, der dir sagt: ..." und darin steht die
Aufforderung, die alles kippt.
Dann das Angebot in zwei Saetzen, CTA.
Fuer Leute, die schon zehn Kurse gekauft haben.`,
  },
};

const VOICE_REGELN = `
DIE VOICE-FASSUNGEN

Sieben feste Bauplaene im Sound von Laura Hersche: gleicher Mechanismus,
gleicher Punch. Das Muster ist immer dasselbe —

  Behauptung ueber ihre Persoenlichkeit widerlegen
  -> vier Gewohnheiten benennen, als Handlung, nie als Eigenschaft
  -> der Dreh: nicht werden, sondern aufhoeren
  -> Angebot mit Preis
  -> der letzte Schlag: ein Ergebnis, kein Kleingedrucktes
  -> Qualifizierung
  -> CTA

WAS DIESEN SOUND AUSMACHT
Kurze Zeilen, viele Umbrueche, jede Aussage steht allein. Keine
Ueberleitungen. Zahlen statt Adjektive. "Du" in jeder Zeile. Das Wort
"Gewohnheit" traegt die ganze Caption — sie ist nicht falsch, sie ist
untrainiert.

VERBOTEN in diesen Fassungen: Emojis, Hashtags, Ausrufezeichen,
Zwischenueberschriften, "In diesem Post zeige ich dir".

Vier Punkte heisst VIER. Nicht drei, nicht fuenf.
`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let monday = false, day = null, keyword = '', art = 0, stories = false, voice = 0, ziel = 2;
  try {
    const body = await req.json();
    day = body.day || null;
    monday = body.monday === true;
    keyword = String(body.keyword || '').trim().slice(0, 24);
    art = [1, 2, 3].includes(Number(body.art)) ? Number(body.art) : 0;
    voice = [1, 2, 3, 4, 5, 6, 7].includes(Number(body.voice)) ? Number(body.voice) : 0;
    ziel = [1, 2, 3, 4, 5].includes(Number(body.ziel)) ? Number(body.ziel) : 2;
    stories = body.stories === true;
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
    : (art === 1 || voice)
      ? `CTA: "Kommentiere ${ZIELE[ziel].cta}"`
      : art === 2
        ? 'CTA: Speichern und ein Kommentar — welcher Punkt trifft dich?'
        : art === 3
          ? 'CTA: "Comment MOVE"'
          : 'CTA: die Frage auf die Liste ("Was davon triggert dich am meisten? 1–N in die Kommentare.")';

  const prompt = `${monday ? 'SCHREIBE IM MONDAY-TON — die Regeln dazu stehen unten.\n\n' : ''}${REGELN}
${art || voice ? ZIELE[ziel].block : ''}
${art ? ARTEN[art] : ''}
${voice ? VOICE_REGELN : ''}
${voice ? `DEIN BAUPLAN — ${VOICE[voice].name}\n${VOICE[voice].bau}` : ''}
${stories ? STORY_ANLEITUNG : ''}

DER POST — Tag ${day.day}${day.title ? `: ${day.title}` : ''}
${folien}

${ctaZeile}

Schreibe die Caption. Wiederhole die Folien nicht wörtlich — die Caption
führt den Gedanken weiter und macht ihn anwendbar.
${art || voice ? 'Die Qualifizierung MUSS vorkommen, und sie geht ueber die Haltung:\nnicht fuer die, die nicht umsetzen, nicht investieren oder an ihrem\nZustand nichts aendern wollen — und nicht fuer die, die glauben, sie\nbekommen das allein hin. Nie daran festmachen, was jemand schon hat.' : ''}

ANTWORTE NUR MIT JSON, ohne Vorwort, ohne Markdown:
${stories
  ? '{"caption":"…","stories":[{"titel":"Call-Out","text":"…"},{"titel":"Mechanismus","text":"…"},{"titel":"Behind","text":"…"},{"titel":"Beweis","text":"…"},{"titel":"Sales","text":"…"}]}'
  : '{"caption":"…"}'}
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
    const storyListe = stories && Array.isArray(out.stories)
      ? out.stories
        .map((st) => ({
          titel: String(st?.titel || '').trim().slice(0, 40),
          text: String(st?.text || '').trim(),
        }))
        .filter((st) => st.text)
        .slice(0, 5)
      : [];

    return new Response(JSON.stringify({ caption, laenge: caption.length, stories: storyListe }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
