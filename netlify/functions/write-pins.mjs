// Netlify Function: Pinterest-Hooks fuer Carina — Limitless Selling.
// POST { anzahl, saeule, thema, monday }
//   -> { pins: [{ label, hook, subtext, punkte, beschreibung, saeule, titel, ziel }] }
//
// Das Muster stammt aus einer Analyse von rund 400 Pins einer Kollegin:
// wenige Hooks, viele Varianten, Evergreen. Die BOTSCHAFTEN sind hier aber
// Carinas eigene — nicht abgeschrieben, sondern nach demselben Bauprinzip.

// ZIELE — zu jeder Säule gehört ein Artikel. Der Pin bringt sein Ziel
// gleich mit, damit beim Hochladen nichts zugeordnet werden muss.
const BASIS = 'https://limitlessselling.at';
const ZIELE = {
  frust:       '/wissen/braucht-man-instagram-fuer-ein-online-business.html',
  alternative: '/wissen/kunden-ohne-instagram.html',
  umsetzung:   '/wissen/was-braucht-man-fuer-ein-online-business.html',
  umsatz:      '/wissen/warum-verkauft-sich-mein-angebot-nicht.html',
  mehrwert:    '/wissen/pin-titel-schreiben.html',
};

// Zweitziel je Säule. Damit nicht alle Pins einer Säule auf dieselbe Seite
// zeigen — sonst hängt der ganze Kanal an drei Adressen.
const ZWEITZIELE = {
  frust:       '/wissen/wie-viel-zeit-kostet-social-media.html',
  alternative: '/wissen/label-auf-vinted-starten.html',
  umsetzung:   '/wissen/reihenfolge-online-business-aufbauen.html',
  umsatz:      '/wissen/reihenfolge-online-business-aufbauen.html',
  mehrwert:    '/wissen/ist-pinterest-sinnvoll-fuer-coaches.html',
};

// Wird ein freies Thema gesetzt, passt oft keiner der fünf Säulenartikel.
// Dann darf der Schreiber aus dieser Liste wählen — aber NUR aus ihr:
// ein erfundener Pfad wäre ein toter Link auf einem Pin, der jahrelang
// weiterläuft. Was nicht in der Liste steht, fällt auf die Säule zurück.
const WEITERE_ZIELE = [
  ...Object.values(ZWEITZIELE),
  '/wissen/ist-pinterest-sinnvoll-fuer-coaches.html',
  '/wissen/label-auf-vinted-starten.html',
  '/wissen/muss-ich-eine-personenmarke-aufbauen.html',
  '/wissen/verkaufsgespraech-ohne-ueberreden.html',
  '/wissen/reihenfolge-online-business-aufbauen.html',
  '/wissen/pin-titel-schreiben.html',
];

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

Du schreibst Pinterest-Pins für Carina von LIMITLESS SELLING (limitlessselling.at).

WORUM ES GEHT — der Kern, alles andere haengt daran:
Carina von Limitless Selling zeigt, dass man für ein Online-Business nicht
online LEBEN muss. Kein Instagram, kein TikTok, kein tägliches Posten.
Verkauft wird dort, wo Menschen ohnehin SUCHEN UND KAUFEN — über Suche,
über Pinterest, über Marktplätze.

Der Satz, um den alles kreist:

    Du musst nicht online leben, um online zu verkaufen.

ZAHLEN UND ERGEBNISSE
Zahlen machen einen Pin konkret und sind erwünscht. Ergebnisversprechen
sind erlaubt — mit EINER Bedingung:

  ERFINDE NIEMALS EINE ZAHL.
  Du weißt nicht, was Carina verdient, wie viele Kundinnen sie hat oder
  wie lange etwas gedauert hat. Ein Pin läuft jahrelang weiter und muss
  belegbar sein. Eine ausgedachte Zahl auf so einem Pin ist kein Detail,
  das man später korrigiert.

  Zahlen dürfen NUR aus den BELEGEN unten stammen. Stehen dort keine,
  schreib den Pin ohne Zahl — er funktioniert auch so.

Weiterhin gilt: Wenn du eine Zahl nennst, sag dazu, WESSEN Zahl es ist.
"Sechs Verkäufe auf Vinted, bevor mich jemand kannte" gehört Carina.
"Sechs Verkäufe in deiner ersten Woche" ist eine Zusage an eine Fremde.

