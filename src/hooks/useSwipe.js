import { useRef } from 'react';

/**
 * useSwipe — attach swipe-left / swipe-right handlers to any element.
 *
 * Returns props to spread onto the swipe target. Works with touch (mobile)
 * and mouse drag (desktop). A swipe only fires if the horizontal move exceeds
 * `threshold` px AND is clearly more horizontal than vertical (so it doesn't
 * hijack vertical scrolling).
 *
 *   const swipe = useSwipe({ onLeft: next, onRight: prev });
 *   <div {...swipe}> ... </div>
 */
export const useSwipe = ({ onLeft, onRight, threshold = 50 } = {}) => {
  const start = useRef(null);

  const begin = (x, y) => { start.current = { x, y }; };
  const end = (x, y) => {
    if (!start.current) return;
    const dx = x - start.current.x;
    const dy = y - start.current.y;
    start.current = null;
    if (Math.abs(dx) < threshold) return;          // too small
    if (Math.abs(dx) < Math.abs(dy) * 1.2) return; // too vertical -> let it scroll
    if (dx < 0) { onLeft && onLeft(); } else { onRight && onRight(); }
  };

  return {
    onTouchStart: (e) => { const t = e.touches[0]; begin(t.clientX, t.clientY); },
    onTouchEnd: (e) => { const t = e.changedTouches[0]; end(t.clientX, t.clientY); },
    onMouseDown: (e) => begin(e.clientX, e.clientY),
    onMouseUp: (e) => end(e.clientX, e.clientY),
  };
};
