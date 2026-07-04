import { fabric } from 'fabric';

/**
 * Renders the slide content onto a Fabric.js canvas.
 * Supports Smart Layouts: Editorial, Paper Box, Split Color, etc.
 * 
 * @param {fabric.Canvas | fabric.StaticCanvas} canvas - The Fabric canvas instance
 * @param {Object} slide - The slide data (text, colors, layout, etc.)
 * @param {number} width - Target width
 * @param {number} height - Target height
 * @param {Object} options - Extra options (scale, globalBrandName, totalSlides, slideIndex)
 */
export const renderSlide = async (canvas, slide, width, height, options = {}) => {
  if (!canvas) return;
  // Guard: a disposed canvas (e.g. export loop reusing/disposing) has no
  // drawing context. Touching it throws "Cannot read properties of null
  // (reading 'clearRect')". Bail out safely instead of crashing the export.
  const hasContext = (c) => {
    try {
      if (typeof c.getContext === 'function') return !!c.getContext();
      // fabric StaticCanvas exposes contextContainer / lowerCanvasEl
      if (c.contextContainer) return true;
      if (c.lowerCanvasEl && c.lowerCanvasEl.getContext) return !!c.lowerCanvasEl.getContext('2d');
      return true; // unknown shape: assume ok, let try/catch handle it
    } catch (e) { return false; }
  };
  if (!hasContext(canvas)) return;

  // Clear and setup
  try {
    canvas.clear();
    canvas.setBackgroundColor(slide.backgroundColor || '#ffffff', () => {
      try { canvas.renderAll(); } catch (e) { /* canvas may be gone */ }
    });
  } catch (e) {
    // Canvas became invalid mid-setup — abort this render safely.
    return;
  }
  
  // Ensure dimensions
  if (canvas.setWidth) canvas.setWidth(width);
  if (canvas.setHeight) canvas.setHeight(height);

  // === CENTRAL MANUAL-OVERRIDE WRAPPER ===
  // Every text object added by any layout passes through here. This is what
  // makes "the last one wins": manual Position (xOffset/yOffset), Opacity,
  // Align and font choices from the Editor always override the layout's
  // computed values, no matter which layout block created the object.
  const uiScale = (options.scale || 1);
  const isPrimaryText = (obj) => {
    // Heuristic: the main body text is the largest Textbox. We tag primary vs
    // secondary by checking against slide.secondaryText content.
    if (!obj || obj.type !== 'textbox') return false;
    return true;
  };
  const applyManualOverrides = (obj) => {
    try {
      if (!obj || (obj.type !== 'textbox' && obj.type !== 'text')) return;

      // --- AUTO-FIT: shrink any textbox so it never overflows the slide ---
      // A textbox has a fixed width and wraps; if the resulting height would
      // push it past the top or bottom edge, reduce the font size until it fits.
      if (obj.type === 'textbox' && obj.text) {
        try {
          const margin = height * 0.04;           // keep a little breathing room
          const originY = obj.originY || 'top';
          // Compute how much vertical space this box has to its nearest edge,
          // based on where its anchor sits.
          let avail;
          if (originY === 'center') {
            const distTop = obj.top - margin;
            const distBot = (height - margin) - obj.top;
            avail = 2 * Math.min(distTop, distBot);
          } else if (originY === 'bottom') {
            avail = (obj.top) - margin;
          } else { // top
            avail = (height - margin) - obj.top;
          }
          if (avail > 0) {
            let guard = 0;
            // Shrink until the rendered height fits (or we hit a floor).
            while (obj.height > avail && obj.fontSize > 10 && guard < 40) {
              obj.set('fontSize', obj.fontSize - 1);
              obj.initDimensions && obj.initDimensions();
              guard++;
            }
          }
          // Also guard horizontal: if a single word is wider than the box,
          // shrink so it fits the width too.
          const words = String(obj.text).split(/\s+/);
          let widthGuard = 0;
          while (widthGuard < 40 && obj.fontSize > 10) {
            const longest = words.reduce((a, b) => (a.length >= b.length ? a : b), '');
            const probe = new fabric.Text(longest, { fontSize: obj.fontSize, fontFamily: obj.fontFamily, fontWeight: obj.fontWeight });
            if (probe.width <= obj.width) break;
            obj.set('fontSize', obj.fontSize - 1);
            obj.initDimensions && obj.initDimensions();
            widthGuard++;
          }
        } catch (e) { /* auto-fit best-effort */ }
      }

      // Identify whether this object is the secondary text (subtext).
      const objText = (obj.text || '').trim();
      const secText = (slide.secondaryText || '').trim();
      const isSecondary = secText && objText === secText;

      const xOff = isSecondary ? slide.secondaryXOffset : slide.xOffset;
      const yOff = isSecondary ? slide.secondaryYOffset : slide.yOffset;
      const opacity = isSecondary ? slide.secondaryTextOpacity : slide.textOpacity;

      if (typeof xOff === 'number' && xOff !== 0) obj.left = obj.left + xOff * uiScale;
      if (typeof yOff === 'number' && yOff !== 0) obj.top = obj.top + yOff * uiScale;
      if (typeof opacity === 'number') obj.opacity = Math.max(0, Math.min(1, opacity));
      obj.setCoords && obj.setCoords();
    } catch (e) { /* override best-effort */ }
  };
  const _origAdd = canvas.__origAdd || canvas.add.bind(canvas);
  canvas.__origAdd = _origAdd;
  canvas.add = (...objs) => {
    objs.forEach(applyManualOverrides);
    return _origAdd(...objs);
  };

  // --- FULL-BLEED BACKGROUND IMAGE (Cover with photo) ---
  // If the slide has a background image (e.g. auto-assigned in Bulk import),
  // draw it edge-to-edge, then add a readability gradient on the text side.
  const drawBackgroundImage = (src) =>
    new Promise((resolve) => {
      if (!src) return resolve(false);
      fabric.Image.fromURL(
        src,
        (img) => {
          if (!img) return resolve(false);
          // Cover-fit: scale so image fills the whole canvas, center-crop.
          const baseScale = Math.max(width / img.width, height / img.height);
          // Apply user Zoom (imageScale, default 1) and position offsets.
          const userZoom = typeof slide.imageScale === 'number' ? slide.imageScale : 1;
          const offsetX = (typeof slide.imageX === 'number' ? slide.imageX : 0) * scale;
          const offsetY = (typeof slide.imageY === 'number' ? slide.imageY : 0) * scale;
          const finalScale = baseScale * userZoom;
          img.set({
            originX: 'center',
            originY: 'center',
            left: width / 2 + offsetX,
            top: height / 2 + offsetY,
            scaleX: finalScale,
            scaleY: finalScale,
            selectable: false,
          });
          // Optional blur via fabric filter (only when explicitly set > 0).
          // Slider range is 0..20; map to fabric's 0..1 blur amount.
          if (typeof slide.blur === 'number' && slide.blur >= 1 && fabric.Image.filters?.Blur) {
            try {
              img.filters = [new fabric.Image.filters.Blur({ blur: Math.min(slide.blur / 40, 0.5) })];
              img.applyFilters();
            } catch (e) { /* blur optional */ }
          }
          canvas.add(img);
          canvas.sendToBack(img);

          // Readability overlay — kept light so the photo stays vibrant.
          const ov = typeof slide.overlay === 'number' ? slide.overlay : 0.28;
          const overlayRect = new fabric.Rect({
            left: 0, top: 0, width, height,
            fill: `rgba(0,0,0,${ov})`, selectable: false,
          });
          canvas.add(overlayRect);

          // Gentle gradient only at the very top & bottom edges (where brand
          // mark / slide number sit). Middle stays clear so the image shows.
          try {
            const grad = new fabric.Rect({
              left: 0, top: 0, width, height, selectable: false,
              fill: new fabric.Gradient({
                type: 'linear',
                coords: { x1: 0, y1: 0, x2: 0, y2: height },
                colorStops: [
                  { offset: 0,    color: 'rgba(0,0,0,0.30)' },
                  { offset: 0.18, color: 'rgba(0,0,0,0.0)' },
                  { offset: 0.82, color: 'rgba(0,0,0,0.0)' },
                  { offset: 1,    color: 'rgba(0,0,0,0.35)' },
                ],
              }),
            });
            canvas.add(grad);
          } catch (e) { /* gradient optional */ }
          resolve(true);
        },
        { crossOrigin: 'anonymous' }
      );
    });

  const scale = options.scale || 1;
  const padding = width * 0.08;

  // Global text size factor — reduces all text ~20% so defaults look balanced.
  const FONT = 0.8;
  const fs = (size) => size * scale * FONT;
  
  // Resolve Style Props (Fallback to defaults if missing in slide)
  const primaryColor = slide.color || '#000000';
  const secondaryColor = slide.secondaryColor || '#666666';
  const accentColor = slide.accentColor || '#000000';
  const fontFamily = slide.fontFamily || 'Inter';
  const accentFont = slide.accentFontFamily || fontFamily;

  // Helper: luminance of a hex color (0=dark, 255=light)
  const hexLuminance = (hex) => {
    if (!hex || typeof hex !== 'string') return 128;
    let h = hex.replace('#', '');
    if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    const r = parseInt(h.slice(0, 2), 16);
    const g = parseInt(h.slice(2, 4), 16);
    const b = parseInt(h.slice(4, 6), 16);
    if ([r, g, b].some(Number.isNaN)) return 128;
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };

  // Contrast-safe text color: if chosen color is too close to the background,
  // flip to white/black so text never disappears on same-tone backgrounds.
  // When a photo background is present, always use white (photo is darkened).
  const hasBgImage = typeof slide.background === 'string' && slide.background.length > 5;

  // Resolve the layout up-front (it's used below for the framed-photo check).
  // Image-only magazine layouts (split/framed/card) look broken without a
  // photo — half-empty panels, empty frames. If there's no image, fall back
  // to a clean text layout so text-only posts always look intentional.
  let layoutResolved = slide.layout || 'centered_focus';
  const imageOnlyLayouts = [];
  if (imageOnlyLayouts.includes(layoutResolved) && !hasBgImage) {
    const textFallbacks = ['editorial_classic', 'minimal_quote', 'paper_box'];
    const pick = (slide.text ? slide.text.length : 0) % textFallbacks.length;
    layoutResolved = textFallbacks[pick];
  }
  const bgLum = hexLuminance(slide.backgroundColor || '#ffffff');
  const contrastColor = (preferred) => {
    if (hasBgImage) return '#FFFFFF';
    const prefLum = hexLuminance(preferred);
    // if preferred and background are both dark or both light -> low contrast
    if (Math.abs(prefLum - bgLum) < 60) {
      return bgLum > 140 ? '#111111' : '#FFFFFF';
    }
    return preferred;
  };

  // Draw the full-bleed background photo FIRST (before any text layout),
  // so all text is drawn on top of the image + readability overlay.
  // EXCEPTION: framed_photo draws the photo small & framed inside its block,
  // not full-bleed — so skip the full-bleed draw for it.
  // These layouts place the photo themselves (framed / in one half), so skip
  // the full-bleed draw for them.
  // Splits place the photo themselves (in one half), so skip the full-bleed
  // draw for them. framed_photo now USES the full-bleed image.
  const selfPlacesImage = [];
  const isFramedPhoto = selfPlacesImage.includes(layoutResolved);
  if (hasBgImage && !isFramedPhoto) {
    try {
      await drawBackgroundImage(slide.background);
    } catch (e) {
      // image failed — fall back to solid background, keep rendering
    }
  }
  
  // Helper: Arrow
  const drawArrow = (fromX, fromY, toX, toY, color) => {
    const path = `M ${fromX} ${fromY} Q ${fromX + (50 * scale)} ${fromY + (50 * scale)} ${toX} ${toY} l ${-10 * scale} ${-5 * scale} M ${toX} ${toY} l ${-5 * scale} ${-10 * scale}`;
    const arrow = new fabric.Path(path, {
      stroke: color,
      strokeWidth: 3 * scale,
      fill: '',
      strokeLineCap: 'round',
      strokeLineJoin: 'round',
      opacity: 0.8,
      selectable: false
    });
    canvas.add(arrow);
  };

  // Helper: Text Processor — strips *accent* markers so asterisks never show
  // as literal characters in any layout. (Accent styling for layouts that
  // support it is applied separately via parseAccent below.)
  const processText = (text) => (text || '').replace(/\*([^*]+)\*/g, '$1');

  // Helper: parse *accent* segments out of a string.
  // Returns { plain, segments: [{text, accent}] } for per-character styling.
  const parseAccent = (text) => {
    const raw = text || '';
    const parts = raw.split(/(\*[^*]+\*)/g).filter((s) => s !== '');
    const segments = parts.map((seg) => {
      const isAccent = seg.startsWith('*') && seg.endsWith('*') && seg.length > 2;
      return { text: isAccent ? seg.slice(1, -1) : seg, accent: isAccent };
    });
    return { plain: segments.map((s) => s.text).join(''), segments };
  };

  // Split text into an editorial structure WITHOUT any markup: short framing
  // lines become small spaced uppercase (sans), the main statement becomes the
  // big serif headline. Mirrors the Eva-Siebenhaar look where the user just
  // types normally. Returns { kicker, headline, footer }.
  const splitEditorial = (text) => {
    const lines = (text || '').split('\n').map((l) => l.trim()).filter(Boolean);
    if (lines.length === 0) return { kicker: '', headline: '', footer: '' };

    // Any straight or typographic quote mark signals a quoted core statement.
    const hasQuote = (s) => /["'\u201C\u201D\u201E\u2033\u00BB\u00AB]/.test(s);
    // A line is "framing" if it's short OR all-caps (kicker/footer style).
    const isFrame = (s) => s.length < 28 || (s === s.toUpperCase() && s.length < 45);

    if (lines.length === 1) {
      const m = lines[0].match(/["'\u201C\u201E\u00BB].+?["'\u201D\u2033\u00AB]/);
      if (m) {
        const headline = m[0];
        const rest = lines[0].replace(m[0], '').trim();
        return { kicker: rest.length && rest.length < 45 ? rest : '', headline, footer: '' };
      }
      return { kicker: '', headline: lines[0], footer: '' };
    }

    // Prefer a quoted line that is NOT all-caps (the real spoken statement);
    // otherwise the longest non-frame line; otherwise the longest line.
    let headlineIdx = -1;
    lines.forEach((l, i) => {
      const quotedStatement = hasQuote(l) && l !== l.toUpperCase();
      if (quotedStatement) { if (headlineIdx === -1 || l.length > lines[headlineIdx].length) headlineIdx = i; }
    });
    if (headlineIdx === -1) {
      let best = -1;
      lines.forEach((l, i) => {
        if (!isFrame(l) && l.length > best) { best = l.length; headlineIdx = i; }
      });
    }
    if (headlineIdx === -1) {
      let best = -1;
      lines.forEach((l, i) => { if (l.length > best) { best = l.length; headlineIdx = i; } });
    }

    const kicker = lines.slice(0, headlineIdx).join(' ');
    const footer = lines.slice(headlineIdx + 1).join(' ');
    return { kicker, headline: lines[headlineIdx], footer };
  };

  // Helper: apply accent color + accent font to *..* parts of a Textbox
  const applyAccentStyles = (textObj, segments) => {
    try {
      let idx = 0;
      segments.forEach((s) => {
        if (s.accent && s.text.length) {
          textObj.setSelectionStyles(
            { fill: accentColor, fontStyle: 'italic', fontFamily: accentFont },
            idx,
            idx + s.text.length
          );
        }
        idx += s.text.length;
      });
    } catch (e) {
      // best-effort; plain text still renders
    }
  };

  // === STRATEGY: LAYOUT ENGINE ===
  let layout = layoutResolved;
  // Strong text shadow whenever text sits on a photo, for readability.
  const textShadow = hasBgImage ? 'rgba(0,0,0,0.7) 0px 2px 12px' : '';

  // === COVER WITH PHOTO: auto-place title in the image's quiet zone ===
  // When a background photo is present, ignore the abstract layout and place
  // the title where the image has free/quiet space (from image analysis).
  // === SARAH-JOY STYLE COVER (editorial photo cover) ===
  // Rich cover: photo bg + small label chip (top) + serif title with one
  // italic/script accent word + subtitle + small brand mark (bottom).
  if (hasBgImage && (layout === 'sarah_cover' || slide.coverStyle === 'sarah')) {
    const { plain, segments } = parseAccent(slide.text);

    // Extra readability: dark gradient-ish band at the bottom third.
    canvas.add(new fabric.Rect({
      left: 0, top: height * 0.55, width, height: height * 0.45,
      fill: 'rgba(0,0,0,0.28)', selectable: false,
    }));

    // 1) LABEL CHIP (top-left) — e.g. "GRATIS CHALLENGE"
    if (slide.label) {
      const labelText = String(slide.label).toUpperCase();
      const chipPadX = fs(14);
      const chipFontSize = fs(13);
      const tmp = new fabric.Text(labelText, { fontSize: chipFontSize, fontFamily: 'Inter', fontWeight: 'bold' });
      const chipW = tmp.width + chipPadX * 2;
      const chipH = fs(34);
      canvas.add(new fabric.Rect({
        left: width * 0.08, top: height * 0.09, width: chipW, height: chipH,
        fill: '#FFFFFF', rx: fs(4), ry: fs(4), selectable: false,
      }));
      canvas.add(new fabric.Text(labelText, {
        left: width * 0.08 + chipPadX, top: height * 0.09 + chipH / 2,
        originY: 'center', fontSize: chipFontSize, fontFamily: 'Inter',
        fontWeight: 'bold', fill: '#1a1a1a', charSpacing: 80, selectable: false,
      }));
    }

    // 2) TITLE (lower third), serif, with italic/script accent word
    const titleObj = new fabric.Textbox(plain, {
      left: width * 0.08,
      top: height * 0.72,
      originX: 'left',
      originY: 'center',
      width: width * 0.84,
      fontSize: fs(slide.fontSize || 52),
      fontFamily: fontFamily,
      fill: '#FFFFFF',
      textAlign: 'left',
      lineHeight: 1.1,
      fontWeight: slide.fontWeight || '600',
      shadow: 'rgba(0,0,0,0.35) 0px 2px 10px',
    });
    try {
      let idx = 0;
      segments.forEach((s) => {
        if (s.accent && s.text.length) {
          titleObj.setSelectionStyles(
            { fill: accentColor, fontStyle: 'italic', fontFamily: accentFont },
            idx, idx + s.text.length
          );
        }
        idx += s.text.length;
      });
    } catch (e) { /* best-effort */ }
    canvas.add(titleObj);

    // 3) SUBTITLE (small, under title)
    if (slide.secondaryText) {
      canvas.add(new fabric.Textbox(slide.secondaryText, {
        left: width * 0.08, top: height * 0.86, originX: 'left',
        width: width * 0.7, fontSize: fs(20), fontFamily: 'Inter',
        fill: 'rgba(255,255,255,0.9)', lineHeight: 1.3, selectable: false,
      }));
    }

    // 4) BRAND MARK (bottom-left small)
    if (options.globalBrandName) {
      canvas.add(new fabric.Text(options.globalBrandName.toUpperCase(), {
        left: width * 0.08, top: height - (padding * 0.5), fontSize: fs(13),
        fill: 'rgba(255,255,255,0.85)', fontFamily: 'Inter', charSpacing: 120,
        originY: 'bottom', selectable: false,
      }));
    }

    canvas.renderAll();
    return;
  }

  const coverLayouts = ['cover_top_left', 'cover_bottom_left', 'cover_bottom_center', 'cover_center_hero', 'cover_top_center'];
  if (hasBgImage && coverLayouts.includes(layout)) {
    const { plain, segments } = parseAccent(slide.text);

    // Position priority: explicit cover_* layout > image quiet zone > center
    const coverPositions = {
      cover_top_left:      { col: 'left',   row: 'top' },
      cover_bottom_left:   { col: 'left',   row: 'bottom' },
      cover_bottom_center: { col: 'center', row: 'bottom' },
      cover_center_hero:   { col: 'center', row: 'mid' },
      cover_top_center:    { col: 'center', row: 'top' },
    };

    let col, row;
    if (coverPositions[layout]) {
      ({ col, row } = coverPositions[layout]);
    } else {
      const zone = slide._autoImage?.quietZone || 'center';
      col = zone.includes('left') ? 'left' : zone.includes('right') ? 'right' : 'center';
      row = zone.includes('top') ? 'top' : zone.includes('bottom') ? 'bottom' : 'mid';
    }

    const boxWidth = width * 0.8;
    let left = width / 2;
    let originX = 'center';
    let textAlign = 'center';
    if (col === 'left') { left = width * 0.08; originX = 'left'; textAlign = 'left'; }
    else if (col === 'right') { left = width * 0.92; originX = 'right'; textAlign = 'right'; }

    let top = height / 2;
    let originY = 'center';
    if (row === 'top') { top = height * 0.12; originY = 'top'; }
    else if (row === 'bottom') { top = height * 0.88; originY = 'bottom'; }

    const titleObj = new fabric.Textbox(plain, {
      left,
      top,
      originX,
      originY,
      width: boxWidth,
      fontSize: fs(slide.fontSize || 46),
      fontFamily: fontFamily,
      fill: '#FFFFFF',
      textAlign,
      lineHeight: 1.2,
      fontWeight: slide.fontWeight || 'bold',
      shadow: 'rgba(0,0,0,0.45) 0px 2px 8px',
    });
    // accent word keeps accent color even on photo
    try {
      let idx = 0;
      segments.forEach((s) => {
        if (s.accent && s.text.length) {
          titleObj.setSelectionStyles(
            { fill: accentColor, fontStyle: 'italic', fontFamily: accentFont },
            idx, idx + s.text.length
          );
        }
        idx += s.text.length;
      });
    } catch (e) { /* best-effort */ }
    canvas.add(titleObj);

    // Brand name + slide number still drawn below
    if (options.globalBrandName) {
      canvas.add(new fabric.Text(options.globalBrandName.toUpperCase(), {
        left: width / 2, top: height - (padding / 2), fontSize: fs(14),
        fill: 'rgba(255,255,255,0.85)', fontFamily: 'Inter',
        originX: 'center', originY: 'bottom',
      }));
    }
    canvas.renderAll();
    return; // cover is complete — skip the abstract layout engine
  }

  // === SMART IMAGE TEXT: find the best spot in the photo and put text there.
  // Preferred: clean white text + soft shadow (NO box). Only if the best spot
  // is still too bright for readable text do we add a gentle local scrim. ===
  const specialImageLayouts = ['tweet_card', 'glass_layer', 'aesthetic_checklist', 'diagonal_overlay', 'split_color', 'paper_box', 'story_text_box', 'bold_number_list'];
  if (hasBgImage && !specialImageLayouts.includes(layout)) {
    const { plain, segments } = parseAccent(slide.text);
    const zone = (slide._autoImage && slide._autoImage.quietZone) || 'center';
    const quietBrightness = (slide._autoImage && typeof slide._autoImage.quietBrightness === 'number')
      ? slide._autoImage.quietBrightness : 90;

    const isTop = zone.includes('top');
    const isBottom = zone.includes('bottom');
    const isLeft = zone.includes('left');
    const isRight = zone.includes('right');

    const rowY = isTop ? height * 0.22 : isBottom ? height * 0.80 : height * 0.5;
    const align = isLeft ? 'left' : isRight ? 'right' : 'center';
    const boxW = width * 0.84;
    const originX = align === 'center' ? 'center' : (align === 'right' ? 'right' : 'left');
    const textLeft = align === 'center' ? width / 2 : (align === 'right' ? width - padding : padding);

    const tObj = new fabric.Textbox(plain, {
      left: textLeft, top: rowY, originX, originY: 'center',
      width: boxW, fontSize: fs(slide.fontSize || 42), fontFamily: fontFamily,
      fill: slide.color || '#FFFFFF', textAlign: slide.textAlign || align, lineHeight: 1.28,
      fontWeight: slide.fontWeight || 'normal',
      fontStyle: slide.fontStyle || 'normal',
      shadow: slide.noShadow ? '' : 'rgba(0,0,0,0.85) 0px 2px 16px',
    });

    // NOTFALL only: quiet zone is too bright (>135) -> add a soft local scrim
    // so white text stays legible. Otherwise: shadow alone, no box.
    if (quietBrightness > 135) {
      const padX = fs(30), padY = fs(24);
      const scrim = new fabric.Rect({
        left: textLeft, top: rowY, originX, originY: 'center',
        width: Math.min(tObj.width + padX * 2, width - padding * 0.5),
        height: tObj.height + padY * 2,
        rx: fs(18), ry: fs(18),
        fill: new fabric.Gradient({
          type: 'radial',
          coords: { x1: (tObj.width) / 2, y1: (tObj.height) / 2, r1: 0, x2: (tObj.width) / 2, y2: (tObj.height) / 2, r2: tObj.width * 0.7 },
          colorStops: [
            { offset: 0, color: 'rgba(0,0,0,0.42)' },
            { offset: 1, color: 'rgba(0,0,0,0.0)' },
          ],
        }),
        selectable: false,
      });
      canvas.add(scrim);
    }

    applyAccentStyles(tObj, segments);
    canvas.add(tObj);
    canvas.renderAll();
    return;
  }


  // === ADAPTIVE AUTO LAYOUT ===
  // One layout to rule them all. The post design engine decides textAnchor
  // (row/col) and bold; here we just draw a headline at that position, with a
  // photo (full-bleed) or on the brand background. Auto-fit keeps text inside.
  if (layout === 'auto') {
    const { plain, segments } = parseAccent(slide.text);

    // === STORY MODE (9:16): fixed, minimal branding ===
    // Small Montserrat text, always same position (lower third), no bold, so it
    // reads as a calm base you can just copy the text from and overwrite in IG.
    const isStory = slide.format === '9:16' || Math.abs((height / width) - (16 / 9)) < 0.1;
    if (isStory) {
      // Light readability wash at the bottom if there's a photo.
      if (hasBgImage) {
        canvas.add(new fabric.Rect({
          left: 0, top: height * 0.62, width, height: height * 0.38,
          fill: 'rgba(0,0,0,0.35)', selectable: false,
        }));
      }
      const storyText = new fabric.Textbox(plain, {
        left: width / 2, top: height * 0.72, originX: 'center', originY: 'center',
        width: width * 0.78,
        fontSize: fs(22),                 // small, calm
        fontFamily: 'Montserrat',
        fontWeight: '400',                // never bold
        fill: hasBgImage ? '#FFFFFF' : contrastColor(slide.backgroundColor || '#fff'),
        textAlign: 'center', lineHeight: 1.35,
        shadow: hasBgImage ? 'rgba(0,0,0,0.5) 0px 1px 6px' : '',
      });
      applyAccentStyles(storyText, segments);
      canvas.add(storyText);
      // Small brand mark at the very bottom.
      if (options.globalBrandName) {
        canvas.add(new fabric.Text(options.globalBrandName.toUpperCase(), {
          left: width / 2, top: height * 0.95, originX: 'center', originY: 'bottom',
          fontSize: fs(11), fill: hasBgImage ? 'rgba(255,255,255,0.85)' : accentColor,
          fontFamily: 'Montserrat', charSpacing: 150, selectable: false,
        }));
      }
      canvas.renderAll();
      return;
    }

    const anchor = slide.textAnchor && typeof slide.textAnchor === 'object'
      ? slide.textAnchor : { row: hasBgImage ? 'bottom' : 'mid', col: 'center' };
    const row = anchor.row || 'mid';
    const col = anchor.col || 'center';

    // Editorial Dark: an extra dark/desaturated wash over the whole photo so
    // any image takes on the moody editorial tone (Eva-Siebenhaar look).
    if (hasBgImage && slide.darkPhoto) {
      canvas.add(new fabric.Rect({
        left: 0, top: 0, width, height,
        fill: 'rgba(20,14,9,0.45)', selectable: false,
      }));
    }

    // On photos, add a soft readability gradient on the half where the text sits.
    if (hasBgImage) {
      const bandTop = row === 'top' ? 0 : row === 'bottom' ? height * 0.5 : height * 0.28;
      const bandH = row === 'mid' ? height * 0.44 : height * 0.5;
      canvas.add(new fabric.Rect({
        left: 0, top: bandTop, width, height: bandH,
        fill: 'rgba(0,0,0,0.42)', selectable: false,
      }));
    }

    // KICKER: small letter-spaced uppercase label at the very top
    // ("SELL IT WITH A STORY"). Only when the preset asks for it.
    if (slide.kicker && (slide.kickerText || options.kickerText)) {
      canvas.add(new fabric.Text((slide.kickerText || options.kickerText).toUpperCase(), {
        left: width / 2, top: height * 0.08, originX: 'center', originY: 'top',
        fontSize: fs(13), fill: hasBgImage ? 'rgba(255,255,255,0.9)' : accentColor,
        fontFamily: 'Montserrat', charSpacing: 300, fontWeight: '500', selectable: false,
      }));
    }

    // (Accent line removed — the brand mark near the text carries the brand.)

    // Position.
    let left = width / 2, originX = 'center', textAlign = 'center';
    if (col === 'left') { left = width * 0.10; originX = 'left'; textAlign = 'left'; }
    else if (col === 'right') { left = width * 0.90; originX = 'right'; textAlign = 'right'; }

    let top = height / 2, originY = 'center';
    if (row === 'top') { top = height * 0.18; originY = 'top'; }
    else if (row === 'bottom') { top = height * 0.82; originY = 'bottom'; }

    // === EDITORIAL AUTO TWO-FONT MODE ===
    // No markup needed: split into small uppercase frame lines (sans) + big
    // serif headline. Only when the Editorial preset is active.
    if (slide.editorialDark || slide.editorialAuto) {
      const { kicker: kickTxt, headline, footer } = splitEditorial(slide.text);
      const centerX = width / 2;
      // Vertical stack, centered as a group around the anchor row.
      let stackTop = row === 'top' ? height * 0.14 : row === 'bottom' ? height * 0.42 : height * 0.30;
      const lightText = hasBgImage ? '#FFFFFF' : contrastColor(slide.backgroundColor || '#fff');
      const dimText = hasBgImage ? 'rgba(255,255,255,0.9)' : accentColor;
      const sh = hasBgImage ? 'rgba(0,0,0,0.55) 0px 2px 12px' : '';

      // Kicker (small, spaced, uppercase — sans)
      if (kickTxt) {
        const k = new fabric.Textbox(kickTxt.toUpperCase(), {
          left: centerX, top: stackTop, originX: 'center', originY: 'top',
          width: width * 0.8, fontSize: fs(15), fill: dimText,
          fontFamily: 'Montserrat', fontWeight: '500', charSpacing: 200,
          textAlign: 'center', lineHeight: 1.3, shadow: sh,
        });
        canvas.add(k);
        stackTop += k.height + height * 0.02;
      }

      // Headline (big serif, italic-friendly)
      const h = new fabric.Textbox(headline, {
        left: centerX, top: stackTop, originX: 'center', originY: 'top',
        width: width * 0.86, fontSize: fs(slide.fontSize || 54),
        fill: lightText, fontFamily: 'Playfair Display', fontWeight: '500',
        textAlign: 'center', lineHeight: 1.08, shadow: sh,
      });
      canvas.add(h);
      stackTop += h.height + height * 0.02;

      // Footer (small, spaced, uppercase — sans)
      if (footer) {
        canvas.add(new fabric.Textbox(footer.toUpperCase(), {
          left: centerX, top: stackTop, originX: 'center', originY: 'top',
          width: width * 0.8, fontSize: fs(15), fill: dimText,
          fontFamily: 'Montserrat', fontWeight: '500', charSpacing: 150,
          textAlign: 'center', lineHeight: 1.3, shadow: sh,
        }));
      }

      // Brand mark near bottom.
      if (options.globalBrandName) {
        canvas.add(new fabric.Text(options.globalBrandName.toUpperCase(), {
          left: centerX, top: height * 0.93, originX: 'center', originY: 'bottom',
          fontSize: fs(12), fill: dimText, fontFamily: 'Montserrat',
          charSpacing: 200, selectable: false,
        }));
      }
      canvas.renderAll();
      return;
    }

    const titleObj = new fabric.Textbox(plain, {
      left, top, originX, originY,
      width: width * 0.82,
      fontSize: fs(slide.fontSize || 42),
      fontFamily,
      fill: hasBgImage ? '#FFFFFF' : contrastColor(slide.backgroundColor || '#fff'),
      textAlign, lineHeight: 1.2,
      fontWeight: slide.fontWeight || 'normal',
      shadow: hasBgImage ? 'rgba(0,0,0,0.5) 0px 2px 10px' : '',
    });
    applyAccentStyles(titleObj, segments);
    canvas.add(titleObj);

    // Brand mark: placed at a FIXED, safe position so it never collides with
    // the headline regardless of text length. It simply anchors to the opposite
    // edge from the headline.
    if (options.globalBrandName) {
      const brandColor = hasBgImage ? 'rgba(255,255,255,0.9)' : accentColor;
      let markTop, markOriginY;
      if (row === 'bottom') {
        // headline low -> brand mark near the TOP
        markTop = height * 0.10; markOriginY = 'top';
      } else if (row === 'top') {
        // headline high -> brand mark near the BOTTOM
        markTop = height * 0.90; markOriginY = 'bottom';
      } else {
        // headline centered -> brand mark near the bottom, safely clear
        markTop = height * 0.90; markOriginY = 'bottom';
      }
      canvas.add(new fabric.Text(options.globalBrandName.toUpperCase(), {
        left: width / 2, top: markTop, originX: 'center', originY: markOriginY,
        fontSize: fs(12), fill: brandColor,
        fontFamily: 'Inter', charSpacing: 150, selectable: false,
      }));
    }
    canvas.renderAll();
    return;
  }


  // 1. EDITORIAL CLASSIC (Line + Title + Body)
  if (layout === 'editorial_classic' || layout === 'minimal_editorial') {
    // Top Line
    const line = new fabric.Line([padding, padding, width - padding, padding], {
      stroke: accentColor,
      strokeWidth: 2 * scale,
      selectable: false
    });
    canvas.add(line);

    // Vertical anchor: vary the starting Y so text-only posts don't all sit at
    // the top. top -> just under the line; center -> vertically centered;
    // bottom -> lower third.
    let currentY = padding + (40 * scale);
    if (slide.textAnchor === 'center') currentY = height * 0.40;
    else if (slide.textAnchor === 'bottom') currentY = height * 0.58;

    // Optional Secondary Text (Hook)
    if (slide.secondaryText) {
      const secText = new fabric.Textbox(slide.secondaryText, {
        left: padding,
        top: currentY,
        width: width - (padding * 2),
        fontSize: fs(slide.secondaryFontSize || 32),
        fontFamily: slide.secondaryFontFamily || accentFont,
        fill: slide.secondaryTextColor || secondaryColor,
        fontStyle: slide.secondaryFontStyle || 'italic',
        textAlign: slide.secondaryTextAlign || 'left'
      });
      canvas.add(secText);
      currentY += secText.height + (20 * scale);
    }

    // Main Body
    const { plain: ecPlain, segments: ecSegs } = parseAccent(slide.text);
    const mainText = new fabric.Textbox(ecPlain, {
      left: padding,
      top: currentY,
      width: width - (padding * 2),
      fontSize: fs(slide.fontSize || 40),
      fontFamily: fontFamily,
      fill: slide.color || contrastColor(primaryColor),
      lineHeight: 1.3,
      textAlign: slide.textAlign || 'left',
      fontWeight: slide.fontWeight || 'normal',
      fontStyle: slide.fontStyle || 'normal',
      shadow: slide.noShadow ? '' : textShadow
    });
    applyAccentStyles(mainText, ecSegs);
    canvas.add(mainText);
  }

  // 2. PAPER BOX (Shadow Box)
  else if (layout === 'paper_box' || layout === 'story_text_box') {
    const boxMargin = width * 0.12;
    // Use the brand's secondary or background tone for the card, not hardcoded white.
    const boxFill = slide.secondaryColor || slide.backgroundColor || '#ffffff';
    const boxTextColor = contrastColor(boxFill);
    const boxRect = new fabric.Rect({
      left: boxMargin,
      top: boxMargin,
      width: width - (boxMargin * 2),
      height: height - (boxMargin * 2),
      fill: boxFill,
      shadow: 'rgba(0,0,0,0.15) 0px 10px 20px',
      rx: 10 * scale,
      ry: 10 * scale,
      selectable: false
    });
    canvas.add(boxRect);

    const innerWidth = width - (boxMargin * 2) - (80 * scale);
    const cleanText = processText(slide.text);
    // Shrink font if a very long word would overflow the inner box width.
    const longestWord = cleanText.split(/\s+/).reduce((a, b) => (b.length > a.length ? b : a), '');
    let boxFont = fs(slide.fontSize || 36);
    // rough width estimate: ~0.6em per char; reduce font so longest word fits
    const estWordWidth = longestWord.length * boxFont * 0.6;
    if (estWordWidth > innerWidth) {
      boxFont = boxFont * (innerWidth / estWordWidth) * 0.95;
    }

    const textObj = new fabric.Textbox(cleanText, {
      left: width / 2,
      top: height / 2,
      originX: 'center',
      originY: 'center',
      width: innerWidth,
      fontSize: boxFont,
      fontFamily: fontFamily,
      fill: boxTextColor,
      textAlign: 'center',
      lineHeight: 1.35,
      breakWords: true
    });
    canvas.add(textObj);
  }

  // 3. SPLIT COLOR (Top/Bottom)
  else if (layout === 'split_color') {
    const topFill = slide.backgroundColor || '#ffffff';
    // Top Half (brand background)
    canvas.add(new fabric.Rect({ left: 0, top: 0, width: width, height: height * 0.4, fill: topFill, selectable: false }));
    // Bottom Half (Accent)
    canvas.add(new fabric.Rect({ left: 0, top: height * 0.4, width: width, height: height * 0.6, fill: accentColor, selectable: false }));

    // Top Text
    if (slide.secondaryText) {
      canvas.add(new fabric.Textbox(slide.secondaryText, {
        left: padding,
        top: (height * 0.4) / 2,
        originY: 'center',
        width: width - (padding * 2),
        fontSize: fs(slide.secondaryFontSize || 42),
        fontFamily: slide.secondaryFontFamily || accentFont,
        fill: slide.secondaryTextColor || contrastColor(topFill),
        textAlign: slide.secondaryTextAlign || 'center',
        fontStyle: slide.secondaryFontStyle || 'italic'
      }));
    }

    // Bottom Text
    canvas.add(new fabric.Textbox(processText(slide.text), {
      left: padding,
      top: (height * 0.4) + ((height * 0.6) / 2),
      originY: 'center',
      width: width - (padding * 2),
      fontSize: fs(slide.fontSize || 38),
      fontFamily: fontFamily,
      fill: contrastColor(accentColor),
      textAlign: 'center',
      fontWeight: slide.fontWeight || 'bold'
    }));
  }

  // 4. BOLD NUMBER LIST (For "Big Numbers" layout)
  else if (layout === 'bold_number_list') {
     const items = slide.text.split('\n').filter(l => l.trim());
     let currentY = padding + (60 * scale);
     
     items.forEach((item, idx) => {
        // Check if item starts with number
        const match = item.match(/^(\d+)[.)]?\s*(.*)/);
        if (match) {
            const num = match[1];
            const content = match[2];
            
            const numObj = new fabric.Text(num, {
                left: padding,
                top: currentY,
                fontSize: fs(64),
                fontFamily: accentFont,
                fill: accentColor,
                fontWeight: 'bold',
                originY: 'top'
            });
            canvas.add(numObj);
            
            const textObj = new fabric.Textbox(content, {
                left: padding + (80 * scale),
                top: currentY + (10 * scale),
                width: width - (padding * 2) - (80 * scale),
                fontSize: fs(32),
                fontFamily: fontFamily,
                fill: primaryColor,
                originY: 'top'
            });
            canvas.add(textObj);
            currentY += Math.max(numObj.height, textObj.height) + (30 * scale);
        } else {
            const textObj = new fabric.Textbox(item, {
                left: padding,
                top: currentY,
                width: width - (padding * 2),
                fontSize: fs(32),
                fontFamily: fontFamily,
                fill: primaryColor
            });
            canvas.add(textObj);
            currentY += textObj.height + (20 * scale);
        }
     });
  }

  // === TWEET CARD: white rounded card like a tweet/post ===
  else if (layout === 'tweet_card') {
    const cardMargin = width * 0.08;
    const cardTop = height * 0.18;
    const cardH = height * 0.64;
    canvas.add(new fabric.Rect({
      left: cardMargin, top: cardTop, width: width - cardMargin * 2, height: cardH,
      fill: '#FFFFFF', rx: fs(24), ry: fs(24),
      shadow: 'rgba(0,0,0,0.18) 0px 12px 30px', selectable: false,
    }));
    // little avatar dot + handle line
    canvas.add(new fabric.Circle({
      left: cardMargin + fs(28), top: cardTop + fs(28), radius: fs(20),
      fill: accentColor, selectable: false,
    }));
    canvas.add(new fabric.Text('@deinhandle', {
      left: cardMargin + fs(64), top: cardTop + fs(34), fontSize: fs(18),
      fontFamily: 'Inter', fill: '#657786', selectable: false,
    }));
    const { plain, segments } = parseAccent(slide.text);
    const tw = new fabric.Textbox(plain, {
      left: cardMargin + fs(28), top: cardTop + fs(90),
      width: width - cardMargin * 2 - fs(56),
      fontSize: fs(slide.fontSize || 34), fontFamily: fontFamily,
      fill: '#15202B', lineHeight: 1.35, textAlign: 'left',
    });
    applyAccentStyles(tw, segments);
    canvas.add(tw);
  }

  // === GLASS OVERLAY: frosted translucent panel over background ===
  else if (layout === 'glass_layer') {
    const gm = width * 0.1;
    const gTop = height * 0.28;
    const gH = height * 0.44;
    // translucent panel
    canvas.add(new fabric.Rect({
      left: gm, top: gTop, width: width - gm * 2, height: gH,
      fill: hasBgImage ? 'rgba(255,255,255,0.18)' : 'rgba(255,255,255,0.10)',
      stroke: 'rgba(255,255,255,0.45)', strokeWidth: 1.5 * scale,
      rx: fs(20), ry: fs(20), selectable: false,
    }));
    const { plain, segments } = parseAccent(slide.text);
    const gtext = new fabric.Textbox(plain, {
      left: width / 2, top: gTop + gH / 2, originX: 'center', originY: 'center',
      width: width - gm * 2 - fs(48),
      fontSize: fs(slide.fontSize || 40), fontFamily: fontFamily,
      fill: hasBgImage ? '#FFFFFF' : contrastColor(primaryColor),
      textAlign: slide.textAlign || 'center', lineHeight: 1.25, fontWeight: slide.fontWeight || 'normal',
      shadow: hasBgImage ? 'rgba(0,0,0,0.4) 0px 2px 8px' : '',
    });
    applyAccentStyles(gtext, segments);
    canvas.add(gtext);
  }

  // === AESTHETIC CHECKLIST: list with check marks + thin lines ===
  else if (layout === 'aesthetic_checklist') {
    const items = (slide.text || '').split('\n').map((l) => l.replace(/^[-•*]\s*/, '').trim()).filter(Boolean);
    const startY = height * 0.28;
    const lineGap = Math.min((height * 0.5) / Math.max(items.length, 1), fs(90));
    const leftX = width * 0.14;
    items.forEach((item, i) => {
      const y = startY + i * lineGap;
      // check circle
      canvas.add(new fabric.Circle({
        left: leftX, top: y, radius: fs(12), fill: '', stroke: accentColor,
        strokeWidth: 2 * scale, selectable: false,
      }));
      // check mark
      canvas.add(new fabric.Path(`M ${leftX + fs(5)} ${y + fs(12)} L ${leftX + fs(10)} ${y + fs(18)} L ${leftX + fs(20)} ${y + fs(5)}`, {
        stroke: accentColor, strokeWidth: 2.5 * scale, fill: '', selectable: false,
      }));
      // item text
      canvas.add(new fabric.Textbox(item, {
        left: leftX + fs(40), top: y - fs(2), width: width - leftX - fs(80),
        fontSize: fs(28), fontFamily: fontFamily, fill: contrastColor(primaryColor),
        lineHeight: 1.2, selectable: false,
      }));
      // thin separator line
      canvas.add(new fabric.Line([leftX, y + lineGap * 0.62, width - width * 0.14, y + lineGap * 0.62], {
        stroke: 'rgba(150,150,150,0.3)', strokeWidth: 1 * scale, selectable: false,
      }));
    });
  }

  // === DIAGONAL OVERLAY: modern diagonal split ===
  else if (layout === 'diagonal_overlay') {
    // diagonal accent triangle (bottom-left)
    canvas.add(new fabric.Polygon(
      [ { x: 0, y: height }, { x: 0, y: height * 0.45 }, { x: width, y: height } ],
      { fill: accentColor, opacity: hasBgImage ? 0.82 : 1, selectable: false }
    ));
    const { plain, segments } = parseAccent(slide.text);
    const dtext = new fabric.Textbox(plain, {
      left: width * 0.08, top: height * 0.78, originY: 'center',
      width: width * 0.8,
      fontSize: fs(slide.fontSize || 40), fontFamily: fontFamily,
      fill: '#FFFFFF', textAlign: 'left', lineHeight: 1.2, fontWeight: slide.fontWeight || '700',
      shadow: 'rgba(0,0,0,0.3) 0px 2px 6px',
    });
    applyAccentStyles(dtext, segments);
    canvas.add(dtext);
  }

  // === SPLIT PHOTO: photo fills one half, text sits in the other half ===
  // (Like the reference: foto rechts, text links — or top/bottom.)
  // === SPLIT PHOTO: photo one side, branded text panel on the other ===


  // === CARD ON PHOTO: a branded card floating over a photo/tonal bg ===

  // 5. MINIMAL QUOTE (Cover / Brand preview) — supports *accent* word
  else if (layout === 'minimal_quote' || layout === 'maximized_bold') {
    const mainColor = contrastColor(primaryColor);
    const { plain, segments } = parseAccent(slide.text);

    const boxWidth = width - (padding * 2);
    let fontSize = fs(slide.fontSize || 44);

    // Auto-shrink so the longest single word fits the box width.
    // (maximized_bold uses huge fonts; long German words can overflow.)
    try {
      const longestWord = plain.split(/\s+/).reduce((a, b) => (a.length >= b.length ? a : b), '');
      const measure = new fabric.Text(longestWord, { fontSize, fontFamily, fontWeight: slide.fontWeight || 'bold' });
      if (measure.width > boxWidth && measure.width > 0) {
        fontSize = Math.floor(fontSize * (boxWidth / measure.width) * 0.96);
      }
    } catch (e) { /* measure best-effort */ }

    const anchorY = slide.textAnchor === 'top' ? height * 0.28
      : slide.textAnchor === 'bottom' ? height * 0.72
      : height / 2;
    // maximized_bold is meant to be bold; minimal_quote defaults to normal.
    const defaultWeight = layout === 'maximized_bold' ? 'bold' : 'normal';
    const textObj = new fabric.Textbox(plain, {
      left: padding,
      top: anchorY,
      originY: 'center',
      width: boxWidth,
      fontSize: fontSize,
      fontFamily: fontFamily,
      fill: slide.color || mainColor,
      textAlign: slide.textAlign || 'center',
      lineHeight: 1.25,
      fontWeight: slide.fontWeight || defaultWeight,
      splitByGrapheme: false,
      shadow: textShadow,
    });
    applyAccentStyles(textObj, segments);
    canvas.add(textObj);
  }

  // 6. CENTERED FOCUS (Default)
  else {
    const { plain: cfPlain, segments: cfSegs } = parseAccent(slide.text);
    const textObj = new fabric.Textbox(cfPlain, {
      left: padding,
      top: height / 2,
      originY: 'center',
      width: width - (padding * 2),
      fontSize: fs(slide.fontSize || 48),
      fontFamily: fontFamily,
      fill: slide.color || contrastColor(primaryColor),
      textAlign: slide.textAlign || 'center',
      lineHeight: 1.3,
      shadow: textShadow
    });
    applyAccentStyles(textObj, cfSegs);
    canvas.add(textObj);
  }

  // --- OVERLAYS & LOGO ---
  // Slide Number
  if (options.totalSlides > 1 && typeof options.slideIndex === 'number') {
    const numText = new fabric.Text(`${options.slideIndex + 1}/${options.totalSlides}`, {
      left: width - padding,
      top: padding / 2,
      fontSize: 16 * scale,
      fill: secondaryColor,
      fontFamily: 'Inter',
      originX: 'right'
    });
    canvas.add(numText);
  }

  // Brand Name — skip for layouts that position their own brand mark, so it
  // doesn't appear twice.
  const drawsOwnBrandMark = [];
  if (options.globalBrandName && !drawsOwnBrandMark.includes(layout)) {
    const brandText = new fabric.Text(options.globalBrandName.toUpperCase(), {
      left: width / 2,
      top: height - (padding / 2),
      fontSize: 14 * scale,
      fill: secondaryColor,
      fontFamily: 'Inter',
      originX: 'center',
      originY: 'bottom',
      letterSpacing: 100
    });
    canvas.add(brandText);
  }

  // --- GRAIN TEXTURE ---
  // Subtle noise overlay across the whole slide (slide.grain 0..0.5).
  if (typeof slide.grain === 'number' && slide.grain > 0) {
    try {
      const gCan = document.createElement('canvas');
      gCan.width = 120; gCan.height = 120;
      const gctx = gCan.getContext('2d');
      const imgData = gctx.createImageData(120, 120);
      for (let i = 0; i < imgData.data.length; i += 4) {
        const v = Math.random() * 255;
        imgData.data[i] = v; imgData.data[i + 1] = v; imgData.data[i + 2] = v;
        imgData.data[i + 3] = 255;
      }
      gctx.putImageData(imgData, 0, 0);
      const grainImg = new fabric.Pattern({ source: gCan, repeat: 'repeat' });
      canvas.add(new fabric.Rect({
        left: 0, top: 0, width, height,
        fill: grainImg, opacity: Math.min(slide.grain, 0.5), selectable: false,
      }));
    } catch (e) { /* grain optional */ }
  }

  // --- LOGO / STICKER OVERLAY (second image on top) ---
  // Draw a SMALL framed photo (not full-bleed). Returns true only if the
  // image actually loaded & drew; false otherwise so the caller can fall back.
  // No clipPath (which is fragile in fabric v5) — instead we fit the image to
  // the box height/width and rely on the caller drawing a frame over the edges.

  const drawOverlayImage = (src) =>
    new Promise((resolve) => {
      if (!src) return resolve(false);
      fabric.Image.fromURL(src, (img) => {
        if (!img) return resolve(false);
        const sc = (typeof slide.overlayImageScale === 'number' ? slide.overlayImageScale : 0.3);
        // scale so the overlay image's width = sc * canvas width
        const targetW = width * sc;
        const factor = targetW / img.width;
        const ox = (typeof slide.overlayImageX === 'number' ? slide.overlayImageX : 0) * scale;
        const oy = (typeof slide.overlayImageY === 'number' ? slide.overlayImageY : 0) * scale;
        img.set({
          originX: 'center', originY: 'center',
          left: width / 2 + ox, top: height / 2 + oy,
          scaleX: factor, scaleY: factor, selectable: false,
        });
        if (slide.overlayImageRounded) {
          img.clipPath = new fabric.Circle({
            radius: Math.min(img.width, img.height) / 2,
            originX: 'center', originY: 'center',
          });
        }
        canvas.add(img);
        resolve(true);
      }, { crossOrigin: 'anonymous' });
    });

  if (slide.overlayImage) {
    try { await drawOverlayImage(slide.overlayImage); } catch (e) { /* optional */ }
  }

  // Render & Wait
  canvas.renderAll();
};