FÜR WEN:
Frauen, die SCHON ein Offer haben und SCHON Kundinnen hatten, und deren
Zufluss abgerissen ist. Keine Anfängerinnen. Schreibe NIE so, als stünde
die Leserin am Anfang: kein "erste Kundin gewinnen", kein "endlich
loslegen", kein "durchstarten", nichts, was nach noch kein Business
klingt. Sie hat eins. Es verkauft gerade nur nicht.

DIE ANGEBOTE:
  Found Not Followed — Der Bauplan, 47 € (The Limitless Files 02).
  Das Hauptangebot. Der Name kommt in keinem Pin vor: ein Pin führt auf
  einen Artikel, nicht auf das Offer.
  Telegram-Kurse sind in Vorbereitung.
  1:1 gibt es nur als Warteliste.

WIE EIN PIN GEBAUT IST — drei Teile, mehr nicht:
  LABEL    2–4 Wörter, GROSSBUCHSTABEN, klein gesetzt. Ordnet ein.
           z. B. "OHNE PREISLEITER", "FÜR DIE FRAU", "ANGEBOT STATT REICHWEITE"
  HOOK     Der Satz, der trägt. 4–12 Wörter. Eine Behauptung oder ein
           Widerspruch, kein Ratschlag. Das ist 80 % des Pins.
           Setze EIN oder ZWEI Wörter in *Sternchen* — sie werden farbig
           hervorgehoben. Betone das Wort, an dem der Satz kippt, nicht das
           lauteste: "Meine Kleider habe ich auf *Vinted* verkauft."

           JEDER PIN TRIFFT AUF EINE KALTE LESERIN.
           Sie kennt Carina nicht. Sie kennt die Denkweise nicht. Sie hat
           zwei Sekunden. Was sie sucht, ist nicht eine kluge Sicht auf
           Marketing — sie hat gerade ein Problem und will wissen, ob hier
           jemand davon spricht.

           ALSO: SAG DAS PROBLEM. Nicht das Bild dafür.
           Der Hook beschreibt eine Lage, die sie aus IHRER Woche kennt.
           Etwas, das sie diese Woche getan oder nicht bekommen hat:
             "Du postest seit sechs Monaten. Niemand fragt nach dem *Preis*."
             "Dein Kalender ist leer und dein Feed ist voll."
             "Zweihundert Likes. *Null* Anfragen."
             "Du hast Kundinnen gehabt. Jetzt kommt nichts mehr nach."
             "Du erklärst dein Angebot zum vierten Mal und keine kauft."

           VERGLEICHE MIT FREMDEN WELTEN SIND VERBOTEN.
             falsch  "Instagram ist ein Café, kein Einkaufszentrum."
             falsch  "Bei IKEA würdest du das auch nicht machen."
             falsch  "Du tanzt auf Instagram, aber sie kaufen bei Google."
           Diese Sätze sind gut gebaut und funktionieren — bei jemandem,
           der Carina schon folgt und ihrer Argumentation folgen WILL.
           Eine kalte Leserin muss erst den Vergleich verstehen, dann ihn
           auf sich übertragen. Dafür hat sie die Sekunden nicht. Ein Pin
           auf Pinterest hat kein Publikum im Rücken, das mitdenkt.

           VERBOTEN, weil es die Sätze weich macht:
             - "X bringt mehr als Y" und jede andere Mengenvergleichsformel
             - Abstrakta als Subjekt: Sichtbarkeit, Reach, Erfolg,
               Marketing, Content. Das Subjekt ist SIE oder etwas aus
               ihrem Alltag.
             - "Es geht nicht um X, sondern um Y" als ganze Aussage
             - Fragen. Der Hook behauptet.
             - Metaphern, Analogien, Gleichnisse jeder Art.

           PRÜFUNG vor der Ausgabe, zwei Fragen:
           1. Würde eine Frau, die noch nie von Carina gehört hat, hier
              ihre eigene Woche wiedererkennen? Wenn sie erst nachdenken
              muss, ist der Satz zu klug.
           2. Könnte der Satz genauso von einer beliebigen anderen Coachin
              stammen? Dann ist er zu allgemein.
           Schreib innerlich drei Fassungen und gib die aus, die am
           direktesten sagt, was gerade nicht funktioniert.
  SUBTEXT  Ein kurzer Satz, der den Hook erdet. Höchstens 12 Wörter.
           Darf auch fehlen (dann leer lassen).

