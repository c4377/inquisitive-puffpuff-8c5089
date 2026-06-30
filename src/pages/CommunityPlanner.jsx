import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import * as FiIcons from 'react-icons/fi';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import SafeIcon from '../common/SafeIcon';
import Canvas from '../components/Canvas';
import StyleShifter from '../components/StyleShifter';
import { useBrand } from '../context/BrandContext';
import { generatePresentationDeck, communityTopics } from '../utils/communityContentTemplates';
import { renderSlide } from '../utils/canvasRenderer';

const { FiMonitor, FiDownload, FiRefreshCw, FiLayers, FiFileText, FiX, FiPlay, FiTrash2, FiEdit3 } = FiIcons;

const CommunityPlanner = () => {
  const { brandSettings, updateCommunityDeck, dataLoaded } = useBrand();
  const navigate = useNavigate();
  const [selectedTopic, setSelectedTopic] = useState('mindset');
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showBulkInput, setShowBulkInput] = useState(false);
  const [bulkText, setBulkText] = useState('');
  const [showShifter, setShowShifter] = useState(false);

  const brandName = brandSettings.currentBrandConfig?.name || "MUSE MENTORING";

  useEffect(() => {
    if (dataLoaded && brandSettings.currentBrandConfig) {
      loadContent();
    }
  }, [selectedTopic, dataLoaded, brandSettings.currentBrandConfig]);

  const loadContent = () => {
    const savedDeck = brandSettings.communityDecks?.[selectedTopic];
    if (savedDeck && Array.isArray(savedDeck) && savedDeck.length > 0) {
      setContent(savedDeck);
      setLoading(false);
    } else {
      generateNewContent();
    }
  };

  const generateNewContent = () => {
    if (!brandSettings.currentBrandConfig) return;
    setLoading(true);
    setTimeout(() => {
      const slides = generatePresentationDeck(selectedTopic, brandSettings.currentBrandConfig);
      const dynamicSlides = slides.map(s => ({
        ...s,
        format: '16:9',
      }));
      setContent(dynamicSlides);
      updateCommunityDeck(selectedTopic, dynamicSlides);
      setLoading(false);
    }, 400);
  };

  // --- HELPER: AUTO HIGHLIGHTER ---
  const applyAutoHighlight = (text) => {
    if (!text) return "";
    if (text.includes('*')) return text;
    const lines = text.split('\n');
    if (lines.length > 0 && lines[0].trim().length > 0) {
      const words = lines[0].trim().split(' ');
      if (words.length >= 1) {
        const lastWord = words.pop();
        lines[0] = [...words, `*${lastWord}*`].join(' ');
      }
    }
    return lines.join('\n');
  };

  // --- HELPER: CONTRAST UTILS ---
  const getLuminance = (hex) => {
    if (!hex) return 255;
    const fullHex = hex.length === 4 ? '#' + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3] : hex;
    const r = parseInt(fullHex.slice(1, 3), 16);
    const g = parseInt(fullHex.slice(3, 5), 16);
    const b = parseInt(fullHex.slice(5, 7), 16);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };

  // --- DYNAMIC STYLE RESOLVER ---
  const resolveSlideStyle = (slide, index) => {
    const config = brandSettings.currentBrandConfig;
    if (!config) return slide;

    const colors = config.colors || { primary: '#000', background: '#fff', secondary: '#ccc', accent: '#888' };
    const typography = config.typography || { fontFamily: 'Inter' };

    // 1. Layout & Font Logic
    const isTitle = index === 0;
    const isQuote = slide.layout === 'minimal_quote';
    const displayFont = typography.fontFamily;
    const bodyFont = typography.bodyFontFamily || displayFont;
    const fontFamily = (isTitle || isQuote) ? displayFont : bodyFont;
    
    let accentFontFamily = typography.accentFontFamily;
    if (!accentFontFamily || accentFontFamily === fontFamily) {
       if (fontFamily.includes('Playfair') || fontFamily.includes('Garamond') || fontFamily.includes('Serif')) {
         accentFontFamily = 'Montserrat';
       } else {
         accentFontFamily = 'Playfair Display';
       }
    }

    // 2. Color Rotation Logic
    let bg = colors.background;
    let txt = colors.primary;
    let acc = colors.accent;
    let sec = colors.secondary;

    // Pattern: 0=Std, 1=Inverted, 2=Pop, 3=Std, 4=Editorial
    const stylePattern = index % 5;
    if (stylePattern === 1) { // Inverted (Primary BG)
      bg = colors.primary;
      txt = colors.background;
      // Text safety on dark primary
      if (getLuminance(bg) < 100 && getLuminance(txt) < 150) txt = '#FFFFFF';
      acc = colors.secondary;
    } else if (stylePattern === 2) { // POP (Accent BG)
      bg = colors.accent;
      txt = '#FFFFFF';
      acc = colors.background;
      // If Accent BG is bright (Yellow), Text must be Black
      if (getLuminance(bg) > 150) txt = '#000000';
    } else if (stylePattern === 4) { // Editorial (Secondary BG)
      bg = colors.secondary;
      txt = colors.primary;
    }

    // 3. ULTRA STRICT CONTRAST ENFORCEMENT
    const bgLum = getLuminance(bg);
    // Helper to flip color if contrast is too low
    const ensureContrast = (colorToCheck) => {
      if (Math.abs(bgLum - getLuminance(colorToCheck)) < 80) {
        return bgLum > 128 ? '#000000' : '#FFFFFF';
      }
      return colorToCheck;
    };

    txt = ensureContrast(txt);
    acc = ensureContrast(acc);
    // Special case: If Secondary is used as BG (Pattern 4) and it's too close to Primary, 
    // ensureContrast above fixes text. 
    // BUT if Secondary is used as an ELEMENT on a Standard BG (Pattern 0/3), we need to check that too.
    if (Math.abs(bgLum - getLuminance(sec)) < 30) {
      // If Secondary is invisible on BG, shift it slightly
      // Simple hack: if BG is light, make sec darker. If BG dark, make sec lighter.
      sec = bgLum > 128 ? '#888888' : '#AAAAAA';
    }

    return {
      ...slide,
      fontFamily,
      accentFontFamily,
      color: txt,
      backgroundColor: bg,
      accentColor: acc,
      secondaryColor: sec,
      layout: slide.layout || 'centered_focus'
    };
  };

  const handleEditDeck = () => {
    if (content.length === 0) return;
    const bakedSlides = content.map((s, i) => resolveSlideStyle(s, i));
    navigate('/editor', { state: { slides: bakedSlides, dayTitle: `${selectedTopic.toUpperCase()} Masterclass`, communityTopicId: selectedTopic } });
  };

  const handleEditSlide = (index) => {
    const bakedSlides = content.map((s, i) => resolveSlideStyle(s, i));
    navigate('/editor', { state: { slides: bakedSlides, initialSlideIndex: index, dayTitle: `${selectedTopic.toUpperCase()} Masterclass`, communityTopicId: selectedTopic } });
  };

  const handleBulkGenerate = () => {
    if (!bulkText.trim()) return;
    
    // UPDATED REGEX: Split only by Slide Markers
    const slideTexts = bulkText.split(/(?:Slide|Folie)\s*\d+\s*[:.-]?/i).filter(t => t.trim().length > 0);
    
    if (slideTexts.length === 0) {
        slideTexts.push(bulkText.trim());
    }

    const newSlides = slideTexts.map((rawText, index) => {
      const text = applyAutoHighlight(rawText.trim());
      const isTitleSlide = index === 0;
      
      // CHECK FOR NUMBERS to conditionally use "Big Numbers" layout
      const hasNumbers = /[0-9]/.test(text);

      // Define Layout Rotation
      // 1. Title (Center)
      // 2. Big Numbers (List) -> ONLY IF NUMBERS
      // 3. Split Editorial (Right)
      // 4. Quote (Center)
      // 5. Left Accent (Left)
      let layout = 'centered_focus';
      if (isTitleSlide) {
        layout = 'centered_focus';
      } else {
        // Smart Rotation logic
        const rotIndex = index % 4;
        // Cycle through 4 main content layouts
        if (hasNumbers) {
          layout = 'bold_number_list';
        } else {
          // Skip bold_number_list if no numbers
          const editorialLayouts = [
            'split_vertical_editorial',
            'minimal_quote',
            'minimal_left_accent',
            'centered_focus' // Fallback/Variety
          ];
          layout = editorialLayouts[rotIndex];
        }
      }

      // Alignments mapping based on layout
      let align = 'center';
      if (layout === 'minimal_left_accent' || layout === 'bold_number_list') align = 'left';
      if (layout === 'split_vertical_editorial') align = 'right';

      return {
        id: Date.now() + index,
        format: '16:9',
        text: text,
        fontSize: isTitleSlide ? 64 : 48,
        layout: layout,
        textAlign: align,
        imageScale: 1,
        slideNumber: index + 1,
        totalSlides: slideTexts.length
      };
    });

    setContent(newSlides);
    updateCommunityDeck(selectedTopic, newSlides);
    setShowBulkInput(false);
    setBulkText('');
  };

  const downloadImage = async (slideData, filename, index) => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const width = 1920;
    const height = 1080;
    canvas.width = width;
    canvas.height = height;
    await document.fonts.ready;
    const scale = 1920 / 960;
    const styledSlide = resolveSlideStyle(slideData, index);
    await renderSlide(ctx, styledSlide, width, height, { slideIndex: 0, totalSlides: 1, scale: scale, globalBrandName: brandName });
    canvas.toBlob((blob) => {
      saveAs(blob, filename);
    });
  };

  const downloadDeck = async () => {
    const zip = new JSZip();
    const folder = zip.folder(`${selectedTopic}_Presentation`);
    await document.fonts.ready;

    for (let i = 0; i < content.length; i++) {
      const rawSlide = content[i];
      const slide = resolveSlideStyle(rawSlide, i);
      const canvas = document.createElement('canvas');
      canvas.width = 1920;
      canvas.height = 1080;
      const ctx = canvas.getContext('2d');
      const scale = 1920 / 960;
      await renderSlide(ctx, slide, 1920, 1080, { slideIndex: i, totalSlides: content.length, scale: scale, globalBrandName: brandName });
      const blob = await new Promise(r => canvas.toBlob(r));
      folder.file(`Slide_${i + 1}.png`, blob);
    }
    const contentZip = await zip.generateAsync({ type: "blob" });
    saveAs(contentZip, `${selectedTopic}_Presentation_Deck.zip`);
  };

  if (!brandSettings.currentBrandConfig) {
    return (
      <div className="flex items-center justify-center h-[60vh] text-gray-500">
        Bitte wähle zuerst eine Brand im Dashboard oder Randomizer aus.
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Presentation Generator</h1>
          <p className="text-gray-600">Erstelle professionelle Decks in 16:9 Format.</p>
        </div>
        <div className="flex space-x-2">
          <button onClick={() => setShowShifter(!showShifter)} className={`flex items-center px-4 py-2 border rounded-lg text-sm font-bold transition-colors ${showShifter ? 'bg-purple-100 border-purple-300 text-purple-700' : 'bg-white border-gray-200 text-gray-600'}`} >
            <SafeIcon icon={FiRefreshCw} className="mr-2" /> Style Shifter
          </button>
          <button onClick={generateNewContent} className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-bold hover:bg-gray-200" >
            <SafeIcon icon={FiRefreshCw} className="mr-2" /> Reset
          </button>
          <div className="bg-white p-2 rounded-xl border border-gray-200 shadow-sm">
            <span className="text-sm font-bold text-purple-700 flex items-center px-2">
              <SafeIcon icon={FiMonitor} className="mr-2" /> PowerPoint Mode
            </span>
          </div>
        </div>
      </div>

      <AnimatePresence>
        {showShifter && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="mb-8 overflow-hidden" >
            <div className="max-w-xl">
              <StyleShifter />
              <p className="text-xs text-gray-400 mt-2 ml-1">
                Änderungen werden live auf alle Slides angewendet.
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="mb-10 overflow-x-auto pb-2 no-scrollbar">
        <div className="flex space-x-3">
          {communityTopics.map(topic => (
            <button 
              key={topic.id} 
              onClick={() => setSelectedTopic(topic.id)}
              className={`flex items-center px-5 py-3 rounded-xl border-2 transition-all whitespace-nowrap ${selectedTopic === topic.id ? 'border-purple-600 bg-purple-50 text-purple-700 font-bold' : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'}`}
            >
              <SafeIcon icon={FiIcons[topic.icon] || FiLayers} className="mr-2 text-lg" />
              {topic.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {[1, 2, 3].map(i => <div key={i} className="aspect-video bg-gray-100 rounded-xl animate-pulse" />)}
        </div>
      ) : (
        <div>
          <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
            <div className="flex items-center space-x-3">
              <h2 className="text-xl font-bold text-gray-900">Slides ({content.length})</h2>
              <button 
                onClick={() => setShowBulkInput(!showBulkInput)}
                className="text-sm bg-purple-50 text-purple-700 px-3 py-1 rounded-lg font-bold hover:bg-purple-100 transition-colors flex items-center"
              >
                <SafeIcon icon={FiFileText} className="mr-1" /> Bulk Text Input
              </button>
            </div>
            <div className="flex space-x-3">
              <button 
                onClick={handleEditDeck}
                className="bg-white border border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-bold shadow-sm hover:bg-gray-50 transition-all flex items-center"
              >
                <SafeIcon icon={FiEdit3} className="mr-2" /> Edit Presentation
              </button>
              <button 
                onClick={downloadDeck}
                className="bg-gray-900 text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-black transition-all flex items-center"
              >
                <SafeIcon icon={FiDownload} className="mr-2" /> Download Deck
              </button>
            </div>
          </div>

          <AnimatePresence>
            {showBulkInput && (
              <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="mb-8 overflow-hidden" >
                <div className="bg-white border-2 border-purple-100 rounded-xl p-6 shadow-sm">
                  <div className="flex justify-between mb-2">
                    <label className="text-sm font-bold text-gray-700">Paste your slide content (Use 'Slide 1' to separate)</label>
                    <button onClick={() => setShowBulkInput(false)}><SafeIcon icon={FiX} className="text-gray-400" /></button>
                  </div>
                  <textarea 
                    value={bulkText} 
                    onChange={(e) => setBulkText(e.target.value)}
                    className="w-full h-48 p-4 border border-gray-300 rounded-lg text-sm font-mono mb-4 focus:ring-2 focus:ring-purple-500"
                    placeholder={`Slide 1\nWelcome to the Masterclass\n(Automatische Highlights werden hinzugefügt)\n\nSlide 2\nAgenda...`}
                  />
                  <div className="flex justify-end">
                    <button 
                      onClick={handleBulkGenerate}
                      className="px-6 py-2 bg-purple-600 text-white font-bold rounded-lg hover:bg-purple-700 flex items-center"
                    >
                      <SafeIcon icon={FiPlay} className="mr-2" /> Generate Slides
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {content.map((rawSlide, index) => {
              const slide = resolveSlideStyle(rawSlide, index);
              // Force re-render if colors change substantially
              const uniqueKey = `${slide.backgroundColor}-${slide.color}-${slide.accentColor}-${index}`;
              
              return (
                <motion.div 
                  key={rawSlide.id || index} 
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.05 }}
                  className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow group"
                >
                  <div className="aspect-video w-full bg-gray-100 relative cursor-pointer" onClick={() => handleEditSlide(index)}>
                    <Canvas key={uniqueKey} data={slide} width={960} height={540} brandName={brandName} />
                    <div className="absolute top-2 left-2 bg-black/50 text-white text-[10px] px-2 py-0.5 rounded font-bold">
                      {index + 1}
                    </div>
                    <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <div className="bg-white text-gray-800 px-3 py-1.5 rounded-lg font-bold text-xs shadow-lg flex items-center">
                        <SafeIcon icon={FiEdit3} className="mr-2" /> Edit
                      </div>
                    </div>
                  </div>
                  <div className="p-3 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
                    <span className="text-xs font-medium text-gray-500 truncate w-32">
                      {slide.text ? slide.text.substring(0, 20) : 'Slide'}...
                    </span>
                    <div className="flex space-x-1">
                      <button onClick={() => handleEditSlide(index)} className="p-1.5 text-gray-400 hover:text-purple-600 rounded bg-white border border-transparent hover:border-gray-200">
                        <SafeIcon icon={FiEdit3} />
                      </button>
                      <button onClick={() => downloadImage(rawSlide, `slide_${index+1}.png`, index)} className="p-1.5 text-gray-400 hover:text-blue-600 rounded bg-white border border-transparent hover:border-gray-200">
                        <SafeIcon icon={FiDownload} />
                      </button>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default CommunityPlanner;