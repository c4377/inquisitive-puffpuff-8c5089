/* Instagram-Ansicht.
 *
 * Ein kleiner Augen-Knopf links unten (über dem Look-Schalter). Er blendet alles
 * aus, was die App über das Raster legt – „Tag 12“, Folienzahl, ⋮-Knöpfe,
 * Look-Schalter, Schwarz-Regler und „?“ – und zieht das Raster bis an den Rand,
 * damit es aussieht wie das Profil auf Instagram. Nochmal tippen holt alles zurück.
 * Der Zustand bleibt im Browser gespeichert (BS_INSTA).
 */
(function () {
  var KEY = "BS_INSTA";
  function an() {
    try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; }
  }
  function setze(v) {
    try { v ? localStorage.setItem(KEY, "1") : localStorage.removeItem(KEY); } catch (e) {}
    document.body.classList.toggle("bs-insta", v);
    knopf && (knopf.textContent = v ? "App-Ansicht" : "Instagram-Ansicht");
  }
  var knopf = null;
  function bau() {
    if (document.getElementById("bs-insta-knopf")) return;
    var css = document.createElement("style");
    css.textContent =
      '#bs-insta-knopf{position:fixed;left:10px;bottom:106px;z-index:2147483001;border:0;border-radius:999px;' +
      'padding:9px 12px;cursor:pointer;background:rgba(20,16,14,.82);color:rgba(255,255,255,.9);' +
      'font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.25)}' +
      'body.bs-insta #bs-insta-knopf{opacity:.35;bottom:14px}' +
      'body.bs-insta [id^="tag-"]>div.absolute:not(.inset-0),' +
      'body.bs-insta [id^="tag-"]>button[aria-label="Aktionen"],' +
      'body.bs-insta #bs-look,body.bs-insta #bs-schwarz,' +
      'body.bs-insta button.fixed.bottom-4.right-4{display:none!important}' +
      'body.bs-insta main .max-w-4xl{padding-left:0!important;padding-right:0!important;max-width:none!important}' +
      'body.bs-insta [id^="tag-"]{background:#fff!important}' +
      'body.bs-insta [id^="tag-"] .bs-canvas-fit{box-shadow:none!important}';
    document.head.appendChild(css);
    knopf = document.createElement("button");
    knopf.id = "bs-insta-knopf";
    knopf.type = "button";
    knopf.addEventListener("click", function () { setze(!document.body.classList.contains("bs-insta")); });
    document.body.appendChild(knopf);
    setze(an());
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bau);
  else bau();
})();
