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

## 9. Caption Import (neuer Dialog) und ein Absturz im Bulk Import

Im Content Plan gab es einen Knopf "Captions", der stumm `/captions.json`
holte und eintrug. Carina wollte stattdessen einen richtigen Import wie
den Bulk Import. Der Knopf oeffnet jetzt den Dialog `CaptionImport`.

Der Dialog steht als eigene Komponente in `tools/caption-import.js` und
wird von `tools/caption-import-einbauen.py` vor `AblaufMenue` eingesetzt.
Wer das Bundle neu baut, braucht im Quellcode:

  - Komponente `CaptionImport({isOpen, onClose, onImport})` — Textfeld,
    zwei Modi ("Überschreiben" / "Nur leere füllen"), ein Knopf
    "Aus captions.json laden" (fuellt das Textfeld aus der Datei) und
    eine laufende Zaehlung der erkannten Captions.
  - Das Format ist zeilenbasiert: `Tag 8: Titel`, darunter `Caption:`
    und der Text, Eintraege durch eine Strichzeile getrennt. Ein
    `Tag N:` mitten im Fliesstext zaehlt nicht, es muss am Zeilenanfang
    stehen. Der Import legt keine neuen Tage an; Tage, die es im Plan
    nicht gibt, werden in der Rueckmeldung genannt.
  - Im Content Plan: `[capOffen, capSetzen]` und `capEintragen(liste,
    modus)`, das ueber `t({contentPlan})` speichert — denselben Weg wie
    der Speichern-Knopf, also IndexedDB und (eingeloggt) Supabase.

Dabei ist ein bestehender Fehler aufgefallen und mitbehoben: im
Bulk-Import stand am Ende

    const Ve = existing.length > 0;

`existing` gibt es dort nicht. Die Zeile kam nach `t({contentPlan: st})`,
der Import lief also durch, aber die Rueckmeldung ("Plan importiert –
x/y mit Bild") ging verloren und im Log stand "existing is not defined".
Gemeint ist der bisherige Plan, der ein paar Zeilen darueber als `ut`
bereitliegt. Bitte im Quellcode ebenfalls korrigieren, sonst kommt der
Absturz mit dem naechsten Bau zurueck.

## 10. Fotostil "Montserrat auf Foto"

Neue Version im Tagesmenue, an der Stelle von "Serif auf Foto" (das ist
raus). Sie setzt `tileMode:"photo"` und `textStil:"montserrat"` und holt
danach wie "Foto" die Bilder.

Der Stil im Aufloeser `T1` (Zweig `l==="montserrat"`, nur mit Foto):

    platten:!1, nurErsteZeilePlatte:!0, ohnePlatteErste:!0, fettNurErste:!0,
    ausrichtung:"links", schriftFarbe:"#FFFFFF", bandSchriftFarbe:"#FFFFFF",
    plattenFarbe:null, polsterX:0,
    schriftUeber:"Montserrat", staerkeUeber:"700"

Drei neue Schalter, die der Zeichner auswertet:

  - `ohnePlatteErste` — der Eingangssatz bekommt keine weisse Platte
    (`tt.platten||Ve&&!tt.ohnePlatteErste`) und dafuer den Schatten, den
    sonst nur die Zeilen ohne Platte bekommen.
  - `fettNurErste` — nur die Zeilen des Eingangssatzes stehen in 700, der
    Rest in 400. Wichtig: der Umbruch des Fliesstexts misst dann auch mit
    400 (`$t(_t(pr),qe,!tt.fettNurErste)`), sonst bricht er zu frueh um.
  - Die erste, scharfe Folie richtet ihre Texthoehe nach `t.textAnchor.row`
    aus (aus der ruhigen Zone der Gesichtserkennung), statt nach der
    festen `textLage`. Auf den verwischten Folgefolien greift das nicht,
    dort zaehlt wieder `textLage` — so wollte Carina es.

Verwischen: `dr=Qe>0&&(t.textStil==="montserrat"||<Streuwerk>)`. Bei diesem
Stil ist Folie 1 scharf und jede weitere verwischt, statt etwa jeder
zweiten nach Streuwerk.

Montserrat liegt jetzt als woff2 unter `site/fonts/` (400 und 700, Subset
latin, SIL OFL, Lizenz daneben) und wird in `site/index.html` per
`@font-face` mit `font-display:block` eingebunden. Ueber Google Fonts
allein war sie beim ersten Zeichnen manchmal noch nicht da, und der
Zeichner misst die Textbreiten auf dem Canvas — dann stimmen die Umbrueche
nicht. Alle anderen Canvas-Schriften der App liegen aus demselben Grund
lokal. Bitte im Quellcode genauso halten.

## 11. Beim Umstellen auf Foto behaelt jede Folie ihr Bild

In `jr` (ein Tag neu laden / auf Foto stellen) stand pro Folie:

    Vt = stJa && hatBild && (ct===0 || ablauf || streuwerk(De,ct)>=34)

Das Streuwerk hat etwa jede dritte Folie wieder aus dem Foto geworfen; sie
wurde dann als Textkachel gezeichnet. Carina ist das bei Folie 9, 12, 13
und 14 aufgefallen. Die Bedingung ist jetzt nur noch

    Vt = stJa && hatBild

Der gleiche Ausfall steckte nicht im Weg "Alle Posts neu laden" — dort
gibt es kein Streuwerk. Bitte im Quellcode nicht wieder einbauen.

## 12. Elegante Serifen und Schrift-Kombinationen im Fonts-Reiter

Carina wollte den Look ihrer Canva-Liste. Hatton, Atteron, Ansam und Black
Mango sind lizenzierte Canva-Schriften und lassen sich nicht ausliefern —
also vier frei lizenzierte (SIL OFL), die dem am naechsten kommen:

  - Bodoni Moda  — hoher Kontrast, feine Haarlinien (Hatton, Atteron)
  - Prata        — weicher und runder (Black Mango)
  - Italiana     — duenne, weite Versalien (Ansam)
  - Marcellus    — ruhige Antiqua fuer Fliesstext

Alle liegen als woff2 unter `site/fonts/` und haengen per `@font-face` in
`site/index.html`, wie Montserrat. Cormorant Garamond stand bisher nur im
Google-Link und liegt jetzt ebenfalls lokal — der Zeichner misst Textbreiten
auf dem Canvas und darf nicht auf eine Ersatzschrift laufen. Lizenzen in
`site/fonts/Serifen-LICENSE.txt`.

Eingebaut an drei Stellen:

  1. Schriftkatalog im Brand-Bereich (die Liste mit Musterzeile) — vier
     neue Eintraege vor "Playfair Display".
  2. Auswahlfeld SCHRIFTART (HEADLINE) im Editor — dieselben vier.
  3. Neu: eine Reihe "SCHRIFT-KOMBINATIONEN" oben im Fonts-Reiter, direkt
     unter der Vorschau. Ein Tipp setzt Titelschrift, Textkachel-Schrift,
     Accent und Body zusammen; die Signatur-Schrift bleibt unangetastet.

         Editorial   Bodoni Moda · Bodoni Moda · Italiana   · Montserrat
         Sanft       Prata       · Prata       · Marcellus  · Montserrat
         Weit        Italiana    · Cormorant   · Italiana   · Montserrat
         Wie bisher  Petrona     · Petrona     · OpenSans   · OpenSans

     "Wie bisher" ist der Rueckweg und soll bleiben.

## 13. Die Schriftwahl aus den Einstellungen wirkt jetzt auch im Feed

Carinas Beobachtung stimmte: im Feed standen weiter Anton und Playfair,
egal was in Settings → Fonts gewaehlt war. Zwei Ursachen, beide behoben.

**a) Die Wahl ueberlebte das Neuladen nicht.** Beim Laden wurden kuratierte
Marken aus dem Code neu aufgebaut; von den eigenen Aenderungen blieben nur
`brandText`, `logo`, `logoUrl`. Die Liste heisst jetzt

    n = ["brandText","logo","logoUrl","typography"]

