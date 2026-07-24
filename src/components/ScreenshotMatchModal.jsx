import React, { useState, useRef, useEffect } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { parseScreenshotPlaceholder, ocrImage, matchScreenshots } from '../utils/screenshotMatcher';
import { CloudService } from '../services/cloudService';

const { FiX, FiUploadCloud, FiCheckCircle, FiLoader, FiImage } = FiIcons;

const fileToDataUrl = (file) => new Promise((res, rej) => {
  const r = new FileReader();
  r.onload = () => res(r.result);
  r.onerror = rej;
  r.readAsDataURL(file);
});

// Shrink a screenshot before uploading. Phone screenshots are 3–4 MB, but the
// app never displays them larger than a tile — and every view re-downloads the
// full file, which is what runs up Supabase egress. Max 1400px wide keeps it
// crisp even when a tile is opened large. OCR still runs on the ORIGINAL, so
// matching quality is unaffected.
const shrinkDataUrl = (dataUrl, maxWidth = 1080, quality = 0.85) =>
  new Promise((resolve) => {
    try {
      const img = new Image();
      img.onload = () => {
        try {
          const scale = img.width > maxWidth ? maxWidth / img.width : 1;
          const c = document.createElement('canvas');
          c.width = Math.round(img.width * scale);
          c.height = Math.round(img.height * scale);
          const ctx = c.getContext('2d');
          ctx.drawImage(img, 0, 0, c.width, c.height);
          // Always re-encode as JPEG: a 4 MB PNG screenshot becomes a few
          // hundred KB, which is the bulk of the egress saving.
          resolve(c.toDataURL('image/jpeg', quality));
        } catch (e) { resolve(dataUrl); }
      };
      img.onerror = () => resolve(dataUrl);
      img.src = dataUrl;
    } catch (e) { resolve(dataUrl); }
  });

// Modal: upload screenshots, OCR them, auto-match to [SCREENSHOT — …] slides.
// onApply(mapping) receives { placeholderSlideKey: screenshotDataUrl }.
const ScreenshotMatchModal = ({ isOpen, onClose, placeholders, onApply }) => {
  const [screenshots, setScreenshots] = useState([]); // {id, dataUrl, ocrText, progress}
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null); // mapping placeholderId -> {screenshotId, score}
  const [libraryCount, setLibraryCount] = useState(null); // null = loading
  const [libraryError, setLibraryError] = useState(null);
  const [saveError, setSaveError] = useState(null);
  const inputRef = useRef(null);

  // On open: pull the stored screenshot library (uploaded once, kept forever)
  // and immediately try to fill every placeholder from it. Only what's still
  // missing needs a fresh upload.
  useEffect(() => {
    if (!isOpen) return;
    let cancelled = false;
    (async () => {
      setLibraryCount(null);
      setLibraryError(null);
      setSaveError(null);
      const { items, error } = await CloudService.loadScreenshotLibrary();
      if (cancelled) return;
      if (error) setLibraryError(error);
      const asShots = items.map((entry, i) => ({
        id: `lib_${i}`,
        dataUrl: entry.url,
        ocrText: entry.ocrText,
        progress: 1,
        fromLibrary: true,
      }));
      setScreenshots(asShots);
      setLibraryCount(asShots.length);
      if (asShots.length > 0 && placeholders.length > 0) {
        setResult(matchScreenshots(placeholders, asShots));
      }
    })();
    return () => { cancelled = true; };
  }, [isOpen, placeholders.length]);

  if (!isOpen) return null;

  const handleFiles = async (files) => {
    const list = Array.from(files || []);
    if (list.length === 0) return;
    setBusy(true);
    const added = [];
    for (let i = 0; i < list.length; i++) {
      const dataUrl = await fileToDataUrl(list[i]);
      const id = `s_${Date.now()}_${i}`;
      const entry = { id, dataUrl, ocrText: '', progress: 0 };
      added.push(entry);
      setScreenshots((prev) => [...prev, entry]);
      // OCR this screenshot.
      const text = await ocrImage(dataUrl, (p) => {
        setScreenshots((prev) => prev.map((s) => (s.id === id ? { ...s, progress: p } : s)));
      });
      entry.ocrText = text;
      setScreenshots((prev) => prev.map((s) => (s.id === id ? { ...s, ocrText: text, progress: 1 } : s)));

      // Store it permanently: upload once, remember the OCR text alongside, so
      // future imports can match against it without re-uploading. The uploaded
      // copy is resized (OCR above already ran on the full-size original).
      const uploadUrl = await shrinkDataUrl(dataUrl);
      const url = await CloudService.uploadScreenshot(uploadUrl);
      if (/^https?:\/\//.test(url)) {
        const res = await CloudService.addToScreenshotLibrary({ url, ocrText: text });
        if (!res.ok) setSaveError(res.error);
        entry.dataUrl = url;
        setScreenshots((prev) => prev.map((s) => (s.id === id ? { ...s, dataUrl: url } : s)));
      } else {
        setSaveError('Upload in den Bucket fehlgeschlagen – Screenshot bleibt nur lokal.');
      }
    }
    // Re-match against the full set (library + newly added).
    setScreenshots((prev) => {
      setResult(matchScreenshots(placeholders, prev));
      return prev;
    });
    setBusy(false);
  };

  const apply = async () => {
    if (!result) return;
    // Convert to placeholderId -> dataUrl for the caller.
    const out = {};
    Object.entries(result).forEach(([pid, v]) => {
      const shot = screenshots.find((s) => s.id === v.screenshotId);
      if (shot) out[pid] = shot.dataUrl;
    });
    setBusy(true);
    try {
      await onApply(out); // uploads to storage; may be async
    } catch (e) { /* handled upstream */ }
    setBusy(false);
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
              {libraryError && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-3 text-sm text-red-800">
                  <p className="font-bold mb-1">Bibliothek nicht verfügbar</p>
                  <p className="text-xs">{libraryError}</p>
                  <p className="text-xs mt-1 text-red-600">Screenshots müssen deshalb jedes Mal neu geladen werden.</p>
                </div>
              )}
              {saveError && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 text-xs text-amber-800">
                  Nicht dauerhaft gespeichert: {saveError}
                </div>
              )}
              {!libraryError && libraryCount !== null && libraryCount > 0 && (
                <div className="bg-purple-50 border border-purple-200 rounded-xl p-3 text-sm text-purple-800">
                  {libraryCount} Screenshots in deiner Bibliothek – automatisch abgeglichen.
                </div>
              )}
              {!libraryError && libraryCount === 0 && (
                <div className="bg-gray-50 border border-gray-200 rounded-xl p-3 text-xs text-gray-600">
                  Bibliothek ist noch leer. Was du jetzt hochlädst, bleibt dauerhaft gespeichert.
                </div>
              )}

              <button
                onClick={() => inputRef.current?.click()}
                disabled={busy}
                className="w-full border-2 border-dashed border-purple-200 rounded-xl py-6 flex flex-col items-center gap-2 text-purple-600 hover:bg-purple-50 disabled:opacity-50"
              >
                <SafeIcon icon={FiUploadCloud} className="text-2xl" />
                <span className="text-sm font-bold">Screenshots hochladen</span>
                <span className="text-xs text-gray-400">Einmal hochladen – bleibt dauerhaft gespeichert</span>
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
