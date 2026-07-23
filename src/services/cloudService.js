import { supabase } from '../supabase';

const SCREENSHOT_BUCKET = 'screenshots';

// Convert a base64 data URL to a Blob for upload.
const dataUrlToBlob = (dataUrl) => {
  const [head, body] = dataUrl.split(',');
  const mime = (head.match(/data:(.*?);/) || [])[1] || 'image/png';
  const bin = atob(body);
  const len = bin.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) bytes[i] = bin.charCodeAt(i);
  return new Blob([bytes], { type: mime });
};

export const CloudService = {
  // Load all user data from cloud
  async loadUserState(userId) {
    if (!supabase || !userId) return null;

    const { data, error } = await supabase
      .from('user_state')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error && error.code !== 'PGRST116') { // PGRST116 is "Row not found" (new user)
      console.error('Error loading cloud state:', error);
      return null;
    }

    return data;
  },

  // Save specific parts of state to cloud
  async saveUserState(userId, data) {
    if (!supabase || !userId) return;

    // We use upsert to handle both insert (new user) and update
    const { error } = await supabase
      .from('user_state')
      .upsert({
        user_id: userId,
        ...data,
        updated_at: new Date().toISOString()
      });

    if (error) {
      console.error('Error saving to cloud:', error);
    }
  },

  // --- Screenshot library ---------------------------------------------------
  // Screenshots are uploaded ONCE and then live in the bucket together with the
  // OCR text we read from them. Later imports can re-use them automatically:
  // whenever a [SCREENSHOT — …] placeholder matches a stored OCR text, that
  // image is pulled in without the user uploading anything again.

  // Load the whole library: [{ url, ocrText, path }]
  async loadScreenshotLibrary() {
    try {
      if (!supabase) return [];
      const { data, error } = await supabase
        .from('screenshot_library')
        .select('*')
        .order('created_at', { ascending: false });
      if (error) {
        console.error('Screenshot library load failed:', error);
        return [];
      }
      return (data || []).map((r) => ({ url: r.url, ocrText: r.ocr_text || '', path: r.path }));
    } catch (e) {
      console.error('Screenshot library error:', e);
      return [];
    }
  },

  // Remember one uploaded screenshot together with its OCR text.
  async addToScreenshotLibrary({ url, ocrText, path }) {
    try {
      if (!supabase || !url) return false;
      const { error } = await supabase
        .from('screenshot_library')
        .insert({ url, ocr_text: ocrText || '', path: path || '' });
      if (error) {
        console.error('Screenshot library save failed:', error);
        return false;
      }
      return true;
    } catch (e) {
      console.error('Screenshot library save error:', e);
      return false;
    }
  },

  // Upload one OCR-matched screenshot (base64 data URL) to Supabase Storage and
  // return its public URL, so screenshots persist across reloads instead of
  // living as huge base64 blobs inside the plan. No login required — files go
  // into a shared folder. Returns the original dataUrl as a fallback if anything
  // fails, so the app still works offline.
  async uploadScreenshot(dataUrl) {
    try {
      if (!supabase || !dataUrl || !dataUrl.startsWith('data:')) return dataUrl;
      const blob = dataUrlToBlob(dataUrl);
      const ext = (blob.type.split('/')[1] || 'png').replace('jpeg', 'jpg');
      const path = `shared/${Date.now()}_${Math.random().toString(36).slice(2, 8)}.${ext}`;
      const { error } = await supabase.storage
        .from(SCREENSHOT_BUCKET)
        .upload(path, blob, { contentType: blob.type, upsert: true });
      if (error) {
        console.error('Screenshot upload failed:', error);
        return dataUrl; // fall back to inline base64
      }
      const { data } = supabase.storage.from(SCREENSHOT_BUCKET).getPublicUrl(path);
      return (data && data.publicUrl) ? data.publicUrl : dataUrl;
    } catch (e) {
      console.error('Screenshot upload error:', e);
      return dataUrl;
    }
  }
};