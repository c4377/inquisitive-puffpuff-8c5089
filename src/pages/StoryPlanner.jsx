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
import { getBufferChannels, sendToBuffer } from '../utils/bufferClient';
import { attachSmartImages } from '../utils/smartLayoutGenerator';
import { decidePostDesign, dayHasImage } from '../utils/postDesignEngine';

const { FiSmartphone, FiDownload, FiRefreshCw, FiLayers, FiFileText, FiX, FiPlay, FiTrash2, FiEdit3, FiPlus, FiSend, FiMessageSquare } = FiIcons;

const StoryPlanner = () => {
  const { brandSettings, updateBrandSettings, dataLoaded } = useBrand();
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showBulkInput, setShowBulkInput] = useState(false);
  const [bulkText, setBulkText] = useState('');
  const [showShifter, setShowShifter] = useState(false);

  // --- Buffer (send stories to Buffer as Instagram Stories) ---
  const [showBuffer, setShowBuffer] = useState(false);
  const [bufferChannels, setBufferChannels] = useState([]);
  const [selectedChannel, setSelectedChannel] = useState('');
  const [bufferStatus, setBufferStatus] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [sendIndex, setSendIndex] = useState(null); // which story is being sent

  const loadBufferChannels = async () => {
    setBufferStatus('Lade Kanäle…');
    try {
      const channels = await getBufferChannels();
      setBufferChannels(channels);
      const ig = channels.find(c => (c.service || '').toLowerCase().includes('instagram'));
      setSelectedChannel(ig?.id || channels[0]?.id || '');
      setBufferStatus(channels.length ? '' : 'Keine Kanäle gefunden.');
    } catch (e) {
      setBufferStatus(e.message || 'Fehler beim Laden der Kanäle.');
    }
  };

  const sendStoryToBuffer = async (slide, index, mode) => {
    const imageUrl = (typeof slide?.background === 'string' && slide.background.startsWith('http'))
      ? slide.background : null;
    if (!selectedChannel) { setBufferStatus('Bitte zuerst einen Kanal wählen.'); return; }
    if (!imageUrl) { setBufferStatus(`Story ${index + 1}: braucht ein öffentliches Bild (Cloud-Upload).`); return; }
    const chan = bufferChannels.find(c => c.id === selectedChannel);
    setIsSending(true);
    setSendIndex(index);
    setBufferStatus(`Story ${index + 1} wird gesendet…`);
    try {
      await sendToBuffer({
        channelId: selectedChannel,
        text: slide.caption || '',
        imageUrl,
        mode,
        service: chan?.service || '',
        igType: 'story',
      });
      setBufferStatus(`✓ Story ${index + 1} ${mode === 'draft' ? 'als Entwurf gespeichert' : 'in die Queue gelegt'}.`);
    } catch (e) {
      setBufferStatus('Fehler: ' + (e.message || 'Senden fehlgeschlagen.'));
    } finally {
      setIsSending(false);
      setSendIndex(null);
    }
  };

  const sendAllStories = async (mode) => {
    if (!selectedChannel) { setBufferStatus('Bitte zuerst einen Kanal wählen.'); return; }
    for (let i = 0; i < stories.length; i++) {
      // eslint-disable-next-line no-await-in-loop
      await sendStoryToBuffer(stories[i], i, mode);
    }
    setBufferStatus(`✓ Alle ${stories.length} Stories gesendet.`);
  };

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

    // Split by "Story 1" / "Slide 1" / "Sequenz 1" markers (same as before).
    let slideTexts = bulkText.split(/(?:Story|Slide|Sequenz)\s*\d+\s*[:.-]?/i).filter(t => t.trim().length > 0);
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
      try { slides = await attachSmartImages(slides, imagePool, 0); } catch (e) { /* keep */ }
    }

    // Apply the design engine per slide: position by quiet zone / rotation, bold every 4th.
    slides = slides.map((slide, index) => {
      const hasImg = typeof slide.background === 'string' && slide.background.length > 5;
      if (!hasImg) {
        const { background, overlay, _autoImage, ...rest } = slide;
        slide = { ...rest, background: null };
      }
      const { textAnchor, bold } = decidePostDesign({
        globalIndex: index, hasImage: hasImg, autoImage: slide._autoImage,
      });
      return { ...slide, textAnchor, fontWeight: bold ? '700' : 'normal' };
    });

    setStories(slides);
    setShowBulkInput(false);
    setBulkText('');
    setLoading(false);
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
          <button onClick={() => { setShowBuffer(!showBuffer); if (!showBuffer && bufferChannels.length === 0) loadBufferChannels(); }} className={`flex items-center px-4 py-2 border rounded-lg text-sm font-bold transition-colors ${showBuffer ? 'bg-pink-100 border-pink-300 text-pink-700' : 'bg-white border-gray-200 text-gray-600'}`} >
            <SafeIcon icon={FiSend} className="mr-2" /> An Buffer
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

      {/* BUFFER PANEL (send stories as Instagram Stories) */}
      <AnimatePresence>
        {showBuffer && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="mb-8 overflow-hidden">
            <div className="bg-white border-2 border-pink-100 rounded-xl p-5 shadow-sm max-w-2xl">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-bold text-gray-900 flex items-center"><SafeIcon icon={FiSend} className="mr-2 text-pink-600" /> Stories an Buffer senden</h3>
                <button onClick={loadBufferChannels} className="text-[12px] text-gray-500 hover:text-pink-600 flex items-center"><SafeIcon icon={FiRefreshCw} className="mr-1" /> Kanäle neu laden</button>
              </div>
              <div className="flex flex-col sm:flex-row gap-2 mb-3">
                <select
                  value={selectedChannel}
                  onChange={(e) => setSelectedChannel(e.target.value)}
                  className="flex-1 border border-gray-200 rounded-lg p-2 text-sm bg-white outline-none focus:border-pink-400"
                >
                  {bufferChannels.length === 0 && <option value="">Keine Kanäle geladen</option>}
                  {bufferChannels.map(c => (
                    <option key={c.id} value={c.id}>{(c.displayName || c.name)} ({c.service})</option>
                  ))}
                </select>
                <div className="flex gap-2">
                  <button onClick={() => sendAllStories('draft')} disabled={isSending || !selectedChannel} className="px-3 py-2 rounded-lg text-xs font-bold border border-gray-200 text-gray-700 hover:bg-gray-50 disabled:opacity-50">Alle als Entwurf</button>
                  <button onClick={() => sendAllStories('addToQueue')} disabled={isSending || !selectedChannel} className="px-3 py-2 rounded-lg text-xs font-bold bg-pink-600 text-white hover:bg-pink-700 disabled:opacity-50 flex items-center"><SafeIcon icon={FiSend} className="mr-1" /> Alle in Queue</button>
                </div>
              </div>
              {bufferStatus && <p className="text-[12px] text-gray-600">{bufferStatus}</p>}
              <p className="text-[11px] text-gray-400 mt-1">Sendet als Instagram-Story. Jede Story braucht ein öffentliches Bild (Cloud-Upload). Du kannst unten auch einzelne Stories senden.</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
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
              <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-2">
                <div className="bg-white text-gray-800 px-3 py-1.5 rounded-lg font-bold text-xs shadow-lg flex items-center">
                  <SafeIcon icon={FiEdit3} className="mr-2" /> Edit
                </div>
                {showBuffer && selectedChannel && (
                  <button
                    onClick={(e) => { e.stopPropagation(); sendStoryToBuffer(slide, index, 'addToQueue'); }}
                    disabled={isSending}
                    className="bg-pink-600 text-white px-3 py-1.5 rounded-lg font-bold text-xs shadow-lg flex items-center hover:bg-pink-700 disabled:opacity-50"
                  >
                    <SafeIcon icon={FiSend} className="mr-1.5" /> {sendIndex === index ? 'Sende…' : 'Story senden'}
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default StoryPlanner;