/**
 * postDesignEngine.js
 * -------------------
 * ONE central place that decides, fully automatically, how each post looks —
 * so we don't need many rigid layouts. For every post it decides:
 *
 *   1. hasImage   — whether this post shows a photo (for feed variety)
 *   2. textAnchor — where the headline sits:
 *                   - with image: the image's QUIET zone (avoids the subject/face),
 *                     falling back to 'bottom' if unknown
 *                   - without image: rotates top -> center -> bottom for variety
 *   3. bold       — every 4th post is bold (statement accent), the rest normal
 *
 * The renderer then draws a single adaptive layout using these decisions.
 */

// Map a 9-zone quiet label to a coarse vertical+horizontal anchor the renderer
// understands. We keep it simple: the renderer positions text by row (top/mid/
// bottom) and column (left/center/right).
const zoneToAnchor = (quietLabel) => {
  if (!quietLabel || typeof quietLabel !== 'string') return { row: 'bottom', col: 'center' };
  const row = quietLabel.includes('top') ? 'top'
    : quietLabel.includes('bottom') ? 'bottom' : 'mid';
  const col = quietLabel.includes('left') ? 'left'
    : quietLabel.includes('right') ? 'right' : 'center';
  return { row, col };
};

/**
 * Decide the design for a single post.
 *
 * @param {object} opts
 * @param {number} opts.globalIndex - running index across the whole plan (day*100+slide)
 * @param {boolean} opts.hasImage   - whether an image is (or should be) attached
 * @param {object}  [opts.autoImage] - image analysis result (_autoImage) if present
 * @returns {{ textAnchor: {row,col}, bold: boolean }}
 */
export const decidePostDesign = ({ globalIndex, hasImage, autoImage }) => {
  // Bold: every 4th post (0-based: indices 3, 7, 11, ...).
  const bold = (globalIndex % 4 === 3);

  let textAnchor;
  if (hasImage) {
    // Text goes to the image's quiet zone (avoids subject/face). Fallback bottom.
    if (autoImage && autoImage.quietZone) {
      textAnchor = zoneToAnchor(autoImage.quietZone);
    } else {
      textAnchor = { row: 'bottom', col: 'center' };
    }
  } else {
    // No image: rotate the vertical position for variety.
    const rows = ['top', 'mid', 'bottom'];
    textAnchor = { row: rows[globalIndex % 3], col: 'center' };
  }

  return { textAnchor, bold };
};

/**
 * Decide whether a given day-index should carry a photo.
 * Default pattern: 5 of every 7 days have a photo (indices 2 and 5 are text).
 */
export const dayHasImage = (dayIndex) => {
  const r = dayIndex % 7;
  return !(r === 2 || r === 5);
};
