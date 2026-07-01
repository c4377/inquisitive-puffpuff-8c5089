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

    const img = new Image();
    img.crossOrigin = 'anonymous';

    img.onload = async () => {
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
        let quietZone = -1, busyZone = 0;
        for (let z = 0; z < 9; z++) {
          if (faceZones.has(z)) continue; // skip face zones entirely
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

        resolve({
          src,
          ok: true,
          zoneBrightness,
          zoneVariance,
          quietZone,
          busyZone,
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
        resolve(fallbackAnalysis(src));
      }
    };

    img.onerror = () => resolve(fallbackAnalysis(src));
    img.src = src;
  });

const fallbackAnalysis = (src) => ({
  src: src || null,
  ok: false,
  zoneBrightness: new Array(9).fill(128),
  zoneVariance: new Array(9).fill(0),
  quietZone: 4,
  busyZone: 4,
  quietLabel: 'center',
  busyLabel: 'center',
  avgColor: { r: 128, g: 128, b: 128 },
  avgBrightness: 128,
});

/**
 * Analyze a whole pool of image objects.
 * Accepts the brandImages shape (objects with .src or .url) OR plain strings.
 * Returns array of analysis objects, preserving order; failures become fallbacks.
 */
export const analyzeImagePool = async (pool = []) => {
  const sources = pool
    .map((item) => (typeof item === 'string' ? item : item?.src || item?.url || item?.dataUrl))
    .filter(Boolean);

  // Sequential-ish but allow parallelism; pools are usually small.
  return Promise.all(sources.map((s) => analyzeImage(s)));
};
