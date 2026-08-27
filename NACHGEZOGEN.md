# Offene Bundle-Änderungen — Stand im Quellcode

Grundlage: `OFFENE-BUNDLE-AENDERUNGEN.md` auf `main`.
Basis: `main`, frisch gezogen.

## Nachgezogen

1. **Verlauf hinter Playfair auf Foto** — `canvasRenderer.js`, im
   Bildlade-Block. 0,82 / 0,58 / 0,90. Der Verlauf existierte im
   Quellcode noch gar nicht, er ist neu.
   *Zu prüfen:* ob die Kachelschrift wirklich über `slide.fontFamily`
   ankommt. Trägt das Feld einen anderen Namen, greift die Bedingung nicht.
2. **Weichzeichner** — `canvasRenderer.js`. `isFollowUp` bleibt, weil es
   auch die Abdunklung steuert; daneben `blurAn` mit dem Keim aus der
   Bildadresse. Filter greift bei `isFollowUp || blurAn`.
3. **Farbfolien** — `ContentPlanner.jsx`, beide `hasImg`-Stellen, inklusive
   der Ausnahme für `karte === 'ablauf'` und `reminderArt === 'ablauf'`.
   Die Streufunktion steht als `streuung` oben in der Datei.
4. **Ersatzwert der Bildanalyse** — `imageAnalysis.js`, `quietZone: 7`,
   `quietLabel: 'bottom-center'`.
5. **Zone unter dem Gesicht** — `imageAnalysis.js`, `gemieden` erweitert um
   `z + 3`, mit Notausgang, falls dann alle neun Zonen wegfielen.
6. **Textspalte endet vor dem Gesicht** — `canvasRenderer.js`, `textBreite`
   aus der Gesichtsspalte, an zwei Stellen eingesetzt.
7. **Sternchen kursiv statt Farbe** — `canvasRenderer.js`, drei Stellen:
   `fill: accentColor` entfernt, `fontStyle: 'italic'` bleibt.

## Nicht nachgezogen, weil es die Stelle im Quellcode nicht gibt

- **7, Pin-Weg.** Der Pin-Zeichner mit `fillStyle` existiert in `src`
  nicht. Nur der Standardweg ist geändert.
- **8, Stationsreihe.** Die Fassung `ablauf` mit `[stationen: …]` gibt es
  im Quellcode nicht. `src/utils/kartenzeichner.js` kennt nur `zitat` und
  `aussage`. Die Änderung steckt im Bundle `karten68`.

## Zahlen zur Kontrolle

Streuung über 400 Posts à 6 Folien: **28 % Farbfolien, 13 % der Posts
ohne eine einzige.** Das Dokument nennt 33 % — der Unterschied kommt aus
der Folienzahl je Post, Folie 1 behält immer ihr Foto.
