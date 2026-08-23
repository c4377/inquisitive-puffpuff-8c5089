# Einspielen — wie dieses Projekt veröffentlicht wird

Der Publish-Skill in `.claude/skills/publish` liest diese Datei zuerst.
Was hier steht, gilt vor seinen allgemeinen Regeln.

## Ausgangslage — bitte einmal lesen

Der Quellcode in `src` ist **älter als die laufende App**. Es fehlen
unter anderem: die Reminder-Folien, der Kartenpfad, die Bandzeile und
sechs der acht Netlify-Funktionen. Ein neuerer `src` existiert nicht —
weder hier noch auf dem Rechner.

Der aktuelle Stand der App liegt **ausschließlich als gebautes Bundle**
vor: `assets/index-*.js`. Der wird gepflegt, indem diese Datei direkt
bearbeitet wird.

Daraus folgt die Regel für dieses Repo:

> **Nicht bauen. Veröffentlicht wird der fertige Ordner.**

Wird `vite build` ausgeführt, entsteht die App aus dem alten `src` und
alles Neuere ist weg. `src` bleibt trotzdem im Repo — als Archiv, nicht
als Quelle.

## netlify.toml — so muss sie aussehen

```toml
# KEIN [build]-Block. Der Ordner "site" wird unverändert veröffentlicht.

[build]
  publish = "site"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[functions]
  directory = "netlify/functions"

[[headers]]
  for = "/index.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

Kein `command`. Steht dort wieder `npm run build`, ist das ein Fehler.

## Wenn ein ZIP kommt

Carina lädt den fertigen Ordner als ZIP hoch. Erkennbar an
`assets/index-*.js`, `fonts/`, `models/` und **keinem** `src`.

1. Inhalt nach `site/` kopieren — nicht ins Wurzelverzeichnis.
2. `rsync -a` ohne `--delete`. Fehlt eine Datei im ZIP, wird sie nicht
   gelöscht.
3. `src/`, `.claude/` und `netlify/functions/` dabei **nicht** anfassen.
4. `netlify/functions/*.mjs` aus dem ZIP separat übernehmen — das ist
   echter Quelltext und wird nicht gebaut.
5. Committen und auf `main` pushen.

Die Schrift- und Modelldateien in `fonts/` und `models/` sind binär und
müssen mit. Ohne sie misst der Zeichner mit einer Ersatzschrift, und
der Text läuft über den Rand.

## Netlify-Funktionen

Alle brauchen `GEMINI_API_KEY` in den Netlify-Umgebungsvariablen.
Fehlt der Schlüssel, antworten sie mit einem Fehler — das ist kein
Codefehler und nichts zum Reparieren.

## Wie der Deploy ausgeloest wird

Die Netlify-Seite ist mit diesem Repo verbunden. Ein Push auf `main`
loest den Deploy aus — es muss nichts mehr von Hand abgelegt werden.

Netlify liest die `netlify.toml` aus dem Repo; was im Netlify-Formular
unter Build-Befehl und Publish-Ordner steht, wird davon ueberstimmt.
Der Build-Befehl ist dort ausdruecklich leer gesetzt. Steht da je wieder
`npm run build`, wird die App aus dem veralteten `src/` gebaut und alles
Neuere ist weg.

## Adresse

https://inquisitive-puffpuff-8c5089.netlify.app

## Prüfen, ob es wirklich live ist

Oben im Kopf der App steht neben „BrandStudio" der Name der geladenen
Bundle-Datei, zum Beispiel `karten19`. Ändert er sich nach dem Deploy
nicht, hängt der Browser am Cache — `assets/*` wird ein Jahr lang als
`immutable` ausgeliefert. Dann hilft nur ein **neuer Dateiname**, kein
Neuladen. Deshalb wird die Bundle-Datei bei jeder Änderung umbenannt.