Farben stehen bewusst noch nicht drin — das kommt, wenn die Farbrichtung
entschieden ist.

**b) Zwei feste Werte haben die Marke ueberschrieben.**

  - `nS()` gab fuer jeden Tag `"anton"` als Kachelschrift zurueck. Ueber
    `co("anton")` → `schriftUeber:"Anton"` hat T1 damit die Schrift aus der
    Marke wieder ueberschrieben. `nS()` gibt jetzt `"marke"` zurueck, und im
    Stil „Band oben“ steht `schriftUeber:co(a)` ohne den Notnagel
    `"ArchivoBlack"` — bei `"marke"` bleibt es leer, die Marke gewinnt.
  - Im Kartenzeichner stand `const SERIF="Playfair Display"` fest. Jetzt

        const SERIF = Je.fassung!=="ablauf" && Je.markenSchrift || "Playfair Display"

    `markenSchrift` wird an beiden Aufrufstellen aus `t.plateFont ||
    t.fontFamily` gesetzt. **Die Ablauf-Folien behalten Playfair** — das ist
    ein fester Bauplan, kein Markenelement.

Ausserdem gewinnt auf der ersten Folie jetzt die Titelschrift vor
`fotoSchriften` (`Ve===0?He.fontFamily||Vt` statt `Vt||He.fontFamily`);
`fotoSchriften` bleibt Rueckfall fuer Marken ohne Typografie.

Damit das keine Einbahnstrasse ist, stehen **Anton** und **ArchivoBlack**
jetzt auch in der Schriftliste — vorher waren sie nur pro Tag erreichbar.
Wer den alten Look will, waehlt Anton als Titelschrift.

## 14. Fotostil "Fließtext auf Foto" — Schrift aus der Marke, Abstaende wie im Beispiel

Carina hat einen fremden Karussell-Post als Vorbild geschickt: ruhiger
Grotesk in zwei Schnitten, enge Zeilen innerhalb eines Absatzes, eine ganze
Leerzeile zwischen den Absaetzen. Der bisherige "Montserrat auf Foto" heisst
jetzt **"Fließtext auf Foto"** und macht genau das.

**Schrift.** Der Stil hatte `schriftUeber:"Montserrat"` fest verdrahtet.
Jetzt setzt er `flieszSchrift:!0`, und der Zeichner nimmt die Body-Schrift
der Marke:

    tt.schriftUeber && (Qe = tt.schriftUeber),
    tt.flieszSchrift && t.bodySchrift && (Qe = t.bodySchrift);

`bodySchrift` kommt neu aus `Rt` (`He.bodyFontFamily||"Montserrat"`) und
gilt fuer alle Folien des Posts, auch die erste — der Stil soll durchgehend
eine Schrift haben, in zwei Schnitten.

**Abstaende.** Vorher lagen Zeilenabstand und Absatzabstand beide bei 1.3;
ein Absatz stand also genauso eng wie seine eigenen Zeilen. Mit
`engZeilen:!0`:

    Zeile im Absatz   Et = qe * 1.17     (vorher 1.3)
    Leerzeile         qe * 0.92
    Gesamthoehe       dr.reduce(...)     statt dr.length*Et

Die Gesamthoehe muss die Leerzeilen einzeln zaehlen, sonst sitzt der Block
nicht mehr mittig.

Dazu eine Eigenheit der Aufteilung: `pr` wird um fuehrende Leerzeilen
gekuerzt, die Leerzeile nach dem fetten Einstieg ging also verloren. Im
Fliesstext-Stil wird sie jetzt fest eingesetzt:

    [...$t(_t(er)...), ...tt.engZeilen&&pr?[[]]:[], ...$t(_t(pr)...)]

**Kombination "Sanft"** ist jetzt Prata mit Helvetica Neue statt Montserrat
— Helvetica Neue liegt seit jeher im Projekt (Thin bis Bold) und kommt dem
Vorbild am naechsten.

## 15. Balken statt Fettdruck, waermeres Weiss, kleinere Schrift

Carina hat den Stil an einem Screenshot korrigiert: der Einstieg steht auf
einem **Balken** und ist **nicht fett** — nicht fett gegen normal, sondern
Balken gegen normal. Der Fliesstext-Stil sieht jetzt so aus:

    plattenFarbe: "#F6F1E6"    Balken in warmem Papierweiss
    bandSchriftFarbe: "#1A1614"
    schriftFarbe: "#F6F1E6"    Fliesstext, waermer als Reinweiss
    staerkeUeber: "400"        auch die erste Zeile normal
    polsterX: n*.42

`ohnePlatteErste` faellt damit weg. `fettNurErste` bleibt gesetzt, weil an
dem Schalter auch die Messung mit 400 und die Ausrichtung nach der ruhigen
Zone haengen — mit `staerkeUeber:"400"` steht trotzdem alles normal.

Schriftgroesse: der Stil startet mit 84 Prozent
(`t.textStil==="montserrat"&&(qe=Math.round(qe*.84))` vor dem T1-Aufruf);
die Schrumpfschleife arbeitet danach von dort weiter.

**Textkacheln folgen jetzt auch der Marke.** Sie liefen bisher ohne eigene
Fassung als `"ablauf"` durch und haben darum Playfair behalten. Ob Playfair
bleibt, entscheidet nicht mehr die Fassung, sondern der Tag:

    Ye.markenSchrift = t.reminderArt==="ablauf" || t.karte==="ablauf"
                       ? "" : t.plateFont || t.fontFamily

Echte Ablauf-Tage behalten Playfair, alles andere folgt der Marke.
Nachgemessen gegen den Stand vor allen Schrift-Aenderungen: vier
Ablauf-Folien, null abweichende Pixel.

## 16. Fliesstext ist der Standard, Schrift noch kleiner

`iS=["bandOben"]` → `iS=["montserrat"]`. Damit stellen sich **alle**
vorhandenen Tage um, ohne dass am gespeicherten Plan etwas geaendert wird:
`textStil` wird pro Tag erst aus `ot.textStil` gelesen und faellt sonst auf
`sS(day)` zurueck — und das ist jetzt der Fliesstext-Stil. Wer einen
einzelnen Tag anders will, waehlt "Band oben" weiterhin im Tagesmenue.

Schriftgroesse von 84 auf **70 Prozent**. Der Wert steht an einer Stelle:

    t.textStil==="montserrat" && (qe = Math.round(qe*.70))

Wenn Carina "noch kleiner" oder "wieder groesser" sagt, ist das genau diese
eine Zahl.

## 17. Textkacheln bekamen ArchivoBlack statt der Marken-Schrift

Direkter Folgefehler von Abschnitt 15. Im Zusammenbau steht

    plateFont: ct || Vt || He.plateFontFamily
    Vt = vT(_e, ot.day-1, {hatFoto: !qt})

und `vT` liefert **ohne Foto fest "ArchivoBlack"**. Fuer jede Textkachel
stand in `plateFont` also ArchivoBlack. Solange der Kartenzeichner Playfair
fest verdrahtet hatte, ist das nie aufgefallen; seit die Kacheln der Marke
folgen, kam die fette Grotesk durch — und lief aus der Kachel heraus, weil
der Zeichner mit ihr nicht mehr sauber umbricht.

Der Zeichner bekommt jetzt eine eigene Angabe aus der Marke:

    platteSchrift: He.plateFontFamily || He.fontFamily || ""
    Ye.markenSchrift = ...ablauf... ? "" : t.platteSchrift || ""

`plateFont` bleibt unangetastet, es wird an anderer Stelle gebraucht.

## 18. Eine Stelle fuer das Aussehen der Textkacheln

*Skript-Eintrag 24. Loest die frueheren Einzelaenderungen an den Farben ab.*

