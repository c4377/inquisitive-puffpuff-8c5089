// DYNAMIC GERMAN CONTENT STRATEGY (High Performance Engine) 
// Focus: Scroll-Stopping Hooks & Psychological Triggers based on Persona

const SemanticAdapter = {
  // Detects if text is likely a full sentence starting with "Ich"
  isIchSentence: (text) => {
    if (!text) return false;
    const lower = text.toLowerCase().trim();
    return lower.startsWith('ich ') || lower.startsWith('"ich ') || lower.startsWith("'ich ");
  },
  
  // Cleans punctuation to avoid double endings
  cleanPunctuation: (text) => {
    if (!text) return "";
    return text.replace(/^["']|["']$/g, '').replace(/[.,;!?]+$/, "").trim();
  },
  
  // --- THE SCROLL STOPPER ENGINE ---
  // Generates high-impact hooks based on type and input content
  // AUTOMATICALLY ADDS *HIGHLIGHTS* FOR MIXED TYPOGRAPHY
  createHook: (input, type = 'pain') => {
    const text = SemanticAdapter.cleanPunctuation(input);
    const isIch = SemanticAdapter.isIchSentence(text);
    
    // Helper to highlight last word or key phrases
    const highlightKey = (str) => {
       const words = str.split(' ');
       if (words.length > 2) {
          // Highlight last 1-2 words
          const last = words.pop();
          return `${words.join(' ')} *${last}*`;
       }
       return `*${str}*`;
    };

    // 1. PAIN POINT HOOKS (The "Stop Scroll" Triggers)
    if (type === 'pain') {
      if (isIch) {
        // Input: "Ich fühle mich unsichtbar"
        const templates = [
          `Hör auf, dir zu sagen: "*${text}*".`, // Stop doing it
          `Die brutale *Wahrheit*, wenn du denkst: "${text}".`, // Hard Truth
          `Warum "*${text}*" deine größte *Lüge* ist.`, // Provocation
          `Hand aufs Herz: Wie oft denkst du *${text}*?`, // Direct Question
          `Dieser Moment, wenn du merkst: *${text}*.` // Relatability
        ];
        return templates[Math.floor(Math.random() * templates.length)];
      } else {
        // Input: "Unsichtbarkeit" or "Chaos"
        const templates = [
          `Warum *${text}* dich heimlich killt.`,
          `Du bist nicht müde. Du bist erschöpft von *${text}*.`,
          `Lass uns ehrlich über *${text}* sprechen.`,
          `Das Problem ist nicht *${text}*. Das Problem ist, dass du es akzeptierst.`,
          `Kennst du dieses *Gefühl* von ${text}?`
        ];
        return templates[Math.floor(Math.random() * templates.length)];
      }
    }

    // 2. GOAL / DESIRE HOOKS (The "Dream" Triggers)
    if (type === 'goal') {
      const templates = [
        `Stell dir vor, *${text}* wäre heute schon Realität.`,
        `Der schnellste Weg, um endlich *${text}*.`,
        `Warum du *${text}* verdienst (und es dir nehmen darfst).`,
        `POV: Du hast endlich erreicht, *${text}*.`,
        `Das *Geheimnis*, um wirklich *${text}*.`
      ];
      return templates[Math.floor(Math.random() * templates.length)];
    }
    
    return highlightKey(input);
  }
};

export const generate7DayPlan = (strategy, brandConfig) => {
  const brandFont = brandConfig?.typography?.fontFamily || 'Playfair Display';
  
  // 1. DATA PREPARATION
  const clean = (str) => str.replace(/^["']|["']$/g, '').trim();
  const painPoints = (strategy?.painPoints && strategy.painPoints.length > 0) ? strategy.painPoints.map(clean) : ["Ich drehe mich im Kreis", "Ich traue mich nicht raus", "Ich fühle mich blockiert"];
  const goals = (strategy?.goals && strategy.goals.length > 0) ? strategy.goals.map(clean) : ["frei sein", "sichtbar werden", "mein Ding machen"];
  
  const p1 = painPoints[0];
  const p2 = painPoints[1] || p1;
  const p3 = painPoints[2] || p1;
  
  const g1 = goals[0];
  
  // 2. HELPER: CREATE SLIDE
  const createBaseSlide = (overrides = {}) => ({
    id: Date.now() + Math.random(),
    fontSize: 42,
    fontFamily: brandFont,
    fontWeight: '400',
    color: '#000000',
    backgroundColor: '#FFFFFF',
    visualElements: [],
    format: '4:5',
    imageScale: 1,
    imageX: 0,
    imageY: 0,
    overlay: 0,
    layout: 'minimal_quote',
    ...overrides
  });

  // 3. THE 7-DAY STRATEGY MIX (High Impact with Highlights)
  
  // --- DAY 1: THE HARD TRUTH (Identity Shift) ---
  const d1Hook = SemanticAdapter.createHook(p1, 'pain');
  
  const day1 = {
    day: 1,
    title: "Real Talk",
    layout: 'maximized_bold', // Big Typography
    caption: `Es muss gesagt werden.`,
    slides: [
      d1Hook, // SCROLL STOPPER with *Highlights*
      `Wir erzählen uns diese *Geschichte* immer wieder.`,
      `Aber solange du glaubst, dass das *wahr* ist, wirst du dich nicht bewegen.`,
      `Die Wahrheit ist: Es ist nur ein *Gedanke*. Keine Tatsache.`,
      `Du kannst diese Story *umschreiben*.`,
      `Fang *heute* damit an.`
    ]
  };

  // --- DAY 2: THE RELATABLE STORY (Connection) ---
  const d2Title = SemanticAdapter.isIchSentence(p2) ? `"${SemanticAdapter.cleanPunctuation(p2)}"` : p2;
  const day2 = {
    day: 2,
    title: "Story Time",
    layout: 'minimal_left_accent', // Reading focus
    caption: `Kennst du das?`,
    slides: [
      `Gestern sagte eine Kundin zu mir:\n*${d2Title}*`, // Story Hook
      `Sie dachte, sie wäre die *Einzige*, die sich so fühlt.`,
      `Sie dachte, alle anderen hätten den *Code* geknackt, nur sie nicht.`,
      `Aber hier ist, was ich ihr gesagt habe...`,
      `Dieses Gefühl ist nicht das Ende. Es ist der Anfang deines *Durchbruchs*.`,
      `Bist du bereit, das *loszulassen*?`
    ]
  };

  // --- DAY 3: THE VISION (Desire) ---
  const d3Hook = SemanticAdapter.createHook(g1, 'goal');
  const day3 = {
    day: 3,
    title: "Vision",
    layout: 'editorial_mask', // Image focus
    caption: `Dein Ziel ist näher als du denkst.`,
    slides: [
      d3Hook,
      `Oft denken wir, wir müssten erst noch X oder Y tun, bevor wir das *haben* dürfen.`,
      `Aber was, wenn du heute schon so handeln würdest, als wärst du schon *dort*?`,
      `*Verkörperung* (Embodiment) kommt VOR dem Ergebnis.`,
      `Sei heute die *Version* von dir, die das schon hat.`,
      `Wie würde sie jetzt *entscheiden*?`
    ]
  };

  // --- DAY 4: THE MYTH BUSTER (Authority) ---
  const day4 = {
    day: 4,
    title: "Klartext",
    layout: 'split_vertical_editorial', // Editorial Look
    caption: `Lass uns damit aufhören.`,
    slides: [
      `Hör auf zu glauben, du müsstest "*perfekt*" sein, um zu starten.`, 
      `Perfektionismus ist nur *Angst* in Schuhen.`,
      `Deine Zielgruppe will keinen glatten Avatar.`,
      `Sie wollen *DICH*. Mit Ecken, Kanten und deiner wahren Energie.`,
      `Zeig dich *unperfekt*. Das ist das neue Gold.`,
      `Traust du dich?`
    ]
  };

  // --- DAY 5: THE REMINDER (Empathy) ---
  const d5Hook = SemanticAdapter.createHook(p3, 'pain');
  const day5 = {
    day: 5,
    title: "Erinnerung",
    layout: 'minimal_quote', // Quote Style
    caption: `Für dich.`,
    slides: [
      d5Hook,
      `Ich weiß, wie *schwer* sich das anfühlen kann.`,
      `Aber vergiss bitte nicht:`,
      `Du bist nicht hier, um *klein* zu bleiben.`,
      `Du bist hier, um *Raum* einzunehmen.`,
      `Nimm ihn dir.`
    ]
  };

  // --- DAY 6: THE STRATEGY (Value) ---
  const day6 = {
    day: 6,
    title: "Strategie",
    layout: 'aesthetic_checklist', // List Style
    caption: `Speicher dir das ab.`,
    slides: [
      `3 Dinge, die ich meinem früheren Ich sagen würde:`,
      `1. Hör auf zu warten, bis du dich "*bereit*" fühlst.`,
      `2. Deine *Identität* ist wichtiger als deine Strategie.`,
      `3. Konsistenz schlägt Intensität. *Immer*.`,
      `Welcher Punkt trifft dich heute am meisten?`
    ]
  };

  // --- DAY 7: THE OFFER (Call to Action) ---
  const day7 = {
    day: 7,
    title: "Zusammenarbeit",
    layout: 'centered_focus', // Clear Focus
    caption: `Bist du bereit?`,
    slides: [
      `Ich suche keine *Follower*.`,
      `Ich suche Frauen, die bereit sind für *mehr*.`,
      `Wenn du spürst, dass da noch so viel mehr in dir steckt...`,
      `...dann ist das hier dein *Zeichen*.`,
      `Schreib mir "*START*" und wir schauen, ob wir matchen.`,
      `Let's do this.`
    ]
  };

  const weekTemplate = [day1, day2, day3, day4, day5, day6, day7];

  // 4. BUILD FINAL PLAN
  return weekTemplate.map((dayContent) => {
    const slides = dayContent.slides.map((text, i) => {
      let fontSize = 42;
      let fontFamily = brandFont;
      let textAlign = undefined;

      // Smart Fonts & Sizes based on Layout
      if (dayContent.layout === 'maximized_bold') {
        fontSize = 64;
        fontFamily = brandConfig?.typography?.bodyFontFamily || 'Montserrat';
      }
      if (dayContent.layout === 'minimal_quote') fontSize = 48;
      if (dayContent.layout === 'centered_focus') fontSize = 46;

      // Slide 2+ Logic (Body Text)
      if (i > 0) {
        fontFamily = brandConfig?.typography?.bodyFontFamily || 'Montserrat';
        fontSize = 24; // Readable Body Text
        textAlign = 'left';
        if (dayContent.layout === 'minimal_quote') textAlign = 'center';
      }

      return createBaseSlide({
        text: text,
        layout: dayContent.layout,
        fontSize: fontSize,
        fontFamily: fontFamily,
        textAlign: textAlign,
        slideNumber: i + 1,
        totalSlides: dayContent.slides.length
      });
    });

    return {
      day: dayContent.day,
      type: 'carousel',
      title: dayContent.title,
      description: dayContent.caption,
      caption: dayContent.caption,
      slides: slides
    };
  });
};