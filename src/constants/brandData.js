// PREMIUM BRAND DEFINITIONS & LAYOUTS

export const colorGenerators = {
  mono_classic: () => ({ primary: '#000000', secondary: '#57534E', tertiary: '#D6D1CC', accent: '#a8a29e', neutral: '#EBE9E6', background: '#FFFFFF' }),
  pure_noir: () => ({ primary: '#000000', secondary: '#F3F4F6', tertiary: '#1A1A1A', accent: '#000000', neutral: '#E5E5E5', background: '#FFFFFF' }),
  clean_yellow_grey: () => ({ primary: '#1F2937', secondary: '#F3F4F6', tertiary: '#9CA3AF', accent: '#FDE047', neutral: '#FAFAFA', background: '#FFFFFF' }),
  dark_matter: () => ({ primary: '#FFFFFF', secondary: '#1F2937', tertiary: '#374151', accent: '#3B82F6', neutral: '#111827', background: '#030712' }),
  executive_navy: () => ({ primary: '#F8FAFC', secondary: '#1E293B', tertiary: '#334155', accent: '#38BDF8', neutral: '#0F172A', background: '#020617' }),
  old_money: () => ({ primary: '#FDFCF8', secondary: '#1a4731', tertiary: '#166534', accent: '#D4AF37', neutral: '#052e16', background: '#022C22' }),
  stone_concrete: () => ({ primary: '#1C1917', secondary: '#D6D3CD', tertiary: '#A8A29E', accent: '#57534E', neutral: '#F5F5F4', background: '#E7E5E4' }),
  coffee_noir: () => ({ primary: '#FFF8E1', secondary: '#3E2723', tertiary: '#4E342E', accent: '#A1887F', neutral: '#261917', background: '#150F0D' }),
  cherry_bomb: () => ({ primary: '#FFFFFF', secondary: '#7f1d1d', tertiary: '#991b1b', accent: '#EF4444', neutral: '#450a0a', background: '#450a0a' }),
  bold_red: () => ({ primary: '#FFFFFF', secondary: '#000000', tertiary: '#1A1A1A', accent: '#D32F2F', neutral: '#333333', background: '#050505' }),
  warm_beige: () => ({ primary: '#FFFFFF', secondary: '#D4C4B7', tertiary: '#A89F91', accent: '#FCD34D', neutral: '#F5F5DC', background: '#EAE0D5' }),
  dark_luxury: () => ({ primary: '#000000', secondary: '#FFFFFF', tertiary: '#3E2723', accent: '#C0A062', neutral: '#F3E5AB', background: '#1C1917' }),
  cool_spring: () => ({ primary: '#647D82', secondary: '#8D9F79', tertiary: '#B6B4B6', accent: '#D0B400', neutral: '#F5F5F5', background: '#FFFFFF' }),
  sporty_petrol: () => ({ primary: '#FFFFFF', secondary: '#CBD5E1', tertiary: '#000000', accent: '#38BDF8', neutral: '#334155', background: '#0F4C5C' }),
  story_contrast: () => ({ primary: '#FFFFFF', secondary: '#000000', tertiary: '#1A1A1A', accent: '#FF0066', neutral: '#333333', background: '#000000' }),
  soho_lights: () => ({ primary: '#FFFFFF', secondary: '#041C2C', tertiary: '#407E8C', accent: '#FACC15', neutral: '#062A3A', background: '#0B3D59' }),
  electric_violet: () => ({ primary: '#FFFFFF', secondary: '#4C1D95', tertiary: '#8B5CF6', accent: '#C4B5FD', neutral: '#2E1065', background: '#1e1b4b' }),
  desert_sun: () => ({ primary: '#431407', secondary: '#F97316', tertiary: '#FECA9A', accent: '#EA580C', neutral: '#FFF7ED', background: '#FFF7ED' }),
  petrol_editorial: () => ({ primary: '#FFFFFF', secondary: '#003D4C', tertiary: '#002935', accent: '#66D2EA', neutral: '#F1F5F9', background: '#004E64' }),
  warm_business: () => ({ primary: '#2F2F2F', secondary: '#B7A89A', tertiary: '#CFC9C3', accent: '#9FAE9C', neutral: '#CFC9C3', background: '#F6F4F1' }),
  growth_yellow: () => ({ primary: '#1a1a1a', secondary: '#1a1a1a', tertiary: '#ffffff', accent: '#ffffff', neutral: '#fef3c7', background: '#FDE047' }),
  // --- Warm bordeaux / cognac world ---
  bordeaux_luxe: () => ({ primary: '#FBF6EF', secondary: '#7B2D2D', tertiary: '#5A1E1E', accent: '#E8C9A0', neutral: '#3A1414', background: '#5C1F1F' }),
  cognac_editorial: () => ({ primary: '#FBF6EF', secondary: '#8A5A2B', tertiary: '#6B4422', accent: '#D9A86C', neutral: '#3A2817', background: '#6F4A28' }),
  warm_cream_serif: () => ({ primary: '#3A2817', secondary: '#8A5A2B', tertiary: '#B08D5B', accent: '#9A3B2E', neutral: '#F0E6D8', background: '#EFE5D6' }),
};

