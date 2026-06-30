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
export const attachSmartImages = async (slides, imagePool = []) => {
  const analyses = await analyzeImagePool(imagePool);
  if (analyses.length === 0) return slides; // nothing to attach

  const cohesive = cohesiveOrder(analyses);
  const used = new Set();
  let rotationOffset = 0; // ensures we cycle through the pool for variety

  return slides.map((slide, index) => {
    const layoutId = slide.layoutId || slide.layout || 'editorial_classic';
    const textZone = LAYOUT_TEXT_ZONE[layoutId] ?? 4;

    // Rank candidates by fit, but rotate the starting point each slide so we
    // don't keep picking the same "best" image for every slide.
    let best = null;
    let bestScore = Infinity;
    const n = cohesive.length;
    for (let i = 0; i < n; i++) {
      const a = cohesive[(i + rotationOffset) % n];
      let score = scoreImageForTextZone(a, textZone);
      if (used.has(a.src)) score += 1000; // strongly discourage repeats
      // small rotation bonus to the next-in-line image for variety
      score += ((i + rotationOffset) % n) * 0.5;
      if (score < bestScore) {
        bestScore = score;
        best = a;
      }
    }

    if (!best) return slide;
    used.add(best.src);
    // If we've used every image once, allow repeats again but keep rotating.
    if (used.size >= n) used.clear();
    rotationOffset = (rotationOffset + 1) % Math.max(n, 1);

    const { overlay, textColorHint } = overlayDecision(best, textZone, bestScore);

    return {
      ...slide,
      background: best.src,
      overlay,
      // expose hints the renderer/editor can optionally use
      _autoImage: {
        textZone: ZONE_LABELS[textZone],
        quietZone: best.quietLabel,
        fitScore: Math.round(bestScore),
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