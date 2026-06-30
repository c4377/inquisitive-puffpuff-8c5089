/* 
# Create User State Schema
1. New Tables
   - `user_state` (Singleton per user to store app state)
     - `user_id` (uuid, PK)
     - `brand_configurations` (jsonb)
     - `content_plan` (jsonb)
     - `saved_designs` (jsonb)
     - `community_decks` (jsonb)
     - `feed_profile` (jsonb)
     - `strategy` (jsonb)
     - `current_brand_config` (jsonb)
     - `updated_at` (timestamp)
2. Security
   - Enable RLS
   - Add policies for users to manage their own state
*/

CREATE TABLE IF NOT EXISTS public.user_state (
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  brand_configurations jsonb DEFAULT '[]'::jsonb,
  content_plan jsonb DEFAULT '[]'::jsonb,
  saved_designs jsonb DEFAULT '[]'::jsonb,
  community_decks jsonb DEFAULT '{}'::jsonb,
  feed_profile jsonb DEFAULT '{}'::jsonb,
  strategy jsonb DEFAULT '{}'::jsonb,
  current_brand_config jsonb DEFAULT NULL,
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE public.user_state ENABLE ROW LEVEL SECURITY;

-- Policy: Users can insert their own state
CREATE POLICY "Users can insert own state" 
ON public.user_state 
FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can select their own state
CREATE POLICY "Users can select own state" 
ON public.user_state 
FOR SELECT 
USING (auth.uid() = user_id);

-- Policy: Users can update their own state
CREATE POLICY "Users can update own state" 
ON public.user_state 
FOR UPDATE 
USING (auth.uid() = user_id);

-- Function to handle updated_at
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updated_at
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON public.user_state
FOR EACH ROW
EXECUTE PROCEDURE handle_updated_at();