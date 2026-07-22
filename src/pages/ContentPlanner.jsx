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
import FeedStyleBar from '../components/FeedStyleBar';
import ScreenshotMatchModal from '../components/ScreenshotMatchModal';
import { parseScreenshotPlaceholder } from '../utils/screenshotMatcher';
import { CloudService } from '../services/cloudService';
import { useAuth } from '../context/AuthContext';
import BulkImportModal from '../components/BulkImportModal';
import { renderSlide } from '../utils/canvasRenderer';
import { brandRuleSets } from '../constants/brandData';
import { createSmartSlide } from '../utils/slideHelpers';
import { attachSmartImages, getActiveImagePool } from '../utils/smartLayoutGenerator';
import { decidePostDesign, dayHasImage } from '../utils/postDesignEngine';
import { saveSetsToDB, loadSetsFromDB } from '../utils/storage';
import { analyzePlanRoles, roleFeedback, ROLE_META } from '../utils/postRole';
import { weightedLayoutPool, getRating, setRating } from '../utils/layoutRatings';

const { FiEdit3, FiDownload, FiRefreshCw, FiZap, FiType, FiMessageSquare, FiCopy, FiExternalLink, FiUser, FiSave, FiFileText, FiThumbsUp, FiThumbsDown, FiShare2, FiLayers, FiPlus , FiMoreVertical, FiMaximize2, FiGrid, FiImage } = FiIcons;

