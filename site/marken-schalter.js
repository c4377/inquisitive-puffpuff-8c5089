/* Der Look-Schalter.
 *
 * Wie der Schwarz-Regler haengt er nicht in der React-App, sondern
 * daneben am body. Er merkt sich den gewaehlten Look (BS_MARKE) und
 * laedt neu; die index.html reicht ihn vor dem Modul als
 * window.BS_MARKE weiter, und der Zeichner legt die passenden Farben
 * und Schriften (BS_MARKEN im Bundle) ueber den normalen Look.
 *
 * Er sitzt links unten ueber dem Schwarz-Regler.
 */
(function () {
  var LOOKS = [
    ["", "Aktuell"],
    ["bordeaux", "Bordeaux"],
    ["bordeauxgloock", "Bordeaux + Waldgrün-Schrift"],
    ["creme", "Creme & Espresso"]
  ];
  function jetzt() {
    try { return localStorage.getItem("BS_MARKE") || ""; } catch (e) { return ""; }
  }
  function name(k) {
    for (var i = 0; i < LOOKS.length; i++) if (LOOKS[i][0] === k) return LOOKS[i][1];
    return "Aktuell";
  }
  function setze(k) {
    try { k ? localStorage.setItem("BS_MARKE", k) : localStorage.removeItem("BS_MARKE"); } catch (e) {}
    location.reload();
  }
  function bau() {
    if (document.getElementById("bs-look")) return;
    var css = document.createElement("style");
    css.textContent =
      '#bs-look{position:fixed;left:10px;bottom:58px;z-index:2147483000;' +
      'font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '#bs-look>button{border:0;border-radius:999px;padding:9px 12px;cursor:pointer;' +
      'background:rgba(20,16,14,.82);color:rgba(255,255,255,.9);font:inherit;' +
      'box-shadow:0 2px 10px rgba(0,0,0,.25)}' +
      '#bs-look ul{list-style:none;margin:0 0 6px;padding:6px;border-radius:14px;' +
      'background:rgba(20,16,14,.94);box-shadow:0 4px 18px rgba(0,0,0,.3);display:none}' +
      '#bs-look.offen ul{display:block}' +
      '#bs-look li{padding:10px 12px;border-radius:9px;color:rgba(255,255,255,.85);cursor:pointer;white-space:nowrap}' +
      '#bs-look li.an{background:rgba(255,255,255,.14);color:#fff}';
    document.head.appendChild(css);
    var box = document.createElement("div");
    box.id = "bs-look";
    var ul = document.createElement("ul");
    var akt = jetzt();
    LOOKS.forEach(function (l) {
      var li = document.createElement("li");
      li.textContent = l[1];
      if (l[0] === akt) li.className = "an";
      li.addEventListener("click", function () { if (l[0] !== akt) setze(l[0]); else box.classList.remove("offen"); });
      ul.appendChild(li);
    });
    var knopf = document.createElement("button");
    knopf.type = "button";
    knopf.textContent = "Look: " + name(akt);
    knopf.addEventListener("click", function () { box.classList.toggle("offen"); });
    box.appendChild(ul);
    box.appendChild(knopf);
    document.body.appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bau);
  else bau();
})();
