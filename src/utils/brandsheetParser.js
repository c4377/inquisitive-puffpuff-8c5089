// brandsheetParser.js
// Parse a pasted "Brandsheet" text into a brand config the app understands.
// Tolerant by design: finds hex colors + role keywords per line, font names
// after Headline/Fließtext/Akzent labels, and the brand name after
// "BRANDSHEET —" (or falls back to the first non-empty line).

const ROLE_MAP = [
  { keys: ['hintergrund', 'background'], slot: 'background' },
  { keys: ['kontrast', 'headline', 'anthrazit'], slot: 'tertiary' },
  { keys: ['akzent', 'accent'], slot: 'accent' },
  { keys: ['sekundär', 'sekundaer', 'secondary', 'trenn'], slot: 'secondary' },
  { keys: ['highlight', 'button'], slot: 'neutral' },
  { keys: ['text'], slot: 'primary' },
];

const cleanFontName = (raw) =>
  (raw || '')
    .replace(/[0-9]+/g, '')          // strip weights like 600
    .replace(/[—–-].*$/, '')          // strip trailing descriptions
    .replace(/\s+/g, ' ')
    .trim();

export const parseBrandsheet = (text) => {
  const src = text || '';
  const lines = src.split('\n').map((l) => l.trim()).filter(Boolean);
  if (lines.length === 0) return { ok: false, error: 'Kein Text gefunden.' };

  // --- Name ---
  let name = '';
  const nameLine = lines.find((l) => /brandsheet/i.test(l));
  if (nameLine) {
    const m = nameLine.match(/brandsheet\s*[—–:-]\s*(.+)/i);
    if (m) name = m[1].trim();
  }
  if (!name) name = lines[0].slice(0, 40);

  // --- Colors: every line containing a hex code ---
  const colors = {};
  const unassigned = [];
  lines.forEach((line) => {
    const hexes = line.match(/#[0-9A-Fa-f]{6}\b/g);
    if (!hexes) return;
    hexes.forEach((hex) => {
      const rest = line.toLowerCase();
      const role = ROLE_MAP.find((r) => r.keys.some((k) => rest.includes(k)));
      if (role && !colors[role.slot]) colors[role.slot] = hex.toUpperCase();
      else unassigned.push(hex.toUpperCase());
    });
  });
  // Fill missing slots from unassigned hexes in order.
  ['background', 'primary', 'tertiary', 'accent', 'secondary', 'neutral'].forEach((slot) => {
    if (!colors[slot] && unassigned.length) colors[slot] = unassigned.shift();
  });
  if (!colors.primary && colors.tertiary) colors.primary = colors.tertiary;
  if (Object.keys(colors).length < 2) {
    return { ok: false, error: 'Keine Farben (Hex-Codes) im Text gefunden.' };
  }

  // --- Typography: Headline / Fließtext|Body / Akzent lines ---
  const findFont = (labelRegex) => {
    const l = lines.find((x) => labelRegex.test(x));
    if (!l) return '';
    const after = l.split(/[:]/)[1] || '';
    return cleanFontName(after);
  };
  const headlineFont = findFont(/^headline/i);
  const bodyFont = findFont(/^(fließtext|fliesstext|body)/i);
  const accentFont = findFont(/^akzent/i);

  const uppercaseHeadline = /versalien|uppercase|caps/i.test(src);

  const config = {
    id: `sheet_${Date.now()}`,
    name: name || 'Importierte Brand',
    colors: {
      primary: colors.primary || '#1A1A1A',
      secondary: colors.secondary || '#8E8E86',
      tertiary: colors.tertiary || colors.primary || '#2A2A28',
      accent: colors.accent || '#C9B99A',
      neutral: colors.neutral || '#EFEFEF',
      background: colors.background || '#FFFFFF',
    },
    typography: {
      fontFamily: headlineFont || 'Playfair Display',
      bodyFontFamily: bodyFont || 'Inter',
      accentFontFamily: accentFont || headlineFont || 'Inter',
      fontWeight: '500',
      fontSize: 48,
      lineHeight: 1.15,
      letterSpacing: uppercaseHeadline ? '0.06em' : '-0.01em',
      uppercaseHeadline,
    },
    layout: 'auto',
    visualElements: [],
    timestamp: new Date().toISOString(),
    fromBrandsheet: true,
  };
  return { ok: true, config };
};