Ganz oben im Bundle steht jetzt ein Block. Wer Farbe, Schrift, Groesse
oder Abstaende aendern will, aendert **nur** ihn:

    const BS_KACHEL={
      grundA:"#BEB7A7",   grundB:"#E7E2CE",   // die zwei Farben im Wechsel
      schrift:"#112250",                      // Text
      schriftart:"HelveticaNeueBrand",
      groesse:80,         // Ausgangsgroesse, schrumpft bis es passt
      zeile:1.28,         // Zeilenabstand
      absatz:.85,         // Abstand zwischen den zwei Absaetzen
      rand:.11,           // Seitenrand als Anteil der Breite
      mitte:.52,          // Hoehe der Textmitte als Anteil
      maxhoehe:.70,       // hoechstens so viel Hoehe darf der Text
      name:"carinaannaprav",              // steht unter dem Text
      nameGroesse:24, nameAbstand:1.9,
      fotoSchrift:"Playfair Display",     // Schrift auf Fotokacheln
      deckblattSchrift:"playfair", deckblattGroesse:46
    };

Farbtafel, Kartenzeichner, Zusammenbau und Groessenzeile lesen daraus.

## 19. Fassung "marke": das Bild aus dem Vorbild

*Skript-Eintraege 25 bis 27.*

`stein` und `hell` hatten als einzige kein Feld `fassung`. Der Zeichner
setzte deshalb

    Ye.fassung = Ye.fassung || "ablauf"

und zeichnete die Alltagskacheln als Ablauf-Fassung: linksbuendig, der
zweite Absatz als winziger Fliesstext, unten die Wortmarke. Das war der
Grund, warum die Kacheln nie wie das Vorbild aussahen.

Beide haben jetzt `fassung:"marke"`, und der Zeichner hat einen eigenen
Zweig dafuer:

* zentriert
* Text am doppelten Zeilenumbruch in zwei Absaetze geteilt, der letzte
  fett als Pointe
* Groesse schrumpft in Schritten von fuenf Prozent, bis der Block in
  `maxhoehe` passt
* keine Wortmarke und **kein Monogramm-Ring**. Der Ring kommt aus `ht`
  und wird nur gezeichnet, wenn `Je.monogrammFarbe` gesetzt ist — die
  Fassung marke setzt das Feld deshalb nicht.

Die Aufteilung in zwei Absaetze greift nicht nur bei einer Leerzeile.
Echte Texte haben meist keine. Ohne Leerzeile trennt der vorhandene
Helfer `teile()` am Ende des ersten Satzes: erster Satz normal, Rest
fett. Genau die Struktur des Vorbilds. Gibt es keinen zweiten Satz,
bleibt es ein Block.

Unter dem Text steht der Name aus `BS_KACHEL.name`, zentriert und
gedaempft. Nicht zu verwechseln mit der alten Wortmarke, die unten links
in der Ecke klebte und dem Monogramm-Ring — beide sind auf dieser
Fassung aus

`linie` und `wieder` bekommen dieselbe Fassung, damit im Bundle keine
ungeprueften Kombinationen stehenbleiben.

**Ansehen statt annehmen.** `tools/kachel-pruefen.py` zieht den Zeichner
und den Konfigurationsblock aus einem Bundle und rendert eine Kachel mit
Fabric, ohne die App zu starten:

    npm install fabric@5.3.0 --prefix tools/.pruefen
    python3 tools/kachel-pruefen.py site/assets/index-B5kartenNN.js
    (cd tools/.pruefen && python3 -m http.server 8080)

Damit laesst sich jede Aenderung sehen, bevor sie veroeffentlicht wird.

## 20. Textkacheln laufen in der Marken-Grotesk

*Skript-Eintrag 20. Hebt die Absicht aus Abschnitt 15 teilweise auf.*

Der Kartenzeichner setzt beides ueber dieselbe Rolle:

    FLIESSCHRIFT = LINKS ? SERIF : GLATT
    TITELSCHRIFT = LINKS ? SERIF : "Anton"
    SERIF        = Je.markenSchrift || "Playfair Display"
    LINKS        = MITTE && !AF,  MITTE = !kopf

`LINKS` ist bei jeder Kachel ohne `#`-Kopfzeile wahr, also bei praktisch
jeder Textkachel. Damit hing Schlagzeile *und* Fliesstext am Ersatzwert
Playfair. Der Ersatzwert ist jetzt `HelveticaNeueBrand`; eine gesetzte
`markenSchrift` sticht ihn weiterhin (siehe Abschnitt 17).

Frueher stand hier ausdruecklich „Textkachel Playfair" als gewollte
Fassung. Carina hat das am 3. September umentschieden.

Zwei Wege fuehren ins Leere, das ist beim Suchen wichtig: `ausrichtung`
und `schriftUeber` aus `T1` wirken fuer Textkacheln **nicht**. Der Aufruf

    if(!$e && Ye.grundFarbe && (… wt(Ye, t.text))) { renderAll(); return }

steigt vorher aus, und `wt` rechnet seine Ausrichtung selbst. Beides ist
trotzdem mitgesetzt (Skript-Eintrag 22), damit der seltene Fall, in dem
`wt` mit `return !1` abbricht, dasselbe Bild ergibt.

## 21. Zwei tote Fassungen aus der Farbtafel

*Skript-Eintrag 21.*

`notiz` und `merken` standen in der Farbtafel, aber keine Regel waehlt sie
je aus: die Laengenregel liefert nur `wieder`, `linie`, `zettel`, `zitat`,
die Reminder liefern `aussage`, `zitat`, `zwei`, zwei Knoepfe setzen
`ablauf` und `hand`, alles andere kommt aus `aS(day-1)`. Beide sind raus.

Nebenbei aufgefallen und **nicht** geaendert: `stein` und `hell` haben als
einzige kein Feld `fassung`. Deshalb greift im Zeichner

    Ye.fassung = Ye.fassung || "ablauf"

und die beiden werden als Ablauf-Fassung gezeichnet. Das ist der Grund,
warum eine Aenderung an `stein`/`hell` im Zeichner nur ueber den
`ablauf`-Zweig wirkt.

## 22. Erste Slide eines Fotoposts: Serife und deutlich groesser

*Skript-Eintrag 23.*

Das Deckblatt lief wie jede Folgeslide in Anton auf `PV = 34`. Im Vorbild
traegt die erste Slide eine Serife und ist klar groesser als der Rest.

**Schrift.** Der Weg ist nicht `fotoSchriften`, sondern `kachelSchrift`.
Der Wert wird im Zusammenbau gesetzt, landet ueber `co(a)` in
`schriftUeber` und wird spaet angewandt:

    tt.schriftUeber && (Qe = tt.schriftUeber)

Damit sticht er die Fotoschrift aus `vT`/`fotoSchriften` (Anton, siehe
Abschnitt 16). `"marke"` liefert bewusst keine Schrift und laesst die
Titelschrift greifen; `"playfair"` liefert `Playfair Display`.

    kachelSchrift: ta === "deckblatt" ? "playfair" : (… wie bisher …)

Nur die Rolle `deckblatt`. Die Rolle `foto` — bei vier und mehr Folien die
vorletzte — bleibt bei Anton, sie gehoert optisch zum Rest.

**Groesse.** `PV` ist der Grundwert fuer Folien mit Foto, `OV` der ohne.

    c($e ? (t.folienRolle === "deckblatt" ? 46 : PV) : OV)

`sizeLocked` sticht weiterhin: eine von Hand gesetzte Groesse bleibt.

Aufpassen bei der Suche: `TITELSCHRIFT = LINKS ? SERIF : "Anton"` steht im
Kartenzeichner und gilt fuer Ablauffolien, nicht fuer normale Fotoposts.


## 23. Fotokacheln in der Serife statt in Anton

*Skript-Eintrag 28.*

Eintrag 16 setzt `fotoSchriften:["Anton"]`. Der Wert kommt schon aus dem
Drop, der Eintrag laeuft hier also nicht mehr. Deshalb tauscht ein
eigener Eintrag den fertigen Wert nochmal aus, gegen
`BS_KACHEL.fotoSchrift`.

