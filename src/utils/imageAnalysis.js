/**
 * imageAnalysis.js
 * ----------------
 * Browser-only (Canvas) image analysis. No external API, no keys.
 *
 * For each image we compute:
 *   - zoneBrightness: a 3x3 grid (9 zones) of average luminance (0-255)
 *   - quietZone: the zone with the LOWEST visual complexity (best place for text)
 *   - busyZone: the zone with the HIGHEST complexity (the "subject" / focal area)
 *   - avgColor: {r,g,b} dominant-ish average color (for cohesion grouping)
 *   - avgBrightness: overall luminance 0-255 (light vs dark image)
 *
 * "Complexity" = variance of luminance within a zone. Low variance = flat area
 * (sky, wall, blur) = good for placing text. High variance = detail/subject.
 */

const GRID = 3; // 3x3 zones
const SAMPLE_SIZE = 90; // downscale longest analysis edge for speed

// Map a zone index (0..8) to a human label, row-major:
// 0 1 2   -> top-left, top-center, top-right
// 3 4 5   -> mid-left, center, mid-right
// 6 7 8   -> bottom-left, bottom-center, bottom-right
export const ZONE_LABELS = [
  'top-left', 'top-center', 'top-right',
  'mid-left', 'center', 'mid-right',
  'bottom-left', 'bottom-center', 'bottom-right',
];

const luminance = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;

import { detectFaceZones } from './faceDetection';

/**
 * Analyze a single image source (data URL or URL).
 * Returns a Promise resolving to the analysis object (or a safe fallback).
 */
