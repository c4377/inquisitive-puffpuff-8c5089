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
  /* Der Grundwert steht im Block des Zeichners (schwarzGrund) und wird
   * von dort als window.BS_GRUND hinterlegt. Hier steht er bewusst
   * nicht noch einmal — sonst gaebe es zwei Wahrheiten. */
  function grund() {
    var v = parseFloat(typeof window !== "undefined" ? window.BS_GRUND : NaN);
    return isFinite(v) && v >= 0 ? v : 1;
  }

  function schwarzJetzt() {
    try {
      var v = parseFloat(localStorage.getItem("BS_SCHWARZ"));
      return isFinite(v) && v >= 0 ? v : grund();
    } catch (e) { return grund(); }
  }

  /* Die Ausnahmen je Tag. Ein flaches Objekt {"47": 0.5}, das die
   * index.html vor dem Modul als window.BS_SCHWARZ_TAG weiterreicht;
   * der Zeichner sucht darin seine eigene Tagesnummer (_tag) und
   * nimmt sonst den allgemeinen Wert. */
  function tageJetzt() {
    try { return JSON.parse(localStorage.getItem("BS_SCHWARZ_TAG") || "{}") || {}; }
    catch (e) { return {}; }
  }

  /* Welche Kachel gerade gewaehlt ist, ueberlebt das Neuladen —
   * sonst muesste man nach jeder Reglerbewegung wieder antippen. */
  var gewaehlt = (function () {
    try { var v = parseInt(localStorage.getItem("BS_SCHWARZ_WAHL"), 10);
          return isFinite(v) ? v : null; } catch (e) { return null; }
  })();

  function standJetzt() {
    if (gewaehlt == null) return schwarzJetzt();
    var m = tageJetzt(), v = parseFloat(m[String(gewaehlt)]);
    return isFinite(v) && v >= 0 ? v : schwarzJetzt();
  }

  function schwarzSetzen(v) {
    try {
      if (gewaehlt == null) {
        if (Math.abs(v - grund()) < 0.001) localStorage.removeItem("BS_SCHWARZ");
        else localStorage.setItem("BS_SCHWARZ", String(v));
      } else {
        var m = tageJetzt();
        if (Math.abs(v - schwarzJetzt()) < 0.001) delete m[String(gewaehlt)];
        else m[String(gewaehlt)] = v;
        if (Object.keys(m).length) localStorage.setItem("BS_SCHWARZ_TAG", JSON.stringify(m));
        else localStorage.removeItem("BS_SCHWARZ_TAG");
      }
    } catch (e) {}
    location.reload();
  }

  /* Welche Kachel wurde angetippt? Die Nummer steht als "Tag 47" im
   * Schildchen der Kachel. Von der angetippten Stelle nach oben
   * gehen und im ersten Vorfahren, der so ein Schildchen enthaelt,
   * die Nummer lesen — das ist die Kachel. Findet sich keine, bleibt
   * die Auswahl, wie sie war. */
  function tagAus(el) {
    for (var n = 0; el && n < 8; el = el.parentElement, n++) {
      if (!el.querySelectorAll) continue;
      var k = el.querySelectorAll("*");
      for (var i = 0; i < k.length && i < 80; i++) {
        var m = /^\s*Tag\s+(\d+)\s*$/.exec(k[i].textContent || "");
        if (m) return parseInt(m[1], 10);
      }
    }
    return null;
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
      '#bs-schwarz input{width:96px;accent-color:#E8836B;margin:0}' +
      '#bs-schwarz button{border:0;cursor:pointer;border-radius:999px;padding:4px 9px;' +
      'color:rgba(255,255,255,.72);background:rgba(255,255,255,.12);font:inherit}' +
      '#bs-schwarz button[data-an="ja"]{background:#E8836B;color:#241C16}' +
      '#bs-schwarz span{min-width:34px;text-align:right;font-variant-numeric:tabular-nums}' +
      '#bs-profilbilder{position:fixed;right:14px;bottom:100px;z-index:2147483000;' +
      'padding:7px 13px;border-radius:999px;text-decoration:none;' +
      'background:rgba(20,18,16,.72);backdrop-filter:blur(6px);' +
      'box-shadow:0 2px 12px rgba(0,0,0,.28);opacity:.55;transition:opacity .15s;' +
      'color:rgba(255,255,255,.72);font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '#bs-profilbilder:hover{opacity:1}' +
      '@media print{#bs-profilbilder{display:none}}';
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
    /* Der Weg zu den Profilbildern. Auch der haengt hier und nicht im
     * Menue der App: dort kaeme man nur mit einem Eingriff in React
     * hinein, und das Schildchen ist ohnehin auf jeder Seite da. */
    var mehr = document.createElement("a");
    mehr.id = "bs-profilbilder";
    mehr.href = "/profilbilder/";
    mehr.textContent = "Profilbilder";
    document.body.appendChild(mehr);

    document.body.appendChild(box);

    var reg = document.createElement("div");
    reg.id = "bs-schwarz";
    var titel = document.createElement("label");
    titel.textContent = "Schwarz";
    titel.setAttribute("for", "bs-schwarz-regler");
    var fuer = document.createElement("button");
    fuer.type = "button";
    fuer.id = "bs-schwarz-fuer";
    fuer.textContent = "alle";
    fuer.title = "Kachel antippen, dann gilt der Regler nur fuer die. Hier klicken zurueck auf alle.";
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
    fuer.addEventListener("click", function () { waehlen(null); });
    reg.appendChild(titel);
    reg.appendChild(fuer);
    reg.appendChild(eingabe);
    reg.appendChild(wert);
    document.body.appendChild(reg);

    function waehlen(tag) {
      gewaehlt = tag;
      try {
        if (tag == null) localStorage.removeItem("BS_SCHWARZ_WAHL");
        else localStorage.setItem("BS_SCHWARZ_WAHL", String(tag));
      } catch (e) {}
      fuer.textContent = tag == null ? "alle" : "Tag " + tag;
      fuer.setAttribute("data-an", tag == null ? "nein" : "ja");
      var v = Math.round(standJetzt() * 100);
      eingabe.value = String(v);
      wert.textContent = v + "%";
    }
    waehlen(gewaehlt);

    /* Nur zuhoeren, nichts abfangen: capture, damit es auch ankommt,
     * wenn die App den Klick selbst verarbeitet, und ohne
     * preventDefault, damit die Kachel trotzdem aufgeht. */
    document.addEventListener("click", function (ev) {
      if (reg.contains(ev.target) || box.contains(ev.target)) return;
      var tag = tagAus(ev.target);
      if (tag != null) waehlen(tag);
    }, true);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bauen);
  } else {
    bauen();
  }
})();
