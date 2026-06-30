import React, { useState } from 'react';
import { FiSun, FiDroplet, FiActivity, FiMaximize, FiMove, FiLayers, FiImage, FiCircle, FiSquare, FiAlertCircle } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const ImageEffects = ({ overlay, blur, grain, imageScale, imageX, imageY, overlayImageScale, overlayImageX, overlayImageY, overlayImageRounded, onUpdate }) => {
  const [activeTab, setActiveTab] = useState('background'); // 'background' or 'overlay'
  
  return (
    <div className="space-y-6">
      {/* TABS FOR TARGET */}
      <div className="flex bg-gray-100 p-1 rounded-lg">
        <button onClick={() => setActiveTab('background')} className={`flex-1 py-2 text-xs font-bold rounded-md transition-all ${activeTab === 'background' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}>
          <SafeIcon icon={FiImage} className="inline mr-1" /> Hintergrund
        </button>
        <button onClick={() => setActiveTab('overlay')} className={`flex-1 py-2 text-xs font-bold rounded-md transition-all ${activeTab === 'overlay' ? 'bg-white shadow text-purple-700' : 'text-gray-500 hover:text-gray-700'}`}>
          <SafeIcon icon={FiLayers} className="inline mr-1" /> Logo / Sticker
        </button>
      </div>

      {activeTab === 'background' ? (
        <div className="animate-fade-in space-y-6">
          <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-5">
            <h3 className="text-xs font-bold text-gray-900 uppercase flex items-center border-b border-gray-100 pb-2">
              <SafeIcon icon={FiMove} className="mr-1.5 text-purple-600"/> Position & Zoom (BG)
            </h3>
            {/* Zoom */}
            <div>
              <label className="flex justify-between items-center text-sm font-medium text-gray-700 mb-2">
                <div className="flex items-center"><SafeIcon icon={FiMaximize} className="mr-2 text-gray-400" /> Zoom</div>
                <span className="text-xs font-mono bg-gray-50 px-2 py-1 rounded border border-gray-200 text-gray-600">x{Number(imageScale || 1).toFixed(2)}</span>
              </label>
              <input type="range" min="1" max="3" step="0.05" value={imageScale || 1} onChange={(e) => onUpdate({ imageScale: parseFloat(e.target.value) })} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" />
            </div>
             {/* X / Y Position */}
            <div className="grid grid-cols-2 gap-4 pt-1">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Horizontal X</span>
                  <span className="text-[10px] text-gray-400 font-mono">{imageX || 0}</span>
                </div>
                <input type="range" min="-300" max="300" value={imageX || 0} onChange={(e) => onUpdate({ imageX: parseInt(e.target.value) })} className="w-full h-1.5 bg-gray-200 rounded-lg accent-purple-600" />
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Vertikal Y</span>
                  <span className="text-[10px] text-gray-400 font-mono">{imageY || 0}</span>
                </div>
                <input type="range" min="-300" max="300" value={imageY || 0} onChange={(e) => onUpdate({ imageY: parseInt(e.target.value) })} className="w-full h-1.5 bg-gray-200 rounded-lg accent-purple-600" />
              </div>
            </div>
          </div>
          {/* FILTER & EFFECTS */}
          <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-5 opacity-90 hover:opacity-100 transition-opacity">
            <h3 className="text-xs font-bold text-gray-500 uppercase flex items-center">
              <SafeIcon icon={FiDroplet} className="mr-1.5"/> Filter & Overlay
            </h3>
            <div>
              <label className="flex justify-between items-center text-sm font-medium text-gray-700 mb-2">
                <div className="flex items-center"><SafeIcon icon={FiSun} className="mr-2 text-gray-400"/> Abdunkeln</div>
                <span className="text-xs font-mono bg-white px-2 py-1 rounded border border-gray-200">{Math.round((overlay || 0) * 100)}%</span>
              </label>
              <input type="range" min="0" max="0.9" step="0.05" value={overlay || 0} onChange={(e) => onUpdate({ overlay: parseFloat(e.target.value) })} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" />
            </div>
            <div>
              <label className="flex justify-between items-center text-sm font-medium text-gray-700 mb-2">
                <div className="flex items-center"><SafeIcon icon={FiDroplet} className="mr-2 text-gray-400" /> Unschärfe (Blur)</div>
                <span className="text-xs font-mono bg-white px-2 py-1 rounded border border-gray-200">{blur || 0}px</span>
              </label>
              <input type="range" min="0" max="20" step="1" value={blur || 0} onChange={(e) => onUpdate({ blur: parseInt(e.target.value) })} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" />
            </div>
            <div>
              <label className="flex justify-between items-center text-sm font-medium text-gray-700 mb-2">
                <div className="flex items-center"><SafeIcon icon={FiActivity} className="mr-2 text-gray-400" /> Körnung (Grain)</div>
                <span className="text-xs font-mono bg-white px-2 py-1 rounded border border-gray-200">{Math.round((grain || 0) * 100)}%</span>
              </label>
              <input type="range" min="0" max="0.5" step="0.01" value={grain || 0} onChange={(e) => onUpdate({ grain: parseFloat(e.target.value) })} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" />
            </div>
          </div>
        </div>
      ) : (
        <div className="animate-fade-in space-y-6">
          <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-5">
            <h3 className="text-xs font-bold text-gray-900 uppercase flex items-center border-b border-gray-100 pb-2">
              <SafeIcon icon={FiLayers} className="mr-1.5 text-purple-600"/> Logo / Sticker Position
            </h3>
            {/* Shape Toggle */}
            <div className="flex space-x-2 mb-2">
              <button onClick={() => onUpdate({ overlayImageRounded: false })} className={`flex-1 py-2 flex items-center justify-center border rounded-lg ${!overlayImageRounded ? 'bg-purple-100 border-purple-500 text-purple-700' : 'bg-white border-gray-200 text-gray-500'}`}>
                <SafeIcon icon={FiSquare} className="mr-1"/> Eckig
              </button>
              <button onClick={() => onUpdate({ overlayImageRounded: true })} className={`flex-1 py-2 flex items-center justify-center border rounded-lg ${overlayImageRounded ? 'bg-purple-100 border-purple-500 text-purple-700' : 'bg-white border-gray-200 text-gray-500'}`}>
                <SafeIcon icon={FiCircle} className="mr-1"/> Rund
              </button>
            </div>
            {/* Scale */}
            <div>
              <label className="flex justify-between items-center text-sm font-medium text-gray-700 mb-2">
                <div className="flex items-center"><SafeIcon icon={FiMaximize} className="mr-2 text-gray-400" /> Größe</div>
                <span className="text-xs font-mono bg-gray-50 px-2 py-1 rounded border border-gray-200 text-gray-600">{Math.round((overlayImageScale || 0.3) * 100)}%</span>
              </label>
              <input type="range" min="0.1" max="1.5" step="0.05" value={overlayImageScale || 0.3} onChange={(e) => onUpdate({ overlayImageScale: parseFloat(e.target.value) })} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" />
            </div>
            {/* X / Y Position */}
            <div className="grid grid-cols-2 gap-4 pt-1">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Horizontal X</span>
                </div>
                <input type="range" min="-300" max="300" value={overlayImageX || 0} onChange={(e) => onUpdate({ overlayImageX: parseInt(e.target.value) })} className="w-full h-1.5 bg-gray-200 rounded-lg accent-purple-600" />
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Vertikal Y</span>
                </div>
                <input type="range" min="-300" max="300" value={overlayImageY || 0} onChange={(e) => onUpdate({ overlayImageY: parseInt(e.target.value) })} className="w-full h-1.5 bg-gray-200 rounded-lg accent-purple-600" />
              </div>
            </div>
          </div>
          {!overlayImageScale && (
            <div className="p-3 bg-yellow-50 text-yellow-800 rounded-lg text-xs border border-yellow-100 flex items-start">
              <SafeIcon icon={FiAlertCircle} className="mr-2 mt-0.5 flex-shrink-0" />
              <div><strong>Hinweis:</strong> Um diese Regler zu nutzen, musst du zuerst ein Logo im Tab "Bilder & Uploads" &gt; "Logo / Sticker" hochladen.</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageEffects;