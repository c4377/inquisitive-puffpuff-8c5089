// Screenshot ↔ placeholder matching via OCR.
//
// Bulk-imported texts may contain placeholders like:
//   [SCREENSHOT — "Btw: 30 Anmeldungen für den Workshop morgen"]
// The text AFTER the dash is the "match text". We OCR each uploaded screenshot,
// then pair every placeholder slide with the screenshot whose OCR text best
// matches — and drop that screenshot in as an overlay image.

import Tesseract from 'tesseract.js';

// Detect a screenshot placeholder and pull out the match text (after the dash).
// Accepts —, –, or - as the separator and optional surrounding quotes/brackets.
export const parseScreenshotPlaceholder = (text) => {
  if (!text || typeof text !== 'string') return null;
  const t = text.trim();
  // Must look like a screenshot placeholder.
  if (!/screenshot/i.test(t)) return null;
  // Everything after the first dash-like separator.
  const m = t.match(/screenshot\s*[—–-]\s*(.+)$/i);
  let matchText = m ? m[1] : t.replace(/screenshot/i, '');
  // Strip wrapping brackets and quotes.
  matchText = matchText.replace(/[\[\]""„"']/g, ' ').replace(/\s+/g, ' ').trim();
  return matchText || null;
};

// Normalise text for comparison: lowercase, strip punctuation, collapse spaces.
const norm = (s) => (s || '')
  .toLowerCase()
  .replace(/[^\p{L}\p{N}\s]/gu, ' ')
  .replace(/\s+/g, ' ')
  .trim();

// Common German filler words carry no identifying signal — two unrelated texts
// both contain "für", "den", "und". Ignoring them prevents false matches.
const STOPWORDS = new Set([
  'der','die','das','den','dem','des','ein','eine','einen','einem','einer','eines',
  'und','oder','aber','doch','denn','weil','dass','ist','sind','war','waren','hat',
  'habe','haben','wird','werden','wurde','für','mit','von','vom','zum','zur','auf',
  'aus','bei','nach','über','unter','vor','durch','nicht','auch','noch','schon',
  'wie','was','wer','wenn','dann','sich','sie','ihr','ihre','ich','due','ganz','sehr',
]);

// Do two words match despite OCR noise? Exact or one-character-off, but only for
// reasonably long words — allowing edits on short words made unrelated texts
// look similar.
const wordsMatch = (a, b) => {
  if (a === b) return true;
  if (a.length < 5 || b.length < 5) return false;      // short words: exact only
  if (Math.abs(a.length - b.length) > 1) return false;
  // Levenshtein distance <= 1
  let i = 0, j = 0, edits = 0;
  while (i < a.length && j < b.length) {
    if (a[i] === b[j]) { i++; j++; continue; }
    if (++edits > 1) return false;
    if (a.length === b.length) { i++; j++; }
    else if (a.length > b.length) i++;
    else j++;
  }
  return edits + (a.length - i) + (b.length - j) <= 1;
};

// How much of the PLACEHOLDER text appears in the screenshot text (0..1).
// Coverage, not symmetry: a short placeholder ("30 Anmeldungen für den
// Workshop") should score high against a screenshot full of other text, which a
// symmetric measure would punish.
export const similarity = (placeholderText, ocrText) => {
  const keep = (w) => w.length > 3 && !STOPWORDS.has(w);
  const want = norm(placeholderText).split(' ').filter(keep);
  const have = norm(ocrText).split(' ').filter((w) => w.length > 2);
  if (want.length === 0 || have.length === 0) return 0;
  let hit = 0;
  want.forEach((w) => { if (have.some((h) => wordsMatch(w, h))) hit++; });
  return hit / want.length;
};

// Run OCR on one image (dataURL or File). Returns recognised text.
export const ocrImage = async (imageSource, onProgress) => {
  try {
    const { data } = await Tesseract.recognize(imageSource, 'deu', {
      logger: (m) => {
        if (onProgress && m.status === 'recognizing text') onProgress(m.progress);
      },
    });
    return data.text || '';
  } catch (e) {
    return '';
  }
};

// Given placeholder slides [{ id, matchText }] and screenshots
// [{ id, dataUrl, ocrText }], return a mapping placeholderId -> screenshotId.
// Greedy best-first: strongest matches are assigned first, each screenshot used
// at most once.
// For EVERY placeholder pick the screenshot whose OCR text covers it best.
// A screenshot may be used for several placeholders (the same proof image can
// legitimately appear twice), and a minimum score avoids random pairings.
export const MATCH_THRESHOLD = 0.45;

export const matchScreenshots = (placeholders, screenshots) => {
  const mapping = {};
  placeholders.forEach((p) => {
    let best = null;
    screenshots.forEach((s) => {
      const score = similarity(p.matchText, s.ocrText);
      if (!best || score > best.score) best = { screenshotId: s.id, score };
    });
    if (best && best.score >= MATCH_THRESHOLD) {
      mapping[p.id] = best;
    }
  });
  return mapping;
};
