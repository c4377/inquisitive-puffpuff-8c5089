/*
 * Heute posten (Carina 13.10.).
 *
 * Knopf „↑ Posten“ links unten öffnet die Freigabe: Tag aus dem Content-Plan wählen
 * (vorgeschlagen ist der Tag nach dem zuletzt geposteten), Folien ansehen, Caption
 * prüfen, dann „Jetzt posten“. Gepostet wird über /.netlify/functions/instagram
 * (offizielle Instagram API, Schlüssel nur auf dem Server).
 *
 * Feed-Post: Karussell aus den Tages-Folien (JPEG, gerendert vom Bundle über
 * window.__bsTagBilder), Caption aus dem Plan. Story: das Cover des Posts.
 * Reel + Story-Video: kommen fertig geschnitten aus /heute.json (schreibt der tägliche
 * Agent), mit 4 Hook-Versionen zur Auswahl.
 *
 * Die Bilder liegen öffentlich in Supabase (brand-images/ig/…), weil Instagram sie
 * sich selbst abholt. Ohne PIN (Netlify: POST_PIN) postet die Funktion nichts.
 */
(function () {
  if (window.BS_RAUM) return; /* Kundenraum: nie auf Carinas Konto posten. */
  var OX = "#5E1A21", FN = "/.netlify/functions/instagram";
  var panel = null, heute = null, bilder = [], tagObj = null;

  function lies(k) { try { return localStorage.getItem(k) || ""; } catch (e) { return ""; } }
  function merke(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function el(tag, css, text) { var e = document.createElement(tag); if (css) e.style.cssText = css; if (text != null) e.textContent = text; return e; }
  function warte(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  async function ruf(daten) {
    daten.pin = lies("BS_IG_PIN");
    var r = await fetch(FN, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(daten) });
    var d = await r.json().catch(function () { return {}; });
    if (!r.ok || d.error) throw new Error(d.error || "HTTP " + r.status);
    return d;
  }

  /* Wartet, bis Instagram die Datei verarbeitet hat (Videos brauchen bis zu ein paar Minuten). */
  async function fertig(id, log, was) {
    for (var i = 0; i < 90; i++) {
      var s = await ruf({ aktion: "status", id: id });
      if (s.status === "FINISHED") return;
      if (s.status === "ERROR" || s.status === "EXPIRED") throw new Error(was + ": Instagram meldet " + s.status + (s.detail ? " (" + s.detail + ")" : ""));
      if (i % 4 === 3) log(was + ": Instagram verarbeitet noch …");
      await warte(i < 3 ? 1500 : 5000);
    }
    throw new Error(was + ": Instagram braucht zu lange. Später nochmal versuchen.");
  }

  async function hochladen(datei, tag, nr) {
    var sb = window.__bsSupa;
    if (!sb) throw new Error("Nicht angemeldet. Erst in der App einloggen.");
    var d = new Date().toISOString().slice(0, 10);
    var pfad = "ig/" + d + "/tag" + tag + "-" + nr + "-" + Math.random().toString(36).slice(2, 8) + ".jpg";
    /* Supabase meldet bei vielen Anfragen kurz „Too many connections“: dann warten und nochmal. */
    var up = null;
    for (var v = 1; v <= 6; v++) {
      up = await sb.storage.from("brand-images").upload(pfad, datei, { contentType: "image/jpeg", cacheControl: "31536000", upsert: true });
      if (!up.error) break;
      if (v < 6) await warte(1500 * v);
    }
    if (up.error) throw new Error("Bild-Upload: " + up.error.message + " (Supabase ist gerade überlastet, in ein paar Minuten nochmal tippen)");
    return sb.storage.from("brand-images").getPublicUrl(pfad).data.publicUrl;
  }

  /* Story 1080×1920 aus dem 4:5-Cover: Instagram würde das Cover sonst auf 9:16 hochzoomen und
     links/rechts abschneiden (Carina 13.10.). Cover ganz sichtbar als Karte, Hintergrund in der Randfarbe. */
  async function storyBild(datei) {
    var img = await new Promise(function (ok, nein) { var i = new Image(); i.onload = function () { ok(i); }; i.onerror = nein; i.src = URL.createObjectURL(datei); });
    var W = 1080, H = 1920, c = document.createElement("canvas"); c.width = W; c.height = H;
    var g = c.getContext("2d");
    var p = document.createElement("canvas"); p.width = 1; p.height = 1;
    var pg = p.getContext("2d"); pg.drawImage(img, 0, 0, img.width, 4, 0, 0, 1, 1);
    var f = pg.getImageData(0, 0, 1, 1).data, hell = (f[0] * 299 + f[1] * 587 + f[2] * 114) / 1000 > 140;
    g.fillStyle = "rgb(" + Math.round(f[0] * .82) + "," + Math.round(f[1] * .82) + "," + Math.round(f[2] * .82) + ")";
    g.fillRect(0, 0, W, H);
    var bw = 940, bh = Math.round(bw * img.height / img.width), x = (W - bw) / 2, y = Math.round((H - bh) / 2) + 40;
    g.save(); g.shadowColor = "rgba(0,0,0,.35)"; g.shadowBlur = 40; g.shadowOffsetY = 12;
    g.fillStyle = "#000"; g.fillRect(x, y, bw, bh); g.restore();
    g.drawImage(img, x, y, bw, bh);
    g.fillStyle = hell ? "rgba(23,17,15,.75)" : "rgba(255,255,255,.85)";
    g.font = "600 30px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
    g.textAlign = "center";
    var t = "NEUER POST", sp = 8, breite = 0;
    for (var k = 0; k < t.length; k++) breite += g.measureText(t[k]).width + sp;
    var cx = W / 2 - breite / 2;
    g.textAlign = "left";
    for (var m = 0; m < t.length; m++) { g.fillText(t[m], cx, y - 50); cx += g.measureText(t[m]).width + sp; }
    var blob = await new Promise(function (ok) { c.toBlob(ok, "image/jpeg", .92); });
    return new File([blob], "story.jpg", { type: "image/jpeg" });
  }

  function plan() { return Array.isArray(window.__bsPlan) ? window.__bsPlan.filter(function (t) { return t && t.slides && t.slides.length; }) : []; }

  function vorschlag() {
    var p = plan(), letzter = Number(lies("BS_IG_LETZTER")) || 0;
    var n = p.filter(function (t) { return Number(t.day) > letzter; }).sort(function (a, b) { return a.day - b.day; })[0];
    return n || p[0] || null;
  }

  function oeffne() {
    if (panel) { panel.remove(); panel = null; }
    panel = el("div", "position:fixed;inset:0;z-index:2147483002;background:rgba(14,12,11,.55);display:flex;align-items:flex-end;justify-content:center;font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#17110F");
    var box = el("div", "background:#fff;width:100%;max-width:560px;max-height:92vh;overflow:auto;border-radius:18px 18px 0 0;padding:18px 16px 28px;box-sizing:border-box");
    panel.appendChild(box);
    panel.addEventListener("click", function (e) { if (e.target === panel) { panel.remove(); panel = null; } });

    var kopf = el("div", "display:flex;justify-content:space-between;align-items:center;margin-bottom:12px");
    kopf.appendChild(el("div", "font:700 11px/1 -apple-system,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:" + OX, "Heute posten"));
    var zu = el("button", "border:0;background:none;font-size:22px;cursor:pointer;color:#7a6a66", "×");
    zu.onclick = function () { panel.remove(); panel = null; };
    kopf.appendChild(zu); box.appendChild(kopf);

    /* PIN + Verbindung */
    var verb = el("div", "background:#F6F2EE;border-radius:12px;padding:10px 12px;margin-bottom:14px;font-size:13px");
    box.appendChild(verb);
    function zeigeVerbindung() {
      verb.innerHTML = "";
      if (!lies("BS_IG_PIN")) {
        verb.appendChild(el("div", "margin-bottom:6px", "PIN eingeben (der Wert von POST_PIN in Netlify):"));
        var pin = el("input", "width:100%;box-sizing:border-box;padding:8px 10px;border:1px solid #ddd;border-radius:8px;font-size:14px");
        pin.type = "password"; verb.appendChild(pin);
        var ok = knopf("Verbinden"); ok.style.marginTop = "8px"; verb.appendChild(ok);
        ok.onclick = function () { merke("BS_IG_PIN", pin.value.trim()); pruefe(); };
        return;
      }
      pruefe();
    }
    async function pruefe() {
      verb.textContent = "Verbindung zu Instagram wird geprüft …";
      try {
        var d = await ruf({ aktion: "check" });
        verb.textContent = "✓ Verbunden mit @" + d.username;
      } catch (e) {
        if (/PIN/.test(e.message)) merke("BS_IG_PIN", "");
        verb.textContent = "✗ " + e.message;
        if (!lies("BS_IG_PIN")) setTimeout(zeigeVerbindung, 1200);
      }
    }
    zeigeVerbindung();

    /* Feed-Post */
    box.appendChild(titel("Post"));
    var wahl = el("select", "width:100%;padding:9px 10px;border:1px solid #ddd;border-radius:8px;font-size:14px;margin-bottom:10px;background:#fff");
    plan().forEach(function (t) { var o = el("option", "", "Tag " + t.day + (t.title ? " · " + t.title : "")); o.value = t.day; wahl.appendChild(o); });
    var v = vorschlag(); if (v) wahl.value = v.day;
    box.appendChild(wahl);
    var reihe = el("div", "display:flex;gap:6px;overflow-x:auto;padding-bottom:6px;margin-bottom:8px;min-height:40px");
    box.appendChild(reihe);
    var cap = el("textarea", "width:100%;box-sizing:border-box;min-height:140px;padding:9px 10px;border:1px solid #ddd;border-radius:8px;font:13px/1.45 -apple-system,sans-serif;margin-bottom:8px");
    box.appendChild(cap);
    var cbPost = haken(box, "Post im Feed veröffentlichen", true);
    var cbStory = haken(box, "Cover als Story posten", true);

    async function ladeTag() {
      tagObj = plan().find(function (t) { return String(t.day) === String(wahl.value); }) || null;
      bilder = []; reihe.innerHTML = ""; cap.value = tagObj ? (tagObj.caption || "") : "";
      if (!tagObj) return;
      if (!window.__bsTagBilder) { reihe.textContent = "Bitte einmal den Content-Plan öffnen, dann hier neu laden."; return; }
      reihe.textContent = "Folien werden gezeichnet …";
      try {
        var fs = await window.__bsTagBilder(tagObj);
        reihe.innerHTML = "";
        fs.forEach(function (f) { var i = el("img", "height:120px;border-radius:6px;flex:none"); i.src = URL.createObjectURL(f); reihe.appendChild(i); });
        bilder = fs;
        /* Vorschau der Story (9:16), genau so, wie sie gepostet wird */
        if (fs[0]) {
          var sb = await storyBild(fs[0]);
          var w = el("div", "flex:none;text-align:center;font:600 10px/1 -apple-system,sans-serif;letter-spacing:.08em;color:#9a7f78");
          var si = el("img", "height:120px;border-radius:6px;display:block;margin-bottom:4px;outline:2px solid " + OX);
          si.src = URL.createObjectURL(sb); si.style.cursor = "zoom-in";
          si.onclick = function () { var gross = el("div", "position:fixed;inset:0;z-index:2147483003;background:rgba(0,0,0,.85);display:flex;align-items:center;justify-content:center"); var gi = el("img", "max-height:92vh;max-width:92vw;border-radius:10px"); gi.src = si.src; gross.appendChild(gi); gross.onclick = function () { gross.remove(); }; document.body.appendChild(gross); };
          w.appendChild(si); w.appendChild(document.createTextNode("STORY"));
          reihe.insertBefore(w, reihe.firstChild);
        }
      } catch (e) { reihe.textContent = "Folien gingen nicht: " + e.message; }
    }
    wahl.onchange = ladeTag; ladeTag();

    /* Reel + Story-Video aus /heute.json */
    var reelBox = el("div", ""); box.appendChild(reelBox);
    var reelWahl = null, reelCap = null, cbReel = null, cbReelStory = null, cbStoryVid = null;
    fetch("/heute.json?t=" + Date.now()).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (h) {
      heute = h;
      reelBox.appendChild(titel("Reel"));
      if (!h || !h.reels || !h.reels.length) { reelBox.appendChild(el("div", "font-size:13px;color:#7a6a66;margin-bottom:10px", "Heute liegt kein fertiges Reel bereit.")); return; }
      reelBox.appendChild(el("div", "font-size:12px;color:#7a6a66;margin-bottom:6px", "Stand " + (h.datum || "") + " · Hook wählen:"));
      var hooks = el("div", "display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;margin-bottom:8px");
      reelBox.appendChild(hooks);
      h.reels.forEach(function (r, i) {
        var k = el("label", "flex:none;width:130px;cursor:pointer;font-size:12px");
        var vid = el("video", "width:130px;height:231px;object-fit:cover;border-radius:8px;background:#000;display:block");
        vid.src = r.vorschau || r.url; vid.muted = true; vid.playsInline = true; vid.preload = "metadata"; vid.controls = true;
        var zeile = el("div", "display:flex;gap:4px;align-items:flex-start;margin-top:4px");
        var rb = el("input"); rb.type = "radio"; rb.name = "bs-hook"; rb.value = i; if (i === 0) rb.checked = true;
        zeile.appendChild(rb); zeile.appendChild(el("span", "", r.hook || "Version " + (i + 1)));
        k.appendChild(vid); k.appendChild(zeile); hooks.appendChild(k);
      });
      reelWahl = function () { var x = reelBox.querySelector("input[name=bs-hook]:checked"); return h.reels[x ? Number(x.value) : 0]; };
      reelCap = el("textarea", "width:100%;box-sizing:border-box;min-height:110px;padding:9px 10px;border:1px solid #ddd;border-radius:8px;font:13px/1.45 -apple-system,sans-serif;margin-bottom:8px");
      reelCap.value = h.caption || ""; reelBox.appendChild(reelCap);
      cbReel = haken(reelBox, "Reel veröffentlichen", true);
      cbReelStory = haken(reelBox, "Reel zusätzlich als Story", false);
      if (h.story_video && h.story_video.url) {
        reelBox.appendChild(titel("Story-Video"));
        var sv = el("video", "width:130px;height:231px;object-fit:cover;border-radius:8px;background:#000;display:block;margin-bottom:6px");
        sv.src = h.story_video.url; sv.controls = true; sv.playsInline = true; sv.preload = "metadata"; reelBox.appendChild(sv);
        cbStoryVid = haken(reelBox, "Story-Video posten", true);
      }
    });

    /* Posten */
    var los = knopf("Jetzt posten"); los.style.cssText += ";width:100%;padding:14px;font-size:15px;margin-top:14px";
    box.appendChild(los);
    var protokoll = el("div", "margin-top:12px;font-size:13px;white-space:pre-wrap");
    box.appendChild(protokoll);
    function log(t) { protokoll.textContent += t + "\n"; protokoll.scrollIntoView({ block: "end" }); }

    los.onclick = async function () {
      var schritte = [];
      if (cbPost.checked && tagObj) schritte.push("Post Tag " + tagObj.day + " (" + bilder.length + " Folien)");
      if (cbStory.checked && tagObj) schritte.push("Cover als Story");
      if (cbReel && cbReel.checked) schritte.push("Reel");
      if (cbReelStory && cbReelStory.checked) schritte.push("Reel als Story");
      if (cbStoryVid && cbStoryVid.checked) schritte.push("Story-Video");
      if (!schritte.length) { alert("Nichts ausgewählt."); return; }
      if ((cbPost.checked || cbStory.checked) && !bilder.length) { alert("Die Folien sind noch nicht fertig gezeichnet."); return; }
      if (!confirm("Jetzt öffentlich auf Instagram:\n\n• " + schritte.join("\n• "))) return;
      los.disabled = true; los.style.opacity = ".5"; protokoll.textContent = "";
      try {
        var urls = [];
        if (cbPost.checked) {
          log("Folien hochladen …");
          for (var i = 0; i < bilder.length; i++) { log("Folie " + (i + 1) + "/" + bilder.length + " hochladen …"); urls.push(await hochladen(bilder[i], tagObj.day, i + 1)); await warte(400); }
        }
        if (cbPost.checked) {
          var id;
          if (urls.length === 1) id = (await ruf({ aktion: "container", art: "bild", url: urls[0], caption: cap.value })).id;
          else {
            var kinder = [];
            for (var j = 0; j < urls.length; j++) { log("Folie " + (j + 1) + "/" + urls.length + " an Instagram …"); kinder.push((await ruf({ aktion: "container", art: "kind", url: urls[j] })).id); }
            for (var k = 0; k < kinder.length; k++) await fertig(kinder[k], log, "Folie " + (k + 1));
            id = (await ruf({ aktion: "karussell", kinder: kinder, caption: cap.value })).id;
          }
          await fertig(id, log, "Post");
          await ruf({ aktion: "veroeffentlichen", id: id });
          merke("BS_IG_LETZTER", String(tagObj.day));
          log("✓ Post Tag " + tagObj.day + " ist online.");
        }
        if (cbStory.checked) {
          log("Story-Bild 9:16 bauen …");
          var sUrl = await hochladen(await storyBild(bilder[0]), tagObj.day, "story");
          var sid = (await ruf({ aktion: "container", art: "story", url: sUrl })).id;
          await fertig(sid, log, "Story");
          await ruf({ aktion: "veroeffentlichen", id: sid });
          log("✓ Cover-Story ist online.");
        }
        if (cbReel && cbReel.checked) {
          var r = reelWahl();
          log("Reel „" + (r.hook || "") + "“ an Instagram …");
          var rid = (await ruf({ aktion: "container", art: "reel", url: r.url, caption: reelCap.value })).id;
          await fertig(rid, log, "Reel");
          await ruf({ aktion: "veroeffentlichen", id: rid });
          log("✓ Reel ist online.");
        }
        if (cbReelStory && cbReelStory.checked) {
          var rs = (await ruf({ aktion: "container", art: "story-video", url: reelWahl().url })).id;
          await fertig(rs, log, "Reel-Story");
          await ruf({ aktion: "veroeffentlichen", id: rs });
          log("✓ Reel-Story ist online.");
        }
        if (cbStoryVid && cbStoryVid.checked) {
          var vs = (await ruf({ aktion: "container", art: "story-video", url: heute.story_video.url })).id;
          await fertig(vs, log, "Story-Video");
          await ruf({ aktion: "veroeffentlichen", id: vs });
          log("✓ Story-Video ist online.");
        }
        log("Fertig.");
      } catch (e) {
        log("✗ " + e.message + "\nWas oben mit ✓ steht, ist schon online — nicht doppelt posten.");
      } finally { los.disabled = false; los.style.opacity = ""; }
    };

    document.body.appendChild(panel);
  }

  function titel(t) { return el("div", "font:700 10px/1 -apple-system,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#9a7f78;margin:14px 0 8px", t); }
  function knopf(t) { var b = el("button", "border:0;border-radius:999px;padding:9px 14px;font:600 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;cursor:pointer;background:" + OX + ";color:#fff", t); b.type = "button"; return b; }
  function haken(wo, text, an) {
    var l = el("label", "display:flex;gap:8px;align-items:center;font-size:13px;margin:4px 0;cursor:pointer");
    var c = el("input"); c.type = "checkbox"; c.checked = an; l.appendChild(c); l.appendChild(el("span", "", text)); wo.appendChild(l); return c;
  }

  function bau() {
    if (document.getElementById("bs-posten-knopf")) return;
    var b = el("button", "position:fixed;left:10px;bottom:152px;z-index:2147483001;border:0;border-radius:999px;padding:9px 12px;cursor:pointer;background:" + OX + ";color:#fff;font:600 12px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.25)", "↑ Posten");
    b.id = "bs-posten-knopf"; b.type = "button"; b.onclick = oeffne;
    document.body.appendChild(b);
    var css = el("style"); css.textContent = "body.bs-insta #bs-posten-knopf,body.bs-auswahl #bs-posten-knopf{display:none!important}";
    document.head.appendChild(css);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bau); else bau();
})();
