# Direkt am Bundle geaendert — noch nicht im Quellcode

Diese Aenderungen wurden im gebauten Bundle vorgenommen, weil sie hier
sofort gebraucht wurden. Im Quellcode der Bau-Session stehen sie NICHT.
Jeder neue Drop setzt sie zurueck, bis sie dort nachgezogen sind.

Stand: Bundle `karten67e`.

## Was inzwischen im Quellcode steht

Die Bau-Session hat **1 bis 7 nachgezogen** (Lieferung vom 27. August,
`NACHGEZOGEN.md`). Sie stehen unten weiter drin, weil das Bundle sie
weiterhin nicht mitbringt: solange die Seite nicht aus `src/` gebaut
wird, muessen sie bei jedem Drop nachgetragen werden. Dafuer gibt es
`tools/bundle-patchen.py`.

**Noch nicht im Quellcode:**

- **8, Stationsreihe.** Die Fassung `ablauf` mit `[stationen: …]` gibt es
  in `src/utils/kartenzeichner.js` nicht — dort stehen nur `zitat` und
  `aussage`. Der ganze Kartenzeichner ist im Quellcode aelter als im
  Bundle.
- **7, Pin-Weg.** Der Pin-Zeichner mit `fillStyle` fehlt in `src`
  ebenfalls. Nur der Standardweg ist dort geaendert.

## Eine Bitte an die Bau-Session

Die Korrektur an Punkt 1 wird bei jeder Lieferung wieder herausgenommen.
Sie beantwortet genau die Frage, die in `NACHGEZOGEN.md` als "zu
pruefen" steht: **nein, die Kopfschrift kommt nicht nur ueber
`slide.fontFamily`.** Der Bold-Statement-Stil 1 setzt die Serife
unabhaengig davon, und Warm Editorial ueberschreibt sie hart auf eine
Groteske. Ohne diese Bedingung fehlt der Verlauf bei jedem
Bold-Statement-Post, und bei Warm Editorial steht er zu Unrecht:

    const playfairKopf = !slide.warmEditorial && (
      /Playfair/.test(String(slide.fontFamily || ''))
      || (slide.boldMode === true && slide.boldStyle === 1)
    );

Diese Fassung steht in `src/utils/canvasRenderer.js` auf `main` und ist
die richtige. Bitte beim naechsten Ziehen von `main` uebernehmen, statt
sie zu ersetzen.

---

## 1. Verlauf hinter Playfair auf Foto — deutlich dunkler

Das Tiefen-Overlay, das gesetzt wird, wenn Playfair auf einem Foto liegt.

Vorher:

    colorStops: [
      { offset: 0,   color: "rgba(18,16,14,0.34)" },
      { offset: 0.5, color: "rgba(18,16,14,0.16)" },
      { offset: 1,   color: "rgba(18,16,14,0.40)" },
    ]

Jetzt:

    colorStops: [
      { offset: 0,   color: "rgba(18,16,14,0.82)" },
      { offset: 0.5, color: "rgba(18,16,14,0.58)" },
      { offset: 1,   color: "rgba(18,16,14,0.90)" },
    ]

---

## 2. Weichzeichner — zufaellig statt an einem Schalter

Die Bedingung haengte an einem Flag, das in der Praxis nie griff, deshalb
war nie ein Weichzeichner zu sehen.

Vorher:

    const blurAn = FLAG && (slide.slideIndex || 0) > 0;

Jetzt: ab Folie 2, und dort etwa jedes zweite Bild. Der Keim kommt aus der
Bildadresse, damit dieselbe Folie immer gleich faellt.

    const idx = slide.slideIndex || 0;
    const blurAn = idx > 0 && (() => {
      const s = String(bildUrl || "");
      let h = 0;
      for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 99991;
      return (h + idx * 17) % 100 >= 50;
    })();

Die Staerke bleibt wie gehabt: `Math.max(design.blur || 0, 12)`.

---

## 3. Farbfolien in Fotoposts — rund ein Drittel ab Folie 2

An der Stelle, die entscheidet, ob eine Folie ueberhaupt ein Hintergrund-
bild bekommt (`hatBild`). Faellt sie negativ aus, wird das Bild entfernt
und die Folie erscheint als reine Farbflaeche.

    hatBild = istFotoPost
      && typeof folie.background === "string"
      && folie.background.length > 5
      && (folieNr === 0 || streu(postNr, folieNr) >= 34);

Mit:

    const streu = (a, b) => {
      let h = Math.imul(a ^ 2654435769, 374761393)
            + Math.imul(b ^ 2246822519, 668265263) | 0;
      h = Math.imul(h ^ h >>> 13, 1274126177);
      return ((h ^ h >>> 16) >>> 0) % 100;
    };

`postNr` ist die laufende Nummer des Posts im Contentplan, `folieNr` die
Folie innerhalb des Posts.

