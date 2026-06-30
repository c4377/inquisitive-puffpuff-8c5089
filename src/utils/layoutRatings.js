// Layout rating store: thumbs up/down per layout, persisted in localStorage.
// Used to bias the import/reload layout selection toward liked layouts.

const KEY = 'layoutRatings';

// Returns { [layoutId]: 1 | -1 }  (1 = thumbs up, -1 = thumbs down)
export const getRatings = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || {};
  } catch {
    return {};
  }
};

export const setRating = (layoutId, value) => {
  const r = getRatings();
  if (r[layoutId] === value) {
    delete r[layoutId]; // clicking same again clears the rating
  } else {
    r[layoutId] = value; // 1 or -1
  }
  try {
    localStorage.setItem(KEY, JSON.stringify(r));
  } catch {
    /* ignore */
  }
  return r;
};

export const getRating = (layoutId) => getRatings()[layoutId] || 0;

/**
 * Order a list of layout ids by preference:
 * liked (👍) first, neutral next, disliked (👎) last.
 * Within the same rating, order is preserved (stable).
 */
export const orderLayoutsByPreference = (layoutIds = []) => {
  const r = getRatings();
  return [...layoutIds].sort((a, b) => (r[b] || 0) - (r[a] || 0));
};

/**
 * Build a weighted pick list: liked layouts appear multiple times (picked more
 * often), disliked layouts are dropped entirely (unless that would leave none).
 */
export const weightedLayoutPool = (layoutIds = []) => {
  const r = getRatings();
  const pool = [];
  layoutIds.forEach((id) => {
    const rating = r[id] || 0;
    if (rating > 0) {
      pool.push(id, id, id); // liked: 3x weight
    } else if (rating === 0) {
      pool.push(id); // neutral: 1x
    }
    // disliked: skipped
  });
  // Safety: if everything was disliked, fall back to the original list.
  return pool.length > 0 ? pool : [...layoutIds];
};
