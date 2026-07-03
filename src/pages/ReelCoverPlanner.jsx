import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import * as FiIcons from 'react-icons/fi';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import { fabric } from 'fabric';
import SafeIcon from '../common/SafeIcon';
import Canvas from '../components/Canvas';
import StyleShifter from '../components/StyleShifter'; // IMPORT NEW SHIFTER
import { useBrand } from '../context/BrandContext';
import { renderSlide } from '../utils/canvasRenderer';
import { attachSmartImages } from '../utils/smartLayoutGenerator';
import { decidePostDesign, dayHasImage } from '../utils/postDesignEngine';
import { saveReelCoverSetsToDB, loadReelCoverSetsFromDB } from '../utils/storage';

const { FiSmartphone, FiDownload, FiRefreshCw, FiLayers, FiFileText, FiX, FiPlay, FiTrash2, FiEdit3, FiPlus, FiCopy, FiCheck, FiImage, FiShuffle, FiZoomIn, FiZoomOut, FiGrid } = FiIcons;

const ReelCoverPlanner = () => {
  const { brandSettings, updateBrandSettings, dataLoaded } = useBrand();
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showBulkInput, setShowBulkInput] = useState(false);
  const [bulkText, setBulkText] = useState('');
  const [showShifter, setShowShifter] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);
  const lastOffsetRef = useRef(0);
  const [storySets, setStorySets] = useState([]);
  const [showLibrary, setShowLibrary] = useState(false);
  const [setName, setSetName] = useState('');

  // Random image-pool offset that differs from the previous one, so a reload
  // actually shows different images instead of the same ones every time.
  const nextOffset = (poolLen) => {
    if (poolLen <= 1) return 0;
    let off = Math.floor(Math.random() * poolLen);
    if (off === lastOffsetRef.current) off = (off + 1 + Math.floor(Math.random() * (poolLen - 1))) % poolLen;
    lastOffsetRef.current = off;
    return off;
  };

  // Re-attach fresh pool images to all existing stories (texts stay).
  // Cards that are deliberately image-free (_noImage) stay image-free.
  const handleReshuffleImages = async () => {
    const pool = brandSettings?.brandImages || [];
    if (pool.length === 0) {
      alert('Kein Bild im Pool. Lade zuerst Bilder hoch.');
      return;
    }
    if (stories.length === 0) return;
    setLoading(true);
    try {
      const offset = nextOffset(pool.length);
      let slides = await attachSmartImages(
        stories.map(s => ({ ...s, layout: 'auto', layoutId: 'auto' })), pool, offset
      );
      slides = slides.map((slide) => {
        if (slide._noImage) {
          const { background, overlay, _autoImage, ...rest } = slide;
          return { ...rest, background: null, _noImage: true };
        }
        return slide;
      });
      setStories(slides);
    } catch (e) {
      console.error('Bilder neu laden fehlgeschlagen:', e);
    } finally {
      setLoading(false);
    }
  };

  const brandName = brandSettings.currentBrandConfig?.name || "MUSE MENTORING";

  // Initialize with one empty story if nothing exists
  // Load saved story sets once.
  useEffect(() => {
    loadReelCoverSetsFromDB().then(sets => setStorySets(Array.isArray(sets) ? sets : []));
  }, []);

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
      reelCoverMode: true,
      text: "Neues Reel Cover",
      fontSize: 36,
      fontFamily: brandConfig?.typography?.fontFamily || 'Inter',
      accentFontFamily: brandConfig?.typography?.accentFontFamily,
      fontWeight: '400',
      color: brandConfig?.colors?.primary || '#000000',
      backgroundColor: brandConfig?.colors?.background || '#FFFFFF',
      secondaryColor: brandConfig?.colors?.secondary || '#CCCCCC',
      accentColor: brandConfig?.colors?.accent || '#EA580C',
      layout: 'auto', // story mode styling (handwritten, lower third)
      layoutId: 'auto',
      textAlign: 'center',
      visualElements: [],
      imageScale: 1,
      slideNumber: stories.length + 1,
      totalSlides: stories.length + 1
    };
    setStories(prev => [...prev, newStory]);
  };

  // --- STORY LIBRARY: save / load / delete named sequences ---
  const handleSaveSet = async () => {
    const name = setName.trim() || `Cover-Set ${new Date().toLocaleDateString('de-AT')}`;
    if (stories.length === 0) return;
    const newSet = { id: Date.now(), name, createdAt: new Date().toISOString(), stories };
    const updated = [newSet, ...storySets];
    setStorySets(updated);
    setSetName('');
    await saveReelCoverSetsToDB(updated);
  };

  const handleLoadSet = (set) => {
    if (!set?.stories?.length) return;
    if (stories.length > 1 && !window.confirm(`"${set.name}" laden? Die aktuellen Cover werden ersetzt.`)) return;
    setStories(set.stories);
    setShowLibrary(false);
  };

  const handleDeleteSet = async (id) => {
    if (!window.confirm('Dieses gespeicherte Cover-Set löschen?')) return;
    const updated = storySets.filter(s => s.id !== id);
    setStorySets(updated);
    await saveReelCoverSetsToDB(updated);
  };

  // --- CARD IMAGE ACTIONS: separate Zoom / Entfernen / Bild rein ---
  const handleCycleLayout = (index) => {
    setStories(prev => prev.map((s, i) => {
      if (i !== index) return s;
      const current = Number.isInteger(s.coverVariant) ? s.coverVariant : (i % 4);
      return { ...s, coverVariant: (current + 1) % 4 };
    }));
  };

  const handleZoomToggle = (index) => {
    setStories(prev => prev.map((s, i) => {
      if (i !== index) return s;
      const zoomed = (s.imageScale || 1) > 1.05;
      return { ...s, imageScale: zoomed ? 1 : 1.5 };
    }));
  };

  const handleRemoveImage = (index) => {
    setStories(prev => prev.map((s, i) => {
      if (i !== index) return s;
      const { background, overlay, _autoImage, ...rest } = s;
      return { ...rest, background: null, imageScale: 1, _noImage: true };
    }));
  };

  const handleAddImage = async (index) => {
    const slide = stories[index];
    const pool = brandSettings?.brandImages || [];
    if (pool.length === 0) {
      alert('Kein Bild im Pool. Lade zuerst Bilder hoch.');
      return;
    }
    try {
      const offset = Math.floor(Math.random() * pool.length);
      const [withImg] = await attachSmartImages(
        [{ ...slide, layout: 'auto', layoutId: 'auto' }], pool, offset
      );
      setStories(prev => prev.map((s, i) => (i === index ? { ...withImg, imageScale: 1, _noImage: false } : s)));
    } catch (e) {
      console.error('Bild anhängen fehlgeschlagen:', e);
    }
  };

  const handleEditSlide = (index) => {
    navigate('/editor', { 
      state: { 
        slides: stories.map(s => ({ ...s, reelCoverMode: true })), 
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
        .split(/(?:Cover|Story|Slide|Sequenz)\s*\d+\s*[:.-]?/i)
        .map(t => t
          // remove divider lines (⸻, ---, ___) and BLOCK section headers
          .replace(/^\s*[⸻—\-_]{2,}\s*$/gm, '')
          .replace(/^\s*BLOCK\s*\d+.*$/gim, '')
          .replace(/[⸻]/g, '')
          .trim()
        )
        .filter(t => t.length > 0);
      if (slideTexts.length === 0) slideTexts.push(bulkText.trim());

      // Detect "(ohne Bild)" / "[kein Bild]" markers per story -> text-only page.
      const noImgRe = /[\(\[]\s*(?:ohne|kein)\s+bild\s*[\)\]]/i;
      const slideDefs = slideTexts.map(raw => ({
        noImage: noImgRe.test(raw),
        text: raw.replace(new RegExp(noImgRe, 'gi'), '').trim(),
      }));

      const brandConfig = brandSettings.currentBrandConfig;
      const imagePool = brandSettings?.brandImages || [];

      // Build base story slides (9:16), then run the SAME engine as the feed:
      // auto layout + pool images (variety) + text position/bold decisions.
      let slides = slideDefs.map(({ text, noImage }, index) => ({
        id: Date.now() + index,
        format: '9:16',
        reelCoverMode: true,
        text,
        _noImage: noImage,
        fontSize: 24,
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
        try { slides = await attachSmartImages(slides, imagePool, nextOffset(imagePool.length)); } catch (e) { /* keep text-only */ }
      }

      // Apply the design engine per slide: position by quiet zone / rotation, bold every 4th.
      slides = slides.map((slide, index) => {
        let s2 = { ...slide };
        // Explicit "(ohne Bild)" marker beats the auto-attached image.
        if (s2._noImage) {
          const { background, overlay, _autoImage, ...rest } = s2;
          s2 = { ...rest, background: null, _noImage: true };
        }
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

  // Render all story frames as PNG File objects (1080x1920).
  const renderStoryFiles = async () => {
    await document.fonts.ready;
    const files = [];
    for (let i = 0; i < stories.length; i++) {
      const canvasEl = document.createElement('canvas');
      canvasEl.width = 1080;
      canvasEl.height = 1920;
      canvasEl.style.position = 'fixed';
      canvasEl.style.left = '-99999px';
      document.body.appendChild(canvasEl);
      const fCanvas = new fabric.StaticCanvas(canvasEl, { width: 1080, height: 1920 });
      await renderSlide(fCanvas, { ...stories[i], reelCoverMode: true, showSafeZone: false }, 1080, 1920, {
        slideIndex: i,
        totalSlides: stories.length,
        scale: 1080 / 400,
        globalBrandName: brandName,
      });
      const dataUrl = fCanvas.toDataURL({ format: 'png', multiplier: 1 });
      const blob = await (await fetch(dataUrl)).blob();
      fCanvas.dispose();
      if (canvasEl.parentNode) canvasEl.parentNode.removeChild(canvasEl);
      files.push(new File([blob], `ReelCover_${i + 1}.png`, { type: 'image/png' }));
    }
    return files;
  };

  // iPhone: share sheet -> "Bilder sichern" legt alle Frames in die FOTOS.
  // Desktop/kein Share: ZIP als Fallback.
  const downloadDeck = async () => {
    if (stories.length === 0) return;
    setLoading(true);
    try {
      const files = await renderStoryFiles();
      if (typeof navigator !== 'undefined' && navigator.canShare && navigator.canShare({ files })) {
        try {
          await navigator.share({ files, title: 'Reel Cover' });
        } catch (e) {
          if (e?.name !== 'AbortError') throw e;
        }
      } else {
        const zip = new JSZip();
        const folder = zip.folder('Reel_Covers');
        files.forEach(f => folder.file(f.name, f));
        const contentZip = await zip.generateAsync({ type: 'blob' });
        saveAs(contentZip, 'Reel_Covers.zip');
      }
    } catch (e) {
      console.error('Story export failed:', e);
      alert('Export fehlgeschlagen. Bitte erneut versuchen.');
    } finally {
      setLoading(false);
    }
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Reel Cover Planner <span className="text-xs font-normal text-gray-400 align-middle">v2</span></h1>
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
          <button 
            onClick={handleReshuffleImages}
            disabled={loading}
            className="text-sm bg-gray-100 text-gray-700 px-3 py-1 rounded-lg font-bold hover:bg-gray-200 transition-colors flex items-center disabled:opacity-50"
          >
            <SafeIcon icon={FiShuffle} className="mr-1" /> Bilder neu
          </button>
          <button 
            onClick={() => setShowLibrary(!showLibrary)}
            className={`text-sm px-3 py-1 rounded-lg font-bold transition-colors flex items-center ${showLibrary ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
          >
            <SafeIcon icon={FiLayers} className="mr-1" /> Library
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
            <SafeIcon icon={FiDownload} className="mr-2" /> {loading ? 'Rendert...' : 'In Fotos sichern'}
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
                placeholder={`Cover 1\nRaten kostet. *Struktur* ersetzt das Raten.\n\nCover 2 (ohne Bild)\nDieses Cover nur mit Brand-Farbe.`}
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

      {/* STORY LIBRARY PANEL */}
      <AnimatePresence>
        {showLibrary && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="mb-8 overflow-hidden" >
            <div className="bg-white border-2 border-purple-100 rounded-xl p-6 shadow-sm">
              <div className="flex justify-between mb-4">
                <h3 className="text-sm font-bold text-gray-700">Cover Library</h3>
                <button onClick={() => setShowLibrary(false)}><SafeIcon icon={FiX} className="text-gray-400" /></button>
              </div>
              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  value={setName}
                  onChange={(e) => setSetName(e.target.value)}
                  placeholder="Name des Cover-Sets..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-purple-500"
                />
                <button
                  onClick={handleSaveSet}
                  disabled={stories.length === 0}
                  className="px-4 py-2 bg-purple-600 text-white text-sm font-bold rounded-lg hover:bg-purple-700 disabled:opacity-50"
                >
                  Speichern
                </button>
              </div>
              {storySets.length === 0 ? (
                <p className="text-sm text-gray-400">Noch keine gespeicherten Cover-Sets.</p>
              ) : (
                <div className="space-y-2">
                  {storySets.map(set => (
                    <div key={set.id} className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2">
                      <div>
                        <span className="text-sm font-bold text-gray-800">{set.name}</span>
                        <span className="text-xs text-gray-400 ml-2">
                          {set.stories?.length || 0} Slides · {new Date(set.createdAt).toLocaleDateString('de-AT')}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleLoadSet(set)}
                          className="text-xs bg-white border border-gray-300 px-3 py-1 rounded-lg font-bold text-gray-700 hover:bg-gray-100"
                        >
                          Laden
                        </button>
                        <button
                          onClick={() => handleDeleteSet(set.id)}
                          className="text-xs text-red-500 px-2 py-1 rounded-lg hover:bg-red-50"
                        >
                          <SafeIcon icon={FiTrash2} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
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
                  reelCoverMode: true,
                  showSafeZone: true,
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
              {/* Hover Overlay — compact icon buttons */}
              <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-1.5">
                <div className="bg-white text-gray-800 p-2 rounded-full shadow-lg flex items-center justify-center" title="Bearbeiten">
                  <SafeIcon icon={FiEdit3} className="text-sm" />
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigator.clipboard?.writeText(slide.text || '');
                    setCopiedIndex(index);
                    setTimeout(() => setCopiedIndex(null), 1500);
                  }}
                  title="Text kopieren"
                  className={`p-2 rounded-full shadow-lg flex items-center justify-center bg-white hover:text-purple-600 ${copiedIndex === index ? 'text-green-600' : 'text-gray-800'}`}
                >
                  <SafeIcon icon={copiedIndex === index ? FiCheck : FiCopy} className="text-sm" />
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); handleCycleLayout(index); }}
                  title="Layout wechseln"
                  className="bg-white text-gray-800 p-2 rounded-full shadow-lg flex items-center justify-center hover:text-purple-600"
                >
                  <SafeIcon icon={FiGrid} className="text-sm" />
                </button>
                {(typeof slide.background === 'string' && slide.background.length > 5) ? (
                  <>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleZoomToggle(index); }}
                      title={(slide.imageScale || 1) > 1.05 ? 'Zoom aus' : 'Zoom'}
                      className={`p-2 rounded-full shadow-lg flex items-center justify-center bg-white hover:text-purple-600 ${(slide.imageScale || 1) > 1.05 ? 'text-purple-600' : 'text-gray-800'}`}
                    >
                      <SafeIcon icon={(slide.imageScale || 1) > 1.05 ? FiZoomOut : FiZoomIn} className="text-sm" />
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleRemoveImage(index); }}
                      title="Bild entfernen"
                      className="bg-white text-red-500 p-2 rounded-full shadow-lg flex items-center justify-center hover:bg-red-50"
                    >
                      <SafeIcon icon={FiX} className="text-sm" />
                    </button>
                  </>
                ) : (
                  <button
                    onClick={(e) => { e.stopPropagation(); handleAddImage(index); }}
                    title="Bild einfügen"
                    className="bg-white text-gray-800 p-2 rounded-full shadow-lg flex items-center justify-center hover:text-purple-600"
                  >
                    <SafeIcon icon={FiImage} className="text-sm" />
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

export default ReelCoverPlanner;