**Wechselwirkung mit Eintrag 14.** Der starke Tiefenverlauf hinter dem
Text gilt nur fuer Playfair:

    if($e && /Playfair/.test(String(Qe)) && t.tiefenOverlay!==!1)

Mit Anton als Fotoschrift traf das nie zu. Jetzt greift er wieder — und
das ist richtig: die duenne Serife braucht den Verlauf auf dem Foto,
sonst steht weisse Schrift auf hellem Bild.

## 24. Groessen als Anteil der Leinwand, nicht ueber c()

*Skript-Eintrag 24, Werte `groesseAnteil` und `nameAnteil`.*

Der Massstab ist nicht 1. Die Vorschau im Content Plan rendert mit

    format "4:5" -> g=800, m=1000,  scale 2

der Export mit `1080, 1350, {scale: 2.7}`. Und `c(x) = x * scale * 0.8`.

Wer die Schriftgroesse ueber `c()` setzt, die Spaltenbreite aber als
`r * Anteil`, bekommt eine Schrift, die zwei- bis dreimal zu gross fuer
ihre Spalte ist. Kurze Saetze zerbrachen dadurch in fuenf Zeilen.

Die Fassung marke rechnet die Groessen deshalb direkt aus der Breite:

    gr = r * K.groesseAnteil     (.066)
    NG = r * K.nameAnteil        (.018)

Damit sieht die Kachel in der Vorschau und im Export gleich aus.

**Fuer die Pruefung wichtig:** `tools/kachel-pruefen.py` rendert
standardmaessig mit 800x1000 und Massstab 2 — wie die Vorschau. Eine
Pruefung mit Massstab 1 sieht richtig aus und ist trotzdem falsch.

## 25. Die Werte sind am Vorbild gemessen, nicht geschaetzt

Die Kachel aus dem Vorbild wurde aus dem Screenshot geschnitten und
vermessen (402 x 502, also 4:5):

    Grund          #F6F1F1
    Schrift        #0F0A08
    Textspalte     83 % der Breite   -> rand .086
    Schriftgroesse 5,8 % der Breite  -> groesseAnteil .058
    Zeilenabstand  1,28
    Absatzabstand  0,70 der Schriftgroesse
    Blockmitte     54 % der Hoehe    -> mitte .54

Mit diesen Werten bricht der erste Absatz zeichengenau so um wie im
Vorbild. Der zweite bricht eine Silbe frueher, weil die fette Schrift
dort schwerer ist als HelveticaNeue-Bold — das ist der einzige Rest.

Die Farben sind bewusst nicht uebernommen: Carina will Warm Taupe und
Champagne mit Navy, nicht das Off-White des Vorbilds.

So wird nachgemessen:

    python3 tools/kachel-pruefen.py <bundle> --breite 402 --hoehe 502 \
      --scale 1 --grund "#F6F1F1" --schrift "#0F0A08" --text "<Vorbildtext>"

## 26. Beige Gruende, braune Schrift, Aspekta

Kein Navy mehr. Textkacheln tragen Braun auf hellem Beige, Weiss bleibt
den Fotokacheln vorbehalten.

    grundA  #E9E0CC   Beige
    grundB  #F4EFE3   helles Beige
    schrift #4A3A2A   Braun   (8,3 und 9,5 zu 1)

Die Schrift ist `AspektaBrand` statt HelveticaNeueBrand. Aspekta hat
einen echten Fettschnitt (400 und 700 sind im CSS registriert) und
trifft den schweren Fettsatz des Vorbilds deutlich besser.

Der fette Absatz kann eine eigene Familie bekommen:

    schriftart      fuer den normalen Absatz
    schriftartFett  fuer die Pointe, sonst wie schriftart

Steht beides auf AspektaBrand. Wer den Fettsatz noch schwerer will:
ArchivoBlack oder Anton, beide im CSS registriert — dann aber nur fuer
schriftartFett, sonst kippt der ganze Satz.

## 27. Inter, und warum die Schrift des Vorbilds nicht erreichbar ist

Die Vorbildkachel (402 x 502) wurde Zeile fuer Zeile ausgemessen und mit
den Kandidaten aus dem Projekt verglichen.

**Inter trifft die Breite.** Bei `groesseAnteil .058` lagen die
Zeilenbreiten bei 327 / 273 / 83 px gegen 329 / 286 / 87 px im Vorbild,
und der Text brach in dieselben acht Zeilen.

**Die Hoehe stimmte dabei nicht:** Buchstabenhoehe 17 px gegen 22 px. Das
Vorbild nutzt eine Schrift, die bei gleicher Zeilenbreite hoehere
Buchstaben hat — eine schmale Grotesk mit grosser x-Hoehe. Im Projekt
gibt es keine solche. `NotoSchmal` klingt danach, zeigt im CSS aber auf
`Petrona-Regular`, eine Serifenschrift.

Beides zugleich ist mit den vorhandenen Schriften nicht zu haben. Carina
hat "zu klein" beanstandet, also gilt die Hoehe:

    groesseAnteil .072   Buchstabenhoehe 21 px (Vorbild 22)
    zeile         1.06   Zeilenabstand 27 px (Vorbild 31)
    absatz        .80
    maxhoehe      .80

Der Preis: zehn Zeilen statt acht. Wer die acht Zeilen wichtiger findet,
setzt `groesseAnteil` zurueck auf `.058` und `zeile` auf `1.28`.

Aspekta war ein Umweg: gleiche Groesse, aber zwoelf Zeilen und optisch
noch kleiner — die x-Hoehe ist dort noch geringer.

## 28. Enger gestellt (ueberholt von Abschnitt 29)

Das Vorbild hatte hohe Buchstaben *und* nur acht Zeilen. Mit Inter war
nur eines davon zu haben: bei passender Breite waren die Buchstaben zu
flach, bei passender Hoehe brauchte es zehn Zeilen. Der fehlende Hebel
ist die Laufweite.

Der Zeichner staucht den Text jetzt waagrecht (`scaleX`):

    enge  .80

Der Umbruch rechnet mit `MAXB / enge`, gesetzt wird mit `scaleX: enge`.
Damit passt derselbe Text in dieselbe Spalte wie im Vorbild, ohne die
Schrift kleiner zu machen.

Gemessen, beides auf 402 x 502:

                       Vorbild   deine Kachel
    Zeilen                   8              8
    Buchstabenhoehe      22 px          21 px
    Zeilenabstand      31,0 px        31,2 px
    Absatzsprung       54 px          53 px
    Blockmitte          53,8 %         53,7 %

Endwerte: `groesseAnteil .072, enge .80, zeile 1.05, absatz .95,
rand .0885, mitte .595, maxhoehe .80`.

`mitte` steht auf .595 und nicht auf .538, weil in die Hoehenrechnung
der Platz fuer den Namen eingeht — der Textblock selbst landet damit auf
53,7 Prozent.

## 29. Enger heisst Abstand, nicht Buchstaben

Die waagrechte Stauchung aus Abschnitt 28 (`enge .80`) traf die Maße des
Vorbilds, verzerrte aber die Buchstabenformen. Carina wollte den
*Abstand* enger, nicht die Buchstaben. `enge` steht deshalb auf 1 und
bleibt nur als Notausgang im Block stehen.

Stattdessen zwei echte Abstandswerte:

    laufweite  -28   Abstand zwischen den Buchstaben, in Tausendstel em
    zeile     1.04   Zeilenabstand

Die Laufweite geht in den Umbruch ein, sonst rechnet der Zeichner mit
der ungetrackten Breite und bricht zu frueh:

    MESS = MAXB / ENG / (1 + laufweite/500)

Der Faktor 500 ist eine Naeherung: ein Zeichen ist im Schnitt etwa ein
halbes em breit, ein Tausendstel em Laufweite pro Zeichen aendert die
Zeilenbreite also um etwa zwei Tausendstel.