// UPDATED TYPOGRAPHY GENERATORS: NOW WITH ACCENT FONTS
export const typographyGenerators = {
  editorial_serif: (size = 52) => ({
    fontFamily: 'Playfair Display',
    accentFontFamily: 'Montserrat', // Contrast: Serif -> Sans
    bodyFontFamily: 'Montserrat',
    fontWeight: '400',
    fontSize: size,
    lineHeight: 1.2,
    letterSpacing: '-0.02em',
    fontStyle: 'normal'
  }),
  impact_bold: (size = 64) => ({
    fontFamily: 'Montserrat',
    accentFontFamily: 'Playfair Display', // Contrast: Sans -> Serif Italic
    bodyFontFamily: 'Inter',
    fontWeight: '900',
    fontSize: size,
    lineHeight: 0.95,
    letterSpacing: '-0.05em',
    textTransform: 'uppercase'
  }),
  modern_clean: (size = 42) => ({
    fontFamily: 'Montserrat',
    accentFontFamily: 'Playfair Display', // Contrast: Sans -> Serif Italic
    bodyFontFamily: 'Montserrat',
    fontWeight: '500',
    fontSize: size,
    lineHeight: 1.4,
    letterSpacing: '-0.03em'
  }),
  handwritten_style: (size = 54) => ({
    fontFamily: 'Caveat',
    accentFontFamily: 'Montserrat', // Contrast: Script -> Sans Bold
    bodyFontFamily: 'Montserrat',
    fontWeight: '700',
    fontSize: size,
    lineHeight: 1.2,
    letterSpacing: '0em',
    fontStyle: 'normal'
  }),
  classic_garamond: (size = 48) => ({
    fontFamily: 'Cormorant Garamond',
    accentFontFamily: 'Inter', // Contrast: Serif -> Clean Sans
    bodyFontFamily: 'Inter',
    fontWeight: '500',
    fontSize: size,
    lineHeight: 1.1,
    letterSpacing: '-0.01em',
    fontStyle: 'italic'
  }),
  retro_typewriter: (size = 38) => ({
    fontFamily: 'Courier Prime',
    accentFontFamily: 'Caveat', // Contrast: Mono -> Script
    bodyFontFamily: 'Courier Prime',
    fontWeight: '400',
    fontSize: size,
    lineHeight: 1.5,
    letterSpacing: '-0.01em',
    fontStyle: 'normal'
  }),
  outfit_playfair_mix: (size = 56) => ({
    fontFamily: 'Outfit',
    accentFontFamily: 'Playfair Display', // Explicit Mix
    bodyFontFamily: 'Outfit',
    fontWeight: '800',
    fontSize: size,
    lineHeight: 1.1,
    letterSpacing: '-0.02em',
    fontStyle: 'normal'
  })
};

