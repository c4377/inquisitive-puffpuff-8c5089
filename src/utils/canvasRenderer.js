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

  const scale = options.scale || 1;
  const padding = width * 0.08;
  
  // Resolve Style Props (Fallback to defaults if missing in slide)
  const primaryColor = slide.color || '#000000';
  const secondaryColor = slide.secondaryColor || '#666666';
  const accentColor = slide.accentColor || '#000000';
  const fontFamily = slide.fontFamily || 'Inter';
  const accentFont = slide.accentFontFamily || fontFamily;
  
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

  // Helper: Text Processor
  const processText = (text) => text || '';

  // === STRATEGY: LAYOUT ENGINE ===
  const layout = slide.layout || 'centered_focus';

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
        fontSize: 32 * scale,
        fontFamily: accentFont,
        fill: secondaryColor,
        fontStyle: 'italic',
        textAlign: 'left'
      });
      canvas.add(secText);
      currentY += secText.height + (20 * scale);
    }

    // Main Body
    const mainText = new fabric.Textbox(processText(slide.text), {
      left: padding,
      top: currentY,
      width: width - (padding * 2),
      fontSize: (slide.fontSize || 40) * scale,
      fontFamily: fontFamily,
      fill: primaryColor,
      lineHeight: 1.3,
      textAlign: 'left',
      fontWeight: slide.fontWeight || 'normal'
    });
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
      fontSize: (slide.fontSize || 36) * scale,
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
        fontSize: 42 * scale,
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
      fontSize: (slide.fontSize || 38) * scale,
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
                fontSize: 64 * scale,
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
                fontSize: 32 * scale,
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
                fontSize: 32 * scale,
                fontFamily: fontFamily,
                fill: primaryColor
            });
            canvas.add(textObj);
            currentY += textObj.height + (20 * scale);
        }
     });
  }

  // 5. CENTERED FOCUS (Default)
  else {
    const textObj = new fabric.Textbox(processText(slide.text), {
      left: padding,
      top: height / 2,
      originY: 'center',
      width: width - (padding * 2),
      fontSize: (slide.fontSize || 48) * scale,
      fontFamily: fontFamily,
      fill: primaryColor,
      textAlign: slide.textAlign || 'center',
      lineHeight: 1.3
    });
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