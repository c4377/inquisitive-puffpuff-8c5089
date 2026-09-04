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

## 50. Fraunces statt Playfair auf dem Deckblatt

    fotoSchrift        Fraunces
    deckblattFamilie   Fraunces
    deckblattGewicht   700   (bleibt)

Fraunces ist schwerer und waermer als Playfair, mit weniger
Strichkontrast — sie steht auf einem Foto fester und passt zu den
warmen Toenen der Kacheln.

Zwei Stellen haetten den Wechsel still verschluckt:

**Der Tiefenverlauf.** Er haengt an der Liste `tiefeSchriften`, und
die kannte Fraunces nicht. Ohne Eintrag waere der Verlauf ausgegangen
und der Text stuende wieder auf hellem Bild — genau der Fehler aus
Abschnitt 39. Fraunces steht jetzt drin.

**Die vorgeladenen Schriften.** Die Liste, auf die die Vorschau
wartet, stand fest im Bundle und kannte nur die alten Familien. Eine
Schrift aus BS_KACHEL, die dort fehlt, wird nicht vorgeladen, die
Kachel wird mit der Ersatzschrift gezeichnet — und nach Abschnitt 48
wissen wir, was das anrichtet. Die Liste ergaenzt sich jetzt selbst
aus dem Block:

    BS_KACHEL.schriftart, .unterSchrift, .deckblattFamilie,
    .folgeFamilie, .fotoSchrift, .schildSchrift

Damit bleibt es dabei: eine Schrift wechseln heisst eine Zeile in
BS_KACHEL aendern. Der Rest zieht nach.

Die Schriftanforderung in index.html laedt Fraunces mit der Achse
opsz (9..144) in 400 und 700.

## 51. Warum die Schrift auf den Fotos klein war

Nicht die Ausgangsgroesse. Zwei andere Werte haben sie
kleingerechnet, und beide standen fest im Bundle.

**Die Textspalte.** Erkennt die App im Bild ein Gesicht, weicht der
Text zur Seite aus — bis hinunter auf 42 Prozent der Breite. In einer
so schmalen Spalte braucht derselbe Satz doppelt so viele Zeilen. Die
Anpassungsschleife schrumpft ihn dann, bis er in die erlaubte Hoehe
passt. Deshalb standen einzelne Kacheln in winziger Schrift in einem
Streifen am linken Rand.

**Die erlaubte Texthoehe** von 74 Prozent der Kachel (48 mit Zaehler).

    deckblattGroesse    52  ->  58
    spalteMin           .42 ->  .72
    textHoehe           .74 ->  .86
    textHoeheZaehler    .48 ->  .60

Gerechnet mit der echten Anpassungsschleife und Fraunces, Vorschau
800x1000:

    kurzer Satz, schmale Spalte    61 px  (7,6%)  ->  93 px  (11,6%)
    langer Satz, schmale Spalte    45 px  (5,6%)  ->  72 px  ( 9,0%)

Zum Vergleich das Vorbild: Zeichenhoehe 27 auf 402 Pixel Breite, also
Schriftgroesse rund 39 — **9,6 Prozent der Breite**. Vorher lagen wir
im schlechtesten Fall bei 5,6 Prozent, jetzt bei 9 bis 11,6.

Beide Werte stehen im Block. Ist eine Spalte von 72 Prozent zu breit,
weil ein Gesicht darunter liegt, ist das eine Zahl.

## 52. Schild und Plaettchen schliessen einander aus

Die Fotokachel hatte laengst eine Flaeche: `nurErsteZeilePlatte` legt
einen cremefarbenen Kasten hinter die erste Zeile — und trennt den
Text dafuer in zwei Bloecke mit einer Luecke dazwischen. Kommt jetzt
oben noch das Schild dazu, hat die Kachel zwei Kaesten uebereinander
und eine Ueberschrift, die auseinanderfaellt:

    [ 5 Levels of Hooks ]
    [ Von der Idee zum  ]

    vierstelligen
    Angebot. Schritt 30
    von 30.

Im Vorbild gibt es genau eine Flaeche, und das ist das Schild. Ist
eines eingetragen, entfallen deshalb Plaettchen und Trennung; die
Ueberschrift laeuft wieder als ein Block ueber das Bild. Ohne Schild
bleibt alles, wie es war — die anderen Kachelarten brauchen das
Plaettchen weiter.

## 53. Vier Sachen an der Fotokachel

**Der Ueberlauf.** `textHoehe` stand auf .86. Die Kachel klemmt den
Text aber zwischen `n*.1` und `n*.9` ein — mehr als **80 Prozent**
passen nie hinein. Bei .86 rechnet die Anpassungsschleife eine Groesse
aus, die anschliessend nicht mehr untergebracht werden kann, und der
Text laeuft unten heraus. Jetzt .78, mit Zaehler .56. Der Wert war
mein Fehler aus 51: gross gerechnet, aber die Klammern nicht
mitgelesen.

**Kein Kasten mehr, dafuer fett und nicht fett.** Bisher war beides
aneinandergekettet: die Marke "erste Zeile" (`nurErsteZeilePlatte`)
steuerte den Kasten UND das Fett. Kasten aus hiess Fett aus. Jetzt
bleibt die Marke stehen, gezeichnet wird der Kasten aber nicht mehr
(`platten` aus, `ohnePlatteErste` an). Auf jedem Foto gilt damit
dasselbe wie auf den Textkacheln: erster Block fett, Rest normal.

**Keine Luecke zwischen den Saetzen.** Zwischen den beiden Bloecken
stand eine leere Zeile. Sie gehoerte zum Kasten und gab ihm Luft.
Ohne Kasten ist sie nur ein Loch. Auf Fotos faellt sie weg, auf
Kacheln ohne Foto bleibt sie.

**Die Folgeslides bekommen ihre Schrift auch ohne Foto.** Die
Zuweisung `folgeFamilie` hing an `$e`, also am Hintergrundbild.
Folgeslides ohne Bild fielen durch und behielten, was ihr Stil vorgab.
Das `$e&&` ist weg.

### Zur Frage, ob die Zeilen darunter Playfair sind

Nein. Sie sind Fraunces in 400. Fraunces hat bei 400 deutlich mehr
Strichkontrast und wirkt klassischer als bei 700 — das liest sich wie
eine andere Schrift, ist aber dieselbe Familie in einem anderen
Schnitt. Zum Vergleich nebeneinander gesetzt in
`tools/.pruefen/frx.html`: Fraunces 700, Fraunces 400, Playfair 400.
Playfair ist deutlich schmaler und spitzer.

Wer die Zeilen darunter kraeftiger will, ist das ein Wert: ein
mittlerer Schnitt statt 400.

## 54. Das Schild sass in der Ecke

Selbst nachgesehen, statt zu fragen: `tools/.pruefen/n_*.html`
zeichnet die Fotokachel mit dem Schild fuer alle drei Textlagen.

Bei `textLage: oben` klebte das Schild oben links am Rand, halb
angeschnitten. Der Grund steht in der Klammer:

    De - Et/2 < n*.1  ->  De = n*.1 + Et/2

Der Text darf nicht hoeher als 10 Prozent starten. Das Schild sitzt
aber ueber der ersten Zeile — also im Rand. Die Klammer kannte es
nicht.

Sie nimmt das Schild jetzt mit auf:

    SR = Schildhoehe + Abstand   (0, wenn kein Schild)
    De - Et/2 < n*.1 + SR  ->  De = n*.1 + SR + Et/2

Steht ein Schild darueber, faengt der Text so viel tiefer an, wie das
Schild braucht. Ohne Schild aendert sich nichts.

