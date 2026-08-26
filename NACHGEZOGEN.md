# Die drei offenen Bundle-Änderungen — jetzt im Quellcode

Grundlage: `OFFENE-BUNDLE-AENDERUNGEN.md` auf `main`, Bundle `karten61f`.
Basis der Dateien: `main`, Stand 26. August 2026.

## 1. Verlauf hinter Playfair auf Foto
`src/utils/canvasRenderer.js`, im Bildlade-Block direkt nach dem
vorhandenen Kantenverlauf. Neu eingefügt — im Quellcode gab es diesen
Verlauf noch gar nicht.

    0.82 / 0.58 / 0.90 statt 0.34 / 0.16 / 0.40

Bedingung: `/Playfair/.test(slide.fontFamily)` und
`slide.tiefenOverlay !== false`, damit der vorhandene Schalter greift.

**Bitte prüfen:** Ob die Kachelschrift im Quellcode wirklich über
`slide.fontFamily` ankommt. Im gebauten Bundle heißt die Variable anders.
Trägt das Feld einen anderen Namen, greift der Verlauf nicht.

## 2. Weichzeichner
`src/utils/canvasRenderer.js`, Zeile ~214. `isFollowUp` bleibt unangetastet
— es steuert auch die Abdunklung weiter unten. Daneben steht jetzt `blurAn`
mit der Streuung aus der Bildadresse; der Filter greift bei `isFollowUp ||
blurAn`. Stärke unverändert `Math.max(slide.blur || 0, 12)`.

## 3. Farbfolien in Fotoposts
`src/pages/ContentPlanner.jsx`, beide Stellen mit `hasImg` — Einzeltag und
alle Tage. Die Streufunktion steht als `streuung` oben in der Datei.

Nachgerechnet über 400 Posts à 6 Folien: **28 % Farbfolien, 13 % der Posts
ohne eine einzige.** Das Dokument nennt 33 % — die Zahl hängt daran, wie
viele Folien ein Post hat. Folie 1 behält immer ihr Foto, deshalb sinkt der
Anteil, je kürzer die Posts sind.