const ContentPlanner = () => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const { user } = useAuth();
  const navigate = useNavigate();
  const weekPlan = brandSettings.contentPlan || [];
  const [loading, setLoading] = useState(false);
  const [activeIndices, setActiveIndices] = useState({});
  const [expandedCaptionId, setExpandedCaptionId] = useState(null);
  const [menuDayId, setMenuDayId] = useState(null); // tile context menu (mobile-friendly)
  const [showStyleShifter, setShowStyleShifter] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [showScreenshotModal, setShowScreenshotModal] = useState(false);
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
  const lastDayOffsetRef = useRef({});   // per-day offset so each day reshuffles
  const [reloadingDay, setReloadingDay] = useState(null);
  const [showStructure, setShowStructure] = useState(false);

  // Live analysis of the feed's red thread (Frage → Beweis → Angebot).
  const roleAnalysis = React.useMemo(() => analyzePlanRoles(weekPlan), [weekPlan]);

  const currentBrand = brandSettings.currentBrandConfig;
  const hasActiveBrand = !!currentBrand;
  const brandName = (() => {
    const isReal = (v) => typeof v === 'string' && v.trim()
      && !['www.deine-website.de', 'dein.business', 'Dein Name | Expertin'].includes(v.trim());
    const cfg = currentBrand || {};
    // Priority: explicit brand line → website → handle → brand name.
    if (isReal(cfg.brandText)) return cfg.brandText.trim();
    if (isReal(brandSettings?.website)) return brandSettings.website.trim().replace(/^www\./, '');
    if (isReal(brandSettings?.username)) return brandSettings.username.trim();
    if (isReal(cfg.name)) return cfg.name.trim();
    return '';
  })();

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
  // Map a photo/frame layout to a matching TEXT layout, used when the rotation
  // assigns a photo layout but no image is available for that slide. Keeps a
  // similar character (big word -> big word, quote -> quote, etc.).
  const photoToTextLayout = (layoutId) => {
    const map = {
      brand_photo_gradient: 'brand_text_plate',
      brand_photo_bottom_left: 'brand_text_left',
      brand_photo_top: 'brand_text_plate_top',
      brand_photo_center: 'brand_text_plate',
      brand_photo_bigword: 'brand_text_bigword',
      brand_photo_quote: 'brand_text_quote',
      brand_photo_bottom_serif: 'brand_text_statement',
      brand_photo_frame: 'brand_text_plate',
      brand_frame_top_text: 'brand_text_plate_top',
      brand_frame_left: 'brand_text_left',
      brand_frame_polaroid: 'brand_text_minimal',
    };
    return map[layoutId] || 'brand_text_plate';
  };

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
        slides: (Array.isArray(day.slides) ? day.slides : []).map((slide, sIdx, allSlides) => {
          const font = sIdx === 0 ? fonts.fontFamily : (fonts.bodyFontFamily || 'Montserrat');
          const accentFont = fonts.accentFontFamily || (font.includes('Playfair') ? 'Montserrat' : 'Playfair Display');
          const isPlayfair = font.includes('Playfair');
          let weight = '400';
          if (sIdx === 0 && !isPlayfair) weight = fonts.fontWeight || '700';
          
          let finalLayout = slide.layout;
          // Brand layouts (brand_*) are self-contained and colour-adjustable.
          // They must survive brand styling untouched — never normalized to the
          // Editorial 'auto' path, or the 20 layouts would collapse to one look.
          const isBrandLayout = typeof finalLayout === 'string' && finalLayout.startsWith('brand_');
          if (sIdx === 0 && !isBrandLayout) {
             if (finalLayout === 'minimal_quote' && rules.vibe === 'bold_pop') {
                 finalLayout = 'maximized_bold';
             }
          }
          // Editorial preset: EVERY slide goes through the adaptive auto layout.
          // Legacy layouts stored on individual slides (from older imports or
          // added days) made single posts render completely differently — wrong
          // position, no CAPS lines, no brand mark. Normalize them away — EXCEPT
          // brand layouts, which render themselves.
          // Per-day override: a day set to 'editorial' forces the editorial look;
          // a day set to 'brand' keeps its brand layout regardless of the global.
          const dayMode = day.dayLayoutMode;
          const editorialActive = dayMode === 'editorial'
            || (dayMode !== 'brand' && (config.editorialDark === true || config.ruleSet === 'editorial_dark'));
          if (editorialActive && !isBrandLayout) finalLayout = 'auto';

          // --- Cover-Blur (pro Post) & CTA-Foto ---
          // coverBlurMode liegt am TAG (day), nicht an der Brand: jeder Post
          // kann eigenständig entscheiden, ob Folgeseiten das Coverfoto nutzen.
          const coverBlurMode = day.coverBlurMode === true;
          const ctaImage = config.ctaImage || null;
          const isLast = sIdx === allSlides.length - 1;
          const coverBg = allSlides[0]?.background;
          let bgOverride = slide.background;
          let isCtaSlide = false;
          // Follow-up slides reuse the cover photo (blur/darkening happens in
          // the renderer). Only when the mode is on and a cover photo exists.
          if (coverBlurMode && sIdx > 0 && typeof coverBg === 'string' && coverBg.length > 5) {
            bgOverride = coverBg;
          }
          // The last slide is the call-to-action: use the fixed CTA photo and
          // keep it SHARP — it's a deliberate choice, not a background.
          if (ctaImage && isLast && allSlides.length > 1) {
            bgOverride = ctaImage;
            isCtaSlide = true;
          }

          // For brand layouts, drive their colour slots from the palette so the
          // feed uses the brand's colours (not the dark Editorial defaults).
          // Photo layouts -> overlayColor is the scrim; plate layouts -> the
          // backgroundColor is the plate. Text stays high-contrast.
          let brandBg = bg, brandText = text, brandOverlay = slide.overlayColor;
          const isPhotoLayout = isBrandLayout && (finalLayout.includes('photo') || finalLayout.includes('frame'));
          if (isBrandLayout) {
            if (isPhotoLayout) {
              // The scrim/gradient over a photo must be DARK so white text always
              // reads. Prefer the brand BACKGROUND colour (that's the swatch the
              // user edits in the feed bar, so the gradient visibly follows it);
              // if the background is light, fall back to the darkest palette tone,
              // then to near-black.
              let ov = colors.background;
              if (!ov || !isDark(ov)) {
                const darkCandidates = [colors.primary, colors.tertiary, colors.secondary, colors.neutral, colors.background]
                  .filter((c) => c && isDark(c));
                ov = darkCandidates[0] || '#1A1512';
              }
              brandOverlay = ov;
              // White text on the dark scrim — guaranteed readable.
              brandText = '#FFFFFF';
              brandBg = colors.background; // plate behind, if no photo
            } else {
              // Text plate — rotate the plate colour across the feed so tiles
              // alternate dark / light / accent (like the reference feeds),
              // instead of every text tile being the same colour. The rotation
              // is keyed on the day index so each day differs from its neighbours.
              const isDarkBg = isDark(colors.background);
              // Build a small palette of plate options from the brand colours.
              const darkPlate = isDarkBg ? colors.background : (colors.neutral && isDark(colors.neutral) ? colors.neutral : colors.primary);
              const lightPlate = isDarkBg ? (colors.neutral && !isDark(colors.neutral) ? colors.neutral : '#F2EEE9') : colors.background;
              const accentPlate = colors.secondary || colors.accent;
              const plateCycle = [
                { bg: darkPlate,   tx: '#FFFFFF' },
                { bg: lightPlate,  tx: isDark(lightPlate) ? '#FFFFFF' : (colors.primary && isDark(colors.primary) ? colors.primary : '#1A1512') },
                { bg: accentPlate, tx: isDark(accentPlate) ? '#FFFFFF' : '#1A1512' },
              ];
              const pick = plateCycle[index % plateCycle.length];
              brandBg = pick.bg || '#EDE9E3';
              brandText = pick.tx;
            }
          }

          // Auto contrast text: on plate layouts, always pick a readable colour
          // for the chosen plate (white on dark, near-black on light), unless the
          // user overrode it per slide.
          if (isBrandLayout && !isPhotoLayout) {
            brandText = isDark(brandBg) ? '#FFFFFF' : '#1A1512';
          }

          // Per-slide manual override wins: if the user set colours in the editor
          // for THIS slide, keep them untouched (brand/feed styling doesn't stomp
          // on a deliberate choice).
          if (slide._colorOverride) {
            return {
              ...slide,
              background: bgOverride,
              coverBlurMode: coverBlurMode && !isCtaSlide,
              isCtaSlide,
              // keep the slide's own colours
              layout: finalLayout,
              layoutId: isBrandLayout ? finalLayout : (editorialActive ? 'auto' : (slide.layoutId || finalLayout)),
              fontFamily: font,
              headlineTracking: (typeof config.headlineTracking === 'number') ? config.headlineTracking : -30,
              editorialDark: isBrandLayout ? false : (config.editorialDark === true || config.ruleSet === 'editorial_dark'),
            };
          }

          return {
            ...slide,
            background: bgOverride,
            coverBlurMode: coverBlurMode && !isCtaSlide,
            isCtaSlide,
            color: isBrandLayout ? brandText : text,
            backgroundColor: isBrandLayout ? brandBg : bg,
            overlayColor: isBrandLayout ? brandOverlay : slide.overlayColor,
            secondaryColor: sec,
            accentColor: acc,
            fontFamily: font,
            // Headline letter spacing from the brand (default slightly tight).
            headlineTracking: (typeof config.headlineTracking === 'number') ? config.headlineTracking : -30,
            boldMode: config.boldMode === true,
            // In Bold Statement mode the feed VARIES like the reference (not one
            // loud font on every tile): rotate the headline treatment per slide.
            //  0 -> Anton display caps (loud)
            //  1 -> Playfair italic serif (elegant statement)
            //  2 -> Montserrat black caps (clean bold)
            boldStyle: config.boldMode === true ? (index % 3) : undefined,
            accentFontFamily: accentFont,
            fontWeight: weight,
            visualElements: config.visualElements || [],
            layout: finalLayout,
            layoutId: isBrandLayout ? finalLayout : (editorialActive ? 'auto' : (slide.layoutId || finalLayout)),
            // Editorial Dark preset flags — drive the photo wash and kicker.
            // Disabled for brand layouts so they keep full colour control.
            darkPhoto: isBrandLayout ? false : (config.darkPhoto === true),
            editorialDark: isBrandLayout ? false : (config.editorialDark === true || config.ruleSet === 'editorial_dark'),
            // Clear legacy kicker fields stored by older builds.
            kicker: false,
            kickerText: undefined,
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
    // Compare across ALL days and a follow-up slide too — the cover slide never
    // changes when cover-blur or the CTA photo is toggled, so a narrow sample
    // would wrongly skip the update.
    const sampleOf = (p) => JSON.stringify((p || []).map((d) => {
      const sl = Array.isArray(d?.slides) ? d.slides : [];
      return {
        cb: d?.coverBlurMode === true,
        s0: { c: sl[0]?.color, f: sl[0]?.fontFamily, e: sl[0]?.editorialDark === true, d: sl[0]?.darkPhoto === true },
        s1: { b: sl[1]?.background, cb: sl[1]?.coverBlurMode === true },
        last: sl.length ? sl[sl.length - 1]?.background : undefined,
      };
    }));
    if (sampleOf(weekPlan) !== sampleOf(styledPlan)) {
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

  // Toggle the BIG headline on the cover slide (slide 1) of one day — the
  // same per-slide switch as in the Editor, reachable from the feed.
  const toggleBigHeadline = (dayNum) => {
    const updated = weekPlan.map((d) => {
      if (d.day !== dayNum) return d;
      const slides = (d.slides || []).map((s, i) => (i === 0 ? { ...s, bigHeadline: s.bigHeadline !== true } : s));
      return { ...d, slides };
    });
    updateBrandSettings({ contentPlan: applyBrandStyling(updated, currentBrand) });
  };

  // Toggle cover-blur for ONE post (day): follow-up slides reuse the cover
  // photo, blurred and slightly darkened.
  // Feed-level colour/font editing — updates the brand config and re-applies
  // styling to every slide so the whole feed changes instantly.
  const handleFeedColors = (newColors) => {
    if (!currentBrand) return;
    const updatedConfig = { ...currentBrand, colors: newColors };
    const restyled = applyBrandStyling(brandSettings.contentPlan || [], updatedConfig);
    updateBrandSettings({ currentBrandConfig: updatedConfig, contentPlan: restyled });
  };
  const handleFeedFont = (font) => {
    if (!currentBrand) return;
    const updatedConfig = {
      ...currentBrand,
      typography: { ...(currentBrand.typography || {}), fontFamily: font },
    };
    const restyled = applyBrandStyling(brandSettings.contentPlan || [], updatedConfig);
    updateBrandSettings({ currentBrandConfig: updatedConfig, contentPlan: restyled });
  };

  // Collect all slides whose text is a [SCREENSHOT — …] placeholder, with a
  // stable key (day.day + slide index) so we can write the overlay back.
  const collectScreenshotPlaceholders = () => {
    const out = [];
    (brandSettings.contentPlan || []).forEach((day) => {
      (day.slides || []).forEach((slide, sIdx) => {
        const matchText = parseScreenshotPlaceholder(slide.text);
        if (matchText) out.push({ id: `${day.day}_${sIdx}`, matchText });
      });
    });
    return out;
  };

  // Apply the OCR mapping: upload each matched screenshot to Supabase Storage
  // (so it persists and doesn't bloat the plan as base64), then place the
  // returned URL as an overlay image on its slide and clear the placeholder.
  const applyScreenshots = async (mapping) => {
    // Upload each unique screenshot once; map placeholder key -> stored URL.
    const urlByKey = {};
    const entries = Object.entries(mapping);
    setSaveStatus && setSaveStatus('Screenshots werden gespeichert…');
    for (const [key, dataUrl] of entries) {
      // If already an http(s) URL (re-applied), keep it; else upload the base64.
      if (typeof dataUrl === 'string' && /^https?:\/\//.test(dataUrl)) {
        urlByKey[key] = dataUrl;
      } else {
        urlByKey[key] = user
          ? await CloudService.uploadScreenshot(user.id, dataUrl)
          : dataUrl; // not logged in -> keep inline base64
      }
    }

    const updated = (brandSettings.contentPlan || []).map((day) => ({
      ...day,
      slides: (day.slides || []).map((slide, sIdx) => {
        const key = `${day.day}_${sIdx}`;
        if (!urlByKey[key]) return slide;
        return {
          ...slide,
          overlayImage: urlByKey[key],   // stored URL (or base64 fallback)
          overlayIsScreenshot: true,     // rectangular card, large + readable
          overlayImageScale: 0.8,        // ~80% of the tile width
          overlayImageRounded: false,
          overlayImageX: 0,
          overlayImageY: 0,
          text: '',                      // remove the placeholder text
          _wasScreenshot: true,
        };
      }),
    }));
    updateBrandSettings({ contentPlan: updated });
    setSaveStatus && setSaveStatus('Screenshots gespeichert');
    setTimeout(() => setSaveStatus && setSaveStatus(''), 1500);
  };

  const toggleCoverBlur = (dayNum) => {
    const updated = weekPlan.map((d) => (d.day === dayNum ? { ...d, coverBlurMode: !d.coverBlurMode } : d));
    updateBrandSettings({ contentPlan: applyBrandStyling(updated, currentBrand) });
  };

  // Toggle a single day between the default brand layouts and Dark Editorial,
  // reassigning each slide's layout so the switch is visible immediately.
  const toggleDayLayoutMode = (dayNum) => {
    const rotation = buildLayoutRotation();
    let idx = 0;
    const updated = weekPlan.map((d) => {
      if (d.day !== dayNum) {
        // keep global index advancing so the rotation stays stable elsewhere
        idx += (d.slides || []).length;
        return d;
      }
      const nextMode = d.dayLayoutMode === 'editorial' ? 'brand' : 'editorial';
      const slides = (d.slides || []).map((slide) => {
        const s = { ...slide };
        if (nextMode === 'editorial') {
          s.layout = 'auto'; s.layoutId = 'auto';
          s.editorialDark = true;
        } else {
          const picked = rotation[idx % rotation.length];
          s.layout = picked; s.layoutId = picked;
          s.editorialDark = false; s.darkPhoto = false;
        }
        idx++;
        return s;
      });
      return { ...d, dayLayoutMode: nextMode, slides };
    });
    updateBrandSettings({ contentPlan: applyBrandStyling(updated, currentBrand) });
  };

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
    // Fixed feed-style pattern using the 20 brand layouts. The order mimics a
    // real personal-brand grid: photo hooks, text plates, framed/quote posts,
    // big-word statements — repeating so every reload keeps the same rhythm.
    return [
      'brand_photo_gradient',
      'brand_text_plate',
      'brand_photo_center',
      'brand_frame_polaroid',
      'brand_text_bigword',
      'brand_photo_bottom_left',
      'brand_text_quote',
      'brand_photo_top',
      'brand_text_statement',
      'brand_photo_frame',
      'brand_text_left',
      'brand_photo_bigword',
      'brand_text_plate_top',
      'brand_frame_top_text',
      'brand_photo_quote',
      'brand_text_kicker_lead',
      'brand_photo_bottom_serif',
      'brand_text_minimal',
      'brand_frame_left',
      'brand_text_bold_top',
    ];
  };

  const handleImportPlan = async (importedDays) => {
    setLoading(true);
    const brandConfig = brandSettings.currentBrandConfig;
    const imagePool = getActiveImagePool(brandSettings);

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

      const rotation = buildLayoutRotation(brandConfig);
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
        // Assign a brand layout from the fixed feed pattern by position.
        let picked = rotation[globalIndex % rotation.length];
        const pickedIsPhoto = typeof picked === 'string' && (picked.includes('photo') || picked.includes('frame'));
        if (pickedIsPhoto && !hasImg) picked = photoToTextLayout(picked);
        globalIndex++;
        return {
          ...s2,
          layout: picked, layoutId: picked,
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
  // Reload ONE day: give this post fresh photos without touching the others.
  const handleReloadDay = async (dayNum) => {
    const dayIdx = weekPlan.findIndex((d) => d.day === dayNum);
    if (dayIdx === -1) return;
    setReloadingDay(dayNum);
    try {
      const imagePool = getActiveImagePool(brandSettings);
      const day = weekPlan[dayIdx];
      const wantsImage = dayHasImage(dayIdx) && imagePool.length > 0;

      let imageOffset = 0;
      if (imagePool.length > 1) {
        const prev = lastDayOffsetRef.current[dayNum];
        do { imageOffset = Math.floor(Math.random() * imagePool.length); }
        while (imagePool.length > 1 && imageOffset === prev);
        lastDayOffsetRef.current[dayNum] = imageOffset;
      }

      let daySlides = day.slides || [];
      if (wantsImage) daySlides = await attachSmartImages(daySlides, imagePool, imageOffset);

      const adjusted = daySlides.map((slide) => {
        const cleaned = { ...slide };
        const hasImg = wantsImage && typeof cleaned.background === 'string' && cleaned.background.length > 5;
        if (!hasImg) {
          const { background, overlay, _autoImage, ...rest } = cleaned;
          Object.assign(cleaned, rest, { background: null, overlay: undefined, _autoImage: undefined });
        }
        const { textAnchor, bold } = decidePostDesign({
          globalIndex: dayIdx, hasImage: hasImg, autoImage: cleaned._autoImage,
        });
        const _rot = buildLayoutRotation();
        let _picked = _rot[dayIdx % _rot.length];
        const _pickedIsPhoto = typeof _picked === 'string' && (_picked.includes('photo') || _picked.includes('frame'));
        if (_pickedIsPhoto && !hasImg) _picked = photoToTextLayout(_picked);
        cleaned.layout = _picked;
        cleaned.layoutId = _picked;
        cleaned.textAnchor = textAnchor;
        cleaned.fontWeight = bold ? '700' : 'normal';
        // Keep the per-slide serif/caps switch.
        if (slide.serifHeadline === false) cleaned.serifHeadline = false;
        return cleaned;
      });

      const updated = weekPlan.map((d, i) => (i === dayIdx ? { ...d, slides: adjusted } : d));
      updateBrandSettings({ contentPlan: applyBrandStyling(updated, currentBrand) });
      setSaveStatus(`Tag ${dayNum} neu geladen.`);
      setTimeout(() => setSaveStatus(''), 2500);
    } catch (e) {
      console.error('single day reload failed', e);
      setSaveStatus('Neu laden fehlgeschlagen.');
    } finally {
      setReloadingDay(null);
    }
  };

  // Cover rule: of the 7 day-covers, days 1,3,5,7 get a background image,
  // days 2,4,6 stay image-free (layout only). Content slides keep images.
  const handleReloadPlan = async () => {
    if (!weekPlan || weekPlan.length === 0) return;
    setLoading(true);
    setSaveStatus('Lade Posts neu...');
    try {
      const imagePool = getActiveImagePool(brandSettings);

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
      let layoutCursor = 0; // tracks rotation position across days
      const rotationAll = buildLayoutRotation();
      for (let dayIdx = 0; dayIdx < weekPlan.length; dayIdx++) {
        const day = weekPlan[dayIdx];
        const dayIsEditorial = day.dayLayoutMode === 'editorial';
        const nSlides = (day.slides || []).length || 1;
        // Determine the layouts this day will get, so we know whether it needs
        // photos. A day needs images if it's Editorial, or if ANY of its slides
        // lands on a photo/frame layout.
        const dayLayouts = [];
        for (let k = 0; k < nSlides; k++) {
          dayLayouts.push(rotationAll[(layoutCursor + k) % rotationAll.length]);
        }
        const dayNeedsPhoto = dayIsEditorial || dayLayouts.some(
          (l) => typeof l === 'string' && (l.includes('photo') || l.includes('frame'))
        );
        const wantsImage = dayNeedsPhoto && imagePool.length > 0;
        let daySlides = day.slides;
        if (wantsImage) {
          daySlides = await attachSmartImages(day.slides, imagePool, imageOffset);
          imageOffset += daySlides.length;
        }

        const adjusted = daySlides.map((slide, slideIdx) => {
          const cleaned = { ...slide };
          if (cleaned.blur === 8 || cleaned.blur === 12) cleaned.blur = 0;

          const _picked2 = rotationAll[layoutCursor % rotationAll.length];
          const pickedIsPhoto = typeof _picked2 === 'string' && (_picked2.includes('photo') || _picked2.includes('frame'));
          // Only keep a background if this specific slide's layout uses one.
          const hasImg = wantsImage && (pickedIsPhoto || dayIsEditorial)
            && typeof cleaned.background === 'string' && cleaned.background.length > 5;
          if (!hasImg) {
            const { background, overlay, _autoImage, ...rest } = cleaned;
            Object.assign(cleaned, rest, { background: null, overlay: undefined, _autoImage: undefined });
          }
          const { textAnchor, bold } = decidePostDesign({
            globalIndex, hasImage: hasImg, autoImage: cleaned._autoImage,
          });
          layoutCursor++;
          globalIndex++;
          if (dayIsEditorial) {
            // Dark Editorial for this day.
            cleaned.layout = 'auto';
            cleaned.layoutId = 'auto';
            const cfg = brandSettings.currentBrandConfig || {};
            cleaned.editorialDark = true;
            cleaned.darkPhoto = cfg.darkPhoto === true;
          } else {
            // Default: brand layout from the fixed rotation. If the rotation
            // handed this slide a PHOTO layout but there's no image for it,
            // swap to a matching TEXT layout so it never renders as an empty
            // dark plate.
            let chosen = _picked2;
            if (pickedIsPhoto && !hasImg) {
              chosen = photoToTextLayout(_picked2);
            }
            cleaned.layout = chosen;
            cleaned.layoutId = chosen;
            cleaned.editorialDark = false;
            cleaned.darkPhoto = false;
          }
          cleaned.kicker = false;
          cleaned.kickerText = undefined;
          cleaned.coverBlurMode = day.coverBlurMode === true;
          // Preserve the per-slide serif/caps switch across reloads.
          if (slide.serifHeadline === false) cleaned.serifHeadline = false;
          cleaned.textAnchor = textAnchor;
          cleaned.fontWeight = bold ? '700' : 'normal';
          return cleaned;
        });

        reloadedPlan.push({ ...day, slides: adjusted });
      }
      // Run brand styling so the CTA photo and per-post cover-blur are applied
      // to the freshly assigned images.
      updateBrandSettings({ contentPlan: applyBrandStyling(reloadedPlan, currentBrand) });
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
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || "";

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
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || "";
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
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || "";
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
      <ScreenshotMatchModal
        isOpen={showScreenshotModal}
        onClose={() => setShowScreenshotModal(false)}
        placeholders={collectScreenshotPlaceholders()}
        onApply={applyScreenshots}
      />
      <div className="sticky top-[64px] z-30 bg-white/95 backdrop-blur border-b border-gray-200 shadow-sm -mx-4 sm:-mx-6 px-4 sm:px-6 transition-all">
        <div className="py-3 flex flex-col md:flex-row justify-between items-center max-w-4xl mx-auto gap-3">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Content Plan <span className="text-[10px] font-normal text-purple-400 align-top">v2 Layouts</span></h1>
            <p className="text-xs text-gray-500 flex items-center mt-1"><SafeIcon icon={FiUser} className="mr-1 text-purple-500" /> Füge deine Texte per Bulk Import ein.</p>
          </div>
          <div className="flex flex-wrap gap-2 items-center justify-end">
            <button onClick={() => setShowImportModal(true)} className="px-3 py-2 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 transition-colors flex items-center shadow-md whitespace-nowrap text-xs"><SafeIcon icon={FiFileText} className="mr-2" /> Bulk Import</button>
            <button onClick={() => setShowScreenshotModal(true)} className="px-3 py-2 bg-white border border-purple-200 text-purple-700 rounded-lg font-bold hover:bg-purple-50 transition-colors flex items-center shadow-sm whitespace-nowrap text-xs"><SafeIcon icon={FiImage} className="mr-2" /> Screenshots</button>
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
      {hasActiveBrand && weekPlan.length > 0 && (
        <FeedStyleBar
          colors={currentBrand?.colors}
          typography={currentBrand?.typography}
          onColors={handleFeedColors}
          onFont={handleFeedFont}
        />
      )}
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


                    {/* Menu button — always visible (no hover on mobile) */}
                    <button
                      onClick={(e) => { e.stopPropagation(); setMenuDayId(menuDayId === day.day ? null : day.day); }}
                      className="absolute top-1.5 right-1.5 z-30 w-7 h-7 rounded-full bg-black/40 backdrop-blur text-white flex items-center justify-center shadow active:scale-90 transition-transform"
                      title="Aktionen"
                      aria-label="Aktionen"
                    >
                      <SafeIcon icon={FiMoreVertical} className="text-xs" />
                    </button>

                    {/* Action sheet — fixed & centered so it's never clipped */}
                    {menuDayId === day.day && (
                      <div className="fixed inset-0 z-[60] flex items-end justify-center" onClick={(e) => { e.stopPropagation(); setMenuDayId(null); }}>
                        <div className="absolute inset-0 bg-black/40" />
                        <div className="relative w-full max-w-sm bg-white rounded-t-2xl shadow-2xl pb-[env(safe-area-inset-bottom)] animate-slide-up" onClick={(e) => e.stopPropagation()}>
                          <div className="flex items-center justify-between px-4 pt-3 pb-2 border-b border-gray-100">
                            <span className="text-sm font-bold text-gray-900">Tag {day.day}</span>
                            <button onClick={() => setMenuDayId(null)} className="w-7 h-7 rounded-full bg-gray-100 text-gray-500 flex items-center justify-center"><span className="text-sm font-bold leading-none">✕</span></button>
                          </div>
                          <button onClick={() => { setMenuDayId(null); handleEditDay(day); }} className="w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50">
                            <SafeIcon icon={FiEdit3} className="text-base text-gray-500" /> Bearbeiten
                          </button>
                          <button onClick={() => { setMenuDayId(null); handleReloadDay(day.day); }} disabled={reloadingDay === day.day} className="w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50 disabled:opacity-50">
                            <SafeIcon icon={FiRefreshCw} className={`text-base text-gray-500 ${reloadingDay === day.day ? 'animate-spin' : ''}`} /> Neu laden
                          </button>
                          <button onClick={() => { setMenuDayId(null); toggleDayLayoutMode(day.day); }} className="w-full flex items-center justify-between px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50">
                            <span className="flex items-center gap-3">
                              <SafeIcon icon={FiGrid} className={`text-base ${day.dayLayoutMode === 'editorial' ? 'text-gray-900' : 'text-purple-500'}`} /> Layout-Stil
                            </span>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${day.dayLayoutMode === 'editorial' ? 'bg-gray-900 text-white' : 'bg-purple-500 text-white'}`}>{day.dayLayoutMode === 'editorial' ? 'Dark Editorial' : 'Default'}</span>
                          </button>
                          <button onClick={() => { setMenuDayId(null); toggleCoverBlur(day.day); }} className="w-full flex items-center justify-between px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50">
                            <span className="flex items-center gap-3">
                              <SafeIcon icon={FiLayers} className={`text-base ${day.coverBlurMode ? 'text-amber-500' : 'text-gray-500'}`} /> Unschärfe Folgeseiten
                            </span>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${day.coverBlurMode ? 'bg-amber-500 text-white' : 'bg-gray-200 text-gray-500'}`}>{day.coverBlurMode ? 'An' : 'Aus'}</span>
                          </button>
                          <button onClick={() => { setMenuDayId(null); toggleBigHeadline(day.day); }} className="w-full flex items-center justify-between px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50">
                            <span className="flex items-center gap-3">
                              <SafeIcon icon={FiMaximize2} className={`text-base ${day.slides?.[0]?.bigHeadline ? 'text-purple-600' : 'text-gray-500'}`} /> Große Headline
                            </span>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${day.slides?.[0]?.bigHeadline ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-500'}`}>{day.slides?.[0]?.bigHeadline ? 'An' : 'Aus'}</span>
                          </button>
                          <button onClick={() => { setMenuDayId(null); setExpandedCaptionId(expandedCaptionId === day.day ? null : day.day); }} className="w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 border-b border-gray-50">
                            <SafeIcon icon={FiMessageSquare} className="text-base text-gray-500" /> Caption
                          </button>
                          <button onClick={() => { setMenuDayId(null); handleShareDay(day); }} disabled={isExportingThisDay} className="w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-purple-700 hover:bg-purple-50 border-b border-gray-50 disabled:opacity-50">
                            <SafeIcon icon={FiShare2} className="text-base" /> In Fotos speichern
                          </button>
                          <button onClick={() => { setMenuDayId(null); handleExportDay(day); }} disabled={isExportingThisDay} className="w-full flex items-center gap-3 px-4 py-3.5 text-sm font-bold text-gray-800 hover:bg-gray-50 disabled:opacity-50">
                            <SafeIcon icon={FiDownload} className="text-base text-gray-500" /> Export
                          </button>
                        </div>
                      </div>
                    )}


                    {/* Collapsible caption panel (restored from the old day view) */}
                    {expandedCaptionId === day.day && (
                      <div className="absolute inset-x-0 bottom-0 z-30 bg-white/95 backdrop-blur-sm border-t border-gray-200 p-2.5 max-h-[70%] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
                        <div className="flex items-start justify-between gap-2">
                          <p className="text-[11px] leading-relaxed text-gray-800 whitespace-pre-wrap flex-1">{day.caption || 'Keine Caption verfügbar.'}</p>
                          <div className="flex flex-col gap-1 shrink-0">
                            <button onClick={() => navigator.clipboard?.writeText(day.caption || '')} className="p-1.5 rounded-md bg-gray-100 text-gray-600 hover:text-purple-600" title="Caption kopieren"><SafeIcon icon={FiCopy} className="text-xs" /></button>
                            <button onClick={() => setExpandedCaptionId(null)} className="p-1.5 rounded-md bg-gray-100 text-gray-600 hover:text-red-500" title="Einklappen"><span className="text-[10px] font-bold leading-none">✕</span></button>
                          </div>
                        </div>
                      </div>
                    )}
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