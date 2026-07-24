import { createClient } from '@supabase/supabase-js';

// --- CONFIGURATION ---
// Credentials come from environment variables (Netlify → Environment
// variables), with a localStorage fallback so they can also be entered
// directly in the app (Admin panel) — useful when env vars aren't set yet.
//   VITE_SUPABASE_URL       = https://<project>.supabase.co
//   VITE_SUPABASE_ANON_KEY  = <anon public key>
const ls = (k) => { try { return localStorage.getItem(k) || ''; } catch { return ''; } };
// Accept the URL in any pasted form ("https://x.supabase.co/rest/v1", trailing
// slash, etc.) and reduce it to the plain origin the client needs. A pasted
// REST endpoint otherwise breaks ALL storage calls with "Invalid path".
const cleanUrl = (u) => {
  if (!u) return '';
  try { return new URL(u).origin; } catch { return String(u).replace(/\/+$/, ''); }
};
const getUrl = () => cleanUrl(import.meta.env.VITE_SUPABASE_URL || ls('vite_supabase_url') || '');
const getKey = () => (import.meta.env.VITE_SUPABASE_ANON_KEY || ls('vite_supabase_key') || '').trim();

// Only create the client if the keys are available
export const supabase = (getUrl() && getKey()) ? createClient(getUrl(), getKey()) : null;

if (!supabase && typeof console !== 'undefined') {
  console.warn('[Supabase] Keine Zugangsdaten gefunden. Bitte VITE_SUPABASE_URL und VITE_SUPABASE_ANON_KEY in Netlify setzen. Cloud-Upload ist deaktiviert.');
}

// Helper to save config dynamically (Admin Panel Override)
export const setupSupabase = (url, key) => {
  if (!url || !key) return false;
  try {
    // Validate URL format roughly
    new URL(url);
    localStorage.setItem('vite_supabase_url', url);
    localStorage.setItem('vite_supabase_key', key);
    
    // Force reload to re-initialize the module with new keys
    window.location.reload();
    return true;
  } catch (e) {
    return false;
  }
};

export const isSupabaseConfigured = () => !!supabase;
// --- IMAGE STORAGE HELPERS (Supabase Storage) ---
// Bucket muss im Supabase-Dashboard existieren und "public" sein.
const BUCKET = 'brand-images';

/**
 * Lädt eine Datei in den Supabase-Storage und gibt die öffentliche URL zurück.
 * Bei Fehler/ohne Supabase: null (Aufrufer kann auf Base64 zurückfallen).
 */
export const uploadImageToCloud = async (file) => {
  if (!supabase || !file) return null;
  try {
    const ext = (file.name?.split('.').pop() || 'jpg').toLowerCase();
    const path = `pool/${Date.now()}-${Math.random().toString(36).slice(2, 8)}.${ext}`;
    const { error } = await supabase.storage
      .from(BUCKET)
      .upload(path, file, { cacheControl: '31536000', upsert: false });
    if (error) {
      console.error('Supabase upload error:', error.message);
      return null;
    }
    const { data } = supabase.storage.from(BUCKET).getPublicUrl(path);
    return data?.publicUrl || null;
  } catch (e) {
    console.error('uploadImageToCloud failed:', e);
    return null;
  }
};

/** Listet alle öffentlichen Bild-URLs im Pool (für geräteübergreifendes Laden). */
export const listCloudImages = async () => {
  if (!supabase) return [];
  try {
    const { data, error } = await supabase.storage.from(BUCKET).list('pool', {
      limit: 1000,
      sortBy: { column: 'created_at', order: 'asc' },
    });
    if (error || !data) return [];
    return data
      .filter((f) => f.name && !f.name.startsWith('.'))
      .map((f) => supabase.storage.from(BUCKET).getPublicUrl(`pool/${f.name}`).data.publicUrl);
  } catch (e) {
    console.error('listCloudImages failed:', e);
    return [];
  }
};

/**
 * Löscht ein Bild aus dem Cloud-Storage anhand seiner öffentlichen URL.
 * Gibt true zurück bei Erfolg (oder wenn es keine Cloud-URL war).
 */
export const deleteCloudImage = async (url) => {
  if (!supabase || !url || typeof url !== 'string') return true;
  // Only handle our own cloud URLs (contain the bucket path)
  const marker = `/${BUCKET}/`;
  const idx = url.indexOf(marker);
  if (idx === -1) return true; // not a cloud image (local base64) -> nothing to delete
  const path = url.substring(idx + marker.length).split('?')[0];
  try {
    const { error } = await supabase.storage.from(BUCKET).remove([path]);
    if (error) {
      console.error('deleteCloudImage error:', error.message);
      return false;
    }
    return true;
  } catch (e) {
    console.error('deleteCloudImage failed:', e);
    return false;
  }
};
