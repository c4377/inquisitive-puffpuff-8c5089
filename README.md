# BrandStudio

Carinas App für Instagram-Karussells: Content-Plan, Bulk Import, Cover und Folien im
eigenen Look, Captions, Stories, Export in die Fotos-App.

Live: https://inquisitive-puffpuff-8c5089.netlify.app

## Was gilt (Stand 12.10.)

- **Look „Moody“** (15.10.): Schrift Instrument Serif, Fotos dunkel mit Vignette, warm, leicht entsättigt (`kontrastFotoOriginal: 3`), Espresso #2A221E mit Lichtkegel, helle Kachel #F1EFEB mit Grau-Verlauf nach unten, Papierbogen auf Espresso, ein einziges Wort in Oxblood-Magenta #8E1838 auf hellen Flächen. Cover-Rhythmus: Foto · Espresso · Papier · Foto · Hell · Foto. (Die Kachel-Familie f7* liegt ungenutzt in `tools/kontrast-familie.js`.)
- **Gesicht auf jedem Cover.** Foto-Cover nehmen nur Fotos mit erkanntem Gesicht. Textkacheln
  tragen ein rundes Porträt mit Namen (Galerie: „Als Porträt“). Die letzte Folie zeigt das
  CTA-Foto (Galerie: „Als CTA-Foto“) unter einem Anthrazit-Overlay.
- **Fotobearbeitung:** Belichtung nach dem Gesicht, neutraler Weißabgleich, tiefes Schwarz,
  Vignette oben und unten. Der **Schwarz-Regler** unten links (Grundwert 20 %) macht dunkler
  oder heller, für alle Posts oder einen einzelnen Tag.
- **Sonderfolien:** Vorher/Nachher und Beispiel mit Screenshots (W-/T-Kennungen), Ergebnis-Folien,
  Ablauf-Folien zu den Angeboten (Intensive, Offer Incubator, Content, Das 1:1).
- **Screenshots:** getrennt in Testimonial (T-) und Work (W-), gespeichert in Supabase.
- **Freisteller:** eigene unter Settings → Freisteller (pro Gerät), sonst die eingebauten.
- **Kundenraum:** oben rechts „Mein Raum“ → „+ Neue Kundin“. Komplett getrennter Plan, eigene
  Fotos, Porträt, Freisteller und Name auf den Kacheln. Story-Studio und Kommentare sind dort aus.
- **Story-Studio:** schreibt Stories in Carinas Stimme, die eigene Geschichte nur sparsam.

## Dateien

| Wo | Was |
|---|---|
| `site/` | wird unverändert veröffentlicht (Netlify baut nichts) |
| `site/assets/index-B5kartenNNN.js` | die App, gebaut aus `tools/` |
| `site/*.js` | eigenständige Zusätze: Kundenraum, Freisteller, Schwarz-Regler, Instagram-Ansicht, Story-Studio, Kommentare, Heute posten, Cover-Export |
| `site/profilbilder/` | Seite für runde Profilbilder |
| `site/v2/` + `v2/` | Feed Studio, die Version zum Verkaufen (gebaut + Quellcode) |
| `tools/` | Build: Grundlage `basis/k451.js`, `editorial-look.py`, Kontrast-Zeichner, Ablauf-Folien, `ziel-pruefen.py` |
| `netlify/functions/` | Server-Funktionen (Story-Studio, Kommentare, Pins, Reminder, Stories, Bilder, Webinar, Ads) |

## Dokumente

- `EINSPIELEN.md`: bauen, prüfen und veröffentlichen
- `VORLAGE-BULK-IMPORT.md`: Vorlage und Regeln für den Bulk Import, auch für den Kundenraum
- `OFFENE-BUNDLE-AENDERUNGEN.md`: Protokoll aller Änderungen an der App (neueste unten)
- `SUPABASE_SETUP.md`: Datenbank für Konto und Synchronisierung