export const analyzeImage = (src) =>
  new Promise((resolve) => {
    if (!src) {
      resolve(fallbackAnalysis(src));
      return;
    }

    // Safety timeout: if an image hasn't loaded/analyzed within 8s (slow network,
    // Supabase hiccup, etc.), resolve with a fallback so the batch keeps moving.
    let settled = false;
    const done = (result) => { if (!settled) { settled = true; resolve(result); } };
    const timer = setTimeout(() => done(fallbackAnalysis(src)), 8000);

    const img = new Image();
    img.crossOrigin = 'anonymous';

    img.onload = async () => {
      clearTimeout(timer);
      try {
        const canvas = document.createElement('canvas');
        const scale = SAMPLE_SIZE / Math.max(img.width, img.height);
        const w = Math.max(GRID, Math.round(img.width * scale));
        const h = Math.max(GRID, Math.round(img.height * scale));
        canvas.width = w;
        canvas.height = h;

        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        ctx.drawImage(img, 0, 0, w, h);

        const { data } = ctx.getImageData(0, 0, w, h);

        // Accumulators per zone
        const zoneSum = new Array(9).fill(0);
        const zoneSumSq = new Array(9).fill(0);
        const zoneCount = new Array(9).fill(0);
        let totalR = 0, totalG = 0, totalB = 0, totalLum = 0, totalPx = 0;

        const cellW = w / GRID;
        const cellH = h / GRID;

        for (let y = 0; y < h; y++) {
          const row = Math.min(GRID - 1, Math.floor(y / cellH));
          for (let x = 0; x < w; x++) {
            const col = Math.min(GRID - 1, Math.floor(x / cellW));
            const zone = row * GRID + col;
            const i = (y * w + x) * 4;
            const r = data[i], g = data[i + 1], b = data[i + 2];
            const lum = luminance(r, g, b);

            zoneSum[zone] += lum;
            zoneSumSq[zone] += lum * lum;
            zoneCount[zone] += 1;

            totalR += r; totalG += g; totalB += b;
            totalLum += lum; totalPx += 1;
          }
        }

        const zoneBrightness = [];
        const zoneVariance = [];
        for (let z = 0; z < 9; z++) {
          const n = zoneCount[z] || 1;
          const mean = zoneSum[z] / n;
          const variance = Math.max(0, zoneSumSq[z] / n - mean * mean);
          zoneBrightness[z] = mean;
          zoneVariance[z] = variance;
        }

        // Detect faces and forbid their zones for text placement.
        // "Text never over the face": faceZones are removed from candidates.
        let faceZones = new Set();
        try {
          faceZones = await detectFaceZones(img, GRID);
        } catch (e) { /* fallback: no face info */ }

        // Quiet zone = lowest variance (flattest -> safest for text),
        // but NEVER a zone containing a face. If every non-face zone is worse,
        // we still prefer a non-face zone over a face zone (strict avoidance).
        // Ein Gesicht reicht in die Zone darunter — Kinn und Hals. Die ist
        // sehr gleichmaessig und wurde deshalb gern als "ruhig" gewaehlt.
        // Also mitmeiden, solange danach ueberhaupt etwas uebrig bleibt.
        const gemieden = new Set(faceZones);
        faceZones.forEach((z) => { if (z + 3 < 9) gemieden.add(z + 3); });
        const meiden = gemieden.size < 9 ? gemieden : faceZones;

        let quietZone = -1, busyZone = 0;
        for (let z = 0; z < 9; z++) {
          if (meiden.has(z)) continue; // Gesicht und die Zone darunter
          if (quietZone === -1 || zoneVariance[z] < zoneVariance[quietZone]) quietZone = z;
        }
        // If literally every zone has a face (rare), fall back to lowest variance overall.
        if (quietZone === -1) {
          quietZone = 0;
          for (let z = 1; z < 9; z++) if (zoneVariance[z] < zoneVariance[quietZone]) quietZone = z;
        }
        for (let z = 1; z < 9; z++) {
          if (zoneVariance[z] > zoneVariance[busyZone]) busyZone = z;
        }

        // ---- FINE TEXT-SPOT SEARCH -------------------------------------
        // The 3x3 grid above is too coarse to place an editorial text block.
        // Scan a fine grid and score every candidate block (a column of the
        // image, roughly 40% wide / 30% tall) by: flatness (low variance),
        // tonal consistency, distance from faces, and a slight preference for
        // the lower half + side columns (where an editorial block usually
        // sits). Returns the block CENTRE as fractions plus its brightness so
        // the renderer can choose light/dark text.
        const FX = 8, FY = 10;                 // fine grid columns / rows
        const fSum = new Array(FX * FY).fill(0);
        const fSumSq = new Array(FX * FY).fill(0);
        const fCount = new Array(FX * FY).fill(0);
        const fcw = w / FX, fch = h / FY;
        for (let y = 0; y < h; y++) {
          const fr = Math.min(FY - 1, Math.floor(y / fch));
          for (let x = 0; x < w; x++) {
            const fc = Math.min(FX - 1, Math.floor(x / fcw));
            const fz = fr * FX + fc;
            const i = (y * w + x) * 4;
            const lum = luminance(data[i], data[i + 1], data[i + 2]);
            fSum[fz] += lum; fSumSq[fz] += lum * lum; fCount[fz] += 1;
          }
        }
        const fBright = new Array(FX * FY).fill(0);
        const fVar = new Array(FX * FY).fill(0);
        for (let z = 0; z < FX * FY; z++) {
          const n = fCount[z] || 1;
          const mean = fSum[z] / n;
          fBright[z] = mean;
          fVar[z] = Math.sqrt(Math.max(0, fSumSq[z] / n - mean * mean));
        }
        // Block size in fine cells (~44% wide, ~34% tall -> narrow editorial column)
        const BW = 3, BH = 3;
        let best = null;
        for (let r = 0; r <= FY - BH; r++) {
          for (let c = 0; c <= FX - BW; c++) {
            let vSum = 0, bSum = 0, n = 0, faceHit = false;
            for (let rr = r; rr < r + BH; rr++) {
              for (let cc = c; cc < c + BW; cc++) {
                vSum += fVar[rr * FX + cc];
                bSum += fBright[rr * FX + cc];
                n += 1;
                // map fine cell -> coarse 3x3 zone to reuse face detection
                const coarse = Math.min(2, Math.floor(rr / (FY / 3))) * 3
                             + Math.min(2, Math.floor(cc / (FX / 3)));
                if (faceZones.has(coarse)) faceHit = true;
              }
            }
            const variance = vSum / n;          // 0 = perfectly flat
            const brightness = bSum / n;
            // Penalties: busy area, face overlap, and the very top/bottom edges.
            let score = variance;
            if (faceHit) score += 220;          // effectively excludes face blocks
            if (r === 0) score += 14;           // avoid hugging the top edge
            if (r + BH === FY) score += 26;     // keep clear of the signature band
            // Slight preference for side columns (editorial look) over dead centre
            const centreCol = Math.abs((c + BW / 2) - FX / 2);
            score += (2.2 - Math.min(2.2, centreCol)) * 5;
            if (!best || score < best.score) {
              best = {
                score,
                brightness,
                variance,
                x: (c + BW / 2) / FX,
                y: (r + BH / 2) / FY,
              };
            }
          }
        }
        const textSpot = best
          ? { x: +best.x.toFixed(3), y: +best.y.toFixed(3),
              brightness: Math.round(best.brightness), variance: Math.round(best.variance) }
          : null;

        done({
          src,
          ok: true,
          zoneBrightness,
          zoneVariance,
          quietZone,
          busyZone,
          textSpot,
          quietLabel: ZONE_LABELS[quietZone],
          busyLabel: ZONE_LABELS[busyZone],
          faceZones: Array.from(faceZones),
          hasFace: faceZones.size > 0,
          avgColor: {
            r: Math.round(totalR / totalPx),
            g: Math.round(totalG / totalPx),
            b: Math.round(totalB / totalPx),
          },
          avgBrightness: totalLum / totalPx,
        });
      } catch (e) {
        // Tainted canvas (CORS) or other failure -> safe fallback
        done(fallbackAnalysis(src));
      }
    };

    img.onerror = () => { clearTimeout(timer); done(fallbackAnalysis(src)); };
    img.src = src;
  });