Der Preis gegenueber Abschnitt 28: zehn Zeilen statt acht. Das ist der
Unterschied zwischen einer echten schmalen Schrift und einer, die man
nur zusammenschiebt. Ohne die passende Schriftdatei ist beides nicht
gleichzeitig zu haben.

## 30. Erste Fotoslide in Prata

*Skript-Eintraege 30 und 31.*

Der Weg ueber `kachelSchrift` und `co()` war zu indirekt: `co()` sucht
die Familie in einer Auswahlliste, und dort steht Prata nicht. Er ist
entfallen. Die Familie wird jetzt direkt gesetzt, an derselben Stelle,
an der `schriftUeber` wirkt:

    $e && t.folienRolle==="deckblatt" && BS_KACHEL.deckblattFamilie
      && (Qe = BS_KACHEL.deckblattFamilie)

`$e` heisst: nur mit Foto. Die Folgeslides bleiben bei
`BS_KACHEL.fotoSchrift`.

**Wo Prata registriert ist:** in `site/index.html` per `@font-face`,
NICHT im gebauten CSS. Wer im CSS sucht, findet sie nicht und haelt sie
faelschlich fuer fehlend. Die Datei ist `site/fonts/Prata-Regular.woff2`.

**Vorladen ist Pflicht.** Prata und Inter stehen jetzt in der Liste, die
der Zeichner vor dem Zeichnen abwartet. Ohne das misst Fabric mit der
Ersatzschrift, haelt zu breite Zeilen fuer passend, und der Text laeuft
aus dem Bild — die Falle aus EINBAU.md.

Geprueft: Prata und Playfair messen bei 60 px unterschiedlich breit
(34,6 gegen 31,1 px fuer "x"). Waeren sie gleich, wuerde die
Ersatzschrift greifen.

## 31. Grosse Serifen-Ueberschrift, kleine Grotesk-Unterzeile

Das zweite Vorbild (Grid vom 3. September) zeigte die eigentliche
Struktur: eine grosse Serifen-Ueberschrift und darunter eine deutlich
kleinere Zeile in einer Grotesk. Nicht zwei gleich grosse Bloecke, von
denen einer fett ist — das war meine Fehlannahme aus dem ersten Vorbild.

Gemessen auf 402 x 502:

                        Vorbild        deine Kachel
    Ueberschrift        28 px          28 px
    Zeilenabstand       40 px          41 px
    Unterzeile          19 px          17 px
    Absatzsprung        48 px          ~48 px

Der Zeichner kennt jetzt zwei Groessen, zwei Familien und zwei Farben:

    schriftart        Prata     Ueberschrift
    unterSchrift      Inter     Unterzeile
    unterVerhaeltnis  .64       Groesse der Unterzeile
    unterFarbe        #6B5B4A   gedaempftes Braun

Fotokacheln: `deckblattGroesse 52` (war 46) und neu `fotoGroesse 41`
statt des eingebauten `PV` von 34 — die Folgeslides waren deutlich
kleiner als im Vorbild.

Was noch fehlt: das Vorbild setzt einzelne Woerter in einem warmen
Goldton ("& 60k", "vertraut") und legt auf Fotokacheln eine kleine
beige Schriftplatte unter die Ueberschrift. Beides ist nicht gebaut.

## 32. Inter auf der Textkachel, Prata auf dem Foto

Carinas Aufteilung, ausdruecklich so gewollt:

    schriftart        Inter    Ueberschrift der Textkachel
    unterSchrift      Inter    Unterzeile der Textkachel
    fotoSchrift       Prata    alle Fotoslides
    deckblattFamilie  Prata    erste Fotoslide

Das Vorbild setzt auch die Textkachel in einer Serife. Carina will dort
Inter — die Serife bleibt den Fotokacheln vorbehalten. Playfair Display
kommt damit nicht mehr vor.

## 33. Palette Urban Espresso, und Prata nur auf der ersten Fotoslide

Farben aus der Palette, die Carina geschickt hat:

    Urban Espresso   #5B4A3E   Schrift
    Pavement Shadow  #8A8077   Unterzeile, siehe unten
    Luxe Oat         #CBBFAF   noch nicht verwendet
    Ivory Silk       #E8DED4   Grund A
    Sunlit Veil      #F6F2EB   Grund B

Urban Espresso traegt auf beiden Gruenden: 6,35 und 7,55 zu 1.

Pavement Shadow als Unterzeile waere mit 2,91 zu 1 auf Ivory Silk zu
blass. Er ist deshalb auf `#70675E` abgedunkelt — derselbe Ton, nur
dunkler: 4,18 und 4,96 zu 1.

**Prata gilt nur fuer die erste Fotoslide.** Ich hatte sie in karten93
eigenmaechtig auf alle Fotoslides ausgeweitet; das war nicht verlangt.
Die Folgeslides laufen wieder in `fotoSchrift`, also Playfair Display.

    fotoSchrift       Playfair Display   Folgeslides
    deckblattFamilie  Prata              nur die erste

## 34. Inter fett und nicht fett im Wechsel

Die Textkachel setzt die Ueberschrift fett und die Unterzeile normal,
beide in Inter:

    gewicht        "700"   Ueberschrift
    unterGewicht   "400"   Unterzeile

Die Staerke geht auch in den Umbruch ein — fett laeuft breiter, sonst
bricht der Zeichner zu spaet und die Zeile ragt heraus.

**Prata, zum Mitschreiben:** sie wird an genau einer Stelle als Schrift
gesetzt, `BS_KACHEL.deckblattFamilie`, und die Bedingung dafuer ist

    $e && t.folienRolle === "deckblatt"

also nur mit Foto und nur auf der ersten Slide. Die uebrigen Treffer im
Bundle sind: die Vorladeliste, zwei Auswahllisten im Einstellungsdialog,
eine Schriftbeschreibung und die Kombination "Sanft" — letztere greift
nur, wenn sie angeklickt wird. Folgeslides laufen in
`fotoSchrift` = Playfair Display.

## 35. Folgeslides eines Fotoposts

*Skript-Eintraege 32 und 33.*

Ab der zweiten Slide gilt der vorhandene Fotostil `montserrat`. Er
liefert genau das Gewuenschte:

    ausrichtung:"links"        linksbuendig
    fettNurErste:!0            erste Zeile fett, Rest normal
    nurErsteZeilePlatte:!0     Platte nur hinter der ersten Zeile

Die Schrift ist `folgeFamilie` = Inter. Die Zuweisung steht NACH den
beiden vorhandenen, weil `flieszSchrift` des Stils sonst
`t.bodySchrift` durchlaesst und gewinnt.

**Zur Groesse.** Der Abzug

    t.textStil==="montserrat" && (qe = Math.round(qe*.70))

prueft `t.textStil`, nicht den in T1 ueberschriebenen Wert — er greift
also nicht. `fotoGroesse` ist deshalb die echte Groesse: 44 gegen 52 auf
der ersten Slide, also 15 Prozent kleiner.

Angenommen war: "15 Prozent kleiner" bezieht sich auf die erste Slide.
Falls es 15 Prozent unter dem alten Wert 41 heissen sollte, ist es 35.

## 36. Marcellus auf den Fotokacheln — und die offene Systemfrage

Prata gefiel nicht. Auf den Fotokacheln steht jetzt Marcellus, erste
Slide und Folgeslides:

    fotoSchrift       Marcellus
    deckblattFamilie  Marcellus

**Warum der Feed trotzdem zusammengestoeppelt wirkt.** Der Grund sind
nicht die einzelnen Schriften, sondern dass zwei Systeme nebeneinander
liegen: Textkacheln in fetter Grotesk (Inter 700), Fotokacheln in einer
Serife. Im Raster liest das wie zwei Marken.

Das Vorbild wirkt ruhig, weil dort **alles** dieselbe Serife ist —
Textkacheln wie Fotokacheln.