export const layoutGenerators = {
  glass_layer: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.8, id: 'glass_layer' }),
  tweet_card: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'left', maxTextWidth: w * 0.75, id: 'tweet_card' }),
  keyword_highlight: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.85, id: 'keyword_highlight' }),
  editorial_fade_bottom: (w, h) => ({ textPosition: { x: w / 2, y: h * 0.82 }, textAlign: 'center', maxTextWidth: w * 0.85, id: 'editorial_fade_bottom' }),
  minimal_quote: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.65, id: 'minimal_quote' }),
  maximized_bold: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.85, id: 'maximized_bold' }),
  minimal_left_accent: (w, h) => ({ textPosition: { x: w * 0.15, y: h * 0.6 }, textAlign: 'left', maxTextWidth: w * 0.70, id: 'minimal_left_accent' }),
  split_vertical_editorial: (w, h) => ({ textPosition: { x: w * 0.5, y: h * 0.75 }, textAlign: 'center', maxTextWidth: w * 0.80, id: 'split_vertical_editorial' }),
  centered_focus: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.80, id: 'centered_focus' }),
  editorial_mask: (w, h) => ({ textPosition: { x: w * 0.5, y: h * 0.5 }, textAlign: 'center', maxTextWidth: w * 0.60, id: 'editorial_mask' }),
  bold_number_list: (w, h) => ({ textPosition: { x: w * 0.25, y: h * 0.5 }, textAlign: 'left', maxTextWidth: w * 0.65, id: 'bold_number_list' }),
  accent_frame: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.7, id: 'accent_frame' }),
  diagonal_overlay: (w, h) => ({ textPosition: { x: w * 0.5, y: h * 0.8 }, textAlign: 'center', maxTextWidth: w * 0.8, id: 'diagonal_overlay' }),
  aesthetic_checklist: (w, h) => ({ textPosition: { x: w * 0.15, y: h * 0.5 }, textAlign: 'left', maxTextWidth: w * 0.70, id: 'aesthetic_checklist' }),
  story_top_left: (w, h) => ({ textPosition: { x: w * 0.1, y: h * 0.15 }, textAlign: 'left', maxTextWidth: w * 0.75, id: 'story_top_left' }),
  story_bottom_right: (w, h) => ({ textPosition: { x: w * 0.9, y: h * 0.85 }, textAlign: 'right', maxTextWidth: w * 0.75, id: 'story_bottom_right' }),
  story_text_box: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.80, id: 'story_text_box' }),
  badge_centered: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 + (h * 0.05) }, textAlign: 'center', maxTextWidth: w * 0.85, id: 'badge_centered' }),
  // --- Cover layouts (photo background, magazine style) ---
  magazine_cover: (w, h) => ({ textPosition: { x: w * 0.08, y: h * 0.72 }, textAlign: 'left', maxTextWidth: w * 0.84, id: 'magazine_cover' }),
  cover_top_left: (w, h) => ({ textPosition: { x: w * 0.08, y: h * 0.12 }, textAlign: 'left', maxTextWidth: w * 0.78, id: 'cover_top_left' }),
  cover_bottom_left: (w, h) => ({ textPosition: { x: w * 0.08, y: h * 0.88 }, textAlign: 'left', maxTextWidth: w * 0.78, id: 'cover_bottom_left' }),
  cover_bottom_center: (w, h) => ({ textPosition: { x: w / 2, y: h * 0.85 }, textAlign: 'center', maxTextWidth: w * 0.82, id: 'cover_bottom_center' }),
  cover_center_hero: (w, h) => ({ textPosition: { x: w / 2, y: h / 2 }, textAlign: 'center', maxTextWidth: w * 0.80, id: 'cover_center_hero' }),
  cover_top_center: (w, h) => ({ textPosition: { x: w / 2, y: h * 0.14 }, textAlign: 'center', maxTextWidth: w * 0.82, id: 'cover_top_center' }),
};

