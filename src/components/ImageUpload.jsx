import React, { useState, useEffect } from 'react';
import { FiUpload, FiImage, FiZap, FiLayers, FiTrash2 } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import { generatePattern } from '../utils/patternGenerator';

const ImageUpload = ({ onImageSelect, onOverlaySelect, currentOverlay }) => {
  const { brandSettings } = useBrand();
  // MODES: 'upload' (Background), 'generate' (Patterns), 'overlay' (Overlay Image)
  const [activeTab, setActiveTab] = useState('upload');
  const [generatedPatterns, setGeneratedPatterns] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const patternTypes = [
    { id: 'soft_gradient', name: 'Soft Gradient' },
    { id: 'mesh_gradient', name: 'Mesh Aura' },
    { id: 'deep_aura', name: 'Deep Glow' },
    { id: 'noise_texture', name: 'Texture Only' },
    { id: 'geometric_minimal', name: 'Geometric' },
    { id: 'stripes_modern', name: 'Modern Stripes' }
  ];

  const handleFileUpload = (event, isOverlay = false) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (isOverlay) {
          onOverlaySelect(e.target.result);
        } else {
          onImageSelect(e.target.result);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setTimeout(() => {
      const colors = brandSettings.currentBrandConfig?.colors || { primary: '#000000', secondary: '#cccccc', accent: '#888888', background: '#ffffff' };
      const newPatterns = patternTypes.map(type => ({
        ...type,
        src: generatePattern(type.id, colors, 400, 500)
      }));
      setGeneratedPatterns(newPatterns);
      setIsGenerating(false);
    }, 500);
  };

  useEffect(() => {
    if (activeTab === 'generate' && generatedPatterns.length === 0) {
      handleGenerate();
    }
  }, [activeTab]);

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="flex bg-gray-100 p-1 rounded-lg overflow-x-auto no-scrollbar">
        <button onClick={() => setActiveTab('upload')} className={`flex-1 py-2 px-2 text-xs font-bold rounded-md transition-all whitespace-nowrap ${activeTab === 'upload' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}>
          <SafeIcon icon={FiImage} className="inline mr-1" /> Hintergrund
        </button>
        <button onClick={() => setActiveTab('overlay')} className={`flex-1 py-2 px-2 text-xs font-bold rounded-md transition-all whitespace-nowrap ${activeTab === 'overlay' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}>
          <SafeIcon icon={FiLayers} className="inline mr-1" /> Logo / Sticker
        </button>
        <button onClick={() => setActiveTab('generate')} className={`flex-1 py-2 px-2 text-xs font-bold rounded-md transition-all whitespace-nowrap ${activeTab === 'generate' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}>
          <SafeIcon icon={FiZap} className="inline mr-1" /> Magic Gen
        </button>
      </div>

      {activeTab === 'upload' && (
        <div className="animate-fade-in">
          <label className="block w-full border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:bg-gray-50 hover:border-purple-300 transition-all group">
            <SafeIcon icon={FiImage} className="text-4xl text-gray-300 group-hover:text-purple-400 mx-auto mb-3 transition-colors" />
            <span className="block text-sm font-bold text-gray-700 mb-1">Eigenes Bild wählen</span>
            <span className="block text-xs text-gray-400">JPG, PNG (Max 5MB)</span>
            <input type="file" accept="image/*" onChange={(e) => handleFileUpload(e, false)} className="hidden" />
          </label>
        </div>
      )}

      {activeTab === 'overlay' && (
        <div className="animate-fade-in space-y-4">
          {currentOverlay ? (
            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 text-center">
              <div className="w-24 h-24 mx-auto bg-gray-200/50 rounded-lg mb-3 flex items-center justify-center overflow-hidden border border-gray-300 relative">
                {/* Checkerboard pattern for transparency check */}
                <div className="absolute inset-0 opacity-20" style={{backgroundImage: 'linear-gradient(45deg, #808080 25%, transparent 25%), linear-gradient(-45deg, #808080 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #808080 75%), linear-gradient(-45deg, transparent 75%, #808080 75%)', backgroundSize: '10px 10px', backgroundPosition: '0 0, 0 5px, 5px -5px, -5px 0px'}}></div>
                <img src={currentOverlay} alt="Overlay" className="max-w-full max-h-full relative z-10 object-contain" />
              </div>

              <div className="flex flex-col space-y-2">
                 <label className="w-full py-2 bg-purple-600 text-white text-xs font-bold rounded-lg hover:bg-purple-700 cursor-pointer flex items-center justify-center transition-colors">
                  <SafeIcon icon={FiUpload} className="mr-2"/> Neues Overlay wählen
                  <input type="file" accept="image/*" onChange={(e) => handleFileUpload(e, true)} className="hidden" />
                </label>
                <button onClick={() => onOverlaySelect(null)} className="w-full py-2 bg-white border border-gray-200 text-red-500 text-xs font-bold rounded-lg hover:bg-red-50 flex items-center justify-center transition-colors">
                  <SafeIcon icon={FiTrash2} className="mr-2"/> Overlay entfernen
                </button>
              </div>
              <p className="text-[10px] text-gray-400 mt-2">
                Tipp: Verwende PNG-Dateien mit transparentem Hintergrund für die besten Ergebnisse. Position & Größe kannst du im Tab "Bild-Effekte" anpassen.
              </p>
            </div>
          ) : (
            <label className="block w-full border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:bg-gray-50 hover:border-purple-300 transition-all group">
              <SafeIcon icon={FiLayers} className="text-4xl text-gray-300 group-hover:text-purple-400 mx-auto mb-3 transition-colors" />
              <span className="block text-sm font-bold text-gray-700 mb-1">Logo / Sticker hochladen</span>
              <span className="block text-xs text-gray-400">Platziere ein Bild (z.B. Logo) über dem Layout.</span>
              <input type="file" accept="image/*" onChange={(e) => handleFileUpload(e, true)} className="hidden" />
            </label>
          )}
        </div>
      )}

      {activeTab === 'generate' && (
        <div className="animate-fade-in">
          <div className="flex justify-between items-center mb-4">
            <label className="text-xs font-bold text-gray-500 uppercase flex items-center"><SafeIcon icon={FiLayers} className="mr-1"/> Brand Patterns</label>
            <button onClick={handleGenerate} disabled={isGenerating} className="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded font-bold hover:bg-purple-100 transition-colors flex items-center">
              <SafeIcon icon={FiZap} className={`mr-1 ${isGenerating ? 'animate-spin' : ''}`} />
              {isGenerating ? 'Generiere...' : 'Neu Generieren'}
            </button>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {isGenerating ? (
              [1, 2, 3, 4].map(n => (
                <div key={n} className="aspect-[4/5] bg-gray-100 rounded-lg animate-pulse"></div>
              ))
            ) : (
              generatedPatterns.map((pattern) => (
                <button key={pattern.id} onClick={() => onImageSelect(pattern.src)} className="group relative aspect-[4/5] rounded-lg overflow-hidden border border-gray-200 hover:border-purple-500 hover:ring-2 hover:ring-purple-200 transition-all">
                  <img src={pattern.src} alt={pattern.name} className="w-full h-full object-cover" />
                  <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <span className="text-[10px] text-white font-bold">{pattern.name}</span>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;