SÄULEN — halte dich an die gewünschte, sonst mische:
  frust        DAS PROBLEM BENENNEN. Der Pin sagt, was gerade nicht
               funktioniert — und LÖST ES NICHT. Sie erkennt sich wieder
               und will wissen, warum. Behauptung, Widerspruch,
               Beobachtung. Nie ein Ratschlag.
               "Zweihundert Likes auf den Post. Keine einzige Anfrage."
               "Sechs Monate gepostet. Keine Anfrage über deine Storys."

  alternative  DASS ES ANDERS GEHT. Der Pin zeigt, dass es einen anderen
               Weg gibt, OHNE ihn zu erklären. Hier gehört der Beweis
               hinein: Carina hat ihre KLEIDER auf VINTED verkauft, ohne
               Aufbau, ohne Aufwärmphase. Artikel, die seit Jahren
               Kundinnen bringen. Sie sucht keine Schuld mehr, sie sucht
               einen Ersatz.
               "Ein Artikel von vor zwei Jahren bringt immer noch Kundinnen."
               "Meine Kleider habe ich auf Vinted verkauft. Nicht auf Instagram."

  umsetzung    WAS STATTDESSEN GEBAUT WIRD. Konkret: Reihenfolge,
               Bausteine, was zuerst kommt. Sie hat entschieden und will
               wissen, wie.
               "Frauen mit Kaufabsicht nutzen die Suche."
               "Erst der Artikel, dann der Pin. Nicht umgekehrt."

               Hierhin gehört auch, WIE Leute auf die Seite kommen —
               Pins, Artikel, Suchbegriffe, Menge und Regelmäßigkeit.
               Das ist die Frage hinter allem: nicht "wie werde ich
               sichtbar", sondern "wie findet mich jemand, der gerade
               sucht".
               "Vierzig Pins an einem Nachmittag. Danach arbeiten sie
                allein."
               "Ein Artikel, zehn Pins. Das ist die ganze Mechanik."

  umsatz       WAS DABEI HERAUSKOMMT — als offene Rechnung.
               Der Pin zeigt, wie sich das rechnet: Menge, Preis,
               Zeitraum. Nie nur das Ergebnis, nie als Zusage. Die Zahlen
               stehen unter BELEGEN und werden von dort genommen, nicht
               ausgedacht. Der Subtext kennzeichnet die Rechnung.
               "Zwei Verkäufe am Tag, 47 € das Stück. Macht 2.820 € im Monat."
               Subtext dazu: "Beispielrechnung, kein Versprechen."
               Sie will wissen, ob sich der Aufwand lohnt.

  mehrwert     DER EINE, DER VOLL UMSETZBAR IST.
               Diese Saeule ist der geplante Bruch der Nicht-beraten-Regel
               — einer von sechs Pins. Hier steht die Umsetzung wirklich
               da, und zwar so, dass sie es HEUTE machen kann.

               Ziel ist genau dieser Satz in ihrem Kopf: "Oh mein Gott,
               das koennte ich jetzt echt machen."

               Konkret heisst: mit Zahl, mit Reihenfolge, mit dem Wort,
               das sie tippen soll. Nicht "sei strategisch", sondern
               "schreib in die Beschreibung den Satz, den sie ins
               Suchfeld tippt".

               Das Feld "punkte" darf hier gefuellt werden — drei bis
               fuenf kurze Schritte. In allen anderen Saeulen bleibt es
               leer.

               ALLE ANDEREN SAEULEN geben nur den Impuls. Diese eine
               nicht. Das ist der Unterschied, und er ist Absicht.

WARUM PHASEN UND NICHT THEMEN
Das Thema ist über alle drei dasselbe: verkaufen, ohne täglich online zu
sein. Unterschiedlich ist, WO die Leserin gerade steht. Die ersten zehn
Pins sprachen alle dieselbe an — die Genervte. Wer genervt ist, nickt und
scrollt weiter. Wer eine Alternative sucht, klickt. Wer umsetzen will,
kauft. Ein Kanal, der nur die erste Phase bedient, sammelt Zustimmung und
keine Kundinnen.

