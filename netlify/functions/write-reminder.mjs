/**
 * REMINDER-FOLIEN SCHREIBEN.
 *
 * Diese Folien sind ZUSATZ: Sie kommen zum Bulk-Import dazu, koennen
 * gepostet werden, muessen aber nicht. Deshalb entstehen sie getrennt
 * von den Karussells und tragen die Kennzeichnung "optional".
 *
 * ZWEI Fassungen, editorial gesetzt, jede mit harter Laengengrenze —
 * die Grenzen kommen aus dem Zeichner, nicht aus dem Geschmack:
 *
 *   zitat    bis 190 Zeichen   heller Grund, grosse Serife, der ruhige Gedanke
 *   aussage  bis  90 Zeichen   dunkler Grund, sehr gross, der harte Satz
 *
 * In jedem Text steht genau ein *Sternchen*-Paar. Das Wort darin wird
 * kursiv gesetzt und traegt die Betonung.
 */

const KANON = `
POSITION (Kanon v3)
Carina sieht den naechsten Verkaufsimpuls.
  Claim:    Was ist dein naechster Money-Making Move?
  Kernsatz: Du machst den Move, statt ihn zu planen. Und du machst Geld,
            wenn du Geld brauchst.

DIE NICHT-BERATEN-REGEL
Der Post gibt den IMPULS, nicht die Umsetzung. Ein Satz, der sitzt, dann
Stille. Keine Anleitungen, keine "5 Tipps"-Listen.
PRUEFFRAGE: Koennte sie das jetzt allein umsetzen? Wenn ja, zu viel.

VOICE
Direkt, vierte Wand, Denglisch erlaubt. Liebt Verkaufen, hoerbar.
Kein Beginner-Shaming.
VERBOTEN: Dienstleisterinnen-Hoeflichkeit ("Ich wuerde mich freuen"),
Absicherungsfloskeln ("Das ist natuerlich individuell"), Ratgeber-Ton,
Selbstbewerbung, erfundene Zahlen.

HOOK-REGEL: eine Behauptung oder ein Widerspruch, kein Ratschlag.
`;