Neu im Block: `schildNeigung` in Grad, Vorgabe 0. Flaeche und Text
drehen zusammen.

## 55. Das Schild sitzt schraeg

    schildNeigung   -3 Grad

Flaeche und Text drehen zusammen. Gedreht wird um den linken Punkt in
der Mitte der Flaeche — die linke Kante bleibt also an derselben
Stelle wie die Ueberschrift darunter, das Schild kippt nur.

Verglichen wurden 2, 3 und 5 Grad. Bei 5 kippt es so weit, dass die
untere rechte Ecke in den Abstand zur Ueberschrift hineinwaechst
(bei einer 250 Pixel breiten Flaeche etwa 22 von 27 Pixeln). 3 Grad
liest sich als Absicht und laesst Luft.

Wer es staerker will: bei mehr als 4 Grad muss der Abstand
(schildAbstand) mitwachsen, sonst beruehrt die Ecke die erste Zeile.

## 56. Der Kasten kommt zurueck, und die Textlage bewegt sich wieder

**Der Kasten.** "Statt Band immer fett und nicht fett" habe ich auf
alle Fotokacheln angewendet. Gemeint waren die Folgeslides. Jetzt:

    Deckblatt ohne Schild   Kasten bleibt
    Deckblatt mit Schild    kein Kasten (das Schild ist der Kasten)
    Folgeslides             kein Kasten

Fett und nicht fett gilt weiter ueberall auf Fotos.

**Die Textlage.** Sie liess sich nicht mehr umstellen — oben, mitte
und unten sahen gleich aus. Das war meine Schuld und rechnerisch
zwingend:

Der Text wird zwischen `n*.1 + SR` und `n*.9` eingeklemmt, das sind
bei gesetztem Schild 72,5 Prozent der Hoehe. Die Anpassungsschleife
durfte ihn aber bis auf **78 Prozent** wachsen lassen. Ein Text, der
hoeher ist als das Fenster, in das er soll, wird von beiden Klammern
gefasst — und die zweite gewinnt immer. Ergebnis: ein und dieselbe
Position, egal was eingestellt war.

Zwei Aenderungen:

1. Die Schleife rechnet das Schild ab: `Je = n*textHoehe - SR`. Damit
   passt der Text immer in das Fenster, und es gibt keinen Ueberlauf
   mehr, unabhaengig vom Schild.
2. `textHoehe` von .78 auf **.70**. Der Weg, den der Text wandern
   kann, ist `n*(.8 - textHoehe)` — bei .78 waren das 2 Prozent der
   Hoehe, jetzt 10. Die Rechnung faellt das Schild heraus, die
   Bewegung ist also mit und ohne Schild gleich.

Nachgerechnet fuer 800x1000 mit Schild:

    oben   De = 222
    mitte  De = 247
    unten  De = 347

Vorher standen alle drei auf 222.

## 57. Helvetica Neue Thin

    gewicht         200   (Textkachel, erster Block)
    leichtGewicht   200   (Fotokachel, alle Zeilen ausser der ersten)
    unterGewicht    700   (bleibt: die Pointe)

Auf den Fotokacheln stand das leichte Gewicht fest im Bundle:

    fontWeight: tt.fettNurErste && !Ve ? "400" : kt

An drei Stellen. Sie lesen jetzt `leichtGewicht`, damit Textkachel und
Fotokachel denselben Schnitt benutzen und eine Aenderung an einer
Stelle reicht.

**200 wird mitgeladen.** Die Ladeliste kannte 400, 500 und 700. Ein
Gewicht, das dort fehlt, kommt zu spaet — und was dann passiert, steht
in Abschnitt 48: Luecken mitten in den Woertern. Jetzt 200, 400, 500,
700.

Verglichen wurden Thin 200, Light 300 und Roman 400 an derselben
Kachel (`tools/.pruefen/th*.html`). Thin gibt der Pointe den groessten
Abstand; Light waere die Zwischenstufe, falls 200 auf dem Handy zu
duenn wirkt.

`tools/kachel-pruefen.py` kennt jetzt auch Thin und Light.

## 58. Auf Fotos lief der Text seitlich heraus

Die Anpassungsschleife hat nur die **Hoehe** geprueft. Der Umbruch in
`$t` hat aber eine Notbremse:

    Ht(Vt,rt,Ve) <= Qt-c(30)  ||  ct.length === 0

Das zweite Oder sorgt dafuer, dass eine Zeile nie leer bleibt. Passt
ein einzelnes Wort nicht in die Spalte, landet es trotzdem darin — und
laeuft rechts hinaus, wo es abgeschnitten wird. Dasselbe beim Kasten:
seine Breite folgt der Zeilenbreite, also lief auch er hinaus.

Sichtbar wurde es erst mit Fraunces: der fette Schnitt setzt rund
**30 Prozent breiter** als Helvetica (nachgemessen: 1789 zu 1603 Pixel
bei 92 px fuer denselben Satz), dazu deckblattGroesse 58 statt 52.

Es ist dieselbe Luecke wie bei den Textkacheln in Abschnitt 45, nur an
der zweiten Stelle. Dort prueft die Schleife seither auch die Breite,
hier nicht. Jetzt hier auch: die laengste Zeile bestimmt die Groesse
mit.

Nachgerechnet, Spalte 0,72 also Umbruchgrenze 528 px:

    "Von der Idee zum vierstelligen Angebot…"
        nur Hoehe   Groesse 87   14 px ueber die Kante
        auch Breite Groesse 82   17 px innerhalb

    "Nervenzusammenbruch nach dem Verkaufsgespraech"
        nur Hoehe   Groesse 93   588 px ueber die Kante
        auch Breite Groesse 41   innerhalb

Der zweite Fall zeigt den Preis: ein Wort mit 19 Buchstaben passt bei
grosser Schrift in keine Spalte, also wird die ganze Ueberschrift
klein. Das ist richtig — abgeschnitten war es vorher — aber es heisst
auch: sehr lange Komposita kosten Schriftgroesse. Wer sie umgeht,
behaelt die grosse Schrift.

## 59. Light statt Thin, und die schwarze fette Zeile

    gewicht         300
    leichtGewicht   300

**Die fette Zeile war schwarz.** Die Textfarbe hing an `Ve`, also an
"gehoert zum ersten Block":

    fill: Ve ? bandSchriftFarbe (schwarz) : schriftFarbe (weiss)

Das stimmte, solange der erste Block **immer** auf dem hellen Kasten
stand. Seit Abschnitt 56 zeichnen die Folgeslides keinen Kasten mehr —
die fette Zeile stand also schwarz auf dem Foto, waehrend der Rest
weiss blieb.

Richtig ist: dunkel genau dann, wenn wirklich ein Kasten darunter
liegt. Das ist dieselbe Bedingung, mit der der Kasten gezeichnet wird:

    !ge && (tt.platten || Ve && !tt.ohnePlatteErste)

Sie steht jetzt an drei Stellen — Fuellfarbe, Rand und Randbreite —
statt des blossen `Ve`. Damit gilt: Kasten da, Schrift dunkel; kein
Kasten, Schrift weiss mit Rand und Schatten wie der Rest.

**Merksatz:** Wenn eine Marke zwei Dinge gleichzeitig bedeutet
("erster Block" und "steht auf hellem Grund"), bricht sie in dem
Moment, in dem man eines der beiden aendert. Erst war es das Fett
(Abschnitt 56), jetzt die Farbe. Beide hingen an derselben Marke.

## 60. Der Kasten wird nie schmaler als seine Zeile

