---
name: publish
description: Änderungen an diesem Projekt live stellen — direkt bearbeitete Dateien oder ein ZIP, das Carina aus einer anderen Session hochgeladen hat. Nutze das, wenn sie "publish", "publishe", "veröffentliche", "stell das online", "mach das live", "einspielen" sagt oder ein ZIP mit Projektdateien anhängt — auch mitten im Gespräch, ohne Slash-Befehl.
---

# Publish — Änderungen live stellen

Carina sagt "publish" → die aktuellen Änderungen werden committet und gepusht,
der Hoster baut neu, kurz darauf ist es online.

Carina ist die Eigentümerin. "Publish" ist ihre Freigabe — frag nicht nochmal nach,
mach es und berichte kurz, was passiert ist. Antworte auf Deutsch, ohne Fachjargon.

## Schritt 0 — Projekt einmal einordnen

Dieser Skill liegt in mehreren Repos. Schau **zuerst** nach, womit du es zu tun hast:

```bash
ls netlify.toml vercel.json app.json package.json 2>/dev/null
git remote -v
git branch --show-current
git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo "origin/main"
```

- **`netlify.toml` vorhanden** → Netlify-Website. Push auf den Standard-Branch
  (meist `main`) veröffentlicht. Schau in `netlify.toml` nach `[build] command` —
  gibt es einen Build-Schritt, führt Netlify ihn selbst aus.
- **`vercel.json`** → dasselbe Prinzip mit Vercel.
- **`app.json` mit `expo`** → Mobile-App (z.B. aus Rork). Ein Push veröffentlicht
  hier **nichts** von selbst. Sag ihr das ehrlich: die Änderung liegt dann auf
  GitHub, aber der App-Store-/Expo-Weg ist ein eigener Schritt. Nicht so tun,
  als wäre es live.
- **nichts davon** → nachsehen, ob im README steht, wie veröffentlicht wird.
  Findest du nichts: committen und pushen, und ihr sagen, dass du keinen
  automatischen Veröffentlichungsweg gefunden hast.

Steht in `README.md` oder `EINSPIELEN.md` etwas zum Veröffentlichen, gilt das
vor diesen allgemeinen Regeln.

## Fall A — hier bearbeitete Dateien

### 1. Schauen, was sich geändert hat
```bash
git status --short
git diff --stat
git log --oneline @{u}..HEAD 2>/dev/null
```
Keine Änderungen? Dann nichts pushen, sondern sagen:
"Es gibt gerade nichts zu veröffentlichen — es ist schon alles online."

### 2. Sicherheitscheck (nie überspringen)
```bash
git diff; git diff --cached
```
**Nicht veröffentlichen**, wenn im Diff auftaucht:
- Schlüssel oder Tokens: `sk-ant-`, `sk_live_`, `ghp_`, `AC_API_KEY=`,
  `STRIPE_SECRET_KEY=`, `TELEGRAM_BOT_TOKEN=`, lange Zufallszeichenketten
  hinter `key`, `token`, `secret`, `password`
- eine `.env`-Datei oder echte Zugangsdaten

Dann stoppen, ihr in einem Satz sagen, welche Datei das Problem ist, und
anbieten, den Wert stattdessen als Umgebungsvariable beim Hoster zu setzen.

**Zusätzlich prüfen, ob Schutzmechanismen wegfallen:**
- Werden in `netlify.toml` / `_redirects` / `vercel.json` Regeln entfernt oder
  überschrieben, die Ordner sperren (`privat/`, `admin/`, `intern/`, alles mit
  Status 404 oder Passwortschutz)? → **stoppen und nachfragen.** Solche Regeln
  schützen oft bezahlte Inhalte. Fallen sie weg, sind die Dateien öffentlich.
- Werden Dateien aus einem gesperrten Ordner in einen öffentlichen verschoben?
  → ebenfalls stoppen.

### 3. Committen
```bash
git add -A
git commit -m "Preise auf der Startseite aktualisiert"
```
Deutsche Nachricht, ein Satz, beschreibt die Änderung aus Sicht der Website —
nicht "neu", nicht "update".

### 4. Pushen
Veröffentlicht wird der Standard-Branch (aus Schritt 0, meist `main`).

```bash
git checkout main
git merge --ff-only <arbeits-branch>   # nur falls auf einem anderen Branch gearbeitet wurde
git push -u origin main
```

- Netzwerkfehler: bis zu 4-mal wiederholen (2s, 4s, 8s, 16s Pause).
- `non-fast-forward`: erst `git pull --rebase origin main`, dann nochmal pushen.

### 5. Bescheid geben
> Online gestellt: **[was geändert wurde]**
> Der Hoster baut gerade neu — in ein bis zwei Minuten sichtbar auf [Adresse].
> (Handy: Seite einmal neu laden.)

Die Adresse steht meist im README oder in der `sitemap.xml`.

## Fall B — Carina hat ein ZIP hochgeladen

Kommt vor, wenn eine andere Claude-Session **ohne** angehängtes Repo gearbeitet
hat: dann gibt es das Ergebnis dort nur als Download.

> Sag ihr einmal beiläufig: startet sie die Session mit ausgewähltem Repository,
> kann Claude dort direkt committen — dann entfällt das ZIP komplett.

### B1. ZIP finden
```bash
ls -lt ~/*.zip /mnt/user-data/uploads/*.zip ./*.zip 2>/dev/null | head
```

### B2. Auspacken — in einen Nebenordner, nie direkt ins Projekt
```bash
rm -rf /tmp/publish-zip && mkdir -p /tmp/publish-zip
unzip -q "<ZIP-PFAD>" -d /tmp/publish-zip
find /tmp/publish-zip -type f | head -50
```
Steckt alles in einem Unterordner (`site/`, `dist/`, `website/`), ist **dessen
Inhalt** das Gemeinte, nicht der Ordner selbst.

### B3. Vergleichen, bevor überschrieben wird
```bash
diff -rq /tmp/publish-zip/<wurzel> . -x .git -x .claude -x node_modules
```
Sag ihr je einen Satz zu: **geändert**, **neu**, **fehlt im ZIP**.

**"Fehlt im ZIP" heißt nicht löschen.** Die andere Session kannte oft nur einen
Ausschnitt. Lösch nie Dateien, nur weil sie im ZIP fehlen — außer sie sagt es
ausdrücklich.

### B4. Kopieren
```bash
rsync -a --exclude .git --exclude .claude --exclude node_modules /tmp/publish-zip/<wurzel>/ .
```
(kein `--delete`)

Dann weiter bei **Fall A, Schritt 2** — der Sicherheitscheck ist hier besonders
wichtig, weil der Inhalt aus einer Session kommt, die das Projekt nicht kannte.

### B5. Vor dem Push gegenprüfen
- Liegen Bilder und Schriften noch richtig (`img/`, `fonts/`)?
- Wurden `netlify/functions/*` überschrieben? Dort hängen Zahlungen,
  Mail-Anbindung und Benachrichtigungen dran — genau hinschauen.
- Gibt es einen Build-Schritt, lauf ihn einmal durch, bevor du pushst:
  `node <build-datei>.mjs` bzw. `npm run build`. Bricht er ab: nicht pushen.
- Sind interne Links noch intakt?

Fällt etwas auf: **nicht pushen**, sondern sagen, was dir aufgefallen ist.

## Wichtig
- **Kein Pull Request.** Carina will veröffentlichen, nicht reviewen lassen.
- **Nichts mitverändern**, was gerade nicht dransteht.
- Geht der Build schief, bleibt die alte Seite online — rückgängig geht immer:
  `git revert <commit>` und nochmal publish.
