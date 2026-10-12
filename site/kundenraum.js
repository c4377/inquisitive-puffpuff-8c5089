/* Kundenräume (Done-for-you): jede Kundin bekommt einen eigenen, komplett getrennten Arbeitsbereich.
 *
 * Läuft als ERSTES Skript im <head>, vor allen anderen. Ist ein Kundenraum aktiv (localStorage BS_RAUM),
 * wird
 *   - jede IndexedDB "BrandStudioDB" auf "BrandStudioDB__<raum>" umgeleitet (Plan, Fotos, Designs, Tagbilder),
 *   - jeder localStorage-Schlüssel mit "R:<raum>:" vorangestellt (Brand-Einstellungen, Look, keine
 *     Supabase-Zugangsdaten → keine Cloud-Synchronisierung mit Carinas Konto),
 *   - der Look auf die Kundin umgestellt (window.BS_RAUM_K: Name, Handle, keine Carina-Freisteller,
 *     keine Carina-Rubriken und -Handschriftsätze).
 * Carinas eigener Raum (BS_RAUM leer) bleibt genau wie bisher, ohne jede Umleitung.
 * Story-Studio und Kommentare sind in Kundenräumen aus, weil sie in Carinas Stimme schreiben.
 */
(function () {
  var L = window.localStorage, SP = Storage.prototype;
  var G0 = SP.getItem, S0 = SP.setItem, R0 = SP.removeItem;
  function rohLesen(k) { try { return G0.call(L, k); } catch (e) { return null; } }
  function rohSchreiben(k, v) { try { S0.call(L, k, v); } catch (e) {} }
  function rohLoeschen(k) { try { R0.call(L, k); } catch (e) {} }
  window.__bsRoh = { lesen: rohLesen, schreiben: rohSchreiben, loeschen: rohLoeschen };

  var raum = rohLesen("BS_RAUM") || "";
  try {
    var q = new URLSearchParams(location.search).get("raum");
    if (q !== null) { q ? rohSchreiben("BS_RAUM", q) : rohLoeschen("BS_RAUM"); raum = q || ""; }
  } catch (e) {}
  var raeume = [];
  try { raeume = JSON.parse(rohLesen("BS_RAEUME") || "[]") || []; } catch (e) { raeume = []; }
  var info = null;
  for (var i = 0; i < raeume.length; i++) if (raeume[i] && raeume[i].id === raum) info = raeume[i];
  if (raum && !info) { rohLoeschen("BS_RAUM"); raum = ""; }
  window.BS_RAUM = raum;
  window.BS_RAEUME = raeume;
  window.BS_RAUM_INFO = info;
  if (!raum) return;

  var GLOBAL = { BS_RAUM: 1, BS_RAEUME: 1 }, P = "R:" + raum + ":";
  function k2(t, k) { return t === L && !GLOBAL[k] ? P + k : k; }
  SP.getItem = function (k) { return G0.call(this, k2(this, k)); };
  SP.setItem = function (k, v) { return S0.call(this, k2(this, k), v); };
  SP.removeItem = function (k) { return R0.call(this, k2(this, k)); };

  var IO = IDBFactory.prototype.open, ID = IDBFactory.prototype.deleteDatabase;
  function db(n) { return n === "BrandStudioDB" ? "BrandStudioDB__" + raum : n; }
  IDBFactory.prototype.open = function (n, v) { return v === undefined ? IO.call(this, db(n)) : IO.call(this, db(n), v); };
  IDBFactory.prototype.deleteDatabase = function (n) { return ID.call(this, db(n)); };

  var name = String(info.name || "Kundin"), handle = String(info.handle || "");
  if (handle && handle.charAt(0) !== "@") handle = "@" + handle;
  window.BS_RAUM_K = {
    kontrastAbsender: name.toLocaleUpperCase("de-DE"),
    kontrastHandle: handle || "@" + name.toLowerCase().replace(/[^a-z0-9äöüß]+/g, ""),
    magKontrastFeed: "fotozeilen|weiss|flaeche|papier|fotoetikett|weiss|flaeche",
    magKontrastRubrik: info.rubriken || "Gut zu wissen|Klartext|Notiz",
    kontrastSkriptJede: 0,
    vnHandle: handle || "@deinbusiness",
    vnMarke: name
  };
})();

