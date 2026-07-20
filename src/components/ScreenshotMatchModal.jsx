import React, { useState, useRef } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { parseScreenshotPlaceholder, ocrImage, matchScreenshots } from '../utils/screenshotMatcher';

const { FiX, FiUploadCloud, FiCheckCircle, FiLoader, FiImage } = FiIcons;

const fileToDataUrl = (file) => new Promise((res, rej) => {
  const r = new FileReader();
  r.onload = () => res(r.result);
  r.onerror = rej;
  r.readAsDataURL(file);
});

// Modal: upload screenshots, OCR them, auto-match to [SCREENSHOT — …] slides.
// onApply(mapping) receives { placeholderSlideKey: screenshotDataUrl }.
const ScreenshotMatchModal = ({ isOpen, onClose, placeholders, onApply }) => {
  const [screenshots, setScreenshots] = useState([]); // {id, dataUrl, ocrText, progress}
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null); // mapping placeholderId -> {screenshotId, score}
  const inputRef = useRef(null);

  if (!isOpen) return null;

  const handleFiles = async (files) => {
    const list = Array.from(files || []);
    if (list.length === 0) return;
    setBusy(true);
    setResult(null);
    const next = [];
    for (let i = 0; i < list.length; i++) {
      const dataUrl = await fileToDataUrl(list[i]);
      const id = `s_${Date.now()}_${i}`;
      const entry = { id, dataUrl, ocrText: '', progress: 0 };
      next.push(entry);
      setScreenshots((prev) => [...prev, entry]);
      // OCR this screenshot.
      const text = await ocrImage(dataUrl, (p) => {
        setScreenshots((prev) => prev.map((s) => (s.id === id ? { ...s, progress: p } : s)));
      });
      entry.ocrText = text;
      setScreenshots((prev) => prev.map((s) => (s.id === id ? { ...s, ocrText: text, progress: 1 } : s)));
    }
    // Match once all are read.
    const mapping = matchScreenshots(placeholders, next);
    setResult(mapping);
    setBusy(false);
  };

  const apply = () => {
    if (!result) return;
    // Convert to placeholderId -> dataUrl for the caller.
    const out = {};
    Object.entries(result).forEach(([pid, v]) => {
      const shot = screenshots.find((s) => s.id === v.screenshotId);
      if (shot) out[pid] = shot.dataUrl;
    });
    onApply(out);
    onClose();
  };

  const matchedCount = result ? Object.keys(result).length : 0;

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4">
      <div className="bg-white w-full sm:max-w-lg sm:rounded-2xl rounded-t-2xl max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-100 px-5 py-4 flex items-center justify-between">
          <div>
            <h3 className="font-bold text-gray-900">Screenshots zuordnen</h3>
            <p className="text-xs text-gray-500">{placeholders.length} Platzhalter im Plan</p>
          </div>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-700"><SafeIcon icon={FiX} /></button>
        </div>

        <div className="p-5 space-y-4">
          {placeholders.length === 0 ? (
            <p className="text-sm text-gray-500 bg-gray-50 rounded-xl p-4">
              Keine <span className="font-mono text-xs">[SCREENSHOT — …]</span>-Platzhalter im aktuellen Plan gefunden. Füge sie per Bulk Import ein, z.&nbsp;B.:
              <span className="block mt-2 font-mono text-xs bg-white border border-gray-200 rounded p-2">[SCREENSHOT — "Btw: 30 Anmeldungen für den Workshop"]</span>
            </p>
          ) : (
            <>
              <button
                onClick={() => inputRef.current?.click()}
                disabled={busy}
                className="w-full border-2 border-dashed border-purple-200 rounded-xl py-6 flex flex-col items-center gap-2 text-purple-600 hover:bg-purple-50 disabled:opacity-50"
              >
                <SafeIcon icon={FiUploadCloud} className="text-2xl" />
                <span className="text-sm font-bold">Screenshots hochladen</span>
                <span className="text-xs text-gray-400">Mehrere auf einmal möglich</span>
              </button>
              <input ref={inputRef} type="file" accept="image/*" multiple className="hidden"
                onChange={(e) => handleFiles(e.target.files)} />

              {screenshots.length > 0 && (
                <div className="space-y-2">
                  {screenshots.map((s) => (
                    <div key={s.id} className="flex items-center gap-3 bg-gray-50 rounded-lg p-2">
                      <img src={s.dataUrl} alt="" className="w-12 h-12 object-cover rounded-md border border-gray-200" />
                      <div className="flex-1 min-w-0">
                        {s.progress < 1 ? (
                          <div className="flex items-center gap-2 text-xs text-gray-500">
                            <SafeIcon icon={FiLoader} className="animate-spin" />
                            OCR läuft… {Math.round((s.progress || 0) * 100)}%
                          </div>
                        ) : (
                          <p className="text-xs text-gray-600 truncate">{s.ocrText.slice(0, 60) || '(kein Text erkannt)'}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {result && (
                <div className="bg-green-50 border border-green-200 rounded-xl p-3 flex items-center gap-2 text-sm text-green-800">
                  <SafeIcon icon={FiCheckCircle} />
                  {matchedCount} von {placeholders.length} Platzhaltern automatisch zugeordnet.
                </div>
              )}
            </>
          )}
        </div>

        {placeholders.length > 0 && (
          <div className="sticky bottom-0 bg-white border-t border-gray-100 px-5 py-3 flex gap-2">
            <button onClick={onClose} className="flex-1 py-2.5 rounded-lg border border-gray-200 text-sm font-bold text-gray-600">Abbrechen</button>
            <button onClick={apply} disabled={!result || matchedCount === 0 || busy}
              className="flex-1 py-2.5 rounded-lg bg-purple-600 text-white text-sm font-bold disabled:opacity-40">
              Platzieren
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScreenshotMatchModal;
