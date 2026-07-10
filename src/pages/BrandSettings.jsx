import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import Canvas from '../components/Canvas';
import { useBrand } from '../context/BrandContext';
import ColorPalette from '../components/ColorPalette';
import FontSelector from '../components/FontSelector';
import BrandRandomizer from '../components/BrandRandomizer';
import { uploadImageToCloud, listCloudImages, deleteCloudImage } from '../supabase';
import { CURATED_BRANDS } from '../constants/brandData';
import { parseBrandsheet } from '../utils/brandsheetParser';

const { FiShuffle, FiDroplet, FiType, FiImage, FiSettings, FiSave, FiUpload, FiEdit3, FiTrash2, FiCheckCircle, FiEye, FiTag, FiX, FiAlertCircle, FiUsers, FiCheck, FiRefreshCw, FiToggleRight, FiToggleLeft } = FiIcons;

const BrandSettings = () => {
  const { brandSettings, updateBrandSettings, addCustomFont, removeCustomFont, loadBrandProfile, deleteBrandProfile } = useBrand();
  const [activeSection, setActiveSection] = useState('identity');
  const [selectMode, setSelectMode] = useState(false);
  const [selectedImages, setSelectedImages] = useState([]);
  const [sheetText, setSheetText] = useState('');
  const [sheetStatus, setSheetStatus] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({ done: 0, total: 0, failed: 0 });
  const [uploadError, setUploadError] = useState('');

  // On mount: pull cloud images (cross-device) and merge with local pool.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const cloud = await listCloudImages();
      if (cancelled || !cloud.length) return;
      const existing = brandSettings.brandImages || [];
      // Keep only LOCAL (base64) images from the existing pool; the cloud list
      // is the single source of truth for cloud images. This prevents the same
      // cloud image being appended again on every mount/reload.
      const localOnly = existing.filter((img) => typeof img === 'string' && img.startsWith('data:'));
      // Dedupe cloud URLs too, just in case.
      const uniqueCloud = [...new Set(cloud)];
      const merged = [...localOnly, ...uniqueCloud];
      // Only write if something actually changed (avoid render loop).
      if (JSON.stringify(merged) !== JSON.stringify(existing)) {
        updateBrandSettings({ brandImages: merged });
      }
    })();
    return () => { cancelled = true; };
  }, []);

  const sections = [
    { id: 'identity', label: 'Meine Brands', icon: FiUsers },
    { id: 'randomizer', label: 'Generator', icon: FiShuffle },
    { id: 'colors', label: 'Farben', icon: FiDroplet },
    { id: 'fonts', label: 'Fonts', icon: FiType },
    { id: 'images', label: 'Bilder', icon: FiImage },
  ];

  const updateCurrentBrand = (field, value) => {
    if (!brandSettings.currentBrandConfig) return;
    const updatedConfig = { ...brandSettings.currentBrandConfig, [field]: value };

    // Cascade color/typography changes onto ALL existing posts so the
    // settings always win and Feed + Posts stay identical.
    const patch = { currentBrandConfig: updatedConfig };
    if (field === 'colors' || field === 'typography') {
      const c = updatedConfig.colors || {};
      const t = updatedConfig.typography || {};
      const applyToSlide = (s) => ({
        ...s,
        ...(field === 'colors' ? {
          color: c.primary,
          backgroundColor: c.background,
          secondaryColor: c.secondary,
          tertiaryColor: c.tertiary,
          neutralColor: c.neutral,
          accentColor: c.accent,
        } : {
          fontFamily: t.fontFamily,
          accentFontFamily: t.accentFontFamily,
        }),
      });
      if (Array.isArray(brandSettings.contentPlan)) {
        patch.contentPlan = brandSettings.contentPlan.map((day) => ({
          ...day,
          slides: (day.slides || []).map(applyToSlide),
        }));
      }
    }
    updateBrandSettings(patch);
  };

  const handleSave = () => {
    if (!brandSettings.currentBrandConfig) return;
    
    let configToSave = { ...brandSettings.currentBrandConfig };

    const savedConfigs = brandSettings.brandConfigurations || [];
    // Update or Add based on ID
    const index = savedConfigs.findIndex(c => c.id === configToSave.id);
    let newSavedConfigs;
    if (index >= 0) {
      newSavedConfigs = [...savedConfigs];
      newSavedConfigs[index] = configToSave;
    } else {
      newSavedConfigs = [...savedConfigs, configToSave];
    }

    updateBrandSettings({
      brandConfigurations: newSavedConfigs,
      currentBrandConfig: configToSave
    });
    setSuccessMessage('Einstellungen gespeichert!');
    setTimeout(() => setSuccessMessage(''), 3000);
  };

  // --- IMAGE UPLOAD HELPER ---
  const resizeImage = (file, maxWidth = 1000) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          let width = img.width;
          let height = img.height;
          if (width > maxWidth) {
            height = height * (maxWidth / width);
            width = maxWidth;
          }
          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);
          resolve(canvas.toDataURL('image/jpeg', 0.8));
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  };

  const handleImageUpload = async (event) => {
    const files = Array.from(event.target.files);
    if (!files.length) return;
    setIsUploading(true);
    setUploadError('');
    setUploadProgress({ done: 0, total: files.length, failed: 0 });
    try {
      let cloudCount = 0;
      let failed = 0;
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        // Cloud-only: no base64 fallback (prevents browser-memory overflow on
        // large batches). A failed upload is counted, not stored.
        const cloudUrl = await uploadImageToCloud(file);
        if (cloudUrl) {
          cloudCount++;
          // Save incrementally so a crash mid-batch never loses prior progress.
          const current = brandSettings.brandImages || [];
          updateBrandSettings({ brandImages: [...current, cloudUrl] });
        } else {
          failed++;
        }
        setUploadProgress({ done: i + 1, total: files.length, failed });
      }
      if (failed === 0) {
        setSuccessMessage(`${cloudCount} Bilder in der Cloud gespeichert.`);
      } else {
        setSuccessMessage(`${cloudCount} gespeichert, ${failed} fehlgeschlagen.`);
      }
      setTimeout(() => setSuccessMessage(''), 5000);
    } catch (error) {
      console.error("Upload error", error);
      setUploadError('Fehler beim Upload.');
    } finally {
      setIsUploading(false);
      event.target.value = '';
    }
  };

  // Delete several images at once (selection mode) or the whole pool.
  const removeImages = async (urls) => {
    if (!urls.length) return;
    const question = urls.length === 1
      ? 'Bild wirklich löschen?'
      : `${urls.length} Bilder wirklich löschen?`;
    if (!window.confirm(question)) return;

    const current = brandSettings.brandImages || [];
    const remaining = current.filter((u) => !urls.includes(u));
    // Clean up the meta and the CTA choice for deleted images.
    const meta = { ...(brandSettings.imageMeta || {}) };
    urls.forEach((u) => delete meta[u]);
    const cfg = brandSettings.currentBrandConfig || {};
    const ctaCleared = urls.includes(cfg.ctaImage) ? { ...cfg, ctaImage: null } : cfg;

    updateBrandSettings({ brandImages: remaining, imageMeta: meta, currentBrandConfig: ctaCleared });
    setSelectedImages([]);
    setSelectMode(false);
    setSuccessMessage(urls.length === 1 ? 'Bild gelöscht.' : `${urls.length} Bilder gelöscht.`);

    let failed = 0;
    for (const u of urls) {
      try { const ok = await deleteCloudImage(u); if (!ok) failed++; }
      catch (e) { failed++; console.error(e); }
    }
    if (failed) setUploadError(`${failed} Bild(er) lokal entfernt, aber Cloud-Löschen fehlgeschlagen.`);
  };

  const removeImage = async (indexToRemove) => {
    if(!window.confirm("Bild wirklich löschen?")) return;
    const currentImages = brandSettings.brandImages || [];
    const imgToRemove = currentImages[indexToRemove];
    // Remove from local pool first (instant feedback)
    const updatedImages = currentImages.filter((_, index) => index !== indexToRemove);
    updateBrandSettings({ brandImages: updatedImages });
    setSuccessMessage("Bild gelöscht.");
    // Also delete from cloud so it doesn't reappear on next load
    try {
      const ok = await deleteCloudImage(imgToRemove);
      if (!ok) setUploadError('Bild lokal entfernt, aber Cloud-Löschen fehlgeschlagen.');
    } catch (e) {
      console.error(e);
    }
    setTimeout(() => setSuccessMessage(''), 2000);
  };

  // --- FONT UPLOAD HELPER ---
  const handleFontUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['otf', 'ttf', 'woff', 'woff2'].includes(ext)) {
      setUploadError('Bitte nur .otf oder .ttf Dateien hochladen.');
      return;
    }
    setIsUploading(true);
    setUploadError('');
    try {
      const arrayBuffer = await file.arrayBuffer();
      const fontName = file.name.replace(/\.[^/.]+$/, "").replace(/[^a-zA-Z0-9\s-_]/g, "");
      const success = await addCustomFont(fontName, arrayBuffer);
      if (success) {
        setSuccessMessage(`Schriftart "${fontName}" erfolgreich installiert!`);
        if (brandSettings.currentBrandConfig) {
          updateCurrentBrand('typography', { ...brandSettings.currentBrandConfig.typography, fontFamily: fontName });
        }
      } else {
        setUploadError('Fehler beim Laden der Schriftart.');
      }
    } catch (e) {
      console.error(e);
      setUploadError('Datei konnte nicht gelesen werden.');
    } finally {
      setIsUploading(false);
      event.target.value = '';
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  }

  // UPDATED LIVE PREVIEW COMPONENT USING CANVAS
  const BrandPreview = ({ config }) => {
    if (!config || !config.colors || !config.typography) return null;

    // Create a data object that mimics a slide to show the mixed fonts
    // We use sampleText or a fallback that includes asterisks for accent testing
    const previewText = config.sampleText || `Welcome to *${config.name}*`;

    // Ensure accent font is properly defaulted if missing
    const safeAccentFont = config.typography.accentFontFamily || config.typography.fontFamily;

    const canvasData = {
      text: previewText,
      // Pass both font families to enable mixing
      fontFamily: config.typography.fontFamily,
      accentFontFamily: safeAccentFont, // Force safe accent font
      fontWeight: config.typography.fontWeight,
      fontSize: 48,
      color: config.colors.primary,
      backgroundColor: config.colors.background,
      secondaryColor: config.colors.secondary,
      accentColor: config.colors.accent,
      layout: 'minimal_quote', // Clean layout for preview
      textAlign: 'center',
      visualElements: config.visualElements || [],
      format: '16:9' // Wide preview for settings header
    };

    // FORCE UNIQUE KEY TO TRIGGER RE-RENDER ON ANY CHANGE (including Accent Color/Font)
    const uniqueKey = `${config.colors.primary}-${config.colors.accent}-${config.typography.fontFamily}-${safeAccentFont}-${config.typography.bodyFontFamily}-${Date.now()}`;

    return (
      <div className="mb-8 border border-gray-200 rounded-xl overflow-hidden shadow-sm bg-gray-50">
        <div className="p-3 border-b border-gray-100 bg-white flex justify-between items-center">
            <div className="flex items-center text-xs font-bold text-gray-500 uppercase tracking-wider">
                <SafeIcon icon={FiEye} className="mr-2" /> Live Preview (Accent Test)
            </div>
        </div>
        <div className="relative w-full aspect-[16/9] md:aspect-[3/1] max-h-64">
          {/* KEY IS CRITICAL FOR REFRESH */}
          <Canvas key={uniqueKey} data={canvasData} width={800} height={450} brandName={config.name} />
        </div>
      </div>
    );
  };


  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-6 pb-24">
      {/* Mobile-First Navigation */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-6 overflow-x-auto p-1 sticky top-16 z-20">
        <div className="flex space-x-1 min-w-max">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeSection === section.id
                ? 'bg-purple-600 text-white'
                : 'text-gray-600 hover:bg-gray-50'
                }`}
            >
              <SafeIcon icon={section.icon} />
              <span>{section.label}</span>
            </button>
          ))}
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="bg-white rounded-xl p-5 sm:p-8 shadow-lg border border-gray-100"
      >
        {!brandSettings.currentBrandConfig && activeSection !== 'randomizer' && activeSection !== 'identity' && (
          <div className="bg-amber-50 text-amber-800 p-4 mb-6 rounded-lg text-sm">
            Bitte erst eine Brand auswählen oder erstellen.
          </div>
        )}

        {/* ALWAYS SHOW PREVIEW IF CONFIG EXISTS (Except Randomizer/Images/Prompt) */}
        {brandSettings.currentBrandConfig && activeSection !== 'randomizer' && activeSection !== 'images' && activeSection !== 'identity' && (
          <BrandPreview config={brandSettings.currentBrandConfig} />
        )}

        {/* --- IDENTITY / MY BRANDS SECTION --- */}
        {activeSection === 'identity' && (
          <div className="space-y-8">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-900">Meine Gespeicherten Brands</h3>
            </div>

            {/* Carousel settings: brand mark + fixed CTA photo */}
            <div className="mb-6 border border-gray-200 rounded-xl p-4 bg-white">
              <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Karussell</div>

              <div className="mb-4 pb-4 border-b border-gray-100">
                <div className="text-sm font-bold text-gray-900 mb-1">Brand-Zeile</div>
                <div className="text-[11px] text-gray-500 mb-2">Erscheint klein am unteren Rand jedes Posts. Leer lassen für keine Zeile.</div>
                <input
                  type="text"
                  value={brandSettings.currentBrandConfig?.brandText ?? ''}
                  onChange={(e) => updateBrandSettings({ currentBrandConfig: { ...(brandSettings.currentBrandConfig || {}), brandText: e.target.value } })}
                  placeholder="z. B. deinname.at"
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-purple-400"
                />
              </div>

              <div>
                <div className="text-sm font-bold text-gray-900 mb-1">Foto für den Call-to-Action</div>
                <div className="text-[11px] text-gray-500 mb-2">Wird immer auf der letzten Slide verwendet.</div>
                {brandSettings.currentBrandConfig?.ctaImage ? (
                  <div className="flex items-center gap-3">
                    <img src={brandSettings.currentBrandConfig.ctaImage} alt="CTA" className="w-16 h-20 object-cover rounded-lg border border-gray-200" />
                    <button onClick={() => updateBrandSettings({ currentBrandConfig: { ...brandSettings.currentBrandConfig, ctaImage: null } })} className="text-xs font-bold text-red-600 hover:underline">Entfernen</button>
                  </div>
                ) : (
                  <p className="text-[11px] text-gray-400">Kein Foto gewählt — unten in der Galerie auf „Als CTA-Foto" tippen.</p>
                )}
              </div>
              <p className="text-[11px] text-gray-400 mt-3 pt-3 border-t border-gray-100">
                Den Unschärfe-Modus für Folgeseiten stellst du pro Post ein — im Content Plan auf der jeweiligen Kachel.
              </p>
            </div>

            {/* Brandsheet Import: paste a brand sheet, get a full brand */}
            <div className="mb-6 border border-dashed border-gray-300 rounded-xl p-4 bg-gray-50/50">
              <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Brandsheet Import</div>
              <textarea
                value={sheetText}
                onChange={(e) => setSheetText(e.target.value)}
                placeholder={"BRANDSHEET — Name\n\nFARBEN\n#F4F2EF Hintergrund\n#3D3D3B Text\n...\n\nTYPOGRAFIE\nHeadline: Schriftname ...\nFließtext: Schriftname ...\nAkzent: Schriftname ..."}
                className="w-full h-32 border border-gray-200 rounded-lg p-3 text-xs font-mono bg-white outline-none focus:border-purple-400 resize-y"
              />
              <div className="flex items-center justify-between mt-2">
                <p className="text-[11px] text-gray-400">Fügt dein Brandsheet ein — Farben (Hex + Rolle), Schriften und Name werden automatisch erkannt.</p>
                <button
                  onClick={async () => {
                    const r = parseBrandsheet(sheetText);
                    if (!r.ok) { setSheetStatus(r.error); return; }
                    setSheetStatus('Lade Schriften…');
                    const { loadGoogleFonts } = await import('../utils/fontLoader');
                    await loadGoogleFonts([
                      r.config.typography.fontFamily,
                      r.config.typography.bodyFontFamily,
                      r.config.typography.accentFontFamily,
                    ]);
                    updateBrandSettings({
                      currentBrandConfig: r.config,
                      brandConfigurations: [r.config, ...(brandSettings.brandConfigurations || [])],
                    });
                    setSheetStatus(`✓ „${r.config.name}" erstellt und aktiviert (Schriften live geladen).`);
                    setSheetText('');
                    setTimeout(() => setSheetStatus(''), 5000);
                  }}
                  disabled={!sheetText.trim()}
                  className="px-4 py-2 rounded-lg bg-purple-600 text-white text-xs font-bold hover:bg-purple-700 disabled:opacity-40 shrink-0 ml-3"
                >Brand erstellen</button>
              </div>
              {sheetStatus && <p className="text-xs mt-2 font-bold text-gray-700">{sheetStatus}</p>}
            </div>

            {/* Fixed curated brands — always available */}
            <div className="mb-4">
              <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Kuratierte Brands</div>
              <div className="grid gap-3">
                {CURATED_BRANDS.map(config => {
                  const isActive = brandSettings.currentBrandConfig?.id === config.id;
                  return (
                    <div key={config.id} className={`border rounded-xl p-4 flex items-center justify-between transition-all ${isActive ? 'border-purple-500 bg-purple-50 ring-1 ring-purple-200' : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'}`}>
                      <div className="flex items-center space-x-4">
                        <div className="flex -space-x-2">
                          {Object.values(config.colors || {}).slice(0, 3).map((c, i) => (
                            <div key={i} className="w-8 h-8 rounded-full border-2 border-white shadow-sm" style={{ backgroundColor: c }} />
                          ))}
                        </div>
                        <div>
                          <h4 className="font-bold text-gray-900">{config.name}</h4>
                          <p className="text-xs text-gray-500">Playfair + Handschrift • {config.darkPhoto ? 'dunkle Fotos' : 'helle Fotos'}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {!isActive && (
                          <button onClick={() => updateBrandSettings({ currentBrandConfig: { ...config, id: config.id } })} className="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs font-bold text-gray-700 hover:bg-gray-100">
                            Laden
                          </button>
                        )}
                        {isActive && <span className="text-xs font-bold text-purple-600 px-2">Aktiv</span>}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* List of Saved Brands */}
            <div className="grid gap-4">
              {brandSettings.brandConfigurations && brandSettings.brandConfigurations.length > 0 ? (
                brandSettings.brandConfigurations.map(config => (
                  <div key={config.id} className={`border rounded-xl p-4 flex items-center justify-between transition-all ${brandSettings.currentBrandConfig?.id === config.id ? 'border-purple-500 bg-purple-50 ring-1 ring-purple-200' : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'}`}>
                    <div className="flex items-center space-x-4">
                      <div className="flex -space-x-2">
                        {Object.values(config.colors || {}).slice(0, 3).map((c, i) => (
                          <div key={i} className="w-8 h-8 rounded-full border-2 border-white shadow-sm" style={{ backgroundColor: c }} />
                        ))}
                      </div>
                      <div>
                        <h4 className="font-bold text-gray-900">{config.name}</h4>
                        <p className="text-xs text-gray-500">
                          {config.strategy?.industry || 'Keine Strategie'} • {config.ruleSet || 'Custom'}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                       {brandSettings.currentBrandConfig?.id !== config.id && (
                         <button onClick={() => loadBrandProfile(config.id)} className="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs font-bold text-gray-700 hover:bg-gray-100">
                           Laden
                         </button>
                       )}
                       {brandSettings.currentBrandConfig?.id === config.id && (
                          <span className="px-3 py-1.5 bg-purple-100 text-purple-700 rounded-lg text-xs font-bold flex items-center">
                            <SafeIcon icon={FiCheck} className="mr-1"/> Aktiv
                          </span>
                       )}
                       <button onClick={() => {if(window.confirm("Brand wirklich löschen?")) deleteBrandProfile(config.id)}} className="p-2 text-gray-400 hover:text-red-500 transition-colors" title="Löschen">
                          <SafeIcon icon={FiTrash2} />
                       </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 bg-gray-50 rounded-xl border border-dashed border-gray-200 text-gray-500">
                  Du hast noch keine Brands gespeichert.
                </div>
              )}
            </div>

            {brandSettings.currentBrandConfig && (
              <div className="mt-8 pt-8 border-t border-gray-100 animate-fade-in">
                  <h4 className="font-bold text-gray-900 mb-4">Aktive Brand bearbeiten</h4>
                  <div className="space-y-4">
                      <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Brand Name</label>
                          <input type="text" value={brandSettings.currentBrandConfig.name || ''} onChange={(e) => updateCurrentBrand('name', e.target.value)} className="w-full p-3 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-purple-500 focus:bg-white transition-colors" />
                      </div>
                      <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
                          <input type="text" value={brandSettings.currentBrandConfig.website || ''} onChange={(e) => updateCurrentBrand('website', e.target.value)} className="w-full p-3 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-purple-500 focus:bg-white transition-colors" />
                      </div>
                  </div>
              </div>
            )}
          </div>
        )}

        {/* Randomizer */}
        {activeSection === 'randomizer' && (
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Brand Generator</h3>
            <BrandRandomizer />
          </div>
        )}

        {/* Colors */}
        {activeSection === 'colors' && brandSettings.currentBrandConfig && (
          <div className="space-y-6">
            <h3 className="text-xl font-bold text-gray-900">Colors</h3>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Primary Color (Text)</label>
              <ColorPalette
                selectedColor={brandSettings.currentBrandConfig.colors.primary}
                onColorSelect={(c) => updateCurrentBrand('colors', { ...brandSettings.currentBrandConfig.colors, primary: c })}
              />
            </div>
            <div className="border-t border-gray-100 pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Background Color</label>
              <ColorPalette
                selectedColor={brandSettings.currentBrandConfig.colors.background}
                onColorSelect={(c) => updateCurrentBrand('colors', { ...brandSettings.currentBrandConfig.colors, background: c })}
              />
            </div>
            <div className="border-t border-gray-100 pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Accent Color</label>
              <ColorPalette
                selectedColor={brandSettings.currentBrandConfig.colors.accent}
                onColorSelect={(c) => updateCurrentBrand('colors', { ...brandSettings.currentBrandConfig.colors, accent: c })}
              />
            </div>
            <div className="border-t border-gray-100 pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Secondary Color</label>
              <ColorPalette
                selectedColor={brandSettings.currentBrandConfig.colors.secondary}
                onColorSelect={(c) => updateCurrentBrand('colors', { ...brandSettings.currentBrandConfig.colors, secondary: c })}
              />
            </div>
            <div className="border-t border-gray-100 pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Tertiary Color (oft Cognac / Zwischenton)</label>
              <ColorPalette
                selectedColor={brandSettings.currentBrandConfig.colors.tertiary}
                onColorSelect={(c) => updateCurrentBrand('colors', { ...brandSettings.currentBrandConfig.colors, tertiary: c })}
              />
            </div>
            <div className="border-t border-gray-100 pt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Neutral Color (heller Hilfston)</label>
              <ColorPalette
                selectedColor={brandSettings.currentBrandConfig.colors.neutral}
                onColorSelect={(c) => updateCurrentBrand('colors', { ...brandSettings.currentBrandConfig.colors, neutral: c })}
              />
            </div>
          </div>
        )}

        {/* Fonts */}
        {activeSection === 'fonts' && brandSettings.currentBrandConfig && (
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Typography</h3>

            {/* HEADLINE FONT */}
            <div className="mb-8">
              <h4 className="text-sm font-bold text-purple-700 uppercase mb-3 flex items-center">
                <SafeIcon icon={FiType} className="mr-2"/> Headline Font (Slide 1)
              </h4>
              <FontSelector
                selectedFont={brandSettings.currentBrandConfig.typography.fontFamily}
                onFontSelect={(f) => {
                  const isPlayfair = f.includes('Playfair');
                  updateCurrentBrand('typography', { ...brandSettings.currentBrandConfig.typography, fontFamily: f, fontWeight: isPlayfair ? '400' : (brandSettings.currentBrandConfig.typography.fontWeight || '400') })
                }}
              />
            </div>
            
            {/* ACCENT FONT (NEW SETTING) */}
            <div className="mb-8 pt-6 border-t border-gray-100">
              <h4 className="text-sm font-bold text-purple-600 uppercase mb-3 flex items-center">
                <SafeIcon icon={FiType} className="mr-2"/> Accent Font (Zweitschrift)
              </h4>
               <p className="text-xs text-gray-400 mb-3 bg-purple-50 text-purple-700 p-3 rounded-lg border border-purple-100">
                Diese Schrift wird für <strong>*hervorgehobene*</strong> Wörter und Zahlen verwendet.
              </p>
              <FontSelector
                selectedFont={brandSettings.currentBrandConfig.typography.accentFontFamily || brandSettings.currentBrandConfig.typography.fontFamily}
                onFontSelect={(f) => {
                  updateCurrentBrand('typography', { ...brandSettings.currentBrandConfig.typography, accentFontFamily: f });
                }}
              />
            </div>

            {/* BODY FONT (NEW SETTING) */}
            <div className="mb-8 pt-6 border-t border-gray-100">
              <h4 className="text-sm font-bold text-gray-500 uppercase mb-3 flex items-center">
                <SafeIcon icon={FiType} className="mr-2"/> Body Font (ab Slide 2)
              </h4>
              <p className="text-xs text-gray-400 mb-3">Diese Schriftart wird automatisch für alle Slides nach dem Titelblatt verwendet.</p>
              <FontSelector
                selectedFont={brandSettings.currentBrandConfig.typography.bodyFontFamily || 'Montserrat'}
                onFontSelect={(f) => {
                  updateCurrentBrand('typography', { ...brandSettings.currentBrandConfig.typography, bodyFontFamily: f });
                }}
              />
            </div>

            {/* CUSTOM FONT UPLOAD */}
            <div className="mt-8 bg-gray-50 border-2 border-dashed border-gray-200 rounded-xl p-6 text-center hover:bg-gray-100 hover:border-purple-300 transition-all">
              <SafeIcon icon={FiUpload} className="text-3xl text-purple-600 mx-auto mb-2"/>
              <h4 className="font-bold text-gray-900 mb-1">Eigene Schriftart hochladen</h4>
              <p className="text-xs text-gray-500 mb-4">Unterstützt: .otf, .ttf (Max 5MB)</p>
              <label className="inline-block cursor-pointer bg-white border border-gray-300 text-gray-700 px-6 py-2.5 rounded-lg font-bold shadow-sm hover:bg-purple-50 hover:text-purple-700 hover:border-purple-200 transition-all">
                Datei auswählen
                <input type="file" accept=".otf,.ttf,.woff,.woff2" onChange={handleFontUpload} className="hidden" />
              </label>
              <div className="mt-2 min-h-[20px]">
                {isUploading && <span className="text-xs text-purple-600 font-bold animate-pulse">Lade hoch… {uploadProgress.done}/{uploadProgress.total}{uploadProgress.failed > 0 ? ` (${uploadProgress.failed} fehlgeschlagen)` : ''}</span>}
                {uploadError && <span className="text-xs text-red-500 font-bold">{uploadError}</span>}
                {successMessage && <span className="text-xs text-green-600 font-bold">{successMessage}</span>}
              </div>
            </div>
            
            {/* List of Custom Fonts */}
            {brandSettings.customFonts && brandSettings.customFonts.length > 0 && (
              <div className="mt-6">
                <h4 className="text-sm font-bold text-gray-500 uppercase mb-3">Deine Uploads</h4>
                <div className="grid grid-cols-2 gap-3">
                  {brandSettings.customFonts.map(font => (
                    <div key={font.id} className="bg-white border border-gray-200 p-3 rounded-lg flex justify-between items-center shadow-sm">
                      <span style={{ fontFamily: font.name }} className="text-lg text-gray-900 truncate mr-2">{font.name}</span>
                      <button onClick={() => {if(window.confirm(`Font "${font.name}" löschen?`)) removeCustomFont(font.id)}} className="text-gray-400 hover:text-red-500 p-1 flex-shrink-0">
                        <SafeIcon icon={FiX} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Images */}
        {activeSection === 'images' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-bold text-gray-900">Brand Assets</h3>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const imgs = brandSettings.brandImages || [];
                    const unique = [...new Set(imgs)];
                    if (unique.length !== imgs.length) {
                      updateBrandSettings({ brandImages: unique });
                      setSuccessMessage(`${imgs.length - unique.length} Duplikate entfernt.`);
                    } else {
                      setSuccessMessage('Keine Duplikate gefunden.');
                    }
                    setTimeout(() => setSuccessMessage(''), 3000);
                  }}
                  className="text-xs px-2 py-1 rounded border border-gray-200 text-gray-600 hover:bg-gray-50"
                  title="Doppelte Bilder entfernen"
                >
                  Duplikate entfernen
                </button>
                <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                  {(brandSettings.brandImages || []).length} / 20
                </span>
              </div>
            </div>
            {(brandSettings.brandImages || []).length > 0 && (
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <button
                  onClick={() => { setSelectMode(!selectMode); setSelectedImages([]); }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${selectMode ? 'bg-purple-600 text-white border-purple-600' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}`}
                >
                  {selectMode ? 'Auswahl beenden' : 'Auswählen'}
                </button>

                {selectMode && (
                  <>
                    <button
                      onClick={() => {
                        const all = brandSettings.brandImages || [];
                        setSelectedImages(selectedImages.length === all.length ? [] : [...all]);
                      }}
                      className="px-3 py-1.5 rounded-lg text-xs font-bold bg-white text-gray-700 border border-gray-200 hover:bg-gray-50"
                    >
                      {selectedImages.length === (brandSettings.brandImages || []).length ? 'Keine' : 'Alle'}
                    </button>
                    <button
                      onClick={() => removeImages(selectedImages)}
                      disabled={selectedImages.length === 0}
                      className="px-3 py-1.5 rounded-lg text-xs font-bold bg-red-600 text-white hover:bg-red-700 disabled:opacity-40"
                    >
                      {selectedImages.length > 0 ? `${selectedImages.length} löschen` : 'Löschen'}
                    </button>
                  </>
                )}

                {!selectMode && (
                  <button
                    onClick={() => removeImages([...(brandSettings.brandImages || [])])}
                    className="px-3 py-1.5 rounded-lg text-xs font-bold bg-white text-red-600 border border-red-200 hover:bg-red-50 ml-auto"
                  >
                    Alle löschen
                  </button>
                )}
              </div>
            )}
            <div className="grid grid-cols-2 gap-4">
              <label className={`aspect-square border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:bg-gray-50 transition-colors ${isUploading ? 'opacity-50' : ''}`}>
                {isUploading ? <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div> : <SafeIcon icon={FiUpload} className="text-2xl text-purple-500 mb-2" />}
                <span className="text-xs font-bold text-gray-500">Upload New</span>
                <input type="file" accept="image/*" multiple onChange={handleImageUpload} disabled={isUploading} className="hidden" />
              </label>

              {brandSettings.brandImages && brandSettings.brandImages.map((img, index) => {
                const meta = (brandSettings.imageMeta || {})[img] || {};
                const isOff = meta.disabled === true;
                const prio = typeof meta.priority === 'number' ? meta.priority : 1;
                const setMeta = (patch) => {
                  const next = { ...(brandSettings.imageMeta || {}), [img]: { ...meta, ...patch } };
                  updateBrandSettings({ imageMeta: next });
                };
                const prioLabel = prio === 2 ? 'Hoch' : prio === 0 ? 'Niedrig' : 'Normal';
                const prioClass = prio === 2 ? 'bg-amber-500 text-white' : prio === 0 ? 'bg-gray-300 text-gray-600' : 'bg-white/90 text-gray-700';
                const isSelected = selectedImages.includes(img);
                const toggleSelect = () => setSelectedImages(isSelected ? selectedImages.filter((u) => u !== img) : [...selectedImages, img]);
                return (
                <div key={index} className={`relative group rounded-xl overflow-hidden shadow-sm border bg-white ${isSelected ? 'border-purple-600 ring-2 ring-purple-300' : isOff ? 'border-gray-300 opacity-60' : 'border-gray-200'}`}>
                    <div className="aspect-square w-full relative">
                        <img src={img} alt="Asset" className={`w-full h-full object-cover ${isOff ? 'grayscale' : ''}`} />

                        {/* Selection mode: whole tile toggles selection */}
                        {selectMode && (
                          <button
                            onClick={(e) => { e.preventDefault(); toggleSelect(); }}
                            className={`absolute inset-0 z-20 flex items-start justify-end p-2 transition-colors ${isSelected ? 'bg-purple-600/25' : 'bg-black/0 hover:bg-black/10'}`}
                            aria-label={isSelected ? 'Abwählen' : 'Auswählen'}
                          >
                            <span className={`w-6 h-6 rounded-full flex items-center justify-center border-2 shadow ${isSelected ? 'bg-purple-600 border-white' : 'bg-white/80 border-white'}`}>
                              {isSelected && <SafeIcon icon={FiCheck} className="text-white text-xs" />}
                            </span>
                          </button>
                        )}

                        {/* Priority badge (tap to cycle Hoch -> Niedrig -> Normal) */}
                        <button
                          onClick={(e) => { e.preventDefault(); setMeta({ priority: prio === 2 ? 0 : prio === 0 ? 1 : 2 }); }}
                          className={`absolute top-1.5 left-1.5 text-[10px] font-bold px-2 py-0.5 rounded-full shadow ${prioClass}`}
                          title="Priorität ändern"
                        >{prioLabel}</button>
                        {isOff && (
                          <div className="absolute inset-0 flex items-center justify-center">
                            <span className="bg-black/60 text-white text-[10px] font-bold px-2 py-1 rounded">Inaktiv</span>
                          </div>
                        )}
                        {brandSettings.currentBrandConfig?.ctaImage === img && (
                          <span className="absolute top-1.5 right-1.5 bg-emerald-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full shadow">CTA</span>
                        )}
                    </div>
                    <button
                      onClick={(e) => { e.preventDefault(); updateBrandSettings({ currentBrandConfig: { ...(brandSettings.currentBrandConfig || {}), ctaImage: brandSettings.currentBrandConfig?.ctaImage === img ? null : img } }); }}
                      className={`w-full py-1.5 text-[10px] font-bold border-t border-gray-100 transition-colors ${brandSettings.currentBrandConfig?.ctaImage === img ? 'bg-emerald-50 text-emerald-700' : 'bg-white text-gray-500 hover:bg-gray-50'}`}
                    >
                      {brandSettings.currentBrandConfig?.ctaImage === img ? 'CTA-Foto ✓' : 'Als CTA-Foto'}
                    </button>
                    <div className="flex border-t border-gray-100">
                      <button onClick={(e) => { e.preventDefault(); setMeta({ disabled: !isOff }); }} className={`flex-1 py-2 text-xs font-bold flex items-center justify-center transition-colors ${isOff ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100' : 'bg-gray-50 text-gray-600 hover:bg-gray-100'}`}>
                        {isOff ? 'Aktivieren' : 'Deaktivieren'}
                      </button>
                      <button onClick={(e) => {e.preventDefault(); removeImage(index)}} className="flex-1 py-2 bg-red-50 text-red-600 text-xs font-bold hover:bg-red-100 flex items-center justify-center border-l border-red-100 transition-colors">
                        <SafeIcon icon={FiTrash2} className="mr-1" /> Löschen
                      </button>
                    </div>
                </div>
              );})}
            </div>
          </div>
        )}

        <div className="sticky bottom-0 bg-white border-t border-gray-200 p-4 -mx-5 -mb-5 sm:-mx-8 sm:-mb-8 mt-8 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] z-10">
          {successMessage && activeSection !== 'images' && (
            <div className="mb-2 text-center text-sm text-green-600 font-bold flex items-center justify-center">
              <SafeIcon icon={FiCheckCircle} className="mr-2" />
              {successMessage}
            </div>
          )}
          <button
            onClick={handleSave}
            className="w-full bg-gray-900 text-white py-3.5 rounded-xl font-bold hover:bg-black shadow-lg transition-transform active:scale-[0.98] flex items-center justify-center"
          >
            <SafeIcon icon={FiSave} className="mr-2" /> Einstellungen Speichern
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default BrandSettings;