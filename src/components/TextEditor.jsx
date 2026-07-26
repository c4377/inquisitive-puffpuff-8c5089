import React, { useState, useEffect } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';

const { FiType, FiAlignCenter, FiAlignLeft, FiAlignRight, FiMove, FiMinus, FiPlus, FiBold, FiItalic, FiTag, FiDroplet, FiStar } = FiIcons;

const TextEditor = ({ currentSlide, onUpdate, onGlobalUpdate, onBatchUpdate, totalSlides }) => {
  const { brandSettings } = useBrand();
  const [activeTab, setActiveTab] = useState('primary'); // 'primary' | 'secondary'
  const [applyPosToAll, setApplyPosToAll] = useState(false);
  const [fontScope, setFontScope] = useState('current');

  // --- KEY MAPPING ---
  const getKeys = () => {
    return activeTab === 'primary' ? 
      { 
        text: 'text', 
        size: 'fontSize', 
        x: 'xOffset', 
        y: 'yOffset', 
        align: 'textAlign', 
        color: 'color', 
        font: 'fontFamily', 
        weight: 'fontWeight', 
        style: 'fontStyle',
        opacity: 'textOpacity'
      } : 
      { 
        text: 'secondaryText', 
        size: 'secondaryFontSize', 
        x: 'secondaryXOffset', 
        y: 'secondaryYOffset', 
        align: 'secondaryTextAlign', 
        color: 'secondaryTextColor', 
        font: 'secondaryFontFamily', 
        weight: 'secondaryFontWeight', 
        style: 'secondaryFontStyle',
        opacity: 'secondaryTextOpacity'
      };
  };

  const keys = getKeys();

  // --- SMART GETTER (With Defaults) ---
  const getValue = (key) => {
    const val = currentSlide[key];
    
    // Explicit Fallbacks for Secondary Text properties to inherit from Primary if unset
    if (activeTab === 'secondary') {
        if (key === 'secondaryTextColor' && val === undefined) return currentSlide.color || '#000000';
        if (key === 'secondaryFontFamily' && val === undefined) return currentSlide.fontFamily || 'Inter';
        if (key === 'secondaryFontSize' && val === undefined) return (currentSlide.fontSize ? Math.round(currentSlide.fontSize * 0.6) : 32);
        if (key === 'secondaryFontWeight' && val === undefined) return '400'; // Default to regular for subtext
    }
    
    return val;
  };

  const updateValue = (key, value) => {
    const updates = { [key]: value };
    
    // Position Sync Logic
    if (applyPosToAll && (key.includes('Offset') || key.includes('Opacity'))) {
      onGlobalUpdate(updates);
      return;
    }
    
    onUpdate(updates);
  };

  // --- ACTION HANDLERS ---

  const handleFontChange = (e) => {
    const newFont = e.target.value;
    const isPlayfair = newFont.includes('Playfair');
    const updates = { [keys.font]: newFont };
    
    // Reset weight when switching fonts to avoid stuck bold on fonts that don't support it well
    if (isPlayfair) {
        updates[keys.weight] = '400';
    }
    
    if (onBatchUpdate) {
      onBatchUpdate(updates, fontScope);
    } else {
      if (fontScope === 'all') onGlobalUpdate(updates);
      else onUpdate(updates);
    }
  };

  const adjustFontSize = (delta) => {
    const currentSize = parseInt(getValue(keys.size)) || (activeTab === 'primary' ? 48 : 32);
    const newSize = Math.max(10, Math.min(200, currentSize + delta));
    updateValue(keys.size, newSize);
  };

  const toggleBold = () => {
    const currentW = String(getValue(keys.weight) || '400');
    // Check if it's currently bold (covers '700', 'bold', '600', '800', '900')
    const isBold = currentW === '700' || currentW === 'bold' || currentW === '600' || (parseInt(currentW) >= 600);
    
    // Toggle
    const newWeight = isBold ? '400' : '700';
    updateValue(keys.weight, newWeight);
  };

  const toggleItalic = () => {
    const currentS = getValue(keys.style) || 'normal';
    updateValue(keys.style, currentS === 'italic' ? 'normal' : 'italic');
  };

  const toggleLight = () => {
    const currentW = String(getValue(keys.weight) || '400');
    updateValue(keys.weight, currentW === '300' ? '400' : '300');
  };

  const handleAlign = (align) => {
    updateValue(keys.align, align);
    // Auto-reset X offset when centering to avoid confusion
    if (align === 'center') {
      updateValue(keys.x, 0);
    }
  };

  // --- HIGHLIGHT HELPER ---
  const insertHighlight = () => {
    const field = keys.text;
    const currentText = currentSlide[field] || ''; // Direct access ensures we get the raw string
    const textarea = document.getElementById('text-input-area');
    
    if (textarea && textarea.selectionStart !== textarea.selectionEnd) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selected = currentText.substring(start, end);
      const newText = currentText.substring(0, start) + `*${selected}*` + currentText.substring(end);
      updateValue(field, newText);
    } else {
      updateValue(field, currentText + " *Highlight*");
    }
  };

  // --- FONT LIST ---
  const standardFonts = [
    { name: 'Aspekta (Warm Editorial)', value: 'AspektaBrand' },
    { name: 'Helvetica Neue', value: 'HelveticaNeueBrand' },
    { name: 'Playfair Display', value: 'Playfair Display' },
    { name: 'Cormorant Garamond', value: 'Cormorant Garamond' },
    { name: 'Montserrat', value: 'Montserrat' },
    { name: 'Inter', value: 'Inter' },
    { name: 'Outfit', value: 'Outfit' },
    { name: 'Poppins', value: 'Poppins' },
    { name: 'Caveat', value: 'Caveat' },
    { name: 'La Belle Aurore', value: 'La Belle Aurore' },
    { name: 'Courier Prime', value: 'Courier Prime' },
  ];
  const customFonts = (brandSettings.customFonts || []).map(f => ({ name: `${f.name} (Custom)`, value: f.name }));
  const allFonts = [...customFonts, ...standardFonts];

  const globalBrandName = brandSettings.currentBrandConfig?.name || "";

  return (
    <div className="space-y-6">
      {/* TABS */}
      <div className="flex bg-gray-100 p-1 rounded-lg">
        <button 
          onClick={() => setActiveTab('primary')} 
          className={`flex-1 py-2 text-xs font-bold rounded-md transition-all ${activeTab === 'primary' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}
        >
          Headline (Haupt)
        </button>
        <button 
          onClick={() => setActiveTab('secondary')} 
          className={`flex-1 py-2 text-xs font-bold rounded-md transition-all ${activeTab === 'secondary' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}
        >
          Subtext (Zusatz)
        </button>
      </div>

      {/* TEXT INPUT AREA */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2 flex items-center justify-between">
          <div className="flex items-center">
            <SafeIcon icon={FiType} className="mr-2 text-purple-600" />
            {activeTab === 'primary' ? 'Inhalt Headline' : 'Inhalt Subtext'}
          </div>
          <button 
            onClick={insertHighlight} 
            className="text-[10px] bg-purple-50 text-purple-700 px-2 py-1 rounded font-bold flex items-center hover:bg-purple-200 transition-colors border border-purple-100"
            title="Wort markieren für Highlights"
          >
            <SafeIcon icon={FiStar} className="mr-1" /> Highlight (*Wort*)
          </button>
        </label>
        <textarea 
          id="text-input-area"
          value={currentSlide[keys.text] || ''} // Use direct access to ensure empty string handling
          onChange={(e) => updateValue(keys.text, e.target.value)}
          placeholder={activeTab === 'primary' ? "Dein Text hier..." : "Zusatztext hier eingeben (optional)..."}
          className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 font-sans text-base shadow-sm min-h-[100px]"
        />
        <p className="text-[10px] text-gray-400 mt-1">
            {activeTab === 'primary' ? 'Tipp: Wörter in *Sternchen* werden hervorgehoben.' : 'Der Subtext erscheint meist kleiner unter oder über der Headline.'}
        </p>
      </div>

      {/* FONT CONTROLS */}
      <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
        <label className="block text-xs font-bold text-gray-500 uppercase mb-3">
            Schriftart ({activeTab === 'primary' ? 'Headline' : 'Subtext'})
        </label>
        
        {totalSlides > 1 && activeTab === 'primary' && (
          <div className="flex bg-white rounded-lg border border-gray-200 p-1 mb-3">
            <button onClick={() => setFontScope('current')} className={`flex-1 py-1.5 text-[10px] font-bold rounded transition-colors ${fontScope === 'current' ? 'bg-purple-100 text-purple-700' : 'text-gray-500 hover:bg-gray-50'}`}>Single</button>
            <button onClick={() => setFontScope('all')} className={`flex-1 py-1.5 text-[10px] font-bold rounded transition-colors ${fontScope === 'all' ? 'bg-purple-100 text-purple-700' : 'text-gray-500 hover:bg-gray-50'}`}>Alle</button>
            <button onClick={() => setFontScope('body')} className={`flex-1 py-1.5 text-[10px] font-bold rounded transition-colors ${fontScope === 'body' ? 'bg-purple-100 text-purple-700' : 'text-gray-500 hover:bg-gray-50'}`}>Body</button>
          </div>
        )}

        <select 
          value={getValue(keys.font) || 'Inter'} 
          onChange={handleFontChange} 
          className="w-full p-2 border border-gray-300 rounded-lg text-sm bg-white mb-2"
          style={{ fontFamily: getValue(keys.font) }}
        >
          {allFonts.map(f => (
            <option key={f.value} value={f.value} style={{ fontFamily: f.value }}>{f.name}</option>
          ))}
        </select>

        <div className="grid grid-cols-3 gap-2 mt-3">
          <button 
            onClick={toggleLight}
            className={`py-2 px-1 rounded-lg border text-xs flex items-center justify-center transition-colors ${String(getValue(keys.weight)) === '300' ? 'bg-purple-100 border-purple-500 text-purple-700 font-bold' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'}`}
          >
            Thin
          </button>
          <button 
            onClick={toggleBold}
            className={`py-2 px-1 rounded-lg border font-bold text-xs flex items-center justify-center transition-colors ${(String(getValue(keys.weight)) === '700' || parseInt(getValue(keys.weight)) >= 600) ? 'bg-purple-100 border-purple-500 text-purple-700' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'}`}
          >
            <SafeIcon icon={FiBold} className="mr-1" /> Bold
          </button>
          <button 
            onClick={toggleItalic}
            className={`py-2 px-1 rounded-lg border italic text-xs flex items-center justify-center transition-colors ${getValue(keys.style) === 'italic' ? 'bg-purple-100 border-purple-500 text-purple-700' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'}`}
          >
            <SafeIcon icon={FiItalic} className="mr-1" /> Italic
          </button>
        </div>
      </div>

      {/* SIZE & OPACITY */}
      <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-4">
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-gray-500 uppercase">Schriftgröße</label>
            <span className="text-xs font-mono bg-white px-2 py-1 rounded border border-gray-200">
              {getValue(keys.size)}px
            </span>
          </div>
          <div className="flex items-center space-x-3">
            <button onClick={() => adjustFontSize(-4)} className="p-2 bg-white rounded-lg border border-gray-200 hover:bg-gray-100"><SafeIcon icon={FiMinus} className="text-xs" /></button>
            <input 
              type="range" 
              min="10" 
              max="200" 
              value={parseInt(getValue(keys.size)) || 32} 
              onChange={(e) => updateValue(keys.size, parseInt(e.target.value))} 
              className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" 
            />
            <button onClick={() => adjustFontSize(4)} className="p-2 bg-white rounded-lg border border-gray-200 hover:bg-gray-100"><SafeIcon icon={FiPlus} className="text-xs" /></button>
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-gray-500 uppercase flex items-center">
              <SafeIcon icon={FiDroplet} className="mr-1" /> Deckkraft
            </label>
            <span className="text-xs font-mono bg-white px-2 py-1 rounded border border-gray-200">
              {Math.round((getValue(keys.opacity) !== undefined ? getValue(keys.opacity) : 1) * 100)}%
            </span>
          </div>
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.05" 
            value={getValue(keys.opacity) !== undefined ? getValue(keys.opacity) : 1} 
            onChange={(e) => updateValue(keys.opacity, parseFloat(e.target.value))} 
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" 
          />
        </div>
      </div>

      {/* ALIGNMENT */}
      <div>
        <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Ausrichtung</label>
        <div className="flex space-x-2">
          {['left', 'center', 'right'].map(align => (
            <button 
              key={align} 
              onClick={() => handleAlign(align)} 
              className={`flex-1 py-2 rounded-lg border transition-all flex justify-center ${getValue(keys.align) === align || (!getValue(keys.align) && align === 'center') ? 'bg-purple-100 border-purple-500 text-purple-700' : 'bg-white border-gray-200 text-gray-500 hover:bg-gray-50'}`}
            >
              <SafeIcon icon={align === 'left' ? FiAlignLeft : align === 'right' ? FiAlignRight : FiAlignCenter} className="text-lg" />
            </button>
          ))}
        </div>
      </div>

      {/* POSITION */}
      <div className="bg-white p-0 pt-2">
        <label className="block text-xs font-bold text-gray-500 uppercase mb-3 flex items-center justify-between">
          <div className="flex items-center">
            <SafeIcon icon={FiMove} className="mr-1"/> Position ({activeTab === 'primary' ? 'Headline' : 'Subtext'})
          </div>
          {totalSlides > 1 && (
            <div className="flex items-center space-x-2 bg-gray-50 px-2 py-1 rounded-lg border border-gray-200">
              <button 
                onClick={() => setApplyPosToAll(!applyPosToAll)} 
                className={`w-8 h-4 rounded-full transition-colors relative ${applyPosToAll ? 'bg-purple-600' : 'bg-gray-300'}`}
                title="Position auf alle Slides anwenden"
              >
                <div className={`absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full shadow-sm transition-transform ${applyPosToAll ? 'translate-x-4' : ''}`} />
              </button>
            </div>
          )}
        </label>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="flex justify-between text-[10px] text-gray-400 mb-1 uppercase tracking-wider">Horizontal (X)</div>
            <input 
              type="range" 
              min="-300" 
              max="300" 
              value={getValue(keys.x) || 0} 
              onChange={(e) => updateValue(keys.x, parseInt(e.target.value))} 
              className={`w-full h-1.5 rounded-lg appearance-none cursor-pointer ${applyPosToAll ? 'bg-purple-100 accent-purple-600' : 'bg-gray-100 accent-gray-400'}`} 
            />
          </div>
          <div>
            <div className="flex justify-between text-[10px] text-gray-400 mb-1 uppercase tracking-wider">Vertikal (Y)</div>
            <input 
              type="range" 
              min="-300" 
              max="300" 
              value={getValue(keys.y) || 0} 
              onChange={(e) => updateValue(keys.y, parseInt(e.target.value))} 
              className={`w-full h-1.5 rounded-lg appearance-none cursor-pointer ${applyPosToAll ? 'bg-purple-100 accent-purple-600' : 'bg-gray-100 accent-gray-400'}`} 
            />
          </div>
        </div>
      </div>

      {/* COLOR */}
      <div>
        <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Text Farbe ({activeTab})</label>
        <div className="flex items-center space-x-3">
          <input 
            type="color" 
            value={getValue(keys.color) || '#000000'} 
            onChange={(e) => updateValue(keys.color, e.target.value)} 
            className="w-10 h-10 border-2 border-gray-200 rounded-lg cursor-pointer" 
          />
          {activeTab === 'secondary' && (
            <button 
              onClick={() => updateValue(keys.color, currentSlide.color || '#000000')}
              className="text-xs text-purple-600 hover:underline"
            >
              Wie Headline
            </button>
          )}
        </div>
      </div>

      <hr className="border-gray-100" />

      {/* FOOTER */}
      <div>
        <label className="block text-xs font-bold text-gray-500 uppercase mb-2 flex items-center">
          <SafeIcon icon={FiTag} className="mr-1" /> Footer Text (Global)
        </label>
        <input 
          type="text" 
          value={currentSlide.brandText !== undefined ? currentSlide.brandText : ''} 
          placeholder={globalBrandName.toUpperCase()}
          onChange={(e) => onGlobalUpdate({ brandText: e.target.value })} 
          className="w-full p-2 border border-gray-300 rounded-lg text-sm bg-gray-50 focus:bg-white focus:ring-2 focus:ring-purple-500 placeholder-gray-400" 
        />
      </div>
    </div>
  );
};

export default TextEditor;