Nachgemessen (`tools/.pruefen/wort.html`): die beiden Messwege — Satz
am Stueck gegen Wort fuer Wort mit gemessener Luecke — stimmen bei
Fraunces 700, Fraunces 400 und Helvetica auf den Pixel ueberein. Die
Breite des Kastens war also nicht zu klein berechnet, und die
gezeichnete Breite passt zur gemessenen. Auch Messen und Malen
stimmen ueberein (`messbreite.html`, Abweichung 0,1 Prozent).

Der Ueberlauf, der zu sehen war, kommt aus Abschnitt 58: ein Wort,
das breiter ist als die Spalte, wurde trotzdem in die Zeile gesetzt.
Der Kasten folgt der Zeilenbreite — also lief er mit hinaus. Behoben
ist das seit **karten117**. Wer eine aeltere Fassung im Browser hat,
sieht den Fehler weiter.

Trotzdem gehaertet: die Kastenbreite nimmt jetzt den groesseren der
beiden Messwerte statt sich fuer einen zu entscheiden. Der Kasten kann
damit zu breit sein, nie zu schmal.

## Zur Schriftstaerke

`gewicht` und `leichtGewicht` stehen auf **300 (Light)**. Auf
"Light nicht thin" hin gesetzt und dort belassen. Thin waere 200 —
eine Zahl, falls doch.

## 61. Fraunces fuellt die Kachel

Vier Werte, kein Umbau:

    deckblattGroesse   58  ->  68
    spalteMin         .72  ->  .82
    umbruchRand        30  ->  12
    fotoZeile         1.30 ->  1.10
    textHoehe         .70  ->  .74

**Der Umbruchrand.** Der Umbruch warf `c(30)` der Spaltenbreite weg,
bei Massstab 2 also 48 Pixel — 6 Prozent der Kachel. Der Abstand
stammte aus einer Zeit, in der Messen und Malen auseinanderliefen;
nachgemessen weichen sie um 0,1 Prozent ab (`messbreite.html`). 12
reicht.

**Der Zeilenabstand.** `Et = qe * 1.3` auf Fotos. Im Vorbild
nachgemessen: Zeilenschritt 39 Pixel bei einer Schriftgroesse von rund
38,6 — also etwa **1,0**. Wir standen ein Drittel darueber. Jede Zeile
Abstand kostet Schriftgroesse, weil die Anpassungsschleife die Hoehe
aller Zeilen zusammenzaehlt. Jetzt 1,10; etwas mehr als das Vorbild,
weil Fraunces laengere Ober- und Unterlaengen hat als eine Grotesk.

Gerechnet mit der echten Schleife (`gross.html`), Text "Von der Idee
zum vierstelligen Angebot. / Schritt 30 von 30.":

    vorher                       77 px   ( 9,6% der Breite)  6 Zeilen
    Spalte .82                   87 px   (10,9%)             5 Zeilen
    + Rand 12 + Start 68         90 px   (11,3%)             5 Zeilen
    + Zeile 1.10                 groesser, siehe Bild

**Achtung, eine Nebenwirkung:** `spalteMin` .82 heisst, dass die
Spalte immer so breit ist. Das Ausweichen vor Gesichtern ist damit
praktisch aus — es war der Grund fuer die winzige Schrift in
Abschnitt 51. Wenn Text kuenftig auf einem Gesicht liegt, ist das der
Wert.

## 62. Ein Band, keine Treppe

Selbst nachgesehen (`tools/.pruefen/band.html`), und der Fehler war
sofort zu sehen: **jede Zeile bekam einen eigenen Kasten in ihrer
eigenen Breite.** Gemessen an einer Kachel:

    Zeile "Von der Idee"        Text 635   Kasten 727
    Zeile "zum"                 Text 219   Kasten 310
    Zeile "vierstelligen"       Text 636   Kasten 728
    Zeile "Angebot."            Text 460   Kasten 552

Vier verschieden lange Kaesten. Der Kasten hinter "zum" ist 310 statt
727 breit — das ist das "zu kurze Band". Kein Rechenfehler: die
Kastenbreite war korrekt, nur eben pro Zeile.

Solange der erste Block **eine** Zeile lang war, fiel das nicht auf.
Seit die Schrift die Kachel fuellt (Abschnitt 61), sind es vier.

Alle Kaesten des ersten Blocks nehmen jetzt dieselbe Breite: die der
laengsten Zeile. Da sie mit `Et` untereinander stehen und `Et+c(1.5)`
hoch sind, stossen sie aneinander und ergeben eine durchgehende
Flaeche. Zeilen ohne Kasten bleiben, wie sie waren.

**Merksatz:** "zu kurz" hiess nicht, dass eine Zahl zu klein war. Es
hiess, dass die Zahl fuer jede Zeile einzeln richtig war, obwohl die
vier Zeilen zusammen eine Form ergeben sollen.

## 63. Der Look aus ihrem Beitrag

Ihr Bildschirmfoto ausgemessen, Kachel 1206 Pixel breit:

    Serifenblock    Zeichenhoehe 71  ->  Groesse rund 95   (7,9%)
    Zeilenschritt   91               ->  0,96 der Groesse
    Grotesk-Block   Zeichenhoehe 53  ->  Groesse rund 71   (5,9%)
    Verhaeltnis     71/95            =   0,75
    linker Rand     122 von 1206     =   10,1%
    Kasten          keiner

### Zwei Schriften auf einer Folie

Bisher lief eine Folie in **einer** Familie. Jetzt:

    Block 1   deckblattFamilie   Fraunces, fett
    Block 2   zweiteFamilie      HelveticaNeueBrand, leicht
    zweitAnteil  .75             Block 2 ist drei Viertel so gross

Umbruch und Anpassungsschleife rechnen weiter mit der **grossen**
Groesse und der Serif. Das schaetzt den zweiten Block zu breit und zu
hoch — also immer zur sicheren Seite: Zeilen brechen frueher, nie
spaeter, nichts kann seitlich hinauslaufen (Abschnitt 58).

### Kein Band mehr, ausser man will eins

    bandAuf   0

Ihr Beitrag hat keinen Kasten, der Text steht direkt auf dem Bild und
bekommt stattdessen den Schatten, den der Zeichner ohnehin setzt,
sobald keine Flaeche darunter liegt. `bandAuf` auf 1 bringt den Kasten
auf dem Deckblatt zurueck.

### Der Zeilenabstand

    fotoZeile   1.10  ->  0.98

Gemessen 0,96. Enger als alles bisher, und genau das macht den
Blocksatz-Eindruck.

### Die Bilder waren zu blass

Der Tiefenverlauf lag bei .12 / .24 / .86. Unten also 86 Prozent
Abdunklung — das frisst Farbe und Zeichnung aus dem Bild, und genau
darum sahen die Fotos flau aus. Im Vorbild ist keine Abdunklung zu
sehen; der weisse Text traegt ueber seine Groesse und den Schatten.

    tiefeOben    .12  ->  .05
    tiefeMitte   .24  ->  .10
    tiefeUnten   .86  ->  .42

Das ist der Kompromiss: sichtbar hellere Bilder, unten noch genug
Halt, damit weisse Schrift auf einer hellen Stelle nicht verschwindet.
Wird es irgendwo zu hell zum Lesen, ist `tiefeUnten` die Zahl.

## 64. Auf Fotos war "unten" wirkungslos

Die Textlage wurde so bestimmt:

    ve = fettNurErste && !blur && textAnchor.row ...   // Automatik
         || t.textLage                                  // ihre Wahl
         || (Foto ? "unten" : "mitte")                  // Vorgabe

