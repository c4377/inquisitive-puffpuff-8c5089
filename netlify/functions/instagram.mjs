// Netlify Function: Posten auf Instagram über die offizielle Instagram API (Instagram-Login).
// Der Schluessel bleibt SERVERSEITIG: IG_ACCESS_TOKEN, IG_USER_ID, POST_PIN (Netlify → Environment variables).
// Jeder Aufruf braucht den PIN (Feld "pin"), sonst koennte jede/r ueber diese Adresse posten.
//
// Die App steuert die Schritte einzeln, weil Instagram Videos erst verarbeiten muss und eine
// Funktion nur wenige Sekunden laufen darf:
//   { aktion: "check" }                                   -> { username, user_id }
//   { aktion: "container", art: "bild"|"kind"|"story"|"story-video"|"reel", url, caption? }
//                                                         -> { id }
//   { aktion: "karussell", kinder: [id…], caption }       -> { id }
//   { aktion: "status", id }                              -> { status }   (FINISHED, IN_PROGRESS, ERROR …)
//   { aktion: "veroeffentlichen", id }                    -> { id: media_id }
//   { aktion: "erneuern" }                                -> { expires_in }  Schluessel um 60 Tage verlaengern

const API = 'https://graph.instagram.com/v23.0';

function antwort(daten, status = 200) {
  return new Response(JSON.stringify(daten), { status, headers: { 'Content-Type': 'application/json' } });
}

async function ig(pfad, params, methode = 'POST') {
  const token = process.env.IG_ACCESS_TOKEN;
  const q = new URLSearchParams({ ...params, access_token: token });
  const url = methode === 'GET' ? `${API}/${pfad}?${q}` : `${API}/${pfad}`;
  const r = await fetch(url, methode === 'GET' ? {} : {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: q,
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok || d.error) {
    const e = d.error || {};
    throw Object.assign(new Error(e.error_user_msg || e.message || `Instagram HTTP ${r.status}`), { status: 502 });
  }
  return d;
}

// Verlaengert den Schluessel um 60 Tage ab heute (geht, solange er noch gueltig und mind. 24 h alt ist).
async function erneuern() {
  const q = new URLSearchParams({ grant_type: 'ig_refresh_token', access_token: process.env.IG_ACCESS_TOKEN || '' });
  const r = await fetch(`https://graph.instagram.com/refresh_access_token?${q}`);
  return r.json().catch(() => ({ error: { message: `HTTP ${r.status}` } }));
}

// Die ID fuers Posten kommt direkt von Instagram (/me → user_id). Die Nummer aus dem Meta-Dashboard
// passt bei Instagram-Login nicht immer (Fehler „Object … does not exist“), deshalb nicht IG_USER_ID.
let meineId = null;
async function nutzer() {
  if (meineId) return meineId;
  const d = await ig('me', { fields: 'user_id' }, 'GET');
  meineId = String(d.user_id || d.id);
  return meineId;
}

function pruefeUrl(u) {
  const s = String(u || '');
  if (!/^https:\/\/[^\s]+$/.test(s)) throw Object.assign(new Error('Ungültige Datei-Adresse.'), { status: 400 });
  return s;
}

export default async (req) => {
  if (req.method !== 'POST') return antwort({ error: 'POST only' }, 405);
  if (!process.env.IG_ACCESS_TOKEN) return antwort({ error: 'IG_ACCESS_TOKEN fehlt (Netlify → Environment variables).' }, 500);
  if (!process.env.POST_PIN) return antwort({ error: 'POST_PIN fehlt (Netlify → Environment variables).' }, 500);

  let b = {};
  try { b = await req.json(); } catch { return antwort({ error: 'Ungültiger Body' }, 400); }
  if (String(b.pin || '') !== String(process.env.POST_PIN)) return antwort({ error: 'PIN stimmt nicht.' }, 401);

  const caption = String(b.caption || '').slice(0, 2200);
  try {
    switch (b.aktion) {
      case 'check': {
        const d = await ig('me', { fields: 'user_id,username' }, 'GET');
        return antwort({ username: d.username, user_id: d.user_id || d.id });
      }
      case 'container': {
        const url = pruefeUrl(b.url);
        const p = {};
        if (b.art === 'bild') Object.assign(p, { image_url: url, caption });
        else if (b.art === 'kind') Object.assign(p, { image_url: url, is_carousel_item: 'true' });
        else if (b.art === 'story') Object.assign(p, { image_url: url, media_type: 'STORIES' });
        else if (b.art === 'story-video') Object.assign(p, { video_url: url, media_type: 'STORIES' });
        else if (b.art === 'reel') Object.assign(p, { video_url: url, media_type: 'REELS', caption, share_to_feed: 'true' });
        else return antwort({ error: 'Unbekannte Art.' }, 400);
        const d = await ig(`${await nutzer()}/media`, p);
        return antwort({ id: d.id });
      }
      case 'karussell': {
        const kinder = (Array.isArray(b.kinder) ? b.kinder : []).map(String).filter((x) => /^\d+$/.test(x));
        if (kinder.length < 2) return antwort({ error: 'Ein Karussell braucht mindestens 2 Bilder.' }, 400);
        const d = await ig(`${await nutzer()}/media`, { media_type: 'CAROUSEL', children: kinder.join(','), caption });
        return antwort({ id: d.id });
      }
      case 'status': {
        if (!/^\d+$/.test(String(b.id || ''))) return antwort({ error: 'id fehlt' }, 400);
        const d = await ig(String(b.id), { fields: 'status_code,status' }, 'GET');
        return antwort({ status: d.status_code, detail: d.status || '' });
      }
      case 'veroeffentlichen': {
        if (!/^\d+$/.test(String(b.id || ''))) return antwort({ error: 'id fehlt' }, 400);
        const d = await ig(`${await nutzer()}/media_publish`, { creation_id: String(b.id) });
        return antwort({ id: d.id });
      }
      case 'erneuern': {
        const d = await erneuern();
        if (d.error) return antwort({ error: d.error.message || 'Erneuern fehlgeschlagen' }, 502);
        return antwort({ expires_in: d.expires_in, gleich: d.access_token === process.env.IG_ACCESS_TOKEN });
      }
      default:
        return antwort({ error: 'Unbekannte Aktion.' }, 400);
    }
  } catch (e) {
    return antwort({ error: String(e?.message || e) }, e?.status || 500);
  }
};