export const brandRuleSets = {
  cleanCreator: {
    name: "Clean Creator",
    description: 'Ultra Clean Grey/White with Yellow Pop.',
    colorStrategy: 'clean_yellow_grey',
    vibe: 'clean_tech',
    layoutRules: ['minimal_quote', 'badge_centered', 'split_vertical_editorial', 'aesthetic_checklist'],
    typographyRules: ['outfit_playfair_mix'],
    tags: ['clean', 'yellow', 'grey', 'modern']
  },
  yellowCreator: {
    name: "Yellow Creator",
    description: 'Vibrant Yellow & Black. The Growth Strategy Look.',
    colorStrategy: 'growth_yellow',
    vibe: 'bold_pop',
    layoutRules: ['badge_centered', 'maximized_bold', 'centered_focus'],
    typographyRules: ['modern_clean'],
    tags: ['yellow', 'growth', 'bold']
  },
  warmBusiness: {
    name: "Warm Business",
    description: 'Clear, Warm, Feminine & Professional.',
    colorStrategy: 'warm_business',
    vibe: 'soft_warm',
    layoutRules: ['minimal_quote', 'aesthetic_checklist', 'centered_focus', 'editorial_mask'],
    typographyRules: ['modern_clean'],
    tags: ['warm', 'business', 'feminine']
  },
  boldRedCreator: {
    name: "High Ticket Editorial",
    description: 'Vogue Style. Black, White & Red Accent.',
    colorStrategy: 'bold_red',
    vibe: 'luxury_dark',
    layoutRules: ['maximized_bold', 'editorial_mask', 'minimal_quote'],
    typographyRules: ['editorial_serif'],
    tags: ['bold', 'red', 'editorial']
  },
  warmAuthentic: {
    name: "Authentic Warmth",
    description: 'Warm Beige & Gold. Playful & Personal.',
    colorStrategy: 'warm_beige',
    vibe: 'soft_warm',
    layoutRules: ['story_text_box', 'glass_layer', 'tweet_card'],
    typographyRules: ['modern_clean'],
    tags: ['warm', 'authentic', 'beige']
  },
  luxuryDark: {
    name: "Luxury Matchmaker",
    description: 'Elegant Dark & Cream. White Text Boxes.',
    colorStrategy: 'dark_luxury',
    vibe: 'luxury_dark',
    layoutRules: ['minimal_quote', 'story_text_box', 'editorial_fade_bottom'],
    typographyRules: ['editorial_serif'],
    tags: ['luxury', 'elegant', 'dark']
  },
  petrolEditorial: {
    name: "Petrol Editorial",
    description: 'Deep Petrol & White. Playfair & Montserrat.',
    colorStrategy: 'petrol_editorial',
    vibe: 'luxury_dark',
    layoutRules: ['editorial_fade_bottom', 'minimal_quote', 'split_vertical_editorial', 'editorial_mask'],
    typographyRules: ['editorial_serif'],
    tags: ['petrol', 'editorial', 'classy']
  },
  bloomingSpring: {
    name: "Blooming Spring",
    description: 'Glass, Blur & Fresh Colors.',
    colorStrategy: 'cool_spring',
    vibe: 'fresh_light',
    layoutRules: ['tweet_card', 'glass_layer', 'centered_focus'],
    typographyRules: ['editorial_serif'],
    tags: ['fresh', 'glass', 'nature']
  },
  healthMindset: {
    name: "Health & Mindset",
    description: 'Petrol, Grey & White. Sporty & Clear.',
    colorStrategy: 'sporty_petrol',
    vibe: 'clean_tech',
    layoutRules: ['split_vertical_editorial', 'minimal_left_accent', 'maximized_bold'],
    typographyRules: ['modern_clean'],
    tags: ['sport', 'health', 'business']
  },
  monoEditorial: {
    name: "Mono Editorial",
    description: 'Clean & Authoritative Monochrome.',
    colorStrategy: 'mono_classic',
    vibe: 'minimal_editorial',
    layoutRules: ['minimal_quote', 'split_vertical_editorial', 'editorial_mask'],
    typographyRules: ['editorial_serif'],
    tags: ['leadership', 'mono', 'clean']
  },
  storyFocus: {
    name: "Story Focus",
    description: 'Instagram Typewriter Style. Black Box & Pink.',
    colorStrategy: 'story_contrast',
    vibe: 'bold_pop',
    layoutRules: ['story_text_box'],
    typographyRules: ['retro_typewriter'],
    tags: ['story', 'personal', 'typewriter']
  },
  sohoLuxury: {
    name: "Soho Luxury",
    description: 'Dark Petrol & Gold. Timeless.',
    colorStrategy: 'soho_lights',
    vibe: 'luxury_dark',
    layoutRules: ['minimal_quote', 'accent_frame', 'editorial_mask'],
    typographyRules: ['editorial_serif'],
    tags: ['luxury', 'elegant', 'navy']
  },
  theEssential: {
    name: "The Essential",
    description: 'Clean White & Black. Playfair.',
    colorStrategy: 'pure_noir',
    vibe: 'minimal_editorial',
    layoutRules: ['minimal_quote', 'editorial_mask'],
    typographyRules: ['editorial_serif'],
    tags: ['clean', 'minimal']
  },
  darkMatter: {
    name: "Dark Matter",
    description: 'Matte Black & White. Montserrat.',
    colorStrategy: 'dark_matter',
    vibe: 'luxury_dark',
    layoutRules: ['maximized_bold', 'minimal_left_accent'],
    typographyRules: ['modern_clean'],
    tags: ['dark', 'luxury']
  },
  navyExecutive: {
    name: "Navy Executive",
    description: 'Deep Navy & Silver. Playfair.',
    colorStrategy: 'executive_navy',
    vibe: 'clean_tech',
    layoutRules: ['split_vertical_editorial'],
    typographyRules: ['editorial_serif'],
    tags: ['business', 'trust']
  },
  theStoic: {
    name: "The Stoic",
    description: 'Stone Grey & White. Montserrat.',
    colorStrategy: 'stone_concrete',
    vibe: 'soft_warm',
    layoutRules: ['minimal_quote', 'centered_focus'],
    typographyRules: ['modern_clean'],
    tags: ['calm', 'grey']
  },
  boldEditorial: {
    name: "Bold Editorial",
    description: 'High Contrast. HUGE Montserrat.',
    colorStrategy: 'pure_noir',
    vibe: 'bold_pop',
    layoutRules: ['maximized_bold', 'bold_number_list'],
    typographyRules: ['impact_bold'],
    tags: ['bold', 'fashion']
  },
  oldMoney: {
    name: "Old Money",
    description: 'Forest Green & Gold. Playfair.',
    colorStrategy: 'old_money',
    vibe: 'luxury_dark',
    layoutRules: ['editorial_mask'],
    typographyRules: ['editorial_serif'],
    tags: ['rich', 'classy']
  },
  coffeeNoir: {
    name: "Coffee Noir",
    description: 'Espresso & Cream. Montserrat.',
    colorStrategy: 'coffee_noir',
    vibe: 'soft_warm',
    layoutRules: ['minimal_left_accent'],
    typographyRules: ['modern_clean'],
    tags: ['warm', 'aesthetic']
  },
  cherryBomb: {
    name: "Cherry Bomb",
    description: 'Deep Red & White. Montserrat.',
    colorStrategy: 'cherry_bomb',
    vibe: 'bold_pop',
    layoutRules: ['maximized_bold'],
    typographyRules: ['impact_bold'],
    tags: ['bold', 'red']
  },
  bordeauxLuxe: {
    name: "Bordeaux Luxe",
    description: 'Editorial Bordeaux with cream serif & cognac accent.',
    colorStrategy: 'bordeaux_luxe',
    vibe: 'luxury_warm',
    layoutRules: ['magazine_cover', 'cover_top_left', 'cover_bottom_left', 'cover_center_hero', 'minimal_quote'],
    typographyRules: ['editorial_serif'],
    tags: ['bordeaux', 'editorial', 'luxury', 'warm']
  },
  cognacStudio: {
    name: "Cognac Studio",
    description: 'Warm cognac tones, photo covers, elegant serif mix.',
    colorStrategy: 'cognac_editorial',
    vibe: 'luxury_warm',
    layoutRules: ['cover_bottom_left', 'cover_top_left', 'cover_bottom_center', 'editorial_classic'],
    typographyRules: ['classic_garamond'],
    tags: ['cognac', 'warm', 'editorial']
  },
  warmCreamSerif: {
    name: "Warm Cream Editorial",
    description: 'Cream background, espresso serif, terracotta accent.',
    colorStrategy: 'warm_cream_serif',
    vibe: 'soft_warm',
    layoutRules: ['cover_center_hero', 'cover_top_center', 'minimal_quote', 'editorial_classic'],
    typographyRules: ['editorial_serif'],
    tags: ['cream', 'warm', 'editorial', 'soft']
  },
};

