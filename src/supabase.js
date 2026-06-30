import { createClient } from '@supabase/supabase-js';

// --- PRODUCTION CONFIGURATION ---
// Diese Werte werden für die Ausrollung genutzt, wenn keine lokalen Einstellungen vorhanden sind.
const DEFAULT_URL = 'https://jrectgvbgtclsqouiyot.supabase.co';
const DEFAULT_KEY = 'sb_publishable_EYA3ijgxMNWZo_rXG7cvRg_DibuJwM5'; 

// Helper to get config from Env OR LocalStorage OR Default
const getUrl = () => {
    return import.meta.env.VITE_SUPABASE_URL || 
           localStorage.getItem('vite_supabase_url') || 
           DEFAULT_URL;
};

const getKey = () => {
    return import.meta.env.VITE_SUPABASE_ANON_KEY || 
           localStorage.getItem('vite_supabase_key') || 
           DEFAULT_KEY;
};

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