Die **Automatik aus der Bildanalyse stand vor ihrer Wahl**. Wo im Bild
ein Gesicht erkannt wurde, war "unten" ohne Wirkung — auf Fotoposts
also fast immer.

Aufgefallen ist es erst jetzt, und das ist meine Schuld. Die Automatik
haengt an `fettNurErste`, und das galt frueher nur fuer den Stil
"montserrat". Seit Abschnitt 56 setze ich es auf **allen**
Fotokacheln, damit dort fett und nicht fett gilt. Damit war die
Automatik ueberall aktiv und ihre Wahl ueberall wirkungslos.

Reihenfolge jetzt: **ihre Wahl, dann die Automatik, dann die
Vorgabe.** Der Schalter "auto" im Tagesmenue setzt `textLage` auf
nichts — dort greift die Automatik weiter, wie gedacht.

**Merksatz, zum dritten Mal in dieser Reihe:** `fettNurErste` bedeutet
inzwischen dreierlei — Kasten, Fettschrift und "Automatik darf die
Lage bestimmen". Wer eines davon einschaltet, schaltet die anderen
mit. Kasten und Farbe sind bereits geloest (56, 59), die Lage jetzt
auch.

## 65. Der erste Block darf mehr als eine Zeile sein

Im Bundle steht eine Stelle, die den ersten Block auf **genau eine
Zeile** zusammenstreicht. Sie sucht die groesste Zahl an Woertern, die
noch in eine Zeile passt, und schiebt alles weitere in den zweiten
Block:

    Ve = Woerter, die in eine Zeile passen
    Ve < rt.length && (pr = Rest + pr, er = erste Ve Woerter)

Das gehoert zum Kasten: der Kasten ist ein Balken hinter **einer**
Zeile. Ohne Kasten ist es nur eine Kappung mitten im Satz — der erste
Satz bricht nach ein paar Woertern ab, der Rest steht klein darunter.
Genau das war zu sehen.

Wieder eine Folge davon, dass ich `nurErsteZeilePlatte` seit
Abschnitt 56 auf allen Fotokacheln setze. Vorher lief die Stelle nur
im Stil "montserrat".

Gekappt wird jetzt nur noch, wenn wirklich ein Kasten gezeichnet wird.
Ohne Kasten trennt allein die Satzgrenze:

    /^(.{10,90}?[.!?:])\s+(.*)$/

Bei ihrem Beitrag heisst das: "Du siehst mich heute, mit einer
starken, mehrfach 6-stelligen Personal Brand." (76 Zeichen, endet auf
Punkt) wird der Serifenblock ueber vier Zeilen, "Aber lass mich dich
mal mitnehmen…" der Grotesk-Block darunter. Genau ihre Aufteilung.

Ist der erste Satz laenger als 90 Zeichen, greift die Regel nicht und
alles bleibt im ersten Block, also durchgehend Serif.

**Damit sind vier Dinge entkoppelt, die alle an derselben Marke
hingen:** Kasten (56), Schriftfarbe (59), Textlage (64) und jetzt die
Kappung auf eine Zeile. Die Marke bedeutet wieder nur eines — "das
ist der erste Block".

## 66. Auf den Folgeslides war der erste Block nicht fett

`deckblattGewicht` gilt nur fuer das Deckblatt. Auf den Folgeslides
blieb `kt` bei dem, was der Stil vorgab — also leicht. Der grosse
erste Block sah damit aus wie der kleine zweite, nur groesser.

    folgeGewicht   700

Gleiche Form wie `deckblattGewicht`, eine Zeile daneben. Der zweite
Block bleibt bei `leichtGewicht`; fett und nicht fett stimmt damit auf
Deckblatt und Folgeslides gleichermassen.

    Deckblatt      Fraunces 700    /  Helvetica 300
    Folgeslides    Helvetica 700   /  Helvetica 300
    Textkacheln    Helvetica 300   /  Helvetica 700

## 67. Text in die ruhige Zone, statt das Bild weichzuzeichnen

Die Bildanalyse gibt es laengst: sie teilt das Bild in neun Felder,
bewertet, wie unruhig jedes ist, meidet das Gesicht und die Zone
darunter (Eintraege 4 und 5) und liefert `quietZone`. Daraus wird
`textAnchor` — die Stelle, an der Text am ruhigsten steht.

Benutzt wurde sie so gut wie nie. Zwei Dinge standen davor:

**Der Weichzeichner.** Eintrag 2 zeichnet etwa jedes zweite Bild ab
Folie 2 weich. Das war die Notloesung, damit Text irgendwo lesbar
wird. Und der Zeichner benutzt die Bildanalyse ausdruecklich nur,
wenn **nicht** weichgezeichnet wird (`!t._blurAn`) — auf einem
verwischten Bild gibt es keine ruhige Zone mehr, nur noch Brei. Der
Weichzeichner hat die Analyse also selbst abgeschaltet.

    weichAnteil   0        (war fest 50 Prozent)

**Die feste Textlage.** Jeder Tag bekam eine Lage aus einer
rotierenden Liste `["unten","mitte","oben"]`, auch ohne eigene Wahl.
Seit Abschnitt 64 schlaegt die eingestellte Lage die Automatik — und
weil immer eine eingestellt war, kam die Automatik nie zum Zug. Die
Liste entfaellt.

Damit gilt jetzt: **ihre Wahl im Tagesmenue, sonst die ruhigste Zone
des Bildes, sonst unten.**

Falls Text auf einem unruhigen Bild schwer lesbar wird, sind das die
Stellschrauben, in dieser Reihenfolge: `tiefeUnten` (Abdunklung
unten), `spalteMin` (Ausweichen vor dem Gesicht, steht auf .82, also
praktisch aus), `weichAnteil` (Weichzeichner zurueckholen).

## 68. "Plan konnte nicht gespeichert werden (UnknownError)"

Der Plan liegt in der IndexedDB des Browsers, nicht auf einem Server.
Die Fotos stecken als Datenzeilen **im Plan selbst** — die Galerie
speichert jedes Bild nur einmal, aber in voller Kameraaufloesung. Bei
siebzig Tagen sind das schnell zig Megabyte. Safari auf dem iPhone
meldet einen vollen Speicher nicht als "quota exceeded", sondern als
`UnknownError`.

Drei Aenderungen, in der Reihenfolge ihrer Wirkung:

### 1. Bilder verkleinern

Vor dem Schreiben wird jedes Bild auf hoechstens `bildKante` (1350)
an der langen Seite gerechnet und als JPEG mit `bildGuete` (.85)
abgelegt. 1350 ist die Hoehe des Exports (1080x1350) — groesser
gespeichert bringt nichts.

**Das Seitenverhaeltnis bleibt.** Der vorhandene Helfer `n9` haette
auf 2:3 beschnitten, und die Kachel schneidet danach noch einmal auf
4:5 — das haette die Bildausschnitte verschoben. Deshalb ein eigener,
der nur die Kantenlaenge begrenzt.

Nachgemessen (`tools/.pruefen/klein.html`):

    3000x2000, 0,63 MB   ->   1350x900, 0,11 MB
    Seitenverhaeltnis    1,500  ->  1,500
    zweiter Durchlauf    aendert nichts
    Bild unter 200 KB    bleibt unangetastet

Der zweite Speichervorgang ist damit so schnell wie vorher: was schon
klein ist, wird nicht noch einmal angefasst. Und das Ergebnis wird nur
uebernommen, wenn es wirklich kuerzer ist.

### 2. Zweiter Versuch

