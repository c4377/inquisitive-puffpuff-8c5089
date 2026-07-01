/**
 * Face detection helper.
 *
 * Uses face-api.js (@vladmandic fork) with the lightweight TinyFaceDetector
 * model. The model is loaded lazily and cached, so the first analysis pays the
 * load cost once, and subsequent images are fast.
 *
 * detectFaceZones(img, GRID) returns a Set of grid-zone indices (0..GRID*GRID-1)
 * that a face overlaps. Callers use this to FORBID placing text in those zones.
 *
 * Everything is best-effort: if the model can't load (offline, unsupported),
 * we resolve to an empty set and the caller falls back to variance-only logic.
 */

let faceApi = null;
let modelLoadPromise = null;
let modelsReady = false;

// Where the model weights are served from. We ship them in /public/models so
// they load from the same origin (no external CDN dependency at runtime).
const MODEL_URL = '/models';

const loadModels = async () => {
  if (modelsReady) return true;
  if (modelLoadPromise) return modelLoadPromise;

  modelLoadPromise = (async () => {
    try {
      // Dynamic import so face-api is only pulled in when needed (keeps the
      // initial app bundle small; the heavy model code loads on first use).
      // @vite-ignore keeps the bundler from hard-failing the build if the
      // package can't be resolved at build time; we handle absence at runtime.
      const mod = await import(/* @vite-ignore */ '@vladmandic/face-api');
      faceApi = mod;
      await faceApi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
      modelsReady = true;
      return true;
    } catch (e) {
      // Model not available -> caller falls back gracefully.
      console.warn('Face model load failed (falling back to variance):', e?.message || e);
      modelsReady = false;
      return false;
    }
  })();

  return modelLoadPromise;
};

/**
 * Detect faces in an already-loaded HTMLImageElement and return the set of
 * grid zones (row-major, GRID x GRID) that any face bounding box overlaps.
 *
 * @param {HTMLImageElement} img - loaded image element
 * @param {number} GRID - grid dimension (e.g. 3 for a 3x3 = 9-zone grid)
 * @returns {Promise<Set<number>>}
 */
export const detectFaceZones = async (img, GRID = 3) => {
  const blocked = new Set();
  try {
    const ok = await loadModels();
    if (!ok || !faceApi) return blocked;

    const options = new faceApi.TinyFaceDetectorOptions({
      inputSize: 320,
      scoreThreshold: 0.5,
    });

    const detections = await faceApi.detectAllFaces(img, options);
    if (!detections || detections.length === 0) return blocked;

    const iw = img.naturalWidth || img.width;
    const ih = img.naturalHeight || img.height;
    if (!iw || !ih) return blocked;

    for (const det of detections) {
      const box = det.box || det._box || det;
      // Expand the box a little (hair/chin/margin) so text keeps clear.
      const pad = 0.15;
      const bx = Math.max(0, box.x - box.width * pad);
      const by = Math.max(0, box.y - box.height * pad);
      const bw = Math.min(iw - bx, box.width * (1 + 2 * pad));
      const bh = Math.min(ih - by, box.height * (1 + 2 * pad));

      const cellW = iw / GRID;
      const cellH = ih / GRID;

      const colStart = Math.floor(bx / cellW);
      const colEnd = Math.floor((bx + bw) / cellW);
      const rowStart = Math.floor(by / cellH);
      const rowEnd = Math.floor((by + bh) / cellH);

      for (let r = rowStart; r <= rowEnd; r++) {
        for (let c = colStart; c <= colEnd; c++) {
          if (r >= 0 && r < GRID && c >= 0 && c < GRID) {
            blocked.add(r * GRID + c);
          }
        }
      }
    }
  } catch (e) {
    // best-effort; return whatever we have (possibly empty)
  }
  return blocked;
};

/** Preload the model in the background (optional, e.g. on app start). */
export const warmUpFaceModel = () => { loadModels(); };
