import React, { useState } from 'react';
import { FiDroplet, FiToggleRight, FiToggleLeft, FiRepeat } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import ColorPalette from './ColorPalette';

const ColorEditor = ({ currentSlide, onUpdate, onGlobalUpdate }) => {
  const [activeSlot, setActiveSlot] = useState('primary');
  const [applyToAll, setApplyToAll] = useState(false);

  const handleColorChange = (color) => {
    let field = 'color';
    if (activeSlot === 'secondary') field = 'secondaryColor';
    if (activeSlot === 'accent') field = 'accentColor';
    if (activeSlot === 'background') field = 'backgroundColor';
    if (activeSlot === 'overlay') field = 'overlayColor';

    const updates = { [field]: color };
    if (applyToAll) {
      onGlobalUpdate(updates);
    } else {
      onUpdate(updates);
    }
  };

  const handleInvert = () => {
    const textColor = currentSlide.color || '#000000';
    const bgColor = currentSlide.backgroundColor || '#FFFFFF';
    const updates = { color: bgColor, backgroundColor: textColor };
    if (applyToAll) {
      onGlobalUpdate(updates);
    } else {
      onUpdate(updates);
    }
  };

  const getColorValue = (slot) => {
    switch (slot) {
      case 'primary': return currentSlide.color || '#000000';
      case 'secondary': return currentSlide.secondaryColor || '#D6D3CD';
      case 'accent': return currentSlide.accentColor || '#EA580C';
      case 'background': return currentSlide.backgroundColor || '#FFFFFF';
      case 'overlay': return currentSlide.overlayColor || '#1A1512';
      default: return '#000000';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between bg-purple-50 p-3 rounded-lg border border-purple-100 mb-4">
        <span className="text-sm font-bold text-purple-900 flex items-center">
          <SafeIcon icon={applyToAll ? FiToggleRight : FiToggleLeft} className={`mr-2 text-xl ${applyToAll ? 'text-purple-600' : 'text-gray-400'}`} />
          {applyToAll ? 'Farben auf ALLE Slides anwenden' : 'Nur auf AKTUELLEN Slide'}
        </span>
        <button
          onClick={() => setApplyToAll(!applyToAll)}
          className={`text-xs px-3 py-1 rounded font-bold transition-colors ${applyToAll ? 'bg-purple-600 text-white' : 'bg-white border border-gray-300 text-gray-600'}`}
        >
          Ändern
        </button>
      </div>

      <div className="flex space-x-2">
        <button
          onClick={handleInvert}
          className="flex-1 bg-white border border-gray-200 text-gray-700 py-2.5 rounded-xl text-xs font-bold flex items-center justify-center hover:bg-gray-50 hover:border-purple-300 hover:text-purple-700 transition-all shadow-sm"
        >
          <SafeIcon icon={FiRepeat} className="mr-2 text-lg" /> Invertieren (Swap)
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {['primary', 'secondary', 'accent', 'background', 'overlay'].map(slot => (
          <button
            key={slot}
            onClick={() => setActiveSlot(slot)}
            className={`p-3 rounded-xl border-2 flex items-center space-x-3 transition-all ${activeSlot === slot ? 'border-purple-600 ring-2 ring-purple-100 bg-white' : 'border-gray-200 hover:border-gray-300 bg-gray-50'}`}
          >
            <div className="w-8 h-8 rounded-full border border-gray-300 shadow-sm" style={{ backgroundColor: getColorValue(slot) }} />
            <div className="text-left">
              <span className="block text-xs font-bold text-gray-900 capitalize">{slot === 'primary' ? 'Text' : slot === 'secondary' ? 'Zweittext' : slot === 'accent' ? 'Akzent' : slot === 'background' ? 'Fläche' : 'Verlauf'}</span>
            </div>
          </button>
        ))}
      </div>

      <div className="pt-4 border-t border-gray-100">
        <label className="block text-sm font-bold text-gray-700 mb-3 flex items-center">
          <SafeIcon icon={FiDroplet} className="mr-2 text-purple-600" /> Farbe wählen: <span className="ml-1 uppercase text-purple-600">{activeSlot}</span>
        </label>
        <ColorPalette selectedColor={getColorValue(activeSlot)} onColorSelect={handleColorChange} />
      </div>
    </div>
  );
};

export default ColorEditor;