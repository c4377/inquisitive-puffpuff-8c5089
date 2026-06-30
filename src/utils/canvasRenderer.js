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
  
  // Clear and setup
  canvas.clear();
  canvas.setBackgroundColor(slide.backgroundColor || '#ffffff', canvas.renderAll.bind(canvas));
  
  // Ensure dimensions
  if (canvas.setWidth) canvas.setWidth(width);
  if (canvas.setHeight) canvas.setHeight(height);

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
          const scaleFactor = Math.max(width / img.width, height / img.height);
          img.set({
            originX: 'center',
            originY: 'center',
            left: width / 2,
            top: height / 2,
            scaleX: scaleFactor,
            scaleY: scaleFactor,
            selectable: false,
          });
          canvas.add(img);
          canvas.sendToBack(img);

          // Readability overlay. Darken toward the text zone so light text reads.
          const ov = typeof slide.overlay === 'number' ? slide.overlay : 0.35;
          const overlayRect = new fabric.Rect({
            left: 0,
            top: 0,
            width,
            height,
            fill: `rgba(0,0,0,${ov})`,
            selectable: false,
          });
          canvas.add(overlayRect);
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
  const hasBgImage = !!slide.background;
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
  if (hasBgImage) {
    await drawBackgroundImage(slide.background);
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
  const layout = slide.layout || 'centered_focus';

  // === COVER WITH PHOTO: auto-place title in the image's quiet zone ===
  // When a background photo is present, ignore the abstract layout and place
  // the title where the image has free/quiet space (from image analysis).
  if (hasBgImage) {
    const zone = slide._autoImage?.quietZone || 'center';
    const { plain, segments } = parseAccent(slide.text);

    // Map a 3x3 zone label to an anchor point + alignment.
    const col = zone.includes('left') ? 'left' : zone.includes('right') ? 'right' : 'center';
    const row = zone.includes('top') ? 'top' : zone.includes('bottom') ? 'bottom' : 'mid';

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
      shadow: new fabric.Shadow({ color: 'rgba(0,0,0,0.45)', blur: 8, offsetX: 0, offsetY: 2 }),
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


  // 1. EDITORIAL CLASSIC (Line + Title + Body)
  if (layout === 'editorial_classic' || layout === 'minimal_editorial') {
    // Top Line
    const line = new fabric.Line([padding, padding, width - padding, padding], {
      stroke: accentColor,
      strokeWidth: 2 * scale,
      selectable: false
    });
    canvas.add(line);

    let currentY = padding + (40 * scale);

    // Optional Secondary Text (Hook)
    if (slide.secondaryText) {
      const secText = new fabric.Textbox(slide.secondaryText, {
        left: padding,
        top: currentY,
        width: width - (padding * 2),
        fontSize: fs(32),
        fontFamily: accentFont,
        fill: secondaryColor,
        fontStyle: 'italic',
        textAlign: 'left'
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
      fill: contrastColor(primaryColor),
      lineHeight: 1.3,
      textAlign: 'left',
      fontWeight: slide.fontWeight || 'normal'
    });
    applyAccentStyles(mainText, ecSegs);
    canvas.add(mainText);
  }

  // 2. PAPER BOX (Shadow Box)
  else if (layout === 'paper_box' || layout === 'story_text_box') {
    const boxMargin = width * 0.12;
    const boxRect = new fabric.Rect({
      left: boxMargin,
      top: boxMargin,
      width: width - (boxMargin * 2),
      height: height - (boxMargin * 2),
      fill: '#ffffff',
      shadow: new fabric.Shadow({ color: 'rgba(0,0,0,0.15)', blur: 20 * scale, offsetX: 0, offsetY: 10 * scale }),
      rx: 10 * scale,
      ry: 10 * scale,
      selectable: false
    });
    canvas.add(boxRect);

    const textObj = new fabric.Textbox(processText(slide.text), {
      left: boxMargin + (40 * scale),
      top: height / 2,
      originY: 'center',
      width: width - (boxMargin * 2) - (80 * scale),
      fontSize: fs(slide.fontSize || 36),
      fontFamily: fontFamily,
      fill: '#1a1a1a', // Force dark on white box
      textAlign: 'center',
      lineHeight: 1.4
    });
    canvas.add(textObj);
  }

  // 3. SPLIT COLOR (Top/Bottom)
  else if (layout === 'split_color') {
    // Top Half (White)
    canvas.add(new fabric.Rect({ left: 0, top: 0, width: width, height: height * 0.4, fill: '#ffffff', selectable: false }));
    // Bottom Half (Accent)
    canvas.add(new fabric.Rect({ left: 0, top: height * 0.4, width: width, height: height * 0.6, fill: accentColor, selectable: false }));

    // Top Text
    if (slide.secondaryText) {
      canvas.add(new fabric.Textbox(slide.secondaryText, {
        left: padding,
        top: (height * 0.4) / 2,
        originY: 'center',
        width: width - (padding * 2),
        fontSize: fs(42),
        fontFamily: accentFont,
        fill: primaryColor,
        textAlign: 'center',
        fontStyle: 'italic'
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
      fill: '#ffffff',
      textAlign: 'center',
      fontWeight: 'bold'
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

  // 5. MINIMAL QUOTE (Cover / Brand preview) — supports *accent* word
  else if (layout === 'minimal_quote' || layout === 'maximized_bold' || layout === 'tweet_card') {
    const mainColor = contrastColor(primaryColor);
    const { plain, segments } = parseAccent(slide.text);

    const textObj = new fabric.Textbox(plain, {
      left: padding,
      top: height / 2,
      originY: 'center',
      width: width - (padding * 2),
      fontSize: fs(slide.fontSize || 44),
      fontFamily: fontFamily,
      fill: mainColor,
      textAlign: slide.textAlign || 'center',
      lineHeight: 1.25,
      fontWeight: slide.fontWeight || 'bold',
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
      fill: contrastColor(primaryColor),
      textAlign: slide.textAlign || 'center',
      lineHeight: 1.3
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

  // Brand Name
  if (options.globalBrandName) {
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

  // Render & Wait
  canvas.renderAll();
  
  // If images (overlay) need loading, we handle them:
  if (slide.visualElements?.length > 0) {
      // Basic support for visual elements if needed
  }
};