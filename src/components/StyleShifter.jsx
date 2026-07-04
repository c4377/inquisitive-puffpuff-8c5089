import React, { useState } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import { buildEditorialDark } from '../constants/brandData';

const { FiRefreshCw, FiType, FiDroplet, FiRotateCw, FiSave, FiCornerUpLeft, FiCheck, FiZap, FiAlertCircle } = FiIcons;

const StyleShifter = ({ compact = false, mode = 'default' }) => {
  const { brandSettings, updateBrandSettings } = useBrand();
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState('');

  const config = brandSettings.currentBrandConfig;

  // Fallback if no brand is selected yet
  if (!config) {
    return (
      <div className={`bg-white border border-yellow-200 rounded-xl shadow-sm p-4 flex items-center justify-center text-yellow-700 text-xs`}>
        <SafeIcon icon={FiAlertCircle} className="mr-2 text-lg" />
        <span>Keine aktive Brand gefunden. Bitte erst eine Brand erstellen.</span>
      </div>
    );
  }

  // --- ACTIONS ---
  const saveCheckpoint = () => {
    setHistory(prev => [...prev, JSON.parse(JSON.stringify(config))]);
    flashMessage("Version gespeichert!");
  };

  const undoLastChange = () => {
    if (history.length === 0) return;
    const previous = history[history.length - 1];
    updateBrandSettings({ currentBrandConfig: previous });
    setHistory(prev => prev.slice(0, -1));
    flashMessage("Wiederhergestellt!");
  };

  // Apply the Editorial Dark look (two-font signature) to the current brand,
  // keeping the user's own brand name/id. darkPhoto toggles the photo wash.
  const applyEditorialDark = (darkPhoto) => {
    if (history.length === 0 || true) saveCheckpoint();
    const preset = buildEditorialDark(darkPhoto);
    updateBrandSettings({
      currentBrandConfig: {
        ...config,
        colors: preset.colors,
        typography: preset.typography,
        layout: preset.layout,
        darkPhoto: preset.darkPhoto,
        editorialDark: true,
      },
    });
    flashMessage(darkPhoto ? 'Editorial Dark aktiv' : 'Editorial Hell aktiv');
  };

  const swapFonts = () => {
    if (!config.typography.accentFontFamily) {
      flashMessage("Keine Akzent-Schrift definiert!");
      return;
    }
    if (history.length === 0) saveCheckpoint();
    
    const newTypo = {
      ...config.typography,
      fontFamily: config.typography.accentFontFamily,
      accentFontFamily: config.typography.fontFamily,
      fontWeight: config.typography.fontFamily.includes('Playfair') ? '700' : '400'
    };
    updateBrandSettings({ currentBrandConfig: { ...config, typography: newTypo } });
    flashMessage("Fonts Getauscht!");
  };

  const shiftColors = (shiftMode = 'rotate') => {
    if (history.length === 0) saveCheckpoint();
    const { colors } = config;
    let newColors = { ...colors };

    if (shiftMode === 'invert') {
      newColors.primary = colors.background;
      newColors.background = colors.primary;
      if (colors.secondary === colors.background) newColors.secondary = colors.primary;
    } else if (shiftMode === 'rotate') {
      newColors.primary = colors.accent;
      newColors.accent = colors.secondary;
      newColors.secondary = colors.primary;
    } else if (shiftMode === 'shuffle') {
      const palette = [colors.primary, colors.secondary, colors.accent, colors.tertiary, colors.neutral].filter(Boolean);
      const random = (arr) => arr[Math.floor(Math.random() * arr.length)];
      newColors.primary = random(palette);
      newColors.secondary = random(palette);
      newColors.accent = random(palette);
      if (newColors.background === newColors.primary) {
          newColors.background = (newColors.primary === '#000000' || newColors.primary === '#000') ? '#FFFFFF' : '#000000';
      }
    }
    updateBrandSettings({ currentBrandConfig: { ...config, colors: newColors } });
    flashMessage("Farben Neu Gemischt!");
  };

  const flashMessage = (msg) => {
    setMessage(msg);
    setTimeout(() => setMessage(''), 2000);
  };

  // --- RENDER MODES ---

  // 1. BAR MODE (Horizontal Sticky Toolbar)
  if (mode === 'bar') {
    return (
        <div className="flex items-center w-full overflow-x-auto no-scrollbar py-1 space-x-2">
            {/* Status Message Overlay (Absolute to not shift layout) */}
            {message && (
                <div className="absolute left-1/2 top-0 -translate-y-full bg-green-600 text-white text-[10px] px-2 py-0.5 rounded-t-lg font-bold shadow-sm animate-fade-in">
                    {message}
                </div>
            )}
            
            <span className="text-[10px] font-bold text-gray-400 uppercase mr-1 hidden sm:block">Style:</span>

            <button onClick={swapFonts} className="flex-shrink-0 flex items-center px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-gray-700 hover:text-purple-600 hover:border-purple-300 shadow-sm transition-all whitespace-nowrap">
                <SafeIcon icon={FiType} className="mr-1.5" /> Fonts
            </button>
            
            <div className="w-px h-5 bg-gray-300 mx-1 flex-shrink-0"></div>

            <button onClick={() => shiftColors('invert')} className="flex-shrink-0 flex items-center px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-gray-700 hover:text-purple-600 hover:border-purple-300 shadow-sm transition-all whitespace-nowrap">
                <SafeIcon icon={FiRefreshCw} className="mr-1.5" /> Invert
            </button>
            <button onClick={() => shiftColors('rotate')} className="flex-shrink-0 flex items-center px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-gray-700 hover:text-purple-600 hover:border-purple-300 shadow-sm transition-all whitespace-nowrap">
                <SafeIcon icon={FiDroplet} className="mr-1.5" /> Rotate
            </button>
             <button onClick={() => shiftColors('shuffle')} className="flex-shrink-0 flex items-center px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-gray-700 hover:text-purple-600 hover:border-purple-300 shadow-sm transition-all whitespace-nowrap">
                <SafeIcon icon={FiRotateCw} className="mr-1.5" /> Mix
            </button>

            <div className="w-px h-5 bg-gray-300 mx-1 flex-shrink-0"></div>

            <button onClick={undoLastChange} disabled={history.length === 0} className="flex-shrink-0 flex items-center px-3 py-1.5 bg-gray-100 border border-gray-200 rounded-lg text-xs font-bold text-gray-600 disabled:opacity-50 hover:bg-gray-200 transition-all whitespace-nowrap">
                <SafeIcon icon={FiCornerUpLeft} className="mr-1.5" /> Undo
            </button>
        </div>
    );
  }

  // 2. DEFAULT / COMPACT CARD MODE
  return (
    <div className={`bg-white border border-purple-100 rounded-xl shadow-sm overflow-hidden ${compact ? 'p-2' : 'p-4'}`}>
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center">
          <SafeIcon icon={FiZap} className="mr-1 text-purple-600" /> Style Shifter
        </h3>
        {message && <span className="text-[10px] font-bold text-green-600 animate-fade-in">{message}</span>}
      </div>

      <div className="grid grid-cols-2 gap-2 mb-3">
        <button onClick={swapFonts} className="flex items-center justify-center px-3 py-2 bg-gray-50 hover:bg-purple-50 text-gray-700 hover:text-purple-700 rounded-lg text-xs font-bold border border-gray-200 transition-colors">
          <SafeIcon icon={FiType} className="mr-2" /> Swap Fonts
        </button>
        <button onClick={() => shiftColors('invert')} className="flex items-center justify-center px-3 py-2 bg-gray-50 hover:bg-purple-50 text-gray-700 hover:text-purple-700 rounded-lg text-xs font-bold border border-gray-200 transition-colors">
          <SafeIcon icon={FiRefreshCw} className="mr-2" /> Invert Colors
        </button>
        <button onClick={() => shiftColors('rotate')} className="flex items-center justify-center px-3 py-2 bg-gray-50 hover:bg-purple-50 text-gray-700 hover:text-purple-700 rounded-lg text-xs font-bold border border-gray-200 transition-colors">
          <SafeIcon icon={FiDroplet} className="mr-2" /> Rotate Accents
        </button>
        <button onClick={() => shiftColors('shuffle')} className="flex items-center justify-center px-3 py-2 bg-gray-50 hover:bg-purple-50 text-gray-700 hover:text-purple-700 rounded-lg text-xs font-bold border border-gray-200 transition-colors">
          <SafeIcon icon={FiRotateCw} className="mr-2" /> Shuffle Mix
        </button>
      </div>

      <div className="flex space-x-2 pt-2 border-t border-gray-100">
        <button onClick={saveCheckpoint} className="flex-1 py-1.5 bg-blue-50 text-blue-700 rounded-lg text-[10px] font-bold hover:bg-blue-100 flex items-center justify-center">
          <SafeIcon icon={FiSave} className="mr-1" /> Version Merken
        </button>
        <button onClick={undoLastChange} disabled={history.length === 0} className="flex-1 py-1.5 bg-gray-100 text-gray-600 rounded-lg text-[10px] font-bold hover:bg-gray-200 disabled:opacity-50 flex items-center justify-center">
          <SafeIcon icon={FiCornerUpLeft} className="mr-1" /> Zurück ({history.length})
        </button>
      </div>
    </div>
  );
};

export default StyleShifter;