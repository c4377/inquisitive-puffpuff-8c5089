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

## Alte Bundles entfernen

Die Regel "nichts loeschen, nur weil es im ZIP fehlt" gilt weiter — mit
einer Ausnahme, die Carina freigegeben hat: das **abgeloeste Bundle**.

Wird `assets/index-*.js` umbenannt, bleibt die alte Datei sonst liegen
und wird bei jedem Einspielen zwei Megabyte schwerer. Sie darf weg —
aber **nicht ersatzlos**.

Der Grund: im Repo verweist danach nichts mehr auf den alten Namen, im
Browser aber schon. Wer die `index.html` zwischengespeichert hat, fragt
weiter nach der alten Datei. Ist sie ersatzlos geloescht, antwortet
Netlify mit 404, und die Seite laedt gar nicht mehr — auch nicht die
neue Fassung. Genau das ist am 26. August passiert.

Deshalb: den alten Namen als **Weiterleitung** stehen lassen. Fuenf
Zeilen statt zwei Megabyte:

    import "./index-B5kartenNN.js";   // der aktuelle Name

Damit startet auch eine alte `index.html` die aktuelle App. Ein echtes
Bundle wird also durch seine Weiterleitung ersetzt, nicht geloescht.

Beim naechsten Einspielen zeigen alle vorhandenen Weiterleitungen auf
den neuen Namen — ein `sed` ueber `site/assets/index-B5karten*.js`
genuegt.

**Weiterleitungen werden nicht mehr geloescht.** Erst hiess es hier, sie
duerften nach etwa fuenf Fassungen weg. Das war falsch: niemand weiss,
wie alt die `index.html` in einem fremden Zwischenspeicher ist, und ein
Handy, das wochenlang nicht neu geladen hat, faellt sonst auf 404. Jede
Weiterleitung kostet 300 Byte — alle Namen zusammen sind ein Bruchteil
eines einzigen Bundles. Sie bleiben liegen.

Fuer alles andere gilt weiter: nicht loeschen.

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
