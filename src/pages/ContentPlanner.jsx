import React, { useState, useEffect, useRef } from 'react';
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
import { attachSmartImages, applyEditorialHighlighting } from '../utils/smartLayoutGenerator';
import { decidePostDesign, dayHasImage } from '../utils/postDesignEngine';
import { saveSetsToDB, loadSetsFromDB } from '../utils/storage';
import { analyzePlanRoles, roleFeedback, ROLE_META } from '../utils/postRole';
import { weightedLayoutPool, getRating, setRating } from '../utils/layoutRatings';

const { FiEdit3, FiDownload, FiRefreshCw, FiZap, FiType, FiMessageSquare, FiCopy, FiExternalLink, FiUser, FiSave, FiFileText, FiThumbsUp, FiThumbsDown, FiShare2, FiLayers, FiPlus, FiCheck, FiGrid, FiImage, FiX, FiZoomIn, FiZoomOut } = FiIcons;

const ContentPlanner = () => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const navigate = useNavigate();
  const weekPlan = brandSettings.contentPlan || [];
  const [copiedKey, setCopiedKey] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeIndices, setActiveIndices] = useState({});
  const [expandedCaptionId, setExpandedCaptionId] = useState(null);
  const [showStyleShifter, setShowStyleShifter] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [isExportingAll, setIsExportingAll] = useState(false);
  const [exportDayCursor, setExportDayCursor] = useState(0); // next day index to save
  const [exportingDayId, setExportingDayId] = useState(null);
  const [saveStatus, setSaveStatus] = useState('');
  const [ratingTick, setRatingTick] = useState(0); // bump to refresh thumb UI
  const [autoApplyStyle, setAutoApplyStyle] = useState(true);

  // Saved post sets (named snapshots of the current plan).
  const [savedSets, setSavedSets] = useState([]);
  const [showSets, setShowSets] = useState(false);
  const lastImageOffsetRef = useRef(-1); // avoid repeating the same reload shuffle
  const [showStructure, setShowStructure] = useState(false);

  // Live analysis of the feed's red thread (Frage → Beweis → Angebot).
  const roleAnalysis = React.useMemo(() => analyzePlanRoles(weekPlan), [weekPlan]);

  // --- PER-CARD QUICK EDIT (same buttons as Stories & Reel Covers) ---
  const updateSlideInPlan = (dayIndex, slideIndex, updater) => {
    const plan = JSON.parse(JSON.stringify(weekPlan));
    const slide = plan[dayIndex]?.slides?.[slideIndex];
    if (!slide) return;
    plan[dayIndex].slides[slideIndex] = updater(slide);
    updateBrandSettings({ contentPlan: plan });
  };

  const handleZoomToggleDay = (dayIndex, slideIndex) => {
    updateSlideInPlan(dayIndex, slideIndex, (s) => ({
      ...s, imageScale: (s.imageScale || 1) > 1.05 ? 1 : 1.5,
    }));
  };

  const handleRemoveImageDay = (dayIndex, slideIndex) => {
    updateSlideInPlan(dayIndex, slideIndex, (s) => {
      const { background, overlay, _autoImage, ...rest } = s;
      // cover_* layouts only render on photos -> fall back to auto without one.
      const isCover = typeof rest.layout === 'string' && rest.layout.startsWith('cover_');
      return {
        ...rest,
        background: null,
        imageScale: 1,
        ...(isCover ? { layout: 'auto', layoutId: 'auto' } : {}),
      };
    });
  };

  const handleAddImageDay = async (dayIndex, slideIndex) => {
    const pool = brandSettings?.brandImages || [];
    if (pool.length === 0) { alert('Kein Bild im Pool. Lade zuerst Bilder hoch.'); return; }
    const slide = weekPlan[dayIndex]?.slides?.[slideIndex];
    if (!slide) return;
    try {
      const [withImg] = await attachSmartImages([{ ...slide }], pool, Math.floor(Math.random() * pool.length));
      updateSlideInPlan(dayIndex, slideIndex, () => ({ ...withImg, imageScale: 1 }));
    } catch (e) { console.error('Bild anhängen fehlgeschlagen:', e); }
  };

  // Explicit, always-visible layout cycle:
  // Tweet -> Postcard -> Cover links -> rechts -> oben -> unten -> von vorn.
  const handleCycleLayoutDay = (dayIndex, slideIndex) => {
    updateSlideInPlan(dayIndex, slideIndex, (s) => {
      const v = ((Number.isInteger(s.postLayoutVariant) ? s.postLayoutVariant : -1) + 1) % 6;
      const hasImg = typeof s.background === 'string' && s.background.length > 5;
      if (v === 0) {
        return { ...s, postLayoutVariant: v, layout: 'tweet_card', layoutId: 'tweet_card' };
      }
      if (v === 1) {
        return { ...s, postLayoutVariant: v, layout: 'paper_box', layoutId: 'paper_box' };
      }
      if (hasImg) {
        const coverByVariant = { 2: 'cover_mid_left', 3: 'cover_mid_right', 4: 'cover_top_center', 5: 'cover_bottom_center' };
        return { ...s, postLayoutVariant: v, layout: coverByVariant[v], layoutId: coverByVariant[v] };
      }
      const anchorByVariant = {
        2: { col: 'left', row: 'mid' },
        3: { col: 'right', row: 'mid' },
        4: { col: 'center', row: 'top' },
        5: { col: 'center', row: 'bottom' },
      };
      return { ...s, postLayoutVariant: v, layout: 'auto', layoutId: 'auto', textAnchor: anchorByVariant[v] };
    });
  };

  const handleCopyText = (text, key) => {
    navigator.clipboard?.writeText(text || '');
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 1500);
  };

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
          // Covers: big but NOT fully bold — emphasis only via **key phrases**.
          
          let finalLayout = slide.layout;
          if (sIdx === 0) {
             if (finalLayout === 'minimal_quote' && rules.vibe === 'bold_pop') {
                 finalLayout = 'maximized_bold';
             }
          }

          return {
            ...slide,
            // Bold ONE key phrase (1-4 words) per line; lines already
            // containing * markers are left untouched.
            text: applyEditorialHighlighting(slide.text || ''),
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
    // Compare font/color AND weight/text so bold-cleanup + key-phrase
    // highlighting migrate existing plans automatically on open.
    const sample = (p) => JSON.stringify({
      c: p[0]?.slides[0]?.color,
      f: p[0]?.slides[0]?.fontFamily,
      w: p[0]?.slides[0]?.fontWeight,
      t: p[0]?.slides[0]?.text,
    });
    if (sample(weekPlan) !== sample(styledPlan)) {
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

  // Load saved post sets once on mount.
  useEffect(() => {
    loadSetsFromDB().then((sets) => setSavedSets(Array.isArray(sets) ? sets : []));
  }, []);

  // Save the CURRENT plan as a named set.
  const handleSaveSet = async () => {
    if (!weekPlan.length) { setSaveStatus('Kein Plan zum Speichern vorhanden.'); return; }
    const name = window.prompt('Name für dieses Set:', `Set ${new Date().toLocaleDateString('de-AT')}`);
    if (name === null) return; // cancelled
    const newSet = {
      id: `set_${Date.now()}`,
      name: name.trim() || `Set ${savedSets.length + 1}`,
      createdAt: Date.now(),
      count: weekPlan.length,
      plan: JSON.parse(JSON.stringify(weekPlan)), // deep copy snapshot
    };
    const updated = [newSet, ...savedSets];
    setSavedSets(updated);
    await saveSetsToDB(updated);
    setSaveStatus(`✓ „${newSet.name}" gespeichert (${newSet.count} Tage).`);
    setTimeout(() => setSaveStatus(''), 4000);
  };

  // Restore a set into the current plan (replaces what's there).
  const handleRestoreSet = (set) => {
    if (!set?.plan?.length) return;
    if (weekPlan.length > 0 && !window.confirm(`Aktuellen Plan durch „${set.name}" ersetzen?`)) return;
    updateBrandSettings({ contentPlan: JSON.parse(JSON.stringify(set.plan)) });
    setShowSets(false);
    setSaveStatus(`✓ „${set.name}" wiederhergestellt.`);
    setTimeout(() => setSaveStatus(''), 4000);
  };

  const handleDeleteSet = async (setId) => {
    const updated = savedSets.filter(s => s.id !== setId);
    setSavedSets(updated);
    await saveSetsToDB(updated);
  };

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
          fontWeight: 'normal', // bold lives in **key phrases**, never whole slides
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
      // Start at a RANDOM point in the pool so every reload shifts which photo
      // lands where — otherwise the same images always map to the same slots.
      // Pick a value different from the previous reload when the pool allows it.
      let imageOffset = 0;
      if (imagePool.length > 1) {
        do {
          imageOffset = Math.floor(Math.random() * imagePool.length);
        } while (imageOffset === lastImageOffsetRef.current);
        lastImageOffsetRef.current = imageOffset;
      }
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
          cleaned.fontWeight = 'normal'; // bold only via **key phrases**
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
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || brandSettings.currentBrandConfig?.name || "MUSE MENTORING";

      const renderDayFiles = async (day) => {
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
        return files;
      };

      const canShareFiles = typeof navigator !== 'undefined' && navigator.canShare;

      // MOBILE: iOS requires a fresh user tap for each share sheet, so we save
      // ONE day per tap and advance a cursor. The button label tells the user
      // which day is next.
      if (canShareFiles) {
        const idx = exportDayCursor;
        const day = weekPlan[idx];
        if (!day) { setExportDayCursor(0); setIsExportingAll(false); return; }
        const files = await renderDayFiles(day);
        if (files.length && navigator.canShare({ files })) {
          try {
            await navigator.share({ files, title: `Tag ${day.day}` });
          } catch (e) {
            if (e?.name === 'AbortError') {
              setSaveStatus('Abgebrochen. Tippe erneut, um fortzusetzen.');
              setIsExportingAll(false);
              return;
            }
            throw e;
          }
        }
        const next = idx + 1;
        if (next >= weekPlan.length) {
          setExportDayCursor(0);
          setSaveStatus('✓ Alle Tage in Fotos gesichert.');
        } else {
          setExportDayCursor(next);
          setSaveStatus(`✓ Tag ${day.day} gesichert. Tippe für Tag ${weekPlan[next].day}.`);
        }
        setTimeout(() => setSaveStatus(''), 6000);
        setIsExportingAll(false);
        return;
      }

      // DESKTOP / no share support -> single ZIP download of everything.
      const zip = new JSZip();
      const folder = zip.folder("Content_Plan_Export");
      for (const day of weekPlan) {
        const files = await renderDayFiles(day);
        for (let i = 0; i < files.length; i++) folder.file(files[i].name, files[i]);
      }
      const content = await zip.generateAsync({ type: "blob" });
      saveAs(content, `Content_Plan.zip`);
      setSaveStatus('Als ZIP heruntergeladen.');
      setTimeout(() => setSaveStatus(''), 5000);
    } catch (e) {
      console.error("Export Failed", e);
      setSaveStatus('Export fehlgeschlagen.');
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
              <button onClick={() => setShowSets(!showSets)} className={`flex items-center px-4 py-2 rounded-lg border transition-all text-xs font-bold ${showSets ? 'bg-indigo-600 text-white border-indigo-600 shadow-inner' : 'bg-white border-indigo-200 text-indigo-700 hover:bg-indigo-50 hover:border-indigo-300 shadow-sm'}`} title="Sets speichern & wiederherstellen"><SafeIcon icon={FiSave} className="mr-2 text-sm" /> Sets{savedSets.length > 0 ? ` (${savedSets.length})` : ''}</button>
              <button onClick={() => setShowStructure(!showStructure)} disabled={weekPlan.length === 0} className={`flex items-center px-4 py-2 rounded-lg border transition-all text-xs font-bold disabled:opacity-40 ${showStructure ? 'bg-amber-600 text-white border-amber-600 shadow-inner' : 'bg-white border-amber-200 text-amber-700 hover:bg-amber-50 hover:border-amber-300 shadow-sm'}`} title="Struktur sichtbar machen"><SafeIcon icon={FiLayers} className="mr-2 text-sm" /> Struktur</button>
              </>
            )}
            <div className="h-6 w-px bg-gray-300 mx-1"></div>
            <button onClick={handleManualSave} className="p-2 hover:bg-white rounded-md text-green-700 transition-colors" title="Speichern"><SafeIcon icon={FiSave} /></button>
            <button onClick={handleExportAll} disabled={isExportingAll || loading} className="px-3 py-2 rounded-lg border bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors flex items-center gap-1 text-xs font-bold" title="Alle Tage in Fotos speichern"><SafeIcon icon={FiDownload} className={isExportingAll ? "animate-bounce" : ""} />{weekPlan.length > 0 && exportDayCursor > 0 ? `Tag ${weekPlan[exportDayCursor]?.day ?? ''} sichern` : 'Alle in Fotos'}</button>
          </div>
        </div>
        <AnimatePresence>
          {showStyleShifter && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden border-t border-gray-100 bg-gray-50"><div className="py-2"><StyleShifter mode="bar" /></div></motion.div>
          )}
          {showStructure && weekPlan.length > 0 && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden border-t border-gray-100 bg-amber-50/40">
              <div className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-bold text-gray-900 flex items-center"><SafeIcon icon={FiLayers} className="mr-2 text-amber-600" /> Dein roter Faden</h3>
                  <span className="text-[11px] text-gray-400">Struktur ersetzt das Raten</span>
                </div>

                {/* Balance bars */}
                <div className="space-y-2 mb-4">
                  {['frage', 'beweis', 'angebot'].map((role) => {
                    const meta = ROLE_META[role];
                    const pct = roleAnalysis.balance[role];
                    const count = roleAnalysis.counts[role];
                    return (
                      <div key={role} className="flex items-center gap-3">
                        <div className="w-20 shrink-0">
                          <span className="text-xs font-bold px-2 py-0.5 rounded" style={{ color: meta.color, background: meta.bg }}>{meta.label}</span>
                        </div>
                        <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                          <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: meta.color }} />
                        </div>
                        <span className="text-[11px] text-gray-500 w-16 text-right">{count}× · {pct}%</span>
                      </div>
                    );
                  })}
                </div>

                {/* Sequence across the feed */}
                <div className="mb-3">
                  <div className="text-[11px] text-gray-500 mb-1.5">Reihenfolge im Feed:</div>
                  <div className="flex flex-wrap gap-1.5">
                    {roleAnalysis.sequence.map((item, i) => {
                      const meta = ROLE_META[item.role];
                      return (
                        <div key={i} className="flex items-center gap-1 px-2 py-1 rounded-md" style={{ background: meta.bg }} title={`Tag ${item.day}: ${meta.label} — ${meta.meaning}`}>
                          <span className="text-[10px] font-bold" style={{ color: meta.color }}>{item.day}</span>
                          <span className="w-1.5 h-1.5 rounded-full" style={{ background: meta.color }} />
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Warm read on the balance */}
                <div className="flex items-start gap-2 bg-white rounded-lg p-3 border border-amber-100">
                  <SafeIcon icon={FiZap} className="text-amber-500 mt-0.5 shrink-0" />
                  <p className="text-xs text-gray-700 leading-relaxed">{roleFeedback(roleAnalysis)}</p>
                </div>

                {/* Legend */}
                <div className="flex flex-wrap gap-3 mt-3">
                  {['frage', 'beweis', 'angebot'].map((role) => {
                    const meta = ROLE_META[role];
                    return (
                      <div key={role} className="flex items-center gap-1.5">
                        <span className="w-2.5 h-2.5 rounded-full" style={{ background: meta.color }} />
                        <span className="text-[11px] text-gray-500"><b className="text-gray-700">{meta.label}:</b> {meta.meaning}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          )}
          {showSets && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden border-t border-gray-100 bg-indigo-50/40">
              <div className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-bold text-gray-900 flex items-center"><SafeIcon icon={FiSave} className="mr-2 text-indigo-600" /> Gespeicherte Sets</h3>
                  <button onClick={handleSaveSet} disabled={weekPlan.length === 0} className="px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-bold hover:bg-indigo-700 disabled:opacity-40 flex items-center"><SafeIcon icon={FiPlus} className="mr-1" /> Aktuellen Plan speichern</button>
                </div>
                {savedSets.length === 0 ? (
                  <p className="text-xs text-gray-500">Noch keine Sets gespeichert. Speichere deinen aktuellen Plan, um ihn später wiederherzustellen.</p>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    {savedSets.map((set) => (
                      <div key={set.id} className="bg-white rounded-lg border border-gray-200 p-3 flex items-center justify-between gap-2">
                        <div className="min-w-0">
                          <div className="text-sm font-bold text-gray-900 truncate">{set.name}</div>
                          <div className="text-[11px] text-gray-400">{set.count} Tage · {new Date(set.createdAt).toLocaleDateString('de-AT')}</div>
                        </div>
                        <div className="flex items-center gap-1 shrink-0">
                          <button onClick={() => handleRestoreSet(set)} className="px-2 py-1 rounded-md bg-indigo-100 text-indigo-700 text-[11px] font-bold hover:bg-indigo-200" title="Wiederherstellen">Laden</button>
                          <button onClick={() => handleDeleteSet(set.id)} className="p-1.5 rounded-md text-gray-400 hover:text-red-600 hover:bg-red-50" title="Löschen"><SafeIcon icon={FiRefreshCw} className="hidden" /><span className="text-[11px] font-bold">✕</span></button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
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
                      <Canvas key={`${day.day}-${activeIndex}-${dynamicActiveSlide.color}-${dynamicActiveSlide.secondaryColor}-${dynamicActiveSlide.fontFamily}-${dynamicActiveSlide.backgroundColor}`} data={{...dynamicActiveSlide, slideNumber: activeIndex + 1, totalSlides: day.slides.length}} brandName={brandName} />
                    </div>

                    {/* Day badge */}
                    <div className="absolute top-1 left-1 bg-black/55 text-white text-[9px] font-bold px-1.5 py-0.5 rounded z-10">
                      Tag {day.day}
                    </div>

                    {/* Role badge (only when structure view is on) */}
                    {showStructure && (() => {
                      const role = roleAnalysis.sequence.find(s => s.day === day.day)?.role || 'beweis';
                      const meta = ROLE_META[role];
                      return (
                        <div className="absolute bottom-1 left-1 text-[9px] font-bold px-1.5 py-0.5 rounded z-10" style={{ color: meta.color, background: meta.bg }}>
                          {meta.label}
                        </div>
                      );
                    })()}

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
                      <div className="flex gap-1.5 mt-0.5">
                        <button
                          onClick={(e) => { e.stopPropagation(); handleCopyText(activeSlide?.text, `${day.day}-${activeIndex}`); }}
                          title="Text kopieren"
                          className={`p-1.5 rounded-full shadow bg-white/95 hover:text-purple-600 flex items-center justify-center ${copiedKey === `${day.day}-${activeIndex}` ? 'text-green-600' : 'text-gray-800'}`}
                        >
                          <SafeIcon icon={copiedKey === `${day.day}-${activeIndex}` ? FiCheck : FiCopy} className="text-xs" />
                        </button>
                        <button
                          onClick={(e) => { e.stopPropagation(); handleCycleLayoutDay(dayIndex, activeIndex); }}
                          title="Layout wechseln"
                          className="p-1.5 rounded-full shadow bg-white/95 text-gray-800 hover:text-purple-600 flex items-center justify-center"
                        >
                          <SafeIcon icon={FiGrid} className="text-xs" />
                        </button>
                        {(typeof activeSlide?.background === 'string' && activeSlide.background.length > 5) ? (
                          <>
                            <button
                              onClick={(e) => { e.stopPropagation(); handleZoomToggleDay(dayIndex, activeIndex); }}
                              title={(activeSlide.imageScale || 1) > 1.05 ? 'Zoom aus' : 'Zoom'}
                              className={`p-1.5 rounded-full shadow bg-white/95 hover:text-purple-600 flex items-center justify-center ${(activeSlide.imageScale || 1) > 1.05 ? 'text-purple-600' : 'text-gray-800'}`}
                            >
                              <SafeIcon icon={(activeSlide.imageScale || 1) > 1.05 ? FiZoomOut : FiZoomIn} className="text-xs" />
                            </button>
                            <button
                              onClick={(e) => { e.stopPropagation(); handleRemoveImageDay(dayIndex, activeIndex); }}
                              title="Bild entfernen"
                              className="p-1.5 rounded-full shadow bg-white/95 text-red-500 hover:bg-red-50 flex items-center justify-center"
                            >
                              <SafeIcon icon={FiX} className="text-xs" />
                            </button>
                          </>
                        ) : (
                          <button
                            onClick={(e) => { e.stopPropagation(); handleAddImageDay(dayIndex, activeIndex); }}
                            title="Bild einfügen"
                            className="p-1.5 rounded-full shadow bg-white/95 text-gray-800 hover:text-purple-600 flex items-center justify-center"
                          >
                            <SafeIcon icon={FiImage} className="text-xs" />
                          </button>
                        )}
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