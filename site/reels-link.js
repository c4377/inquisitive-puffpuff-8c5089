/* Link zur Reel-Werkstatt (/reels/).
 * Haengt wie die Schalter nicht in der React-App, sondern daneben am body,
 * rechts unten.
 */
(function () {
  if (location.pathname.indexOf('/reels') === 0) return;
  var a = document.createElement('a');
  a.href = '/reels/';
  a.textContent = '🎬 Reel-Werkstatt';
  a.setAttribute('style', 'position:fixed;right:14px;bottom:14px;z-index:9999;padding:8px 13px;border-radius:999px;' +
    'background:#241C16;color:#F6F2EB;font:600 12.5px/1 -apple-system,BlinkMacSystemFont,sans-serif;text-decoration:none;' +
    'box-shadow:0 2px 10px rgba(0,0,0,.18);opacity:.9');
  document.body.appendChild(a);
})();
