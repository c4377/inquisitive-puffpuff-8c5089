/* Cover-Export (Carina 15.10.): Knopf „Cover“ in der Plan-Leiste öffnet dieses Fenster.
 * Eingabe „von Tag … bis Tag …“, dann rendert die App nur die erste Folie (das Cover) jedes Tages als JPEG
 * (gleiche Zeichnung wie „In Fotos speichern“, über window.__bsTagBilder aus dem Bundle) und bietet sie
 * zum Sichern in Fotos an. Gedacht für Feed-Vorschau-Apps.
 * Das iPhone erlaubt das Teilen nur direkt nach einem Tipp, deshalb zwei Schritte: erst erstellen, dann sichern.
 * Bei vielen Covern wird in Paketen zu je 10 geteilt.
 */
(function () {
  var css = document.createElement("style");
  css.textContent =
    "#bs-cover{position:fixed;inset:0;z-index:2147483004;background:rgba(20,16,14,.55);display:flex;align-items:flex-end;justify-content:center;font-family:-apple-system,Helvetica,Arial,sans-serif}" +
    "#bs-cover .p{background:#fff;width:100%;max-width:520px;max-height:88vh;overflow:auto;border-radius:18px 18px 0 0;padding:18px 18px 28px}" +
    "#bs-cover h3{margin:0 0 4px;font-size:17px;color:#111}#bs-cover .h{font-size:12px;color:#6B7280;margin:0 0 14px;line-height:1.45}" +
    "#bs-cover .r{display:flex;gap:10px;align-items:center;margin-bottom:12px;font-size:14px;color:#111}" +
    "#bs-cover input{width:72px;padding:9px 10px;border:1px solid #D1D5DB;border-radius:9px;font-size:15px}" +
    "#bs-cover .k{display:block;width:100%;border:0;border-radius:11px;padding:12px;font-size:14px;font-weight:700;cursor:pointer;margin-top:8px}" +
    "#bs-cover .k.a{background:#7C3AED;color:#fff}#bs-cover .k.b{background:#111;color:#fff}#bs-cover .k.c{background:#F3F4F6;color:#111}" +
    "#bs-cover .k:disabled{opacity:.5}#bs-cover .m{font-size:12px;color:#374151;margin-top:10px;min-height:16px}#bs-cover .m.f{color:#B91C1C}" +
    "#bs-cover .g{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:12px}#bs-cover .g img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:4px;background:#eee}";
  document.head.appendChild(css);

  function plan() {
    var p = Array.isArray(window.__bsPlan) ? window.__bsPlan : [];
    return p.filter(function (x) { return x && typeof x.day === "number" && Array.isArray(x.slides) && x.slides.length; })
      .sort(function (a, b) { return a.day - b.day; });
  }

  window.__bsCoverDialog = function () {
    if (document.getElementById("bs-cover")) return;
    var tage = plan(), max = tage.length ? tage[tage.length - 1].day : 1, min = tage.length ? tage[0].day : 1;
    var o = document.createElement("div"); o.id = "bs-cover";
    o.innerHTML = '<div class="p"><h3>Cover als Fotos</h3><p class="h">Nur die erste Folie jedes Posts, für deine Feed-Vorschau-App. Gib an, von welchem bis zu welchem Tag.</p>' +
      '<div class="r">von Tag <input type="number" inputmode="numeric" class="von" min="1"> bis Tag <input type="number" inputmode="numeric" class="bis" min="1"></div>' +
      '<button class="k a los">Cover erstellen</button><div class="pak"></div><button class="k c zu">Schließen</button><div class="m"></div><div class="g"></div></div>';
    document.body.appendChild(o);
    var von = o.querySelector(".von"), bis = o.querySelector(".bis"), los = o.querySelector(".los"), m = o.querySelector(".m"), g = o.querySelector(".g"), pak = o.querySelector(".pak");
    von.value = min; bis.value = Math.min(max, min + 19);
    function meld(t, f) { m.textContent = t || ""; m.className = "m" + (f ? " f" : ""); }
    o.querySelector(".zu").onclick = function () { o.remove(); };
    o.addEventListener("click", function (e) { if (e.target === o) o.remove(); });

    function sichern(files, knopf) {
      if (navigator.canShare && navigator.canShare({ files: files })) {
        navigator.share({ files: files }).then(function () { knopf && (knopf.textContent = "✓ " + knopf.textContent); })
          .catch(function (e) { if (e && e.name !== "AbortError") meld("Teilen ging nicht: " + (e.name || e) + ". Noch einmal tippen.", true); });
        return;
      }
      files.forEach(function (f, k) {
        setTimeout(function () { var a = document.createElement("a"); a.href = URL.createObjectURL(f); a.download = f.name; document.body.appendChild(a); a.click(); a.remove(); }, k * 350);
      });
      meld(files.length + " Cover werden heruntergeladen.");
    }

    los.onclick = async function () {
      var a = parseInt(von.value, 10), b = parseInt(bis.value, 10);
      if (!(a > 0) || !(b > 0)) { meld("Bitte zwei Tage eintragen.", true); return; }
      if (a > b) { var t = a; a = b; b = t; }
      if (typeof window.__bsTagBilder !== "function") { meld("Bitte zuerst den Content-Plan öffnen, dann noch einmal.", true); return; }
      var liste = plan().filter(function (x) { return x.day >= a && x.day <= b; });
      if (!liste.length) { meld("In diesem Bereich gibt es keine Posts.", true); return; }
      los.disabled = true; pak.innerHTML = ""; g.innerHTML = "";
      var files = [];
      for (var i = 0; i < liste.length; i++) {
        var p = liste[i];
        meld("Cover " + (i + 1) + " von " + liste.length + " wird erstellt (Tag " + p.day + ") …");
        try {
          var s0 = Object.assign({}, p.slides[0], { _tag: p.day });
          var r = await window.__bsTagBilder(Object.assign({}, p, { slides: [s0] }));
          if (r && r[0]) {
            var f = new File([r[0]], "Cover_Tag" + String(p.day).padStart(2, "0") + ".jpg", { type: "image/jpeg" });
            files.push(f);
            var im = document.createElement("img"); im.src = URL.createObjectURL(f); im.alt = "Tag " + p.day; g.appendChild(im);
          }
        } catch (e) { console.warn("Cover Tag " + p.day, e); }
      }
      los.disabled = false;
      if (!files.length) { meld("Es konnte kein Cover erstellt werden.", true); return; }
      meld(files.length + " Cover fertig. Jetzt sichern: im nächsten Fenster „Bilder sichern“ wählen.");
      for (var j = 0; j < files.length; j += 10) {
        (function (teil, nr, ges) {
          var k = document.createElement("button"); k.className = "k b";
          k.textContent = ges > 1 ? "Paket " + nr + " von " + ges + " in Fotos sichern (" + teil.length + ")" : teil.length + " Cover in Fotos sichern";
          k.onclick = function () { sichern(teil, k); };
          pak.appendChild(k);
        })(files.slice(j, j + 10), j / 10 + 1, Math.ceil(files.length / 10));
      }
    };
  };
})();
