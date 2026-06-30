export const communityTopics = [
  { id: 'business', label: 'Business Strategy', icon: 'FiBriefcase' },
  { id: 'mindset', label: 'Identity & Mindset', icon: 'FiUserCheck' },
  { id: 'marketing', label: 'Marketing & Sales', icon: 'FiTrendingUp' },
  { id: 'decisions', label: 'Decision Making', icon: 'FiTarget' }
];

// Helper to create slide object
const createSlide = (brandConfig, overrides = {}) => {
  const brandFont = brandConfig?.typography?.fontFamily || 'Inter';
  // NEW: Ensure Accent Font is passed
  const accentFont = brandConfig?.typography?.accentFontFamily; 
  
  const safeWeight = brandFont.includes('Playfair') ? '400' : '700';

  return {
    id: Date.now() + Math.random(),
    format: '16:9',
    fontSize: 56,
    fontFamily: brandFont,
    accentFontFamily: accentFont, // PASS ACCENT FONT
    fontWeight: safeWeight,
    color: brandConfig?.colors?.primary || '#000000',
    backgroundColor: brandConfig?.colors?.background || '#FFFFFF',
    secondaryColor: brandConfig?.colors?.secondary || '#CCCCCC',
    accentColor: brandConfig?.colors?.accent || '#888888',
    visualElements: brandConfig?.visualElements || [],
    layout: 'minimal_left_accent', // Default layout
    imageScale: 1,
    imageX: 0,
    imageY: 0,
    overlay: 0,
    ...overrides
  };
};

export const generatePresentationDeck = (topic, brandConfig) => {
  const slides = [];
  const bodyFont = brandConfig?.typography?.bodyFontFamily || 'Inter';

  // Slide 1: Title (Centered) - WITH ACCENT HIGHLIGHTS
  slides.push(createSlide(brandConfig, {
    text: topic === 'mindset' ? "IDENTITY\n*SHIFT*" : "BUSINESS\n*MASTERY*",
    secondaryText: "MASTERCLASS WITH " + (brandConfig.name || "MUSE MENTORING"),
    layout: 'centered_focus',
    fontSize: 80,
    textAlign: 'center'
  }));

  // Slide 2: Agenda (Right Aligned per request mixed)
  slides.push(createSlide(brandConfig, {
    text: "*AGENDA*",
    secondaryText: "01. Status Quo\n02. The *Gap*\n03. The Strategy\n04. Execution",
    layout: 'minimal_left_accent',
    fontSize: 56,
    fontFamily: bodyFont,
    textAlign: 'right'
  }));

  // Slide 3: Quote (Center)
  slides.push(createSlide(brandConfig, {
    text: topic === 'mindset' 
      ? "\"You don't get what you want.\nYou get *who you are*.\"" 
      : "\"Revenue is a lagging indicator\nof your *habits*.\"",
    layout: 'minimal_quote',
    fontSize: 48,
    textAlign: 'center'
  }));

  // Slide 4: 3 Pillars (Right)
  slides.push(createSlide(brandConfig, {
    text: "THE 3 *PILLARS*",
    secondaryText: "1. Clarity (*Klarheit*)\n2. Consistency (*Konstanz*)\n3. Conversion (*Abschluss*)",
    layout: 'split_vertical_editorial',
    fontSize: 64,
    textAlign: 'right'
  }));

  // Slide 5: Framework (Center)
  slides.push(createSlide(brandConfig, {
    text: "THE *FRAMEWORK*",
    secondaryText: "[ Hier Grafik/Chart einfügen ]",
    layout: 'accent_frame',
    fontSize: 56,
    textAlign: 'center'
  }));

  // Slide 6: CTA (Right)
  slides.push(createSlide(brandConfig, {
    text: "YOUR *NEXT STEP*",
    secondaryText: "Join the Inner Circle.",
    layout: 'glass_layer',
    fontSize: 72,
    textAlign: 'right'
  }));

  return slides;
};