const FASSUNGEN = `
ZWEI FASSUNGEN, MEHR NICHT

zitat   BIS 190 ZEICHEN, zwei bis vier Saetze. Steht auf hellem Grund,
        gross in einer Serifenschrift gesetzt, gemischt geschrieben.
        Das ist der lange, ruhige Gedanke — einer, bei dem eine
        Unternehmerin innerlich nickt, bevor sie zu Ende gelesen hat.
        Sie darf ihn sich selbst schicken wollen.
        Beispiel: Du hast diese Woche zwei Angebote nicht rausgeschickt,
        weil sie noch nicht fertig genug waren. Fertig genug gibt es nicht.
        Es gibt nur verschickt oder nicht verschickt.

aussage BIS 90 ZEICHEN, ein bis zwei Saetze. Steht auf dunklem Grund,
        sehr gross gesetzt. Das ist der kurze harte Satz, der allein
        stehen kann und nichts erklaert.
        Beispiel: Kein Move ist auch eine Entscheidung gegen Umsatz.

DAS STERNCHEN
In JEDEM Text steht GENAU EIN Wort oder eine kurze Wendung in
*Sternchen*. Das wird kursiv gesetzt und traegt die Betonung.
Setze es auf das Wort, das den Satz kippt — nicht auf das lauteste.
  Richtig: Fertig genug gibt es *nicht*.
  Falsch:  *Fertig genug* gibt es nicht.

WAS EIN JA AUSLOEST
Nenne einen konkreten Moment, den sie diese Woche hatte. Eine Uhrzeit,
ein Tab, ein Entwurf, eine ungesendete Nachricht. Je genauer die Szene,
desto sicherer das Nicken.
VERBOTEN: Mutmach-Saetze, "du bist genug", Manifestieren, Hustle,
Ausrufezeichen, Anfuehrungszeichen, Emojis, Hashtags.
Kein Beginner-Shaming: sie ist nicht dumm, sie ist im Leerlauf.

DIE GRENZEN SIND HART. Zu langer Text faellt auf eine schlichte Karte
zurueck, dann ist die Fassung weg. Lieber kuerzer.
`;

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response('Nur POST', { status: 405 });
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return new Response(JSON.stringify({
      error: 'GEMINI_API_KEY fehlt (Netlify → Environment variables).',
    }), { status: 500 });
  }

  let anzahl = 16;
  let thema = '';
  try {
    const body = await req.json();
    anzahl = Math.max(1, Math.min(40, Number(body.anzahl) || 16));
    thema = String(body.thema || '').slice(0, 500);
  } catch {
    // Standardwerte behalten.
  }

  const auftrag = `${KANON}
${FASSUNGEN}

AUFTRAG
Schreibe ${anzahl} Reminder-Folien auf Deutsch.
${thema ? `Themenschwerpunkt: ${thema}` : 'Themen frei aus der Position oben.'}

Verteile sie ungefaehr halbe halbe auf die zwei Fassungen.
Kein Text darf seine Grenze ueberschreiten — zaehle die Zeichen.
In jedem Text MUSS genau ein *Sternchen*-Paar stehen.

Antworte NUR mit JSON, ohne Vorrede, ohne Backticks:
[{"art":"zitat","text":"... *Wort* ..."}, {"art":"aussage","text":"... *Wort* ..."}]

Erlaubte Werte fuer "art": zitat, aussage`;

  const MODELLE = ['gemini-2.5-flash', 'gemini-flash-latest'];
  let letzterFehler = '';

  for (const modell of MODELLE) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: auftrag }] }],
            generationConfig: { temperature: 1.0, maxOutputTokens: 6000 },
          }),
        },
      );
      if (!res.ok) { letzterFehler = `HTTP ${res.status}`; continue; }

      const daten = await res.json();
      const roh = daten?.candidates?.[0]?.content?.parts?.[0]?.text || '';
      const sauber = roh.replace(/```json|```/g, '').trim();
      const liste = JSON.parse(sauber);
      if (!Array.isArray(liste)) { letzterFehler = 'Antwort ist keine Liste'; continue; }

      /**
       * NACHPRUEFEN, NICHT VERTRAUEN.
       *
       * Das Modell haelt sich nicht zuverlaessig an Zeichengrenzen. Was
       * zu lang ist, wird hier AUSSORTIERT statt durchgereicht — sonst
       * faellt die Kachel spaeter still auf die schlichte Karte zurueck
       * und niemand weiss, warum.
       */
      const GRENZEN = { zitat: 190, aussage: 90 };
      const geprueft = [];
      const verworfen = [];
      liste.forEach((e) => {
        const art = String(e?.art || '').trim();
        const text = String(e?.text || '').trim();
        if (!GRENZEN[art] || !text) { verworfen.push({ art, text, grund: 'unbekannte Fassung' }); return; }
        if (text.length > GRENZEN[art]) {
          verworfen.push({ art, text, grund: `${text.length} statt max ${GRENZEN[art]} Zeichen` });
          return;
        }
        const sterne = (text.match(/\*/g) || []).length;
        if (sterne !== 2) {
          verworfen.push({ art, text, grund: `${sterne} Sternchen statt genau zwei` });
          return;
        }
        if (/[!"\u201c\u201e\u201d]/.test(text)) {
          verworfen.push({ art, text, grund: 'Ausrufe- oder Anfuehrungszeichen' });
          return;
        }
        geprueft.push({ art, text, optional: true });
      });

      return new Response(JSON.stringify({
        folien: geprueft,
        verworfen,
        modell,
      }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    } catch (e) {
      letzterFehler = e.message;
    }
  }

  return new Response(JSON.stringify({
    error: `Keine Antwort erhalten. Letzter Fehler: ${letzterFehler}`,
  }), { status: 502 });
};
