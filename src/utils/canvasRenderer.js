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
          // coverBlurMode: follow-up slides (index > 0) reuse the cover photo
          // blurred + darkened, so carousels stay calm and readable.
          const isFollowUp = coverBlurActive && (options.slideIndex || 0) > 0;
          const effBlur = isFollowUp ? Math.max(slide.blur || 0, 12) : slide.blur;
          if (typeof effBlur === 'number' && effBlur >= 1 && fabric.Image.filters?.Blur) {
            try {
              img.filters = [new fabric.Image.filters.Blur({ blur: Math.min(effBlur / 40, 0.5) })];
              img.applyFilters();
            } catch (e) { /* blur optional */ }
          }
          canvas.add(img);
          canvas.sendToBack(img);

          // Readability overlay — kept light so the photo stays vibrant.
          // EDITORIAL slides skip this entirely: they apply their own light
          // tone + a local text scrim. Stacking all three made photos muddy.
          // Follow-up slides in cover-blur mode get darkening (their scrim is
          // skipped), everything else editorial stays bright.
          const isEditorialSlide = slide.editorialDark === true || slide.editorialAuto === true;
          let ov = typeof slide.overlay === 'number' ? slide.overlay : 0.28;
          if (isEditorialSlide) ov = isFollowUp ? 0.42 : 0;
          else if (isFollowUp) ov = Math.max(ov, 0.42);
          const overlayRect = new fabric.Rect({
            left: 0, top: 0, width, height,
            fill: `rgba(0,0,0,${ov})`, selectable: false,
          });
          if (ov > 0) canvas.add(overlayRect);

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
  // Cover-blur mode: follow-up slides show the cover photo blurred + darkened.
  // A CTA slide is exempt — its photo is a deliberate choice and stays sharp.
  const coverBlurActive = (slide.coverBlurMode === true || options.coverBlurMode === true) && slide.isCtaSlide !== true;

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
  // Robust against **double stars** (markdown paste) and stray unpaired stars:
  // no '*' can ever reach the rendered output.
  const parseAccent = (text) => {
    const raw = (text || '').replace(/\*{2,}/g, '*');
    const parts = raw.split(/(\*[^*]+\*)/g).filter((s) => s !== '');
    const segments = parts.map((seg) => {
      const isAccent = seg.startsWith('*') && seg.endsWith('*') && seg.length > 2;
      // Strip any leftover stray stars from non-accent segments too.
      return { text: (isAccent ? seg.slice(1, -1) : seg).replace(/\*/g, ''), accent: isAccent };
    });
    return { plain: segments.map((s) => s.text).join(''), segments };
  };

  // Split text into an editorial structure WITHOUT any markup: short framing
  // lines become small spaced uppercase (sans), the main statement becomes the
  // big serif headline. Mirrors the magazine editorial look where the user just
  // types normally. Returns { kicker, headline, footer }.
  const splitEditorial = (text) => {
    // Always returns three STRINGS — never undefined, so downstream Textbox
    // calls can't crash on .length.
    const safe = (v) => (typeof v === 'string' ? v : '');
    const lines = safe(text).replace(/\*/g, '').split('\n').map((l) => l.trim()).filter(Boolean);
    if (lines.length === 0) return { kicker: '', headline: '', footer: '' };

    // Any straight or typographic quote mark signals a quoted core statement.
    const hasQuote = (s) => /["'\u201C\u201D\u201E\u2033\u00BB\u00AB]/.test(s);
    // A line is "framing" if it's short OR all-caps (kicker/footer style).
    const isFrame = (s) => s.length < 28 || (s === s.toUpperCase() && s.length < 45);

    if (lines.length === 1) {
      // No manual line breaks: structure the paragraph AUTOMATICALLY.
      // The FIRST sentence is the hook and becomes the serif headline; the
      // rest follows below as small CAPS. That matches how hooks are written:
      // the point comes first, the elaboration after.
      const parts = (lines[0].match(/[^.!?…]+[.!?…]+["'\u201D\u2033\u00AB]?|\S[^.!?…]*$/g) || [lines[0]])
        .map((t) => t.trim()).filter(Boolean);
      if (parts.length === 1) return { kicker: '', headline: parts[0], footer: '' };

      // A short opener ("Kennst du das?") is a lead-in, not the hook: in that
      // case it becomes the CAPS line above and the next sentence the headline.
      let hi = 0;
      if (parts[0].length < 18 && parts.length > 1) hi = 1;

      // Hooks are often two short sentences ("Über dreißig Angebote. Fast immer
      // derselbe Fehler."). Keep them together in the headline while it stays
      // comfortably short.
      let headline = parts[hi];
      let next = hi + 1;
      while (next < parts.length && headline.length < 45 && parts[next].length < 40) {
        headline = `${headline} ${parts[next]}`;
        next++;
        if (headline.length >= 60) break;
      }

      const kicker = parts.slice(0, hi).join(' ');
      const footer = parts.slice(next).join(' ');
      return { kicker, headline, footer };
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
  const textShadow = hasBgImage ? 'rgba(0,0,0,0.35) 0px 1px 6px' : '';

  // === ADS: PIN LIST (photo + hook pill + checkmark bullets + CTA button) ===
  if (layout === 'ad_pins') {
    const accent = slide.accentColor || '#7C2D2D';
    const dark = '#1F1B16';
    const pillBg = 'rgba(255,252,248,0.96)';

    // --- COHERENT FLOW: bottom zone first (CTA + promise), then hook from the
    // top, then bullets ONLY into the space that remains. Nothing can overlap.

    // 1) CTA button, anchored at the bottom.
    let bottomLimit = height * 0.94;
    if (slide.cta) {
      const ctaText = new fabric.Text(String(slide.cta), {
        left: width / 2, top: height * 0.885, originX: 'center', originY: 'center',
        fontSize: fs(15), fill: hexLuminance(accent) < 140 ? '#FFFFFF' : '#1F1B16',
        fontFamily: 'Montserrat', fontWeight: '700',
      });
      const padX = fs(16), padY = fs(9);
      const btn = new fabric.Rect({
        left: width / 2, top: height * 0.885, originX: 'center', originY: 'center',
        width: (ctaText.width || fs(120)) + padX * 2, height: (ctaText.height || fs(18)) + padY * 2,
        rx: fs(7), ry: fs(7), fill: accent, selectable: false,
      });
      canvas.add(btn); canvas.add(ctaText);
      bottomLimit = height * 0.885 - (btn.height / 2) - height * 0.025;
    }

    // 2) Promise line sits directly above the CTA.
    if (slide.promise) {
      const pr = new fabric.Textbox(String(slide.promise), {
        left: width / 2, top: bottomLimit, originX: 'center', originY: 'bottom',
        width: width * 0.82, fontSize: fs(15), fill: dark,
        fontFamily: 'Montserrat', fontWeight: '700', lineHeight: 1.4,
        textAlign: 'center', textBackgroundColor: pillBg,
      });
      canvas.add(pr);
      bottomLimit -= (pr.getScaledHeight?.() || fs(15) * 2) + height * 0.03;
    }

    // 3) Hook from the top — font adapts to length so it stays a hook,
    // not a novel.
    let y = height * 0.07;
    if (slide.hook) {
      const hookLen = String(slide.hook).length;
      const hookFs = hookLen > 150 ? 15 : hookLen > 100 ? 17 : 19;
      const hookBox = new fabric.Textbox(String(slide.hook), {
        left: width * 0.06, top: y, originX: 'left', originY: 'top',
        width: width * 0.64, fontSize: fs(hookFs), fill: dark,
        fontFamily: 'Montserrat', fontWeight: '700', lineHeight: 1.45,
        textAlign: 'left', textBackgroundColor: pillBg,
      });
      canvas.add(hookBox);
      y += (hookBox.getScaledHeight?.() || fs(hookFs) * 3) + height * 0.05;
    }

    // 4) Bullets fill ONLY the space between hook and promise. Anything that
    // would collide is skipped instead of drawn over other elements.
    const bullets = Array.isArray(slide.bullets) ? slide.bullets.filter(Boolean).slice(0, 3) : [];
    y = Math.max(y, height * 0.42);
    for (const b of bullets) {
      const bx = new fabric.Textbox(`✅ ${b}`, {
        left: width * 0.06, top: y, originX: 'left', originY: 'top',
        width: width * 0.58, fontSize: fs(15), fill: dark,
        fontFamily: 'Montserrat', fontWeight: '600', lineHeight: 1.4,
        textAlign: 'left', textBackgroundColor: pillBg,
      });
      const bh = bx.getScaledHeight?.() || fs(15) * 2;
      if (y + bh > bottomLimit - height * 0.02) break; // no space left — skip, never overlap
      canvas.add(bx);
      y += bh + height * 0.03;
    }

    canvas.renderAll();
    return;
  }

  // === ADS: COLLAGE (ransom-note words on paper strips + handwritten circle) ===
  if (layout === 'ad_collage') {
    const ink = '#1F1B16';
    const tones = ['rgba(247,241,230,0.97)', 'rgba(246,229,178,0.97)', 'rgba(255,255,255,0.97)'];
    const words = String(slide.statement || '').split(/\s+/).filter(Boolean);

    if (words.length) {
      const fSize = fs(words.length > 24 ? 19 : words.length > 15 ? 23 : 27);
      const spaceW = fSize * 0.35;
      const maxW = width * 0.82;
      // Build word objects (each its own paper strip, deterministic tilt).
      const objs = words.map((w, i) => new fabric.Text(` ${w} `, {
        fontSize: fSize, fontFamily: 'Montserrat', fontWeight: '800',
        fill: ink, textBackgroundColor: tones[i % tones.length],
        angle: ((i * 37) % 5) - 2, // -2..+2 degrees, stable per word
        originX: 'left', originY: 'top', selectable: false,
      }));
      // Wrap into lines by measured widths.
      const lines = [[]];
      let lw = 0;
      for (const o of objs) {
        const w0 = o.width || fSize * 3;
        if (lw + w0 > maxW && lines[lines.length - 1].length) { lines.push([]); lw = 0; }
        lines[lines.length - 1].push(o); lw += w0 + spaceW;
      }
      const lineH = fSize * 1.65;
      const blockH = lines.length * lineH;
      let ly = Math.max(height * 0.10, height * 0.42 - blockH / 2);
      for (const line of lines) {
        const lineW = line.reduce((a, o) => a + (o.width || 0), 0) + spaceW * (line.length - 1);
        let lx = (width - lineW) / 2;
        for (const o of line) {
          o.set({ left: lx, top: ly });
          canvas.add(o);
          lx += (o.width || 0) + spaceW;
        }
        ly += lineH;
      }
    }

    if (slide.ctaLine) {
      const ct = new fabric.Text(String(slide.ctaLine), {
        left: width / 2, top: height * 0.80, originX: 'center', originY: 'center',
        fontSize: fs(30), fill: '#FFFFFF', fontFamily: 'Caveat', fontWeight: '600',
        shadow: 'rgba(0,0,0,0.55) 0px 2px 10px', selectable: false,
      });
      const ell = new fabric.Ellipse({
        left: width / 2, top: height * 0.80, originX: 'center', originY: 'center',
        rx: (ct.width || fs(180)) / 2 + fs(16), ry: (ct.height || fs(30)) / 2 + fs(12),
        fill: '', stroke: '#FFFFFF', strokeWidth: 2.5 * scale,
        shadow: 'rgba(0,0,0,0.4) 0px 1px 6px', selectable: false,
      });
      canvas.add(ell); canvas.add(ct);
    }
    canvas.renderAll();
    return;
  }

  // === ADS: STATEMENT (paper-strip statement + circled handwriting CTA) ===
  if (layout === 'ad_statement') {
    const accent = slide.accentColor || '#B0402F';
    const bgFill = slide.backgroundColor || accent;
    canvas.add(new fabric.Rect({ left: 0, top: 0, width, height, fill: bgFill, selectable: false }));
    // Contrast-aware ink for the circled line + brand mark on light backgrounds.
    const inkLight = hexLuminance(bgFill) < 140;
    const ink = inkLight ? '#FFFFFF' : '#2A2118';
    const inkDim = inkLight ? 'rgba(255,255,255,0.85)' : 'rgba(42,33,24,0.75)';

    if (slide.statement) {
      const st = new fabric.Textbox(String(slide.statement), {
        left: width / 2, top: height * 0.40, originX: 'center', originY: 'center',
        width: width * 0.78, fontSize: fs(26), fill: '#1F1B16',
        fontFamily: 'Montserrat', fontWeight: '700', lineHeight: 1.5,
        textAlign: 'center', textBackgroundColor: 'rgba(247,241,230,0.96)',
      });
      canvas.add(st);
    }

    if (slide.ctaLine) {
      const ct = new fabric.Text(String(slide.ctaLine), {
        left: width / 2, top: height * 0.74, originX: 'center', originY: 'center',
        fontSize: fs(24), fill: ink, fontFamily: 'Playfair Display',
        fontStyle: 'italic', fontWeight: '500',
      });
      const ell = new fabric.Ellipse({
        left: width / 2, top: height * 0.74, originX: 'center', originY: 'center',
        rx: (ct.width || fs(180)) / 2 + fs(18), ry: (ct.height || fs(28)) / 2 + fs(14),
        fill: '', stroke: ink, strokeWidth: 2.5 * scale, selectable: false,
      });
      canvas.add(ell); canvas.add(ct);
    }

    if (options.globalBrandName) {
      canvas.add(new fabric.Text(options.globalBrandName.toUpperCase(), {
        left: width / 2, top: height * 0.94, originX: 'center', originY: 'bottom',
        fontSize: fs(11), fill: inkDim, fontFamily: 'Montserrat',
        charSpacing: 200, selectable: false,
      }));
    }
    canvas.renderAll();
    return;
  }


  // === COVER WITH PHOTO: auto-place title in the image's quiet zone ===
  // When a background photo is present, ignore the abstract layout and place
  // the title where the image has free/quiet space (from image analysis).
  // === MAGAZINE STYLE COVER (editorial photo cover) ===
  // Rich cover: photo bg + small label chip (top) + serif title with one
  // italic/script accent word + subtitle + small brand mark (bottom).
  if (hasBgImage && (layout === 'magazine_cover' || layout === 'sarah_cover' || slide.coverStyle === 'sarah')) {
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
      shadow: 'rgba(0,0,0,0.3) 0px 1px 5px',
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
  if (hasBgImage && !specialImageLayouts.includes(layout) && !slide.editorialDark) {
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
      shadow: slide.noShadow ? '' : 'rgba(0,0,0,0.3) 0px 1px 5px',
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
      // Light readability wash at the bottom if there's a photo — soft fade.
      if (hasBgImage) {
        const swTop = height * 0.58; const swH = height * 0.42;
        canvas.add(new fabric.Rect({
          left: 0, top: swTop, width, height: swH,
          fill: new fabric.Gradient({
            type: 'linear', coords: { x1: 0, y1: 0, x2: 0, y2: swH },
            colorStops: [
              { offset: 0, color: 'rgba(0,0,0,0)' },
              { offset: 1, color: 'rgba(0,0,0,0.45)' },
            ],
          }),
          selectable: false,
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
        shadow: hasBgImage ? 'rgba(0,0,0,0.3) 0px 1px 5px' : '',
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
    // Text-only posts: ALWAYS the same centered level (no jumping between
    // posts). Position rotation only applies when there's a photo to respect.
    const row = hasBgImage ? (anchor.row || 'mid') : 'mid';
    const col = hasBgImage ? (anchor.col || 'center') : 'center';

    // Editorial Dark: heavy washes are handled INSIDE the editorial branch
    // (light global tone + local scrim only), so the subject stays visible.
    if (hasBgImage && slide.darkPhoto && !slide.editorialDark) {
      canvas.add(new fabric.Rect({
        left: 0, top: 0, width, height,
        fill: 'rgba(20,14,9,0.45)', selectable: false,
      }));
    }

    // On photos, add a soft readability gradient on the half where the text sits.
    if (hasBgImage && !slide.editorialDark) {
      const bandTop = row === 'top' ? 0 : row === 'bottom' ? height * 0.5 : height * 0.28;
      const bandH = row === 'mid' ? height * 0.44 : height * 0.5;
      const stops = row === 'top'
        ? [{ offset: 0, color: 'rgba(0,0,0,0.48)' }, { offset: 1, color: 'rgba(0,0,0,0)' }]
        : row === 'bottom'
          ? [{ offset: 0, color: 'rgba(0,0,0,0)' }, { offset: 1, color: 'rgba(0,0,0,0.48)' }]
          : [{ offset: 0, color: 'rgba(0,0,0,0)' }, { offset: 0.5, color: 'rgba(0,0,0,0.44)' }, { offset: 1, color: 'rgba(0,0,0,0)' }];
      canvas.add(new fabric.Rect({
        left: 0, top: bandTop, width, height: bandH,
        fill: new fabric.Gradient({ type: 'linear', coords: { x1: 0, y1: 0, x2: 0, y2: bandH }, colorStops: stops }),
        selectable: false,
      }));
    }

    // (Kicker label removed — frame lines come from the user's own text.)

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
      const _split = splitEditorial(slide.text);
      const kickTxt = typeof _split.kicker === 'string' ? _split.kicker : '';
      const headline = typeof _split.headline === 'string' ? _split.headline : '';
      const footer = typeof _split.footer === 'string' ? _split.footer : '';
      // Nothing to draw — bail out instead of feeding undefined into fabric.
      if (!kickTxt && !headline && !footer) { canvas.renderAll(); return; }
      const centerX = width / 2;
      // Per-slide switch: ON (default) = first sentence as serif headline.
      // OFF = the whole text renders as small spaced CAPS, no serif headline.
      const serifOn = slide.serifHeadline !== false;
      // Brightness-aware: if the text zone is BRIGHT, use dark text on a light
      // scrim (dunkel auf hell); if dark, white text on a dark scrim.
      const zb = typeof slide.smartTextBright === 'number'
        ? slide.smartTextBright
        : (slide._autoImage?.zoneBrightness?.[slide._autoImage?.quietZone]);
      const brightZone = hasBgImage && typeof zb === 'number' && zb > 150;
      const lightText = hasBgImage ? (brightZone ? '#1A1310' : '#FFFFFF') : contrastColor(slide.backgroundColor || '#fff');
      // Frame lines + brand mark: never trust the slide's accent blindly — if
      // it has too little contrast to the background (beige on beige), fall
      // back to the guaranteed-readable text color.
      let dimBase = accentColor;
      if (!hasBgImage) {
        const bgLum = hexLuminance(slide.backgroundColor || '#FFFFFF');
        if (Math.abs(hexLuminance(accentColor) - bgLum) < 60) {
          dimBase = contrastColor(slide.backgroundColor || '#fff');
        }
      }
      const dimText = hasBgImage ? (brightZone ? 'rgba(26,19,16,0.85)' : 'rgba(255,255,255,0.9)') : dimBase;
      const sh = hasBgImage && !brightZone ? 'rgba(0,0,0,0.55) 0px 2px 12px' : '';
      const scrimRGB = brightZone ? '245,240,232' : '8,6,4';

      // Place the text stack in the photo's QUIET zone (from image analysis)
      // so it never covers the subject/face. Fall back to the anchor row.
      let stackTop;
      let bandTop, bandH;
      if (hasBgImage) {
        const zone = (slide._autoImage && slide._autoImage.quietZone) || '';
        if (zone.includes('top')) { stackTop = height * 0.10; }
        else if (zone.includes('bottom')) { stackTop = height * 0.56; }
        else if (zone) { stackTop = height * 0.32; }
        else { stackTop = height * 0.56; } // default: lower area, faces are usually upper
        // Only a LIGHT global tone so the whole photo (incl. face) stays visible.
        // The local scrim is drawn AFTER the text is positioned, so it always
        // sits exactly behind the text — never where the text used to be.
        if (slide.darkPhoto) {
          canvas.add(new fabric.Rect({
            left: 0, top: 0, width, height,
            fill: 'rgba(20,14,9,0.18)', selectable: false,
          }));
        }
      }

      // Build all three layers FIRST (unpositioned), measure them, then place
      // the whole group. Text-only posts are ALWAYS vertically centered at the
      // same level — no jumping between posts. Photo posts keep the quiet zone.
      const GAP_K = height * 0.045;
      const GAP_H = height * 0.04;
      let kObj = null, fObj = null;

      // CAPS-ONLY MODE: one calm block of spaced uppercase, no serif headline.
      if (!serifOn) {
        const all = [kickTxt, headline, footer].filter(Boolean).join(' ');
        const capsOnly = new fabric.Textbox(all.toUpperCase(), {
          left: centerX, top: 0, originX: 'center', originY: 'top',
          width: width * 0.82, fontSize: fs(20), fill: lightText,
          fontFamily: 'Montserrat', fontWeight: '500', charSpacing: 160,
          textAlign: 'center', lineHeight: 1.55, shadow: sh,
        });
        const SAFE_TOP_C = height * 0.07;
        const SAFE_BOTTOM_C = height * 0.80;
        const availC = SAFE_BOTTOM_C - SAFE_TOP_C;
        let g2 = 0;
        while (g2 < 60 && (capsOnly.height || 0) > availC && capsOnly.fontSize > 10) {
          capsOnly.set('fontSize', capsOnly.fontSize - 1);
          if (capsOnly.initDimensions) capsOnly.initDimensions();
          g2++;
        }
        const cH = capsOnly.height || fs(20) * 3;
        // Same fixed centered position as the serif mode: block midpoint at 55%.
        let cTop = height * 0.55 - cH / 2;
        cTop = Math.min(Math.max(cTop, height * 0.06), height * 0.90 - cH);
        if (hasBgImage) {
          const padC = height * 0.06;
          const sT = Math.max(0, cTop - padC);
          const sHgt = Math.min(height - sT, cH + padC * 2);
          canvas.add(new fabric.Rect({
            left: 0, top: sT, width, height: sHgt,
            fill: new fabric.Gradient({
              type: 'linear', coords: { x1: 0, y1: 0, x2: 0, y2: sHgt },
              colorStops: [
                { offset: 0, color: `rgba(${scrimRGB},0)` },
                { offset: 0.18, color: `rgba(${scrimRGB},0.32)` },
                { offset: 0.82, color: `rgba(${scrimRGB},0.32)` },
                { offset: 1, color: `rgba(${scrimRGB},0)` },
              ],
            }),
            selectable: false,
          }));
        }
        capsOnly.set({ top: cTop });
        canvas.add(capsOnly);
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

      if (kickTxt) {
        kObj = new fabric.Textbox(kickTxt.toUpperCase(), {
          left: centerX, top: 0, originX: 'center', originY: 'top',
          width: width * 0.8, fontSize: fs(15), fill: dimText,
          fontFamily: 'Montserrat', fontWeight: '500', charSpacing: 200,
          textAlign: 'center', lineHeight: 1.3, shadow: sh,
        });
      }
      const h = new fabric.Textbox(headline, {
        left: centerX, top: 0, originX: 'center', originY: 'top',
        width: width * 0.86, fontSize: fs(slide.fontSize || 54),
        fill: lightText, fontFamily: 'Playfair Display', fontWeight: '500',
        textAlign: 'center', lineHeight: 1.08, shadow: sh,
      });
      // Hard cap by text length BEFORE measuring — this is the reliable guard.
      // Font metrics can be wrong on first paint (font still loading), so we
      // never rely on measurement alone. These caps are tuned so the worst-case
      // wrap always fits the 4:5 safe area with the CAPS frame lines present.
      const charCount = headline.length + (kickTxt ? kickTxt.length * 0.5 : 0) + (footer ? footer.length * 0.5 : 0);
      const capRaw = charCount > 140 ? 26
        : charCount > 110 ? 30
        : charCount > 85 ? 36
        : charCount > 60 ? 42
        : charCount > 40 ? 48
        : 54;
      // Per-slide switch: bigHeadline scales the serif headline up ~35% for
      // the large magazine-cover look. The length tiers scale with it, so
      // long texts grow controlled rather than exploding.
      const capBase = slide.bigHeadline === true ? Math.round(capRaw * 1.35) : capRaw;
      h.set('fontSize', fs(capBase));
      if (h.initDimensions) h.initDimensions();
      if (footer) {
        fObj = new fabric.Textbox(footer.toUpperCase(), {
          left: centerX, top: 0, originX: 'center', originY: 'top',
          width: width * 0.8, fontSize: fs(15), fill: dimText,
          fontFamily: 'Montserrat', fontWeight: '500', charSpacing: 150,
          textAlign: 'center', lineHeight: 1.3, shadow: sh,
        });
      }
      const mh = (o, fallback) => (o ? ((typeof o.getScaledHeight === 'function' ? o.getScaledHeight() : o.height) || fallback) : 0);

      // FIXED POSITION, centered: the block's MIDPOINT sits at a fixed height
      // (slightly below the geometric middle for an editorial feel). Same
      // position on every slide; short and long texts share the same center.
      const CENTER_Y = height * 0.55;

      const GAP_K2 = height * 0.03;
      const GAP_H2 = height * 0.025;
      const hK = kObj ? mh(kObj, fs(15) * 1.8) : 0;
      const hH2 = mh(h, fs(capBase) * 2.4);
      const hF = fObj ? mh(fObj, fs(15) * 1.8) : 0;
      const blockH = hK + (kObj ? GAP_K2 : 0) + hH2 + (fObj ? GAP_H2 : 0) + hF;

      let cursor = CENTER_Y - blockH / 2;
      // Keep the block clear of the very top and of the brand line at 93%.
      cursor = Math.min(Math.max(cursor, height * 0.06), height * 0.90 - blockH);

      // Soft scrim behind the block for readability (skip on already-dark blur).
      const isBlurFollowUp = coverBlurActive && (options.slideIndex || 0) > 0;
      if (hasBgImage && !isBlurFollowUp) {
        const pad = height * 0.05;
        const sTop = Math.max(0, cursor - pad);
        const sH = Math.min(height - sTop, blockH + pad * 2);
        canvas.add(new fabric.Rect({
          left: 0, top: sTop, width, height: sH,
          fill: new fabric.Gradient({
            type: 'linear', coords: { x1: 0, y1: 0, x2: 0, y2: sH },
            colorStops: [
              { offset: 0, color: `rgba(${scrimRGB},0)` },
              { offset: 0.2, color: `rgba(${scrimRGB},0.32)` },
              { offset: 0.8, color: `rgba(${scrimRGB},0.32)` },
              { offset: 1, color: `rgba(${scrimRGB},0)` },
            ],
          }),
          selectable: false,
        }));
      }

      if (kObj) { kObj.set({ top: cursor }); canvas.add(kObj); cursor += hK + GAP_K2; }
      h.set({ top: cursor }); canvas.add(h); cursor += hH2 + GAP_H2;
      if (fObj) { fObj.set({ top: cursor }); canvas.add(fObj); }

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

    const zbStd = typeof slide.smartTextBright === 'number'
      ? slide.smartTextBright
      : (slide._autoImage?.zoneBrightness?.[slide._autoImage?.quietZone]);
    const brightStd = hasBgImage && typeof zbStd === 'number' && zbStd > 150;
    const titleObj = new fabric.Textbox(plain, {
      left, top, originX, originY,
      width: width * 0.82,
      fontSize: fs(slide.fontSize || 42),
      fontFamily,
      fill: hasBgImage ? (brightStd ? '#1A1310' : '#FFFFFF') : contrastColor(slide.backgroundColor || '#fff'),
      textAlign, lineHeight: 1.2,
      fontWeight: slide.fontWeight || 'normal',
      shadow: hasBgImage && !brightStd ? 'rgba(0,0,0,0.3) 0px 1px 5px' : '',
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