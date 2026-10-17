/* Vorher/Nachher als Reel (Carina 17.10.): Knopf „VN-Reels“ in der Plan-Leiste öffnet dieses Fenster.
 * „Tage durchsuchen“ rendert das Cover jedes Tages im Bereich (window.__bsTagBilder); ist es eine
 * Vorher/Nachher-Kachel, legt der Zeichner die Teile in window.__bsVNTeile[tag] ab (Satz, Label,
 * Vorher- und Nachher-Bild, Farben). Daraus entsteht pro Tag ein 7-Sekunden-Video in 9:16 und 3:4:
 * Satz → Vorher gleitet herein → Nachher gleitet herein → Vorher tritt zurück, Nachher nach vorn.
 * Aufnahme über canvas.captureStream + MediaRecorder (iPhone: MP4, sonst WebM).
 * Das iPhone erlaubt das Teilen nur direkt nach einem Tipp, deshalb: erst erstellen, dann sichern.
 * Pro Tag steht die Caption aus dem Plan darunter (bearbeitbar, „Caption kopieren“).
 */
(function () {
  var DAUER = 7, FPS = 30;
  var css = document.createElement("style");
  css.textContent =
    "#bs-vnr{position:fixed;inset:0;z-index:2147483004;background:rgba(20,16,14,.55);display:flex;align-items:flex-end;justify-content:center;font-family:-apple-system,Helvetica,Arial,sans-serif}" +
    "#bs-vnr .p{background:#fff;width:100%;max-width:560px;max-height:90vh;overflow:auto;border-radius:18px 18px 0 0;padding:18px 18px 28px}" +
    "#bs-vnr h3{margin:0 0 4px;font-size:17px;color:#111}#bs-vnr .h{font-size:12px;color:#6B7280;margin:0 0 14px;line-height:1.45}" +
    "#bs-vnr .r{display:flex;gap:10px;align-items:center;margin-bottom:12px;font-size:14px;color:#111}" +
    "#bs-vnr input{width:72px;padding:9px 10px;border:1px solid #D1D5DB;border-radius:9px;font-size:15px}" +
    "#bs-vnr .k{border:0;border-radius:11px;padding:11px 14px;font-size:13px;font-weight:700;cursor:pointer;margin:6px 6px 0 0}" +
    "#bs-vnr .k.a{background:#7C3AED;color:#fff}#bs-vnr .k.b{background:#111;color:#fff}#bs-vnr .k.c{background:#F3F4F6;color:#111}" +
    "#bs-vnr .k:disabled{opacity:.5}#bs-vnr .m{font-size:12px;color:#374151;margin-top:10px;min-height:16px}#bs-vnr .m.f{color:#B91C1C}" +
    "#bs-vnr .tag{border-top:1px solid #eee;padding:12px 0}#bs-vnr .tag b{font-size:14px}#bs-vnr .tag .s{font-size:12px;color:#6B7280;margin:2px 0 4px}" +
    "#bs-vnr .cap{width:100%;box-sizing:border-box;margin:8px 0 2px;border:1px solid #E5E7EB;border-radius:10px;padding:9px 10px;font:16px/1.4 -apple-system,Helvetica,Arial,sans-serif;color:#111;resize:vertical}" +
    "#bs-vnr video{width:46%;margin:8px 2% 0 0;border-radius:8px;background:#111;vertical-align:top}";
  document.head.appendChild(css);

  function plan() {
    var p = Array.isArray(window.__bsPlan) ? window.__bsPlan : [];
    return p.filter(function (x) { return x && typeof x.day === "number" && Array.isArray(x.slides) && x.slides.length; })
      .sort(function (a, b) { return a.day - b.day; });
  }
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(v) { v = clamp(v); return 1 - Math.pow(1 - v, 3); }

  // Papierstruktur wie die Vergleichskachel (Korn, Flecken, Sprenkel), einmal pro Format.
  function grund(T, w, h) {
    if (T.foto) {
      var cf = document.createElement("canvas"); cf.width = w; cf.height = h;
      var xf = cf.getContext("2d"), fw = T.foto.naturalWidth || T.foto.width, fh = T.foto.naturalHeight || T.foto.height, fs = Math.max(w / fw, h / fh);
      xf.drawImage(T.foto, (w - fw * fs) / 2, Math.min(0, (h - fh * fs) * 0.3), fw * fs, fh * fs);
      xf.fillStyle = T.fotoTon || "rgba(140,118,96,0.68)"; xf.fillRect(0, 0, w, h);
      return cf;
    }
    var c = document.createElement("canvas"); c.width = Math.round(w / 2); c.height = Math.round(h / 2);
    var x = c.getContext("2d"), cw = c.width, ch = c.height; x.fillStyle = T.bg || "#B5A08A"; x.fillRect(0, 0, cw, ch);
    var s = 271; function R() { s = (s * 9301 + 49297) % 233280; return s / 233280; }
    var fl = T.flecken || 1;
    for (var k = 0; k < Math.round(18 * fl); k++) {
      var gx = R() * cw, gy = R() * ch, gr = 40 + R() * 170, g = x.createRadialGradient(gx, gy, 0, gx, gy, gr), hl = R() < 0.5;
      g.addColorStop(0, hl ? "rgba(255,250,240," + 0.1 * fl + ")" : "rgba(40,35,30," + 0.08 * fl + ")"); g.addColorStop(1, "rgba(0,0,0,0)");
      x.fillStyle = g; x.fillRect(0, 0, cw, ch);
    }
    if (T.korn) {
      try {
        var d = x.getImageData(0, 0, cw, ch), q = d.data;
        for (var i = 0; i < q.length; i += 4) { var n = (R() - 0.5) * T.korn; q[i] += n; q[i + 1] += n; q[i + 2] += n; }
        x.putImageData(d, 0, 0);
      } catch (e) {}
    }
    for (var j = 0; j < (T.sprenkel || 0) * (cw * ch) / (540 * 675); j++) {
      x.fillStyle = "rgba(30,26,22," + (0.15 + R() * 0.35) + ")"; var z = 0.4 + R() * 1.1; x.fillRect(R() * cw, R() * ch, z, z * (0.6 + R()));
    }
    return c;
  }

  // Satz mit *kursiven* Stellen, ausgeglichen umbrochen.
  function worte(satz) {
    var out = [];
    String(satz || "").split(/(\*[^*]+\*)/).filter(Boolean).forEach(function (teil) {
      var it = /^\*.*\*$/.test(teil), roh = it ? teil.slice(1, -1) : teil, klebt = !/^\s/.test(roh);
      roh.split(/\s+/).filter(Boolean).forEach(function (w, k) {
        if (k === 0 && klebt && out.length && /^[.,!?…:;“”"»«)]+/.test(w)) { out[out.length - 1].w += w; return; }
        out.push({ w: w, i: it });
      });
    });
    return out;
  }
  function setze(x, ws, fam, fs, breite) {
    var sp = function (w) { x.font = (w.i ? "italic " : "") + "400 " + fs + "px \"" + fam + "\""; return x.measureText(w.w).width; };
    var leer = (x.font = "400 " + fs + "px \"" + fam + "\"", x.measureText(" ").width);
    function brich(b) {
      var zl = [], z = [], zb = 0;
      ws.forEach(function (w) { var wb = sp(w); if (z.length && zb + leer + wb > b) { zl.push({ ws: z, b: zb }); z = [w]; zb = wb; } else { zb += (z.length ? leer : 0) + wb; z.push(w); } });
      z.length && zl.push({ ws: z, b: zb }); return zl;
    }
    var zl = brich(breite), n = zl.length, lo = breite * 0.5, hi = breite;
    if (n > 1) { for (var k = 0; k < 10; k++) { var m = (lo + hi) / 2; brich(m).length > n ? (lo = m) : (hi = m); } zl = brich(hi); }
    return { zl: zl, leer: leer, fs: fs };
  }
  function satzPlan(x, T, fam, fs0, breite, maxZ) {
    var ws = worte(T.satz), fs = fs0, p;
    for (var k = 0; k < 30; k++) { p = setze(x, ws, fam, fs, breite); if (p.zl.length <= maxZ) break; fs *= 0.94; }
    return p;
  }
  function maleSatz(x, p, fam, cx, y, farbe) {
    x.fillStyle = farbe; x.textAlign = "left"; x.textBaseline = "alphabetic";
    p.zl.forEach(function (z, k) {
      var xx = cx - z.b / 2;
      z.ws.forEach(function (w) { x.font = (w.i ? "italic " : "") + "400 " + p.fs + "px \"" + fam + "\""; x.fillText(w.w, xx, y + p.fs * 0.82 + k * p.fs * 1.02); xx += x.measureText(w.w).width + p.leer; });
    });
    return p.zl.length * p.fs * 1.02;
  }
  function caps(x, t, cx, y, fs, farbe, sp) {
    x.font = "500 " + fs + "px \"HelveticaNeueBrand\""; x.fillStyle = farbe; x.textAlign = "center"; x.textBaseline = "alphabetic";
    if ("letterSpacing" in x) x.letterSpacing = (sp || 6) + "px";
    x.fillText(String(t || "").toLocaleUpperCase("de-DE"), cx + (sp || 6) / 2, y);
    if ("letterSpacing" in x) x.letterSpacing = "0px";
  }
  function karte(x, img, cx, cy, w, h, sc, alpha, schatten) {
    if (!img || alpha <= 0) return;
    x.save(); x.globalAlpha = alpha; x.translate(cx, cy); x.scale(sc, sc);
    x.shadowColor = "rgba(0,0,0," + schatten + ")"; x.shadowBlur = 55; x.shadowOffsetY = 26;
    x.fillStyle = "#000"; x.fillRect(-w / 2, -h / 2, w, h); x.shadowColor = "transparent";
    x.drawImage(img, -w / 2, -h / 2, w, h); x.restore();
  }

  // Ein Bild zum Zeitpunkt t (Sekunden). Format: H = 1920 (9:16) oder 1440 (3:4), W = 1080.
  function bild(x, T, t, W, H, bg) {
    x.drawImage(bg, 0, 0, W, H);
    var lang = H > 1600, fam = T.serif || "Feed Serif";
    var p = satzPlan(x, T, fam, lang ? 100 : 84, 900, 3), shh = p.zl.length * p.fs * 1.02;
    var cw = lang ? 470 : 400, gap = 50, luecke = lang ? 150 : 96;
    var dims = T.bilder.map(function (im) { if (!im) return [cw, cw * 1.25]; var r = (im.naturalHeight || im.height) / (im.naturalWidth || im.width); return [cw, Math.min(cw * r, cw * 1.4)]; });
    var hmax = Math.max(dims[0][1], dims[1][1]), block = 50 + shh + luecke + 40 + hmax;
    var y0 = Math.max(lang ? 200 : 100, (H - block) / 2 - (lang ? 60 : 20)), kickY = y0 + 26, satzY = y0 + 50;
    var a = ease((t - 0.15) / 0.8), k0 = ease(t / 0.7);
    if (T.kick) { x.globalAlpha = k0; caps(x, T.kick, W / 2, kickY, 26, T.akz || T.lab, 7); x.globalAlpha = 1; }
    x.globalAlpha = a; var sh = maleSatz(x, p, fam, W / 2, satzY + (1 - a) * 40, T.ink); x.globalAlpha = 1;
    var top = satzY + shh + luecke + 40, cy = top + hmax / 2;
    var xv = W / 2 - cw / 2 - gap / 2, xn = W / 2 + cw / 2 + gap / 2;
    var b = ease((t - 0.9) / 0.9), c = ease((t - 2.9) / 0.9), d = ease((t - 4.5) / 0.9), e = ease((t - 5.2) / 0.6);
    var lv = (T.labels && T.labels[0]) || "Vorher", ln = (T.labels && T.labels[1]) || "Nachher";
    x.globalAlpha = b * (1 - 0.5 * d); caps(x, lv, xv, top - 40 + (1 - b) * 90, 24, T.lab, 6); x.globalAlpha = 1;
    karte(x, T.bilder[0], xv, cy + (1 - b) * 90, dims[0][0], dims[0][1], (0.96 + 0.04 * b) * (1 - 0.06 * d), b * (1 - 0.5 * d), 0.38);
    x.globalAlpha = c; caps(x, ln, xn + (1 - c) * 140, top - 40, 24, T.lab, 6); x.globalAlpha = 1;
    karte(x, T.bilder[1], xn + (1 - c) * 140, cy, dims[1][0], dims[1][1], 1 + 0.08 * d, c, 0.38 + 0.12 * d);
    x.globalAlpha = e; caps(x, T.hand, W / 2, H - (lang ? 150 : 80), 22, T.lab, 5); x.globalAlpha = 1;
  }

  function aufnehmen(T, H) {
    return new Promise(function (ok, nein) {
      var W = 1080, c = document.createElement("canvas"); c.width = W; c.height = H;
      var x = c.getContext("2d"), bg = grund(T, W, H);
      if (!c.captureStream || typeof MediaRecorder === "undefined") return nein(new Error("Dieser Browser kann keine Videos aufnehmen"));
      var typen = ["video/mp4;codecs=avc1", "video/mp4", "video/webm;codecs=vp9", "video/webm"], typ = "";
      for (var i = 0; i < typen.length; i++) { if (MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(typen[i])) { typ = typen[i]; break; } }
      bild(x, T, 0, W, H, bg);
      var st = c.captureStream(FPS), rec, teile = [];
      try { rec = new MediaRecorder(st, typ ? { mimeType: typ, videoBitsPerSecond: 8e6 } : { videoBitsPerSecond: 8e6 }); } catch (e) { return nein(e); }
      rec.ondataavailable = function (ev) { ev.data && ev.data.size && teile.push(ev.data); };
      rec.onstop = function () { var mt = (rec.mimeType || typ || "video/webm").split(";")[0]; ok(new Blob(teile, { type: mt })); };
      rec.start(250);
      var t0 = performance.now();
      (function schritt() {
        var t = (performance.now() - t0) / 1000;
        bild(x, T, Math.min(t, DAUER), W, H, bg);
        if (t < DAUER + 0.15) requestAnimationFrame(schritt); else rec.stop();
      })();
    });
  }
  window.__bsVNReelBild = function (T, t, H) { var c = document.createElement("canvas"); c.width = 1080; c.height = H; bild(c.getContext("2d"), T, t, 1080, H, grund(T, 1080, H)); return c; };

  window.__bsVNReelDialog = function () {
    if (document.getElementById("bs-vnr")) return;
    var tage = plan(), max = tage.length ? tage[tage.length - 1].day : 1, min = tage.length ? tage[0].day : 1;
    var o = document.createElement("div"); o.id = "bs-vnr";
    o.innerHTML = '<div class="p"><h3>Vorher/Nachher als Reel</h3><p class="h">7 Sekunden, animiert, in 9:16 und 3:4. Die App sucht im Bereich die Vorher/Nachher-Posts, dann erstellst du pro Tag die Videos und sicherst sie in Fotos.</p>' +
      '<div class="r">von Tag <input type="number" inputmode="numeric" class="von" min="1"> bis Tag <input type="number" inputmode="numeric" class="bis" min="1"></div>' +
      '<button class="k a such">Tage durchsuchen</button><button class="k c zu">Schließen</button><div class="m"></div><div class="liste"></div></div>';
    document.body.appendChild(o);
    var von = o.querySelector(".von"), bis = o.querySelector(".bis"), m = o.querySelector(".m"), liste = o.querySelector(".liste"), such = o.querySelector(".such");
    von.value = min; bis.value = Math.min(max, min + 29);
    function meld(t, f) { m.textContent = t || ""; m.className = "m" + (f ? " f" : ""); }
    o.querySelector(".zu").onclick = function () { o.remove(); };
    o.addEventListener("click", function (e) { if (e.target === o) o.remove(); });
    function sichern(f) {
      if (navigator.canShare && navigator.canShare({ files: [f] })) { navigator.share({ files: [f] }).catch(function (e) { if (e && e.name !== "AbortError") meld("Teilen ging nicht: " + (e.name || e), true); }); return; }
      var a = document.createElement("a"); a.href = URL.createObjectURL(f); a.download = f.name; document.body.appendChild(a); a.click(); a.remove();
    }
    function zeile(tag, T, cap) {
      var d = document.createElement("div"); d.className = "tag";
      d.innerHTML = "<b>Tag " + tag + "</b><div class='s'></div>"; d.querySelector(".s").textContent = String(T.satz || "").replace(/\*/g, "");
      var ct = document.createElement("textarea"); ct.className = "cap"; ct.rows = 5; ct.value = String(cap || ""); ct.placeholder = "Für diesen Tag ist keine Caption im Plan.";
      var ck = document.createElement("button"); ck.className = "k c"; ck.textContent = "Caption kopieren";
      ck.onclick = function () {
        var fertig = function () { ck.textContent = "Kopiert ✓"; setTimeout(function () { ck.textContent = "Caption kopieren"; }, 1400); };
        try { navigator.clipboard.writeText(ct.value).then(fertig, function () { ct.select(); document.execCommand("copy"); fertig(); }); } catch (e) { ct.select(); try { document.execCommand("copy"); fertig(); } catch (e2) {} }
      };
      d.appendChild(ct); d.appendChild(ck); d.appendChild(document.createElement("br"));
      [["9:16", 1920, "9x16"], ["3:4", 1440, "3x4"]].forEach(function (fm) {
        var b = document.createElement("button"); b.className = "k b"; b.textContent = "Reel " + fm[0] + " erstellen";
        b.onclick = function () {
          if (b._datei) return sichern(b._datei);
          b.disabled = true; b.textContent = "Wird aufgenommen (7 s) …";
          aufnehmen(T, fm[1]).then(function (bl) {
            var ext = /mp4/.test(bl.type) ? "mp4" : "webm";
            b._datei = new File([bl], "VN-Reel_Tag" + String(tag).padStart(2, "0") + "_" + fm[2] + "." + ext, { type: bl.type });
            var v = document.createElement("video"); v.src = URL.createObjectURL(bl); v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true; d.appendChild(v);
            b.disabled = false; b.textContent = fm[0] + " in Fotos sichern";
            ext === "webm" && meld("Hinweis: Dieser Browser nimmt WebM auf. Auf dem iPhone entsteht MP4.");
          }).catch(function (e) { b.disabled = false; b.textContent = "Reel " + fm[0] + " erstellen"; meld("Aufnahme ging nicht: " + (e.message || e), true); });
        };
        d.appendChild(b);
      });
      liste.appendChild(d);
    }
    such.onclick = async function () {
      var a = parseInt(von.value, 10), z = parseInt(bis.value, 10);
      if (!(a > 0) || !(z > 0)) { meld("Bitte zwei Tage eintragen.", true); return; }
      if (a > z) { var tt = a; a = z; z = tt; }
      if (typeof window.__bsTagBilder !== "function") { meld("Bitte zuerst den Content-Plan öffnen, dann noch einmal.", true); return; }
      var l = plan().filter(function (p) { return p.day >= a && p.day <= z; });
      if (!l.length) { meld("In diesem Bereich gibt es keine Posts.", true); return; }
      such.disabled = true; liste.innerHTML = ""; var n = 0;
      for (var i = 0; i < l.length; i++) {
        var p = l[i]; meld("Suche … Tag " + p.day + " (" + (i + 1) + " von " + l.length + ")");
        try {
          window.__bsVNTeile && delete window.__bsVNTeile[String(p.day)];
          await window.__bsTagBilder(Object.assign({}, p, { slides: [Object.assign({}, p.slides[0], { _tag: p.day })] }));
          var T = window.__bsVNTeile && window.__bsVNTeile[String(p.day)];
          if (T && T.bilder && T.bilder[0] && T.bilder[1]) { zeile(p.day, T, p.caption); n++; }
        } catch (e) { console.warn("VN-Reel Tag " + p.day, e); }
      }
      such.disabled = false;
      meld(n ? n + " Vorher/Nachher-Posts gefunden. Pro Format einmal tippen zum Erstellen, dann noch einmal zum Sichern." : "Keine Vorher/Nachher-Posts in diesem Bereich.", !n);
    };
  };
})();
