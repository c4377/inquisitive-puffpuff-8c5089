# Einspielen — wie dieses Projekt gebaut und veröffentlicht wird

Der Publish-Skill in `.claude/skills/publish` liest diese Datei zuerst.
Was hier steht, gilt vor seinen allgemeinen Regeln.

## Ausgangslage

Netlify baut nichts. Veröffentlicht wird der Ordner `site/` genau so, wie er im
Repo liegt (`netlify.toml`: `publish = "site"`, `command = ""`). Ein Push auf
`main` löst den Deploy aus.

Die App selbst ist eine einzige gebaute Datei: `site/assets/index-B5kartenNNN.js`.
Einen React-Quellcode dazu gibt es nicht mehr (der alte `src/` war veraltet und
ist gelöscht, liegt aber in der Git-Historie). Die App entsteht so:

```
tools/basis/k451.js          gesicherte Grundlage (nie von Hand ändern)
  + tools/editorial-look.py  alle Änderungen am App-Code (ersetze(...)) und die Look-Einstellungen
  + tools/kontrast-zeichner.js  der Look Kontrast (Cover, Folgefolien, Fotobearbeitung)
  + tools/kontrast-ablauf.js    die Ablauf-/Zusammenarbeit-Folien
  + tools/ablauf-folien.json    Inhalte der Ablauf-Folien (Angebote laut carinaannaprav.at)
  = site/assets/index-B5kartenNNN.js
```

Neben der App liegen in `site/` kleine eigenständige Skripte, die ohne Neubau
geändert werden können: `kundenraum.js`, `freisteller.js`, `stil-schalter.js`
(Schwarz-Regler), `insta-ansicht.js`, `story-studio.js`, `kommentare.js`, die Seite
`profilbilder/` und das Feed Studio unter `v2/` (eigener Quellcode im Wurzelordner `v2/`).

## Eine Änderung an der App bauen

1. Änderung in `tools/` machen (Zeichner-Dateien: keine `//`-Kommentare, die
   Zeilenumbrüche werden entfernt).
2. Neue Nummer NNN = bisherige + 1. Bauen:

   ```
   cd site/assets
   python3 ../../tools/editorial-look.py ../../tools/basis/k451.js index-B5kartenNNN.js NNN
   node --check index-B5kartenNNN.js
   ```

3. Die bisherige Datei durch eine Weiterleitung ersetzen und alle Verweise nachziehen
   (ALT = bisherige Nummer):

   ```
   for f in $(grep -l "kartenALT\.js" index-B5karten*.js); do sed -i "s/kartenALT\.js/kartenNNN.js/g" $f; done
   echo 'import "./index-B5kartenNNN.js";' > index-B5kartenALT.js
   sed -i "s/kartenALT\.js/kartenNNN.js/g" ../index.html ../../netlify.toml
   ```

4. Prüfen:

   ```
   python3 tools/ziel-pruefen.py
   ```

   Bricht das Skript ab: **nicht einspielen.** Es prüft, dass `site/index.html` und
   die Auffangregel in `netlify.toml` auf dasselbe vorhandene Bundle zeigen und keine
   Weiterleitung ins Leere läuft. Sonst bleibt die Seite weiß.

5. In der App ansehen (lokal `cd site && python3 -m http.server 8899`), dann einen
   Abschnitt in `OFFENE-BUNDLE-AENDERUNGEN.md` ergänzen, committen, pushen.

## Warum die Datei bei jeder Änderung einen neuen Namen bekommt

`assets/*` wird ein Jahr lang als `immutable` ausgeliefert. Ein Browser lädt eine
geänderte Datei mit gleichem Namen nicht neu. Deshalb steht oben in der App neben
„BrandStudio“ der Name der geladenen Datei (z. B. `karten547`). Ändert er sich nach
dem Deploy nicht, hängt der Browser an einer alten `index.html`: einmal neu laden.

## Alte Dateinamen

Es bleiben nur die letzten etwa zehn Namen als Weiterleitung liegen. Ältere werden
gelöscht. Fragt ein Browser mit einer sehr alten, zwischengespeicherten `index.html`
nach einem gelöschten Namen, greift die Auffangregel in `netlify.toml`
(`/assets/index-B5karten*` → aktuelles Bundle). Deshalb muss diese Regel bei jedem
Build mitgezogen werden (Schritt 3), `ziel-pruefen.py` kontrolliert das.

Eine Datei `site/_redirects` darf es nicht geben: ihre Regeln würden vor denen aus
`netlify.toml` greifen, und die Auffangregel `/*` würde alte Bundle-Namen mit der
HTML-Seite beantworten.

## Wenn ein ZIP kommt

Carina lädt manchmal einen fertigen Ordner aus einer anderen Session hoch.

1. Inhalt nach `site/` kopieren, nicht ins Wurzelverzeichnis.
2. `rsync -a` ohne `--delete`: Fehlt eine Datei im ZIP, wird sie nicht gelöscht.
3. `.claude/`, `tools/` und `netlify/functions/` dabei nicht überschreiben, ohne
   genau hinzusehen. `netlify/functions/*.mjs` ist echter Quelltext.
4. Kommt ein neues Bundle im ZIP, ist es außerhalb von `tools/` entstanden: Carina
   fragen, ob die Änderung in `tools/` nachgezogen werden soll, sonst geht sie beim
   nächsten Build verloren.

## Netlify-Funktionen

`netlify/functions/*.mjs` (Story-Studio, Kommentare, Pins, Reminder, Stories, Bilder,
Webinar, Ads). Sie brauchen keine npm-Pakete. Der Schlüssel `GEMINI_API_KEY` steht
in den Netlify-Umgebungsvariablen, nie im Repo.

## Adresse

https://inquisitive-puffpuff-8c5089.netlify.app
