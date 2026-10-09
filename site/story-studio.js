/* Story-Studio.
 *
 * Knopf „✦ Stories“ links unten öffnet ein eigenes Menü: Thema eintragen, Anzahl
 * wählen, „Stories schreiben“. Die Texte kommen aus /.netlify/functions/story-studio
 * (Carinas Story-Prompt, Gemini). Jede Story wird als Bild 1080×1920 im Klar-Stil
 * gesetzt: Foto mit weißem Text, Oxblood mit Gold-Element, Büttenpapier oder Schwarz.
 * Texte sind direkt editierbar, das Bild zieht sofort nach. Eigene Texte lassen sich
 * auch einfügen („Story 1 … Story 2 …“), dann braucht es keine KI.
 * „Stories zum Post“: Tag aus dem Content-Plan wählen, die Stories führen zu diesem Post
 * hin; die letzte Story zeigt das Titelbild des Posts als Karte mit „Neuer Post ↓“.
 */
(function () {
  var W = 1080, H = 1920, OX = "#5E1A21", OX2 = "#4A1219", SW = "#0E0E0E", OFF = "#F3EEE7", INK = "#17110F";
  var DESIGNS = ["foto", "oxblood", "papier", "schwarz"];
  var ELEMENTE = ["e1", "e3", "e7", "e11", "e15", "e2", "e8", "e14", "e10", "e9", "e13", "e4", "e12", "e5"];
  var stories = [], fotos = [], bilder = {}, panel = null, liste = null, status = null;
  var tage = [], zumPost = null, postFuer = null, fuelleTage = null;

  function serif() {
    var m = ""; try { m = localStorage.getItem("BS_MARKE") || ""; } catch (e) {}
    return m === "editorial-klar-playfair" ? "Playfair Display" : "Instrument Serif";
  }
  function ladeBild(src) {
    if (bilder[src]) return bilder[src];
    bilder[src] = new Promise(function (ok) {
      var fremd = /^https?:/i.test(src) && src.indexOf(location.origin) !== 0;
      var i = new Image(); if (fremd) i.crossOrigin = "anonymous";
      i.onload = function () { ok(i); }; i.onerror = function () { ok(null); }; i.src = src;
    });
    return bilder[src];
  }
  function ladeFotos() {
    return new Promise(function (ok) {
      try {
        var r = indexedDB.open("BrandStudioDB");
        r.onerror = function () { ok([]); };
        r.onsuccess = function () {
          var db = r.result;
          if (!db.objectStoreNames.contains("assets")) { db.close(); return ok([]); }
          var g = db.transaction("assets", "readonly").objectStore("assets").get("brand_images");
          g.onsuccess = function () {
            db.close();
            var a = Array.isArray(g.result) ? g.result : [];
            ok(a.map(function (x) { return typeof x === "string" ? x : (x && (x.src || x.dataUrl || x.url || x.data)) || ""; })
                .filter(function (x) { return /^(data:image|blob:|https?:|\/)/.test(x); }));
          };
          g.onerror = function () { db.close(); ok([]); };
        };
      } catch (e) { ok([]); }
    });
  }

  // ── Text setzen ──────────────────────────────────────────────────────────
  // ── Content-Plan (Tag 1 … x) aus der App-Datenbank ─────────────────────────
  function hookAus(t) {
    t = String(t || "").replace(/^\s*\[[^\]\n]{1,24}\]\s*/, "").replace(/\*+|__/g, "").replace(/\s+/g, " ").trim();
    var a = t.search(/(^|\s)&\s/); if (a > 0) t = t.slice(0, a).trim();
    var m = /^(.{12,}?[.!?])\s/.exec(t + " "); if (m) t = m[1];
    return t.length > 110 ? t.slice(0, t.lastIndexOf(" ", 107)) + " …" : t;
  }
  function ladePlan() {
    return new Promise(function (ok) {
      try {
        var r = indexedDB.open("BrandStudioDB");
        r.onerror = function () { ok([]); };
        r.onsuccess = function () {
          var db = r.result;
          if (!db.objectStoreNames.contains("assets")) { db.close(); return ok([]); }
          var g = db.transaction("assets", "readonly").objectStore("assets").get("content_plan");
          g.onsuccess = function () {
            db.close();
            var v = g.result, gal = [], days = [];
            if (Array.isArray(v)) days = v; else if (v && Array.isArray(v.days)) { days = v.days; gal = v.gallery || []; }
            ok(days.filter(function (d) { return d && Array.isArray(d.slides) && d.slides.length; }).map(function (d, k) {
              var sl = d.slides.map(function (x) { return String(x && (x.text || x.content) || "").trim(); }).filter(Boolean);
              var bg = String(d.slides[0] && d.slides[0].background || ""), m = /^@@img:(\d+)$/.exec(bg);
              var bild = m ? gal[+m[1]] : /^(data:image|blob:|https?:|\/)/.test(bg) ? bg : "";
              return { tag: d.day || k + 1, titel: d.title || "", caption: d.caption || "", slides: sl, bild: typeof bild === "string" ? bild : "", hook: hookAus(sl[0] || d.title || "") };
            }).sort(function (a, b) { return a.tag - b.tag; }));
          };
          g.onerror = function () { db.close(); ok([]); };
        };
      } catch (e) { ok([]); }
    });
  }

  function umbruch(ctx, text, breite) {
    var worte = String(text).split(/\s+/).filter(Boolean), zeilen = [], z = "";
    worte.forEach(function (w) {
      var t = z ? z + " " + w : w;
      if (z && ctx.measureText(t).width > breite) { zeilen.push(z); z = w; } else z = t;
    });
    z && zeilen.push(z);
    return zeilen;
  }
  function ausgeglichen(ctx, text, breite) {
    var n = umbruch(ctx, text, breite).length;
    if (n < 2) return umbruch(ctx, text, breite);
    var lo = breite * 0.5, hi = breite;
    for (var k = 0; k < 10; k++) { var m = (lo + hi) / 2; umbruch(ctx, text, m).length > n ? (lo = m) : (hi = m); }
    return umbruch(ctx, text, hi);
  }
  function setzeText(ctx, absaetze, box, farbe, fam) {
    var sk = 1, plan;
    for (var k = 0; k < 40; k++) {
      plan = []; var h = 0;
      absaetze.forEach(function (a, i) {
        var fs = (i === 0 ? 76 : 56) * sk, lh = fs * (i === 0 ? 1.04 : 1.16);
        ctx.font = "400 " + fs + "px \"" + fam + "\"";
        var z = ausgeglichen(ctx, a, box.w);
        if (i) h += fs * 0.75;
        plan.push({ fs: fs, lh: lh, zeilen: z, y: h });
        h += z.length * lh;
      });
      if (h <= box.h) break;
      sk *= 0.95;
    }
    var hoehe = plan.length ? plan[plan.length - 1].y + plan[plan.length - 1].zeilen.length * plan[plan.length - 1].lh : 0;
    var y0 = box.anker === "unten" ? box.y + box.h - hoehe : box.y + (box.h - hoehe) / 2;
    ctx.fillStyle = farbe; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    plan.forEach(function (p) {
      ctx.font = "400 " + p.fs + "px \"" + fam + "\"";
      p.zeilen.forEach(function (z, j) { ctx.fillText(z, W / 2, y0 + p.y + p.lh * j + p.fs * 0.82); });
    });
    return { oben: y0, unten: y0 + hoehe };
  }
  function riss(ctx, x, y, w, h) {
    ctx.beginPath(); var s = 0;
    function j() { s = (s * 9301 + 49297) % 233280; return s / 233280; }
    s = Math.round(w + h);
    ctx.moveTo(x, y + j() * 8);
    for (var i = 1; i <= 60; i++) ctx.lineTo(x + w * i / 60, y + j() * 8);
    for (i = 1; i <= 80; i++) ctx.lineTo(x + w - j() * 5, y + h * i / 80);
    for (i = 59; i >= 0; i--) ctx.lineTo(x + w * i / 60, y + h - j() * 12);
    for (i = 79; i > 0; i--) ctx.lineTo(x + j() * 5, y + h * i / 80);
    ctx.closePath();
  }
  function korn(ctx, alpha) {
    var c = document.createElement("canvas"); c.width = c.height = 200;
    var x = c.getContext("2d"), d = x.createImageData(200, 200);
    for (var k = 0; k < d.data.length; k += 4) { var v = Math.random() > 0.5 ? 255 : 0; d.data[k] = d.data[k + 1] = d.data[k + 2] = v; d.data[k + 3] = Math.random() * alpha; }
    x.putImageData(d, 0, 0); ctx.fillStyle = ctx.createPattern(c, "repeat"); ctx.fillRect(0, 0, W, H);
  }

  function pille(ctx, cta, cy) {
    ctx.font = "600 44px \"HelveticaNeueBrand\""; var tw = ctx.measureText(cta).width + 110;
    var gg = ctx.createLinearGradient(W / 2 - tw / 2, 0, W / 2 + tw / 2, 0);
    gg.addColorStop(0, "#9C7A33"); gg.addColorStop(0.35, "#E8CC86"); gg.addColorStop(0.55, "#F7E6B0"); gg.addColorStop(1, "#A47D31");
    ctx.save(); ctx.shadowColor = "rgba(0,0,0,.35)"; ctx.shadowBlur = 24; ctx.shadowOffsetY = 8;
    ctx.fillStyle = gg; ctx.beginPath(); var rx = W / 2 - tw / 2, rh = 104;
    ctx.moveTo(rx + 52, cy); ctx.arcTo(rx + tw, cy, rx + tw, cy + rh, 52); ctx.arcTo(rx + tw, cy + rh, rx, cy + rh, 52); ctx.arcTo(rx, cy + rh, rx, cy, 52); ctx.arcTo(rx, cy, rx + tw, cy, 52); ctx.fill(); ctx.restore();
    ctx.fillStyle = "#3a2608"; ctx.textAlign = "center"; ctx.fillText(cta, W / 2, cy + 68);
  }
  // Letzte Story „zum Post“: Text oben, Titelbild des Posts als Karte, goldene Pille.
  function zeichnePost(ctx, st, zeilen, cta, bild, fam) {
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = OX; ctx.fillRect(0, 0, W, H); korn(ctx, 22);
    ctx.font = "500 26px \"HelveticaNeueBrand\""; ctx.textAlign = "center"; ctx.fillStyle = "rgba(255,255,255,.72)";
    if ("letterSpacing" in ctx) ctx.letterSpacing = "9px";
    ctx.fillText("CARINA ANNA PRAV", W / 2, 200);
    if ("letterSpacing" in ctx) ctx.letterSpacing = "0px";
    if (zeilen.length) setzeText(ctx, zeilen, { y: 270, h: 420, w: W - 200, anker: "mitte" }, "#FFFFFF", fam);
    var cw = 600, ch = 750, top = 745, p = st.post || {};
    ctx.save(); ctx.translate(W / 2, top + ch / 2); ctx.rotate(-0.025);
    ctx.save(); ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 50; ctx.shadowOffsetY = 22;
    ctx.fillStyle = "#FBF8F3"; ctx.fillRect(-cw / 2 - 16, -ch / 2 - 16, cw + 32, ch + 32); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.rect(-cw / 2, -ch / 2, cw, ch); ctx.clip();
    if (bild) {
      var sk = Math.max(cw / bild.width, ch / bild.height), bw = bild.width * sk, bh = bild.height * sk;
      ctx.drawImage(bild, -bw / 2, -ch / 2 + Math.min(0, (ch - bh) * 0.3), bw, bh);
      var g = ctx.createLinearGradient(0, 0, 0, ch / 2); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, "rgba(0,0,0,.75)");
      ctx.fillStyle = g; ctx.fillRect(-cw / 2, 0, cw, ch / 2);
    } else { ctx.fillStyle = SW; ctx.fillRect(-cw / 2, -ch / 2, cw, ch); }
    var hook = p.hook || p.titel || "";
    if (hook) {
      ctx.font = "400 54px \"" + fam + "\""; ctx.fillStyle = "#FFFFFF"; ctx.textAlign = "center";
      var zl = umbruch(ctx, hook, cw - 90).slice(0, 4), lh = 60;
      zl.forEach(function (z, k) { ctx.fillText(z, 0, ch / 2 - 50 - (zl.length - 1 - k) * lh); });
    }
    ctx.restore();
    ctx.save(); ctx.translate(0, -ch / 2 - 6); ctx.rotate(0.04); ctx.fillStyle = "rgba(227,106,44,.92)"; ctx.fillRect(-150, -30, 300, 60);
    ctx.font = "600 26px \"HelveticaNeueBrand\""; ctx.fillStyle = "#FFFFFF"; ctx.textAlign = "center";
    if ("letterSpacing" in ctx) ctx.letterSpacing = "6px";
    ctx.fillText("NEUER POST", 3, 10);
    if ("letterSpacing" in ctx) ctx.letterSpacing = "0px";
    ctx.restore(); ctx.restore();
    pille(ctx, cta || "Neuer Post ↓", 1565);
  }

  // ── Eine Story zeichnen ──────────────────────────────────────────────────
  function zeichne(st, i, n, canvas) {
    var ctx = canvas.getContext("2d"), fam = serif();
    var zeilen = String(st.text || "").split(/\n+/).map(function (z) { return z.trim(); }).filter(Boolean);
    var cta = "";
    zeilen = zeilen.filter(function (z) { if ((/STARTEN/.test(z) || /^Neuer Post\b/i.test(z)) && z.length < 60) { cta = z; return false; } return true; });
    var design = st.design || DESIGNS[0];
    var foto = design === "foto" && fotos.length && !st._ohneFoto ? fotos[(i * 3 + 1) % fotos.length] : "";
    if (design === "foto" && !foto) design = "oxblood";
    return Promise.all([
      foto ? ladeBild(foto) : design === "post" && st.post && st.post.bild ? ladeBild(st.post.bild) : null,
      design === "oxblood" || design === "schwarz" ? ladeBild("/scrap/" + ELEMENTE[(i * 5 + (st.el || 0)) % ELEMENTE.length] + ".webp") : null,
      document.fonts.load("400 60px \"" + fam + "\""), document.fonts.load("500 30px \"HelveticaNeueBrand\""), document.fonts.load("400 40px \"Nothing You Could Do\"")
    ].map(function (p) { return Promise.resolve(p).catch(function () { return null; }); })).then(function (r) {
      var bild = r[0], el = r[1], weiss = design !== "papier";
      if (design === "post") { zeichnePost(ctx, st, zeilen, cta, bild, fam); return; }
      ctx.clearRect(0, 0, W, H);
      if (design === "foto" && bild) {
        var s = Math.max(W / bild.width, H / bild.height), bw = bild.width * s, bh = bild.height * s;
        ctx.drawImage(bild, (W - bw) / 2, Math.min(0, (H - bh) * 0.3), bw, bh);
        ctx.fillStyle = "rgba(0,0,0," + (i % 2 ? 0.3 : 0.42) + ")"; ctx.fillRect(0, 0, W, H);
        var g = ctx.createLinearGradient(0, H * 0.35, 0, H); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, "rgba(0,0,0,.72)");
        ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      } else {
        ctx.fillStyle = design === "schwarz" ? SW : design === "papier" ? OX2 : OX; ctx.fillRect(0, 0, W, H);
        korn(ctx, design === "schwarz" ? 14 : 22);
      }
      if (design === "papier") {
        ctx.save(); ctx.shadowColor = "rgba(0,0,0,.35)"; ctx.shadowBlur = 40; ctx.shadowOffsetY = 18;
        ctx.fillStyle = "#FBF8F3"; riss(ctx, 80, 300, W - 160, H - 640); ctx.fill(); ctx.restore();
        ctx.save(); ctx.translate(W / 2, 300); ctx.rotate(-0.05); ctx.fillStyle = "rgba(227,106,44,.85)"; ctx.fillRect(-120, -26, 240, 52); ctx.restore();
      }
      // Absender oben, dezent
      ctx.font = "500 26px \"HelveticaNeueBrand\""; ctx.textAlign = "center";
      ctx.fillStyle = weiss ? "rgba(255,255,255,.72)" : "rgba(23,17,15,.6)";
      if ("letterSpacing" in ctx) ctx.letterSpacing = "9px";
      ctx.fillText("CARINA ANNA PRAV", W / 2, design === "papier" ? 400 : 200);
      if ("letterSpacing" in ctx) ctx.letterSpacing = "0px";
      if (el) { var es = 230 / Math.max(el.width, el.height); ctx.save(); ctx.translate(W - 190, 330); ctx.rotate(0.14); ctx.drawImage(el, -el.width * es / 2, -el.height * es / 2, el.width * es, el.height * es); ctx.restore(); }
      var unten = H - 360 - (st.sticker ? 330 : 0) - (cta ? 170 : 0);
      var box = design === "papier" ? { y: 460, h: Math.min(unten, H - 420) - 460, w: W - 300, anker: "mitte" }
        : design === "foto" ? { y: 520, h: unten - 520, w: W - 200, anker: "unten" }
        : { y: 470, h: unten - 470, w: W - 200, anker: "mitte" };
      setzeText(ctx, zeilen, box, weiss ? "#FFFFFF" : INK, fam);
      if (st.sticker) {
        var sy = unten + 40;
        ctx.save(); ctx.setLineDash([14, 12]); ctx.lineWidth = 3; ctx.strokeStyle = weiss ? "rgba(255,255,255,.35)" : "rgba(23,17,15,.3)";
        ctx.strokeRect(170, sy, W - 340, 250); ctx.restore();
      }
      if (cta) pille(ctx, cta, H - 360 - 130);
    });
  }

  // ── Themen aus Carinas Narrativ (nur Material aus ihrem Prompt, nichts erfunden) ──
  var THEMEN = [
    { s: "Ja zu dir", t: [
      "Ja sagen, bevor du dich bereit fühlst",
      "Warten aufs Bereitsein kostet dich mehr als jedes Programm",
      "Du bist nicht zu viel. Du bist nur noch nicht sichtbar genug",
      "Woran du eine Ja-Sagerin erkennst",
      "Der Moment, in dem du Ja zu dir sagst, obwohl alle anderen zögern"
    ] },
    { s: "Meine Geschichte", t: [
      "Mit 15 der Traum Amerika, mit 21 dort: was mir das über Ja-Sagen beigebracht hat",
      "Ich hatte als Kind keine Mentorin und hab mir meine Mentoren immer selbst gesucht",
      "Zweimal ohne Mentoring im Business: was mich das gekostet hat",
      "Bühne, US-Radio, TV: Sichtbarkeit kann man trainieren",
      "18 Jahre in Businesses jeder Größe, vom Millionenprojekt bis zum kleinen Business Case"
    ] },
    { s: "Umsetzen", t: [
      "Wissen sammeln ohne Umsetzen ist der teuerste Fehler fähiger Frauen",
      "Ich judge nichts. Außer, wenn du's nicht umsetzt",
      "Ich schau jedes Video meiner Mentees an und sag die Lücke sofort",
      "Allein rumprobieren fühlt sich sparsam an und ist das Teuerste überhaupt",
      "Der nächste Kurs ist nicht dein Problem. Dein Umsetzen ist es"
    ] },
    { s: "Angebot & Preis", t: [
      "Rabattieren fühlt sich nett an und kostet dich deinen Wert",
      "Was ein Angebot hat, das sich verkauft",
      "Content, der verkauft, statt Content, der nur gefällt",
      "Warum du deinen Content nicht selbst schreiben musst (Done-for-you Content)",
      "Vom Wissen im Kopf zum fertigen Angebot (Offer Incubator)"
    ] },
    { s: "Mama & Business", t: [
      "Mama, Job, Business: meine Videos entstehen auch mal am Abend",
      "Du brauchst keinen perfekten Tag, um dein Business zu bauen",
      "Wenn das Kind schläft und du trotzdem Ja zu dir sagst"
    ] },
    { s: "Ergebnisse & Angebote", t: [
      "Was meine Kundinnen umgesetzt haben: Membership-Plätze, 1:1-Plätze, vierstellige Umsätze",
      "Das Intensive: für wen es ist und für wen nicht",
      "Das 1:1: wann es sich für dich lohnt",
      "Für wen ich nicht die Richtige bin"
    ] }
  ];
  var ALLE_THEMEN = THEMEN.reduce(function (a, g) { return a.concat(g.t); }, []);
  function heute() { var d = new Date(); return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(); }
  function themaDesTages() {
    var tag = Math.floor((Date.now() - new Date().getTimezoneOffset() * 60000) / 86400000);
    var g = THEMEN[tag % THEMEN.length];
    return g.t[Math.floor(tag / THEMEN.length) % g.t.length];
  }

  // ── Menü ─────────────────────────────────────────────────────────────────
  function knopf(text, primaer) {
    var b = document.createElement("button"); b.type = "button"; b.textContent = text;
    b.style.cssText = "border:0;border-radius:999px;padding:12px 18px;font:600 14px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;cursor:pointer;" +
      (primaer ? "background:" + OX + ";color:#fff" : "background:#fff;color:" + OX + ";box-shadow:inset 0 0 0 1.5px " + OX);
    return b;
  }
  function parseEigen(t) {
    var teile = String(t).split(/\n?\s*Story\s*\d+\s*[:.\-–]?\s*\n?/i).map(function (x) { return x.trim(); }).filter(Boolean);
    return teile.map(function (x) {
      var st = "", z = x.split("\n").filter(function (l) { if (/^\s*(📊|💬)/.test(l)) { st = l.trim(); return false; } return true; });
      return { text: z.join("\n").trim(), sticker: st };
    }).filter(function (s) { return s.text; });
  }
  function startDesigns() {
    stories.forEach(function (s, i) {
      s.post = postFuer || null;
      s.design = i === stories.length - 1 ? (postFuer ? "post" : "oxblood") : i === 0 ? (fotos.length ? "foto" : "oxblood") : ["oxblood", "foto", "papier", "schwarz"][(i - 1) % 4];
    });
  }
  function zeigeStories() {
    liste.innerHTML = "";
    if (!stories.length) return;
    var leiste = document.createElement("div"); leiste.style.cssText = "display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 14px";
    var alle = knopf("Alle Bilder speichern", true); alle.onclick = alleSpeichern; leiste.appendChild(alle);
    var tx = knopf("Alle Texte kopieren"); tx.onclick = function () { kopiere(stories.map(function (s, i) { return "Story " + (i + 1) + "\n" + s.text + (s.sticker ? "\n" + s.sticker : ""); }).join("\n\n"), tx); }; leiste.appendChild(tx);
    liste.appendChild(leiste);
    stories.forEach(function (st, i) {
      var karte = document.createElement("div");
      karte.style.cssText = "background:#fff;border-radius:18px;padding:14px;margin-bottom:16px;box-shadow:0 2px 14px rgba(0,0,0,.06);display:flex;gap:14px;flex-wrap:wrap";
      var cv = document.createElement("img"); cv.alt = "Story " + (i + 1);
      cv.style.cssText = "width:170px;height:302px;border-radius:12px;background:#ddd;flex:none;object-fit:cover";
      var rechts = document.createElement("div"); rechts.style.cssText = "flex:1;min-width:200px;display:flex;flex-direction:column;gap:8px";
      var kopf = document.createElement("div"); kopf.textContent = "Story " + (i + 1); kopf.style.cssText = "font:700 13px/1 -apple-system,sans-serif;color:" + OX + ";letter-spacing:.08em;text-transform:uppercase";
      var ta = document.createElement("textarea"); ta.value = st.text; ta.rows = 8;
      ta.style.cssText = "width:100%;border:1px solid #e5ddd8;border-radius:12px;padding:10px;font:15px/1.45 -apple-system,sans-serif;resize:vertical";
      var stk = document.createElement("div"); stk.style.cssText = "font:13px/1.4 -apple-system,sans-serif;color:#5b4a46";
      stk.textContent = st.sticker ? "Sticker in Instagram setzen (gestrichelter Platz): " + st.sticker : "";
      var reihe = document.createElement("div"); reihe.style.cssText = "display:flex;gap:6px;flex-wrap:wrap";
      var b1 = knopf("Bild speichern", true), b2 = knopf("Design wechseln"), b3 = knopf("Text kopieren");
      var neu = function () { rendere(st, i); };
      var t; ta.oninput = function () { st.text = ta.value; clearTimeout(t); t = setTimeout(neu, 250); };
      b1.onclick = function () { speichere([st]); };
      b2.onclick = function () { var D = st.post ? DESIGNS.concat(["post"]) : DESIGNS, k = D.indexOf(st.design); st.design = D[(k + 1) % D.length]; if (st.design === "foto" && !fotos.length) st.design = D[(k + 2) % D.length]; st.el = (st.el || 0) + 1; neu(); };
      b3.onclick = function () { kopiere(st.text + (st.sticker ? "\n" + st.sticker : ""), b3); };
      reihe.appendChild(b1); reihe.appendChild(b2); reihe.appendChild(b3);
      rechts.appendChild(kopf); rechts.appendChild(ta); rechts.appendChild(stk); rechts.appendChild(reihe);
      karte.appendChild(cv); karte.appendChild(rechts); liste.appendChild(karte);
      st._img = cv; neu();
    });
  }
  function kopiere(t, b) {
    try { navigator.clipboard.writeText(t); var a = b.textContent; b.textContent = "Kopiert ✓"; setTimeout(function () { b.textContent = a; }, 1400); } catch (e) {}
  }
  // Bilder werden nach jedem Zeichnen schon als Datei vorbereitet: iPhone/Safari erlaubt
  // „Teilen → Bilder sichern“ nur direkt beim Tippen, ohne Warten dazwischen.
  var leinwand = null, schlange = [], laeuft = false;
  function rendere(st, i) {
    st._file = null; st._nr = (st._nr || 0) + 1;
    schlange = schlange.filter(function (q) { return q.st !== st; }); schlange.push({ st: st, i: i });
    fortschritt(); arbeite();
  }
  function arbeite() {
    if (laeuft || !schlange.length) return;
    laeuft = true;
    var q = schlange.shift(), st = q.st, nr = st._nr;
    if (!leinwand) { leinwand = document.createElement("canvas"); leinwand.width = W; leinwand.height = H; }
    var weiter = function () { laeuft = false; fortschritt(); setTimeout(arbeite, 0); };
    zeichne(st, q.i, stories.length, leinwand).then(function () {
      if (nr !== st._nr) return weiter();
      try {
        leinwand.toBlob(function (bl) {
          if (nr === st._nr) {
            if (bl) {
              st._file = new File([bl], "story-" + (q.i + 1) + ".jpg", { type: "image/jpeg" });
              if (st._img) { if (st._url) URL.revokeObjectURL(st._url); st._url = URL.createObjectURL(bl); st._img.src = st._url; }
            } else if (!st._nochmal) { st._nochmal = 1; schlange.push(q); st._nr++; }
          }
          weiter();
        }, "image/jpeg", 0.92);
      } catch (e) {
        if (!st._ohneFoto) { st._ohneFoto = true; st._nr++; schlange.unshift(q); }
        weiter();
      }
    }).catch(function () { weiter(); });
  }
  function fortschritt() {
    if (!stories.length || !status) return;
    var fertig = stories.filter(function (s) { return s._file; }).length;
    if (fertig < stories.length) status.textContent = "Bilder werden vorbereitet … " + fertig + " von " + stories.length;
    else if (/vorbereitet/.test(status.textContent)) status.textContent = "Alle " + stories.length + " Bilder bereit ✓";
  }
  function speichere(liste) {
    var files = liste.map(function (s) { return s._file; });
    if (files.some(function (f) { return !f; })) { fortschritt(); arbeite(); return; }
    if (navigator.share && navigator.canShare && navigator.canShare({ files: files })) {
      navigator.share({ files: files }).catch(function (e) { if (!e || e.name !== "AbortError") galerie(files); });
      return;
    }
    if (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) { galerie(files); return; }
    files.forEach(function (f, k) { setTimeout(function () { var a = document.createElement("a"); a.href = URL.createObjectURL(f); a.download = f.name; document.body.appendChild(a); a.click(); a.remove(); }, k * 400); });
  }
  // Ersatz, falls Teilen nicht geht: alle Bilder groß zeigen, lange drücken → „Zu Fotos hinzufügen“.
  function galerie(files) {
    var g = document.createElement("div");
    g.style.cssText = "position:fixed;inset:0;z-index:2147483003;background:#1d0b0e;overflow:auto;-webkit-overflow-scrolling:touch;padding:16px 16px 40px";
    var kopf = document.createElement("div"); kopf.style.cssText = "position:sticky;top:-16px;z-index:1;background:#1d0b0e;padding:12px 0;display:flex;justify-content:space-between;align-items:center;color:#fff;font:15px/1.4 -apple-system,sans-serif;margin:-16px 0 14px;gap:10px";
    kopf.innerHTML = "<div><b>Bild lange drücken</b> → „Zu Fotos hinzufügen“</div>";
    var zu = document.createElement("button"); zu.type = "button"; zu.textContent = "Fertig"; zu.style.cssText = "border:0;border-radius:999px;padding:10px 16px;font:600 14px -apple-system,sans-serif;background:#fff;color:" + OX;
    zu.onclick = function () { g.remove(); }; kopf.appendChild(zu); g.appendChild(kopf);
    files.forEach(function (f) { var im = document.createElement("img"); im.src = URL.createObjectURL(f); im.alt = f.name; im.style.cssText = "display:block;width:100%;max-width:420px;margin:0 auto 16px;border-radius:12px"; g.appendChild(im); });
    document.body.appendChild(g);
  }
  function alleSpeichern() { speichere(stories); }

  function oeffne() {
    if (!panel) baue();
    panel.style.display = "block"; document.body.style.overflow = "hidden";
    ladeFotos().then(function (f) { fotos = f; });
    ladePlan().then(function (t) { tage = t; fuelleTage && fuelleTage(); });
  }
  function schliesse() { panel.style.display = "none"; document.body.style.overflow = ""; }
  function baue() {
    panel = document.createElement("div"); panel.id = "bs-story";
    panel.style.cssText = "position:fixed;inset:0;z-index:2147483002;background:#F6F2EE;overflow:auto;display:none;-webkit-overflow-scrolling:touch";
    var kopf = document.createElement("div");
    kopf.style.cssText = "position:sticky;top:0;z-index:2;background:" + OX + ";color:#fff;display:flex;align-items:center;justify-content:space-between;padding:14px 18px";
    kopf.innerHTML = "<div style=\"font:400 26px/1 'Instrument Serif',serif\">Story-Studio</div>";
    var zu = document.createElement("button"); zu.type = "button"; zu.textContent = "✕"; zu.style.cssText = "border:0;background:none;color:#fff;font:600 22px/1 sans-serif;cursor:pointer;padding:6px 10px"; zu.onclick = schliesse;
    kopf.appendChild(zu); panel.appendChild(kopf);
    var inhalt = document.createElement("div"); inhalt.style.cssText = "max-width:760px;margin:0 auto;padding:18px 16px 60px";
    inhalt.innerHTML = "<div style=\"font:600 13px/1 -apple-system,sans-serif;color:" + OX + ";letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px\">Thema heute</div>";
    var thema = document.createElement("textarea"); thema.rows = 3; thema.placeholder = "z. B. Warum du nicht bereit sein musst, um zu verkaufen";
    thema.style.cssText = "width:100%;border:1px solid #e5ddd8;border-radius:14px;padding:12px;font:16px/1.4 -apple-system,sans-serif;background:#fff";
    try { thema.value = localStorage.getItem("BS_STORY_TAG") === heute() ? localStorage.getItem("BS_STORY_THEMA") || "" : ""; } catch (e) {}
    if (!thema.value) thema.value = themaDesTages();
    var chipCss = "border:0;border-radius:999px;padding:9px 13px;margin:0 6px 6px 0;font:500 13px/1.25 -apple-system,sans-serif;cursor:pointer;text-align:left;background:#fff;color:#3b2a27;box-shadow:inset 0 0 0 1px #e5ddd8";
    function waehle(t) { setzePost(null); thema.value = t; try { localStorage.setItem("BS_STORY_THEMA", t); localStorage.setItem("BS_STORY_TAG", heute()); } catch (e) {} thema.focus(); }
    var tagesZeile = document.createElement("div"); tagesZeile.style.cssText = "display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 0";
    var tagesB = knopf("☀ Thema des Tages"); tagesB.style.padding = "9px 14px"; tagesB.style.fontSize = "13px";
    tagesB.onclick = function () { waehle(themaDesTages()); };
    var zufallB = knopf("↻ Anderes Thema"); zufallB.style.padding = "9px 14px"; zufallB.style.fontSize = "13px";
    zufallB.onclick = function () { var t; do { t = ALLE_THEMEN[Math.floor(Math.random() * ALLE_THEMEN.length)]; } while (t === thema.value && ALLE_THEMEN.length > 1); waehle(t); };
    tagesZeile.appendChild(tagesB); tagesZeile.appendChild(zufallB);
    var themen = document.createElement("details"); themen.style.cssText = "margin:10px 0 0;font:14px -apple-system,sans-serif;color:#5b4a46";
    themen.innerHTML = "<summary style=\"cursor:pointer;font-weight:600;color:" + OX + "\">Themen aus deinem Narrativ</summary>";
    THEMEN.forEach(function (g) {
      var h = document.createElement("div"); h.textContent = g.s;
      h.style.cssText = "font:600 11px/1 -apple-system,sans-serif;color:" + OX + ";letter-spacing:.08em;text-transform:uppercase;margin:14px 0 8px";
      themen.appendChild(h);
      var w = document.createElement("div");
      g.t.forEach(function (t) { var c = document.createElement("button"); c.type = "button"; c.textContent = t; c.style.cssText = chipCss; c.onclick = function () { waehle(t); themen.open = false; window.scrollTo && panel.scrollTo({ top: 0, behavior: "smooth" }); }; w.appendChild(c); });
      themen.appendChild(w);
    });
    var postBlock = document.createElement("div"); postBlock.style.cssText = "margin:0 0 18px";
    postBlock.innerHTML = "<div style=\"font:600 13px/1 -apple-system,sans-serif;color:" + OX + ";letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px\">Stories zum Post</div><div style=\"font:13px/1.4 -apple-system,sans-serif;color:#7a6a66;margin-bottom:8px\">Tag wählen: die Stories führen zu diesem Post, der Post ist das Ende.</div>";
    var tagReihe = document.createElement("div"); tagReihe.style.cssText = "display:flex;gap:6px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:4px";
    var tagInfo = document.createElement("div"); tagInfo.style.cssText = "font:13px/1.4 -apple-system,sans-serif;color:#3b2a27;margin-top:6px;min-height:0";
    postBlock.appendChild(tagReihe); postBlock.appendChild(tagInfo);
    function setzePost(d) {
      zumPost = d;
      [].forEach.call(tagReihe.children, function (c) { var an = d && c.__tag === d.tag; c.style.background = an ? OX : "#fff"; c.style.color = an ? "#fff" : OX; });
      tagInfo.textContent = d ? "Führt zu Tag " + d.tag + ": „" + d.hook + "“" : "";
    }
    fuelleTage = function () {
      tagReihe.innerHTML = "";
      if (!tage.length) { tagReihe.innerHTML = "<div style=\"font:13px -apple-system,sans-serif;color:#9a8a86\">Noch kein Plan mit Posts – erst einen Plan erstellen.</div>"; return; }
      tage.forEach(function (d) {
        var c = knopf("Tag " + d.tag); c.__tag = d.tag; c.style.padding = "9px 14px"; c.style.fontSize = "13px"; c.style.flex = "none";
        c.onclick = function () {
          if (zumPost && zumPost.tag === d.tag) { setzePost(null); return; }
          setzePost(d); thema.value = "Hinführung zu meinem neuen Post: " + d.hook;
        };
        tagReihe.appendChild(c);
      });
      if (zumPost) setzePost(tage.filter(function (d) { return d.tag === zumPost.tag; })[0] || null);
    };
    fuelleTage();
    var zeile = document.createElement("div"); zeile.style.cssText = "display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:12px 0";
    var anz = document.createElement("select"); anz.style.cssText = "border:1px solid #e5ddd8;border-radius:999px;padding:11px 14px;font:600 14px -apple-system,sans-serif;background:#fff";
    [5, 6, 7].forEach(function (n) { var o = document.createElement("option"); o.value = n; o.textContent = n + " Stories"; n === 6 && (o.selected = true); anz.appendChild(o); });
    var los = knopf("Stories schreiben", true);
    status = document.createElement("div"); status.style.cssText = "font:14px/1.4 -apple-system,sans-serif;color:#5b4a46;min-height:20px;margin:6px 0";
    los.onclick = function () {
      var t = thema.value.trim(); if (!t) { status.textContent = "Bitte zuerst ein Thema eintragen."; return; }
      try { localStorage.setItem("BS_STORY_THEMA", t); localStorage.setItem("BS_STORY_TAG", heute()); } catch (e) {}
      los.disabled = true; status.textContent = "Schreibe Stories … (dauert etwa 20 Sekunden)";
      fetch("/.netlify/functions/story-studio", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ thema: t, count: Number(anz.value), post: zumPost ? { titel: zumPost.titel, slides: zumPost.slides, caption: zumPost.caption } : undefined }) })
        .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw new Error(d && d.error || "Fehlgeschlagen"); return d; }); })
        .then(function (d) { stories = d.stories || []; postFuer = zumPost; return ladeFotos().then(function (f) { fotos = f; startDesigns(); zeigeStories(); status.textContent = stories.length + " Stories fertig. Texte kannst du direkt ändern."; }); })
        .catch(function (e) { status.textContent = "Fehler: " + (e.message || e); })
        .then(function () { los.disabled = false; });
    };
    zeile.appendChild(anz); zeile.appendChild(los);
    var eigen = document.createElement("details"); eigen.style.cssText = "margin:4px 0 16px;font:14px -apple-system,sans-serif;color:#5b4a46";
    eigen.innerHTML = "<summary style=\"cursor:pointer\">Eigene Texte einfügen (Story 1 … Story 2 …)</summary>";
    var eta = document.createElement("textarea"); eta.rows = 6; eta.placeholder = "Story 1\nText …\n\nStory 2\nText …";
    eta.style.cssText = "width:100%;margin-top:8px;border:1px solid #e5ddd8;border-radius:12px;padding:10px;font:15px/1.4 -apple-system,sans-serif;background:#fff";
    var eb = knopf("Als Stories setzen"); eb.style.marginTop = "8px";
    eb.onclick = function () { stories = parseEigen(eta.value); postFuer = zumPost; ladeFotos().then(function (f) { fotos = f; startDesigns(); zeigeStories(); status.textContent = stories.length ? stories.length + " Stories gesetzt." : "Keine Stories erkannt – schreib „Story 1“, „Story 2“ … davor."; }); };
    eigen.appendChild(eta); eigen.appendChild(eb);
    liste = document.createElement("div");
    inhalt.insertBefore(postBlock, inhalt.firstChild); inhalt.appendChild(thema); inhalt.appendChild(tagesZeile); inhalt.appendChild(themen); inhalt.appendChild(zeile); inhalt.appendChild(status); inhalt.appendChild(eigen); inhalt.appendChild(liste);
    panel.appendChild(inhalt); document.body.appendChild(panel);
  }
  function start() {
    if (document.getElementById("bs-story-knopf")) return;
    var css = document.createElement("style");
    css.textContent = "#bs-story-knopf{position:fixed;left:10px;bottom:154px;z-index:2147483001;border:0;border-radius:999px;padding:9px 13px;cursor:pointer;" +
      "background:" + OX + ";color:#fff;font:600 12px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.25)}" +
      "body.bs-insta #bs-story-knopf,body.bs-auswahl #bs-story-knopf{display:none}";
    document.head.appendChild(css);
    var b = document.createElement("button"); b.id = "bs-story-knopf"; b.type = "button"; b.textContent = "✦ Stories"; b.onclick = oeffne;
    document.body.appendChild(b);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
  window.BS_STORY_TEST = { setze: function (a, post) { stories = a; postFuer = post || null; startDesigns(); zeigeStories(); }, oeffne: oeffne, fotos: function (f) { fotos = f; } };
})();
