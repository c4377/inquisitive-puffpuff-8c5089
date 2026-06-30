import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import * as FiIcons from 'react-icons/fi';
import { fabric } from 'fabric'; // Added Fabric import
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import Canvas from '../components/Canvas';
import StyleShifter from '../components/StyleShifter';
import BulkImportModal from '../components/BulkImportModal';
import { renderSlide } from '../utils/canvasRenderer';
import { brandRuleSets } from '../constants/brandData';
import { createSmartSlide } from '../utils/slideHelpers';
import { attachSmartImages } from '../utils/smartLayoutGenerator';
import { weightedLayoutPool, getRating, setRating } from '../utils/layoutRatings';

const { FiEdit3, FiDownload, FiRefreshCw, FiZap, FiType, FiMessageSquare, FiCopy, FiExternalLink, FiUser, FiSave, FiFileText, FiThumbsUp, FiThumbsDown } = FiIcons;

const ContentPlanner = () => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const navigate = useNavigate();
  const weekPlan = brandSettings.contentPlan || [];
  const [loading, setLoading] = useState(false);
  const [activeIndices, setActiveIndices] = useState({});
  const [expandedCaptionId, setExpandedCaptionId] = useState(null);
  const [showStyleShifter, setShowStyleShifter] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [isExportingAll, setIsExportingAll] = useState(false);
  const [exportingDayId, setExportingDayId] = useState(null);
  const [saveStatus, setSaveStatus] = useState('');
  const [ratingTick, setRatingTick] = useState(0); // bump to refresh thumb UI
  const [autoApplyStyle, setAutoApplyStyle] = useState(true);

  const currentBrand = brandSettings.currentBrandConfig;
  const hasActiveBrand = !!currentBrand;
  const brandName = currentBrand?.name || "MUSE MENTORING";

  // --- HELPER: COLOR CONTRAST ---
  const getBrightness = (hex) => {
    if (!hex) return 255;
    const r = parseInt(hex.substr(1, 2), 16);
    const g = parseInt(hex.substr(3, 2), 16);
    const b = parseInt(hex.substr(5, 2), 16);
    return ((r * 299) + (g * 587) + (b * 114)) / 1000;
  };
  const isDark = (hex) => getBrightness(hex || '#ffffff') < 128;

  // --- CORE: ADVANCED BRAND STYLING ENGINE ---
  const applyBrandStyling = (plan, config) => {
    if (!config || !plan) return [];
    
    const colors = config.colors || { primary: '#000', background: '#fff', secondary: '#ccc', accent: '#888' };
    const fonts = config.typography || { fontFamily: 'Inter', fontWeight: '400' };
    
    let rules = { vibe: 'minimal_editorial', layoutRules: [] };
    const ruleKey = config.ruleSet;
    
    if (ruleKey && brandRuleSets[ruleKey]) {
      rules = brandRuleSets[ruleKey];
    } else {
      if (isDark(colors.background)) rules.vibe = 'luxury_dark';
      else if (colors.accent && !isDark(colors.accent)) rules.vibe = 'bold_pop';
    }

    return plan.map((day, index) => {
      let bg, text, sec, acc;
      
      // Smart Color Rotation Logic
      if (rules.vibe === 'luxury_dark') {
        const luxPattern = ['primary', 'primary', 'accent', 'primary', 'background', 'primary', 'primary'];
        const role = luxPattern[index % 7];
        if (role === 'primary') {
           if (isDark(colors.background)) { bg = colors.background; text = colors.primary; }
           else { bg = '#000000'; text = '#FFFFFF'; }
        } else if (role === 'accent') {
           bg = colors.accent; text = '#FFFFFF';
        } else {
           bg = '#FFFFFF'; text = '#000000';
        }
      } else if (rules.vibe === 'soft_warm') {
        if (index % 2 === 0) { bg = colors.background; text = colors.primary; }
        else { bg = colors.secondary; text = colors.primary; }
      } else if (rules.vibe === 'bold_pop') {
        const popPattern = ['bg', 'inv', 'acc', 'bg', 'inv', 'bg', 'inv'];
        const role = popPattern[index % 7];
        if (role === 'bg') { bg = colors.background; text = colors.primary; }
        else if (role === 'inv') { bg = colors.primary; text = colors.background; }
        else { bg = colors.accent; text = '#FFFFFF'; }
      } else {
        const pattern = ['std', 'inv', 'std', 'sec', 'inv', 'std', 'inv'];
        const role = pattern[index % 7];
        if (role === 'std') { bg = colors.background; text = colors.primary; }
        else if (role === 'inv') { bg = colors.primary; text = colors.background; }
        else { bg = colors.secondary; text = colors.primary; }
      }
      sec = colors.secondary;
      acc = colors.accent;

      return {
        ...day,
        slides: day.slides.map((slide, sIdx) => {
          const font = sIdx === 0 ? fonts.fontFamily : (fonts.bodyFontFamily || 'Montserrat');
          const accentFont = fonts.accentFontFamily || (font.includes('Playfair') ? 'Montserrat' : 'Playfair Display');
          const isPlayfair = font.includes('Playfair');
          let weight = '400';
          if (sIdx === 0 && !isPlayfair) weight = fonts.fontWeight || '700';
          
          let finalLayout = slide.layout;
          if (sIdx === 0) {
             if (finalLayout === 'minimal_quote' && rules.vibe === 'bold_pop') {
                 finalLayout = 'maximized_bold';
             }
          }

          return {
            ...slide,
            color: text,
            backgroundColor: bg,
            secondaryColor: sec,
            accentColor: acc,
            fontFamily: font,
            accentFontFamily: accentFont,
            fontWeight: weight,
            visualElements: config.visualElements || [],
            layout: finalLayout
          };
        })
      };
    });
  };

  const syncStyleToPlan = (configToUse = null) => {
    const config = configToUse || currentBrand;
    if (!config || weekPlan.length === 0) return;
    if (!config.colors || !config.typography) return;

    const styledPlan = applyBrandStyling(weekPlan, config);
    const oldSample = JSON.stringify({ c: weekPlan[0]?.slides[0]?.color, f: weekPlan[0]?.slides[0]?.fontFamily });
    const newSample = JSON.stringify({ c: styledPlan[0]?.slides[0]?.color, f: styledPlan[0]?.slides[0]?.fontFamily });
    
    if (oldSample !== newSample) {
        updateBrandSettings({ contentPlan: styledPlan });
    }
  };

  useEffect(() => {
    if (autoApplyStyle && brandSettings.currentBrandConfig && weekPlan.length > 0) {
      const timer = setTimeout(() => {
        syncStyleToPlan(brandSettings.currentBrandConfig);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [brandSettings.currentBrandConfig, autoApplyStyle]);

  const handleImportPlan = (importedDays) => {
    setLoading(true);
    const brandConfig = brandSettings.currentBrandConfig;
    const ruleKey = brandConfig?.ruleSet;
    const rules = (ruleKey && brandRuleSets[ruleKey]) ? brandRuleSets[ruleKey] : { layoutRules: [] };
    const baseLayouts = rules.layoutRules.length > 0 ? rules.layoutRules : ['minimal_quote', 'centered_focus', 'glass_layer'];
    const allowedLayouts = weightedLayoutPool(baseLayouts);

    const newPlan = importedDays.map((dayData, dIdx) => {
        const slides = dayData.slides.map((text, sIdx) => {
            // Rotate through allowed layouts (offset per day) so slides vary
            // instead of always using the same layout.
            const layout = allowedLayouts[(dIdx + sIdx) % allowedLayouts.length];
            return createSmartSlide(brandConfig, { text, layout }, sIdx, dayData.slides.length);
        });

        return {
            day: dayData.day,
            title: dayData.title,
            caption: dayData.caption,
            type: slides.length > 1 ? 'carousel' : 'hook',
            slides: slides
        };
    });

    const finalPlan = applyBrandStyling(newPlan, brandConfig);
    updateBrandSettings({ contentPlan: finalPlan });
    
    setLoading(false);
    setSaveStatus('Plan importiert!');
    setTimeout(() => setSaveStatus(''), 3000);
  };

  const handleManualSave = () => {
    setSaveStatus('Speichere...');
    updateBrandSettings({ contentPlan: [...weekPlan] });
    setTimeout(() => setSaveStatus('Gespeichert!'), 600);
    setTimeout(() => setSaveStatus(''), 2000);
  };

  // RELOAD: re-initialize the ALREADY GENERATED posts (not the import text).
  // Cover rule: of the 7 day-covers, days 1,3,5,7 get a background image,
  // days 2,4,6 stay image-free (layout only). Content slides keep images.
  const handleReloadPlan = async () => {
    if (!weekPlan || weekPlan.length === 0) return;
    setLoading(true);
    setSaveStatus('Lade Posts neu...');
    try {
      const imagePool = brandSettings?.brandImages || [];
      // Fixed pattern: which day-INDEX (0-based) gets a cover image.
      // days 1,3,5,7 => indices 0,2,4,6
      const coverGetsImage = (dayIdx) => dayIdx % 2 === 0;

      const reloadedPlan = [];
      for (let dayIdx = 0; dayIdx < weekPlan.length; dayIdx++) {
        const day = weekPlan[dayIdx];
        const withImages = await attachSmartImages(day.slides, imagePool);

        // Enforce cover rule on slide 0 (the cover)
        const adjusted = withImages.map((slide, sIdx) => {
          // Reset any stale default blur from older generations (was 8/12).
          const cleaned = { ...slide };
          if (cleaned.blur === 8 || cleaned.blur === 12) cleaned.blur = 0;
          if (sIdx !== 0) return cleaned; // only the cover is governed by the rule
          if (coverGetsImage(dayIdx)) {
            return cleaned; // keep assigned image
          }
          // remove image -> layout-only cover
          const { background, overlay, _autoImage, ...rest } = cleaned;
          // If the cover had a photo-only layout (cover_*/sarah_cover), swap to
          // a strong text layout so the image-free cover still looks designed.
          const photoLayouts = ['sarah_cover', 'cover_top_left', 'cover_bottom_left', 'cover_bottom_center', 'cover_center_hero', 'cover_top_center'];
          const textCoverLayouts = ['minimal_quote', 'maximized_bold', 'editorial_classic', 'diagonal_overlay'];
          const curLayout = rest.layout || rest.layoutId;
          const newLayout = photoLayouts.includes(curLayout)
            ? textCoverLayouts[dayIdx % textCoverLayouts.length]
            : curLayout;
          return { ...rest, background: null, layout: newLayout, layoutId: newLayout };
        });

        reloadedPlan.push({ ...day, slides: adjusted });
      }
      updateBrandSettings({ contentPlan: reloadedPlan });
      const imgCovers = weekPlan.filter((_, i) => coverGetsImage(i)).length;
      setSaveStatus(
        imagePool.length > 0
          ? `Neu generiert – ${imgCovers} Cover mit Bild, Rest mit Layout.`
          : 'Neu generiert (keine Bilder im Pool).'
      );
    } catch (e) {
      console.error('reload failed', e);
      setSaveStatus('Fehler beim Neuladen.');
    } finally {
      setLoading(false);
      setTimeout(() => setSaveStatus(''), 3500);
    }
  };

  const handleExportAll = async () => {
    if (!weekPlan || weekPlan.length === 0) return;
    setIsExportingAll(true);
    try {
      const zip = new JSZip();
      const folder = zip.folder("Content_Plan_Export");
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || brandSettings.currentBrandConfig?.name || "MUSE MENTORING";

      for (const day of weekPlan) {
        for (let i = 0; i < day.slides.length; i++) {
          const slide = day.slides[i];
          const canvasEl = document.createElement('canvas');
          const canvasWidth = 1080;
          const canvasHeight = slide.format === '9:16' ? 1920 : 1350;
          const scale = canvasWidth / 400;
          const fCanvas = new fabric.StaticCanvas(canvasEl, { width: canvasWidth, height: canvasHeight });
          await renderSlide(fCanvas, { ...slide, visualElements: slide.visualElements || [] }, canvasWidth, canvasHeight, {
            slideIndex: i, totalSlides: day.slides.length, scale, globalBrandName
          });
          const dataUrl = fCanvas.toDataURL({ format: 'png', multiplier: 1 });
          const blob = await (await fetch(dataUrl)).blob();
          if (blob) {
            const cleanTitle = day.title.replace(/[^a-z0-9]/gi, '_').substring(0, 20);
            folder.file(`Tag_${day.day}_${cleanTitle}_Slide_${i + 1}.png`, blob);
          }
          fCanvas.dispose();
        }
      }
      const content = await zip.generateAsync({ type: "blob" });
      saveAs(content, `Content_Plan_Flat.zip`);
    } catch (e) {
      console.error("Export Failed", e);
    } finally {
      setIsExportingAll(false);
    }
  };

  // Export a SINGLE day (was previously a dead button).
  const handleExportDay = async (day) => {
    if (!day || !day.slides?.length) return;
    setExportingDayId(day.day);
    try {
      const zip = new JSZip();
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || brandSettings.currentBrandConfig?.name || "MUSE MENTORING";
      for (let i = 0; i < day.slides.length; i++) {
        const slide = day.slides[i];
        const canvasEl = document.createElement('canvas');
        const canvasWidth = 1080;
        const canvasHeight = slide.format === '9:16' ? 1920 : 1350;
        const scale = canvasWidth / 400;
        const fCanvas = new fabric.StaticCanvas(canvasEl, { width: canvasWidth, height: canvasHeight });
        await renderSlide(fCanvas, { ...slide, visualElements: slide.visualElements || [] }, canvasWidth, canvasHeight, {
          slideIndex: i, totalSlides: day.slides.length, scale, globalBrandName
        });
        const dataUrl = fCanvas.toDataURL({ format: 'png', multiplier: 1 });
        const blob = await (await fetch(dataUrl)).blob();
        if (blob) zip.file(`Slide_${i + 1}.png`, blob);
        fCanvas.dispose();
      }
      const content = await zip.generateAsync({ type: "blob" });
      const cleanTitle = (day.title || `Tag_${day.day}`).replace(/[^a-z0-9]/gi, '_').substring(0, 20);
      saveAs(content, `Tag_${day.day}_${cleanTitle}.zip`);
    } catch (e) {
      console.error("Day export failed", e);
    } finally {
      setExportingDayId(null);
    }
  };

  const handleEditDay = (dayData) => {
    navigate('/editor', { state: { slides: dayData.slides, dayId: dayData.day, dayTitle: dayData.title } });
  };

  const updateActiveSlideFontSize = (dayId, newSize) => {
    const activeIdx = activeIndices[dayId] || 0;
    const updatedPlan = weekPlan.map(day => {
      if (day.day === dayId) {
        const newSlides = [...day.slides];
        newSlides[activeIdx] = { ...newSlides[activeIdx], fontSize: newSize };
        return { ...day, slides: newSlides };
      }
      return day;
    });
    updateBrandSettings({ contentPlan: updatedPlan });
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 pb-32">
      <BulkImportModal isOpen={showImportModal} onClose={() => setShowImportModal(false)} onImportPlan={handleImportPlan} />
      <div className="sticky top-[64px] z-30 bg-white/95 backdrop-blur border-b border-gray-200 shadow-sm -mx-4 sm:-mx-6 px-4 sm:px-6 transition-all">
        <div className="py-3 flex flex-col md:flex-row justify-between items-center max-w-4xl mx-auto gap-3">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Content Plan</h1>
            <p className="text-xs text-gray-500 flex items-center mt-1"><SafeIcon icon={FiUser} className="mr-1 text-purple-500" /> Füge deine Texte per Bulk Import ein.</p>
          </div>
          <div className="flex flex-wrap gap-2 items-center justify-end">
            <button onClick={() => setShowImportModal(true)} className="px-3 py-2 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 transition-colors flex items-center shadow-md whitespace-nowrap text-xs"><SafeIcon icon={FiFileText} className="mr-2" /> Bulk Import</button>
            {hasActiveBrand && (
              <>
              <button onClick={() => setShowStyleShifter(!showStyleShifter)} className={`flex items-center px-4 py-2 rounded-lg border transition-all text-xs font-bold ${showStyleShifter ? 'bg-purple-600 text-white border-purple-600 shadow-inner' : 'bg-white border-purple-200 text-purple-700 hover:bg-purple-50 hover:border-purple-300 shadow-sm'}`} title="Style Shifter (Fonts/Colors)"><SafeIcon icon={FiRefreshCw} className="mr-2 text-sm" /> Shifter</button>
              <button onClick={handleReloadPlan} disabled={loading || weekPlan.length === 0} className="flex items-center px-4 py-2 rounded-lg border border-emerald-200 bg-white text-emerald-700 hover:bg-emerald-50 hover:border-emerald-300 shadow-sm transition-all text-xs font-bold disabled:opacity-40" title="Posts neu generieren (Bilder neu zuordnen)"><SafeIcon icon={FiRefreshCw} className={`mr-2 text-sm ${loading ? 'animate-spin' : ''}`} /> Neu laden</button>
              </>
            )}
            <div className="h-6 w-px bg-gray-300 mx-1"></div>
            <button onClick={handleManualSave} className="p-2 hover:bg-white rounded-md text-green-700 transition-colors" title="Speichern"><SafeIcon icon={FiSave} /></button>
            <button onClick={handleExportAll} disabled={isExportingAll || loading} className="p-2 rounded-lg border bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors" title="Alles Exportieren"><SafeIcon icon={FiDownload} className={isExportingAll ? "animate-bounce" : ""} /></button>
          </div>
        </div>
        <AnimatePresence>
          {showStyleShifter && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden border-t border-gray-100 bg-gray-50"><div className="py-2"><StyleShifter mode="bar" /></div></motion.div>
          )}
        </AnimatePresence>
        {saveStatus && (<div className="absolute top-16 left-0 right-0 text-center pointer-events-none"><span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-bold border border-green-200 shadow-sm animate-fade-in-down">{saveStatus}</span></div>)}
      </div>
      <div className="mb-6 mt-6"></div>
      {loading ? (
        <div className="space-y-6 pt-4">{[1, 2, 3].map(i => <div key={i} className="h-64 bg-gray-100 rounded-xl animate-pulse"></div>)}</div>
      ) : (
        <div className="space-y-8">
          {weekPlan.length === 0 ? (
            <div className="text-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
              <h3 className="text-lg font-bold text-gray-700 mb-2">Noch kein Plan erstellt</h3>
              <p className="text-gray-500 mb-4">Klicke auf "Bulk Import", um deine Texte einzufügen.</p>
              <div className="flex justify-center gap-4"><button onClick={() => setShowImportModal(true)} className="bg-purple-600 text-white px-6 py-3 rounded-lg font-bold shadow-md hover:bg-purple-700 transition-colors">Bulk Import Starten</button></div>
            </div>
          ) : (
            weekPlan.map((day, dayIndex) => {
              const activeIndex = activeIndices[day.day] || 0;
              const activeSlide = day.slides[activeIndex];
              const isCaptionOpen = expandedCaptionId === day.day;
              const dynamicActiveSlide = { ...activeSlide, visualElements: activeSlide.visualElements || [], format: activeSlide.format || '4:5' };
              const isExportingThisDay = exportingDayId === day.day;
              return (
                <motion.div key={`${day.day}-${day.title}`} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: dayIndex * 0.1 }} className="bg-white rounded-xl overflow-hidden shadow-md border border-gray-100">
                  <div className="border-b border-gray-100 px-4 py-3 flex justify-between items-center bg-gray-50">
                    <span className="font-bold text-gray-900">Tag {day.day}</span>
                    <div className="flex items-center space-x-2"><span className="text-xs text-purple-700 bg-purple-50 px-2 py-1 rounded border border-purple-100 font-bold uppercase tracking-wider">{day.type === 'hook' ? 'Hook' : 'Post'}</span></div>
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-normal text-gray-900 font-playfair mb-2">{day.title}</h3>
                    <div className="relative bg-gray-100 rounded-lg overflow-hidden border border-gray-200 aspect-[4/5] mb-4 shadow-inner">
                      <div className="w-full h-full flex items-center justify-center">
                        <div className="w-full h-full max-h-full transition-all duration-300">
                          <Canvas key={`${day.day}-${activeIndex}-${dynamicActiveSlide.color}-${dynamicActiveSlide.secondaryColor}-${dynamicActiveSlide.fontFamily}-${dynamicActiveSlide.backgroundColor}`} data={{...dynamicActiveSlide, slideNumber: undefined}} brandName={brandName} />
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-2 flex-1 mr-4"><SafeIcon icon={FiType} className="text-gray-400 text-xs"/><input type="range" min="16" max="160" value={activeSlide.fontSize} onChange={(e) => updateActiveSlideFontSize(day.day, parseInt(e.target.value))} className="flex-1 h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" /></div>
                      <button onClick={() => setExpandedCaptionId(isCaptionOpen ? null : day.day)} className={`p-2 rounded-lg transition-colors ${isCaptionOpen ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}><SafeIcon icon={FiMessageSquare} /></button>
                    </div>
                    {/* Layout-Bewertung: Daumen hoch/runter fürs aktuelle Layout */}
                    {(() => {
                      const lay = dynamicActiveSlide.layout || dynamicActiveSlide.layoutId;
                      const rating = getRating(lay);
                      return (
                        <div className="flex items-center justify-center gap-3 mb-4 text-xs text-gray-500">
                          <span>Layout «{lay}»</span>
                          <button
                            onClick={() => { setRating(lay, 1); setRatingTick((t) => t + 1); }}
                            className={`p-1.5 rounded-lg border transition-colors ${rating === 1 ? 'bg-emerald-100 border-emerald-300 text-emerald-700' : 'bg-white border-gray-200 text-gray-400 hover:text-emerald-600'}`}
                            title="Dieses Layout öfter nutzen"
                          >
                            <SafeIcon icon={FiThumbsUp} />
                          </button>
                          <button
                            onClick={() => { setRating(lay, -1); setRatingTick((t) => t + 1); }}
                            className={`p-1.5 rounded-lg border transition-colors ${rating === -1 ? 'bg-red-100 border-red-300 text-red-700' : 'bg-white border-gray-200 text-gray-400 hover:text-red-600'}`}
                            title="Dieses Layout seltener/nicht nutzen"
                          >
                            <SafeIcon icon={FiThumbsDown} />
                          </button>
                        </div>
                      );
                    })()}
                    {isCaptionOpen && (
                      <div className="mb-4 p-3 bg-blue-50 text-sm text-blue-900 rounded-lg border border-blue-100 relative"><p className="whitespace-pre-wrap pr-6">{day.caption || "Keine Caption verfügbar."}</p><button onClick={() => navigator.clipboard.writeText(day.caption)} className="absolute top-2 right-2 p-1 hover:bg-blue-100 rounded text-blue-500" title="Kopieren"><SafeIcon icon={FiCopy} /></button></div>
                    )}
                    <div className="grid grid-cols-3 gap-2">
                      <button onClick={() => handleEditDay(day)} className="bg-white border border-gray-200 text-gray-700 py-2.5 px-3 rounded-lg font-bold text-xs flex items-center justify-center hover:bg-gray-50 hover:border-purple-300 hover:text-purple-700 transition-all"><SafeIcon icon={FiEdit3} className="mr-1.5" /> Bearbeiten</button>
                      <button onClick={() => handleExportDay(day)} disabled={isExportingThisDay} className="bg-gray-100 border border-gray-200 text-gray-700 py-2.5 px-3 rounded-lg font-bold text-xs flex items-center justify-center hover:bg-gray-200 hover:text-purple-700 transition-all disabled:opacity-50">{isExportingThisDay ? <span className="animate-spin mr-1.5"><SafeIcon icon={FiRefreshCw} /></span> : <SafeIcon icon={FiDownload} className="mr-1.5" />} Export</button>
                      <button onClick={() => navigate('/create')} className="bg-gray-50 text-gray-500 py-2.5 px-3 rounded-lg font-bold text-xs flex items-center justify-center hover:bg-gray-100 transition-colors"><SafeIcon icon={FiExternalLink} className="mr-1.5" /> Neu</button>
                    </div>
                  </div>
                </motion.div>
              );
            })
          )}
        </div>
      )}
    </div>
  );
};

export default ContentPlanner;