import { supabase } from '../supabase';

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
  }
};