import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FiMail, FiLock, FiZap, FiAlertCircle, FiCheck, FiDatabase, FiSettings, FiX } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { setupSupabase, isSupabaseConfigured } from '../supabase';

const Login = () => {
  const { user, signIn, signUp } = useAuth();
  const navigate = useNavigate();
  
  // State for Login/Register
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Admin Config State (Hidden by default)
  const [showAdminConfig, setShowAdminConfig] = useState(false);
  const [sbUrl, setSbUrl] = useState(localStorage.getItem('vite_supabase_url') || '');
  const [sbKey, setSbKey] = useState(localStorage.getItem('vite_supabase_key') || '');

  // AUTO-REDIRECT: Wenn User eingeloggt ist, sofort zum Dashboard
  useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  const handleConfigSubmit = (e) => {
    e.preventDefault();
    setError('');
    const success = setupSupabase(sbUrl, sbKey);
    if (!success) {
      setError("Ungültige URL oder fehlende Daten.");
    } else {
      setSuccess("System verbunden! Seite wird neu geladen...");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    // Check configuration first
    if (!isSupabaseConfigured()) {
        setError("Systemfehler: Datenbank nicht verbunden. Bitte Admin kontaktieren.");
        setLoading(false);
        return;
    }

    try {
      if (isLogin) {
        const { error } = await signIn(email, password);
        if (error) throw error;
      } else {
        const { data, error } = await signUp(email, password);
        if (error) throw error;
        
        if (data?.user?.identities?.length === 0) {
            setError("Dieser User existiert bereits. Bitte einloggen.");
        } else {
            setSuccess("Account erstellt! Du wirst automatisch eingeloggt...");
        }
      }
    } catch (err) {
      console.error("Auth Error:", err);
      if (err.message && err.message.includes("Invalid login credentials")) {
        setError("Email oder Passwort falsch.");
      } else {
        setError(err.message || "Ein Fehler ist aufgetreten.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12 relative">
      
      {/* ADMIN TRIGGER (Discreet Gear Icon) */}
      <button 
        onClick={() => setShowAdminConfig(true)}
        className="absolute top-6 right-6 text-gray-300 hover:text-gray-500 transition-colors p-2"
        title="Admin Setup"
      >
        <SafeIcon icon={FiSettings} />
      </button>

      {/* ADMIN CONFIG MODAL OVERLAY */}
      {showAdminConfig && (
        <div className="absolute inset-0 z-50 bg-white/95 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl border border-gray-200 relative animate-fade-in">
            <button 
                onClick={() => setShowAdminConfig(false)}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
            >
                <SafeIcon icon={FiX} className="text-xl" />
            </button>

            <div className="text-center mb-6">
                <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <SafeIcon icon={FiDatabase} className="text-gray-600 text-2xl" />
                </div>
                <h2 className="text-xl font-bold text-gray-900">Admin Setup</h2>
                <p className="text-xs text-gray-500 mt-1">Supabase Verbindung konfigurieren</p>
            </div>

            <form onSubmit={handleConfigSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Project URL</label>
                  <input 
                    type="text" 
                    value={sbUrl}
                    onChange={(e) => setSbUrl(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-xl text-sm font-mono"
                    placeholder="https://xyz.supabase.co"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Anon Key</label>
                  <input 
                    type="password" 
                    value={sbKey}
                    onChange={(e) => setSbKey(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-xl text-sm font-mono"
                    placeholder="public-key..."
                  />
                </div>
                <button 
                  type="submit" 
                  className="w-full py-3 bg-gray-900 text-white rounded-xl font-bold hover:bg-black transition-all flex items-center justify-center"
                >
                  <SafeIcon icon={FiCheck} className="mr-2" /> Speichern & Neustart
                </button>
            </form>
          </div>
        </div>
      )}

      {/* NORMAL LOGIN CARD */}
      <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 w-full max-w-md relative overflow-hidden">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <SafeIcon icon={FiZap} className="text-white text-2xl" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">
            {isLogin ? 'Willkommen zurück' : 'Account erstellen'}
          </h1>
          <p className="text-gray-500 mt-2 text-sm">
            {isLogin 
              ? 'Logge dich ein, um deine Brands zu synchronisieren.' 
              : 'Erstelle einen Account, um deine Designs zu speichern.'}
          </p>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 text-red-600 p-3 rounded-lg text-sm flex items-center border border-red-100">
            <SafeIcon icon={FiAlertCircle} className="mr-2 flex-shrink-0" />
            {error}
          </div>
        )}
        
        {success && (
          <div className="mb-4 bg-green-50 text-green-600 p-3 rounded-lg text-sm flex items-center border border-green-100">
            <SafeIcon icon={FiCheck} className="mr-2 flex-shrink-0" />
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Email</label>
            <div className="relative">
              <SafeIcon icon={FiMail} className="absolute left-3 top-3 text-gray-400" />
              <input 
                type="email" 
                required 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="deine@email.com"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-xs font-bold text-gray-700 uppercase mb-1">Passwort</label>
            <div className="relative">
              <SafeIcon icon={FiLock} className="absolute left-3 top-3 text-gray-400" />
              <input 
                type="password" 
                required 
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3 bg-gray-900 text-white rounded-xl font-bold hover:bg-black transition-all flex items-center justify-center shadow-lg disabled:opacity-50"
          >
            {loading ? <span className="animate-spin text-xl mr-2"><SafeIcon icon={FiZap} /></span> : (isLogin ? 'Einloggen' : 'Registrieren')}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className="text-sm text-purple-600 font-bold hover:underline"
          >
            {isLogin ? 'Noch keinen Account? Registrieren' : 'Bereits einen Account? Einloggen'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;