Schlaegt das Schreiben fehl, werden **Bilder-Vorrat** und
**Pin-Archiv** geloescht — beides ist nachladbar, der Plan nicht — und
es wird noch einmal geschrieben.

### 3. Ehrliche Meldung

Statt "UnknownError" steht jetzt der Grund, die Groesse der Bilder im
Plan und, wo der Browser es hergibt, belegter und verfuegbarer
Speicher:

    QuotaExceededError — Bilder im Plan 48,3 MB, belegt 52,1 MB von 60,0 MB

Damit ist beim naechsten Mal sichtbar, ob es wirklich der Platz ist
oder etwas anderes.

## 69. Text hoeher, Wortmarke an feste Stelle, Grading

### Die Unterkante

Der Text durfte bis `n*.9` reichen. Die Wortmarke wird **darunter**
gezeichnet (`De + qe*.5`) und stand deshalb auf der Kachelkante, halb
angeschnitten. Zwei Aenderungen statt einer:

    textUnten   .86    der Text endet hoeher
    nameUnten   .945   die Wortmarke steht an einer FESTEN Stelle

Die Wortmarke gehoert zur Kachel, nicht zum Textblock. Solange sie am
Textende hing, schob jede weitere Zeile sie weiter aus dem Bild.

Weil der Text jetzt zwischen 10 und 86 Prozent liegt, also in 76
Prozent der Hoehe, muss `textHoehe` darunter bleiben — sonst klemmen
beide Klammern und die Textlage steht wieder still, wie in Abschnitt
56. Deshalb .74 auf **.70**, Weg also 6 Prozent der Hoehe.

### Das Grading

Bisher lag nur ein Verlauf ueber dem Bild. Ein Verlauf dunkelt
gleichmaessig ab und nimmt Zeichnung heraus — das war der Grund fuer
die blassen Bilder. Kontrast gibt er keinen. Jetzt wird das Bild
selbst gerechnet:

    bildKontrast     .18    spreizt Lichter und Tiefen
    bildHelligkeit  -.06    setzt den Schwarzpunkt tiefer

Beide auf 0 heisst: kein Filter, keine Rechenzeit. Gerechnet wird auf
dem Bild, das der Lader ohnehin schon auf 1800 Pixel begrenzt hat.

Nachgesehen in `tools/.pruefen/grading.html`: Tiefen deutlich tiefer,
Lichter bleiben hell — also Kontrast statt Abdunklung.

## 70. Nein — die Folgeslides waren noch weichgezeichnet

Gute Frage, und die Antwort war nein. Abschnitt 67 hat den
Zufallsanteil auf 0 gesetzt. Davor steht aber eine zweite Bedingung,
die der Drop selbst mitbringt:

    dr = Qe>0 && ( t.textStil==="montserrat" || Zufall )

Und **alle** Folgeslides haben `textStil: "montserrat"` — das ist der
Stil, der sie linksbuendig mit fetter erster Zeile setzt
(`folgeStil`). Die erste Bedingung war also immer wahr, der
Zufallsanteil kam nie zum Zug. Weichgezeichnet wurde weiter, und zwar
**jede einzelne** Folgeslide.

`weichAnteil` schaltet jetzt den ganzen Weichzeichner: bei 0 bleibt
kein Bild weich, auch kein montserrat-Bild.

## 71. Und der Weichzeichner hat das Grading ueberschrieben

Abschnitt 69 haengt Kontrast und Schwarzpunkt an `me.filters`. Ein
paar Zeilen weiter setzte der Weichzeichner

    me.filters = [ new Blur(...) ]

mit eckigen Klammern, also **ersetzend**. Auf jedem weichgezeichneten
Bild war das Grading damit weg — und weichgezeichnet war jede
Folgeslide. Jetzt haengt er sich an, statt zu ersetzen.

**Merksatz:** Zwei Stellen, die derselben Eigenschaft etwas zuweisen,
und die spaetere gewinnt. Erst pruefen, wer sonst noch an `filters`
schreibt, bevor man selbst etwas hineinlegt.

## 72. Die Ablauf-Folien in dasselbe System

Sie standen als einzige noch auf eigenen Werten: Grund `#EFEAE2`,
Schrift `#141210`, Titel in **Anton** — einer schmalen Grotesk, die
mit dem Rest nichts zu tun hat.

    Farben   grundA / schriftA aus dem Block
    Titel    ablaufTitel (HelveticaNeueBrand) in
             ablaufTitelGewicht (700)

Das Monogramm faellt weg, wie bei den anderen Kacheln (Abschnitt 26):
`ht()` zeichnet es, sobald `monogrammFarbe` gesetzt ist.

Die Titelstaerke wird nur im Ablauf-Zweig gesetzt (dort ist `LINKS`
falsch). Der andere Zweig, der dieselbe Zeile benutzt, bleibt
unveraendert — deshalb der Spread `...(LINKS?{}:{fontWeight:…})`
statt einer festen Zuweisung.

Damit stehen alle vier Kachelarten auf demselben Block: Textkacheln,
Fotokacheln, Folgeslides, Ablauf.

### Noch nicht angefasst: die Texte

Die 23 Ablauf-Texte stehen als feste Zeichenketten im Bundle. "Die
Ansprache authentischer" heisst, sie neu zu schreiben — Struktur
(Kopfzeile, Titel, Unterzeile, Liste/Stationen, Fliesstext) bleibt,
der Ton aendert sich. Das ist Redaktion an ihrer Stimme, nicht am
Aussehen, und wird erst nach ihrer Freigabe eines Musters gemacht.

## 73. Das letzte Overlay ausserhalb des Systems

Liegt eine Ablauf-Folie auf einem Foto, bekam sie einen eigenen
Verlauf, fest im Bundle:

    rgba(18,16,14, .62 / .38 / .66)

Kalter Ton, oben wie unten mehr als 60 Prozent Abdunklung. Waehrend
die Fotokacheln seit Abschnitt 63 bei .05/.10/.42 in warmem Ton
liegen, stand hier noch der alte Wert — das Bild war praktisch nicht
mehr zu sehen.

Ablauf-Folien tragen viel kleinen Text und brauchen mehr Halt als eine
Ueberschrift, deshalb eigene Werte statt derselben:

    ablaufTiefeOben    .30
    ablaufTiefeMitte   .22
    ablaufTiefeUnten   .42

Der Ton kommt aus `bildTon`, also derselbe warme Braunton wie ueberall
sonst. Damit liegt kein Verlauf mehr ausserhalb des Blocks.

## 74. Die Ansprache der Ablauf-Texte

Dreiundzwanzig feste Texte in drei Feldern: Das Intensive (6), The
Money Room (7), Mentoring (10).

**Der Ablauf bleibt unangetastet.** Kopfzeile, Titel, Unterzeile und
die Listen- beziehungsweise Stationeneintraege stehen Zeichen fuer
Zeichen wie vorher. Neu ist nur die letzte Zeile jedes Textes, der
Fliesstext.

Was sich aendert:

- **Die Doppelverneinung faellt weg.** "Nicht besprochen, nicht
  analysiert, sondern umgebaut" stand in fast jedem Absatz. Das ist
  Werbetext, keine Sprechweise.
- **Dafuer ein konkretes Bild aus der Sache selbst**, etwa "ich tippe
  mit, du siehst zu, wie sich die Sätze verändern".
- **An zwei Stellen ein Eingestaendnis statt einer Behauptung:** "Ich
  habe das lange anders geglaubt" und "das ist der unangenehme Teil".
