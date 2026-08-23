/**
 * REMINDER-FOLIEN SCHREIBEN.
 *
 * Diese Folien sind ZUSATZ: Sie kommen zum Bulk-Import dazu, koennen
 * gepostet werden, muessen aber nicht. Deshalb entstehen sie getrennt
 * von den Karussells und tragen die Kennzeichnung "optional".
 *
 * ACHT Fassungen, jede mit einer HARTEN Laengengrenze — die Grenzen
 * kommen aus dem Zeichner, nicht aus dem Geschmack. Passt der Text
 * nicht, faellt die Kachel auf die schlichte Karte zurueck.
 *
 *   zitat   140   linie  60   wieder  22   zettel 110
 *   notiz    90   merken 80   zwei   2x55  aussage 28+70
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
DIE ACHT FASSUNGEN UND IHRE GRENZEN

zitat   BIS 140 ZEICHEN. Ein Satz mit Haltung, der auch allein steht.
        Wird mit Anfuehrungszeichen und "— Carina Anna Prav" gesetzt.
        Beispiel: Du brauchst keine Money-Making Energy. Du brauchst
        einen Verkaufsprozess.

linie   BIS 60 ZEICHEN. Zwei sehr kurze Saetze, mittig, in Versalien.
        Der zweite kippt den ersten.
        Beispiel: Family > Business. Always.

wieder  BIS 22 ZEICHEN, EINE Zeile, hoechstens drei Woerter. Sie wird
        VIERMAL untereinander gesetzt und verblasst nach unten.
        Beispiel: Less is MORE

zettel  BIS 110 ZEICHEN. Notizzettel mit Klebestreifen. Klingt wie eine
        Notiz an sich selbst, nicht wie eine Ansage ans Publikum.
        Beispiel: Freiheit ist kein Privileg. Freiheit ist eine
        Entscheidung.

notiz   BIS 90 ZEICHEN. Sieht aus wie ein Screenshot aus der Notizen-App.
        Trocken, beilaeufig, ohne Pathos.
        Beispiel: Manifestieren bringt keine Kunden. Systeme schon.

merken  BIS 80 ZEICHEN. Steht unter der Kopfzeile "HEUTE MERKEN", also
        ein Satz zum Mitnehmen, fett gesetzt.
        Beispiel: Mehr Stunden loesen keine strukturellen Probleme.

zwei    ZWEI TEILE, getrennt durch |, jeder Teil bis 55 Zeichen. Der
        erste steht fett, der zweite leise darunter und dreht ihn.
        Beispiel: Ich sage dir, was du hoeren musst.|Nicht was du hoeren willst.

aussage ZWEI TEILE, getrennt durch |. Teil 1 bis 28 Zeichen, wird RIESIG
        gesetzt. Teil 2 bis 70 Zeichen, kleine Unterzeile.
        Beispiel: Weniger ist mehr|Fuenf Stunden Fokus schlagen vierzig Stunden Chaos.

WAS EIN JA AUSLOEST
Nenne einen konkreten Moment, den sie diese Woche hatte. Eine Uhrzeit,
ein Tab, ein Entwurf, eine ungesendete Nachricht. Je genauer die Szene,
desto sicherer das Nicken.
VERBOTEN: Mutmach-Saetze, "du bist genug", Manifestieren, Hustle,
Emojis, Hashtags. Kein Beginner-Shaming: sie ist nicht dumm, sie ist
im Leerlauf.

DIE GRENZEN SIND HART. Der Zeichner faellt bei laengerem Text auf eine
schlichte Karte zurueck — die Fassung waere dann weg. Lieber kuerzer.
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

Verteile sie ungefaehr gleichmaessig auf die acht Fassungen.
Kein Text darf seine Grenze ueberschreiten — zaehle die Zeichen.
Bei "zwei" und "aussage" MUSS ein | im Text stehen.

Antworte NUR mit JSON, ohne Vorrede, ohne Backticks:
[{"art":"zitat","text":"..."}, {"art":"aussage","text":"Teil eins|Teil zwei"}]

Erlaubte Werte fuer "art": zitat, linie, wieder, zettel, notiz, merken, zwei, aussage`;

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
      const GRENZEN = {
        zitat: 140, linie: 60, wieder: 22, zettel: 110,
        notiz: 90, merken: 80, zwei: 115, aussage: 100,
      };
      const ZWEITEILIG = { zwei: [55, 55], aussage: [28, 70] };
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
        if (art === 'wieder' && text.split(/\s+/).length > 3) {
          verworfen.push({ art, text, grund: 'mehr als drei Woerter' });
          return;
        }
        if (ZWEITEILIG[art]) {
          const teile = text.split('|').map((t) => t.trim()).filter(Boolean);
          if (teile.length !== 2) {
            verworfen.push({ art, text, grund: 'kein | zwischen den zwei Teilen' });
            return;
          }
          const [maxA, maxB] = ZWEITEILIG[art];
          if (teile[0].length > maxA || teile[1].length > maxB) {
            verworfen.push({
              art, text,
              grund: `Teile ${teile[0].length}/${teile[1].length} statt max ${maxA}/${maxB}`,
            });
            return;
          }
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
