import React from 'react';
import { useBrand } from '../context/BrandContext';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const FontSelector = ({ selectedFont, onFontSelect }) => {
  const { brandSettings } = useBrand();

  const defaultFonts = [
    { 
      name: 'Outfit', 
      category: 'Sans Serif', 
      style: { fontFamily: 'Outfit, sans-serif', fontWeight: '600' }, 
      description: 'Modern, Clean & Geometric' 
    },
    { 
      name: 'Playfair Display', 
      category: 'Serif', 
      style: { fontFamily: 'Playfair Display, serif' }, 
      description: 'Elegant & Classic' 
    },
    { 
      name: 'Montserrat', 
      category: 'Sans Serif', 
      style: { fontFamily: 'Montserrat, sans-serif', fontWeight: '600' }, 
      description: 'Bold & Modern' 
    },
    { 
      name: 'Inter', 
      category: 'Sans Serif', 
      style: { fontFamily: 'Inter, sans-serif' }, 
      description: 'Clean & Neutral' 
    },
    { 
      name: 'Courier Prime', 
      category: 'Typewriter', 
      style: { fontFamily: 'Courier Prime, monospace' }, 
      description: 'Raw & Authentic Story' 
    },
    { 
      name: 'Caveat', 
      category: 'Handwriting', 
      style: { fontFamily: 'Caveat, cursive' }, 
      description: 'Creative & Personal' 
    },
    { 
      name: 'Cormorant Garamond', 
      category: 'Serif', 
      style: { fontFamily: 'Cormorant Garamond, serif' }, 
      description: 'Luxury & Refined' 
    }
  ];

  // Merge Defaults with Custom Fonts
  const customFonts = (brandSettings.customFonts || []).map(f => ({
    name: f.name,
    category: 'Custom',
    style: { fontFamily: f.name },
    description: 'Dein eigener Upload',
    isCustom: true
  }));

  const allFonts = [...customFonts, ...defaultFonts];

  return (
    <div className="space-y-3">
      {allFonts.map((font) => (
        <button
          key={font.name}
          onClick={() => onFontSelect(font.name)}
          className={`w-full p-4 text-left border-2 rounded-lg transition-all ${
            selectedFont === font.name 
              ? 'border-purple-500 bg-purple-50' 
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-1" style={font.style}>
                {font.name}
              </h3>
              <p className="text-sm text-gray-600">{font.description}</p>
            </div>
            <span className={`text-xs px-2 py-1 rounded ${font.isCustom ? 'bg-purple-100 text-purple-700 font-bold' : 'bg-gray-100 text-gray-500'}`}>
              {font.isCustom ? <><SafeIcon icon={FiIcons.FiUpload} className="inline mr-1"/> Custom</> : font.category}
            </span>
          </div>
          <div className="mt-3 text-2xl text-gray-800" style={font.style}>
            The quick brown fox jumps
          </div>
        </button>
      ))}
    </div>
  );
};

export default FontSelector;