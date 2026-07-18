import React from 'react';
// FIX: Use named imports directly to avoid undefined destructuring crashes
import { FiLayout, FiMaximize, FiSquare, FiList, FiSidebar, FiImage, FiAlignLeft, FiAlignRight, FiBox, FiMessageSquare, FiArrowUpLeft, FiArrowDownRight, FiArrowDown, FiTwitter, FiEdit2, FiType, FiLayers, FiHexagon, FiColumns, FiCreditCard } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const LayoutPicker = ({ currentLayout, onUpdate }) => {
  const layouts = [
    // --- TEXT AUF FOTO (Verlauf) ---
    { id: 'brand_photo_gradient', name: 'Foto Verlauf', icon: FiImage, description: 'Text unten auf Foto' },
    { id: 'brand_photo_bottom_left', name: 'Foto unten links', icon: FiAlignLeft, description: 'Text unten links' },
    { id: 'brand_photo_top', name: 'Foto oben', icon: FiAlignLeft, description: 'Text oben auf Foto' },
    { id: 'brand_photo_center', name: 'Foto Mitte', icon: FiMaximize, description: 'Text mittig auf Foto' },
    { id: 'brand_photo_bigword', name: 'Foto Big-Word', icon: FiMaximize, description: 'Riesenwort auf Foto' },
    { id: 'brand_photo_quote', name: 'Foto Zitat', icon: FiMessageSquare, description: 'Kicker + Zitat' },
    { id: 'brand_photo_bottom_serif', name: 'Foto Serif', icon: FiType, description: 'Serif unten + Fuß' },

    // --- FOTO GERAHMT ---
    { id: 'brand_photo_frame', name: 'Foto gerahmt', icon: FiCreditCard, description: 'Foto im Rahmen' },
    { id: 'brand_frame_top_text', name: 'Rahmen Text oben', icon: FiCreditCard, description: 'Text über Rahmen' },
    { id: 'brand_frame_left', name: 'Rahmen links', icon: FiColumns, description: 'Rahmen versetzt' },
    { id: 'brand_frame_polaroid', name: 'Polaroid', icon: FiSquare, description: 'Foto wie Polaroid' },

    // --- TEXT-FLÄCHE ---
    { id: 'brand_text_plate', name: 'Text-Fläche', icon: FiSquare, description: 'Text mittig, Rahmen' },
    { id: 'brand_text_plate_top', name: 'Fläche oben', icon: FiAlignLeft, description: 'Text oben' },
    { id: 'brand_text_left', name: 'Fläche links', icon: FiAlignLeft, description: 'Text linksbündig' },
    { id: 'brand_text_bigword', name: 'Big-Word', icon: FiMaximize, description: 'Riesenwort-Statement' },
    { id: 'brand_text_quote', name: 'Zitat-Fläche', icon: FiMessageSquare, description: 'Kicker + Zitat' },
    { id: 'brand_text_statement', name: 'Statement', icon: FiType, description: 'Aussage + Fußzeile' },
    { id: 'brand_text_kicker_lead', name: 'Kicker-Lead', icon: FiType, description: 'Kicker führt ein' },
    { id: 'brand_text_minimal', name: 'Minimal', icon: FiSquare, description: 'Nur Text, ruhig' },
    { id: 'brand_text_bold_top', name: 'Bold oben links', icon: FiMaximize, description: 'Großer Text oben links' },

    // --- TEXT LAYOUTS (klassisch, ohne Foto) ---
    { id: 'editorial_classic', name: 'Classic Center', icon: FiSquare, description: 'Klarer, zentrierter Text' },
    { id: 'minimal_quote', name: 'Quote Focus', icon: FiMessageSquare, description: 'Zitat-Stil, ruhig' },
    { id: 'maximized_bold', name: 'Impact Text', icon: FiMaximize, description: 'Großer Aussage-Text' },
    { id: 'paper_box', name: 'Paper Box', icon: FiType, description: 'Text auf ruhiger Fläche' },

    // --- PHOTO LAYOUTS (full-bleed photo + text) ---
    { id: 'cover_top_center', name: 'Cover Oben', icon: FiAlignLeft, description: 'Titel oben auf Foto' },
    { id: 'cover_center_hero', name: 'Cover Mitte', icon: FiMaximize, description: 'Großer Titel mittig' },
    { id: 'cover_bottom_center', name: 'Cover Unten', icon: FiArrowDown, description: 'Titel unten zentriert' },
    { id: 'cover_top_left', name: 'Cover Oben Links', icon: FiArrowUpLeft, description: 'Titel oben links' },
    { id: 'cover_bottom_left', name: 'Cover Unten Links', icon: FiArrowDownRight, description: 'Titel unten links' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-medium text-gray-700">
          <SafeIcon icon={FiLayout} className="inline mr-2" /> Choose Layout Style
        </label>
        <span className="text-[10px] bg-purple-100 text-purple-700 px-2 py-0.5 rounded font-bold">
          Tipp: Nutze *Wort* für Farben
        </span>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {layouts.map((layout) => (
          <button
            key={layout.id}
            onClick={() => onUpdate({ layout: layout.id, xOffset: 0, yOffset: 0, secondaryXOffset: 0, secondaryYOffset: 0, textAnchor: null })}
            className={`flex flex-col items-center justify-center p-3 rounded-xl border-2 transition-all relative ${currentLayout === layout.id ? 'border-purple-600 bg-purple-50 text-purple-700 shadow-sm' : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50 text-gray-600'}`}
          >
            <SafeIcon icon={layout.icon} className="text-2xl mb-2" />
            <span className="text-xs font-bold">{layout.name}</span>
            <span className="text-[10px] text-gray-400 mt-1 text-center leading-tight">{layout.description}</span>
            {currentLayout === layout.id && (
              <div className="absolute top-2 right-2 w-2 h-2 bg-purple-600 rounded-full"></div>
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

export default LayoutPicker;