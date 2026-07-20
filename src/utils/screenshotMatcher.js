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

// Token-overlap similarity (0..1). Robust to OCR noise and word order — we only
// need to know which screenshot is the *best* match for a given placeholder.
export const similarity = (a, b) => {
  const A = new Set(norm(a).split(' ').filter((w) => w.length > 2));
  const B = new Set(norm(b).split(' ').filter((w) => w.length > 2));
  if (A.size === 0 || B.size === 0) return 0;
  let hit = 0;
  A.forEach((w) => { if (B.has(w)) hit++; });
  // Dice coefficient.
  return (2 * hit) / (A.size + B.size);
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
export const matchScreenshots = (placeholders, screenshots) => {
  const pairs = [];
  placeholders.forEach((p) => {
    screenshots.forEach((s) => {
      pairs.push({ pid: p.id, sid: s.id, score: similarity(p.matchText, s.ocrText) });
    });
  });
  pairs.sort((a, b) => b.score - a.score);

  const usedP = new Set();
  const usedS = new Set();
  const mapping = {};
  pairs.forEach(({ pid, sid, score }) => {
    if (score <= 0) return;
    if (usedP.has(pid) || usedS.has(sid)) return;
    mapping[pid] = { screenshotId: sid, score };
    usedP.add(pid);
    usedS.add(sid);
  });
  return mapping;
};
