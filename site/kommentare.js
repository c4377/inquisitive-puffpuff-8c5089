/*
 * BrandStudio — 2 Kommentare zum Kopieren bei jedem Post.
 *
 * Das Bundle setzt unter jede Caption (Post-Editor → „Caption“ und Feed → Caption
 * aufklappen) einen Platzhalter <div data-bs-komm data-cap data-titel data-slides>.
 * Dieses Skript füllt ihn: zwei Kommentare in Carinas Stimme (Netlify-Funktion
 * „kommentare“), je mit Kopieren-Knopf, plus „Neu schreiben“.
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

  function zeige(el) {
    var k = schluessel(el), daten = lies(k);
    el.innerHTML = "";
    el.style.cssText = "margin-top:10px;padding-top:10px;border-top:1px solid #eee;font:12px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#3b2a27";
    var kopf = document.createElement("div"); kopf.style.cssText = "display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:6px";
    var titel = document.createElement("div"); titel.textContent = "2 Kommentare zum Kopieren";
    titel.style.cssText = "font:700 10px/1 -apple-system,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:" + OX;
    var neu = document.createElement("button"); neu.type = "button"; neu.textContent = "↻ Neu schreiben";
    neu.style.cssText = "border:0;background:none;padding:2px 0;font:600 11px -apple-system,sans-serif;color:" + OX + ";cursor:pointer";
    neu.onclick = function (e) { e.stopPropagation(); schreibe(el, true); };
    kopf.appendChild(titel); kopf.appendChild(neu); el.appendChild(kopf);

    if (laufend[k]) { var w = document.createElement("div"); w.textContent = "Schreibe 2 Kommentare …"; w.style.color = "#7a6a66"; el.appendChild(w); return; }
    if (fehler[k]) { var f = document.createElement("div"); f.textContent = fehler[k]; f.style.color = "#a33"; el.appendChild(f); return; }
    if (!daten || !daten.k) return;
    daten.k.forEach(function (km) {
      var box = document.createElement("div");
      box.style.cssText = "display:flex;gap:8px;align-items:flex-start;background:#F6F2EE;border-radius:10px;padding:8px 10px;margin-bottom:6px";
      var txt = document.createElement("div"); txt.style.cssText = "flex:1;min-width:0;white-space:pre-wrap";
      var art = document.createElement("div"); art.textContent = km.art; art.style.cssText = "font:700 9px/1 -apple-system,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#9a7f78;margin-bottom:4px";
      var t = document.createElement("div"); t.textContent = km.text;
      txt.appendChild(art); txt.appendChild(t);
      var b = knopf("Kopieren"); b.onclick = function (e) { e.stopPropagation(); kopiere(km.text, b); };
      box.appendChild(txt); box.appendChild(b); el.appendChild(box);
    });
  }

  function schreibe(el, erzwingen) {
    var k = schluessel(el);
    if (laufend[k]) return;
    var cap = el.getAttribute("data-cap") || "", slides = [];
    try { slides = JSON.parse(el.getAttribute("data-slides") || "[]"); } catch (e) {}
    if (!cap.trim() && !slides.length) { fehler[k] = "Erst Caption oder Slides schreiben, dann kommen hier 2 Kommentare."; alleZeigen(k); return; }
    if (!erzwingen && lies(k) && lies(k).k) return;
    laufend[k] = true; delete fehler[k]; alleZeigen(k);
    fetch("/.netlify/functions/kommentare", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ caption: cap, titel: el.getAttribute("data-titel") || "", slides: slides }) })
      .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw new Error(d && d.error || "Fehlgeschlagen"); return d; }); })
      .then(function (d) { merke(k, { k: d.kommentare, cap: hash(cap) }); })
      .catch(function (e) { fehler[k] = "Kommentare gerade nicht möglich: " + (e.message || e) + " — „Neu schreiben“ tippen."; })
      .then(function () { delete laufend[k]; alleZeigen(k); });
  }
  function alleZeigen(k) {
    document.querySelectorAll("[data-bs-komm]").forEach(function (el) { if (schluessel(el) === k) zeige(el); });
  }

  function pruefe() {
    document.querySelectorAll("[data-bs-komm]").forEach(function (el) {
      var k = schluessel(el);
      var leer = !String(el.getAttribute("data-cap") || "").trim() && (el.getAttribute("data-slides") || "[]") === "[]";
      if (el.__bsK === k && !(el.__bsLeer && !leer)) return;
      el.__bsK = k; el.__bsLeer = leer;
      if (leer) { fehler[k] = "Erst Caption oder Slides schreiben, dann kommen hier 2 Kommentare."; zeige(el); return; }
      if (/^Erst Caption/.test(fehler[k] || "")) delete fehler[k];
      zeige(el);
      var d = lies(k);
      if (!d || !d.k) { if (!fehler[k]) schreibe(el, false); }
    });
  }
  function start() {
    pruefe();
    new MutationObserver(function () { clearTimeout(start.t); start.t = setTimeout(pruefe, 120); })
      .observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["data-titel", "data-bs-komm", "data-cap", "data-slides"] });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