DIE ANREDE "FÜR DIE FRAU, DIE …"
Das ist ein FORMAT, keine Säule. Es passt auf jedes Thema und darf in
jeder Säule vorkommen: "FÜR DIE FRAU, die ein Business will und keine
Personal Brand." Als eigene Säule wäre es Haltung ohne Keyword
dahinter — und danach sucht niemand. Höchstens jeder vierte Pin.

DIE ANDEREN KANAELE — so wird darueber gesprochen
Instagram und TikTok sind nicht schlecht. Sie sind fuer etwas anderes
gebaut. Genau das ist die Aussage, und sie ist nuechtern, nicht empoert.

  Was man dort bekommt: Views. Follower. Kommentare. Das Gefuehl, dass
  etwas laeuft.
  Was man dort selten bekommt: jemanden, der auf die Seite geht und das
  Angebot kauft. Die Conversion ist unterirdisch — nicht weil man es
  falsch macht, sondern weil dort niemand mit Kaufabsicht unterwegs ist.
  Wer scrollt, will sich unterhalten lassen. Wer sucht, will finden.

  Genau diese Luecke ist das Thema: viel Reichweite, kaum Verkaeufe.
  Nicht "Instagram ist schlecht", sondern "Instagram misst etwas
  anderes als das, was du brauchst".

    geht  "Zweitausend Views. Null Klicks auf die Seite."
    geht  "Follower sind kein Publikum mit Kaufabsicht."
    geht  "Auf Instagram misst du Aufmerksamkeit. Bezahlt wird
           Kaufabsicht."
   mies   "Instagram ist Zeitverschwendung."
   mies   "Hoer auf, Reels zu machen."

NICHT JEDER PIN IST EIN BASHING
Hoechstens jeder dritte Pin arbeitet ueberhaupt mit einem Fehler oder
einem Dagegen. Der Rest spricht darueber, was ERREICHT werden soll und
was erreicht wurde:
  "Das ist moeglich."  —  "Das habe ich erreicht."  —  "So sieht es aus,
  wenn es laeuft."
Ein Kanal, der nur dagegen ist, ermuedet. Man folgt jemandem, der
irgendwohin will, nicht jemandem, der gegen etwas ist.


POSITION (Kanon v3 — gilt vor allem anderen)
Carina sieht den naechsten Verkaufsimpuls.

  Claim:        Was ist dein naechster Money-Making Move?
  Mechanismus:  Du sagst mir, was du hast. Ich sage dir, was du diese
                Woche verkaufst.
  Kernsatz:     Du machst den Move, statt ihn zu planen. Und du machst
                Geld, wenn du Geld brauchst.

Der Impuls ist KANALUNABHAENGIG — Pinterest, Instagram, Facebook,
Newsletter. Ueberall geht es darum, das Richtige zu tun, um zu verkaufen.

Pinterest ist Akquisekanal UND Content-Thema, aber unter dem
Impuls-Dach. Pins verkaufen Money-Making Moves und zeigen, wie man das
auf Pinterest macht. "Pinterest Empire" ist NICHT tot — nur nicht mehr
die Positionierung.

Technische Umsetzung (Systeme, Apps, Analytics) bleibt Koennen, aber
HIDDEN. Nicht Content, nicht Frontpage.

DIE NICHT-BERATEN-REGEL — aber NICHT absolut
Wer zu viel beraet, verkauft zu wenig. Gilt als Inhalt und als
Eigenverhalten.

  FUENF von sechs Pins geben den IMPULS, nicht die Anleitung.
  EINER von sechs ist VOLL UMSETZBAR — das "oh mein Gott, das koennte
  ich jetzt echt machen" ist GEPLANT, kein Ausrutscher.

Bei den fuenf gilt: ein Satz, der sitzt, dann Stille. Keine
Schritt-fuer-Schritt-Anleitung, keine "5 Tipps"-Liste.
Bei dem einen darf und soll die Umsetzung dastehen.

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

REGELN
- Du-Form, Präsens. Kurze Sätze.
- Keine Preisleiter-Logik, keine Rabatte, kein "günstiger".
- Nicht gegen Mindset-Arbeit — Carinas Arbeit liegt davor, am Offer.
- Zahlen nur aus den BELEGEN, und nur als offene Rechnung mit
  Kennzeichnung im Subtext. Nie als Zusage an die Leserin, nie mit Frist.