- **Einmal etwas gegen das eigene Interesse gesagt:** "Und wenn der
  Money Room besser passt, sage ich dir das, statt dir die Sitzung zu
  verkaufen."

### Nachweis

Alle drei Felder werden als Ganzes ersetzt. Vor dem Ersetzen wurde die
Rekonstruktion gegen das Original geprueft: mit den **alten** Texten
ergibt sie Zeichen fuer Zeichen dieselbe Zeile. Danach wurde das
Ergebnis gegengelesen:

    23 von 23   Kopfzeile, Titel, Unterzeile, Liste unveraendert
    23 von 23   Fliesstext neu
    Zahlen      identisch (888, 444, 97, 3, 12, 8, 14, 2)

Preise, Fristen, Platzzahlen und Bedingungen sind damit nachweislich
dieselben geblieben.

## 75. Der Wechsel fett/leicht war weg, sobald der Text nur einen Satz hat

Die Trennung in ersten und zweiten Block haengt an einer Satzgrenze:

    /^(.{10,90}?[.!?:])\s+(.*)$/

Bis Abschnitt 65 gab es daneben die Kappung auf eine Zeile: was nicht
in die erste Zeile passte, rutschte in den zweiten Block. Damit gab es
**immer** zwei Bloecke — dafuer mitten im Wort getrennt, was zu Recht
bemaengelt wurde. Die Kappung ist weg, und mit ihr bei einsaetzigen
Texten auch der Wechsel. Ihre Kacheln bestehen fast alle aus einem
Satz, also stand alles in fettem Fraunces.

Neue Reihenfolge:

1. eigene Zeilenumbrueche im Text
2. Satzgrenze
3. **Satzteilgrenze** — das Komma oder die Konjunktion (und, aber,
   weil, denn, damit, sondern, oder), die der Mitte am naechsten
   liegt, und nur zwischen 25 und 78 Prozent der Laenge, damit kein
   Zweizeiler mit einem einzelnen Wort dahinter entsteht
4. sonst gar nicht — kurze Saetze bleiben ein Block

`teilungAb` (52 Zeichen) legt fest, ab welcher Laenge ueberhaupt
geteilt wird.

Getrennt wird damit dort, wo man auch beim Sprechen Luft holt. An
ihren echten Texten geprueft (die Regel aus dem gebauten Bundle
geschnitten und in node laufen lassen):

    Wie kommst du in die Energie,          / aus der heraus verkauft wird?
    Scham ist der teuerste Zustand,        / in dem du arbeiten kannst.
    Es gibt eine Skala fuer …zustaende     / und sie erklaert mehr ueber …
    Alles, was gerade in deinem Leben ist, / hast du dorthin gebracht.
    Ich glaub nicht an positives Denken.   / (bleibt ein Block)

## 76. Zeilen liefen wieder ueber den Rand — derselbe Speicher

Auf ihren Kacheln waren einzelne fette Zeilen rechts abgeschnitten
("Es gibt eine Skala fi", "Du kannst niemanden auf ein"), andere nicht.

Nachgerechnet ist die Umbruchrechnung sauber: bei Spalte .82 endet die
breiteste Zeile bei 693 bis 739 von 800 Pixeln, also gut innerhalb.
Und Messen und Zeichnen benutzen dieselbe Familie, dasselbe Gewicht,
dieselbe Groesse — es kann nur auseinanderlaufen, wenn die **Messung**
aus dem Zeichenbreiten-Speicher von Fabric kommt und dort noch die
Masse der Ersatzschrift liegen. Das ist der Fehler aus Abschnitt 48,
diesmal fuer Fraunces, das erst seit karten109 benutzt wird.

Abschnitt 48 leert den Speicher, bevor **die Vorschau** zeichnet. Das
deckt aber nur ihre eigene Zeichnung ab. Jede andere Leinwand, die
frueher zeichnet — Bildexport, Vorschaustreifen, was auch immer —
fuellt ihn danach wieder mit Ersatzmassen.

Deshalb jetzt zusaetzlich global und einmalig:

    document.fonts.addEventListener("loadingdone",
      () => fabric.util.clearFabricFontCache())

Sobald der Browser mit dem Laden **irgendeiner** Schrift fertig ist,
faellt der Speicher weg. Danach misst jede Leinwand neu, egal welche
vorher zu frueh gezeichnet hat.

## 77. Im Raster sah alles gleich aus

Abschnitt 67 hat die rotierende Vorgabe ["unten","mitte","oben"]
entfernt, damit die Bildanalyse ueberhaupt zum Zug kommt. Die
Bildanalyse liefert aber bei aehnlichen Fotos — dieselbe Person,
dieselbe Haltung, dieselbe Kameraposition — immer dieselbe ruhige
Zone. Im Raster stand der Text dadurch auf jeder Fotokachel an
derselben Stelle.

Beide Wuensche gleichzeitig, in dieser Reihenfolge:

1. **Ihre Wahl** im Tagesmenue gilt unveraendert.
2. Sonst eine **feste Streuung** ueber unten / mitte / oben, berechnet
   aus der Bildadresse. Fest heisst: dasselbe Bild bekommt immer
   dieselbe Lage, es springt nicht bei jedem Zeichnen.
3. Die **Bildanalyse ist jetzt die Wache**, nicht die Entscheidung:
   liegt in der gestreuten Reihe ein Gesicht, gilt statt ihrer die
   ruhige Zone.

`lagenWechsel` auf 0 schaltet die Streuung ab, dann entscheidet wieder
allein die Analyse.

Geprueft an ihren zehn letzten Texten (Regel aus dem gebauten Bundle
geschnitten, in node gelaufen): 4 oben, 2 mitte, 4 unten. In der App
wird die Bildadresse genommen, nicht der Text — dort streut es noch
gleichmaessiger, weil sich Fotos staerker unterscheiden als Saetze.

## 78. Mehr Textkacheln im Raster

Ob ein Tag ein Foto bekommt, entschied eine feste Regel:

    tS = e => { const t = (e%10+10)%10; return !(t===4 || t===9) }

Von zehn Tagen bekommen acht ein Bild, zwei bleiben Text. **Zwanzig
Prozent** — im Raster verschwinden die zwischen den Fotos.

Der Anteil steht jetzt im Block. `textAnteil` ist der Anteil der Tage
**ohne** Foto, in Prozent:

    (pt*37+13) % 100 >= textAnteil   ->  Foto

Der Multiplikator 37 ist teilerfremd zu 100, die Reihe laeuft also
einmal durch alle Werte, bevor sie sich wiederholt. Nachgerechnet:

    textAnteil 20   20 von 100, nie zwei hintereinander
    textAnteil 35   35 von 100, nie zwei hintereinander   <- eingestellt
    textAnteil 40   40 von 100, gelegentlich zwei hintereinander

Bei 35 kommt im Schnitt alle zwei bis drei Tage eine Textkachel, und
es stehen nie zwei nebeneinander. Die ersten dreissig Tage:

    T F F T F F F F T F F T F F T F T F F T F F T F T F F T F F

`textAnteil` auf 0 stellt die alte Regel wieder her.

## 79. Textkacheln auf mindestens zwei zu eins

    textAnteil   35  ->  67

Nachgerechnet ueber hundert Tage:

    67 von 100 Textkacheln          Verhaeltnis 2,03 : 1
    laengste Reihe Textkacheln       4
    laengste Reihe Fotokacheln       1
    Verteilung auf die drei Spalten  24 / 21 / 22

