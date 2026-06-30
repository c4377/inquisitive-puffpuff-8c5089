# Supabase Setup Anleitung

Damit die App funktioniert, folge diesen Schritten in deinem Supabase Dashboard.

## 1. Tabelle erstellen (SQL Editor)

Gehe in Supabase links auf **SQL Editor**, klicke auf "New Query", füge den folgenden Code ein und klicke auf **RUN**:

```sql
-- 1. Tabelle erstellen (Speichert alle App-Daten pro User)
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

-- 2. Row Level Security (RLS) aktivieren (Datenschutz)
ALTER TABLE public.user_state ENABLE ROW LEVEL SECURITY;

-- 3. Policies erstellen (Damit jeder nur SEINE Daten sieht)
-- Erlaubt das Erstellen der eigenen Daten
CREATE POLICY "Users can insert own state" 
ON public.user_state FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Erlaubt das Lesen der eigenen Daten
CREATE POLICY "Users can select own state" 
ON public.user_state FOR SELECT 
USING (auth.uid() = user_id);

-- Erlaubt das Aktualisieren der eigenen Daten
CREATE POLICY "Users can update own state" 
ON public.user_state FOR UPDATE 
USING (auth.uid() = user_id);

-- 4. Automatisches Update-Datum (Optional, aber gut für Sync)
CREATE OR REPLACE FUNCTION handle_updated_at() RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON public.user_state
FOR EACH ROW
EXECUTE PROCEDURE handle_updated_at();
```

## 2. Authentifizierung einstellen

1. Gehe im Menü links auf **Authentication**.
2. Klicke auf **Providers** und stelle sicher, dass **Email** aktiviert ist.
3. **WICHTIG:** Gehe auf **URL Configuration** (oder "Site URL") und trage deine App-URL ein (z.B. die Localhost URL oder deine Live-URL).
4. **OPTIONAL (Empfohlen für Tests):** Deaktiviere "Confirm email" unter **Providers > Email**, damit du dich nach dem Registrieren sofort einloggen kannst, ohne erst in ein E-Mail-Postfach schauen zu müssen.

## 3. Verbindung herstellen

1. Gehe auf **Settings (Zahnrad)** > **API**.
2. Kopiere die **Project URL**.
3. Kopiere den **anon / public** Key.
4. Öffne deine App.
5. Klicke im Login-Screen oben rechts auf das kleine **Zahnrad-Icon**.
6. Füge die Daten ein und speichere.

Fertig!