/* Der Raum-Schalter oben rechts. */
(function () {
  function bau() {
    if (document.getElementById("bs-raum")) return;
    var roh = window.__bsRoh, raum = window.BS_RAUM || "", raeume = window.BS_RAEUME || [], info = window.BS_RAUM_INFO;
    var css = document.createElement("style");
    css.textContent =
      "#bs-raum{position:fixed;top:14px;right:64px;z-index:2147483001;font:600 12px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}" +
      "#bs-raum>button{border:0;border-radius:999px;padding:8px 12px;cursor:pointer;font:inherit;box-shadow:0 2px 8px rgba(0,0,0,.18);" +
      (raum ? "background:#C2410C;color:#fff}" : "background:#F3F4F6;color:#374151}") +
      "#bs-raum .menue{display:none;position:absolute;right:0;top:40px;min-width:240px;background:#fff;border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,.22);padding:6px}" +
      "#bs-raum.offen .menue{display:block}" +
      "#bs-raum .zeile{display:flex;align-items:center;gap:6px;border-radius:9px}" +
      "#bs-raum .zeile.an{background:#F3F4F6}" +
      "#bs-raum .zeile button{border:0;background:none;font:inherit;cursor:pointer;padding:11px 10px;text-align:left;color:#111827}" +
      "#bs-raum .zeile .wahl{flex:1}" +
      "#bs-raum .zeile .x{color:#9CA3AF;padding:11px 8px}" +
      "#bs-raum .neu{width:100%;border:0;background:#7C3AED;color:#fff;font:inherit;border-radius:9px;padding:11px;margin-top:6px;cursor:pointer}" +
      "#bs-raum .hinweis{font:400 11px/1.4 -apple-system,sans-serif;color:#6B7280;padding:8px 10px 4px}";
    document.head.appendChild(css);
    var box = document.createElement("div");
    box.id = "bs-raum";
    var knopf = document.createElement("button");
    knopf.type = "button";
    knopf.textContent = raum ? "Kundin: " + (info && info.name || raum) : "Mein Raum";
    knopf.addEventListener("click", function () { box.classList.toggle("offen"); });
    var m = document.createElement("div");
    m.className = "menue";
    function wechsel(id) { id ? roh.schreiben("BS_RAUM", id) : roh.loeschen("BS_RAUM"); location.href = location.pathname; }
    function zeile(text, id, an, loeschbar) {
      var z = document.createElement("div");
      z.className = "zeile" + (an ? " an" : "");
      var b = document.createElement("button");
      b.className = "wahl"; b.textContent = text;
      b.addEventListener("click", function () { an ? box.classList.remove("offen") : wechsel(id); });
      z.appendChild(b);
      if (loeschbar) {
        var x = document.createElement("button");
        x.className = "x"; x.textContent = "✕"; x.title = "Kundenraum löschen";
        x.addEventListener("click", function () {
          if (!confirm("Kundenraum „" + text + "“ mit Plan, Fotos und Einstellungen endgültig löschen?")) return;
          try { indexedDB.deleteDatabase.call(indexedDB, "BrandStudioDB__" + id); } catch (e) {}
          var rest = []; for (var k = 0; k < localStorage.length; k++) { var s = localStorage.key(k); if (s && s.indexOf("R:" + id + ":") === 0) rest.push(s); }
          rest.forEach(function (s) { roh.loeschen(s); });
          var neu = (window.BS_RAEUME || []).filter(function (r) { return r && r.id !== id; });
          roh.schreiben("BS_RAEUME", JSON.stringify(neu));
          if (raum === id) wechsel(""); else location.reload();
        });
        z.appendChild(x);
      }
      m.appendChild(z);
    }
    zeile("Mein Raum (Carina)", "", !raum, false);
    raeume.forEach(function (r) { if (r && r.id) zeile(r.name + (r.handle ? " · " + r.handle : ""), r.id, r.id === raum, true); });
    var neu = document.createElement("button");
    neu.className = "neu"; neu.type = "button"; neu.textContent = "+ Neue Kundin";
    neu.addEventListener("click", function () {
      var name = (prompt("Name der Kundin (steht unten auf ihren Kacheln):") || "").trim();
      if (!name) return;
      var handle = (prompt("Instagram-Handle der Kundin (z. B. @studio.lena):") || "").trim();
      var id = name.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "kundin";
      var liste = window.BS_RAEUME || [], basis = id, n = 2;
      while (liste.some(function (r) { return r && r.id === id; })) id = basis + "-" + n++;
      liste.push({ id: id, name: name, handle: handle, angelegt: new Date().toISOString().slice(0, 10) });
      roh.schreiben("BS_RAEUME", JSON.stringify(liste));
      ["brandSettings", "BS_STIL", "BS_MARKE"].forEach(function (k) { var v = roh.lesen(k); v !== null && roh.schreiben("R:" + id + ":" + k, v); });
      wechsel(id);
    });
    m.appendChild(neu);
    var h = document.createElement("div");
    h.className = "hinweis";
    h.textContent = raum
      ? "Du bist im Raum der Kundin: eigener Plan, eigene Fotos, eigener Bulk Import. Deine Fotos und Freisteller sind hier nicht drin."
      : "Kundenräume sind komplett getrennt: eigener Plan, eigene Fotos, eigener Bulk Import.";
    m.appendChild(h);
    box.appendChild(knopf);
    box.appendChild(m);
    document.body.appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bau); else bau();
})();
