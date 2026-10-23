/* Foto-Story (Carina 23.10.): ein echtes Foto aus dem Alltag → 3 Storylines mit je 7 Slides.
 *
 * Geöffnet über „📷 Foto-Story“ im Story-Studio. Carina wählt ein Foto und schreibt optional dazu,
 * was das für ein Moment ist. /.netlify/functions/foto-story schreibt drei Storylines in ihrer Stimme
 * (Zielgruppe: Coachin, die postet und nicht verkauft), parallel, je eine Anfrage pro Storyline.
 * Jede Storyline kommt in einem eigenen Look aus dem Brandblatt, alle auf demselben Foto:
 *   Klar   Foto randlos, Verlauf in Espresso, Instrument Serif weiß, ein Wort kursiv.
 *   Karte  Foto randlos, unten ein durchsichtiger Creme-Schleier, Instrument Serif in Tinte, kleines Label in Sand.
 *   Ruhig  Foto weich unscharf unter Espresso, Versalien weiß, letzte kurze Zeile als Signatur in Gold.
 * Pro Slide ein anderer Ausschnitt des Fotos. Texte lassen sich ändern, der Look lässt sich wechseln.
 * „Diese nehme ich“ wählt eine Storyline, „Exportieren“ teilt die 7 Bilder (1080×1920 JPEG).
 */
