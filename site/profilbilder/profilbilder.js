/* Profilbilder.
 *
 * Eine eigene Seite, keine Erweiterung der React-App: sie liest
 * dieselbe Datenbank (BrandStudioDB / assets / brand_images) und
 * zeichnet mit dem blossen Canvas. Damit kann hier nichts kaputtgehen,
 * was am Plan haengt, und der Zeichner der Kacheln bleibt unberuehrt.
 *
 * Die Tonwerte sind absichtlich dieselben Zahlen wie im dunklen
 * Aufsatz — Schwarzpunkt, Farbschicht, Vignette. Wer sie dort aendert,
 * muss sie hier mitaendern; dafuer haengt die Seite an keiner
 * Bundle-Version.
 */
(function () {
  var DB = "BrandStudioDB", STORE = "assets", KEY = "brand_images";
  var KANTE = 640;                 // Instagram nimmt 320, 640 bleibt scharf
  var PUNKT = 0.07;                // bildSchwarzpunkt
  var VIGNETTE = 0.60;             // bildVignette
  var TON = "13,13,13";            // tonNeutral

  function grund() {
    var v = parseFloat(localStorage.getItem("BS_SCHWARZ"));
    return isFinite(v) && v >= 0 ? v : 0.2;   // schwarzGrund
  }
  function merken(schluessel, wert) {
    try { localStorage.setItem(schluessel, String(wert)); } catch (e) {}
  }
  function geholt(schluessel, vorgabe) {
    var v = parseFloat(localStorage.getItem(schluessel));
    return isFinite(v) ? v : vorgabe;
  }

  function bilderLaden() {
    return new Promise(function (fertig) {
      var a = indexedDB.open(DB, 3);
      a.onerror = function () { fertig([]); };
      a.onsuccess = function (e) {
        try {
          var db = e.target.result;
          if (!db.objectStoreNames.contains(STORE)) return fertig([]);
          var r = db.transaction([STORE], "readonly").objectStore(STORE).get(KEY);
          /* Verbindung wieder zumachen: bleibt sie offen, blockiert sie
           * spaeter jede Version-Aenderung der App. */
          r.onsuccess = function () { var w = r.result || []; try { db.close(); } catch (f) {} fertig(w); };
          r.onerror = function () { try { db.close(); } catch (f) {} fertig([]); };
        } catch (f) { fertig([]); }
      };
    });
  }

  /* Die App legt entweder blosse Adressen ab oder Objekte; und in den
   * brandSettings steht, welche abgeschaltet sind. Beides beruecksichtigen,
   * damit hier dieselben Bilder stehen wie dort. */
  function adressen(roh) {
    var aus = {};
    try {
      var s = JSON.parse(localStorage.getItem("brandSettings") || "{}");
      aus = (s && s.imageMeta) || {};
    } catch (e) {}
    return (roh || []).map(function (b) {
      return typeof b === "string" ? b : (b && (b.src || b.url || b.dataUrl)) || "";
    }).filter(function (b) {
      return b && !(aus[b] && aus[b].disabled);
    });
  }

  /* Kann der Browser die zwei Mischmodi? Beide werden gebraucht:
   * color-burn zieht die Tiefen auf Schwarz, color holt danach die
   * Farbe des Originals zurueck, damit der Schwarzpunkt nicht die
   * Saettigung hochdrueckt (siehe Abschnitt 118/119). */
  function kann(modus) {
    try {
      var c = document.createElement("canvas").getContext("2d");
      c.globalCompositeOperation = modus;
      return c.globalCompositeOperation === modus;
    } catch (e) { return false; }
  }
  var BRENNBAR = kann("color-burn"), FARBMISCH = kann("color");

  function zeichnen(cv, bild, schwarz, zoom, hoehe) {
    var x = cv.getContext("2d");
    var W = cv.width, H = cv.height;
    x.globalCompositeOperation = "source-over";
    x.clearRect(0, 0, W, H);

    /* Deckend fuellen, dann mittig zuschneiden. hoehe verschiebt den
     * Ausschnitt senkrecht: 0 ist ganz oben, 100 ganz unten, 35 trifft
     * bei stehenden Fotos meist das Gesicht. */
    var s = Math.max(W / bild.width, H / bild.height) * zoom;
    var bw = bild.width * s, bh = bild.height * s;
    var links = (W - bw) / 2;
    var oben = (H - bh) * (hoehe / 100);
    x.drawImage(bild, links, oben, bw, bh);

    if (schwarz > 0 && PUNKT > 0 && BRENNBAR) {
      var g = Math.round(255 * (1 - PUNKT * Math.min(schwarz, 1)));
      x.globalCompositeOperation = "color-burn";
      x.fillStyle = "rgb(" + g + "," + g + "," + g + ")";
      x.fillRect(0, 0, W, H);
      if (FARBMISCH) {
        x.globalCompositeOperation = "color";
        x.drawImage(bild, links, oben, bw, bh);
      }
    }

    x.globalCompositeOperation = "source-over";
    var v = VIGNETTE * schwarz;
    if (v > 0) {
      var R = Math.max(W, H) * 0.72, cx = W / 2, cy = H * 0.45;
      var vg = x.createRadialGradient(cx, cy, R * 0.45, cx, cy, R);
      vg.addColorStop(0, "rgba(" + TON + ",0)");
      vg.addColorStop(1, "rgba(" + TON + "," + v + ")");
      x.fillStyle = vg; x.fillRect(0, 0, W, H);
    }
  }

  function laden(adresse) {
    return new Promise(function (fertig, schade) {
      var im = new Image();
      im.crossOrigin = "anonymous";
      im.onload = function () { fertig(im); };
      im.onerror = function () { schade(new Error("Bild nicht ladbar")); };
      im.src = adresse;
    });
  }

  var eintraege = [];   // {cv, bild}

  function allesZeichnen() {
    var schwarz = grund(), zoom = geholt("BS_PB_ZOOM", 1.15), hoehe = geholt("BS_PB_HOEHE", 35);
    eintraege.forEach(function (e) { zeichnen(e.cv, e.bild, schwarz, zoom, hoehe); });
  }

  function reglerBauen() {
    var s = document.getElementById("schwarz"), sw = document.getElementById("schwarzWert");
    var z = document.getElementById("zoom"), zw = document.getElementById("zoomWert");
    var h = document.getElementById("hoehe"), hw = document.getElementById("hoeheWert");
    s.value = String(Math.round(grund() * 100)); sw.textContent = s.value + "%";
    z.value = String(Math.round(geholt("BS_PB_ZOOM", 1.15) * 100)); zw.textContent = z.value + "%";
    h.value = String(geholt("BS_PB_HOEHE", 35)); hw.textContent = h.value + "%";
    function an(regler, anzeige, endung, wirkung) {
      regler.addEventListener("input", function () {
        anzeige.textContent = regler.value + endung;
        wirkung(parseFloat(regler.value));
        allesZeichnen();
      });
    }
    an(s, sw, "%", function (v) { merken("BS_SCHWARZ", v / 100); });
    an(z, zw, "%", function (v) { merken("BS_PB_ZOOM", v / 100); });
    an(h, hw, "%", function (v) { merken("BS_PB_HOEHE", v); });
  }

  function sichern(cv, nr) {
    try {
      var a = document.createElement("a");
      a.download = "profilbild-" + nr + ".png";
      a.href = cv.toDataURL("image/png");
      a.click();
    } catch (e) {
      alert("Herunterladen ging nicht: " + e.message);
    }
  }

  async function start() {
    reglerBauen();
    var raster = document.getElementById("raster");
    var liste = adressen(await bilderLaden());
    raster.innerHTML = "";
    if (!liste.length) {
      raster.innerHTML = '<p class="leer">Keine Bilder in der Mediathek gefunden. ' +
        'Lade sie im Plan hoch, dann stehen sie auch hier.</p>';
      return;
    }
    for (var i = 0; i < liste.length; i++) {
      var fig = document.createElement("figure");
      var box = document.createElement("div"); box.className = "rund";
      var cv = document.createElement("canvas"); cv.width = KANTE; cv.height = KANTE;
      box.appendChild(cv);
      var cap = document.createElement("figcaption"); cap.textContent = "lädt …";
      fig.appendChild(box); fig.appendChild(cap);
      raster.appendChild(fig);
      try {
        var bild = await laden(liste[i]);
        eintraege.push({ cv: cv, bild: bild });
        zeichnen(cv, bild, grund(), geholt("BS_PB_ZOOM", 1.15), geholt("BS_PB_HOEHE", 35));
        cap.textContent = "Bild " + (i + 1);
        (function (c, n) {
          box.addEventListener("click", function () { sichern(c, n); });
        })(cv, i + 1);
      } catch (e) {
        cap.textContent = "Bild " + (i + 1) + " — nicht ladbar";
      }
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
