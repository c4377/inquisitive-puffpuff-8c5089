# Einbau in das Repo — nicht für Drop

Repo: `c4377/inquisitive-puffpuff-8c5089`, Branch `main`, Build `vite build`.

## Sofort committen, unverändert

| Datei | Ziel im Repo |
|---|---|
| `write-reminder.mjs` | `netlify/functions/write-reminder.mjs` |
| `write-caption.mjs` | `netlify/functions/write-caption.mjs` |

Beides ist echter Quelltext, kein Build nötig. Beide brauchen
`GEMINI_API_KEY` in den Netlify-Umgebungsvariablen.

`write-reminder` schreibt die zwei Fassungen und verwirft jeden Text,
der zu lang ist, kein Sternchenpaar hat oder Ausrufe- und
Anführungszeichen enthält.

`write-caption` nimmt zusätzlich `art` (1, 2 oder 3) und `stories`
(true/false) entgegen und gibt neben `caption` ein Feld `stories` mit
fünf Einträgen zurück.

## Muss verdrahtet werden

`kartenzeichner.js` — die Farbtafel und der Zeichner für die
Reminder-Folien. Gehört nach `src/utils/`, aufgerufen aus dem
Kartenpfad in `canvasRenderer.js`.

Erwartet im Gültigkeitsbereich: `fabric`, `e` (Canvas), `r` (Breite),
`n` (Höhe), `c` (Skalierung).

Vor dem Zeichnen muss Playfair geladen sein, kursiv eingeschlossen:

```js
await Promise.all([
  document.fonts.load('400 40px "Playfair Display"'),
  document.fonts.load('italic 400 40px "Playfair Display"'),
]);
```

Ohne das misst Fabric mit der Ersatzschrift, hält zu breite Zeilen für
passend, und der Text läuft über den Rand. Das war ein echter Fehler,
kein theoretischer.

## Was im Repo fehlt

Der Quellcode auf `main` ist deutlich älter als die laufende App. Nicht
vorhanden sind unter anderem: Reminder-Folien, `reminderArt`, der
Kartenpfad (`istKarte`), die Bandzeile (`nurErsteZeilePlatte`), das
Monogramm, sowie sechs der acht Netlify-Funktionen.

Solange der neuere `src` vom Rechner nicht im Repo ist, lässt sich
`kartenzeichner.js` nicht anschließen — es gibt keinen Kartenpfad, in
den er hineingehört. Die zwei Funktionen oben gehen trotzdem sofort.

## Weitere Änderungen, die nur im gebauten Bundle stecken

Diese sind in `src` noch nicht abgebildet und müssen beim Zusammenführen
mitgedacht werden:

- Zeilenumbrüche und Leerzeilen aus dem Textfeld werden gesetzt statt
  zu Leerzeichen zusammengefaltet
- Steht ein Umbruch im Feld, ist die erste Zeile die Bandzeile
- Ein Tag ist entweder Fotopost oder Kartenpost, nie gemischt
- Kartentage nach festem Muster, drei von sieben
- Kein Seitenzähler mehr
- Bildprompts auf Schiefergrau statt warmem Gold
- Kachelknöpfe „Headline" und „Normal/Groß" liegen unter der Vorschau
  statt darüber
- Anzeige der geladenen Bundle-Datei im Kopf statt des Build-Datums
