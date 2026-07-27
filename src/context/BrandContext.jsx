import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { 
  saveImagesToDB, loadImagesFromDB, 
  saveDesignsToDB, loadDesignsFromDB, 
  saveFontsToDB, loadFontsFromDB,
  savePlanToDB, loadPlanFromDB,
  saveCommunityDecksToDB, loadCommunityDecksFromDB
} from '../utils/storage';
import { useAuth } from './AuthContext';
import { CURATED_BRANDS } from '../constants/brandData';
import { loadGoogleFonts } from '../utils/fontLoader';
import { CloudService } from '../services/cloudService';

const BrandContext = createContext();

export const useBrand = () => {
  const context = useContext(BrandContext);
  if (!context) throw new Error('useBrand must be used within a BrandProvider');
  return context;
};

// --- DEFAULT STRATEGY ---
const DEFAULT_STRATEGY = {
  industry: 'Identity & Business Mentoring',
  targetAudience: 'Ambitionierte, intelligente Frauen, die fühlen, dass in ihnen mehr steckt...',
  painPoints: [
    'Feststecken im Kopf',
    'Angst „zu viel/zu wenig“ zu sein',
    'Selbstsabotage durch Unsichtbarkeit',
  ],
  goals: [
    'Wahre Identität freilegen',
    'Klarheit in Messaging & Angebot',
  ]
};

const DEFAULT_FEED_PROFILE = {
  username: 'dein.business',
  name: 'Dein Name | Expertin',
  bio: 'Ich helfe dir, deine Brand aufzubauen.\n✨ Strategie & Design',
  website: 'www.deine-website.de',
  stats: { posts: 42, followers: 1250, following: 300 },
  profileImage: null,
  highlights: [
    { id: 1, title: 'Neu', image: null },
    { id: 2, title: 'Business', image: null },
    { id: 3, title: 'Mindset', image: null },
  ],
  extraPosts: []
};