Zwei Punkte, die dabei zaehlen: Fotos stehen nie zwei nebeneinander,
bleiben also Akzente. Und die Spalten sind gleichmaessig belegt — eine
Regel mit Periode 3 (etwa `pt%3`) haette im dreispaltigen Raster einen
senkrechten Streifen aus Fotos ergeben, weil sich Periode und
Spaltenzahl decken. Der Multiplikator 37 vermeidet das.

Die ersten sechsunddreissig Tage:

    T T F T T F T F T T F T T F T F T T F T T F T T T T F T T F T T F T F T

## 80. Schrift auf Fotos reinweiss

Der Stil "montserrat", auf dem alle Fotoslides laufen, setzt

    schriftFarbe: "#F6F1E6"

also ein warmes Elfenbein, kein Weiss. Auf dem Foto liest sich das als
leicht vergilbt, besonders neben dem echten Weiss des Schildchens.

    fotoSchriftFarbe   #FFFFFF

wird gesetzt, sobald ein Foto im Spiel ist — an derselben Stelle, an
der die Fotokacheln ohnehin ihre Eigenheiten bekommen (kein Kasten,
fett und leicht). Der Wert ueberschreibt `tt.schriftFarbe`, damit
greift er auf alle Zeilen, ohne dass jede Zeichenstelle einzeln
angefasst werden muss.

Kacheln ohne Foto behalten ihre Farben aus dem Farbpaar.

## 81. Oranger Lichtsaum am Bildrand

Ein radialer Verlauf ueber dem Foto: in der Mitte durchsichtig, an den
Raendern orange. Er gibt dem Bild Licht von aussen, statt es
einzufaerben, und bindet die Fotokacheln farblich an die warmen
Textkacheln.

    saumTon       217,123,43
    saumMitte     .18          bei 55 Prozent des Radius
    saumStaerke   .62          aussen

Er liegt **ueber** dem Tiefenverlauf. Anders herum waeren die Ecken
erst abgedunkelt und dann eingefaerbt worden — das Orange soll auf dem
fertigen Bild sitzen, nicht darunter.

`saumStaerke` auf 0 schaltet ihn ab.

### Verworfen: der Rahmen rundum

Ein orangener Rahmen um jede Kachel wurde gebaut und im Raster
angesehen. Einzeln sieht er ordentlich aus; zu fuenfzehnt nebeneinander
wird jede Kachel zur Briefmarke, und die Rahmen reden mehr als die
Inhalte. Der Saum macht dasselbe, ohne eine Kante zu ziehen.

## 82. Der Tiefenverlauf faellt weg, der Saum bleibt

    tiefeOben    .05  ->  0
    tiefeMitte   .10  ->  0
    tiefeUnten   .42  ->  0

Zwei Verlaeufe uebereinander sind einer zu viel: der Tiefenverlauf
dunkelt ab, der Saum faerbt ein, und zusammen nehmen sie dem Bild
genau das Licht, wegen dem der Saum da ist.

Der Saum uebernimmt die Aufgabe des Tiefenverlaufs mit, weil er zu
allen Raendern hin dichter wird — auch nach unten, wo der Text steht.
Dazu kommt der Schatten, den der Zeichner ohnehin setzt, sobald keine
Flaeche unter dem Text liegt.

**Wo es kippen kann:** ein Foto, das unten links sehr hell ist (weisse
Wand, heller Himmel). Dort traegt weisse Schrift nur noch ueber Saum
und Schatten. Fuer diesen Fall in dieser Reihenfolge: `saumStaerke`
hoeher, oder `tiefeUnten` wieder auf einen kleinen Wert wie .15 —
nicht auf .42.

## 83. Zwei Sachen an den Fotos: Schaerfe und der Umbruch

### Die Bilder waren zu weich — mein Fehler aus Abschnitt 68

Beim Speichern werden die Fotos verkleinert, damit der Plan in die
IndexedDB passt. Ich hatte `bildKante` auf **1350** gesetzt, mit der
Begruendung "das ist die Hoehe des Exports". Das war falsch gerechnet:

    Vorschau auf dem Telefon   800 CSS-Pixel x 3 (Retina)  = 2400
    Export ueber downloadImage 1080 x multiplier 2          = 2160

Die Vorschau zeichnet also auf **2400** Bildpunkte. Ein 1350 Pixel
breites Bild wird darauf um das 1,8-fache hochgerechnet — und sieht
genau so weich aus, wie es aussah.

    bildKante   1350  ->  2000
    bildGuete   .85   ->  .82

2000 deckt beide Faelle knapp ab. Die etwas niedrigere Qualitaet
gleicht den Zuwachs teilweise aus; unterm Strich rund doppelt so viele
Bytes wie mit 1350, aber immer noch ein Bruchteil der
Kameraaufloesung.

### Der Umbruch lief wieder ueber den Rand

Ihr Fall nachgemessen: "Du kannst niemanden auf ein Niveau ziehen,"
bei Umbruchgrenze 637 und Groesse 109. Beide Messwege — Canvas
`measureText` und `fabric.Text.width` — ergeben dieselben Breiten
(561, 612, 371, 376, 389) und denselben Umbruch:

    Du kannst / niemanden / auf ein / Niveau / ziehen,

Auf ihrem Bildschirm stand aber

    Du kannst / niemanden auf ein / Niveau ziehen,

"niemanden auf ein" misst rund **1030** Pixel. Das haette nie in 637
gepasst. Beim Umbruch wurde also mit einer viel schmaleren Schrift
gerechnet als beim Zeichnen — der Ersatzschrift aus dem
Zeichenbreiten-Speicher.

Die bisherigen Freigaben (48 und 76) haengen an Ereignissen: vor der
Freigabe der Vorschau, und wenn der Browser mit dem Laden fertig ist.
Beide koennen zu frueh oder zu spaet liegen, und eine einmal
gezeichnete Kachel wird davon nicht neu gezeichnet.

**Jetzt wird der Speicher am Anfang JEDER Kachel geleert.** Damit gilt
ohne Ausnahme: gemessen wird mit derselben Schrift, mit der im selben
Durchgang gezeichnet wird. Der Preis ist etwas Rechenzeit pro Kachel.
Der Gewinn ist, dass diese Fehlerklasse — dreimal aufgetreten, dreimal
anders geflickt — nicht wiederkommen kann.

## 84. Nichts wird mehr abgeschnitten — eine Notbremse statt einer Erklaerung

Dreimal habe ich die Ursache gesucht und dreimal etwas repariert, was
es nicht war:

    48   Zeichenbreiten-Speicher vor der Freigabe der Vorschau leeren
    76   zusaetzlich global, wenn der Browser fertig geladen hat
    83   zusaetzlich am Anfang jeder Kachel

Es kam trotzdem wieder. Und die Rechnung sagt weiterhin, dass es
passen muesste: bei Umbruchgrenze 637 und Groesse 109 messen Canvas
und Fabric identisch, und der Umbruch faellt richtig aus.

Deshalb jetzt keine weitere Ursachensuche, sondern eine **Garantie im
Zeichner**:

    zF = Platz zwischen den Raendern / breiteste gezeichnete Zeile
         (hoechstens 1)

Vor dem Zeichnen wird jede Zeile so gemessen, wie sie gezeichnet wird
— dieselbe Familie, dasselbe Gewicht, dieselbe Groesse. Ist die
breiteste breiter als der Platz, wird der **ganze Block** mit
demselben Faktor verkleinert. Gleichmaessig, damit nicht einzelne
Zeilen kleiner werden als andere (der Fehler aus Abschnitt 45).

Warum das trägt, auch wenn die Ursache unbekannt bleibt: Messung und
Zeichnung liegen im selben Durchgang. Selbst wenn die Schrift in
diesem Moment die falsche ist, ist sie es fuer beide. Eine Zeile kann
danach rechnerisch nicht mehr ueber den Rand ragen.