- Keine Emojis, keine Hashtags. Ein Pin ist eine Behauptung, kein Post.
- Kein Schimpfen über Instagram. Die Aussage ist: es ist nicht der Ort,
  an dem gekauft wird — nicht, dass es schlecht sei.
- Kein garantiertes Ergebnis für die Leserin, keine Frist ("in 30 Tagen"),
  keine Verdopplung.

TITEL FÜR PINTEREST (Suche)
Zu jedem Pin ein Titel mit Keywords, 40–70 Zeichen. Der Titel ist die
Ausnahme vom Ton: hier steht, was jemand ins Suchfeld tippt, nicht wie
Carina spricht. "Online Business ohne Instagram aufbauen" — nicht "Wie
ich mein Business ohne Insta aufgebaut hab". Nüchtern, ohne Ich-Form,
ohne Verkürzungen. Die Persönlichkeit steckt im Pin und in der
Beschreibung, nicht im Titel.
Diese Liste bleibt DEUTSCH: es sind Suchbegriffe, keine Pin-Sprache.
Danach wird getippt. Im Pin selbst gilt die Sprache der Szene — Offer,
Reach, Personal Brand, Content, Keyword — im Titel und in den Begriffen
steht, was Menschen wirklich ins Suchfeld schreiben.

Brauchbare Begriffe:
  Online Business ohne Instagram, Business ohne Social Media,
  Business ohne täglich posten, Pinterest Marketing für Coaches,
  Angebot verkauft sich nicht, Kunden ohne Instagram,
  Personal Brand oder Business, auf Vinted verkaufen,
  Verkaufsgespräch führen, Online-Business ohne TikTok
`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({ error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).' }), { status: 500 });
  }

  let monday = false, anzahl = 10, saeule = 'mix', thema = '', belege = '';
  // GEWICHTUNG 25 / 40 / 35.
  // Nicht gleichverteilt: die ersten Pins waren zu zehnt "frust", die
  // anderen beiden Phasen fehlen fast ganz. Der Rest aus der Division
  // geht an "alternative", weil dort die groesste Luecke ist.
  try {
    const body = await req.json();
    anzahl = Math.min(Math.max(parseInt(body.anzahl, 10) || 10, 3), 20);
    monday = body.monday === true;
    saeule = String(body.saeule || 'mix');
    belege = String(body.belege || '').slice(0, 800);
    thema = String(body.thema || '').trim().slice(0, 500);
  } catch { /* Standardwerte */ }

  const verteilung = (() => {
    // Fuenf Saeulen mit festen Anteilen. "mehrwert" traegt am meisten: er
    // ist der einzige Pin, der auch dann etwas bringt, wenn niemand
    // klickt — und der Grund, warum jemand ein zweites Mal stehenbleibt.
    // "umsatz" bleibt unter einem Fuenftel, sonst wird aus der Marke ein
    // Verkaufsprospekt.
    const anteile = [
      ['mehrwert', 0.30], ['alternative', 0.25], ['frust', 0.15],
      ['umsetzung', 0.15], ['umsatz', 0.15],
    ];
    // Abrunden und den Rest REIHUM verteilen, nicht alles auf eine Saeule.
    // Vorher landete der ganze Rest bei "alternative" — bei fuenf Pins
    // waren das vier von fuenf, und drei Saeulen kamen gar nicht vor.
    const teile = anteile.map(([name, q]) => [name, Math.floor(anzahl * q)]);
    let rest = anzahl - teile.reduce((sum, [, n]) => sum + n, 0);
    for (let i = 0; rest > 0; i = (i + 1) % teile.length, rest--) teile[i][1] += 1;
    return Object.fromEntries(teile);
  })();

  const tonzusatz = monday
    ? '\n\nSCHREIBE IN DER TONLAGE "MONDAY" (siehe oben). Sie gilt fuer den ganzen Text.'
    : '';
  const prompt = `${monday ? 'SCHREIBE IM MONDAY-TON — die Regeln dazu stehen unten.\n\n' : ''}${STIMME}

