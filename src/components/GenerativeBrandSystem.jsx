import React, { useState, useEffect } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import { generateMixedBrand } from '../constants/brandData';
import Canvas from './Canvas';

// IMPORT CANVAS FOR LIVE PREVIEW
const { FiRefreshCw, FiZap, FiSave, FiCheckCircle, FiPlus } = FiIcons;

const GenerativeBrandSystem = ({ compact = false, onGenerate }) => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const [currentBrandConfig, setCurrentBrandConfig] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState('');

  // --- SYNC FIX: Listen to Global Changes (e.g. from StyleShifter) ---
  useEffect(() => {
    if (brandSettings.currentBrandConfig) {
      // Wenn sich die globale Config ändert (z.B. durch StyleShifter),
      // aktualisieren wir die lokale Vorschau.
      setCurrentBrandConfig(brandSettings.currentBrandConfig);
    }
  }, [brandSettings.currentBrandConfig]);

  // ZUFALLSGENERATOR (Echt Random)
  const generateNewIdentity = () => {
    setIsGenerating(true);
    setSaveSuccess('');
    
    // Simulate thinking time for effect
    setTimeout(() => {
      const newConfig = generateMixedBrand();
      setCurrentBrandConfig(newConfig);
      setIsGenerating(false);
      
      if (onGenerate) {
        onGenerate(newConfig);
      }
    }, 400);
  };

  const handleSaveToMyBrands = () => {
    if (!currentBrandConfig) return;
    
    // Save to context list
    // Create a new config with a guaranteed unique ID to prevent overwrites if generated multiple times
    const configToSave = {
      ...currentBrandConfig,
      id: Date.now(),
      // Ensure strategy is preserved or defaulted
      strategy: brandSettings.strategy || brandSettings.currentBrandConfig?.strategy || {}
    };

    // Explicitly add to list without forcing it as "current" if we just want to save it
    // But typically user wants to "Adopt" it eventually. 
    // For now, let's just save it to the list.
    const currentList = brandSettings.brandConfigurations || [];
    
    // Check if duplicate ID exists (unlikely with Date.now())
    const newList = [configToSave, ...currentList];
    
    updateBrandSettings({ 
      brandConfigurations: newList,
      // Also set it as current so the user can continue editing/using it immediately
      currentBrandConfig: configToSave
    });

    setSaveSuccess('In "Meine Brands" gespeichert!');
    setTimeout(() => setSaveSuccess(''), 3000);
  };

  const renderPreview = (config) => {
    // CONSTRUCT DATA FOR CANVAS TO SHOW MIXED FONTS
    const canvasData = {
      text: config.sampleText || "YOUR *BRAND*",
      fontFamily: config.typography.fontFamily,
      accentFontFamily: config.typography.accentFontFamily, // Critical for mixed font view
      fontWeight: config.typography.fontWeight,
      fontSize: 38,
      color: config.colors.primary,
      backgroundColor: config.colors.background,
      secondaryColor: config.colors.secondary,
      accentColor: config.colors.accent,
      layout: 'minimal_quote',
      textAlign: 'center',
      visualElements: [],
      format: '16:9'
    };

    return (
      <div className="w-full h-56 rounded-xl overflow-hidden relative bg-white border border-gray-200 shadow-sm transition-all duration-500 group">
        <div className="absolute inset-0">
          {/* CANVAS RENDERING FOR REAL PREVIEW */}
          {/* Key ensures re-render on deep changes */}
          <Canvas 
            key={`${config.colors.primary}-${config.typography.fontFamily}-${config.typography.accentFontFamily}`}
            data={canvasData} 
            width={600} 
            height={337} 
            brandName={config.name} 
          />
        </div>
      </div>
    );
  };

  // Auto-init only if empty
  useEffect(() => {
    if (!currentBrandConfig && !brandSettings.currentBrandConfig) {
       // Don't auto-generate immediately to let user click the button
    } else if (brandSettings.currentBrandConfig && !currentBrandConfig) {
       setCurrentBrandConfig(brandSettings.currentBrandConfig);
    }
  }, []);

  if (compact) {
    return (
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-bold text-gray-900">AI Randomizer</h3>
          <div className="flex space-x-2">
            <button 
              onClick={generateNewIdentity} 
              disabled={isGenerating}
              className={`p-2 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 transition-colors ${isGenerating ? 'animate-pulse' : ''}`}
              title="Neu Generieren"
            >
              <SafeIcon icon={FiZap} />
            </button>
          </div>
        </div>
        <p className="text-xs text-gray-500 mb-2">Erstellt eine komplett neue Kombination.</p>
        
        {currentBrandConfig && (
          <div className="mt-2 text-xs border border-gray-100 rounded p-2 bg-gray-50 flex justify-between items-center">
             <span className="font-bold truncate max-w-[120px]">{currentBrandConfig.name}</span>
             <button onClick={handleSaveToMyBrands} className="text-purple-600 hover:text-purple-800 flex items-center" title="In Liste speichern">
               <SafeIcon icon={saveSuccess ? FiCheckCircle : FiPlus} className="mr-1"/> {saveSuccess ? 'Saved' : 'Save'}
             </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row gap-8 items-center justify-center py-8">
      {/* CONTROLS */}
      <div className="w-full md:w-1/3 text-center md:text-left space-y-6">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2 flex items-center justify-center md:justify-start">
            <span className="bg-purple-100 text-purple-700 p-2 rounded-lg mr-3"><SafeIcon icon={FiZap} /></span>
            Identity Generator
          </h3>
          <p className="text-gray-600">
            Klicke auf den Button, um eine einzigartige Brand-Identität aus tausenden Kombinationen zu generieren.
          </p>
        </div>

        <button 
          onClick={generateNewIdentity} 
          disabled={isGenerating}
          className="w-full py-4 bg-gray-900 text-white rounded-xl font-bold text-lg shadow-lg hover:bg-black hover:scale-[1.02] transition-all flex items-center justify-center"
        >
          <SafeIcon icon={FiRefreshCw} className={`mr-3 text-xl ${isGenerating ? 'animate-spin' : ''}`} />
          {isGenerating ? 'Designing...' : 'Generate New Identity'}
        </button>

        {currentBrandConfig && (
          <button 
            onClick={handleSaveToMyBrands}
            className={`w-full py-3 rounded-xl font-bold flex items-center justify-center transition-all ${saveSuccess ? 'bg-green-100 text-green-700 border border-green-200' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'}`}
          >
            <SafeIcon icon={saveSuccess ? FiCheckCircle : FiSave} className="mr-2" />
            {saveSuccess ? 'Gespeichert!' : 'In "Meine Brands" speichern'}
          </button>
        )}
        
        {saveSuccess && (
          <div className="text-xs text-green-600 font-bold text-center bg-green-50 p-2 rounded">
            Brand wurde gespeichert und aktiviert!
          </div>
        )}

        <div className="text-xs text-gray-400 text-center">
          Kombiniert zufällig Farben, Schriften & Layouts.
        </div>
      </div>

      {/* PREVIEW AREA */}
      <div className="w-full md:w-2/3">
        {currentBrandConfig ? (
          <div className="animate-fade-in">
            {renderPreview(currentBrandConfig)}
            
            <div className="flex gap-4 mt-4">
              <div className="flex-1 bg-white p-3 rounded-lg border border-gray-200 text-xs">
                <span className="block font-bold text-gray-500 uppercase mb-1">Font</span>
                {currentBrandConfig.typography.fontFamily} <span className="text-gray-400"> + {currentBrandConfig.typography.accentFontFamily}</span>
              </div>
              <div className="flex-1 bg-white p-3 rounded-lg border border-gray-200 text-xs">
                <span className="block font-bold text-gray-500 uppercase mb-1">Colors</span>
                {currentBrandConfig.generatedDetails?.colorName || 'Custom Mix'}
              </div>
            </div>
          </div>
        ) : (
          <div className="w-full h-56 rounded-xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400 bg-gray-50">
            <SafeIcon icon={FiZap} className="text-4xl mb-2 opacity-20" />
            <span>Bereit zum Generieren</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default GenerativeBrandSystem;