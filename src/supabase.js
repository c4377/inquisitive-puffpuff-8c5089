import { createClient } from '@supabase/supabase-js';

// --- PRODUCTION CONFIGURATION ---
// Diese Werte werden für die Ausrollung genutzt, wenn keine lokalen Einstellungen vorhanden sind.
const DEFAULT_URL = 'https://kfrdrcrgbkjuusrhftlg.supabase.co';
const DEFAULT_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtmcmRyY3JnYmtqdXVzcmhmdGxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzMzMDgsImV4cCI6MjA5ODQwOTMwOH0.IvIEPallRrka5sWZrREumo0U3jGWQMAXEshyGSLyRic';

// Helper to get config from Env OR Default.
// (localStorage override removed so stale keys from the old Greta project
//  can never take precedence over this project's credentials.)
const getUrl = () => import.meta.env.VITE_SUPABASE_URL || DEFAULT_URL;
const getKey = () => import.meta.env.VITE_SUPABASE_ANON_KEY || DEFAULT_KEY;

// Only create the client if the keys are available
export const supabase = (getUrl() && getKey()) ? createClient(getUrl(), getKey()) : null;

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
      limit: 100,
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
