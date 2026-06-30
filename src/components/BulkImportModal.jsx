import React, { useState } from 'react';
import { FiDownloadCloud, FiX, FiFileText, FiAlertCircle, FiClipboard } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { parseSmartInput } from '../utils/textParser';

const BulkImportModal = ({ isOpen, onClose, onImportPlan }) => {
  const [inputContent, setInputContent] = useState('');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleProcessInput = () => {
    setError('');
    const parsedDays = parseSmartInput(inputContent);
    
    if (parsedDays.length === 0) {
      setError("Konnte keinen Plan erkennen. Bitte nutze 'Tag 1' für Tage und 'Slide 1' für Folien.");
      return;
    }
    
    onImportPlan(parsedDays);
    onClose();
  };

  const insertTemplate = () => {
    const template = `Tag 1: Mein Thema
Slide 1: Das ist die Headline
Slide 2: Das ist der erste Inhaltspunkt
Slide 3: Hier kommt ein Fazit

Tag 2: Nächstes Thema
Slide 1: Neue Headline
Slide 2: Weiterer Content...`;
    setInputContent(template);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* HEADER */}
        <div className="bg-gradient-to-r from-purple-900 to-purple-800 p-6 flex justify-between items-center text-white">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 p-2 rounded-lg">
              <SafeIcon icon={FiFileText} className="text-2xl text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold">Bulk Content Import</h2>
              <p className="text-xs text-purple-200">Füge deinen fertigen Text ein.</p>
            </div>
          </div>
          <button onClick={onClose} className="text-purple-200 hover:text-white transition-colors">
            <SafeIcon icon={FiX} className="text-2xl" />
          </button>
        </div>

        {/* CONTENT */}
        <div className="p-6 overflow-y-auto flex-1 flex flex-col">
          {error && (
            <div className="mb-4 bg-red-50 text-red-600 p-3 rounded-lg text-sm flex items-center border border-red-100">
              <SafeIcon icon={FiAlertCircle} className="mr-2" /> {error}
            </div>
          )}

          <div className="flex justify-between items-center mb-2">
            <label className="text-sm font-bold text-gray-700">Dein Content (Text)</label>
            <button 
              onClick={insertTemplate} 
              className="text-xs text-purple-600 font-bold flex items-center hover:bg-purple-50 px-2 py-1 rounded transition-colors"
            >
              <SafeIcon icon={FiClipboard} className="mr-1" /> Beispiel einfügen
            </button>
          </div>

          <div className="bg-blue-50 p-3 rounded-lg border border-blue-100 mb-3 text-xs text-blue-800">
            <strong>Format:</strong> Nutze "Tag 1" für neue Tage und "Slide 1" (oder "Folie 1") für einzelne Slides.
          </div>

          <textarea 
            value={inputContent} 
            onChange={(e) => setInputContent(e.target.value)} 
            placeholder={`Tag 1: Titel des Posts\nSlide 1: Deine Headline hier...\nSlide 2: Dein Text...\n\nTag 2: ...`}
            className="w-full flex-1 p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 font-mono text-sm leading-relaxed min-h-[300px] resize-none"
          />
        </div>

        {/* FOOTER */}
        <div className="p-6 border-t border-gray-100 bg-gray-50">
          <button 
            onClick={handleProcessInput} 
            disabled={!inputContent.trim()}
            className="w-full py-4 bg-purple-600 text-white rounded-xl font-bold flex items-center justify-center hover:bg-purple-700 disabled:opacity-50 transition-all shadow-md text-lg"
          >
            <SafeIcon icon={FiDownloadCloud} className="mr-2" /> Plan erstellen & Design anwenden
          </button>
        </div>
      </div>
    </div>
  );
};

export default BulkImportModal;