export const getRandomVisualElements = (ruleSetKey) => {
  return [];
};

const getRandomKey = (obj) => {
  const keys = Object.keys(obj);
  return keys[Math.floor(Math.random() * keys.length)];
};

const generateRandomName = () => {
  const prefixes = ["Nova", "Luma", "Vertex", "Aura", "Zenith", "Flux", "Echo", "Prisma", "Arc", "Solo", "Mio"];
  const suffixes = ["Studio", "Lab", "Co.", "Brand", "Vision", "Space", "Collective", "Club", "Society"];
  const p = prefixes[Math.floor(Math.random() * prefixes.length)];
  const s = suffixes[Math.floor(Math.random() * suffixes.length)];
  return `${p} ${s}`;
};

// --- CURATED PRESET: Editorial Dark (magazine-editorial inspired) ---
// The signature is the TWO-FONT pairing, applied automatically:
//   headline  = Playfair Display (large serif, italic emphasis on key words)
//   accent    = a script for the sub-line ("Lauras Erfolgsstory", "Wie ging das?")
//   kicker    = small letter-spaced uppercase Montserrat ("SELL IT WITH A STORY")
// darkPhoto controls whether photos get the dark/desaturated editorial wash.
export const buildEditorialDark = (darkPhoto = true) => ({
  id: Date.now(),
  name: 'Editorial Dark',
  ruleSet: 'editorial_dark',
  colors: darkPhoto
    ? { primary: '#FBF7F1', secondary: '#2A211C', tertiary: '#4E3F36', accent: '#D9C4A9', neutral: '#1A1310', background: '#151009' }
    : { primary: '#2A211C', secondary: '#8A6A4B', tertiary: '#B79B7C', accent: '#9A3B2E', neutral: '#F1E9DD', background: '#EFE7DA' },
  typography: {
    fontFamily: 'Playfair Display',   // big serif headline
    accentFontFamily: 'Montserrat',   // small spaced UPPERCASE sans (frame lines)
    bodyFontFamily: 'Montserrat',
    fontWeight: '500',
    fontSize: 52,
    lineHeight: 1.12,
    letterSpacing: '-0.02em',
    fontStyle: 'normal',
  },
  layout: 'auto',
  visualElements: [],
  timestamp: new Date().toISOString(),
  generatedDetails: { colorName: darkPhoto ? 'editorial_dark' : 'editorial_warm', typoName: 'serif_caps_pairing' },
  darkPhoto,
  sampleText: "WENN DIR JEMAND SAGT\nDu bist Fotografin, aber du verkaufst keine Fotos",
  tags: ['editorial', 'dark', 'serif', 'caps'],
});