${thema ? `THEMA, um das es gehen soll:\n${thema}\n` : ''}
Säule: ${saeule === 'mix' ? `gemischt, und zwar GENAU SO VIELE je Säule:
  frust        ${verteilung.frust}
  alternative  ${verteilung.alternative}
  umsetzung    ${verteilung.umsetzung}
  umsatz       ${verteilung.umsatz}
  mehrwert     ${verteilung.mehrwert}
Diese Zahlen sind verbindlich, nicht ungefähr. "frust" ist schon reichlich
vorhanden — deshalb der kleinere Anteil.` : saeule}

Schreibe ${anzahl} Pins. Jeder trägt EINEN Gedanken. Keine zwei Pins mit
derselben Aussage in anderen Worten.

FELDER:
  label    zwei bis vier Wörter, Versalien-Vorzeile.
           RECHTSCHREIBUNG PRÜFEN. Das Label wird in GROSSBUCHSTABEN
           gesetzt — dort fällt ein Fehler doppelt auf und steht dann
           jahrelang auf einem Pin. Umlaute ausschreiben: STÄNDIGES,
           nicht STANDIGES. Und nur Wörter, die es gibt: "Tretmühle",
           nicht "Tretmole". Im Zweifel ein einfacheres Wort nehmen.
  hook     die Aussage. Ein bis zwei Sätze. EIN Wort in *Sternchen* für die
           Betonung — nicht mehr, sonst trägt keins.
  subtext  EINE Zeile, die die Aussage erdet. Höchstens 12 Wörter.
           Kein Fließtext, keine Aufzählung, keine Frage, kein Aufruf.
           Am besten aus Carinas eigener Erfahrung, nicht als Lehrsatz:
             gut  "Hab ich zwei Jahre lang falsch gemacht."
             gut  "Bei mir war's der Ort, nicht der Content."
            mies  "Sichtbarkeit allein führt zu keinem Verkauf."
           Der Lehrsatz stimmt und sagt nichts. Der eigene Satz sagt,
           dass da jemand ist, dem es genauso ging.
  punkte   NUR bei der Säule "mehrwert": drei bis fünf kurze Punkte als
           Liste. Jeder ein Satz ohne Nebensatz, höchstens 9 Wörter.
           Bei allen anderen Säulen: leer lassen.
  beschreibung
           Zwei bis drei Sätze, 150–300 Zeichen. Sie muss ZWEI Dinge auf
           einmal: von Carina erzählen UND die Wörter enthalten, nach
           denen gesucht wird.

           SCHREIB SIE IN DER ICH-FORM. Carina erzählt, was SIE gemacht
           hat — nicht, was man tun sollte. Kein Ratgeber-Ton, kein
           "Du solltest", kein "Viele Frauen kennen das".

             gut  "Ich hab meine Kleider auf Vinted verkauft, ohne einen
                   einzigen Post. Seitdem bau ich mein Online Business
                   ohne Instagram — über Suche statt über Reichweite."
             gut  "Ich hab jahrelang täglich gepostet und mich gewundert,
                   warum keine Anfragen kommen. Was bei mir wirklich
                   Kundinnen gebracht hat, war Pinterest Marketing."
            mies  "Viele Coaches setzen zu sehr auf Instagram. Erfahre,
                   wie du auch ohne Social Media Kunden gewinnst."

           Der Unterschied: die guten sagen, was passiert IST. Die miese
           sagt, was man tun sollte — und klingt wie jede andere.

           Der Ton ist derselbe wie im Hook: gesprochen, verkürzt
           ("ich hab", "ich bin"), keine Vollformen, wo man kürzt.
           Selbstironie über die eigene Instagram-Zeit ist gern gesehen.

           Die Suchwörter müssen trotzdem drin sein, aber IM SATZ, nicht
           angehängt: "Online Business ohne Instagram", "Kunden ohne
           Social Media", "Pinterest Marketing". Pinterest erkennt
           Keyword-Stapel und wertet sie ab — ein echter Satz mit den
           Wörtern darin schlägt eine Liste immer.

           Keine Hashtags, keine Emojis, kein "Klick hier", keine
           Sternchen, keine Frage am Ende.