const fallbackAnalysis = (src) => ({
  src: src || null,
  ok: false,
  zoneBrightness: new Array(9).fill(128),
  zoneVariance: new Array(9).fill(0),
  // Scheitert die Analyse, landete der Text bisher in der Mitte — bei
  // einem Portraet also im Gesicht. Unten mittig ist der sichere Platz.
  quietZone: 7,
  busyZone: 4,
  quietLabel: 'bottom-center',
  busyLabel: 'center',
  textSpot: null,
  avgColor: { r: 128, g: 128, b: 128 },
  avgBrightness: 128,
});

/**
 * Analyze a whole pool of image objects.
 * Accepts the brandImages shape (objects with .src or .url) OR plain strings.
 * Returns array of analysis objects, preserving order; failures become fallbacks.
 */
// Cache analyses by src so re-runs (e.g. "Neu laden") are instant and we never
// re-analyze the same image twice within a session.
const _analysisCache = new Map();

/**
 * Analyze a whole pool of image objects.
 * Accepts the brandImages shape (objects with .src or .url) OR plain strings.
 * Returns array of analysis objects, preserving order; failures become fallbacks.
 *
 * IMPORTANT: images are analyzed in small BATCHES (not all at once) so a large
 * pool (68+) never floods the browser with parallel image loads + canvas reads.
 */
export const analyzeImagePool = async (pool = []) => {
  const sources = pool
    .map((item) => (typeof item === 'string' ? item : item?.src || item?.url || item?.dataUrl))
    .filter(Boolean);

  const BATCH_SIZE = 6; // how many images to analyze at the same time
  const results = new Array(sources.length);

  for (let start = 0; start < sources.length; start += BATCH_SIZE) {
    const batch = sources.slice(start, start + BATCH_SIZE);
    // Analyze this batch in parallel, then move on to the next batch.
    const batchResults = await Promise.all(
      batch.map(async (s) => {
        if (_analysisCache.has(s)) return _analysisCache.get(s);
        const r = await analyzeImage(s);
        _analysisCache.set(s, r);
        return r;
      })
    );
    for (let i = 0; i < batchResults.length; i++) {
      results[start + i] = batchResults[i];
    }
  }
  return results;
};
