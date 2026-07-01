import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import * as FiIcons from 'react-icons/fi';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import SafeIcon from '../common/SafeIcon';
import Canvas from '../components/Canvas';
import StyleShifter from '../components/StyleShifter'; // IMPORT NEW SHIFTER
import { useBrand } from '../context/BrandContext';
import { renderSlide } from '../utils/canvasRenderer';
import { attachSmartImages } from '../utils/smartLayoutGenerator';
import { decidePostDesign, dayHasImage } from '../utils/postDesignEngine';

const { FiSmartphone, FiDownload, FiRefreshCw, FiLayers, FiFileText, FiX, FiPlay, FiTrash2, FiEdit3, FiPlus } = FiIcons;

const StoryPlanner = () => {
  const { brandSettings, updateBrandSettings, dataLoaded } = useBrand();
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showBulkInput, setShowBulkInput] = useState(false);
  const [bulkText, setBulkText] = useState('');
  const [showShifter, setShowShifter] = useState(false);

  const brandName = brandSettings.currentBrandConfig?.name || "MUSE MENTORING";

  // Initialize with one empty story if nothing exists
  useEffect(() => {
    if (dataLoaded && stories.length === 0) {
      // Optional: Load from DB if we save story plans specifically. 
      // For now, we start fresh or from a basic template.
      handleAddStory();
    }
  }, [dataLoaded]);

  const handleAddStory = () => {
    const brandConfig = brandSettings.currentBrandConfig;
    const newStory = {
      id: Date.now(),
      format: '9:16',
      text: "Neue Story",
      fontSize: 36,
      fontFamily: brandConfig?.typography?.fontFamily || 'Inter',
      accentFontFamily: brandConfig?.typography?.accentFontFamily,
      fontWeight: '400',
      color: brandConfig?.colors?.primary || '#000000',
      backgroundColor: brandConfig?.colors?.background || '#FFFFFF',
      secondaryColor: brandConfig?.colors?.secondary || '#CCCCCC',
      accentColor: brandConfig?.colors?.accent || '#EA580C',
      layout: 'story_text_box', // Default story layout
      textAlign: 'center',
      visualElements: [],
      imageScale: 1,
      slideNumber: stories.length + 1,
      totalSlides: stories.length + 1
    };
    setStories(prev => [...prev, newStory]);
  };

  const handleEditSlide = (index) => {
    navigate('/editor', { 
      state: { 
        slides: stories, 
        initialSlideIndex: index,
        dayTitle: `Story Sequence`,
      } 
    });
  };

  const handleBulkGenerate = async () => {
    if (!bulkText.trim()) return;
    setLoading(true);
    try {
      // Split by "Story 1" / "Slide 1" / "Sequenz 1" markers.
      let slideTexts = bulkText
        .split(/(?:Story|Slide|Sequenz)\s*\d+\s*[:.-]?/i)
        .map(t => t
          // remove divider lines (⸻, ---, ___) and BLOCK section headers
          .replace(/^\s*[⸻—\-_]{2,}\s*$/gm, '')
          .replace(/^\s*BLOCK\s*\d+.*$/gim, '')
          .replace(/[⸻]/g, '')
          .trim()
        )
        .filter(t => t.length > 0);
      if (slideTexts.length === 0) slideTexts.push(bulkText.trim());

      const brandConfig = brandSettings.currentBrandConfig;
      const imagePool = brandSettings?.brandImages || [];

      // Build base story slides (9:16), then run the SAME engine as the feed:
      // auto layout + pool images (variety) + text position/bold decisions.
      let slides = slideTexts.map((text, index) => ({
        id: Date.now() + index,
        format: '9:16',
        text: text.trim(),
        fontSize: 40,
        fontFamily: brandConfig?.typography?.fontFamily || 'Inter',
        accentFontFamily: brandConfig?.typography?.accentFontFamily,
        fontWeight: '400',
        color: brandConfig?.colors?.primary || '#000000',
        backgroundColor: brandConfig?.colors?.background || '#FFFFFF',
        secondaryColor: brandConfig?.colors?.secondary || '#CCCCCC',
        accentColor: brandConfig?.colors?.accent || '#EA580C',
        layout: 'auto',
        layoutId: 'auto',
        textAlign: 'center',
        visualElements: [],
        imageScale: 1,
        slideNumber: index + 1,
        totalSlides: slideTexts.length,
      }));

      // Attach pool images across the whole sequence (global offset = unique images).
      if (imagePool.length > 0) {
        try { slides = await attachSmartImages(slides, imagePool, 0); } catch (e) { /* keep text-only */ }
      }

      // Apply the design engine per slide: position by quiet zone / rotation, bold every 4th.
      slides = slides.map((slide, index) => {
        let s2 = { ...slide };
        const hasImg = typeof s2.background === 'string' && s2.background.length > 5;
        if (!hasImg) {
          const { background, overlay, _autoImage, ...rest } = s2;
          s2 = { ...rest, background: null };
        }
        let decision = { textAnchor: { row: 'mid', col: 'center' }, bold: false };
        try {
          decision = decidePostDesign({ globalIndex: index, hasImage: hasImg, autoImage: s2._autoImage });
        } catch (e) { /* fall back to default position */ }
        return { ...s2, textAnchor: decision.textAnchor, fontWeight: decision.bold ? '700' : 'normal' };
      });

      setStories(slides);
      setShowBulkInput(false);
      setBulkText('');
    } catch (e) {
      console.error('Story bulk import failed:', e);
      alert('Beim Generieren ist ein Fehler aufgetreten. Bitte versuche es erneut.');
    } finally {
      setLoading(false);
    }
  };

  const downloadDeck = async () => {
    const zip = new JSZip();
    const folder = zip.folder(`Story_Sequence`);
    
    await document.fonts.ready;

    for (let i = 0; i < stories.length; i++) {
      const slide = stories[i];
      const canvas = document.createElement('canvas');
      canvas.width = 1080;
      canvas.height = 1920;
      const ctx = canvas.getContext('2d');
      // Base width for 9:16 in Canvas.jsx is 400. 
      // Scale = 1080 / 400 = 2.7
      const scale = 1080 / 400;
      
      await renderSlide(ctx, slide, 1080, 1920, { 
        slideIndex: i, 
        totalSlides: stories.length,
        scale: scale,
        globalBrandName: brandName
      });
      
      const blob = await new Promise(r => canvas.toBlob(r));
      folder.file(`Story_${i + 1}.png`, blob);
    }
    
    const contentZip = await zip.generateAsync({ type: "blob" });
    saveAs(contentZip, `Story_Sequence.zip`);
  };

  if (!brandSettings.currentBrandConfig) {
    return (
      <div className="flex items-center justify-center h-[60vh] text-gray-500">
        Bitte wähle zuerst eine Brand im Dashboard.
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Story Planner</h1>
          <p className="text-gray-600">Erstelle vertikale Sequenzen (9:16) für Instagram & TikTok.</p>
        </div>
        <div className="flex space-x-2">
           <button onClick={() => setShowShifter(!showShifter)} className={`flex items-center px-4 py-2 border rounded-lg text-sm font-bold transition-colors ${showShifter ? 'bg-purple-100 border-purple-300 text-purple-700' : 'bg-white border-gray-200 text-gray-600'}`} >
            <SafeIcon icon={FiRefreshCw} className="mr-2" /> Style Shifter
          </button>
          <div className="bg-white p-2 rounded-xl border border-gray-200 shadow-sm">
            <span className="text-sm font-bold text-pink-600 flex items-center px-2">
              <SafeIcon icon={FiSmartphone} className="mr-2" /> Story Mode (9:16)
            </span>
          </div>
        </div>
      </div>

      {/* SHIFTER PANEL */}
      <AnimatePresence>
        {showShifter && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="mb-8 overflow-hidden" >
            <div className="max-w-xl">
              <StyleShifter />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* BUFFER PANEL removed */}

      <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
        <div className="flex items-center space-x-3">
          <h2 className="text-xl font-bold text-gray-900">Sequenz ({stories.length})</h2>
          <button 
            onClick={() => setShowBulkInput(!showBulkInput)}
            className="text-sm bg-purple-50 text-purple-700 px-3 py-1 rounded-lg font-bold hover:bg-purple-100 transition-colors flex items-center"
          >
            <SafeIcon icon={FiFileText} className="mr-1" /> Bulk Text Input
          </button>
          <button 
            onClick={handleAddStory}
            className="text-sm bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold hover:bg-gray-200 transition-colors flex items-center"
          >
            <SafeIcon icon={FiPlus} className="mr-1" /> + Slide
          </button>
        </div>
        <div className="flex space-x-3">
          <button 
            onClick={() => handleEditSlide(0)}
            className="bg-white border border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-bold shadow-sm hover:bg-gray-50 transition-all flex items-center"
          >
            <SafeIcon icon={FiEdit3} className="mr-2" /> Edit Sequence
          </button>
          <button 
            onClick={downloadDeck}
            className="bg-gray-900 text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-black transition-all flex items-center"
          >
            <SafeIcon icon={FiDownload} className="mr-2" /> Download All (.zip)
          </button>
        </div>
      </div>

      <AnimatePresence>
        {showBulkInput && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="mb-8 overflow-hidden" >
            <div className="bg-white border-2 border-purple-100 rounded-xl p-6 shadow-sm">
              <div className="flex justify-between mb-2">
                <label className="text-sm font-bold text-gray-700">Paste your story text (Use 'Story 1' to separate)</label>
                <button onClick={() => setShowBulkInput(false)}><SafeIcon icon={FiX} className="text-gray-400" /></button>
              </div>
              <textarea 
                value={bulkText} 
                onChange={(e) => setBulkText(e.target.value)}
                className="w-full h-48 p-4 border border-gray-300 rounded-lg text-sm font-mono mb-4 focus:ring-2 focus:ring-purple-500"
                placeholder={`Story 1\nHey Leute! Ich habe heute etwas *Verrücktes* erlebt...\n\nStory 2\nHabt ihr das auch schon mal gehabt? (Poll)`}
              />
              <div className="flex justify-end">
                <button 
                  onClick={handleBulkGenerate}
                  className="px-6 py-2 bg-purple-600 text-white font-bold rounded-lg hover:bg-purple-700 flex items-center"
                >
                  <SafeIcon icon={FiPlay} className="mr-2" /> Generate Stories
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* GRID VIEW (Vertical Cards) */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
        {stories.map((slide, index) => (
          <motion.div 
            key={index} 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow group relative"
          >
            <div className="aspect-[9/16] w-full bg-gray-100 relative cursor-pointer" onClick={() => handleEditSlide(index)}>
              {/* FORCE RENDER ON CONFIG CHANGE */}
              <Canvas 
                key={`${brandSettings.currentBrandConfig.colors.primary}-${brandSettings.currentBrandConfig.typography.fontFamily}`}
                data={{
                  ...slide,
                  // Ensure dynamic updates from global config apply if not overridden
                  fontFamily: brandSettings.currentBrandConfig.typography.fontFamily,
                  accentFontFamily: brandSettings.currentBrandConfig.typography.accentFontFamily,
                  color: brandSettings.currentBrandConfig.colors.primary,
                  backgroundColor: brandSettings.currentBrandConfig.colors.background,
                  accentColor: brandSettings.currentBrandConfig.colors.accent,
                  secondaryColor: brandSettings.currentBrandConfig.colors.secondary,
                }} 
                width={400} 
                height={711} 
                brandName={brandName} 
              />
              <div className="absolute top-2 left-2 bg-black/50 text-white text-[10px] px-2 py-0.5 rounded font-bold">
                {index + 1}
              </div>
              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <div className="bg-white text-gray-800 px-3 py-1.5 rounded-lg font-bold text-xs shadow-lg flex items-center">
                  <SafeIcon icon={FiEdit3} className="mr-2" /> Edit
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default StoryPlanner;