export const BrandProvider = ({ children }) => {
  const { user } = useAuth();

  // Ensure the fixed curated brands are always present (and up to date) in the
  // brand list, without duplicating them.
  const withCuratedBrands = (list = []) => {
    const others = list.filter(b => !String(b?.id || '').startsWith('curated_'));
    return [...CURATED_BRANDS, ...others];
  };

  const [brandSettings, setBrandSettings] = useState(() => {
    try {
      const savedSettings = localStorage.getItem('brandSettings');
      const parsedSettings = savedSettings ? JSON.parse(savedSettings) : {};
      
      return {
        brandImages: [],
        brandConfigurations: withCuratedBrands([]),
        savedDesigns: [],
        customFonts: [],
        currentBrandConfig: null,
        contentPlan: [],
        communityDecks: {},
        feedProfile: { ...DEFAULT_FEED_PROFILE, ...(parsedSettings.feedProfile || {}) },
        ...parsedSettings,
        // Hard guarantee: the plan must always be an array of days that each
        // have a slides array. Anything else would crash the feed grid.
        contentPlan: (Array.isArray(parsedSettings.contentPlan) ? parsedSettings.contentPlan : [])
          .filter((d) => d && typeof d === 'object')
          .map((d) => ({ ...d, slides: Array.isArray(d.slides) ? d.slides.filter(Boolean) : [] })),
        brandConfigurations: withCuratedBrands(parsedSettings.brandConfigurations || []),
        strategy: { ...DEFAULT_STRATEGY, ...(parsedSettings.strategy || {}) }
      };
    } catch (e) {
      console.error("Error loading settings:", e);
      return {
        brandImages: [],
        brandConfigurations: withCuratedBrands([]),
        savedDesigns: [],
        customFonts: [],
        contentPlan: [],
        communityDecks: {},
        strategy: DEFAULT_STRATEGY,
        feedProfile: DEFAULT_FEED_PROFILE
      };
    }
  });

  const [dataLoaded, setDataLoaded] = useState(false);
  const syncTimeoutRef = useRef(null);

  // 1. LOAD LOCAL DATA ON MOUNT
  // Live-load the active brand's fonts (Brandsheet brands may use any Google
  // Font). Deduped internally, so this is free when fonts are already present.
  useEffect(() => {
    const t = brandSettings?.currentBrandConfig?.typography;
    if (!t) return;
    loadGoogleFonts([t.fontFamily, t.bodyFontFamily, t.accentFontFamily]);
  }, [brandSettings?.currentBrandConfig?.typography?.fontFamily,
      brandSettings?.currentBrandConfig?.typography?.bodyFontFamily,
      brandSettings?.currentBrandConfig?.typography?.accentFontFamily]);

  useEffect(() => {
    const loadLocalData = async () => {
      try {
        const [images, designs, fonts, plan, decks] = await Promise.all([
          loadImagesFromDB(),
          loadDesignsFromDB(),
          loadFontsFromDB(),
          loadPlanFromDB(),
          loadCommunityDecksFromDB()
        ]);

        if (fonts && fonts.length > 0) {
          fonts.forEach(async (fontData) => {
            try {
              const fontFace = new FontFace(fontData.name, fontData.data);
              await fontFace.load();
              document.fonts.add(fontFace);
            } catch (err) {
              console.error(`Failed to load font ${fontData.name}`, err);
            }
          });
        }

        // Normalise the plan coming from IndexedDB: it must be an array of day
        // objects that each carry a slides array. A malformed entry here would
        // crash the feed grid on render (white screen).
        const safePlan = (Array.isArray(plan) ? plan : [])
          .filter((d) => d && typeof d === 'object')
          .map((d) => ({ ...d, slides: Array.isArray(d.slides) ? d.slides.filter(Boolean) : [] }))
          .filter((d) => d.slides.length > 0);

        // TOTE BILDVERWEISE ENTFERNEN.
        // Wird ein Foto im Brand-Bereich geloescht, behalten alte Kacheln ihre
        // URL. Der Browser fordert die geloeschte Datei dann weiter an und der
        // Speicher antwortet mit "Bad Request". Deshalb beim Laden pruefen:
        // zeigt eine Kachel auf ein Foto, das es nicht mehr gibt, wird der
        // Verweis geloescht — die Kachel wird zur Textkachel statt kaputt.
        // Nur wenn der Pool wirklich geladen ist, sonst wuerde ein Ladefehler
        // alle Fotos aus dem Plan werfen.
        const pool = Array.isArray(images) ? images : [];
        let planForState = safePlan;
        if (pool.length > 0) {
          const alive = new Set(
            pool.map((i) => (typeof i === 'string' ? i : i?.src || i?.url || i?.dataUrl))
              .filter(Boolean)
          );
          let removed = 0;
          planForState = safePlan.map((d) => ({
            ...d,
            slides: d.slides.map((sl) => {
              const bg = sl && sl.background;
              if (typeof bg !== 'string' || !bg || alive.has(bg)) return sl;
              removed++;
              return { ...sl, background: null, overlay: undefined, _autoImage: undefined };
            }),
          }));
          if (removed > 0) {
            console.warn(`[BrandStudio] ${removed} Kachel(n) zeigten auf geloeschte Fotos — Verweis entfernt.`);
          }
        }

        setBrandSettings(prev => ({
          ...prev,
          brandImages: images || [],
          savedDesigns: designs || [],
          customFonts: fonts || [],
          contentPlan: planForState,
          communityDecks: decks || {}
        }));
      } catch (error) {
        console.error("Critical Error loading DB:", error);
      } finally {
        setDataLoaded(true);
      }
    };
    loadLocalData();
  }, []);

  // 2. CLOUD SYNC: LOAD WHEN USER LOGS IN
  useEffect(() => {
    const syncCloudData = async () => {
      if (user && dataLoaded) {
        console.log("User logged in, syncing cloud state...");
        const cloudState = await CloudService.loadUserState(user.id);
        
        if (cloudState) {
          // Merge Cloud Data with Local State — but always keep the fixed
          // curated brands present (cloud data predates them).
          setBrandSettings(prev => ({
            ...prev,
            brandConfigurations: withCuratedBrands(cloudState.brand_configurations || prev.brandConfigurations),
            contentPlan: cloudState.content_plan || prev.contentPlan,
            savedDesigns: cloudState.saved_designs || prev.savedDesigns,
            communityDecks: cloudState.community_decks || prev.communityDecks,
            feedProfile: cloudState.feed_profile || prev.feedProfile,
            strategy: cloudState.strategy || prev.strategy,
            currentBrandConfig: cloudState.current_brand_config || prev.currentBrandConfig
          }));
        } else {
             // New user or no data yet: Upload current local state as initial state
             console.log("No cloud data found, uploading local state...");
             saveToCloud(user.id, brandSettings);
        }
      }
    };
    syncCloudData();
  }, [user, dataLoaded]);

  // Helper to save to Cloud with Debounce
  const saveToCloud = (userId, settings) => {
      if (!userId) return;
      
      if (syncTimeoutRef.current) clearTimeout(syncTimeoutRef.current);
      
      syncTimeoutRef.current = setTimeout(() => {
          CloudService.saveUserState(userId, {
              brand_configurations: settings.brandConfigurations,
              content_plan: settings.contentPlan,
              saved_designs: settings.savedDesigns,
              community_decks: settings.communityDecks,
              feed_profile: settings.feedProfile,
              strategy: settings.strategy,
              current_brand_config: settings.currentBrandConfig
          });
      }, 2000); // 2 second debounce
  };

  // 3. PERSISTENCE LISTENERS
  useEffect(() => {
    // A. LocalStorage (Lightweight)
    const settingsToSave = { ...brandSettings };
    delete settingsToSave.brandImages;
    delete settingsToSave.savedDesigns;
    delete settingsToSave.customFonts;
    delete settingsToSave.contentPlan;
    delete settingsToSave.communityDecks;
    
    try {
      localStorage.setItem('brandSettings', JSON.stringify(settingsToSave));
    } catch (e) {
      console.error("LocalStorage Quota Exceeded", e);
    }
    
    // B. Cloud Sync (if user exists)
    if (user && dataLoaded) {
        saveToCloud(user.id, brandSettings);
    }

  }, [brandSettings, user, dataLoaded]);

  // C. IndexedDB (Heavy Data)
  useEffect(() => {
    if (dataLoaded) {
      saveImagesToDB(brandSettings.brandImages || []);
      saveDesignsToDB(brandSettings.savedDesigns || []);
      saveFontsToDB(brandSettings.customFonts || []);
      savePlanToDB(brandSettings.contentPlan || []);
      saveCommunityDecksToDB(brandSettings.communityDecks || {});
    }
  }, [
    brandSettings.brandImages, 
    brandSettings.savedDesigns, 
    brandSettings.customFonts, 
    brandSettings.contentPlan,
    brandSettings.communityDecks, 
    dataLoaded
  ]);

  // --- ACTIONS ---

  const updateBrandSettings = (updates) => {
    setBrandSettings(prev => ({ ...prev, ...updates }));
  };

  const updateStrategy = (updates) => {
    setBrandSettings(prev => {
      const newStrategy = { ...prev.strategy, ...updates };
      let newCurrentBrandConfig = prev.currentBrandConfig;
      if (newCurrentBrandConfig) {
        newCurrentBrandConfig = {
          ...newCurrentBrandConfig,
          strategy: { ...(newCurrentBrandConfig.strategy || {}), ...updates }
        };
      }
      return { ...prev, strategy: newStrategy, currentBrandConfig: newCurrentBrandConfig };
    });
  };

  const updateCommunityDeck = (topic, slides) => {
    setBrandSettings(prev => ({
      ...prev,
      communityDecks: { ...(prev.communityDecks || {}), [topic]: slides }
    }));
  };

  const saveCurrentProfile = (nameOverride = null) => {
    if (!brandSettings.currentBrandConfig) return;
    const profileToSave = {
      ...brandSettings.currentBrandConfig,
      id: brandSettings.currentBrandConfig.id || Date.now(),
      name: nameOverride || brandSettings.currentBrandConfig.name || 'Mein Brand',
      lastModified: new Date().toISOString(),
      strategy: brandSettings.currentBrandConfig.strategy || brandSettings.strategy || DEFAULT_STRATEGY
    };

    setBrandSettings(prev => {
      const existingIndex = prev.brandConfigurations.findIndex(b => b.id === profileToSave.id);
      let newConfigs;
      if (existingIndex >= 0) {
        newConfigs = [...prev.brandConfigurations];
        newConfigs[existingIndex] = profileToSave;
      } else {
        newConfigs = [...prev.brandConfigurations, profileToSave];
      }
      return { ...prev, brandConfigurations: newConfigs, currentBrandConfig: profileToSave };
    });
  };

  const loadBrandProfile = (profileId) => {
    const profile = brandSettings.brandConfigurations.find(b => b.id === profileId);
    if (profile) {
      setBrandSettings(prev => ({
        ...prev,
        currentBrandConfig: profile,
        strategy: profile.strategy || prev.strategy
      }));
    }
  };

  const deleteBrandProfile = (profileId) => {
    // Curated brands are fixed and cannot be deleted.
    if (String(profileId).startsWith('curated_')) return;
    setBrandSettings(prev => ({
      ...prev,
      brandConfigurations: prev.brandConfigurations.filter(b => b.id !== profileId),
    }));
  };

  const saveDesignToLibrary = (slideData) => {
    const newDesign = { ...slideData, id: Date.now(), savedAt: new Date().toISOString() };
    setBrandSettings(prev => ({
      ...prev,
      savedDesigns: [newDesign, ...(prev.savedDesigns || [])]
    }));
  };

  const deleteDesignFromLibrary = (id) => {
    setBrandSettings(prev => ({
      ...prev,
      savedDesigns: (prev.savedDesigns || []).filter(d => d.id !== id)
    }));
  };

  const addCustomFont = async (name, arrayBuffer) => {
    try {
      const fontFace = new FontFace(name, arrayBuffer);
      await fontFace.load();
      document.fonts.add(fontFace);
      
      const newFont = { id: Date.now(), name: name, data: arrayBuffer, type: 'custom' };
      setBrandSettings(prev => ({
        ...prev,
        customFonts: [...(prev.customFonts || []), newFont]
      }));
      return true;
    } catch (e) {
      console.error("Error adding font", e);
      return false;
    }
  };

  const removeCustomFont = (id) => {
    setBrandSettings(prev => ({
      ...prev,
      customFonts: (prev.customFonts || []).filter(f => f.id !== id)
    }));
  };

  const updateFeedProfile = (updates) => {
    setBrandSettings(prev => ({
      ...prev,
      feedProfile: { ...prev.feedProfile, ...updates }
    }));
  };

  const addPostToFeed = (design) => {
    setBrandSettings(prev => ({
      ...prev,
      feedProfile: {
        ...prev.feedProfile,
        extraPosts: [...(prev.feedProfile.extraPosts || []), { ...design, id: Date.now(), isExtra: true }]
      }
    }));
  };

  const removePostFromFeed = (postId) => {
    setBrandSettings(prev => ({
      ...prev,
      feedProfile: {
        ...prev.feedProfile,
        extraPosts: (prev.feedProfile.extraPosts || []).filter(p => p.id !== postId)
      }
    }));
  };

  return (
    <BrandContext.Provider value={{
      brandSettings,
      dataLoaded,
      updateBrandSettings,
      updateStrategy,
      saveDesignToLibrary,
      deleteDesignFromLibrary,
      addCustomFont,
      removeCustomFont,
      saveCurrentProfile,
      loadBrandProfile,
      deleteBrandProfile,
      updateFeedProfile,
      addPostToFeed,
      removePostFromFeed,
      updateCommunityDeck
    }}>
      {children}
    </BrandContext.Provider>
  );
};