(function () {
  if (window.BS_RAUM) return;
  var W = 1080, H = 1920, SERIF = "Instrument Serif", SIG = "Mrs Saint Delafield", IN = "Inter";
  var F = { espresso: "#271E1C", creme: "#F3EFE4", tinte: "#16130F", sand: "#635645", gold: "#E2C49A", weiss: "#FFFFFF", oliv: "#4E3F20" };
  var LOOKS = [
    { id: "klar", name: "Klar", info: "Foto mit Verlauf, Serif in Weiß" },
    { id: "karte", name: "Karte", info: "Foto mit Creme-Schleier unten" },
    { id: "ruhig", name: "Ruhig", info: "Foto weich, Versalien und Signatur" }
  ];
  var AUSSCHNITT = [[1, .5, .45], [1.14, .35, .3], [1.26, .62, .4], [1.08, .5, .65], [1.32, .45, .28], [1.18, .58, .55], [1.04, .5, .4]];
  var panel = null, foto = null, fotoKlein = "", lines = [], wahl = -1, liste = null, status = null, exportB = null;

  function el(tag, css, txt) { var e = document.createElement(tag); css && (e.style.cssText = css); txt != null && (e.textContent = txt); return e; }
  function knopf(t, primaer) {
    var b = el("button", "border:0;border-radius:999px;padding:12px 18px;font:600 14px -apple-system,sans-serif;cursor:pointer;" + (primaer ? "background:" + F.espresso + ";color:#fff" : "background:#fff;color:" + F.espresso + ";box-shadow:inset 0 0 0 1px #ddd3c6"), t);
    b.type = "button"; return b;
  }
  function schriften() {
    return Promise.race([Promise.all(["400 80px \"" + SERIF + "\"", "italic 400 80px \"" + SERIF + "\"", "400 80px \"" + SIG + "\"", "600 30px \"" + IN + "\""].map(function (q) { return document.fonts.load(q).catch(function () {}); })), new Promise(function (ok) { setTimeout(ok, 4000); })]);
  }

  /* Foto: Ausschnitt pro Slide, „cover“ mit Zoom und Blickpunkt. */
  function cover(ctx, img, x0, y0, w, h, a) {
    var s = Math.max(w / img.width, h / img.height) * a[0], dw = img.width * s, dh = img.height * s;
    ctx.save(); ctx.beginPath(); ctx.rect(x0, y0, w, h); ctx.clip();
    ctx.drawImage(img, x0 + (w - dw) * a[1], y0 + (h - dh) * a[2], dw, dh); ctx.restore();
  }
  function weich(ctx, img, a) {
    /* Weichzeichnen ohne ctx.filter (Safari): stufenweise klein und wieder groß rechnen. */
    var stufen = [[270, 480], [68, 120], [270, 480]], quelle = null;
    stufen.forEach(function (g, j) {
      var k = document.createElement("canvas"); k.width = g[0]; k.height = g[1];
      var kc = k.getContext("2d"); kc.imageSmoothingEnabled = true; kc.imageSmoothingQuality = "high";
      j === 0 ? cover(kc, img, 0, 0, g[0], g[1], a) : kc.drawImage(quelle, 0, 0, g[0], g[1]);
      quelle = k;
    });
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high"; ctx.drawImage(quelle, -30, -30, W + 60, H + 60);
  }

  /* Text: Zeilen aus dem Slide-Text, *Wort* kursiv, Umbruch auf Breite. */
  function worte(zeile, gross) {
    var out = [], k = false;
    String(zeile).split(/(\*)/).forEach(function (t) {
      if (t === "*") { k = !k; return; }
      t.split(/(\s+)/).forEach(function (w, j) {
        if (!w || /^\s+$/.test(w)) return;
        var g = gross ? w.toLocaleUpperCase("de-DE") : w, vorher = j > 0 || /^\s/.test(t);
        if (out.length && !vorher && /^[.,!?:;…“”"»«)]+/.test(g)) { var m = /^[.,!?:;…“”"»«)]+/.exec(g)[0]; out[out.length - 1].n = (out[out.length - 1].n || "") + m; g = g.slice(m.length); if (!g) return; }
        out.push({ w: g, k: k });
      });
    });
    return out;
  }
  function schrift(ctx, fs, k) { ctx.font = (k ? "italic " : "") + "400 " + fs + "px \"" + SERIF + "\""; }
  function satz(ctx, absaetze, fs, breite, gross) {
    var zz = [];
    absaetze.forEach(function (a, ai) {
      var z = [], b = 0, erste = true; schrift(ctx, fs, false); var sp = ctx.measureText(" ").width;
      var schiebe = function () { zz.push({ w: z, b: b, neu: erste && ai > 0 }); erste = false; z = []; b = 0; };
      worte(a, gross).forEach(function (w) {
        schrift(ctx, fs, w.k); var wk = ctx.measureText(w.w).width; schrift(ctx, fs, false); var ww = wk + (w.n ? ctx.measureText(w.n).width : 0);
        if (z.length && b + sp + ww > breite) schiebe();
        b += (z.length ? sp : 0) + ww; z.push({ w: w.w, k: w.k, n: w.n || "", wk: wk, b: ww });
      });
      z.length && schiebe();
    });
    return zz;
  }
  function passe(ctx, absaetze, fs0, breite, maxH, lh, gross) {
    var fs = fs0, zz = [];
    for (var i = 0; i < 40; i++) {
      zz = satz(ctx, absaetze, fs, breite, gross);
      var hoch = hoehe(zz, fs, lh), lang = Math.max.apply(null, zz.map(function (z) { return z.b; }).concat([0]));
      if (hoch <= maxH && lang <= breite) break;
      fs *= 0.95;
    }
    return { zz: zz, fs: fs, lh: lh, hoch: hoehe(zz, fs, lh) };
  }
  function hoehe(zz, fs, lh) { return zz.reduce(function (s, z, i) { return s + fs * lh + (z.neu && i ? fs * 0.35 : 0); }, 0); }
  function male(ctx, r, y, farbe, links) {
    ctx.fillStyle = farbe; ctx.textBaseline = "alphabetic";
    r.zz.forEach(function (z, i) {
      z.neu && i && (y += r.fs * 0.35);
      schrift(ctx, r.fs, false); var sp = ctx.measureText(" ").width, x = links != null ? links : W / 2 - z.b / 2;
      z.w.forEach(function (w) { schrift(ctx, r.fs, w.k); ctx.fillText(w.w, x, y + r.fs * 0.86); if (w.n) { schrift(ctx, r.fs, false); ctx.fillText(w.n, x + w.wk, y + r.fs * 0.86); } x += w.b + sp; });
      y += r.fs * r.lh;
    });
    return y;
  }
  function gesperrt(ctx, t, cx, y, fs, farbe, abstand) {
    ctx.font = "600 " + fs + "px \"" + IN + "\""; ctx.fillStyle = farbe; ctx.textBaseline = "alphabetic";
    var zs = String(t).toLocaleUpperCase("de-DE").split(""), b = zs.reduce(function (s, c) { return s + ctx.measureText(c).width + abstand; }, -abstand), x = cx - b / 2;
    zs.forEach(function (c) { ctx.fillText(c, x, y); x += ctx.measureText(c).width + abstand; });
  }
  function absaetze(text) { return String(text || "").split(/\n+/).map(function (z) { return z.trim(); }).filter(Boolean); }

  function zeichne(canvas, look, slide, k, n, titel) {
    var ctx = canvas.getContext("2d"), a = AUSSCHNITT[k % AUSSCHNITT.length], abs = absaetze(slide.text);
    ctx.clearRect(0, 0, W, H);
    if (look === "karte") {
      /* Keine Fläche (Carina 23.10.: „keine Hintergrundfarbe, nur Overlays, die durchsichtig sind“): Foto randlos, unten ein Creme-Schleier. */
      ctx.fillStyle = F.espresso; ctx.fillRect(0, 0, W, H);
      foto && cover(ctx, foto, 0, 0, W, H, a);
      var gk = ctx.createLinearGradient(0, 880, 0, H);
      gk.addColorStop(0, "rgba(243,239,228,0)"); gk.addColorStop(0.28, "rgba(243,239,228,0.62)"); gk.addColorStop(1, "rgba(243,239,228,0.8)");
      ctx.fillStyle = gk; ctx.fillRect(0, 880, W, H - 880);
      var r = passe(ctx, abs, 76, 860, 420, 1.1, false), y = 1150 + (560 - r.hoch) / 2;
      gesperrt(ctx, k === 0 && titel ? titel : (k + 1) + " / " + n, W / 2, 1205, 24, F.sand, 7);
      male(ctx, r, Math.max(1250, y), F.tinte);
    } else if (look === "ruhig") {
      ctx.fillStyle = F.espresso; ctx.fillRect(0, 0, W, H);
      foto && weich(ctx, foto, a);
      ctx.fillStyle = "rgba(39,30,28,0.5)"; ctx.fillRect(0, 0, W, H);
      var sig = abs.length > 1 && abs[abs.length - 1].replace(/\*/g, "").length <= 44 ? abs.pop().replace(/\*/g, "") : "";
      var r2 = passe(ctx, abs, 90, 860, 700, 1.0, true), sigH = sig ? 125 : 0, y2 = 900 - (r2.hoch + sigH) / 2;
      var yE = male(ctx, r2, y2, F.weiss);
      if (sig) { ctx.font = "400 74px \"" + SIG + "\""; ctx.fillStyle = F.gold; ctx.textAlign = "center"; ctx.fillText(sig, W / 2, yE + 88, 900); ctx.textAlign = "left"; }
    } else {
      ctx.fillStyle = F.espresso; ctx.fillRect(0, 0, W, H);
      foto && cover(ctx, foto, 0, 0, W, H, a);
      var g = ctx.createLinearGradient(0, H * 0.35, 0, H);
      g.addColorStop(0, "rgba(39,30,28,0)"); g.addColorStop(0.55, "rgba(39,30,28,0.55)"); g.addColorStop(1, "rgba(39,30,28,0.9)");
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      var r3 = passe(ctx, abs, 84, 860, 620, 1.1, false), y3 = 1540 - r3.hoch;
      k === 0 && titel && gesperrt(ctx, titel, W / 2, y3 - 40, 26, F.weiss, 8);
      male(ctx, r3, y3, F.weiss);
    }
  }

  function rendereLinie(L) {
    L.files = L.files || []; L.nr = (L.nr || 0) + 1; var nr = L.nr;
    return schriften().then(function () {
      var kette = Promise.resolve();
      L.slides.forEach(function (s, k) {
        kette = kette.then(function () {
          if (nr !== L.nr) return;
          var c = document.createElement("canvas"); c.width = W; c.height = H;
          zeichne(c, L.look, s, k, L.slides.length, L.titel);
          return new Promise(function (ok) {
            c.toBlob(function (bl) {
              if (bl && nr === L.nr) {
                L.files[k] = new File([bl], "story-" + (L.nr0 + 1) + "-" + (k + 1) + ".jpg", { type: "image/jpeg" });
                var im = L.bilder && L.bilder[k]; if (im) { im.src && URL.revokeObjectURL(im.src); im.src = URL.createObjectURL(bl); }
              }
              c.width = c.height = 0; ok();
            }, "image/jpeg", 0.92);
          });
        });
      });
      return kette.then(function () { aktualisiereExport(); });
    });
  }

  function karte(L, i) {
    var box = el("div", "background:#fff;border-radius:18px;padding:14px;margin:0 0 14px;box-shadow:inset 0 0 0 1px #e6ddd0");
    L.box = box;
    var kopf = el("div", "display:flex;justify-content:space-between;align-items:flex-start;gap:10px");
    var t = el("div", "");
    t.appendChild(el("div", "font:600 11px -apple-system,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:" + F.sand, "Vorschlag " + "ABC"[i] + " · Look " + LOOKS.filter(function (x) { return x.id === L.look; })[0].name));
    L.lookInfo = t.firstChild;
    t.appendChild(el("div", "font:400 26px/1.1 '" + SERIF + "',serif;color:" + F.tinte + ";margin-top:4px", L.titel || "Storyline " + (i + 1)));
    L.idee && t.appendChild(el("div", "font:14px/1.4 -apple-system,sans-serif;color:#5b4f45;margin-top:4px", L.idee));
    var nehmen = knopf("Diese nehme ich"); nehmen.style.flex = "none"; L.nehmen = nehmen;
    nehmen.onclick = function () { wahl = wahl === i ? -1 : i; lines.forEach(function (x, j) { if (!x || !x.box) return; var an = wahl === j; x.box.style.boxShadow = an ? "inset 0 0 0 3px " + F.espresso : "inset 0 0 0 1px #e6ddd0"; x.nehmen.textContent = an ? "✓ Gewählt" : "Diese nehme ich"; x.nehmen.style.background = an ? F.espresso : "#fff"; x.nehmen.style.color = an ? "#fff" : F.espresso; }); aktualisiereExport(); };
    kopf.appendChild(t); kopf.appendChild(nehmen); box.appendChild(kopf);
    var reihe = el("div", "display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px -14px 0;padding:0 14px 6px");
    L.bilder = L.slides.map(function () { var im = el("img", "flex:none;width:132px;height:235px;object-fit:cover;border-radius:10px;background:#eee"); reihe.appendChild(im); return im; });
    box.appendChild(reihe);
    var st = L.slides.map(function (s, k) { return s.sticker ? "Slide " + (k + 1) + ": " + s.sticker : ""; }).filter(Boolean);
    st.length && box.appendChild(el("div", "font:13px/1.45 -apple-system,sans-serif;color:#5b4f45;margin-top:6px", "Sticker in Instagram dazu: " + st.join(" · ")));
    var leiste = el("div", "display:flex;gap:8px;flex-wrap:wrap;margin-top:10px");
    var lookB = knopf("Anderer Look"); lookB.style.padding = "9px 14px"; lookB.style.fontSize = "13px";
    lookB.onclick = function () { var k = LOOKS.map(function (x) { return x.id; }).indexOf(L.look); L.look = LOOKS[(k + 1) % LOOKS.length].id; L.lookInfo.textContent = "Vorschlag " + "ABC"[i] + " · Look " + LOOKS[(k + 1) % LOOKS.length].name; L.files = []; aktualisiereExport(); rendereLinie(L); };
    leiste.appendChild(lookB);
    var tx = el("details", "margin-top:10px;font:14px -apple-system,sans-serif;color:#5b4f45");
    tx.appendChild(el("summary", "cursor:pointer;font-weight:600;color:" + F.espresso, "Texte ändern"));
    L.slides.forEach(function (s, k) {
      var ta = el("textarea", "width:100%;box-sizing:border-box;margin-top:8px;border:1px solid #e6ddd0;border-radius:10px;padding:8px;font:15px/1.4 -apple-system,sans-serif"); ta.rows = 3; ta.value = s.text;
      var zt; ta.oninput = function () { s.text = ta.value; clearTimeout(zt); zt = setTimeout(function () { L.files = []; aktualisiereExport(); rendereLinie(L); }, 400); };
      tx.appendChild(el("div", "font:600 11px -apple-system,sans-serif;margin-top:10px;color:" + F.sand, "SLIDE " + (k + 1))); tx.appendChild(ta);
    });
    box.appendChild(leiste); box.appendChild(tx);
    return box;
  }

  function aktualisiereExport() {
    if (!exportB) return;
    var L = wahl >= 0 && lines[wahl], fertig = L && L.files && L.slides.every(function (s, k) { return L.files[k]; });
    exportB.disabled = !fertig;
    exportB.textContent = !L ? "Erst eine Storyline wählen" : fertig ? "Exportieren (" + L.slides.length + " Bilder)" : "Bilder werden vorbereitet …";
    exportB.style.opacity = fertig ? "1" : ".55";
  }
  function exportiere() {
    var L = wahl >= 0 && lines[wahl]; if (!L) return;
    var files = L.slides.map(function (s, k) { return L.files[k]; });
    if (files.some(function (f) { return !f; })) return;
    if (navigator.share && navigator.canShare && navigator.canShare({ files: files })) {
      navigator.share({ files: files }).catch(function (e) { if (!e || e.name !== "AbortError") galerie(files); }); return;
    }
    if (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) { galerie(files); return; }
    files.forEach(function (f, k) { setTimeout(function () { var a = document.createElement("a"); a.href = URL.createObjectURL(f); a.download = f.name; document.body.appendChild(a); a.click(); a.remove(); }, k * 400); });
  }
  function galerie(files) {
    var g = el("div", "position:fixed;inset:0;z-index:2147483005;background:" + F.espresso + ";overflow:auto;-webkit-overflow-scrolling:touch;padding:16px 16px 40px");
    var kopf = el("div", "position:sticky;top:-16px;background:" + F.espresso + ";padding:12px 0;display:flex;justify-content:space-between;align-items:center;color:#fff;font:15px/1.4 -apple-system,sans-serif;margin:-16px 0 14px;gap:10px");
    kopf.innerHTML = "<div><b>Bild lange drücken</b> → „Zu Fotos hinzufügen“</div>";
    var zu = knopf("Fertig"); zu.onclick = function () { g.remove(); }; kopf.appendChild(zu); g.appendChild(kopf);
    files.forEach(function (f) { var im = el("img", "display:block;width:100%;max-width:420px;margin:0 auto 16px;border-radius:12px"); im.src = URL.createObjectURL(f); g.appendChild(im); });
    document.body.appendChild(g);
  }

  function fotoLaden(datei, vorschau) {
    var fr = new FileReader();
    fr.onload = function () {
      var im = new Image();
      im.onload = function () {
        foto = im;
        var m = Math.min(1, 1024 / Math.max(im.width, im.height)), c = document.createElement("canvas");
        c.width = Math.round(im.width * m); c.height = Math.round(im.height * m); c.getContext("2d").drawImage(im, 0, 0, c.width, c.height);
        fotoKlein = c.toDataURL("image/jpeg", 0.82);
        vorschau.src = fotoKlein; vorschau.style.display = "block";
        status.textContent = "Foto bereit. Schreib optional dazu, was das für ein Moment ist.";
      };
      im.src = fr.result;
    };
    fr.readAsDataURL(datei);
  }

  function schreibe(moment, los) {
    if (!fotoKlein) { status.textContent = "Bitte zuerst ein Foto wählen."; return; }
    los.disabled = true; wahl = -1; lines = [null, null, null]; liste.innerHTML = ""; aktualisiereExport();
    status.textContent = "Schreibe 3 Storylines … (etwa 20 Sekunden)";
    var platz = [0, 1, 2].map(function (i) { var p = el("div", "background:#fff;border-radius:18px;padding:18px;margin:0 0 14px;box-shadow:inset 0 0 0 1px #e6ddd0;font:14px -apple-system,sans-serif;color:#8a7d72", "Vorschlag " + "ABC"[i] + " wird geschrieben …"); liste.appendChild(p); return p; });
    var fertig = 0;
    function eine(i) {
      return fetch("/.netlify/functions/foto-story", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ bild: fotoKlein, moment: moment, variante: i + 1 }) })
        .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw new Error(d && d.error || "Fehlgeschlagen"); return d; }); })
        .then(function (d) {
          var L = { nr0: i, titel: d.titel, idee: d.idee, slides: d.slides, look: LOOKS[i].id };
          lines[i] = L; var k = karte(L, i); liste.replaceChild(k, platz[i]); platz[i] = k; rendereLinie(L);
        })
        .catch(function (e) {
          platz[i].textContent = "Vorschlag " + "ABC"[i] + ": " + (e.message || e) + " ";
          var nb = knopf("Nochmal"); nb.style.padding = "8px 14px"; nb.onclick = function () { platz[i].textContent = "Vorschlag " + "ABC"[i] + " wird geschrieben …"; eine(i); }; platz[i].appendChild(nb);
        })
        .then(function () { fertig++; if (fertig >= 3) { los.disabled = false; status.textContent = "Fertig. Tippe bei deinem Favoriten auf „Diese nehme ich“, dann auf Exportieren."; } });
    }
    [0, 1, 2].forEach(eine);
  }

  function baue() {
    panel = el("div", "position:fixed;inset:0;z-index:2147483004;background:#F4F1EC;overflow:auto;display:none;-webkit-overflow-scrolling:touch");
    var kopf = el("div", "position:sticky;top:0;z-index:2;background:" + F.espresso + ";color:#fff;display:flex;align-items:center;justify-content:space-between;padding:14px 18px");
    kopf.appendChild(el("div", "font:400 26px/1 '" + SERIF + "',serif", "Foto-Story"));
    var zu = el("button", "border:0;background:none;color:#fff;font:600 22px/1 sans-serif;cursor:pointer;padding:6px 10px", "✕"); zu.type = "button";
    zu.onclick = function () { panel.style.display = "none"; };
    kopf.appendChild(zu); panel.appendChild(kopf);
    var inhalt = el("div", "max-width:760px;margin:0 auto;padding:18px 16px 120px");
    inhalt.appendChild(el("div", "font:15px/1.45 -apple-system,sans-serif;color:#4a3f37;margin-bottom:12px", "Ein echtes Foto aus deinem Alltag. Daraus werden 3 Storylines mit je 7 Slides, jede in einem anderen Look. Du nimmst eine und exportierst sie."));
    var datei = el("input"); datei.type = "file"; datei.accept = "image/*"; datei.style.display = "none";
    var waehle = knopf("Foto wählen", true);
    waehle.onclick = function () { datei.click(); };
    var vorschau = el("img", "display:none;width:120px;height:213px;object-fit:cover;border-radius:12px;margin:12px 0");
    datei.onchange = function () { datei.files && datei.files[0] && fotoLaden(datei.files[0], vorschau); };
    var moment = el("textarea", "width:100%;box-sizing:border-box;border:1px solid #e6ddd0;border-radius:12px;padding:10px;font:16px/1.4 -apple-system,sans-serif;background:#fff;margin-top:6px");
    moment.rows = 3; moment.placeholder = "Optional: Was ist das für ein Moment? z. B. „Kaffee nach dem Kita-Bringen, bevor ich die Videos meiner Mentees anschaue.“ Je echter, desto besser die Story.";
    var los = knopf("3 Storylines schreiben", true); los.style.marginTop = "10px";
    los.onclick = function () { schreibe(moment.value.trim(), los); };
    status = el("div", "font:14px/1.4 -apple-system,sans-serif;color:#5b4f45;min-height:20px;margin:10px 0 14px");
    liste = el("div");
    inhalt.appendChild(waehle); inhalt.appendChild(datei); inhalt.appendChild(vorschau); inhalt.appendChild(moment); inhalt.appendChild(los); inhalt.appendChild(status); inhalt.appendChild(liste);
    panel.appendChild(inhalt);
    var fuss = el("div", "position:fixed;left:0;right:0;bottom:0;z-index:3;padding:12px 16px calc(env(safe-area-inset-bottom) + 12px);background:rgba(244,241,236,.96);box-shadow:0 -1px 0 #e6ddd0;display:flex;justify-content:center");
    exportB = knopf("Erst eine Storyline wählen", true); exportB.style.width = "100%"; exportB.style.maxWidth = "520px"; exportB.onclick = exportiere;
    fuss.appendChild(exportB); panel.appendChild(fuss);
    document.body.appendChild(panel); aktualisiereExport();
  }
  function oeffne() { if (!panel) baue(); panel.style.display = "block"; }
  window.BS_FOTOSTORY = { oeffne: oeffne, test: { zeichne: zeichne, setzeFoto: function (im) { foto = im; }, schriften: schriften } };
})();
