/* Look zum Ausprobieren (Carina 21.10.: Pinterest-Vorlage „Herground“, „Ginge das mal zum ausprobieren“).
 *
 * Ein kleines Schildchen links unten über dem Schwarz-Regler: „Look: Kontrast“ oder „Look: Studio“.
 * Antippen merkt die Wahl (BS_LOOK) und lädt neu. Die index.html liest BS_LOOK vor dem Modul und setzt
 * dann window.BS_LOOK_K; der Zeichner legt das über den Look Kontrast (tools/kontrast-studio.js).
 * Gespeicherte Texte und Pläne bleiben, es ändern sich nur die Titelkacheln.
 */
(function () {
  function jetzt() { try { return localStorage.getItem("BS_LOOK") === "studio" ? "studio" : "kontrast"; } catch (e) { return "kontrast"; } }
  function bauen() {
    if (document.getElementById("bs-look")) return;
    var css = document.createElement("style");
    css.textContent =
      "@media print{#bs-look{display:none}}" +
      "#bs-look{position:fixed;left:10px;bottom:52px;z-index:2147483000;border:0;cursor:pointer;border-radius:999px;" +
      "padding:7px 12px;background:rgba(20,18,16,.72);backdrop-filter:blur(6px);box-shadow:0 2px 10px rgba(0,0,0,.28);" +
      "color:rgba(255,255,255,.85);font:600 11px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;opacity:.6}" +
      "#bs-look:hover{opacity:1}#bs-look[data-an='studio']{background:#A3321B;color:#F6EEE6;opacity:.9}";
    document.head.appendChild(css);
    var b = document.createElement("button");
    b.type = "button";
    b.id = "bs-look";
    var l = jetzt();
    b.setAttribute("data-an", l);
    b.textContent = l === "studio" ? "Look: Studio ↺" : "Look: Kontrast";
    b.title = l === "studio" ? "Zurück zum Look Kontrast" : "Look Studio ausprobieren";
    b.addEventListener("click", function () {
      try { if (l === "studio") localStorage.removeItem("BS_LOOK"); else localStorage.setItem("BS_LOOK", "studio"); } catch (e) {}
      location.reload();
    });
    document.body.appendChild(b);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bauen); else bauen();
})();
