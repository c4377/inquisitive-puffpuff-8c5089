import { brandRuleSets } from '../constants/brandData';
import { analyzeImagePool, ZONE_LABELS } from './imageAnalysis';

/**
 * Maps a layoutId to the GRID zone (0..8) where the TEXT sits.
 * The image's "quiet zone" should be OPPOSITE this so text never covers the subject.
 * Grid: 0 1 2 / 3 4 5 / 6 7 8
 */
const LAYOUT_TEXT_ZONE = {
  editorial_classic: 3,    // text left -> want quiet space left, subject right
  minimal_editorial: 3,
  minimal_left_accent: 6,  // bottom-left accent
  paper_box: 4,            // boxed center
  story_text_box: 4,
  split_color: 7,          // text bottom
  minimal_quote: 4,        // centered cover
  centered_focus: 4,
  maximized_bold: 4,
  glass_layer: 7,          // CTA bottom
  tweet_card: 4,
};

// The "opposite" zone we'd ideally like to be quiet, given where text sits.
const OPPOSITE_ZONE = {
  0: 8, 1: 7, 2: 6,
  3: 5, 4: 4, 5: 3,
  6: 2, 7: 1, 8: 0,
};

/**
 * Score how well an image fits a target text zone.
 * Lower score = better fit. We want:
 *   - the text zone itself to be FLAT (low variance) so text is readable
 *   - the image subject (busy zone) to sit away from the text zone
 */
const scoreImageForTextZone = (analysis, textZone) => {
  if (!analysis) return Infinity;
  const flatnessAtText = analysis.zoneVariance[textZone]; // lower better
  const want = OPPOSITE_ZONE[textZone];
  // distance (in grid steps) between image subject and the ideal opposite zone
  const subjRow = Math.floor(analysis.busyZone / 3);
  const subjCol = analysis.busyZone % 3;
  const wantRow = Math.floor(want / 3);
  const wantCol = want % 3;
  const subjectDistance = Math.abs(subjRow - wantRow) + Math.abs(subjCol - wantCol);

  // Weighting: readability under text matters most, then subject placement.
  return flatnessAtText * 1.0 + subjectDistance * 30;
};

/**
 * Decide whether a chosen image needs a darkening overlay for legible text,
 * and what text color to use. Returns { overlay, textColorHint }.
 */
const overlayDecision = (analysis, textZone, fitScore) => {
  if (!analysis) return { overlay: 0.25, textColorHint: null };
  const brightnessUnderText = analysis.zoneBrightness[textZone];
  // If the spot under the text is bright, dark text; if dark, light text.
  const textColorHint = brightnessUnderText > 140 ? 'dark' : 'light';
  // Poor fit (text lands on busy/contrasty area) -> stronger overlay.
  // fitScore grows with bad placement; normalize loosely.
  let overlay = 0.2;
  if (fitScore > 200) overlay = 0.45;
  else if (fitScore > 90) overlay = 0.35;
  return { overlay, textColorHint };
};

/**
 * Build a cohesive subset/ordering of the analyzed pool.
 * We sort by avgBrightness so the carousel doesn't jump light/dark/light,
 * giving a "from one set" feel. Returns the analyses array (cohesive order).
 */
const cohesiveOrder = (analyses) =>
  [...analyses].sort((a, b) => a.avgBrightness - b.avgBrightness);

/**
 * MAIN: attach background images to already-laid-out slides.
 *
 * @param {Array}  slides      slides that already have a layoutId/layout
 * @param {Array}  imagePool   brandImages (objects with .src/.url) or strings
 * @returns {Promise<Array>}   slides with background + overlay + image meta set
 */