WICHTIG: Eine einfache lineare Formel wie `(postNr*73 + folieNr*151) % 100`
reicht hier NICHT. Sie ergibt je Post eine starre Reihe — manche Posts
bekommen dann gar keine Farbfolie, andere strikt jede zweite. Der
Mischschritt oben streut richtig; nachgerechnet ueber 400 Posts: 33 %
Farbfolien, 13 % der Posts ohne eine einzige.

Folie 1 behaelt immer ihr Foto.

---

Ausgenommen sind Posts mit `karte === "ablauf"` oder
`reminderArt === "ablauf"`. Dort stellt Carina das Foto ausdruecklich pro
Post ein — eine Folie, die es dann doch nicht bekommt, liest sich als
Fehler, nicht als Abwechslung.

    && (slideIndex === 0
        || post.karte === "ablauf" || post.reminderArt === "ablauf"
        || mischer(postIndex, slideIndex) >= 34)

## 4. Ersatzwert der Bildanalyse: Mitte -> unten mittig

Scheitert die Analyse (Zeitueberschreitung, Ladefehler, fremdes Bild),
setzte der Ersatzwert die ruhige Zone auf 4 = Mitte. Bei einem Portraet
landet der Text damit im Gesicht.

    quietZone: 7, quietLabel: "bottom-center"   // statt 4 / "center"

## 5. Zone unter dem Gesicht mitmeiden

Gemieden wurde nur die Zone, in der ein Gesicht erkannt wurde. Ein Gesicht
reicht in die Zone darunter (Kinn, Hals) — und die ist sehr gleichmaessig,
wird also gerne als "ruhig" gewaehlt.

    const jx = new Set(faceZones);
    faceZones.forEach(N => { if (N + 3 < 9) jx.add(N + 3) });
    const wahl = jx.size < 9 ? jx : faceZones;   // Notausgang, falls alles voll

## 6. Textspalte endet vor dem Gesicht

Die Textbreite war fest bei 82 Prozent, unabhaengig davon, wo die Person
steht.

    const spalte = faceZones.length ? Math.min(...faceZones.map(z => z % 3)) : -1;
    const breite = ausrichtungLinks
      ? (spalte > 0 ? Math.max(.42, Math.min(.82, spalte / 3 + .08)) : .82)
      : .86;

Bei Gesicht in der linken Spalte bleibt es bei 82 — dort wuerde Schmaelern
nichts bringen, weil der Text links beginnt.

## 7. Sternchen setzt kursiv statt Farbe

`*Wort*` hat je nach Weg gefaerbt statt kursiv zu setzen. Carina will
kursiv, ohne Farbwechsel.

  - Standardweg: `const rr = wort.kursiv && stil.highlight` -> `false`,
    und `fontStyle: stil.kursiv || wort.kursiv ? "italic" : "normal"`
    (vorher stand dort `wort.kursiv && !stil.highlight`, das Wort wurde
    also gerade gesetzt, sobald eine Highlight-Farbe existierte)
  - Pin-Weg: `fillStyle = wort.betont ? akzent : normal` -> immer `normal`
    (zwei Stellen). Die Schriftlage bleibt an `betont`.

Die Handschrift-Karte bleibt unberuehrt: dort bedeutet das Sternchen
kursiv UND unterstrichen, das ist so gewollt.

## 8. Stationsreihe: Beschriftung bleibt im Rahmen und bei ihrem Punkt

Bei acht Etappen standen die Punkte in zwei Reihen bei 28 und 72 Prozent
der Rahmenhoehe, die Beschriftung fest 24 Punkt darunter. Die zweite Reihe
lag damit auf dem unteren Rahmenrand. Ausserdem sassen der erste und der
letzte Text aussen buendig am Rahmen, also sichtbar neben ihrem Punkt.

Jede Reihe bekommt ein eigenes Band, Punkt und Text stehen darin mittig:

    const bandH = bh / reihen;
    const gp = Math.min(c(26), bandH * .40);     // Abstand Punkt -> Text
    const linieY = y + bandH * ri + (bandH - gp) / 2;
    const textY  = linieY + gp;

Damit ist der Abstand oben und unten in jeder Reihe gleich gross.

Die Beschriftung steht mittig unter ihrem Punkt und rueckt nur so weit
herein, wie noetig, statt pauschal an den Rand zu springen:

    const halb = Math.min(gemesseneBreite, MAXB / k * .92) / 2;
    const lx = Math.max(L + c(8) + halb, Math.min(L + MAXB - c(8) - halb, px));

Dazu zwei Kleinigkeiten: die Linie endet kurz hinter dem ersten und dem
letzten Punkt statt quer durch den Rahmen zu laufen, und die Schrift ist
von c(11) auf c(13) gewachsen — dieselbe Groesse wie die Tagesnamen im
Wochenraster, damit sie auf dem Handy lesbar ist.