Zwei Wege, beides je eine Zeile:

    A  schriftart:"Inter",     gewicht:"700"    zwei Systeme (aktuell)
    B  schriftart:"Marcellus", gewicht:"400"    ein System

Carina hat Inter auf der Textkachel ausdruecklich gewollt, deshalb steht
A. Der Vergleich ist gerendert und liegt ihr vor.

## 37. Ein System: Marcellus als Hauptstimme

Die Textkachel setzt die Ueberschrift jetzt in Marcellus, Gewicht 400.
Damit gibt es nur noch eine Hauptstimme, auf Textkacheln wie auf der
ersten Fotoslide.

    schriftart      Marcellus   Ueberschrift Textkachel
    gewicht         "400"
    unterSchrift    Inter       kleine Unterzeile, bewusster Kontrast
    unterGewicht    "400"
    deckblattFamilie Marcellus  erste Fotoslide
    folgeFamilie    Inter       Folgeslides, ausdruecklich so gewollt

Die Groessen auf den Fotokacheln bleiben gestaffelt:

    deckblattGroesse 52   erste Slide, gross
    fotoGroesse      44   Folgeslides, 15 Prozent kleiner

Die fette Grotesk als Hauptstimme ist damit weg. Sie war der Grund,
warum der Feed wie zwei Marken wirkte.

## 38. Warmes Overlay ueber den Bildern

*Skript-Eintrag 34.*

Ueber einem Foto liegen drei Ebenen. Sie waren alle neutral schwarz,
dadurch wirkten die Bilder kuehl und grau:

    1. flaches Abdunkeln mit der Deckkraft Et
       (normal .05, bei Weichzeichner .42)
    2. NEU: eine warme Lasur
    3. der Kantenverlauf oben und unten

Jetzt:

    bildTon     "74,58,44"     warmes Braun statt Schwarz
                               fuer Ebene 1 und 3
    waermeTon   "150,112,76"   die Lasur
    waerme      .16            ihre Deckkraft, 0 schaltet sie ab

Waermer wird es mit `waerme` hoeher, kuehler mit niedriger. Ganz ohne
Lasur: `waerme: 0` — dann bleiben nur die warm getoenten Ebenen 1 und 3.

## 39. Warum das Vorbild besser zu lesen war

*Skript-Eintrag 35.*

Der starke Tiefenverlauf hinter dem Text auf einem Foto hing an

    if($e && /Playfair/.test(String(Qe)) && t.tiefenOverlay!==!1)

Eintrag 14 hatte ihn absichtlich auf Playfair beschraenkt, weil die
Fotoschrift damals Anton war und der Verlauf dort doppelt verdunkelte.
Seit die Fotoschrift Marcellus ist, war er damit **aus** — und genau er
macht weissen Text auf einem Foto lesbar. Das war der ganze Unterschied
zum Vorbild.

Die Bedingung liest die Liste jetzt aus dem Block:

    tiefeSchriften  "Playfair|Marcellus|Prata|Italiana|Cormorant|
                     Bodoni|Inter|Aspekta|Helvetica"

Anton und ArchivoBlack sind absichtlich nicht drin, die tragen ohne.

## 40. Kartenfarben Schiefer und Beton

    grundA   #3A4750   Schiefer
    grundB   #7D7469   Beton
    schrift  #FFFFFF   weiss, auch die Unterzeile

Weiss auf Schiefer: 9,56 zu 1. Auf Beton: 4,59 zu 1.

Beton ist gegenueber dem Palettenwert Pavement Shadow `#8A8077` leicht
abgedunkelt. Im Original kaeme Weiss dort nur auf 3,86 zu 1 — fuer die
grosse Ueberschrift reicht das, fuer die 18-Pixel-Unterzeile nicht.
Mit `#7D7469` tragen beide.

Die Unterzeile ist weiss und nicht gedaempft: auf Beton waere jeder
dunklere Ton unter der Schwelle.

## 41. Warum man auf den Fotos nichts lesen konnte

*Skript-Eintrag 36.*

Ueber einem Foto lagen vier Ebenen, und sie multiplizieren sich:

    Abdunkeln .05  ->  95,0 % vom Bild
    Lasur     .16  ->  79,8 %
    Kante     .34  ->  52,7 %
    Tiefe     .82  ->   9,5 %

Der Tiefenverlauf war der Uebeltaeter. Seine Werte waren .82 oben,
.58 in der Mitte, .90 unten — das ist kein Verlauf, das ist ein
Vollflaechen-Dunkel. Danach war das Foto Schlamm, und weisser Text
traegt in Schlamm nicht, weil ihm der Untergrund fehlt, von dem er sich
abheben koennte.

Das Vorbild macht es umgekehrt: oben hell, unten dunkel, genau dort wo
der Text sitzt. Jetzt:

    tiefeOben   .12
    tiefeMitte  .24
    tiefeUnten  .86
    waerme      .07   (war .16)

Damit bleiben oben 51 Prozent vom Bild und unten 7 Prozent. Das Foto
ist zu sehen, und der Text steht auf einer dunklen Flaeche.

**Merksatz fuer das naechste Mal:** Deckkraefte addieren sich nicht,
sie multiplizieren sich. Vier Ebenen mit je "nur ein bisschen" ergeben
schwarz.

## 42. Orange Beton statt Schiefer

    grundA   #9C5E3B   Orange Beton   Weiss 5,15 zu 1
    grundB   #7D7469   Beton          Weiss 4,59 zu 1

Schiefer #3A4750 ist raus. Beide Kartenfarben sind jetzt warme
Betontoene, einer mit Orange, einer neutral — sie wechseln sich auf den
Kartentagen ab.

Geprueft und verworfen: `#B0714A` und `#A2705A` sehen heller und
freundlicher aus, tragen Weiss aber nur mit 3,96 beziehungsweise 4,20
zu 1. Das reicht fuer die grosse Ueberschrift, nicht fuer die
18-Pixel-Unterzeile. `#A66743` liegt mit 4,52 knapp darueber und waere
die hellere Alternative, wenn es waermer sein soll.

## 43. Invertiert statt Orange: Grund und Schrift sind ab jetzt ein Paar

Orange Beton war zu weit weg von Beton — zwei Farben statt einer
Handschrift. Die Kartentage wechseln jetzt hell und dunkel:

    grundA   #E5DED2   Sand         Schrift #4A443C   7,20 zu 1
    grundB   #7D7469   Beton        Schrift #FFFFFF   4,59 zu 1

Der Umbau dahinter ist wichtiger als die Farbe selbst. Vorher gab es im
Block eine einzige `schrift` fuer beide Gruende. Das ging nur so lange
gut, wie beide Gruende dunkel waren; beim ersten hellen Grund waere
weisse Schrift auf Sand herausgekommen. Statt einer Ausnahme im
Zeichner gehoeren Grund und Schrift jetzt zusammen:

    grundA / schriftA     stein, linie
    grundB / schriftB     hell, wieder

Wer eine Kachelfarbe aendert, aendert das Paar. Ein Grund ohne seine
Schrift laesst sich nicht mehr eintragen, ohne dass es auffaellt.

Ebenfalls raus: `unterFarbe`. Die Unterzeile hatte eine eigene
Farbangabe, die immer denselben Wert hatte wie `schrift` — ein zweiter
Schalter fuer dieselbe Sache, und genau der haette beim hellen Grund
vergessen werden koennen. Die Unterzeile erbt jetzt die Schriftfarbe
ihres Grundes. Sie unterscheidet sich weiter durch Schriftart und
Groesse, nicht durch Farbe.

`tools/kachel-pruefen.py` kennt die Paare: `--paar A` und `--paar B`
zeichnen die Kachel so, wie die App sie zeichnet. `--grund` und
`--schrift` ueberschreiben das weiterhin einzeln, zum Ausprobieren.

