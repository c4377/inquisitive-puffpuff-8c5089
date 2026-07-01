// postRole.js
// Makes the "red thread" of a feed visible: every post plays a role in the
// journey from raising a question to delivering proof to leading to the offer.
// This is the app embodying Carina's claim "Struktur ersetzt das Raten" —
// instead of guessing why a feed works, the structure is shown.
//
// Three roles:
//   'frage'   — hook / opens a question / names a problem (creates pull)
//   'beweis'  — proof / example / explanation / result (builds trust)
//   'angebot' — call-to-action / leads to the offer (converts)
//
// The role is inferred from the post text using light heuristics. It is a
// suggestion the user can see and think with, not a hard classification.

const OFFER_SIGNALS = [
  'buch dir', 'buche', 'termin', 'link in bio', 'schreib mir', 'melde dich',
  'sichere dir', 'arbeite mit mir', 'zusammenarbeit', 'schreib mir eine',
  'anmeld', 'warteliste', 'begleite dich', 'orientierungscall',
  'buch dir einen', 'komm in', 'hol dir', 'jetzt starten', 'jetzt buchen',
];

const PROOF_SIGNALS = [
  'beispiel', 'z.b', 'zum beispiel', 'kundin', 'kunde', 'ergebnis',
  'case', 'vorher', 'nachher', 'so funktioniert', 'schritt für schritt',
  'weil', 'deshalb', 'darum', 'studie', 'zahlen', 'erfahrung',
  'ich sehe', 'ich beobachte', 'in calls', 'in meinen calls', 'konkret',
  'analyse', 'strategie', 'system', 'menschen kaufen', 'die wahrheit',
];

const HOOK_SIGNALS = [
  'kennst du', 'kennst du das', 'frage mich', 'frage ich mich', 'warum',
  'manchmal', 'was wäre', 'stell dir vor', 'hast du schon', 'weißt du',
];

const cleanText = (t) => (typeof t === 'string' ? t.toLowerCase() : '');
const hasAny = (text, list) => list.some((w) => text.includes(w));

// Decide the role of a single post from its text.
export const detectPostRole = (text) => {
  const t = cleanText(text);
  if (!t.trim()) return 'frage';

  // Clear call to action -> offer.
  if (hasAny(t, OFFER_SIGNALS)) return 'angebot';

  // Opens a question / hooks the reader.
  const opensQuestion = t.includes('?') || hasAny(t, HOOK_SIGNALS);

  // Proof language -> proof (even alongside a soft opener, proof carries it).
  if (hasAny(t, PROOF_SIGNALS)) return 'beweis';

  if (opensQuestion) return 'frage';

  // Default: a statement that neither asks nor sells still carries the
  // argument -> proof.
  return 'beweis';
};

// Role metadata for display (label, short meaning, accent color).
export const ROLE_META = {
  frage: {
    label: 'Frage',
    meaning: 'Öffnet ein Thema, zieht rein',
    color: '#B45309', // amber-700
    bg: '#FEF3C7',    // amber-100
  },
  beweis: {
    label: 'Beweis',
    meaning: 'Zeigt, dass du es kannst',
    color: '#443027', // Kaffeebraun (brand)
    bg: '#EFE9E5',
  },
  angebot: {
    label: 'Angebot',
    meaning: 'Führt zum nächsten Schritt',
    color: '#065F46', // emerald-800
    bg: '#D1FAE5',    // emerald-100
  },
};

// Analyze a whole plan (array of days, each with slides) and return a summary:
// counts per role + the ordered sequence of roles across the feed. Uses the
// FIRST slide's text of each day as the post's leading message.
export const analyzePlanRoles = (weekPlan = []) => {
  const sequence = [];
  const counts = { frage: 0, beweis: 0, angebot: 0 };
  weekPlan.forEach((day) => {
    const lead = day?.slides?.[0]?.text || day?.slides?.[0]?.caption || '';
    const role = detectPostRole(lead);
    counts[role] += 1;
    sequence.push({ day: day.day, title: day.title, role });
  });
  const total = sequence.length || 1;
  const balance = {
    frage: Math.round((counts.frage / total) * 100),
    beweis: Math.round((counts.beweis / total) * 100),
    angebot: Math.round((counts.angebot / total) * 100),
  };
  return { sequence, counts, balance, total: sequence.length };
};

// Short, human read on whether the feed is balanced — so the user sees not just
// the numbers but what they mean. Reflects Carina's warm, clear voice.
export const roleFeedback = (analysis) => {
  const { counts, total } = analysis;
  if (!total) return '';
  if (counts.angebot === 0) {
    return 'Kein Post führt zum Angebot. Ein klarer nächster Schritt fehlt noch.';
  }
  if (counts.beweis === 0) {
    return 'Es fehlt Beweis — Posts, die zeigen, dass du lieferst.';
  }
  if (counts.frage === 0) {
    return 'Nichts öffnet ein Thema. Ein Hook, der reinzieht, würde helfen.';
  }
  if (counts.angebot > total / 2) {
    return 'Viel Angebot, wenig Aufbau. Mehr Frage & Beweis trägt das Angebot.';
  }
  return 'Guter Rhythmus: Fragen ziehen rein, Beweise tragen, das Angebot führt weiter.';
};
