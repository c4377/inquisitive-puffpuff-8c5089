/* Hook-Generator (Carina 24.10.): Hooks in ihrer Stimme, für Feed-Posts oder Reels.
 *
 * Geöffnet über „✎ Hooks“ im Story-Studio. Feed: Slide 1 im Bulk-Format, passend zum Feed-Rhythmus
 * (Quote- und Kuli-Tage ohne Zeichen, Zeichen A–D nur wo erlaubt). „Ab Tag“ ist der Tag nach dem letzten
 * Tag im Plan, damit der Rhythmus beim Anhängen stimmt. Reels: Satz der ersten 2 Sekunden plus Format.
 * Mehr als 20 Hooks werden in Paketen zu 20 parallel geschrieben, jedes Paket mit eigenem Schwerpunkt.
 * Hooks lassen sich abhaken; „Kopieren“ legt die ausgewählten in die Zwischenablage (Feed im Bulk-Format).
 * „mit Caption“ (Standard an, Carina 24.10.): zu jedem Hook eine Caption, im Feed als „Caption:“ im Bulk-Format;
 * dann Pakete zu 10, weil die Antworten länger sind.
 */
(function () {
  if (window.BS_RAUM) return;
  var ES = "#271E1C", SAND = "#635645", TINTE = "#16130F";
  var WINKEL = [
    "Funkstille zwischen Like und Anfrage, Angebot klar sagen",
    "Echt statt perfekt, sich zeigen, Angst vor Hate und laut sein",
    "Typische Sätze der Zielkundin wörtlich zitieren und übersetzen",
    "Carinas Geschichte und Fakten, immer mit Bedeutung für die Leserin",
    "Haltung zu Content: Karussells, Mehrwert, Inspo sammeln, Tipps vs. Entscheidungen"
  ];
  var panel = null, liste = null, status = null, hooks = [], art = "feed", mitCaption = true, stil = "klartext";

  function el(tag, css, txt) { var e = document.createElement(tag); css && (e.style.cssText = css); txt != null && (e.textContent = txt); return e; }
  function knopf(t, primaer) {
    var b = el("button", "border:0;border-radius:999px;padding:11px 16px;font:600 14px -apple-system,sans-serif;cursor:pointer;" + (primaer ? "background:" + ES + ";color:#fff" : "background:#fff;color:" + ES + ";box-shadow:inset 0 0 0 1px #ddd3c6"), t);
    b.type = "button"; return b;
  }
  function letzterTag() {
    return new Promise(function (ok) {
      try {
        var r = indexedDB.open("BrandStudioDB");
        r.onerror = function () { ok(0); };
        r.onsuccess = function () {
          var db = r.result;
          try {
            var g = db.transaction("assets").objectStore("assets").get("content_plan");
            g.onsuccess = function () { var a = Array.isArray(g.result) ? g.result : []; db.close(); ok(a.reduce(function (m, d) { return Math.max(m, Number(d && d.day) || 0); }, 0)); };
            g.onerror = function () { db.close(); ok(0); };
          } catch (e) { db.close(); ok(0); }
        };
      } catch (e) { ok(0); }
    });
  }
  function bulkText(h) { return "Tag " + h.tag + ": " + h.thema + "\nSlide 1: " + h.slide1 + (h.caption ? "\nCaption:\n" + h.caption : ""); }
  function kopiere(t, b) {
    var fertig = function () { var a = b.textContent; b.textContent = "Kopiert ✓"; setTimeout(function () { b.textContent = a; }, 1600); };
    try { navigator.clipboard.writeText(t).then(fertig, function () { alt(); }); } catch (e) { alt(); }
    function alt() { var ta = el("textarea"); ta.value = t; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); fertig(); } catch (e) {} ta.remove(); }
  }

  function zeige() {
    liste.innerHTML = "";
    if (!hooks.length) return;
    var leiste = el("div", "position:sticky;top:58px;z-index:1;background:#F4F1EC;display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:8px 0 10px");
    var alle = knopf("Alle"), keine = knopf("Keine"), kop = knopf("Ausgewählte kopieren", true);
    [alle, keine].forEach(function (b) { b.style.padding = "8px 13px"; b.style.fontSize = "13px"; });
    alle.onclick = function () { hooks.forEach(function (h) { h.an = true; }); zeige(); };
    keine.onclick = function () { hooks.forEach(function (h) { h.an = false; }); zeige(); };
    var zahl = el("div", "font:13px -apple-system,sans-serif;color:" + SAND);
    function zaehle() { var n = hooks.filter(function (h) { return h.an; }).length; zahl.textContent = n + " von " + hooks.length + " ausgewählt"; }
    kop.onclick = function () {
      var w = hooks.filter(function (h) { return h.an; });
      if (!w.length) return;
      kopiere(art === "nische" ? (function () { var k = 0; return w.map(function (h) { return h.titel ? h.hook : (++k) + ". " + h.hook; }).join("\n\n"); })() : art === "feed" ? w.map(bulkText).join("\n\n") : w.map(function (h) { return h.caption ? h.hook + "\n\n" + h.caption : h.hook; }).join(w.some(function (h) { return h.caption; }) ? "\n\n———\n\n" : "\n"), kop);
    };
    leiste.appendChild(kop); leiste.appendChild(alle); leiste.appendChild(keine); leiste.appendChild(zahl); liste.appendChild(leiste);
    hooks.forEach(function (h) {
      var z = el("label", "display:flex;gap:12px;align-items:flex-start;background:#fff;border-radius:14px;padding:12px 14px;margin:0 0 8px;box-shadow:inset 0 0 0 1px #e6ddd0;cursor:pointer");
      var cb = el("input"); cb.type = "checkbox"; cb.checked = !!h.an; cb.style.cssText = "margin-top:3px;width:18px;height:18px;accent-color:" + ES + ";flex:none";
      cb.onchange = function () { h.an = cb.checked; zaehle(); };
      var t = el("div", "flex:1;min-width:0");
      if (art === "feed") {
        t.appendChild(el("div", "font:600 11px -apple-system,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:" + SAND, "Tag " + h.tag + " · " + h.thema));
        t.appendChild(el("div", "font:16px/1.4 -apple-system,sans-serif;color:" + TINTE + ";margin-top:3px;word-break:break-word", h.slide1));
      } else {
        t.appendChild(el("div", "font:600 11px -apple-system,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:" + SAND, h.format));
        t.appendChild(el("div", "font:16px/1.4 -apple-system,sans-serif;color:" + TINTE + ";margin-top:3px", h.hook));
      }
      if (h.caption) { var cap = el("details", "margin-top:8px;font:14px/1.45 -apple-system,sans-serif;color:#4a3f37"); cap.appendChild(el("summary", "cursor:pointer;color:" + SAND + ";font-weight:600", "Caption")); cap.appendChild(el("div", "white-space:pre-wrap;margin-top:6px", h.caption)); cap.onclick = function (ev) { ev.stopPropagation(); }; t.appendChild(cap); }
      z.appendChild(cb); z.appendChild(t); liste.appendChild(z);
    });
    zaehle();
  }

  function schreibe(thema, anzahl, start, los) {
    los.disabled = true; hooks = []; zeige();
    var pakete = [], rest = anzahl, s = start, k = 0;
    var gr = art === "nische" ? 25 : mitCaption ? 10 : 20; if (art === "nische") anzahl = Math.min(anzahl, 25);
    while (rest > 0) { var n = Math.min(gr, rest); pakete.push({ start: s, anzahl: n, winkel: WINKEL[k % WINKEL.length], nr: k * 10 + 1 }); s += n; rest -= n; k++; }
    var fertig = 0, fehler = [], teile = [];
    status.textContent = "Schreibe " + anzahl + " Hooks" + (mitCaption ? " mit Caption" : "") + " … (etwa 20–30 Sekunden)";
    pakete.forEach(function (p, i) {
      fetch("/.netlify/functions/hooks", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ art: art, thema: thema, start: p.start, anzahl: p.anzahl, winkel: anzahl > gr ? p.winkel : "", nr: p.nr, caption: mitCaption, stil: stil }) })
        .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw new Error(d && d.error || "Fehlgeschlagen"); return d; }); })
        .then(function (d) { teile[i] = d.hooks || []; })
        .catch(function (e) { fehler.push(e.message || String(e)); teile[i] = []; })
        .then(function () {
          fertig++;
          status.textContent = "Schreibe " + anzahl + " Hooks … " + fertig + " von " + pakete.length + " Paketen fertig";
          if (fertig < pakete.length) return;
          var gesehen = {};
          hooks = [].concat.apply([], teile).filter(function (h) {
            var key = String(art === "feed" ? h.slide1 : h.hook).toLowerCase().replace(/[^a-zäöüß0-9]/g, "");
            if (gesehen[key]) return false; gesehen[key] = 1; return true;
          }).map(function (h) { h.an = true; return h; });
          los.disabled = false;
          status.textContent = hooks.length ? (art === "nische" && hooks[0] && hooks[0].titel ? "Fertig: Hook über die Hooks + " + (hooks.length - 1) + " Hooks." : hooks.length + " Hooks fertig.") + (fehler.length ? " (" + fehler.length + " Paket(e) fehlgeschlagen: " + fehler[0] + ")" : "") + (art === "feed" ? " Kopieren und im Bulk Import mit „Anhängen“ einfügen." : "") : "Fehler: " + (fehler[0] || "keine Hooks erhalten");
          zeige();
        });
    });
  }

  function baue() {
    panel = el("div", "position:fixed;inset:0;z-index:2147483004;background:#F4F1EC;overflow:auto;display:none;-webkit-overflow-scrolling:touch");
    var kopf = el("div", "position:sticky;top:0;z-index:2;background:" + ES + ";color:#fff;display:flex;align-items:center;justify-content:space-between;padding:14px 18px;box-sizing:border-box;height:58px");
    kopf.appendChild(el("div", "font:400 26px/1 'Instrument Serif',serif", "Hook-Generator"));
    var zu = el("button", "border:0;background:none;color:#fff;font:600 22px/1 sans-serif;cursor:pointer;padding:6px 10px", "✕"); zu.type = "button";
    zu.onclick = function () { panel.style.display = "none"; };
    kopf.appendChild(zu); panel.appendChild(kopf);
    var inhalt = el("div", "max-width:760px;margin:0 auto;padding:18px 16px 60px");
    var artZeile = el("div", "display:flex;gap:8px;margin-bottom:12px");
    var feedB = knopf("Feed-Posts"), reelB = knopf("Reels"), nischeB = knopf("Für Coach-Nische");
    var startZeile = el("div", "display:flex;gap:8px;align-items:center;font:14px -apple-system,sans-serif;color:" + SAND);
    function setzeArt(a) {
      art = a; [[feedB, "feed"], [reelB, "reels"], [nischeB, "nische"]].forEach(function (x) { var an = x[1] === a; x[0].style.background = an ? ES : "#fff"; x[0].style.color = an ? "#fff" : ES; });
      startZeile.style.display = a === "feed" ? "flex" : "none"; hooks = []; zeige(); status.textContent = "";
      /* Für Coach-Nische (Carina 24.10.): Thema = Nische, 5 Hooks + Hook über die Hooks, ohne Stil, Caption und Tage. */
      var n = a === "nische"; stilZeile.style.display = n ? "none" : "flex"; capL.style.display = n ? "none" : "flex";
      thema.placeholder = n ? "Nische, z. B. Ernährungscoach, Mindset-Coach, Paar-Coach" : "Optional: Thema, z. B. „Warum Coaches ihr Angebot verstecken“. Leer = quer durch deine Themen.";
      anz.value = n ? "5" : (anz.value === "5" ? "20" : anz.value);
    }
    feedB.onclick = function () { setzeArt("feed"); }; reelB.onclick = function () { setzeArt("reels"); }; nischeB.onclick = function () { setzeArt("nische"); };
    artZeile.style.flexWrap = "wrap"; artZeile.appendChild(feedB); artZeile.appendChild(reelB); artZeile.appendChild(nischeB);
    /* Stil (Carina 24.10.: „Hooks mehr wie eve“): Klartext = ruhige Pointen, Neugier = offene Schleifen, Fragen, Nummern. */
    var stilZeile = el("div", "display:flex;gap:8px;align-items:center;margin:-4px 0 12px;font:13px -apple-system,sans-serif;color:" + SAND);
    var klarB = knopf("Klartext"), neuB = knopf("Neugier");
    [klarB, neuB].forEach(function (b) { b.style.padding = "8px 13px"; b.style.fontSize = "13px"; });
    var stilInfo = el("span", "");
    function setzeStil(x) { stil = x; [[klarB, "klartext"], [neuB, "neugier"]].forEach(function (y) { var an = y[1] === x; y[0].style.background = an ? SAND : "#fff"; y[0].style.color = an ? "#fff" : SAND; }); stilInfo.textContent = x === "neugier" ? "offene Schleifen, Fragen, Nummern" : "ruhige Pointen, Haltung"; }
    klarB.onclick = function () { setzeStil("klartext"); }; neuB.onclick = function () { setzeStil("neugier"); };
    stilZeile.appendChild(el("span", "", "Stil:")); stilZeile.appendChild(klarB); stilZeile.appendChild(neuB); stilZeile.appendChild(stilInfo); setzeStil("klartext");
    var thema = el("textarea", "width:100%;box-sizing:border-box;border:1px solid #e6ddd0;border-radius:12px;padding:10px;font:16px/1.4 -apple-system,sans-serif;background:#fff");
    thema.rows = 2; thema.placeholder = "Optional: Thema, z. B. „Warum Coaches ihr Angebot verstecken“. Leer = quer durch deine Themen.";
    var zeile = el("div", "display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0");
    var anz = el("select", "border:1px solid #e6ddd0;border-radius:999px;padding:10px 14px;font:600 14px -apple-system,sans-serif;background:#fff");
    [5, 10, 20, 30, 50, 100].forEach(function (n) { var o = el("option", "", n + " Hooks"); o.value = n; n === 20 && (o.selected = true); anz.appendChild(o); });
    var start = el("input", "width:76px;border:1px solid #e6ddd0;border-radius:999px;padding:10px 12px;font:600 14px -apple-system,sans-serif;background:#fff"); start.type = "number"; start.min = "1"; start.value = "1";
    startZeile.appendChild(el("span", "", "ab Tag")); startZeile.appendChild(start);
    letzterTag().then(function (t) { start.value = String(t + 1); });
    var capL = el("label", "display:flex;gap:6px;align-items:center;font:600 14px -apple-system,sans-serif;color:" + ES + ";cursor:pointer");
    var capC = el("input"); capC.type = "checkbox"; capC.checked = true; capC.style.cssText = "width:18px;height:18px;accent-color:" + ES;
    capC.onchange = function () { mitCaption = capC.checked; };
    capL.appendChild(capC); capL.appendChild(document.createTextNode("mit Caption"));
    var los = knopf("Hooks schreiben", true);
    los.onclick = function () { if (art === "nische" && !thema.value.trim()) { status.textContent = "Bitte zuerst eine Nische eintragen, z. B. Ernährungscoach."; thema.focus(); return; } schreibe(thema.value.trim(), Number(anz.value) || 20, Math.max(1, parseInt(start.value, 10) || 1), los); };
    zeile.appendChild(anz); zeile.appendChild(startZeile); zeile.appendChild(capL); zeile.appendChild(los);
    status = el("div", "font:14px/1.4 -apple-system,sans-serif;color:#5b4f45;min-height:20px;margin:0 0 6px");
    liste = el("div");
    inhalt.appendChild(el("div", "font:15px/1.45 -apple-system,sans-serif;color:#4a3f37;margin-bottom:12px", "Hooks in deiner Stimme für die Coachin, die postet und nicht verkauft. Feed-Hooks kommen im Bulk-Format und passen zum Rhythmus (Quotes, Kuli-Notizen, Zeichen A–D)."));
    inhalt.appendChild(artZeile); inhalt.appendChild(stilZeile); inhalt.appendChild(thema); inhalt.appendChild(zeile); inhalt.appendChild(status); inhalt.appendChild(liste);
    panel.appendChild(inhalt); document.body.appendChild(panel);
    setzeArt("feed");
  }
  function oeffne() { if (!panel) baue(); panel.style.display = "block"; }
  window.BS_HOOKS = { oeffne: oeffne };
})();
