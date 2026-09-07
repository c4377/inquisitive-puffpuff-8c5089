/* Der Schwarz-Regler.
 *
 * Er haengt bewusst NICHT in der React-App: die App verwaltet nur
 * #root, dieses Schildchen haengt daneben am body. Damit kann es
 * nicht kaputtgehen, wenn die App neu zeichnet, und es ist auf jeder
 * Seite da — auch auf /content-planner.
 *
 * Der Warm-Dunkel-Umschalter stand frueher hier daneben. Es gibt nur
 * noch einen Feed, den dunklen, also ist er weg. Die Pfadregel in der
 * index.html ist ebenfalls entfallen: dunkel gilt immer.
 *
 * Er ist zugeklappt, bis man ihn braucht. Offen ist er 300 Pixel breit
 * und lag damit staendig auf einer Kachel, auf der Blaetterleiste oder
 * auf der Speicherzeile im Editor. Zugeklappt ist er ein Griff von 42
 * Pixeln, der nur den Wert zeigt. Ob er offen oder zu ist, merkt sich
 * der Browser (BS_SCHWARZ_OFFEN) — nach dem Neuladen steht er wieder
 * so da, wie sie ihn verlassen hat.
 *
 * Er steht links unten, nicht mehr rechts: rechts unten sitzt der
 * Hilfeknopf der App (fixed bottom-4 right-4), die beiden lagen
 * uebereinander.
 */
(function () {
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
    if (document.getElementById("bs-schwarz")) return;
    var css = document.createElement("style");
    css.textContent =
      '@media print{#bs-schwarz{display:none}}' +
      '#bs-schwarz{position:fixed;left:10px;bottom:10px;z-index:2147483000;' +
      'display:flex;align-items:center;gap:8px;padding:6px 12px;border-radius:999px;' +
      'background:rgba(20,18,16,.72);backdrop-filter:blur(6px);' +
      'box-shadow:0 2px 12px rgba(0,0,0,.28);opacity:.55;transition:opacity .15s;' +
      'color:rgba(255,255,255,.72);font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '#bs-schwarz:hover{opacity:1}' +
      /* Zugeklappt: nur der Griff, alles andere ist weg — nicht bloss
         durchsichtig, sondern ohne Platzbedarf, sonst faengt die Ecke
         weiter Klicks ab, die der Kachel gehoeren. */
      '#bs-schwarz.bs-zu{gap:0;padding:0;background:none;box-shadow:none;' +
      'backdrop-filter:none;opacity:.42}' +
      '#bs-schwarz.bs-zu:hover{opacity:1}' +
      '#bs-schwarz.bs-zu>*{display:none}' +
      '#bs-schwarz.bs-zu>#bs-schwarz-griff{display:block}' +
      '#bs-schwarz-griff{border:0;cursor:pointer;border-radius:999px;' +
      'padding:6px 10px;color:rgba(255,255,255,.8);background:rgba(20,18,16,.72);' +
      'backdrop-filter:blur(6px);box-shadow:0 2px 10px rgba(0,0,0,.28);' +
      'font:600 11px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;' +
      'font-variant-numeric:tabular-nums}' +
      '#bs-schwarz input{width:96px;accent-color:#E8836B;margin:0}' +
      '#bs-schwarz button{border:0;cursor:pointer;border-radius:999px;padding:4px 9px;' +
      'color:rgba(255,255,255,.72);background:rgba(255,255,255,.12);font:inherit}' +
      '#bs-schwarz button[data-an="ja"]{background:#E8836B;color:#241C16}' +
      '#bs-schwarz span{min-width:34px;text-align:right;font-variant-numeric:tabular-nums}';
    document.head.appendChild(css);

    var reg = document.createElement("div");
    reg.id = "bs-schwarz";
    var griff = document.createElement("button");
    griff.type = "button";
    griff.id = "bs-schwarz-griff";
    griff.title = "Schwarz einstellen";
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
    reg.appendChild(griff);
    reg.appendChild(titel);
    reg.appendChild(fuer);
    reg.appendChild(eingabe);
    reg.appendChild(wert);
    document.body.appendChild(reg);

    /* Auf- und zuklappen. Der Griff zeigt zugeklappt den Wert, damit
     * man auch ohne Aufklappen sieht, worauf sie steht. */
    function offenJetzt() {
      try { return localStorage.getItem("BS_SCHWARZ_OFFEN") === "1"; }
      catch (e) { return false; }
    }
    function klappen(auf) {
      reg.classList.toggle("bs-zu", !auf);
      griff.textContent = auf ? "\u00d7" : (eingabe.value + "%");
      griff.title = auf ? "Zuklappen" : "Schwarz einstellen \u2014 steht auf " + eingabe.value + "%";
      try {
        if (auf) localStorage.setItem("BS_SCHWARZ_OFFEN", "1");
        else localStorage.removeItem("BS_SCHWARZ_OFFEN");
      } catch (e) {}
    }
    griff.addEventListener("click", function () { klappen(reg.classList.contains("bs-zu")); });

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
      if (reg.classList.contains("bs-zu")) griff.textContent = v + "%";
    }
    waehlen(gewaehlt);
    klappen(offenJetzt());

    /* Nur zuhoeren, nichts abfangen: capture, damit es auch ankommt,
     * wenn die App den Klick selbst verarbeitet, und ohne
     * preventDefault, damit die Kachel trotzdem aufgeht. */
    document.addEventListener("click", function (ev) {
      if (reg.contains(ev.target)) return;
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