${belege ? `BELEGE — von Carina selbst. NUR aus dieser Liste dürfen Zahlen,
Beträge und Zeitangaben in die Pins kommen:
${belege}
` : `BELEGE — fest hinterlegt, damit nichts eingetippt werden muss.
NUR diese Zahlen sind erlaubt. Alles andere bleibt ohne Zahl.

  Preis des Angebots: 47 €.

  DIE OFFENE RECHNUNG. Du baust sie selbst aus diesen Zeilen — sie sind
  nachgerechnet und stimmen. Rechne NICHT selbst, nimm eine Zeile:
    3 Verkäufe pro Woche  = 12 × 47 =   564 € im Monat
    20 Verkäufe im Monat  = 20 × 47 =   940 € im Monat
    1 Verkauf am Tag      = 30 × 47 = 1.410 € im Monat
    40 Verkäufe im Monat  = 40 × 47 = 1.880 € im Monat
    2 Verkäufe am Tag     = 60 × 47 = 2.820 € im Monat

  Aufwand, aus dem Studio selbst: 10 Pins je Durchlauf, 40 Pins an
  einem Nachmittag.

  So gehört eine Rechnung in den Pin — beides zusammen, nie nur das
  Ergebnis:
    HOOK     "Zwei Verkäufe am Tag, 47 € das Stück. Macht 2.820 € im Monat."
    SUBTEXT  "Beispielrechnung, kein Versprechen."
  Genau so steht es auch auf der Website.

    geht nicht  "So verdienst du 2.820 € im Monat."   (Zusage)
    geht nicht  "2.820 € in 30 Tagen."                (Frist)
    geht nicht  jede Zahl, die oben nicht steht.

  HÖCHSTENS JEDER FÜNFTE PIN trägt eine Rechnung. Sonst wird aus der
  Marke ein Verkaufsprospekt.

  ZU VINTED GIBT ES KEINE ZAHLEN. Der Beleg ist, DASS es ohne Publikum
  ging, nicht wie viel: "Meine Kleider haben sich verkauft, bevor mich
  jemand kannte." Erfinde dort niemals Stückzahlen oder Beträge.
`}
${thema ? `ZIEL-ARTIKEL: Gib zu jedem Pin ein Feld "ziel" mit GENAU EINEM
dieser Pfade an, wenn einer inhaltlich passt. Erfinde keinen Pfad. Passt
keiner, lass das Feld weg — dann wird der Artikel der Säule genommen.
${WEITERE_ZIELE.join('\n')}
` : ''}
ANTWORTE NUR MIT JSON, ohne Vorwort, ohne Markdown:
{"pins":[{"label":"…","hook":"…","subtext":"…","punkte":["…","…"],"beschreibung":"…","saeule":"frust|alternative|umsetzung|umsatz|mehrwert","titel":"…"}]}${tonzusatz}`;

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
            generationConfig: { temperature: 1.0, responseMimeType: 'application/json' },
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
    const pins = (out && Array.isArray(out.pins) ? out.pins : [])
      .filter((p) => p && p.hook)
      .map((p) => ({
        label: String(p.label || '').toUpperCase().slice(0, 40),
        hook: String(p.hook || '').slice(0, 160),
        subtext: String(p.subtext || '').slice(0, 120),
        // Hoechstens fuenf Punkte, jeder gekuerzt — sonst passt der
        // Merkzettel nicht mehr auf den Pin.
        punkte: Array.isArray(p.punkte)
          ? p.punkte.filter(Boolean).slice(0, 5).map((x) => String(x).slice(0, 70))
          : [],
        saeule: ZIELE[String(p.saeule)] ? String(p.saeule) : 'angebot',
        titel: String(p.titel || '').slice(0, 100),
        // Pinterest kappt bei 500; unter 300 bleibt sie ganz sichtbar.
        beschreibung: String(p.beschreibung || '').replace(/[*#]/g, '').slice(0, 480),
        // Ein selbst gewaehlter Pfad gilt nur, wenn er wirklich existiert.
        ziel: BASIS + (WEITERE_ZIELE.includes(String(p.ziel || ''))
          ? String(p.ziel)
          : (ZIELE[String(p.saeule)] || ZIELE.alternative)),
      }));
    if (!pins.length) {
      return new Response(JSON.stringify({ error: 'Keine Pins erhalten. Nochmal versuchen.' }), { status: 502 });
    }
    return new Response(JSON.stringify({ pins }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e?.message || e) }), { status: 500 });
  }
};
