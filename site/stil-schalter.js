/* Der Umschalter zwischen den zwei Feeds.
 *
 * Er haengt bewusst NICHT in der React-App: die App verwaltet nur
 * #root, dieses Schildchen haengt daneben am body. Damit kann es
 * nicht kaputtgehen, wenn die App neu zeichnet, und es ist auf jeder
 * Seite da — auch auf /content-planner, wo der Pfad das "/dunkel"
 * laengst verloren hat.
 *
 * Die Pfadregel in der index.html gilt weiter: "/" schaltet auf den
 * Grundstil zurueck, "/dunkel/..." auf den zweiten. Deshalb reicht es
 * nicht, nur den gemerkten Wert zu setzen — von "/" aus muss der
 * Schalter nach "/dunkel/" gehen und umgekehrt, sonst ueberschreibt
 * die Pfadregel beim Neuladen sofort wieder, was gerade gewaehlt
 * wurde.
 */
(function () {
  function jetzt() {
    try { return localStorage.getItem("BS_STIL") === "dunkel" ? "dunkel" : "grund"; }
    catch (e) { return "grund"; }
  }

  function ziel(wahl) {
    var p = location.pathname;
    var aufDunkel = p.indexOf("/dunkel") === 0;
    var aufWurzel = p === "/" || p === "";
    if (wahl === "dunkel") return aufWurzel ? "/dunkel/" : (aufDunkel ? null : p);
    return aufDunkel ? "/" : (aufWurzel ? null : p);
  }

  function waehle(wahl) {
    if (wahl === jetzt()) return;
    try {
      if (wahl === "dunkel") localStorage.setItem("BS_STIL", "dunkel");
      else localStorage.removeItem("BS_STIL");
    } catch (e) {}
    var z = ziel(wahl);
    if (z && z !== location.pathname) location.assign(z);
    else location.reload();
  }


  /* Der Schwarz-Regler.
   *
   * Er aendert nichts an einer schon gezeichneten Kachel — die liegen
   * als Canvas fertig da. Deshalb merkt er den Wert und laedt neu; die
   * index.html reicht ihn vor dem Modul als window.BS_SCHWARZ weiter,
   * und der Zeichner multipliziert Auflage und Vignette damit.
   *
   * Erst bei "change", nicht bei "input": sonst laedt die Seite
   * waehrend des Schiebens bei jedem Pixel neu.
   */
  function schwarzJetzt() {
    try {
      var v = parseFloat(localStorage.getItem("BS_SCHWARZ"));
      return isFinite(v) && v >= 0 ? v : 1;
    } catch (e) { return 1; }
  }

  function schwarzSetzen(v) {
    try {
      if (Math.abs(v - 1) < 0.001) localStorage.removeItem("BS_SCHWARZ");
      else localStorage.setItem("BS_SCHWARZ", String(v));
    } catch (e) {}
    location.reload();
  }

  function bauen() {
    if (document.getElementById("bs-stil-schalter")) return;
    var css = document.createElement("style");
    css.textContent =
      '#bs-stil-schalter{position:fixed;right:14px;bottom:14px;z-index:2147483000;' +
      'display:flex;gap:2px;padding:3px;border-radius:999px;' +
      'background:rgba(20,18,16,.72);backdrop-filter:blur(6px);' +
      'box-shadow:0 2px 12px rgba(0,0,0,.28);opacity:.55;transition:opacity .15s;' +
      'font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '#bs-stil-schalter:hover{opacity:1}' +
      '#bs-stil-schalter button{border:0;cursor:pointer;border-radius:999px;' +
      'padding:7px 13px;color:rgba(255,255,255,.72);background:transparent;font:inherit}' +
      '#bs-stil-schalter button[data-an="ja"]{background:#E8836B;color:#241C16}' +
      '@media print{#bs-stil-schalter,#bs-schwarz{display:none}}' +
      '#bs-schwarz{position:fixed;right:14px;bottom:58px;z-index:2147483000;' +
      'display:flex;align-items:center;gap:8px;padding:6px 12px;border-radius:999px;' +
      'background:rgba(20,18,16,.72);backdrop-filter:blur(6px);' +
      'box-shadow:0 2px 12px rgba(0,0,0,.28);opacity:.55;transition:opacity .15s;' +
      'color:rgba(255,255,255,.72);font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '#bs-schwarz:hover{opacity:1}' +
      '#bs-schwarz input{width:104px;accent-color:#E8836B;margin:0}' +
      '#bs-schwarz span{min-width:34px;text-align:right;font-variant-numeric:tabular-nums}';
    document.head.appendChild(css);

    var box = document.createElement("div");
    box.id = "bs-stil-schalter";
    box.setAttribute("role", "group");
    box.setAttribute("aria-label", "Stil");
    [["grund", "Warm"], ["dunkel", "Dunkel"]].forEach(function (paar) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = paar[1];
      b.setAttribute("data-an", jetzt() === paar[0] ? "ja" : "nein");
      b.setAttribute("aria-pressed", jetzt() === paar[0] ? "true" : "false");
      b.addEventListener("click", function () { waehle(paar[0]); });
      box.appendChild(b);
    });
    document.body.appendChild(box);

    var reg = document.createElement("div");
    reg.id = "bs-schwarz";
    var titel = document.createElement("label");
    titel.textContent = "Schwarz";
    titel.setAttribute("for", "bs-schwarz-regler");
    var eingabe = document.createElement("input");
    eingabe.id = "bs-schwarz-regler";
    eingabe.type = "range";
    eingabe.min = "0";
    eingabe.max = "160";
    eingabe.step = "5";
    eingabe.value = String(Math.round(schwarzJetzt() * 100));
    var wert = document.createElement("span");
    wert.textContent = eingabe.value + "%";
    eingabe.addEventListener("input", function () { wert.textContent = eingabe.value + "%"; });
    eingabe.addEventListener("change", function () { schwarzSetzen(parseInt(eingabe.value, 10) / 100); });
    reg.appendChild(titel);
    reg.appendChild(eingabe);
    reg.appendChild(wert);
    document.body.appendChild(reg);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bauen);
  } else {
    bauen();
  }
})();
