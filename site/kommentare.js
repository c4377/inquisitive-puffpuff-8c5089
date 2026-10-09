/*
 * BrandStudio — 2 Kommentare + Instagram-Alternativtext zum Kopieren bei jedem Post.
 *
 * Das Bundle setzt unter jede Caption (Post-Editor → „Caption“ und Feed → Caption
 * aufklappen) einen Platzhalter <div data-bs-komm data-cap data-titel data-slides>.
 * Dieses Skript füllt ihn: zwei Kommentare in Carinas Stimme (Netlify-Funktion
 * „kommentare“) und je Slide ein Alternativtext für Instagram, alles mit
 * Kopieren-Knopf, plus „Neu schreiben“.
 * Gespeichert wird pro Post im Browser (localStorage), damit sie nicht jedes Mal neu
 * geschrieben werden.
 */
(function () {
  var OX = "#5E1A21";
  var laufend = {}, fehler = {};

  function hash(t) { var h = 0; t = String(t || ""); for (var i = 0; i < t.length; i++) h = (h * 31 + t.charCodeAt(i)) | 0; return (h >>> 0).toString(36); }
  function schluessel(el) {
    var tag = el.getAttribute("data-bs-komm") || "";
    var titel = el.getAttribute("data-titel") || "";
    var erste = ""; try { erste = String((JSON.parse(el.getAttribute("data-slides") || "[]")[0]) || ""); } catch (e) {}
    var basis = titel + "|" + (erste || String(el.getAttribute("data-cap") || "")).slice(0, 80);
    return "BS_KOMM:" + tag + ":" + hash(basis);
  }
  function lies(k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } }
  function merke(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  function kopiere(text, b) {
    var fertig = function () { var a = b.textContent; b.textContent = "Kopiert ✓"; setTimeout(function () { b.textContent = a; }, 1400); };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(fertig, function () { altKopie(text); fertig(); }); return; }
    } catch (e) {}
    altKopie(text); fertig();
  }
  function altKopie(text) {
    var ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:0;left:0;opacity:0"; document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); } catch (e) {} ta.remove();
  }
  function knopf(text) {
    var b = document.createElement("button"); b.type = "button"; b.textContent = text;
    b.style.cssText = "border:0;border-radius:999px;padding:6px 11px;font:600 11px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;cursor:pointer;background:" + OX + ";color:#fff;flex:none";
    return b;
  }

  // Zwei Teile im selben Platzhalter: Kommentare und Instagram-Alternativtext je Slide.
  var TEILE = [
    { id: "komm", titel: "2 Kommentare zum Kopieren", warte: "Schreibe 2 Kommentare …", art: "",
      feld: "kommentare", liste: function (d) { return d.map(function (km) { return { art: km.art, text: km.text }; }); } },
    { id: "alt", titel: "Alternativtext für Instagram", warte: "Schreibe Alternativtexte …", art: "alt",
      hinweis: "Beim Posten in Instagram unter „Erweiterte Einstellungen“ bzw. „Barrierefreiheit“ → „Alternativtext“ eintragen, für jede Slide einzeln.",
      feld: "alttexte", liste: function (d) { return d.map(function (t, i) { return { art: "Slide " + (i + 1) + " · " + t.length + " Zeichen", text: t }; }); } }
  ];
  function tk(el, teil) { return schluessel(el) + (teil.id === "komm" ? "" : ":" + teil.id); }

  function zeige(el) {
    el.innerHTML = "";
    el.style.cssText = "margin-top:10px;font:12px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#3b2a27";
    TEILE.forEach(function (teil) { el.appendChild(abschnitt(el, teil)); });
  }
  function abschnitt(el, teil) {
    var k = tk(el, teil), daten = lies(k);
    var w = document.createElement("div"); w.style.cssText = "padding-top:10px;margin-bottom:6px;border-top:1px solid #eee";
    var kopf = document.createElement("div"); kopf.style.cssText = "display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:6px";
    var titel = document.createElement("div"); titel.textContent = teil.titel;
    titel.style.cssText = "font:700 10px/1 -apple-system,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:" + OX;
    var neu = document.createElement("button"); neu.type = "button"; neu.textContent = "↻ Neu schreiben";
    neu.style.cssText = "border:0;background:none;padding:2px 0;font:600 11px -apple-system,sans-serif;color:" + OX + ";cursor:pointer";
    neu.onclick = function (e) { e.stopPropagation(); schreibe(el, teil, true); };
    kopf.appendChild(titel); kopf.appendChild(neu); w.appendChild(kopf);
    if (teil.hinweis) { var h = document.createElement("div"); h.textContent = teil.hinweis; h.style.cssText = "font-size:11px;color:#7a6a66;margin:-2px 0 6px"; w.appendChild(h); }
    if (laufend[k]) { var l = document.createElement("div"); l.textContent = teil.warte; l.style.color = "#7a6a66"; w.appendChild(l); return w; }
    if (fehler[k]) { var f = document.createElement("div"); f.textContent = fehler[k]; f.style.color = "#a33"; w.appendChild(f); return w; }
    if (!daten || !daten.k) return w;
    daten.k.forEach(function (km) {
      var box = document.createElement("div");
      box.style.cssText = "display:flex;gap:8px;align-items:flex-start;background:#F6F2EE;border-radius:10px;padding:8px 10px;margin-bottom:6px";
      var txt = document.createElement("div"); txt.style.cssText = "flex:1;min-width:0;white-space:pre-wrap";
      var art = document.createElement("div"); art.textContent = km.art; art.style.cssText = "font:700 9px/1 -apple-system,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#9a7f78;margin-bottom:4px";
      var t = document.createElement("div"); t.textContent = km.text;
      txt.appendChild(art); txt.appendChild(t);
      var b = knopf("Kopieren"); b.onclick = function (e) { e.stopPropagation(); kopiere(km.text, b); };
      box.appendChild(txt); box.appendChild(b); w.appendChild(box);
    });
    return w;
  }

  function schreibe(el, teil, erzwingen) {
    var k = tk(el, teil);
    if (laufend[k]) return;
    var cap = el.getAttribute("data-cap") || "", slides = [];
    try { slides = JSON.parse(el.getAttribute("data-slides") || "[]"); } catch (e) {}
    if (!cap.trim() && !slides.length) { fehler[k] = "Erst Caption oder Slides schreiben, dann kommt das hier automatisch."; alleZeigen(el); return; }
    if (!erzwingen && lies(k) && lies(k).k) return;
    laufend[k] = true; delete fehler[k]; alleZeigen(el);
    fetch("/.netlify/functions/kommentare", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ art: teil.art, caption: cap, titel: el.getAttribute("data-titel") || "", slides: slides }) })
      .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw new Error(d && d.error || "Fehlgeschlagen"); return d; }); })
      .then(function (d) { merke(k, { k: teil.liste(d[teil.feld] || []), capText: cap.slice(0, 3000) }); })
      .catch(function (e) { fehler[k] = "Gerade nicht möglich: " + (e.message || e) + " — „Neu schreiben“ tippen."; })
      .then(function () { delete laufend[k]; alleZeigen(el); });
  }
  function alleZeigen(quelle) {
    var k = schluessel(quelle);
    document.querySelectorAll("[data-bs-komm]").forEach(function (el) { if (schluessel(el) === k) zeige(el); });
  }

  // „Deutlich geändert“: viele Wörter anders oder >40 Zeichen Längenunterschied.
  function deutlich(alt, neu) {
    alt = String(alt || "").trim(); neu = String(neu || "").trim();
    if (alt === neu) return false;
    if (Math.abs(alt.length - neu.length) > 40) return true;
    var wa = alt.toLowerCase().split(/\W+/).filter(Boolean), wb = neu.toLowerCase().split(/\W+/).filter(Boolean);
    var a = {}, gleich = 0, alle = {};
    wa.forEach(function (w) { a[w] = 1; alle[w] = 1; });
    wb.forEach(function (w) { if (a[w] && !alle["#" + w]) { gleich++; alle["#" + w] = 1; } alle[w] = 1; });
    var n = Object.keys(alle).filter(function (x) { return x[0] !== "#"; }).length;
    return n > 0 && gleich / n < 0.8;
  }
  function captionGeaendert(el) {
    var cap = el.getAttribute("data-cap") || "";
    var veraltet = TEILE.filter(function (teil) { var d = lies(tk(el, teil)); return d && d.k && deutlich(d.capText || "", cap); });
    clearTimeout(el.__bsT);
    if (!veraltet.length) return;
    // erst schreiben, wenn sie 3 Sekunden nicht mehr tippt
    el.__bsT = setTimeout(function () {
      if (!document.body.contains(el)) return;
      var jetzt = el.getAttribute("data-cap") || "";
      veraltet.forEach(function (teil) { var d = lies(tk(el, teil)); if (d && d.k && deutlich(d.capText || "", jetzt)) schreibe(el, teil, true); });
    }, 3000);
  }
  function pruefe() {
    document.querySelectorAll("[data-bs-komm]").forEach(function (el) {
      var k = schluessel(el);
      var leer = !String(el.getAttribute("data-cap") || "").trim() && (el.getAttribute("data-slides") || "[]") === "[]";
      if (el.__bsK === k && !(el.__bsLeer && !leer)) { if (!leer) captionGeaendert(el); return; }
      el.__bsK = k; el.__bsLeer = leer;
      TEILE.forEach(function (teil) {
        var kt = tk(el, teil);
        if (leer) fehler[kt] = "Erst Caption oder Slides schreiben, dann kommt das hier automatisch.";
        else if (/^Erst Caption/.test(fehler[kt] || "")) delete fehler[kt];
      });
      zeige(el);
      if (leer) return;
      TEILE.forEach(function (teil) { var d = lies(tk(el, teil)); if ((!d || !d.k) && !fehler[tk(el, teil)]) schreibe(el, teil, false); });
    });
  }
  function start() {
    pruefe();
    new MutationObserver(function () { clearTimeout(start.t); start.t = setTimeout(pruefe, 120); })
      .observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["data-titel", "data-bs-komm", "data-cap", "data-slides"] });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
