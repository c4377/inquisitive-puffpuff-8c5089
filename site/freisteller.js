/* Eigene Freisteller (Carina 12.10.): In Settings, direkt unter „Foto für den Call-to-Action“, gibt es
 * einen Bereich „Freisteller“. Dort lädt man ausgeschnittene Fotos (PNG mit durchsichtigem Hintergrund,
 * z. B. am iPhone in Fotos lange auf die Person drücken → „Kopieren“ / „Teilen → Bild sichern“) hoch.
 *
 * Gespeichert wird im Browser in einer eigenen IndexedDB („BrandStudioFrei“, im Kundenraum
 * „BrandStudioFrei__<raum>“), also pro Gerät und pro Raum getrennt.
 * window.__bsFreiP liefert die Liste der Bilder (Data-URLs). Der Kontrast-Zeichner nimmt sie für die
 * Freisteller-Cover (cutwort); ist die Liste leer, bleiben die eingebauten Freisteller.
 */
(function () {
  var DB = "BrandStudioFrei" + (window.BS_RAUM ? "__" + window.BS_RAUM : ""), ST = "bilder";
  function oeffnen() {
    return new Promise(function (ok, nein) {
      var r = indexedDB.open(DB, 1);
      r.onupgradeneeded = function () { r.result.createObjectStore(ST, { keyPath: "id", autoIncrement: true }); };
      r.onsuccess = function () { ok(r.result); };
      r.onerror = function () { nein(r.error); };
    });
  }
  function alle() {
    return oeffnen().then(function (db) {
      return new Promise(function (ok) {
        var r = db.transaction(ST, "readonly").objectStore(ST).getAll();
        r.onsuccess = function () { db.close(); ok(r.result || []); };
        r.onerror = function () { db.close(); ok([]); };
      });
    }).catch(function () { return []; });
  }
  function schreiben(fn) {
    return oeffnen().then(function (db) {
      return new Promise(function (ok) {
        var tx = db.transaction(ST, "readwrite");
        fn(tx.objectStore(ST));
        tx.oncomplete = function () { db.close(); ok(); };
        tx.onerror = function () { db.close(); ok(); };
      });
    });
  }
  var liste = [];
  function laden() {
    window.__bsFreiP = alle().then(function (l) { liste = l; return l.map(function (x) { return x.url; }); });
    return window.__bsFreiP;
  }
  laden();

  /* Bild prüfen, auf den sichtbaren Bereich zuschneiden und verkleinern. */
  function aufbereiten(datei) {
    return new Promise(function (ok, nein) {
      var fr = new FileReader();
      fr.onload = function () {
        var im = new Image();
        im.onload = function () {
          var w = im.naturalWidth, h = im.naturalHeight, c = document.createElement("canvas");
          c.width = w; c.height = h;
          var x = c.getContext("2d");
          x.drawImage(im, 0, 0);
          var d;
          try { d = x.getImageData(0, 0, w, h).data; } catch (e) { nein("Bild konnte nicht gelesen werden."); return; }
          var x0 = w, y0 = h, x1 = -1, y1 = -1, durch = 0, n = 0;
          for (var yy = 0; yy < h; yy += 2) for (var xx = 0; xx < w; xx += 2) {
            var a = d[(yy * w + xx) * 4 + 3]; n++;
            if (a < 20) { durch++; continue; }
            if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (yy < y0) y0 = yy; if (yy > y1) y1 = yy;
          }
          if (durch / n < 0.05 || x1 < 0) { nein("Dieses Bild hat keinen durchsichtigen Hintergrund. Bitte zuerst freistellen (am iPhone: in Fotos lange auf dich drücken → „Kopieren“ oder „Teilen → Bild sichern“)."); return; }
          var bw = x1 - x0 + 2, bh = y1 - y0 + 2, s = Math.min(1, 1600 / Math.max(bw, bh));
          var o = document.createElement("canvas");
          o.width = Math.max(1, Math.round(bw * s)); o.height = Math.max(1, Math.round(bh * s));
          o.getContext("2d").drawImage(c, x0, y0, bw, bh, 0, 0, o.width, o.height);
          ok(o.toDataURL("image/png"));
        };
        im.onerror = function () { nein("Bild konnte nicht geöffnet werden."); };
        im.src = fr.result;
      };
      fr.onerror = function () { nein("Datei konnte nicht gelesen werden."); };
      fr.readAsDataURL(datei);
    });
  }

  var css = document.createElement("style");
  css.textContent =
    "#bs-frei{margin-bottom:24px;border:1px solid #E5E7EB;border-radius:12px;padding:16px;background:#fff;font-family:inherit}" +
    "#bs-frei .t{font-size:14px;font-weight:700;color:#111827;margin-bottom:4px}" +
    "#bs-frei .h{font-size:11px;line-height:1.45;color:#6B7280;margin-bottom:10px}" +
    "#bs-frei .g{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px}" +
    "#bs-frei .k{position:relative;aspect-ratio:3/4;border-radius:8px;border:1px solid #E5E7EB;background:#33363A;display:flex;align-items:flex-end;justify-content:center;overflow:hidden}" +
    "#bs-frei .k img{max-width:100%;max-height:100%;object-fit:contain}" +
    "#bs-frei .k button{position:absolute;top:4px;right:4px;width:22px;height:22px;border-radius:999px;border:0;background:rgba(255,255,255,.9);color:#B91C1C;font-size:12px;cursor:pointer}" +
    "#bs-frei .lade{display:inline-block;background:#7C3AED;color:#fff;font-size:12px;font-weight:700;border-radius:9px;padding:9px 12px;cursor:pointer}" +
    "#bs-frei .m{font-size:11px;margin-top:8px;color:#6B7280}" +
    "#bs-frei .m.f{color:#B91C1C}";
  document.head.appendChild(css);

  function panel() {
    var box = document.createElement("div");
    box.id = "bs-frei";
    box.innerHTML =
      '<div class="t">Freisteller</div>' +
      '<div class="h">Für die Cover mit dem großen Wort. Am iPhone: Foto in der Fotos-App öffnen, lange auf dich drücken, dann „Kopieren“ oder „Teilen → Bild sichern“. Das gesicherte Bild hier hochladen. Sobald hier Freisteller sind, nimmt die App nur noch diese.</div>' +
      '<div class="g"></div>' +
      '<label class="lade">+ Freisteller hochladen<input type="file" accept="image/png,image/webp,image/*" multiple style="display:none"></label>' +
      '<div class="m"></div>';
    var g = box.querySelector(".g"), m = box.querySelector(".m"), inp = box.querySelector("input");
    function meldung(t, fehler) { m.textContent = t || ""; m.className = "m" + (fehler ? " f" : ""); }
    function zeigen() {
      g.innerHTML = "";
      liste.forEach(function (x) {
        var k = document.createElement("div"); k.className = "k";
        var im = document.createElement("img"); im.src = x.url; im.alt = "Freisteller";
        var del = document.createElement("button"); del.type = "button"; del.textContent = "✕"; del.title = "Löschen";
        del.addEventListener("click", function () {
          if (!confirm("Diesen Freisteller löschen?")) return;
          schreiben(function (st) { st.delete(x.id); }).then(laden).then(zeigen).then(function () { meldung("Gelöscht. Öffne einen Post neu, damit die Cover neu gezeichnet werden."); });
        });
        k.appendChild(im); k.appendChild(del); g.appendChild(k);
      });
      g.style.display = liste.length ? "grid" : "none";
      if (!liste.length && !m.textContent) meldung("Noch keine eigenen Freisteller. Bis dahin nimmt die App die eingebauten.");
    }
    inp.addEventListener("change", function () {
      var dateien = Array.prototype.slice.call(inp.files || []);
      inp.value = "";
      if (!dateien.length) return;
      meldung("Wird verarbeitet …");
      var gut = 0, fehler = "";
      dateien.reduce(function (p, f) {
        return p.then(function () {
          return aufbereiten(f).then(function (url) {
            gut++;
            return schreiben(function (st) { st.add({ url: url, t: Date.now() }); });
          }).catch(function (e) { fehler = String(e); });
        });
      }, Promise.resolve()).then(laden).then(function () {
        zeigen();
        if (fehler && !gut) meldung(fehler, true);
        else meldung(gut + (gut === 1 ? " Freisteller" : " Freisteller") + " gespeichert." + (fehler ? " Eins ging nicht: " + fehler : "") + " Öffne einen Post neu, damit die Cover neu gezeichnet werden.", !!fehler);
      });
    });
    window.__bsFreiP.then(zeigen);
    return box;
  }

  function einsetzen() {
    if (document.getElementById("bs-frei")) return;
    var t = null, ds = document.querySelectorAll("div");
    for (var i = 0; i < ds.length; i++) if (ds[i].textContent.trim() === "Foto für den Call-to-Action") { t = ds[i]; break; }
    var ziel = t && t.parentElement && t.parentElement.parentElement;
    if (!ziel || !ziel.parentElement) return;
    ziel.insertAdjacentElement("afterend", panel());
  }
  var wartet = false;
  new MutationObserver(function () {
    if (wartet) return;
    wartet = true;
    setTimeout(function () { wartet = false; einsetzen(); }, 300);
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
