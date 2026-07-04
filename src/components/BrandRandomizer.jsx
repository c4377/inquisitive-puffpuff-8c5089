import React, { useState, useEffect, useMemo } from 'react';
import { FiCheck, FiZap, FiRefreshCw } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import Canvas from './Canvas';
import { useBrand } from '../context/BrandContext';
import { generateTrulyRandomBrand, brandRuleSets, CURATED_BRANDS } from '../constants/brandData';
import GenerativeBrandSystem from './GenerativeBrandSystem';
import StyleShifter from './StyleShifter';

const BrandRandomizer = () => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const [selectedKey, setSelectedKey] = useState(null);

  // Sync selected key with active brand
  useEffect(() => {
    if (brandSettings.currentBrandConfig?.ruleSet) {
      setSelectedKey(brandSettings.currentBrandConfig.ruleSet);
    }
  }, [brandSettings.currentBrandConfig]);

  // 1. HANDLER: AI GENERATOR (Creates NEW Unique Brands)
  const handleAiGeneration = (newConfig) => {
    // Determine the closest matching ruleset key for the UI highlight
    // If it's a completely random mix, we might not have a key, so we clear it or keep 'custom'
    setSelectedKey(newConfig.ruleSet || 'custom');
    // Update Global Settings (Activate it immediately for preview)
    updateBrandSettings({
      currentBrandConfig: newConfig,
    });
  };

  // 2. HANDLER: PRESET SELECTION (Applies Fixed Templates)
  const applyTemplate = (ruleSetKey) => {
    // Generate new visual style based on the specific rule set
    const newBrandVisuals = generateTrulyRandomBrand(ruleSetKey);
    
    // MERGE with existing Identity (keep Name, Strategy, etc.)
    const existingBrand = brandSettings.currentBrandConfig || {};
    const mergedBrand = {
      ...newBrandVisuals,
      name: existingBrand.name || newBrandVisuals.name,
      brandText: existingBrand.brandText,
      website: existingBrand.website,
      strategy: existingBrand.strategy || newBrandVisuals.strategy,
      id: existingBrand.id || newBrandVisuals.id
    };

    updateBrandSettings({
      currentBrandConfig: mergedBrand,
      // Update the saved version if it exists in the list
      brandConfigurations: (brandSettings.brandConfigurations || []).map(c => 
        c.id === mergedBrand.id ? mergedBrand : c
      )
    });
    setSelectedKey(ruleSetKey);
    // Smooth scroll to top to see result
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Apply a FIXED curated brand (Editorial Dark/Hell): take its full config
  // (incl. editorialDark + darkPhoto flags), keep the user's identity fields.
  const applyCuratedBrand = (brand) => {
    const existingBrand = brandSettings.currentBrandConfig || {};
    const mergedBrand = {
      ...brand,
      brandText: existingBrand.brandText,
      website: existingBrand.website,
      strategy: existingBrand.strategy || {},
    };
    updateBrandSettings({ currentBrandConfig: mergedBrand });
    setSelectedKey(brand.id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Prepare Template Previews - Force Refresh
  const templatePreviews = useMemo(() => {
    // Fixed curated brands FIRST (Editorial Dark/Hell) — always identical,
    // full config incl. editorialDark flag for the auto two-font rendering.
    const curatedCards = CURATED_BRANDS.map((brand) => ({
      key: brand.id,
      curatedBrand: brand,
      ruleSet: { name: brand.name, description: 'Playfair + Handschrift, automatisch.' },
      canvasData: {
        text: brand.sampleText || 'Du bist Fotografin, aber du verkaufst keine Fotos',
        backgroundColor: brand.colors.background,
        color: brand.colors.primary,
        secondaryColor: brand.colors.secondary,
        accentColor: brand.colors.accent,
        fontFamily: brand.typography.fontFamily,
        accentFontFamily: brand.typography.accentFontFamily,
        fontWeight: brand.typography.fontWeight,
        fontSize: 30,
        visualElements: [],
        layout: 'auto',
        editorialDark: true,
        darkPhoto: brand.darkPhoto,
        textAlign: 'center',
        format: '4:5',
        isPreview: true,
      },
      tags: brand.tags,
    }));

    const ruleCards = Object.entries(brandRuleSets).map(([key, ruleSet]) => {
      const brand = generateTrulyRandomBrand(key);
      const canvasData = {
        // USE SAMPLE TEXT WITH ACCENTS TO SHOW MIXED FONTS
        text: brand.sampleText || "KLARHEIT DURCH *FOKUS*",
        backgroundColor: brand.colors.background,
        color: brand.colors.primary,
        secondaryColor: brand.colors.secondary,
        accentColor: brand.colors.accent,
        fontFamily: brand.typography.fontFamily,
        accentFontFamily: brand.typography.accentFontFamily, // IMPORTANT: Pass accent font
        fontWeight: brand.typography.fontWeight,
        fontSize: 36,
        visualElements: brand.visualElements,
        layout: brand.layout,
        textAlign: brand.layout === 'minimal_bottom_left' || brand.layout === 'magazine_left_middle' ? 'left' : 'center',
        format: '4:5',
        isPreview: true
      };
      return { key, ruleSet, canvasData, tags: brand.tags };
    });

    return [...curatedCards, ...ruleCards];
  }, []); // Empty dependency ensures it runs once on mount, but hot reload will refresh it

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8 pb-32">
      {/* HEADER */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4 font-playfair">Brand Identity Designer</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Lass die KI deine Brand entwerfen oder wähle einen kuratierten Style.
        </p>
      </div>

      {/* SECTION 1: AI GENERATOR (The "Designer") */}
      <div className="mb-20">
        <div className="bg-white rounded-2xl shadow-xl border border-purple-100 overflow-hidden max-w-5xl mx-auto">
          <div className="bg-gradient-to-r from-gray-900 to-gray-800 p-4 border-b border-gray-700 flex justify-between items-center">
            <h2 className="text-white font-bold text-lg flex items-center">
              <SafeIcon icon={FiZap} className="mr-2 text-yellow-400" /> AI Brand Designer
            </h2>
            <span className="text-xs text-gray-400 uppercase tracking-wider font-semibold">Generative Mode</span>
          </div>
          <div className="p-6 md:p-8 bg-gray-50">
            <div className="flex flex-col md:flex-row gap-8 items-start">
              <div className="flex-1 w-full">
                <p className="text-sm text-gray-600 mb-6">
                  Der AI Designer kombiniert Farben, Schriftarten und Layouts basierend auf Design-Regeln, um einzigartige Identitäten zu schaffen. Klicke auf "Generate New", um neue Entwürfe zu erhalten.
                </p>
                {/* GENERATOR COMPONENT with Save Logic */}
                <GenerativeBrandSystem compact={false} onGenerate={handleAiGeneration} />

                {/* NEW: STYLE SHIFTER INTEGRATION */}
                {brandSettings.currentBrandConfig && (
                  <div className="mt-8 pt-8 border-t border-gray-200">
                    <h3 className="text-sm font-bold text-gray-700 mb-3 flex items-center">
                      <SafeIcon icon={FiRefreshCw} className="mr-2 text-purple-600"/> Fine-Tuning: Style Shifter
                    </h3>
                    <p className="text-xs text-gray-500 mb-4">Gefällt dir der Style, aber die Farben oder Fonts sind vertauscht? Nutze den Shifter.</p>
                    <StyleShifter compact={false} />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SEPARATOR */}
      <div className="relative flex py-5 items-center mb-12">
        <div className="flex-grow border-t border-gray-300"></div>
        <span className="flex-shrink-0 mx-4 text-gray-400 text-sm font-bold uppercase tracking-widest">ODER WÄHLE EINEN STYLE</span>
        <div className="flex-grow border-t border-gray-300"></div>
      </div>

      {/* SECTION 2: CURATED PRESETS */}
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 font-playfair">Kuratierte Styles</h2>
        <p className="text-gray-500">Klicke auf ein Design, um es sofort zu aktivieren.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        {templatePreviews.map(({ key, ruleSet, canvasData, tags, curatedBrand }) => {
          const isSelected = selectedKey === key;
          return (
            <button
              key={key}
              onClick={() => curatedBrand ? applyCuratedBrand(curatedBrand) : applyTemplate(key)}
              className={`group relative flex flex-col items-center text-left transition-all duration-300 rounded-xl ${isSelected ? 'ring-4 ring-purple-600 ring-offset-4 scale-105 z-10 shadow-2xl' : 'hover:scale-105 hover:shadow-xl hover:z-10 opacity-90 hover:opacity-100'}`}
            >
              <div className="w-full aspect-[4/5] rounded-xl overflow-hidden shadow-sm border border-gray-200 bg-white relative">
                <div className="w-full h-full pointer-events-none">
                  {/* Static Brand Name to verify preview */}
                  <Canvas data={canvasData} brandName={ruleSet.name} />
                </div>
                {/* Hover Overlay */}
                <div className={`absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300 flex items-center justify-center`}>
                  {isSelected && (
                    <div className="bg-purple-600 text-white p-2 rounded-full shadow-lg transform scale-100 transition-transform">
                      <SafeIcon icon={FiCheck} className="text-xl" />
                    </div>
                  )}
                </div>
              </div>
              <div className="mt-3 w-full px-1">
                <div className="flex justify-between items-start">
                  <h3 className={`font-bold text-sm leading-tight ${isSelected ? 'text-purple-700' : 'text-gray-900'}`}>{ruleSet.name}</h3>
                </div>
                <div className="flex flex-wrap gap-1 mt-1.5">
                  {tags.slice(0, 2).map(tag => (
                    <span key={tag} className="text-[9px] uppercase tracking-wider font-semibold text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default BrandRandomizer;