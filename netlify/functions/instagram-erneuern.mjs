// Geplante Netlify Function: verlaengert den Instagram-Schluessel (IG_ACCESS_TOKEN) jede Woche
// um 60 Tage. So laeuft er nie ab, solange die Seite online ist.
export default async () => {
  const q = new URLSearchParams({ grant_type: 'ig_refresh_token', access_token: process.env.IG_ACCESS_TOKEN || '' });
  const r = await fetch(`https://graph.instagram.com/refresh_access_token?${q}`);
  const d = await r.json().catch(() => ({}));
  console.log(d.error ? `Erneuern fehlgeschlagen: ${d.error.message}` : `Schluessel verlaengert, gueltig ${Math.round((d.expires_in || 0) / 86400)} Tage`);
};

export const config = { schedule: '@weekly' };