export const generateMixedBrand = () => {
  const randomColorKey = getRandomKey(colorGenerators);
  const randomTypoKey = getRandomKey(typographyGenerators);
  const randomLayoutKey = getRandomKey(layoutGenerators);
  
  const colors = colorGenerators[randomColorKey]();
  const typography = typographyGenerators[randomTypoKey]();
  const layout = randomLayoutKey;
  
  return {
    id: Date.now(),
    name: generateRandomName(),
    ruleSet: 'custom_generated',
    colors,
    typography,
    layout,
    visualElements: [],
    timestamp: new Date().toISOString(),
    generatedDetails: {
      colorName: randomColorKey,
      typoName: randomTypoKey
    },
    sampleText: "DEINE VISION. *DEIN WEG*.", // GENERATOR SAMPLE WITH HIGHLIGHTS
    tags: ['custom', 'generated']
  };
};

// --- FIXED CURATED BRANDS ---
// Always present in "Meine Brands", stable IDs, never randomly generated.
// buildEditorialDark(true/false) provides the two-font signature look.
export const CURATED_BRANDS = [
  {
    ...buildEditorialDark(true),
    id: 'curated_editorial_dark',
    name: 'Editorial Dark',
    curated: true,
    editorialDark: true,
    tags: ['editorial', 'dark', 'kuratiert'],
  },
  {
    ...buildEditorialDark(false),
    id: 'curated_editorial_hell',
    name: 'Editorial Hell',
    curated: true,
    editorialDark: true,
    tags: ['editorial', 'hell', 'kuratiert'],
  },
];

export const generateTrulyRandomBrand = (specificRuleSetKey = null) => {
  const keys = Object.keys(brandRuleSets);
  const ruleSetKey = specificRuleSetKey && brandRuleSets[specificRuleSetKey] ? specificRuleSetKey : (keys.includes('cleanCreator') ? 'cleanCreator' : keys[0]);
  const ruleSet = brandRuleSets[ruleSetKey];
  
  const colors = colorGenerators[ruleSet.colorStrategy] ? colorGenerators[ruleSet.colorStrategy]() : colorGenerators.mono_classic();
  const typoKey = ruleSet.typographyRules[0];
  const typography = typographyGenerators[typoKey] ? typographyGenerators[typoKey]() : typographyGenerators.editorial_serif();
  
  const layoutRules = ruleSet.layoutRules || ['centered_focus'];
  const layoutKey = layoutRules[Math.floor(Math.random() * layoutRules.length)];
  
  return {
    id: Date.now(),
    name: ruleSet.name,
    ruleSet: ruleSetKey,
    colors,
    typography,
    layout: layoutKey,
    visualElements: [],
    timestamp: new Date().toISOString(),
    generatedDetails: {
      industry: 'Leadership',
      targetAudience: 'Entrepreneurs'
    },
    sampleText: "KLARHEIT DURCH *FOKUS*.", // PRESET SAMPLE WITH HIGHLIGHTS
    tags: ruleSet.tags
  };
};