`zF` ist 1, sobald die Anpassungsschleife ihre Arbeit getan hat — im
Normalfall aendert sich also nichts.

Dieselbe Idee wie das `maxB` im Zeichner der Textkacheln, das es dort
seit jeher gibt. Der Fotozweig hatte es nie.

## 85. Der Saum sitzt in zwei diagonalen Ecken und ist orange-rosa

Statt eines Rings rundum jetzt **zwei** radiale Verlaeufe, je einer in
einer Ecke, und zwar in zwei diagonal gegenueberliegenden.

    saumTon      232,131,107   orange-rosa, kein reines Orange
    saumStaerke  .62           in der Ecke
    saumMitte    .22           bei 55 Prozent des Radius
    saumWeite    .62           Radius als Anteil der laengeren Seite

Welches Eckenpaar drankommt, entscheidet dieselbe feste Streuung wie
bei der Textlage: eine Zahl aus der Bildadresse. Gerade heisst oben
links und unten rechts, ungerade oben rechts und unten links. Dasselbe
Bild bekommt immer dieselben Ecken — es springt nicht bei jedem
Zeichnen, und im Feed wechselt es von Post zu Post.

Zwei Ecken statt eines Rings hat einen Nebeneffekt, der hier hilft:
die beiden freien Ecken bleiben unberuehrt, das Bild wirkt weniger
eingefaerbt und mehr angeleuchtet.

## 86. Das Bild soll durchkommen

    saumStaerke   .62  ->  .30
    saumMitte     .22  ->  .08
    saumWeite     .62  ->  .58
    bildKante    2000  -> 2400
    bildGuete     .82  ->  .84

**Der Saum** war halb deckend in der Ecke — das ist kein Lichtschein
mehr, das ist eine Einfaerbung. Bei .30 liegt er als Hauch auf dem
Bild, und die Mitte bleibt praktisch unberuehrt (.08 statt .22).

**Die Schaerfe** hat eine harte Grenze, die nicht im Zeichner liegt,
sondern im Speicher: die Vorschau zeichnet auf einem Telefon mit
dreifacher Pixeldichte auf **2400** Bildpunkte. Ein Foto, das kleiner
gespeichert ist, wird hochgerechnet, und keine Einstellung im Zeichner
holt das zurueck.

    bildKante 2400 = genau die Breite, auf die die Vorschau zeichnet

**Wichtig:** das gilt nur fuer Fotos, die ab jetzt gespeichert werden.
Was mit bildKante 1350 abgelegt wurde (Abschnitte 68 bis 83), ist auf
1350 heruntergerechnet und bleibt es. Diese Bilder muessen neu
zugewiesen werden, sonst bleiben sie weich.

## Verworfen: das Orange-Rad

Fuenf Abstufungen von Creme bis Espresso als Grundfarben der
Textkacheln. Gebaut wurde es nie, nur gezeigt. Bleibt bei den zwei
Farbpaaren.

## 87 — "Tag 8 ist perfekt, der Rest ist mit overlay blass"

Der Unterschied liegt nicht am Bild, nicht an der Ecke und nicht an der
Schaerfe, sondern an **einem Wert, der auf der Kachel gespeichert ist**.

Ueber jedem Foto liegen fuenf Ebenen. Vier davon sind auf jeder Kachel
gleich: die Filterkette der App (Kontrast .07, Saettigung .3, Aufhellung
.13), die warme Lasur, der Kantenverlauf oben und unten, der Saum in den
zwei Ecken. Die fuenfte — das flache Abdunkeln — ist es nicht:

    t.overlay gesetzt        ->  genau dieser Wert
    editorialDark            ->  0
    bildVerblasst            ->  .55
    sonst                    ->  .05

Und die **automatische Bildzuweisung schreibt jeder Folie ein overlay
mit**: `.2`, wenn die Bildanalyse geklappt hat, sonst `.25`. Eine Kachel,
deren Bild nicht ueber die Zuweisung kam, hat kein overlay und landet bei
`.05`. Das ist Tag 8.

Gemessen im Vollaufbau (`tools/.pruefen/schleier.html`, dasselbe Foto,
alle fuenf Ebenen, Bildmitte):

| flaches Abdunkeln | Mittel | Streuung | hellstes |
|---|---|---|---|
| .05 (Tag 8) | 143 | **24.1** | 187 |
| .20 (auto) | 132 | 20.4 | 167 |
| .25 (auto) | 128 | **19.2** | 162 |
| .55 (Folgefolie) | 104 | **11.9** | 125 |

Ein Fuenftel Kontrast weg und die Lichter um 25 Stufen gedeckelt — genau
das sieht man als blass.

**Der Umbau:** der Wert kommt jetzt aus dem Block, nicht mehr von der
Kachel.

    bildSchleier              .05   Deckel fuer jede Fotokachel
    bildSchleierWiederholung  .28   Folgefolie, die das Bild erbt

`bildSchleier` deckelt: keine Kachel kann dunkler verschleiert werden als
der Block erlaubt, weniger darf sie. Damit ist es egal, was die
Zuweisung einmal gespeichert hat.

Die `.55` ist **kein Versehen**: sie gehoert zu einer Folgefolie, die das
Bild des Deckblatts noch einmal zeigt (`bildVerblasst` wird nur wahr, wenn
die Folie keinen eigenen Hintergrund hat und den des Deckblatts erbt).
Ohne Abdunkeln waere sie eine Wiederholung statt eines Hintergrunds.
Angesehen in `tools/.pruefen/wiederholung.html`, Text in der Mitte, also
ohne Hilfe vom Kantenverlauf: bei .55 ist das Bild fast weg, bei .20 ist
es so stark wie das Deckblatt, bei **.28** kommt es durch und die weisse
Fraunces traegt noch.

Der Weichzeichner-Pfad bleibt ausgenommen. Dort traegt die `.42` den Text
ueber dem unscharfen Bild.

**Absichtlich nicht angefasst:** Lasur, Kantenverlauf und Filterkette.
Die liegen auf *jeder* Kachel, auch auf Tag 8 — und Tag 8 ist perfekt.
Was auf Tag 8 gleich ist, kann nicht die Ursache sein. `kanteOben` und
`kanteUnten` stehen trotzdem jetzt im Block, damit der Kantenverlauf
spaeter an einer Stelle aenderbar ist; die Werte sind unveraendert
(.34 / .40).

### Zwei Dinge zur Arbeitsweise

**Die Vergleichsseite von gestern war unvollstaendig.** `klar.html` hat
nur Bild, Tiefenverlauf und Saum gezeichnet — das flache Abdunkeln, die
Lasur und den Kantenverlauf nicht. Deshalb sah der Saum-Vergleich sauber
aus, waehrend die App weiter blass war. `schleier.html` zeichnet jetzt
alle fuenf Ebenen.

**karten146 ist ein Delta auf karten145, kein voller Durchlauf.** Der
unveraenderte Drop, auf den Eintrag 1 von `bundle-patchen.py` zeigt
(`rgba(18,16,14,0.16)`), liegt nicht mehr auf der Platte; ein voller
Durchlauf bricht dort ab. Die vier Ersetzungen wurden einzeln auf
"genau einmal" geprueft und danach aus der gebauten Datei wieder
herausgegriffen, und die Datei wurde als ES-Modul auf Syntax geprueft.
`bundle-patchen.py` traegt Eintrag 87 trotzdem, damit der naechste Drop
ihn wieder mitbekommt.
