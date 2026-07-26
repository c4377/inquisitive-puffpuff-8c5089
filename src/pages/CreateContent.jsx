import React, { useState, useRef, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import * as FiIcons from 'react-icons/fi';
import { fabric } from 'fabric'; // Added Fabric import
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import SafeIcon from '../common/SafeIcon';
import Canvas from '../components/Canvas';
import { useSwipe } from '../hooks/useSwipe';
import TextEditor from '../components/TextEditor';
import BulkTextEditor from '../components/BulkTextEditor';
import ImageUpload from '../components/ImageUpload';
import FormatSelector from '../components/FormatSelector';
import LayoutPicker from '../components/LayoutPicker';
import ColorEditor from '../components/ColorEditor';
import GenerativeBrandSystem from '../components/GenerativeBrandSystem';
import StyleShifter from '../components/StyleShifter';
import ImageEffects from '../components/ImageEffects';
import { useBrand } from '../context/BrandContext';
import { renderSlide } from '../utils/canvasRenderer';

const { FiPlus, FiDownload, FiTrash2, FiFolder, FiSave, FiArrowLeft, FiType, FiLayout, FiDroplet, FiImage, FiMove, FiList, FiZap, FiGrid, FiToggleRight, FiToggleLeft } = FiIcons;

const ToolTab = ({ id, label, icon, isActive, onClick }) => (
  <button onClick={() => onClick(id)} className={`w-full flex flex-col items-center justify-center py-4 px-1 transition-all border-l-4 ${isActive ? 'bg-purple-50 border-purple-600 text-purple-700' : 'bg-white border-transparent text-gray-500 hover:bg-gray-50 hover:text-gray-900'}`}>
    <SafeIcon icon={icon} className={`text-2xl mb-1 ${isActive ? 'text-purple-600' : 'text-gray-400'}`} />
    <span className="text-[10px] font-bold uppercase tracking-wider">{label}</span>
  </button>
);

const CreateContent = () => {
  const { brandSettings, saveDesignToLibrary, deleteDesignFromLibrary } = useBrand();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const mainCanvasRef = useRef();
  const thumbnailsRef = useRef(null);

  const [activeTab, setActiveTab] = useState('text');
  const [isExporting, setIsExporting] = useState(false);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [applyToAll, setApplyToAll] = useState(false);
  const [showSavedDesigns, setShowSavedDesigns] = useState(false);

  const selectedLayout = searchParams.get('layout');

  // If the ACTIVE brand is an editorial preset, new slides must carry its
  // flags and the adaptive 'auto' layout — otherwise they render through a
  // generic layout and look like a different brand.
  const _cfg = brandSettings.currentBrandConfig || {};
  const _editorialActive = _cfg.editorialDark === true || _cfg.ruleSet === 'editorial_dark';

  const [slides, setSlides] = useState([{
      id: 1,
      format: '4:5',
      background: null,
      text: brandSettings.currentBrandConfig?.sampleText || 'Your Headline',
      fontSize: 48,
      fontFamily: brandSettings.currentBrandConfig?.typography?.fontFamily || 'Inter',
      accentFontFamily: brandSettings.currentBrandConfig?.typography?.accentFontFamily || brandSettings.currentBrandConfig?.typography?.fontFamily || 'Inter',
      color: brandSettings.currentBrandConfig?.colors?.primary || '#000000',
      backgroundColor: brandSettings.currentBrandConfig?.colors?.background || '#FFFFFF',
      secondaryColor: brandSettings.currentBrandConfig?.colors?.secondary || '#D6D3CD',
      accentColor: brandSettings.currentBrandConfig?.colors?.accent || '#EA580C',
      overlay: _editorialActive ? undefined : 0.2, blur: 0, grain: 0,
      layout: _editorialActive ? 'auto' : (selectedLayout || brandSettings.currentBrandConfig?.layout || 'minimal-center'),
      layoutId: _editorialActive ? 'auto' : undefined,
      editorialDark: _editorialActive || undefined,
      darkPhoto: _editorialActive ? (_cfg.darkPhoto === true || undefined) : undefined,
      visualElements: brandSettings.currentBrandConfig?.visualElements || [],
      imageScale: 1, imageX: 0, imageY: 0,
      overlayImage: null, overlayImageScale: 0.3, overlayImageX: 0, overlayImageY: 0, overlayImageRounded: false
  }]);

  const currentSlide = slides[currentSlideIndex] || slides[0];

  const slideSwipe = useSwipe({
    onLeft: () => setCurrentSlideIndex((i) => Math.min(slides.length - 1, i + 1)),
    onRight: () => setCurrentSlideIndex((i) => Math.max(0, i - 1)),
  });

  useEffect(() => {
    if (thumbnailsRef.current) {
      const activeThumb = thumbnailsRef.current.children[currentSlideIndex];
      if (activeThumb) activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }, [currentSlideIndex]);

  useEffect(() => {
    if (activeTab === 'brand' && brandSettings.currentBrandConfig) {
      const newConfig = brandSettings.currentBrandConfig;
      const updates = {
        fontFamily: newConfig.typography.fontFamily,
        accentFontFamily: newConfig.typography.accentFontFamily || newConfig.typography.fontFamily,
        color: newConfig.colors.primary,
        backgroundColor: newConfig.colors.background,
        secondaryColor: newConfig.colors.secondary,
        accentColor: newConfig.colors.accent,
      };
      handleGlobalUpdate(updates);
    }
  }, [brandSettings.currentBrandConfig, activeTab]);

  const handleSlideUpdate = (updates) => setSlides(prev => prev.map((slide, idx) => idx === currentSlideIndex ? { ...slide, ...updates } : slide));
  const handleGlobalUpdate = (updates) => setSlides(prev => prev.map(slide => ({ ...slide, ...updates })));
  const handleBatchUpdate = (updates, scope = 'all') => setSlides(prev => prev.map((slide, idx) => {
      if (scope === 'all') return { ...slide, ...updates };
      if (scope === 'body') return idx > 0 ? { ...slide, ...updates } : slide;
      if (scope === 'current') return idx === currentSlideIndex ? { ...slide, ...updates } : slide;
      return slide;
  }));
  const handleSmartUpdate = (updates) => applyToAll ? handleGlobalUpdate(updates) : handleSlideUpdate(updates);

  const handleBrandConfigUpdate = (newConfig) => {
    const updates = {
      fontFamily: newConfig.typography.fontFamily,
      accentFontFamily: newConfig.typography.accentFontFamily || newConfig.typography.fontFamily,
      color: newConfig.colors.primary,
      backgroundColor: newConfig.colors.background,
      secondaryColor: newConfig.colors.secondary,
      accentColor: newConfig.colors.accent,
      visualElements: newConfig.visualElements,
    };
    handleGlobalUpdate(updates);
  };

  const addSlide = () => {
    const lastSlide = slides[slides.length - 1];
    setSlides([...slides, { ...lastSlide, id: Date.now(), text: 'New Slide', background: null, imageScale: 1, imageX: 0, imageY: 0 }]);
    setCurrentSlideIndex(slides.length);
  };

  const deleteSlide = () => {
    if (slides.length > 1) {
      const newSlides = slides.filter((_, idx) => idx !== currentSlideIndex);
      setSlides(newSlides);
      setCurrentSlideIndex(Math.max(0, currentSlideIndex - 1));
    }
  };

  const handleBulkUpdate = (newSlides) => {
    setSlides(newSlides);
    setCurrentSlideIndex(0);
  };

  const downloadAllSlides = async () => {
    setIsExporting(true);
    try {
      const zip = new JSZip();
      const slidesFolder = zip.folder("slides");
      const globalBrandName = brandSettings.currentBrandConfig?.brandText || "";

      for (let i = 0; i < slides.length; i++) {
        const slide = slides[i];
        
        // Fabric Export Logic
        const canvasEl = document.createElement('canvas');
        let renderW = 1080;
        let renderH = 1350;
        let baseWidth = 400; // Default base for scale calc

        if (slide.format === '16:9') { renderW = 1920; renderH = 1080; baseWidth = 960; }
        else if (slide.format === '9:16') { renderW = 1080; renderH = 1920; baseWidth = 400; }
        else if (slide.format === '1:1') { renderW = 1080; renderH = 1080; baseWidth = 500; }
        
        const scale = renderW / baseWidth;
        const fCanvas = new fabric.StaticCanvas(canvasEl, { width: renderW, height: renderH });

        await renderSlide(fCanvas, slide, renderW, renderH, {
          slideIndex: i,
          totalSlides: slides.length,
          scale: scale,
          globalBrandName: globalBrandName
        });

        const dataUrl = fCanvas.toDataURL({ format: 'png', multiplier: 1 });
        const blob = await (await fetch(dataUrl)).blob();
        slidesFolder.file(`slide-${String(i + 1).padStart(3, '0')}.png`, blob);
        fCanvas.dispose();
      }

      const content = await zip.generateAsync({ type: 'blob' });
      saveAs(content, `slides-export-${new Date().toISOString().slice(0, 10)}.zip`);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export fehlgeschlagen.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleSaveToLibrary = () => {
    if (slides.length > 1) {
      const collection = {
        isCollection: true,
        slides: slides,
        background: slides[0].background,
        backgroundColor: slides[0].backgroundColor,
        color: slides[0].color,
        text: `[${slides.length} Slides] ${slides[0].text}`,
        id: Date.now(),
      };
      saveDesignToLibrary(collection);
    } else {
      saveDesignToLibrary(currentSlide);
    }
    const btn = document.getElementById('save-lib-btn');
    if (btn) {
      const originalText = btn.innerHTML;
      btn.innerHTML = `<span class="flex items-center">Saved!</span>`;
      setTimeout(() => { btn.innerHTML = originalText; }, 2000);
    }
  };

  const loadDesign = (design) => {
    if (design.isCollection && design.slides) {
      const restoredSlides = design.slides.map((s, i) => ({ ...s, id: Date.now() + i }));
      setSlides(restoredSlides);
      setCurrentSlideIndex(0);
    } else {
      const loadedSlide = { ...design, id: Date.now() };
      setSlides(prev => {
        const newSlides = [...prev];
        newSlides[currentSlideIndex] = loadedSlide;
        return newSlides;
      });
    }
    setShowSavedDesigns(false);
  };

  const brandName = brandSettings.currentBrandConfig?.name || "";

  return (
    <div className="flex flex-col bg-gray-50 h-[calc(100vh-64px)] overflow-hidden">
      <div className="h-16 bg-white border-b border-gray-200 px-4 flex items-center justify-between shadow-sm flex-shrink-0 z-30">
        <button onClick={() => navigate(-1)} className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"><SafeIcon icon={FiArrowLeft} /></button>
        <div className="flex space-x-2 items-center">
          <button onClick={() => setShowSavedDesigns(!showSavedDesigns)} className={`p-2 rounded-lg font-bold text-xs flex items-center transition-colors ${showSavedDesigns ? 'bg-gray-200 text-gray-900' : 'text-gray-600 hover:bg-gray-100'}`}><SafeIcon icon={FiFolder} className="text-lg mr-1" /><span className="hidden sm:inline">Bibliothek</span></button>
          <button onClick={downloadAllSlides} disabled={isExporting || slides.length === 0} className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold shadow-md hover:bg-blue-700 disabled:opacity-50"><SafeIcon icon={FiDownload} className="mr-1" />{isExporting ? 'Exporting...' : slides.length > 1 ? `Alle (${slides.length})` : 'Export'}</button>
        </div>
      </div>
      <AnimatePresence>
        {showSavedDesigns && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="bg-gray-100 border-b border-gray-200 overflow-hidden flex-shrink-0 z-20"><div className="p-4"><div className="flex space-x-4 overflow-x-auto pb-2 no-scrollbar">{brandSettings.savedDesigns?.map(design => (<div key={design.id} className="flex-shrink-0 w-24 cursor-pointer" onClick={() => loadDesign(design)}><div className="w-24 h-32 bg-white rounded border border-gray-300" style={{ backgroundColor: design.backgroundColor }}></div><div className="text-[10px] mt-1 truncate">{design.text}</div><button onClick={(e) => { e.stopPropagation(); deleteDesignFromLibrary(design.id) }} className="text-red-500 text-[10px]">Löschen</button></div>))}</div></div></motion.div>
        )}
      </AnimatePresence>
      <div className="flex-1 overflow-hidden grid grid-cols-1 md:grid-cols-[1fr_420px]">
        <div className="relative bg-gray-100 flex flex-col items-center justify-center p-4 md:p-8 overflow-y-auto">
          <div {...(slides.length > 1 ? slideSwipe : {})} className={`shadow-2xl rounded-sm overflow-hidden bg-white w-full transition-all duration-300 relative shrink-0 ${currentSlide.format === '9:16' ? 'max-w-[280px] aspect-[9/16]' : (currentSlide.format === '16:9' ? 'max-w-[800px] aspect-video' : 'max-w-[400px] aspect-[4/5]')}`}>
            <Canvas ref={mainCanvasRef} data={{...currentSlide, slideNumber: slides.length > 1 ? currentSlideIndex + 1 : undefined, totalSlides: slides.length}} brandName={brandName} />
            <button id="save-lib-btn" onClick={handleSaveToLibrary} className="absolute bottom-4 right-4 bg-white/90 backdrop-blur border border-gray-200 shadow-lg text-gray-700 px-3 py-1.5 rounded-lg text-xs font-bold flex items-center hover:bg-white hover:text-purple-600 transition-colors"><SafeIcon icon={FiSave} className="mr-1" /> Save</button>
          </div>
          <div className="mt-8 w-full max-w-2xl bg-white rounded-xl shadow-sm border border-gray-200 p-3 flex space-x-3 overflow-x-auto no-scrollbar" ref={thumbnailsRef}>
            {slides.map((slide, idx) => (
              <div key={slide.id} onClick={() => setCurrentSlideIndex(idx)} className={`flex-shrink-0 w-16 h-20 rounded border overflow-hidden relative cursor-pointer transition-all ${currentSlideIndex === idx ? 'border-purple-600 ring-4 ring-purple-100 opacity-100 transform scale-105' : 'border-gray-200 opacity-60 hover:opacity-100'}`}>
                <div className="w-full h-full bg-gray-50 flex items-center justify-center text-sm font-bold text-gray-400">{idx + 1}</div>
                {slides.length > 1 && currentSlideIndex === idx && (<button onClick={(e) => { e.stopPropagation(); deleteSlide(); }} className="absolute top-0 right-0 bg-red-500 text-white p-1.5 rounded-bl shadow-sm hover:bg-red-600 z-10"><SafeIcon icon={FiTrash2} className="text-[10px]" /></button>)}
              </div>
            ))}
            <button onClick={addSlide} className="flex-shrink-0 w-16 h-20 border-2 border-dashed border-gray-300 rounded flex items-center justify-center text-gray-400 hover:text-purple-600 hover:border-purple-600 hover:bg-purple-50 transition-colors"><SafeIcon icon={FiPlus} className="text-xl" /></button>
          </div>
        </div>
        <div className="flex h-full border-l border-gray-200 bg-white overflow-hidden">
          <div className="w-20 bg-white border-r border-gray-100 flex flex-col items-center py-2 overflow-y-auto no-scrollbar z-10 shadow-[4px_0_10px_rgba(0,0,0,0.02)]">
            <ToolTab id="text" label="Text" icon={FiType} isActive={activeTab === 'text'} onClick={setActiveTab} />
            <ToolTab id="layout" label="Layout" icon={FiLayout} isActive={activeTab === 'layout'} onClick={setActiveTab} />
            <ToolTab id="colors" label="Farben" icon={FiDroplet} isActive={activeTab === 'colors'} onClick={setActiveTab} />
            <ToolTab id="images" label="Bilder" icon={FiImage} isActive={activeTab === 'images'} onClick={setActiveTab} />
            <ToolTab id="effects" label="Effekte" icon={FiMove} isActive={activeTab === 'effects'} onClick={setActiveTab} />
            <ToolTab id="format" label="Format" icon={FiGrid} isActive={activeTab === 'format'} onClick={setActiveTab} />
            <div className="w-8 h-px bg-gray-200 my-2"></div>
            <ToolTab id="brand" label="Magic" icon={FiZap} isActive={activeTab === 'brand'} onClick={setActiveTab} />
            <ToolTab id="bulk" label="Bulk" icon={FiList} isActive={activeTab === 'bulk'} onClick={setActiveTab} />
          </div>
          <div className="flex-1 overflow-y-auto bg-gray-50/50 relative">
            <div className="p-5 min-h-full pb-20">
              <div className="mb-6 flex items-center justify-between border-b border-gray-100 pb-4">
                <h3 className="text-lg font-bold text-gray-900 capitalize flex items-center">
                  {activeTab === 'text' && <><SafeIcon icon={FiType} className="mr-2 text-purple-600"/> Text & Inhalt</>}
                  {activeTab === 'layout' && <><SafeIcon icon={FiLayout} className="mr-2 text-purple-600"/> Design Style</>}
                  {activeTab === 'colors' && <><SafeIcon icon={FiDroplet} className="mr-2 text-purple-600"/> Farb-Palette</>}
                  {activeTab === 'images' && <><SafeIcon icon={FiImage} className="mr-2 text-purple-600"/> Uploads & Assets</>}
                  {activeTab === 'effects' && <><SafeIcon icon={FiMove} className="mr-2 text-purple-600"/> Position & Filter</>}
                  {activeTab === 'format' && <><SafeIcon icon={FiGrid} className="mr-2 text-purple-600"/> Bildformat</>}
                  {activeTab === 'brand' && <><SafeIcon icon={FiZap} className="mr-2 text-purple-600"/> Brand Generator</>}
                  {activeTab === 'bulk' && <><SafeIcon icon={FiList} className="mr-2 text-purple-600"/> Massen-Editor</>}
                </h3>
              </div>
              <div className="animate-fade-in">
                {activeTab === 'text' && (<TextEditor currentSlide={currentSlide} onUpdate={handleSlideUpdate} onGlobalUpdate={handleGlobalUpdate} onBatchUpdate={handleBatchUpdate} totalSlides={slides.length} />)}
                {activeTab === 'layout' && (<><div className="mb-4 flex items-center justify-between bg-purple-50 p-3 rounded-lg border border-purple-100"><span className="text-xs font-bold text-purple-900 flex items-center">{applyToAll ? 'Gilt für ALLE Slides' : 'Nur aktueller Slide'}</span><button onClick={() => setApplyToAll(!applyToAll)} className={`text-[10px] px-2 py-1 rounded font-bold transition-colors ${applyToAll ? 'bg-purple-600 text-white' : 'bg-white border border-gray-300 text-gray-600'}`} ><SafeIcon icon={applyToAll ? FiToggleRight : FiToggleLeft} className="mr-1 inline text-sm"/> Wechseln</button></div><LayoutPicker currentLayout={currentSlide.layout} onUpdate={(updates) => handleSmartUpdate(updates)} /></>)}
                {activeTab === 'colors' && (<ColorEditor currentSlide={currentSlide} onUpdate={handleSlideUpdate} onGlobalUpdate={handleGlobalUpdate} />)}
                {activeTab === 'images' && (<><div className="mb-4 flex items-center justify-between"><span className="text-xs text-gray-500 font-medium">Bilder werden {applyToAll ? 'überall' : 'lokal'} angewendet</span><button onClick={() => setApplyToAll(!applyToAll)} className={`text-[10px] px-2 py-1 rounded font-bold transition-colors ${applyToAll ? 'bg-purple-100 text-purple-700' : 'bg-gray-200 text-gray-600'}`}>{applyToAll ? 'Alle' : 'Einzeln'}</button></div><ImageUpload onImageSelect={(image) => { if (applyToAll) { handleGlobalUpdate({ background: image }); } else { handleSlideUpdate({ background: image }); } }} onOverlaySelect={(image) => { if (applyToAll) { handleGlobalUpdate({ overlayImage: image }); } else { handleSlideUpdate({ overlayImage: image }); } }} currentOverlay={currentSlide.overlayImage} /></>)}
                {activeTab === 'effects' && (<ImageEffects overlay={currentSlide.overlay} blur={currentSlide.blur} grain={currentSlide.grain} brownTone={currentSlide.brownTone} imageScale={currentSlide.imageScale} imageX={currentSlide.imageX} imageY={currentSlide.imageY} overlayImageScale={currentSlide.overlayImageScale} overlayImageX={currentSlide.overlayImageX} overlayImageY={currentSlide.overlayImageY} overlayImageRounded={currentSlide.overlayImageRounded} onUpdate={(updates) => { if (applyToAll) { handleGlobalUpdate(updates); } else { handleSlideUpdate(updates); } }} />)}
                {activeTab === 'format' && (<FormatSelector format={currentSlide.format} onUpdate={handleGlobalUpdate} />)}
                {activeTab === 'bulk' && (<BulkTextEditor onUpdateSlides={handleBulkUpdate} currentSlides={slides} onGlobalUpdate={handleGlobalUpdate} />)}
                {activeTab === 'brand' && (<div className="space-y-6"><GenerativeBrandSystem compact={true} onGenerate={handleBrandConfigUpdate} /><div className="border-t border-gray-100 pt-6"><h4 className="text-xs font-bold text-gray-500 uppercase mb-3">Style Shifter</h4><StyleShifter compact={true} /><p className="text-[10px] text-gray-400 mt-2">Der Shifter passt die Farben/Fonts deiner globalen Brand an. Das Design hier im Editor wird automatisch synchronisiert.</p></div></div>)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateContent;