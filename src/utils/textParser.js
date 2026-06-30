/**
 * Intelligent Text Parser
 * Optimized for "Human" format (No JSON required)
 */

export const parseSmartInput = (input) => {
  if (!input || !input.trim()) return [];

  // 1. TRY JSON PARSING FIRST (Legacy Support)
  try {
    const cleanJson = input.replace(/```json/g, '').replace(/```/g, '').trim();
    if (cleanJson.startsWith('[') && cleanJson.endsWith(']')) {
      const parsed = JSON.parse(cleanJson);
      if (Array.isArray(parsed)) return parsed.map(day => ({
        day: day.day || 1,
        title: day.title || 'Untitled',
        caption: day.caption || '',
        slides: Array.isArray(day.slides) ? day.slides : [day.slides || '']
      }));
    }
  } catch (e) {
    // Not JSON, ignore
  }

  // 2. ROBUST TEXT PARSING (The "Human" Way)
  const days = [];
  const lines = input.split('\n');
  let currentDay = null;
  let currentSlides = [];
  let bufferText = [];

  const flushBufferToSlide = () => {
    if (bufferText.length > 0) {
      const fullText = bufferText.join('\n').trim();
      if (fullText) currentSlides.push(fullText);
      bufferText = [];
    }
  };

  lines.forEach(line => {
    const trimmed = line.trim();
    if (!trimmed) return;

    // Detect Day Header (Tag 1, Day 1, Woche 1)
    const dayMatch = trimmed.match(/^(?:Tag|Day|Woche)\s*(\d+)(?:[:.-]|\s+|$)(.*)/i);
    if (dayMatch) {
      flushBufferToSlide();
      if (currentDay) {
        currentDay.slides = currentSlides.length > 0 ? currentSlides : ["Inhalt folgt..."];
        days.push(currentDay);
      }
      currentDay = {
        day: parseInt(dayMatch[1]),
        title: dayMatch[2] ? dayMatch[2].trim() : `Tag ${dayMatch[1]}`,
        caption: "",
        slides: []
      };
      currentSlides = [];
      return;
    }

    // Detect Slide Marker
    const slideMatch = trimmed.match(/^(?:Slide|Folie|Bild|Page)\s*\d+(?:[:.-]|\s+|$)(.*)/i);
    if (slideMatch && currentDay) {
      flushBufferToSlide();
      if (slideMatch[1] && slideMatch[1].trim()) {
        bufferText.push(slideMatch[1].trim());
      }
      return;
    }

    // Detect Caption
    if (trimmed.toLowerCase().startsWith('caption:')) {
      if (currentDay) currentDay.caption = trimmed.substring(8).trim();
      return;
    }

    // Normal Text Content
    if (currentDay) {
      bufferText.push(trimmed);
    } else {
      // Content before any "Tag 1" -> Implicit Day 1
      currentDay = { day: 1, title: 'Mein Content', caption: '', slides: [] };
      bufferText.push(trimmed);
    }
  });

  flushBufferToSlide();
  if (currentDay) {
    currentDay.slides = currentSlides.length > 0 ? currentSlides : ["Inhalt..."];
    days.push(currentDay);
  }

  return days;
};

// --- NEW: PERSONA PARSER (Derive Strategy) ---
export const deriveStrategyFromPersona = (text) => {
  if (!text) return { painPoints: [], goals: [] };

  // 1. Split into sentences (simple regex for basic punctuation)
  // Maps roughly to sentence structures
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
  
  const painPoints = [];
  const goals = [];
  
  // Keywords indicating pain or desire
  const painKeywords = ['angst', 'sorge', 'problem', 'schwer', 'müde', 'zweifel', 'druck', 'allein', 'chaos', 'feststecken', 'unsichtbar', 'überfordert', 'nicht gut genug', 'traut sich nicht', 'versteckt'];
  const goalKeywords = ['will', 'möchte', 'traum', 'ziel', 'frei', 'leicht', 'erfolg', 'geld', 'wachstum', 'sichtbar', 'klarheit', 'erreichen', 'wünscht'];

  sentences.forEach(rawSentence => {
    let s = rawSentence.trim();
    if (s.length < 10) return;

    // Pronoun Swapping (Third Person -> First Person)
    // Translates "Sie hat Angst" -> "Ich habe Angst" automatically
    s = s.replace(/\b(Sie|Er)\s+hat\b/gi, "Ich habe");
    s = s.replace(/\b(Sie|Er)\s+ist\b/gi, "Ich bin");
    s = s.replace(/\b(Sie|Er)\s+will\b/gi, "Ich will");
    s = s.replace(/\b(Sie|Er)\s+fühlt\b/gi, "Ich fühle");
    s = s.replace(/\b(Sie|Er)\s+denkt\b/gi, "Ich denke");
    s = s.replace(/\b(Sie|Er)\s+glaubt\b/gi, "Ich glaube");
    s = s.replace(/\b(Sie|Er)\s+möchte\b/gi, "Ich möchte");
    s = s.replace(/\b(Sie|Er)\s+kann\b/gi, "Ich kann");
    s = s.replace(/\b(Sie|Er)\s+traut\b/gi, "Ich traue");
    
    // Possessive Pronouns
    s = s.replace(/\bIhr\s+/g, "Mein "); // Case sensitive start
    s = s.replace(/\bSein\s+/g, "Mein ");
    s = s.replace(/\bihr\s+/gi, "mein ");
    s = s.replace(/\bsein\s+/gi, "mein ");
    s = s.replace(/\bIhre\s+/g, "Meine ");
    s = s.replace(/\bSeine\s+/g, "Meine ");
    s = s.replace(/\bihre\s+/gi, "meine ");
    s = s.replace(/\bseine\s+/gi, "meine ");
    
    // Check keywords to categorize
    const lower = s.toLowerCase();
    const isPain = painKeywords.some(k => lower.includes(k));
    const isGoal = goalKeywords.some(k => lower.includes(k));

    if (isPain) {
      if (painPoints.length < 6) painPoints.push(s);
    } else if (isGoal) {
      if (goals.length < 4) goals.push(s);
    } else {
      // If ambiguous but looks like a statement about the self, treat as pain point if we don't have enough
      if (s.startsWith("Ich") && painPoints.length < 6) {
        painPoints.push(s);
      }
    }
  });

  // Defaults if nothing found (Fallbacks)
  if (painPoints.length === 0) {
    painPoints.push("Ich fühle mich unsichtbar.");
    painPoints.push("Ich weiß nicht, wo ich anfangen soll.");
  }
  if (goals.length === 0) {
    goals.push("Ich will endlich sichtbar werden.");
  }

  return { painPoints, goals };
};