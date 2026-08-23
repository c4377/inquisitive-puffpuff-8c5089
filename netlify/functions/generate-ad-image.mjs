// Netlify Function: AI ad-background generation via Google Gemini.
// The API key stays SERVER-SIDE (env var GEMINI_API_KEY) — never in the app.
// POST { prompt: string } -> { image: "data:image/png;base64,..." }

export default async (req) => {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405 });
  }
  // Der Schluessel wird erst gebraucht, wenn Rork nicht liefert — die
  // Pruefung stand vorher hier oben und haette den kostenlosen Weg
  // blockiert, nur weil der teure Schluessel fehlt.
  const key = process.env.GEMINI_API_KEY;

  let prompt = '';
  let referenz = '';
  let seiten = '4:5';
  try {
    const body = await req.json();
    prompt = String(body.prompt || '').slice(0, 2000);
    // Referenzbild fuer Rork (Data-URL oder reines Base64), optional.
    referenz = String(body.referenz || body.reference || '');
    if (body.aspectRatio) seiten = String(body.aspectRatio).slice(0, 8);
  } catch {
    return new Response(JSON.stringify({ error: 'Ungültiger Body' }), { status: 400 });
  }
  if (!prompt) return new Response(JSON.stringify({ error: 'prompt fehlt' }), { status: 400 });

  /* ------------------------------------------------------------- RORK */
  /**
   * ERST RORK, DANN GEMINI.
   *
   * Rork kostet nichts — kein Schluessel, kein Kontingent. Gemini kostet
   * rund 4 bis 6 Cent je Bild. Bei sechs Bildern pro Lauf ist das der
   * gesamte Kostenblock der App; die Textmodelle liegen bei etwa 0,8 Cent
   * je Lauf und fallen daneben nicht auf.
   *
   * Die Angaben stammen aus RORK-INTEGRATION.md der Portrait-App, nicht
   * aus einer Vermutung:
   *   POST https://toolkit.rork.com/images/edit/
   *   { prompt, images: [{ type:'image', image:<reines Base64> }], aspectRatio }
   *   Antwort: { image: { base64Data, mimeType } }
   *
   * ZWEI DINGE, DIE MAN WISSEN MUSS:
   *
   * 1. Es ist ein BEARBEITUNGS-Endpunkt. Ohne Referenzbild ist unklar, ob
   *    er antwortet — deshalb wird eines mitgeschickt, wenn die App eines
   *    hat. Nebeneffekt: die erzeugten Hintergruende passen zu den echten
   *    Fotos statt beliebig zu sein.
   * 2. Kein Vertrag, kein Kontingent, kein AV-Vertrag. Die Nutzung von
   *    aussen wurde laut derselben Dokumentation schon mehrfach gedrosselt
   *    oder abgeschaltet. Deshalb ist Gemini NICHT entfernt, sondern
   *    Rueckfall: schlaegt Rork fehl, laeuft es weiter, und die Antwort
   *    sagt im Feld "quelle", welcher Weg genommen wurde.
   *
   * Von hier aus konnte Rork nicht ausprobiert werden (der Netzzugang
   * dieser Umgebung erlaubt nur GitHub, npm und PyPI). Der erste echte
   * Test ist der erste Klick in der App — er kann nichts kaputt machen,
   * weil Gemini danebensteht.
   */
  const rorkVersuch = async () => {
    const bilder = [];
    if (referenz) {
      // Das "data:image/…;base64," davor muss weg — Rork will reines Base64.
      bilder.push({ type: 'image', image: String(referenz).replace(/^data:[^,]+,/, '') });
    }

    for (let versuch = 1; versuch <= 3; versuch += 1) {
      const abbruch = new AbortController();
      // Eigene Frist: der Endpunkt braucht laut Doku 20 bis 60 Sekunden.
      const frist = setTimeout(() => abbruch.abort(), 20000);
      try {
        const res = await fetch('https://toolkit.rork.com/images/edit/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt, images: bilder, aspectRatio: seiten }),
          signal: abbruch.signal,
        });
        clearTimeout(frist);

        if (res.status === 429) {
          // Drosselung: kurz warten, dann erneut. Laenger als die Funktion
          // leben darf, warten wir nicht — dann uebernimmt Gemini.
          await new Promise((r2) => setTimeout(r2, 1500 * versuch));
          continue;
        }
        if (!res.ok) {
          if (res.status >= 500 && versuch < 3) {
            await new Promise((r2) => setTimeout(r2, 800 * versuch));
            continue;
          }
          return null;
        }
        const daten = await res.json().catch(() => null);
        const b64 = daten && daten.image && daten.image.base64Data;
        if (!b64) return null;      // Antwort ohne Bild gilt als Fehlschlag
        const typ = (daten.image.mimeType) || 'image/png';
        return `data:${typ};base64,${b64}`;
      } catch (e) {
        clearTimeout(frist);
        // "Failed to fetch", Abbruch, DNS — alles gleich behandeln: aufhoeren
        // und Gemini uebernehmen lassen.
        return null;
      }
    }
    return null;
  };

  const ausRork = await rorkVersuch();
  if (ausRork) {
    return new Response(JSON.stringify({ quelle: "gemini", image: ausRork, quelle: 'rork' }), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    });
  }

  // Ab hier: Gemini als Rueckfall. Ohne Schluessel geht das nicht — dann
  // ist der Fehler ehrlich, statt still ein leeres Bild zu liefern.
  if (!key) {
    return new Response(JSON.stringify({
      error: 'Rork hat nicht geantwortet und GEMINI_API_KEY fehlt (Netlify → Environment variables).',
    }), { status: 500 });
  }

  try {
    // Mehrere Bildmodelle der Reihe nach — Google schaltet alte Namen ab
    // (Gemini 2.5 laeuft im Oktober 2026 aus). Schlaegt eines wegen des Namens
    // fehl, kommt das naechste dran.
    // REIHENFOLGE NACH PREIS, nicht nach Qualitaet.
    //
    // Diese Liste stand lange mit dem Pro-Modell vorne. Das kostet rund
    // 13 Cent je Bild statt 4 — bei zehn Bildern 1,24 EUR statt 0,36 EUR,
    // und niemand hat es gemerkt, weil beide dasselbe liefern: einen
    // unscharfen Hintergrund, ueber dem Text steht. Fuer diesen Zweck ist
    // das teure Modell rausgeworfenes Geld.
    //
    // Das Pro-Modell steht bewusst NICHT mehr in der Liste. Kaeme es als
    // letzter Ausweg dazu, waere es genau dann dran, wenn die guenstigen
    // gerade streiken — also unbemerkt und im Dauerlauf.
    const MODELLE = ['gemini-2.5-flash-image', 'gemini-flash-image-latest'];
    let r = null, data = null, letzterFehler = '';
    // Die Funktion selbst wird nach rund zehn Sekunden abgeschnitten. Drei
    // Modelle nacheinander durchzuprobieren kann darueber hinauslaufen —
    // dann kommt beim Aufrufer ein 504 an, obwohl das erste Modell nur
    // langsam war. Deshalb eine eigene Frist je Versuch: lieber das
    // naechste Modell fragen, als in die Abschaltung zu laufen.
    // FRIST unter dem, was Netlify erlaubt.
    // Netlify schneidet eine Funktion nach 10 Sekunden ab. Steht die Frist
    // hier hoeher, wartet die Funktion laenger, als sie leben darf: Netlify
    // beendet sie mitten im Warten, es kommt gar keine Antwort zurueck, und
    // der Browser meldet nur "Load failed". Lieber selbst rechtzeitig
    // aufgeben und einen lesbaren Grund schicken.
    const FRIST = 8500;
    const start = Date.now();
    for (const modell of MODELLE) {
      const rest = FRIST - (Date.now() - start);
      // Unter 2,5 Sekunden lohnt kein weiterer Versuch mehr.
      if (rest < 2500) break;
      const abbruch = AbortSignal.timeout(rest);
      try {
        r = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/${modell}:generateContent?key=${key}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }],
              generationConfig: { responseModalities: ['IMAGE'] },
            }),
            signal: abbruch,
          }
        );
      } catch (e) {
        letzterFehler = e?.name === 'TimeoutError'
          ? `${modell} hat nicht rechtzeitig geantwortet`
          : (e?.message || 'Netzwerkfehler');
        continue;
      }
      data = await r.json().catch(() => null);
      if (r.ok) break;
      letzterFehler = data?.error?.message || `HTTP ${r.status}`;
      const modellProblem = r.status === 404
        || /model|not (found|available|supported)|no longer/i.test(letzterFehler);
      if (!modellProblem) break;
    }
    // r bleibt null, wenn ALLE Modelle schon beim Verbinden scheitern —
    // dann darf hier nicht r.ok gelesen werden. Genau das hat vorher den
    // echten Grund verschluckt und ihn durch "Cannot read properties of
    // null" ersetzt.
    if (!r || !r.ok) {
      return new Response(
        JSON.stringify({ error: letzterFehler || 'Bilderzeugung nicht erreichbar' }),
        { status: 502, headers: { 'Content-Type': 'application/json' } }
      );
    }
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imgPart = parts.find((p) => p.inlineData?.data);
    if (!imgPart) {
      return new Response(JSON.stringify({ error: 'Kein Bild in der Antwort' }), { status: 502 });
    }
    const mime = imgPart.inlineData.mimeType || 'image/png';
    return new Response(
      JSON.stringify({ quelle: "gemini", image: `data:${mime};base64,${imgPart.inlineData.data}` }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e.message || e) }), { status: 500 });
  }
};