Geprueft und verworfen als Ersatz fuer Orange, alle nah an Beton:
Tabak `#6B6258` (5,98), Oliv `#767561` (4,68), Rauch `#6F6E69` (5,11).
Alle drei tragen Weiss, alle drei sind aber nur eine Stufe neben Beton
— im Feed sieht man den Wechsel kaum. Hell gegen dunkel sieht man.

## 44. Tiefe statt Blass — nachgemessen am Vorbild

Nach 43 kam: "nicht mal in der Naehe des Beispiels, so blass und
seicht". Statt weiter zu raten habe ich das Vorbild ausgemessen.

Die Textkachel bei marina.persano:

    Grund       #F6F1F1   fast weiss, minimal warm
    Schrift     #050100   fast schwarz
    Kontrast    16,9 zu 1
    Block 1     normal
    Block 2     FETT, gleiche Groesse
    Zeile       1,11
    Absatz      etwa eine ganze Zeilenhoehe Luft
    Rand        8,2 Prozent der Breite

Vier Sachen waren bei uns anders, und zusammen ergaben sie "blass":

1. **Kontrast.** 7,2 und 4,6 zu 1 statt 17. Mittelbraun auf Sand und
   Weiss auf Beton sind beide weich. Jetzt 15,0 und 10,7 zu 1.
2. **Der zweite Block war kleiner und nicht fett.** Genau umgekehrt
   zum Vorbild: dort ist die Pointe fett und gleich gross wie der
   Aufbau. `unterVerhaeltnis` von .64 auf 1, `unterGewicht` von 400
   auf 700.
3. **Kein Absatz.** .20 gegen die gemessene ganze Zeilenhoehe. Die
   zwei Bloecke klebten aneinander, es gab keinen Moment vor der
   Pointe. Jetzt .55.
4. **Zeilen zu eng.** 1,02 gegen 1,11 im Vorbild. Wir waren enger als
   das, was wir nachbauen wollten. Jetzt 1,10.

Farben aus ihrer eigenen Palette (Urban Espresso):

    grundA   #F6F2EB  Sunlit Veil     schriftA #241C16   15,0 zu 1
    grundB   #4A3B30  Urban Espresso  schriftB #FFFFFF   10,7 zu 1

`#5B4A3E` aus der Palette direkt traegt Weiss nur mit 8,4 und sieht
neben dem hellen Grund noch grau aus; eine Stufe tiefer sitzt es.

**Schrift: Inter statt Marcellus auf der Textkachel.** Das Vorbild ist
durchgehend eine Grotesk, normal und fett. Marcellus hat ueberhaupt
keinen fetten Schnitt — mit Marcellus ist die fette Pointe nicht
baubar. Deshalb Inter fuer beide Bloecke. Die Fotokacheln bleiben
Marcellus, dort geht es um Serifen, nicht um Fett.

Nebenbei ehrlich gemacht: `hell` nimmt jetzt den hellen Grund und
`stein` den dunklen. Vorher war es nach 43 andersherum, weil nur die
Farben getauscht wurden und nicht die Zuordnung. Namen, die das
Gegenteil von dem sagen, was sie tun, sind die naechste Stolperstelle.

**Merksatz:** Bevor etwas "wie das Vorbild" aussehen soll, das Vorbild
ausmessen — Farbe, Kontrast, Gewicht, Zeile, Absatz. Alle vier Zahlen
lagen daneben, jede einzeln haette man fuer Geschmack halten koennen.

## 45. Ein Schriftsystem statt einer Schriftsammlung

Bisher: Marcellus auf der Textkachel, Inter fuer die Unterzeile,
Marcellus auf dem Foto, Montserrat im Folgestil. Vier Familien, keine
Entscheidung. Jetzt zwei, jede mit einer Aufgabe.

    Textkachel, Folgeslides, Name    DM Sans      400 und 700
    Deckblatt der Fotokachel         Playfair Display  700

**DM Sans** statt Inter, weil das Vorbild eine geometrische Grotesk
ist: kreisrunde Punzen bei o und C, flach abgeschnittene Enden. Inter
hat engere Punzen und liest sich wie eine Oberflaeche, nicht wie eine
Zeitschrift. Verglichen wurden am selben Satz: Inter, DM Sans, Plus
Jakarta Sans, Figtree, Schibsted Grotesk, Manrope. Manrope waere die
Alternative, wenn es fetter sein soll; Schibsted ist neutraler,
Figtree schmaler, Jakarta eigenwilliger im a und z.

**Playfair Display 700** statt Marcellus auf dem Deckblatt. Das
Vorbild setzt dort eine fette Serif mit starkem Strichkontrast.
Marcellus hat nur einen Schnitt, und der ist duenn — auf einem Foto
verschwindet er. Ebenfalls verglichen: Prata (feiner), Bodoni Moda
Bold (kaelter), Fraunces Bold (eigenwilliger), Instrument Serif (zu
leicht).

### Zwei Fallen, die dabei aufgefallen sind

**Playfair wurde hart auf 400 gezwungen.** Im Bundle steht

    /Playfair/.test(String(Qe))&&(kt="400");

Wer die Deckblattschrift auf Playfair stellt, bekommt still eine
duenne Ueberschrift und sucht den Fehler bei der Groesse. Das
Deckblatt liest jetzt `deckblattGewicht`, alles andere bleibt.

**Einzelne Zeilen wurden kleiner gezeichnet als der Rest.** Passte ein
langes Wort wie "Nervenzusammenbruch" nicht in die Spalte, schrumpfte
`txt` nur diese eine Zeile. Der Block hatte dann drei Groessen. Die
Anpassungsschleife prueft jetzt neben der Hoehe auch die Breite: die
laengste Zeile bestimmt die Groesse fuer alle. Das nachtraegliche
Schrumpfen einzelner Zeilen ist nur noch Notnagel.

### Und eine Falle im Pruefwerkzeug

Die Schriftvergleiche waren zuerst wertlos: fuenf von sechs Kandidaten
sahen identisch aus, weil alle in dieselbe Serif zurueckfielen. Grund:
Google liefert pro Familie mehrere woff2-Ausschnitte, und der erste im
Stylesheet ist kyrillisch. Geladen wurde also eine Datei ohne
lateinische Zeichen. Der Browser meldet das nicht, er nimmt die
Ersatzschrift. `tools/.pruefen/fonts` enthaelt jetzt nur Dateien, deren
unicode-range U+0000-00FF abdeckt.

`tools/kachel-pruefen.py` kann mit `--wert NAME=WERT` einzelne Werte
aus BS_KACHEL ueberschreiben, ohne das Bundle neu zu bauen. Damit
entstand der Vergleich.

### Noch nicht gebaut

