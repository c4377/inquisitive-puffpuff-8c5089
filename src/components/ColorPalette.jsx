import React, { useMemo } from 'react';
import { useBrand } from '../context/BrandContext';

const ColorPalette = ({ selectedColor, onColorSelect }) => {
  const { brandSettings } = useBrand();

  const colorPalettes = [
    { name: 'Cool Spring', colors: ['#647D82', '#8D9F79', '#D0B400', '#B6B4B6', '#FFFFFF'] }, // NEW
    { name: 'Health & Mindset', colors: ['#0F4C5C', '#FFFFFF', '#94A3B8', '#38BDF8', '#000000'] },
    { name: 'Noir Luxe', colors: ['#000000', '#FFFFFF', '#1A1A1A', '#333333', '#F5F5F5'] },
    { name: 'Beige Aesthetic', colors: ['#2C1810', '#8C8682', '#D6D1CC', '#EBE9E6', '#F5F2EF'] },
    { name: 'Deep Forest', colors: ['#022C22', '#052e16', '#14532D', '#C1A87D', '#FDFCF8'] },
    { name: 'Midnight Navy', colors: ['#020617', '#0F172A', '#1E293B', '#94A3B8', '#F8FAFC'] },
    { name: 'Soho Luxury', colors: ['#0B3D59', '#FFFFFF', '#041C2C', '#FACC15', '#407E8C'] },
    { name: 'Cherry Bomb', colors: ['#450a0a', '#7f1d1d', '#991b1b', '#DC2626', '#FFFFFF'] },
    { name: 'Espresso', colors: ['#150F0D', '#261917', '#3E2723', '#8D6E63', '#FFF8E1'] }
  ];

  const monochromeColors = [
    '#000000', '#1A1A1A', '#333333', '#666666', '#999999', '#CCCCCC', '#E5E5E5', '#FFFFFF'
  ];

  // Helper function to resolve color names to hex for input[type=color]
  const resolveColorToHex = (colorStr) => {
    if (!colorStr) return '#000000';
    if (colorStr.startsWith('#')) {
      if (colorStr.length === 7) return colorStr;
      if (colorStr.length === 4) {
        return '#' + colorStr[1] + colorStr[1] + colorStr[2] + colorStr[2] + colorStr[3] + colorStr[3];
      }
      return '#000000';
    }
    // Attempt to resolve named color using a temporary element
    const ctx = document.createElement('canvas').getContext('2d');
    ctx.fillStyle = colorStr;
    const computed = ctx.fillStyle;
    return computed; // returns hex or #000000 if invalid
  };

  const hexToHSL = (hex) => {
    let fullHex = hex;
    if (hex.length === 4) {
       fullHex = '#' + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3];
    }
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(fullHex);
    if (!result) return { h: 0, s: 0, l: 0 };
    let r = parseInt(result[1], 16);
    let g = parseInt(result[2], 16);
    let b = parseInt(result[3], 16);
    r /= 255; g /= 255; b /= 255;
    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    if (max === min) {
      h = s = 0;
    } else {
      let d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
        default: break;
      }
      h /= 6;
    }
    return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
  };

  const hslToHex = (h, s, l) => {
    l /= 100;
    const a = s * Math.min(l, 1 - l) / 100;
    const f = n => {
      const k = (n + h / 30) % 12;
      const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
      return Math.round(255 * color).toString(16).padStart(2, '0');
    };
    return `#${f(0)}${f(8)}${f(4)}`;
  };

  const brandNuances = useMemo(() => {
    const colors = brandSettings.currentBrandConfig?.colors;
    if (!colors) return [];
    
    const anchors = [colors.primary, colors.secondary, colors.accent]
      .filter(c => c && typeof c === 'string');
      
    if (anchors.length === 0) return [];
    
    const variations = [];
    const clamp = (val, min, max) => Math.min(Math.max(val, min), max);

    anchors.forEach(color => {
      // Must resolve name to hex for HSL math
      const hex = resolveColorToHex(color);
      if (hex === '#000000' && color !== 'black' && color !== '#000000' && color !== '#000') return;

      const { h, s, l } = hexToHSL(hex);
      variations.push(hex);
      variations.push(hslToHex(h, s, clamp(l + 10, 0, 100)));
      variations.push(hslToHex(h, s, clamp(l - 10, 0, 100)));
    });

    return [...new Set(variations)].slice(0, 12);
  }, [brandSettings.currentBrandConfig]);

  return (
    <div className="space-y-6">
      {/* Custom Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Custom Color
        </label>
        <div className="flex items-center space-x-3">
          <div className="relative">
            <input
              type="color"
              value={resolveColorToHex(selectedColor)}
              onChange={(e) => onColorSelect(e.target.value)}
              className="w-12 h-12 border border-gray-300 rounded-lg cursor-pointer shadow-sm p-0 overflow-hidden"
            />
          </div>
          <input
            type="text"
            value={selectedColor || '#000000'}
            onChange={(e) => onColorSelect(e.target.value)}
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent uppercase font-mono text-sm"
            placeholder="#000000 or purple"
          />
        </div>
      </div>

      {/* Brand Nuances */}
      {brandNuances.length > 0 && (
        <div className="animate-fade-in">
          <label className="block text-sm font-medium text-gray-700 mb-3 flex items-center justify-between">
            <span>Brand Nuances</span>
          </label>
          <div className="grid grid-cols-6 gap-2">
            {brandNuances.map((color, idx) => (
              <button
                key={`${color}-${idx}`}
                onClick={() => onColorSelect(color)}
                className={`w-full aspect-square rounded-lg border border-gray-300 shadow-sm hover:scale-110 hover:shadow-md transition-all duration-200 ${
                  resolveColorToHex(selectedColor) === resolveColorToHex(color) ? 'ring-2 ring-purple-500 ring-offset-1 scale-105' : ''
                }`}
                style={{ backgroundColor: color }}
                title={color}
              />
            ))}
          </div>
        </div>
      )}

      {/* Modern Palettes */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Aesthetic Palettes
        </label>
        <div className="space-y-4">
          {colorPalettes.map((palette) => (
            <div key={palette.name}>
               <h4 className="text-xs font-medium text-gray-600 mb-2">{palette.name}</h4>
               <div className="flex space-x-2">
                {palette.colors.map((color) => (
                  <button
                    key={color}
                    onClick={() => onColorSelect(color)}
                    className={`w-10 h-10 rounded-lg border border-gray-300 shadow-sm transition-all ${
                      resolveColorToHex(selectedColor) === resolveColorToHex(color) ? 'border-gray-900 scale-110 ring-2 ring-gray-100' : 'hover:border-gray-400'
                    }`}
                    style={{ backgroundColor: color }}
                    title={color}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Monochrome */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Monochrome
        </label>
        <div className="flex flex-wrap gap-2">
          {monochromeColors.map((color) => (
            <button
              key={color}
              onClick={() => onColorSelect(color)}
              className={`w-8 h-8 rounded-lg border border-gray-300 shadow-sm transition-all ${
                resolveColorToHex(selectedColor) === resolveColorToHex(color) ? 'border-gray-900 scale-110' : 'hover:border-gray-400'
              }`}
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ColorPalette;