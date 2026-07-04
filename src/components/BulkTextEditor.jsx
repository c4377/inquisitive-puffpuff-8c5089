import React, { useState } from 'react';
import { FiFileText, FiMinus, FiPlus, FiRefreshCw, FiMove, FiCheck, FiLayers } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import { assignSmartLayouts, attachSmartImages } from '../utils/smartLayoutGenerator';

const BulkTextEditor = ({ slides, setSlides, onClose, currentSlides, onUpdateSlides }) => {
  const { brandSettings } = useBrand();
  const brand = brandSettings?.currentBrandConfig || {};
  // The Editor passes currentSlides/onUpdateSlides — support both prop shapes.
  const slideList = slides || currentSlides || [];
  const commitSlides = setSlides || onUpdateSlides || (() => {});
  // Initialize with current slides content joined by "Slide X" markers or new empty string
  const [inputText, setInputText] = useState(
    slideList.length > 0 
      ? slideList.map((s, i) => `Slide ${i + 1}:\n${s.text}`).join('\n\n') 
      : ''
  );

  const handleProcess = async () => {
    // 1. Basic Split
    const rawSegments = inputText.split(/Slide \d+:/i).filter(t => t.trim());
    
    // 2. Create Raw Slide Objects
    const rawSlides = rawSegments.map((text, index) => ({
      id: Date.now() + index,
      text: text.trim(),
      secondaryText: '', // Will be filled by smart engine
      layoutId: 'centered', // Will be overwritten
    }));

    // 3. Apply Smart Layout Engine
    const smartSlides = assignSmartLayouts(rawSlides, brand);

    // 4. Auto-attach background images from the global Brand pool,
    //    matched to each slide's text position (fresh analysis each run).
    const imagePool = brandSettings?.brandImages || [];
    const withImages = await attachSmartImages(smartSlides, imagePool);

    commitSlides(withImages);
    if (onClose) onClose();
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-bold text-gray-800 flex items-center gap-2">
          <SafeIcon icon={FiLayers} className="text-purple-600" />
          Smart Bulk Import
        </h3>
        <button 
          onClick={handleProcess}
          className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2"
        >
          <SafeIcon icon={FiCheck} />
          Generate Carousel
        </button>
      </div>

      <p className="text-sm text-gray-500 mb-2">
        Paste your script here. Use "Slide 1:", "Slide 2:" to separate. 
        The <strong>Smart Engine</strong> will automatically detect the best layout (Editorial, Split, Boxed) 
        and highlight key phrases for you.
      </p>

      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        className="w-full h-96 p-4 border rounded-lg font-mono text-sm focus:ring-2 focus:ring-purple-500 outline-none"
        placeholder={`Slide 1:
Your headline here...
Your body text...

Slide 2:
Next point...`}
      />
    </div>
  );
};

export default BulkTextEditor;