Das beige Schildchen ueber der Ueberschrift der Fotokachel ("Die 5
Levels von Hooks"). Es ist das Element, das die Fotokacheln im Vorbild
als Reihe lesbar macht. Es fehlt ihm aber eine Quelle im Datenmodell —
es braucht einen kurzen Reihen- oder Themennamen, den es heute nicht
gibt. Deshalb bewusst offen und nicht erfunden.

## 46. Helvetica, und die Laufweite gemessen statt geschaetzt

Sie hat die Schrift des Vorbilds erkannt: Helvetica. DM Sans war die
naechstbeste Google-Schrift, aber die naechstbeste ist nicht dieselbe.
HelveticaNeueBrand liegt seit jeher im Projekt und ist im gebauten CSS
mit 400, 500 und 700 angemeldet — es war nichts nachzuladen.

    schriftart      HelveticaNeueBrand
    unterSchrift    HelveticaNeueBrand
    folgeFamilie    HelveticaNeueBrand

DM Sans ist aus der Schriftanforderung in index.html wieder raus, es
wird nirgends mehr benutzt.

### Laufweite: gemessen, nicht geschaetzt

Statt Werte auszuprobieren wurde ein Verhaeltnis verglichen, das von
der Aufloesung unabhaengig ist: Breite durch Hoehe desselben Wortes.

    Vorbild, "Nervenzusammenbruch" fett     309/22 = 14,05
    Vorbild, "machst kurz Content und"      286/21 = 13,62

Dieselben Woerter in HelveticaNeueBrand bei verschiedenen Werten
gesetzt und gemessen (tools/.pruefen/mess.html):

    fett      charSpacing -50 -> 14,24     -60 -> 13,99
    normal    charSpacing -40 -> 13,81     -50 -> 13,52

Ein Wert fuer beide: **-50**. Nachgemessen an der fertigen Kachel
14,30 gegen 14,05 im Vorbild, also 1,8 Prozent daneben — innerhalb der
Messunsicherheit einer 22 Pixel hohen Zeile.

### Korrektur zu Abschnitt 44

Dort steht "Zeile 1,11 im Vorbild". Das war falsch. Die Zahl entstand
aus einer geschaetzten Schriftgroesse von 27 Pixeln. Aus der jetzt
gemessenen Zeichenhoehe folgt eine Groesse von 28 bis 30 Pixeln, und
damit ein Zeilenschritt von rund 1,02 — genau der Wert, der vor 44
schon eingestellt war und den ich mit einer schlechteren Messung
"korrigiert" habe. Steht wieder auf 1,02.

**Merksatz:** Ein Verhaeltnis zweier gemessener Strecken im selben
Bild ist belastbar. Eine aus dem Augenmass geschaetzte Schriftgroesse
ist es nicht — und alles, was man darauf rechnet, erbt den Fehler.

## 47. Das Schildchen — Eingabefeld und Zeichnung

Im Vorbild steht ueber der Ueberschrift der Fotokachel eine kleine
beige Flaeche mit dem Namen der Reihe ("Die 5 Levels von Hooks"). Sie
ist das Element, das die Fotokacheln als Reihe lesbar macht. Es fehlte
ihm bisher eine Quelle; jetzt hat es eine.

### Eintragen

Im Tagesmenue des Content Plans, zwischen VERSION und SCHRIFT, steht
ein Feld **SCHILD**. Was dort steht, wird auf den Tag und auf jede
seiner Folien geschrieben — dieselbe Form wie bei den Schaltern
daneben. Leer lassen heisst: kein Schild.

Das Feld ist bewusst unkontrolliert (`defaultValue` statt `value`) und
schreibt erst beim Verlassen oder mit Enter. Ein kontrolliertes Feld
wuerde bei jedem Tastendruck den ganzen Plan neu zeichnen und dabei
den Schreibcursor verlieren.

### Bewegt sich mit der Ueberschrift

Das Schild haengt an keiner festen Hoehe, sondern an der ersten Zeile:

    De   Mitte der ersten Zeile
    Et   Zeilenhoehe
    _e   linker Rand der Ueberschrift

    Mitte des Schilds = De - Et/2 - Abstand - Schildhoehe/2

Steht der Text oben, mitte oder unten, hat er zwei Zeilen oder fuenf,
faellt er wegen eines Gesichts im Bild anders aus — das Schild wandert
mit. Es sitzt immer direkt ueber der ersten Zeile und beginnt an
derselben Kante, wenn linksbuendig gesetzt wird.

    schildGrund        #A57F55
    schildSchriftFarbe #FFFFFF
    schildGroesse      .030 der Breite
    schildPolster      .9 der Schriftgroesse
    schildHoehe        2.0 der Schriftgroesse
    schildAbstand      .034 der Breite
    schildRundung      .004 der Breite

Ihre Flaeche ist genau ausgemessen `#BD9A71` — mit weisser Schrift
sind das 2,62 zu 1. Das traegt auch fuer eine grosse Schrift nicht
(noetig waeren 3). `#A57F55` liegt im selben Ton und kommt auf 3,64.
Wer ihre Farbe exakt will, aendert eine Zeile.

Der ganze Block liegt in einem try/catch. Ein Fehler im Schild darf
nie die Kachel leer lassen.

### Nachweis

Der Schnipsel wurde aus dem gebauten Bundle geschnitten und mit den
Werten gezeichnet, die der Zeichner beim Export einsetzt
(tools/.pruefen/schild.html). Das Schild sitzt an der richtigen
Stelle. Die Einbettung selbst ist ueber die Sichtbarkeit der
Variablen geprueft: De, Et, _e, tt, r, e, Pe, $e und t stehen an der
Einfuegestelle alle im selben Gueltigkeitsbereich, und das Bundle
laeuft durch `node --check`.

## 48. Die Luecken mitten in den Woertern

    D afuer bin ich no ch nich t weit genug.
    Diesen S atz hoer ich fas t tae glich.
    car i naannaprav

Fabric misst die Breite jedes Zeichens einmal und merkt sie sich
global, fuer die ganze Sitzung. Wird eine Kachel gezeichnet, bevor die
Schrift geladen ist, landen die Masse der **Ersatzschrift** in diesem
Speicher. Danach zeichnet der Browser die **richtigen** Buchstaben,
setzt sie aber an die Stellen der falschen. Ergebnis: Luecken mitten
im Wort.

Sichtbar wird das nur mit charSpacing. Ohne charSpacing setzt Fabric
die Zeile am Stueck und der Browser bestimmt die Positionen selbst;
mit charSpacing setzt Fabric Zeichen fuer Zeichen und braucht die
Masse. Die Laufweite hat den Fehler also nicht verursacht, sondern
aufgedeckt.

### Drei Ursachen, alle drei behoben

1. **Die Vorschau wartete gar nicht auf die Schriften.** Die Bedingung
   lautete `if(!p||!e||i&&!u)return` — gewartet wurde nur, wenn die
   Kachel als Bild gebraucht wurde (`i`). Im Content Plan wurde sofort
   gezeichnet. Jetzt `if(!p||!e||!u)return`. `u` steht bereits in der
   Abhaengigkeitsliste `[e,u,n]`, die Neuzeichnung loest also aus.
2. **Der Speicher wurde nie geleert.** Jetzt vor jedem Freigeben mit
   `Pe.fabric.util.clearFabricFontCache()`.
3. **Der Notausgang nach zwei Sekunden.** Er zeichnet mit
   Ersatzschrift. Kam die echte Schrift spaeter, blieb die Kachel
   falsch, weil `d(!0)` auf einen bereits gesetzten Wert keine
   Neuzeichnung ausloest. Der Pfad nach dem Laden schaltet jetzt
   ausdruecklich zurueck und wieder vor (`d(!1)`, dann in einer
   Mikroaufgabe `d(!0)`), damit React zweimal rendert.

Ausserdem wird das mittlere Gewicht mitgeladen (`400`, `500`, `700`):
der Name unter dem Text steht in 500 und war deshalb ebenfalls
betroffen.

### Nachweis

`tools/.pruefen/drift.html` stellt den Fehler nach: einmal zeichnen
ohne Schriften, dann Schriften laden, dann noch einmal zeichnen. Die
Luecken erscheinen genau wie auf ihrem Bildschirm.
`tools/.pruefen/drift_fix.html` ist dieselbe Datei mit einem
`clearFabricFontCache()` dazwischen — die Luecken sind weg.

## 49. Warum sie zwei Fassungen hinterherhinkte

Auf ihrem Bildschirm stand `karten105`, veroeffentlicht war `107`.

In `netlify.toml` galt

    [[headers]]
      for = "/index.html"

Netlify ordnet Kopfzeilen nach dem **angefragten Pfad** zu, nicht nach
der Datei, die am Ende ausgeliefert wird. Wer die App unter `/`
aufmacht — also jeder — fragt nicht `/index.html` an, bekam die Regel
nicht und behielt eine alte index.html im Browser. Die zeigt auf einen
alten Bundle-Namen, und der liegt wegen `immutable` ein Jahr im Cache.
Die Weiterleitungsdateien halfen nicht: sie greifen nur, wenn der
Browser den alten Namen neu anfragt, nicht wenn er ihn schon hat.

Die Regel gilt jetzt fuer `/` und fuer `/index.html`.
