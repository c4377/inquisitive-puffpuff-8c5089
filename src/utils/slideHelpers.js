import { brandRuleSets } from '../constants/brandData';

/**
 * Creates a standardized slide object with brand styling.
 * Centralizes logic used in Templates, AI generation, and Manual creation.
 */
export const createSmartSlide = (brandConfig, overrides = {}, index = 0, totalSlides = 1, layoutDef = null) => {
  const brandFont = brandConfig?.typography?.fontFamily || 'Inter';
  const bodyFont = brandConfig?.typography?.bodyFontFamily || 'Montserrat';
  const brandColors = brandConfig?.colors || {
    primary: '#000000',
    background: '#FFFFFF', 
    secondary: '#CCCCCC',
    accent: '#888888'
  };

  // Determine Font Strategy
  // Slide 1 (Title) gets Brand Font, others get Body Font
  const useBrandFont = index === 0;
  const fontFamily = useBrandFont ? brandFont : bodyFont;
  
  // Playfair looks best regular, others might need bold
  const safeWeight = fontFamily.includes('Playfair') ? '400' : (useBrandFont ? '700' : '400');
  
  // Determine Layout
  // If no specific layout provided, default to a smart sequence
  let layout = overrides.layout;
  if (!layout) {
    if (index === 0) layout = layoutDef?.layout || 'minimal_quote'; // Cover
    else if (index === totalSlides - 1) layout = 'glass_layer'; // CTA
    else layout = 'minimal_left_accent'; // Content
  }

  // Determine Font Size
  let fontSize = overrides.fontSize || 42;
  if (!overrides.fontSize) {
      if (layout === 'maximized_bold') fontSize = 64;
      if (layout === 'minimal_quote') fontSize = 48;
      if (layout === 'centered_focus') fontSize = 46;
      if (!useBrandFont) fontSize = 32; // Body text smaller
  }
  
  // Text Align
  let textAlign = overrides.textAlign;
  if (!textAlign) {
      if (!useBrandFont) textAlign = 'left';
  }

  return {
    id: Date.now() + Math.random(),
    text: overrides.text || '',
    layout: layout,
    fontSize: fontSize,
    fontFamily: fontFamily,
    fontWeight: safeWeight,
    textAlign: textAlign,
    color: brandColors.primary,
    backgroundColor: brandColors.background,
    secondaryColor: brandColors.secondary,
    accentColor: brandColors.accent,
    visualElements: brandConfig?.visualElements || [],
    format: '4:5',
    slideNumber: index + 1,
    totalSlides: totalSlides,
    imageScale: 1,
    imageX: 0,
    imageY: 0,
    overlay: layout === 'tweet_card' ? 0.1 : 0.25,
    blur: 0,
    background: overrides.background || null,
    // Merge any other overrides
    ...overrides
  };
};