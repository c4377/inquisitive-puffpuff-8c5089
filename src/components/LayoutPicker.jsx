import React from 'react';
// FIX: Use named imports directly to avoid undefined destructuring crashes
import { FiLayout, FiMaximize, FiSquare, FiList, FiSidebar, FiImage, FiAlignLeft, FiAlignRight, FiBox, FiMessageSquare, FiArrowUpLeft, FiArrowDownRight, FiArrowDown, FiTwitter, FiEdit2, FiType, FiLayers, FiHexagon, FiColumns, FiCreditCard } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const LayoutPicker = ({ currentLayout, onUpdate }) => {
  const layouts = [
    // --- MAGAZINE-STYLE VARIANTS (photo/text structure) ---
    { id: 'split_photo', name: 'Split Foto', icon: FiColumns, description: 'Foto eine Seite, Text andere' },
    { id: 'split_photo_v', name: 'Split Vertikal', icon: FiSquare, description: 'Foto oben, Text unten' },
    { id: 'card_on_photo', name: 'Karte auf Foto', icon: FiCreditCard, description: 'Weiße Karte über Hintergrund' },

    // --- COVER LAYOUTS (Photo background, Sarah-Joy style) ---
    { id: 'sarah_cover', name: 'Editorial Cover', icon: FiImage, description: 'Foto + Label + Script-Akzent' },
    { id: 'cover_top_left', name: 'Cover Oben Links', icon: FiArrowUpLeft, description: 'Titel oben links auf Foto' },
    { id: 'cover_bottom_left', name: 'Cover Unten Links', icon: FiArrowDownRight, description: 'Titel unten links auf Foto' },
    { id: 'cover_bottom_center', name: 'Cover Unten', icon: FiArrowDown, description: 'Titel unten zentriert' },
    { id: 'cover_center_hero', name: 'Cover Mitte', icon: FiMaximize, description: 'Großer Titel mittig' },
    { id: 'cover_top_center', name: 'Cover Oben', icon: FiAlignLeft, description: 'Titel oben zentriert' },

    // NEW PREUSS STYLE
    { id: 'badge_centered', name: 'Badge Focus', icon: FiHexagon, description: 'Preuss Style Header' },
    
    // NEW SOCIAL LAYOUTS
    { id: 'story_text_box', name: 'Story Box', icon: FiType, description: 'Text with background box' },
    { id: 'glass_layer', name: 'Glass Overlay', icon: FiSquare, description: 'Transparent full overlay' },
    { id: 'tweet_card', name: 'Tweet Post', icon: FiTwitter, description: 'Social Media Card Style' },

    // EXISTING
    { id: 'editorial_fade_bottom', name: 'Soft Fade', icon: FiArrowDown, description: 'Image fades to bottom' },
    { id: 'minimal_quote', name: 'Quote Focus', icon: FiMessageSquare, description: 'Pinterest Style Quote' },
    { id: 'maximized_bold', name: 'Impact Text', icon: FiMaximize, description: 'Auto-size Huge Text' },
    { id: 'minimal_left_accent', name: 'Left Accent', icon: FiAlignLeft, description: 'Bar + Left Align' },
    { id: 'centered_focus', name: 'Classic Center', icon: FiSquare, description: 'Simple & Clean' },
    { id: 'bold_number_list', name: 'Big Numbers', icon: FiList, description: 'Giant Number List' },
    { id: 'accent_frame', name: 'Accent Frame', icon: FiBox, description: 'Bordered Box' },
    { id: 'editorial_mask', name: 'Circle Mask', icon: FiImage, description: 'Photo Focus' },
    { id: 'split_vertical_editorial', name: 'Split View', icon: FiSidebar, description: 'Half Color/Image' },
    { id: 'story_top_left', name: 'Story Top', icon: FiArrowUpLeft, description: 'Top Left Align (9:16)' },
    { id: 'story_bottom_right', name: 'Story Bottom', icon: FiArrowDownRight, description: 'Bottom Right Align (9:16)' },
    { id: 'diagonal_overlay', name: 'Diagonal', icon: FiLayers, description: 'Modern Split' },
    { id: 'aesthetic_checklist', name: 'Checklist', icon: FiList, description: 'List with Lines' },
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