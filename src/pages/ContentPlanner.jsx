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
import { decidePostDesign, dayHasImage } from '../utils/postDesignEngine';
import { weightedLayoutPool, getRating, setRating } from '../utils/layoutRatings';

const { FiEdit3, FiDownload, FiRefreshCw, FiZap, FiType, FiMessageSquare, FiCopy, FiExternalLink, FiUser, FiSave, FiFileText, FiThumbsUp, FiThumbsDown, FiShare2, FiLayers } = FiIcons;

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

  // Central layout rotation — used by BOTH import and reload so variety is
  // consistent everywhere, not only on fresh import. Returns an array of real
  // layout ids mixing brand rules with the magazine-style variants.
  const REAL_LAYOUTS = ['aesthetic_checklist','bold_number_list','diagonal_overlay','editorial_classic','glass_layer','maximized_bold','minimal_editorial','minimal_quote','paper_box','cover_bottom_left','cover_bottom_center','cover_top_left','cover_top_center','cover_center_hero','split_color','story_text_box','tweet_card'];
  const LAYOUT_ALIAS = {
    badge_centered: 'minimal_quote',
    split_vertical_editorial: 'split_color',
    editorial_mask: 'editorial_classic',
    editorial_fade_bottom: 'paper_box',
    minimal_left_accent: 'editorial_classic',
    centered_focus: 'minimal_quote',
  };
  const resolveLayout = (name) => {
    if (REAL_LAYOUTS.includes(name)) return name;
    if (LAYOUT_ALIAS[name]) return LAYOUT_ALIAS[name];
    return 'editorial_classic';
  };
  const buildLayoutRotation = (brandConfig) => {
    const ruleKey = brandConfig?.ruleSet;
    const rules = (ruleKey && brandRuleSets[ruleKey]) ? brandRuleSets[ruleKey] : { layoutRules: [] };
    const baseLayouts = rules.layoutRules.length > 0 ? rules.layoutRules : ['minimal_quote', 'editorial_classic', 'glass_layer'];
    const allowed = weightedLayoutPool(baseLayouts).map(resolveLayout);
    // The magazine variants that give the feed its structural variety.
    const variety = ['editorial_classic', 'minimal_quote'];
    const mixed = [];
    const maxLen = Math.max(allowed.length, variety.length);
    for (let i = 0; i < maxLen; i++) {
      if (allowed[i % allowed.length]) mixed.push(allowed[i % allowed.length]);
      mixed.push(variety[i % variety.length]);
    }
    return mixed;
  };

  const handleImportPlan = async (importedDays) => {
    setLoading(true);
    const brandConfig = brandSettings.currentBrandConfig;
    const imagePool = brandSettings?.brandImages || [];

    // Fully automatic: the engine decides image / text position / bold per post.
    let globalIndex = 0;
    let imageOffset = 0; // global image cursor across the whole plan
    const newPlan = [];
    for (let dIdx = 0; dIdx < importedDays.length; dIdx++) {
      const dayData = importedDays[dIdx];
      const wantsImage = dayHasImage(dIdx) && imagePool.length > 0;

      let slides = dayData.slides.map((text, sIdx) =>
        createSmartSlide(brandConfig, { text }, sIdx, dayData.slides.length)
      );

      if (wantsImage) {
        try {
          slides = await attachSmartImages(slides, imagePool, imageOffset);
          imageOffset += slides.length; // advance cursor so next day differs
        } catch (e) { /* keep */ }
      }

      slides = slides.map((slide) => {
        let s2 = { ...slide };
        const hasImg = wantsImage && typeof s2.background === 'string' && s2.background.length > 5;
        if (!hasImg) {
          const { background, overlay, _autoImage, ...rest } = s2;
          s2 = { ...rest, background: null };
        }
        const { textAnchor, bold } = decidePostDesign({
          globalIndex, hasImage: hasImg, autoImage: s2._autoImage,
        });
        globalIndex++;
        return {
          ...s2,
          layout: 'auto', layoutId: 'auto',
          textAnchor,
          fontWeight: bold ? '700' : 'normal',
        };
      });

      newPlan.push({
        day: dayData.day,
        title: dayData.title,
        caption: dayData.caption,
        type: slides.length > 1 ? 'carousel' : 'hook',
        slides,
      });
    }

    const finalPlan = applyBrandStyling(newPlan, brandConfig);
    updateBrandSettings({ contentPlan: finalPlan });

    // Count how many slides actually received a photo, so the user sees
    // immediately whether the image pool was found and attached.
    const withPhotos = finalPlan.reduce((acc, day) =>
      acc + day.slides.filter(s => typeof s.background === 'string' && s.background.length > 5).length, 0);
    const totalSlides = finalPlan.reduce((acc, day) => acc + day.slides.length, 0);

    setLoading(false);
    setSaveStatus(`Plan importiert – ${withPhotos}/${totalSlides} mit Bild (Pool: ${imagePool.length}).`);
    setTimeout(() => setSaveStatus(''), 5000);
    // The planner view itself is now the grid feed, so we stay here and the
    // covers appear immediately.
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

      let globalIndex = 0;
      let imageOffset = 0; // global image cursor across the whole plan
      const reloadedPlan = [];
      for (let dayIdx = 0; dayIdx < weekPlan.length; dayIdx++) {
        const day = weekPlan[dayIdx];
        const wantsImage = dayHasImage(dayIdx) && imagePool.length > 0;
        let daySlides = day.slides;
        if (wantsImage) {
          daySlides = await attachSmartImages(day.slides, imagePool, imageOffset);
          imageOffset += daySlides.length; // advance so next day gets new images
        }

        const adjusted = daySlides.map((slide) => {
          const cleaned = { ...slide };
          if (cleaned.blur === 8 || cleaned.blur === 12) cleaned.blur = 0;

          const hasImg = wantsImage && typeof cleaned.background === 'string' && cleaned.background.length > 5;
          if (!hasImg) {
            const { background, overlay, _autoImage, ...rest } = cleaned;
            Object.assign(cleaned, rest, { background: null, overlay: undefined, _autoImage: undefined });
          }
          const { textAnchor, bold } = decidePostDesign({
            globalIndex, hasImage: hasImg, autoImage: cleaned._autoImage,
          });
          globalIndex++;
          cleaned.layout = 'auto';
          cleaned.layoutId = 'auto';
          cleaned.textAnchor = textAnchor;
          cleaned.fontWeight = bold ? '700' : 'normal';
          return cleaned;
        });

        reloadedPlan.push({ ...day, slides: adjusted });
      }
      updateBrandSettings({ contentPlan: reloadedPlan });
      const withPhotos = reloadedPlan.reduce((a, d) =>
        a + d.slides.filter(s => typeof s.background === 'string' && s.background.length > 5).length, 0);
      const total = reloadedPlan.reduce((a, d) => a + d.slides.length, 0);
      setSaveStatus(
        imagePool.length > 0
          ? `Neu generiert – ${withPhotos}/${total} mit Bild.`
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
          const canvasWidth = 1080;
          const canvasHeight = slide.format === '9:16' ? 1920 : 1350;
          const scale = canvasWidth / 400;
          const canvasEl = document.createElement('canvas');
          canvasEl.width = canvasWidth; canvasEl.height = canvasHeight;
          canvasEl.style.display = 'none';
          document.body.appendChild(canvasEl);
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
          if (canvasEl.parentNode) canvasEl.parentNode.removeChild(canvasEl);
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
        const canvasWidth = 1080;
        const canvasHeight = slide.format === '9:16' ? 1920 : 1350;
        const scale = canvasWidth / 400;
        const canvasEl = document.createElement('canvas');
        canvasEl.width = canvasWidth; canvasEl.height = canvasHeight;
        canvasEl.style.display = 'none';
        document.body.appendChild(canvasEl);
        const fCanvas = new fabric.StaticCanvas(canvasEl, { width: canvasWidth, height: canvasHeight });
        await renderSlide(fCanvas, { ...slide, visualElements: slide.visualElements || [] }, canvasWidth, canvasHeight, {
          slideIndex: i, totalSlides: day.slides.length, scale, globalBrandName
        });
        const dataUrl = fCanvas.toDataURL({ format: 'png', multiplier: 1 });
        const blob = await (await fetch(dataUrl)).blob();
        if (blob) zip.file(`Slide_${i + 1}.png`, blob);
        fCanvas.dispose();
        if (canvasEl.parentNode) canvasEl.parentNode.removeChild(canvasEl);
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

  // Share the day's slides as image FILES via the native share sheet.
  // On iPhone this offers "Save to Photos" / "In Fotos sichern" directly.
  const handleShareDay = async (day) => {
    if (!day || !day.slides?.length) return;
    setExportingDayId(day.day);
    try {
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || brandSettings.currentBrandConfig?.name || "MUSE MENTORING";
      const files = [];
      for (let i = 0; i < day.slides.length; i++) {
        const slide = day.slides[i];
        const canvasWidth = 1080;
        const canvasHeight = slide.format === '9:16' ? 1920 : 1350;
        const scale = canvasWidth / 400;
        const canvasEl = document.createElement('canvas');
        canvasEl.width = canvasWidth; canvasEl.height = canvasHeight;
        canvasEl.style.display = 'none';
        document.body.appendChild(canvasEl);
        const fCanvas = new fabric.StaticCanvas(canvasEl, { width: canvasWidth, height: canvasHeight });
        await renderSlide(fCanvas, { ...slide, visualElements: slide.visualElements || [] }, canvasWidth, canvasHeight, {
          slideIndex: i, totalSlides: day.slides.length, scale, globalBrandName
        });
        const dataUrl = fCanvas.toDataURL({ format: 'png', multiplier: 1 });
        const blob = await (await fetch(dataUrl)).blob();
        fCanvas.dispose();
        if (canvasEl.parentNode) canvasEl.parentNode.removeChild(canvasEl);
        if (blob) files.push(new File([blob], `Tag${day.day}_Slide${i + 1}.png`, { type: 'image/png' }));
      }

      // Try native share with files (best on mobile -> "Save to Photos")
      if (navigator.canShare && navigator.canShare({ files })) {
        await navigator.share({ files, title: `Tag ${day.day}` });
        setSaveStatus('Zum Teilen geöffnet.');
      } else {
        // Fallback: download each image individually (desktop / unsupported)
        for (const f of files) saveAs(f, f.name);
        setSaveStatus(`${files.length} Bild(er) heruntergeladen (Teilen nicht unterstützt).`);
      }
    } catch (e) {
      if (e?.name !== 'AbortError') {
        console.error("Share failed", e);
        setSaveStatus('Teilen fehlgeschlagen.');
      }
    } finally {
      setExportingDayId(null);
      setTimeout(() => setSaveStatus(''), 3000);
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
            <h1 className="text-xl font-bold text-gray-900">Content Plan <span className="text-[10px] font-normal text-purple-400 align-top">v2 Layouts</span></h1>
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
        <div>
          {weekPlan.length === 0 ? (
            <div className="text-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
              <h3 className="text-lg font-bold text-gray-700 mb-2">Noch kein Plan erstellt</h3>
              <p className="text-gray-500 mb-4">Klicke auf "Bulk Import", um deine Texte einzufügen.</p>
              <div className="flex justify-center gap-4"><button onClick={() => setShowImportModal(true)} className="bg-purple-600 text-white px-6 py-3 rounded-lg font-bold shadow-md hover:bg-purple-700 transition-colors">Bulk Import Starten</button></div>
            </div>
          ) : (
            // GRID FEED: one cover per day. Tap a cover to edit that day.
            <div className="grid grid-cols-3 gap-1">
              {weekPlan.map((day, dayIndex) => {
                const activeIndex = activeIndices[day.day] || 0;
                const activeSlide = day.slides[activeIndex] || day.slides[0];
                const dynamicActiveSlide = { ...activeSlide, visualElements: activeSlide.visualElements || [], format: activeSlide.format || '4:5' };
                const isExportingThisDay = exportingDayId === day.day;
                return (
                  <motion.div
                    key={`${day.day}-${day.title}`}
                    initial={{ opacity: 0, scale: 0.96 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: dayIndex * 0.04 }}
                    className="relative group aspect-[4/5] bg-gray-100 overflow-hidden cursor-pointer"
                    onClick={() => handleEditDay(day)}
                    title={`Tag ${day.day} – ${day.title} · tippen zum Bearbeiten`}
                  >
                    <div className="absolute inset-0 pointer-events-none">
                      <Canvas key={`${day.day}-${activeIndex}-${dynamicActiveSlide.color}-${dynamicActiveSlide.secondaryColor}-${dynamicActiveSlide.fontFamily}-${dynamicActiveSlide.backgroundColor}`} data={{...dynamicActiveSlide, slideNumber: undefined}} brandName={brandName} />
                    </div>

                    {/* Day badge */}
                    <div className="absolute top-1 left-1 bg-black/55 text-white text-[9px] font-bold px-1.5 py-0.5 rounded z-10">
                      Tag {day.day}
                    </div>

                    {/* Carousel indicator */}
                    {day.slides.length > 1 && (
                      <div className="absolute top-1 right-1 bg-black/55 text-white text-[9px] font-bold px-1.5 py-0.5 rounded z-10 flex items-center">
                        <SafeIcon icon={FiLayers} className="mr-0.5 text-[9px]" /> {day.slides.length}
                      </div>
                    )}

                    {/* Hover overlay with quick actions */}
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex flex-col items-center justify-center gap-1.5 opacity-0 group-hover:opacity-100 z-20">
                      <div className="bg-white/95 text-gray-800 text-[10px] font-bold px-2.5 py-1 rounded-full flex items-center">
                        <SafeIcon icon={FiEdit3} className="mr-1" /> Bearbeiten
                      </div>
                      <div className="flex gap-1.5">
                        <button
                          onClick={(e) => { e.stopPropagation(); handleShareDay(day); }}
                          disabled={isExportingThisDay}
                          className="bg-purple-600 text-white text-[9px] font-bold px-2 py-1 rounded-full flex items-center hover:bg-purple-700 disabled:opacity-50"
                          title="In Fotos speichern"
                        >
                          <SafeIcon icon={FiShare2} className="mr-0.5" /> Fotos
                        </button>
                        <button
                          onClick={(e) => { e.stopPropagation(); handleExportDay(day); }}
                          disabled={isExportingThisDay}
                          className="bg-white/90 text-gray-700 text-[9px] font-bold px-2 py-1 rounded-full flex items-center hover:bg-white disabled:opacity-50"
                          title="Exportieren"
                        >
                          {isExportingThisDay ? <span className="animate-spin"><SafeIcon icon={FiRefreshCw} /></span> : <><SafeIcon icon={FiDownload} className="mr-0.5" /> Export</>}
                        </button>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ContentPlanner;