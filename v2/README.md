# Feed Studio (Version 2, zum Verkaufen)

Eigenständige Version von BrandStudio, sauber aus Quellcode gebaut. Jede Kundin
bekommt ihre eigene Kopie und stellt sie selbst auf Netlify (siehe `ANLEITUNG.md`).
Es gibt kein Konto und kein Backend: Marke, Plan und Fotos liegen in IndexedDB im
Browser der Kundin. Die Sicherung läuft über eine JSON-Datei (Einstellungen).

## Befehle

```
npm install
npm run dev        # Entwicklung, http://localhost:5173
npm run build      # fertige App in dist/
npm run paket      # dist/ + Anleitung als feedstudio-paket.zip (zum Verkaufen)
```

Der Build nutzt relative Pfade (`base: "./"`). Dieselbe Version läuft deshalb
unter `/v2/` auf Carinas Seite und im Wurzelverzeichnis einer Kundinnen-Seite.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `src/lib/importParser.js` | Import „Tag / Slide / Caption / Story“, Absätze, Kicker, `/`-Zeile, Markierungen |
| `src/lib/looks.js` | Look-Vorlagen (Klassisch, Bordeaux, Bordeaux Mix, Creme) und allgemeine Regeln |
| `src/lib/planen.js` | Textposts (jeder n. Tag) und Verteilung der Fotos |
| `src/lib/store.js`, `db.js` | Speichern im Browser, Fotos verkleinern, Gesichtserkennung |
| `src/lib/export.js` | PNG, ZIP, Teilen-Menü, Sicherung |
| `src/render/` | Zeichenmaschine: Zuschnitt (Gesicht/Details), SW, Verlauf, Textsatz, Platzierung |
| `src/ui/` | Oberfläche: Einrichtung, Feed, Tages-Editor, Stories, Captions, Fotos, Einstellungen |

## Regeln der Zeichenmaschine (aus der Arbeit an BrandStudio übernommen)

- Text unter dem Gesicht. Ist dort weniger als 28 % Platz, kommt er darüber.
  Ohne Gesicht oder bei Detail-Ausschnitt ohne Gesicht steht er unten.
- Titelbild mittig, Folgefolien linksbündig im Eck, Stories mittig.
- Größenanpassung mit dem echten Zeilenabstand. Die Mindestgröße gilt nur, solange der
  Text dann noch in die freie Fläche passt.
- Detail-Ausschnitte: Folgefolien etwa jede zweite (Nah, Brust, Unten), Titelbild jedes vierte.
- Textposts jeden 2. Tag (einstellbar). Fotos im Wechsel Farbe/SW je nach Look.
- Absätze: einfacher Umbruch = neue Zeile, Leerzeile = Absatz mit Luft.

## Schriften

Nur frei lizenzierte Schriften (SIL OFL): Playfair Display, Instrument Serif, Gloock,
Bodoni Moda SC, Inter, Courier Prime, Caveat, Mrs Saint Delafield. Helvetica Neue
aus der alten App ist kaufpflichtig und darf in einem verkauften Produkt **nicht**
enthalten sein; stattdessen wird Inter verwendet.
