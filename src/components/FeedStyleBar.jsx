import React, { useState, useRef, useEffect } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const { FiDroplet, FiType } = FiIcons;

// Always-visible bar above the feed. Editing a colour or the font here calls
// onColors / onFont, which cascade to EVERY slide immediately (same path the
// Brand Settings use), so the whole feed updates live.
const FONTS = [
  'AspektaBrand', 'HelveticaNeueBrand',
  'Playfair Display', 'Cormorant Garamond', 'Montserrat',
  'Inter', 'Outfit', 'Poppins', 'Caveat', 'La Belle Aurore', 'Courier Prime',
];

// A native <input type="color"> fires onChange continuously while dragging. If
// we restyled the whole feed on every tick it would run dozens of times per
// second and crash the app. So we preview the colour locally and only COMMIT
// (restyle the feed) when the user releases the picker.
const Swatch = ({ label, value, onChange }) => {
  const [local, setLocal] = useState(value || '#000000');
  useEffect(() => { setLocal(value || '#000000'); }, [value]);
  return (
    <label className="flex items-center gap-1.5 cursor-pointer group" title={label}>
      <span
        className="w-7 h-7 rounded-full border-2 border-white shadow ring-1 ring-gray-200 relative overflow-hidden"
        style={{ background: local }}
      >
        <input
          type="color"
          value={local}
          onChange={(e) => setLocal(e.target.value)}          // live preview only
          onBlur={(e) => onChange(e.target.value)}            // commit on release
          onMouseUp={(e) => onChange(e.target.value)}         // commit (desktop)
          onTouchEnd={() => onChange(local)}                  // commit (mobile)
          className="absolute inset-0 opacity-0 cursor-pointer"
        />
      </span>
      <span className="text-[10px] font-bold text-gray-500 hidden sm:inline">{label}</span>
    </label>
  );
};

const FeedStyleBar = ({ colors, typography, onColors, onFont }) => {
  if (!colors || !typography) return null;

  const setColor = (key, val) => onColors({ ...colors, [key]: val });

  return (
    <div className="flex items-center gap-3 flex-wrap bg-white border border-gray-200 rounded-xl px-3 py-2.5 shadow-sm mb-4">
      <div className="flex items-center gap-1 text-gray-400">
        <SafeIcon icon={FiDroplet} className="text-sm" />
        <span className="text-[10px] font-bold uppercase tracking-wider hidden sm:inline">Farben</span>
      </div>
      <div className="flex items-center gap-3">
        <Swatch label="Text" value={colors.primary} onChange={(v) => setColor('primary', v)} />
        <Swatch label="Fläche" value={colors.background} onChange={(v) => setColor('background', v)} />
        <Swatch label="Akzent" value={colors.accent} onChange={(v) => setColor('accent', v)} />
        <Swatch label="Zweit" value={colors.secondary} onChange={(v) => setColor('secondary', v)} />
      </div>

      <div className="w-px h-6 bg-gray-200 mx-1 hidden sm:block" />

      <div className="flex items-center gap-2 flex-1 min-w-[140px]">
        <SafeIcon icon={FiType} className="text-sm text-gray-400" />
        <select
          value={typography.fontFamily || 'Playfair Display'}
          onChange={(e) => onFont(e.target.value)}
          className="flex-1 text-xs font-bold bg-gray-50 border border-gray-200 rounded-lg px-2 py-1.5 focus:border-purple-400 focus:outline-none"
          style={{ fontFamily: typography.fontFamily }}
        >
          {FONTS.map((f) => (
            <option key={f} value={f} style={{ fontFamily: f }}>{f}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default FeedStyleBar;
