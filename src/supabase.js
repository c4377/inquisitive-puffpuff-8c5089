import { createClient } from '@supabase/supabase-js';

// --- CONFIGURATION ---
// Credentials MUST come from environment variables (Netlify → Environment
// variables). No hardcoded fallback: every instance uses its own Supabase
// project, so no customer can ever write into someone else's bucket.
//   VITE_SUPABASE_URL       = https://<project>.supabase.co
//   VITE_SUPABASE_ANON_KEY  = <anon public key>
const getUrl = () => import.meta.env.VITE_SUPABASE_URL || '';
const getKey = () => import.meta.env.VITE_SUPABASE_ANON_KEY || '';

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
      .upload(path, file, { cacheControl: '3600', upsert: false });
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