export const attachSmartImages = async (slides, imagePool = [], startOffset = 0) => {
  const analyses = await analyzeImagePool(imagePool);
  if (analyses.length === 0) return slides; // nothing to attach

  // VARIETY MODE: hand out images round-robin using a GLOBAL offset so every
  // post across the whole plan gets a different image (not per-day-reset).
  // We deliberately do NOT reshuffle per call — a stable order + global offset
  // guarantees uniqueness across days. The pool itself is shuffled once by the
  // caller's ordering (upload order), which is fine for variety.
  const n = analyses.length;

  return slides.map((slide, index) => {
    const layoutId = slide.layoutId || slide.layout || 'editorial_classic';
    const textZone = LAYOUT_TEXT_ZONE[layoutId] ?? 4;

    // Global round-robin pick: offset + local index, wrapped over the pool.
    const best = analyses[(startOffset + index) % n];
    if (!best) return slide;

    const { overlay, textColorHint } = overlayDecision(best, textZone, 50);

    // Brightness at the quiet zone (best text spot). Lets the renderer decide:
    // dark enough -> white text + shadow only; too bright -> needs a scrim.
    const quietBrightness = (best.zoneBrightness && typeof best.quietZone === 'number')
      ? best.zoneBrightness[best.quietZone]
      : (best.zoneBrightness ? best.zoneBrightness[4] : 128);

    return {
      ...slide,
      background: best.src,
      overlay,
      _autoImage: {
        textZone: ZONE_LABELS[textZone],
        quietZone: best.quietLabel,
        quietBrightness,
        fitScore: 0,
        textColorHint,
        ok: best.ok,
      },
    };
  });
};

/**
 * Analyzes text content and assigns the most appropriate layout and styling
 * mimicking the "Editorial/Storytelling" vibe.
 */
export const assignSmartLayouts = (rawSlides, brandConfig) => {
  return rawSlides.map((slide, index) => {
    const textLength = slide.text.length;
    const paragraphs = slide.text.split('\n').filter(p => p.trim() !== '');
    const lineCount = paragraphs.length;
    
    let layoutId = 'editorial_classic'; // Default
    let secondaryText = '';
    let primaryText = slide.text;
    
    // 1. Layout Selection Heuristics
    if (index === 0) {
      // Title Slide Strategy
      layoutId = 'editorial_classic'; 
      // Try to split title if multiple lines
      if (lineCount > 1) {
        secondaryText = paragraphs[0]; // Hook/Top text
        primaryText = paragraphs.slice(1).join('\n'); // Main Title
      }
    } else if (lineCount >= 4 && textLength > 150) {
      // Dense text -> Boxed layout for readability (Like Image 3/4)
      layoutId = 'paper_box';
    } else if (lineCount === 2 || lineCount === 3) {
      // Comparison or Punchy text -> Split layout (Like Image 5)
      layoutId = 'split_color';
      secondaryText = paragraphs[0]; // Top part
      primaryText = paragraphs.slice(1).join('\n'); // Bottom part
    } else {
      // Standard Storytelling
      layoutId = 'editorial_classic';
    }

    // 2. Auto-Highlighting (Bolding) Strategy
    // The images show bolding of key phrases. We simulate this by bolding the first meaningful segment or keyword.
    // In a real NLP system we'd find keywords, here we use structural heuristics.
    const formattedText = applyEditorialHighlighting(primaryText);

    // Pull colors + fonts from the active brand (Brandomizer) so every slide
    // is styled with the current brand identity.
    const c = brandConfig?.colors || {};
    const t = brandConfig?.typography || {};

    return {
      ...slide,
      text: formattedText,
      secondaryText: secondaryText,
      layoutId: layoutId,
      layout: layoutId, // renderer reads slide.layout
      // Brand colors (from Brandomizer)
      backgroundColor: c.background || '#ffffff',
      color: c.primary || '#111111',
      secondaryColor: c.secondary || '#666666',
      tertiaryColor: c.tertiary || c.secondary || '#999999',
      neutralColor: c.neutral || c.background || '#F5F5F5',
      accentColor: c.accent || c.secondary || '#B8860B',
      // Brand fonts
      fontFamily: t.fontFamily || 'Inter',
      accentFontFamily: t.accentFontFamily || t.fontFamily || 'Playfair Display',
      fontWeight: t.fontWeight || 'normal',
      // Default styles based on layout vibe
      textAlign: layoutId === 'editorial_classic' ? 'left' : 'center',
      fontSize: layoutId === 'paper_box' ? 36 : 42,
    };
  });
};

// Helper: mark specific parts of the text as *accent* (single asterisks,
// matching the renderer's accent parser).
const applyEditorialHighlighting = (text) => {
  const lines = text.split('\n');
  return lines.map(line => {
    const words = line.split(' ');
    // Heuristic: If line is short (< 8 words), accent the whole line (Impact statement)
    if (words.length < 8 && words.length > 2) {
      return `*${line}*`;
    }
    // Heuristic: bold the first few words of long paragraphs as a lead-in
    if (words.length > 15) {
      const leadIn = words.slice(0, 4).join(' ');
      const rest = words.slice(4).join(' ');
      return `*${leadIn}* ${rest}`;
    }
    return line;
  }).join('\n');
};