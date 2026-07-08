import React, { useState, useRef, useEffect } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import { motion, AnimatePresence } from 'framer-motion';
import StyleShifter from '../components/StyleShifter';

const { FiFileText, FiDownload, FiRefreshCw, FiZap, FiEye, FiEdit3, FiAlignLeft } = FiIcons;

const WorksheetGenerator = () => {
  const { brandSettings } = useBrand();
  
  // --- CONFIG SAFETY ---
  const defaultConfig = {
    colors: { primary: '#000000', secondary: '#CCCCCC', accent: '#EA580C', background: '#FFFFFF' },
    typography: { fontFamily: 'Inter', bodyFontFamily: 'Inter', accentFontFamily: 'Inter' },
    name: ''
  };

  const activeConfig = brandSettings.currentBrandConfig || {};
  const config = {
    ...defaultConfig,
    ...activeConfig,
    colors: { ...defaultConfig.colors, ...(activeConfig.colors || {}) },
    typography: { ...defaultConfig.typography, ...(activeConfig.typography || {}) },
    name: activeConfig.name || defaultConfig.name
  };

  const previewRef = useRef(null);
  const [isExporting, setIsExporting] = useState(false);
  const [zoom, setZoom] = useState(0.65);
  const [activeTab, setActiveTab] = useState('editor'); // 'editor' | 'preview'
  const [showShifter, setShowShifter] = useState(false);

  // --- SINGLE SOURCE OF TRUTH ---
  const [rawText, setRawText] = useState(
`Insights lesen, nicht bewerten
Ziel: Verständnis statt Selbstkritik

1. Wähle ein Reel aus, das sich für dich gut angefühlt hat. Welche Insights siehst du?
- Watchtime
- Likes
- Kommentare
- Shares

---

2. Beantworte nicht „gut oder schlecht“, sondern:
- Wo bleiben Menschen?
- Wo springen sie ab?

---

3. Lies die Kommentare neu:
Welche zeigen Zustimmung? Welche zeigen Denken oder Verschiebung?
Markiere einen Kommentar, der Tiefe zeigt.

---

Footer: Insights sagen dir nicht, wie gut du bist. Sie zeigen dir, wie dein Denken wirkt.`
  );

  // --- PARSER ENGINE ---
  const parseContent = (input) => {
    const lines = input.split('\n');
    const cleanLines = lines.map(l => l.trim());

    let title = "";
    let subTitle = "";
    let footer = "";
    let bodyStartIndex = 0;

    // Find Title
    for (let i = 0; i < cleanLines.length; i++) {
        if (cleanLines[i]) {
            title = cleanLines[i];
            bodyStartIndex = i + 1;
            break;
        }
    }

    // Find Subtitle
    for (let i = bodyStartIndex; i < Math.min(bodyStartIndex + 3, cleanLines.length); i++) {
        if (cleanLines[i]) {
            if (cleanLines[i].length < 100 || cleanLines[i].toLowerCase().startsWith('ziel:')) {
                subTitle = cleanLines[i];
                bodyStartIndex = i + 1;
            }
            break;
        }
    }

    // Find Footer
    for (let i = cleanLines.length - 1; i >= bodyStartIndex; i--) {
        if (cleanLines[i]) {
            if (cleanLines[i].toLowerCase().startsWith('footer:') || cleanLines[i].toLowerCase().startsWith('merksatz:')) {
                footer = cleanLines[i].replace(/^(footer|merksatz):\s*/i, '');
            } else if (i === cleanLines.length - 1) {
                 if (!cleanLines[i-1]) {
                     footer = cleanLines[i];
                 }
            }
            break;
        }
    }

    // Extract Body
    const bodyLines = lines.slice(bodyStartIndex);
    if (footer && bodyLines[bodyLines.length-1].includes(footer)) {
        bodyLines.pop();
    } else if (footer && bodyLines.some(l => l.includes(footer))) {
         const lastIdx = bodyLines.findLastIndex(l => l.includes(footer));
         if (lastIdx > -1) bodyLines.splice(lastIdx);
    }

    const fullBodyText = bodyLines.join('\n').trim();
    const blocks = fullBodyText.split(/\n\s*-{3,}\s*\n/);
    
    const parsedSections = blocks.map((block, index) => {
      const blockLines = block.split('\n');
      const inputs = [];
      const texts = [];
      
      blockLines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed.startsWith('-') || trimmed.startsWith('•') || trimmed.startsWith('INPUT:')) {
          inputs.push(trimmed.replace(/^(-|•|INPUT:)\s*/, ''));
        } else if (trimmed.length > 0) {
          texts.push(trimmed);
        }
      });
      
      return { id: index, text: texts.join('\n'), inputs: inputs };
    });

    return { title, subTitle, sections: parsedSections, footer };
  };

  const { title, subTitle, sections, footer } = parseContent(rawText);

  // --- SMART HIGHLIGHTER ---
  const applySmartHighlights = () => {
    const lines = rawText.split('\n');
    const processedLines = lines.map(line => {
        if (line.trim().length === 0) return line;
        if (line.includes('*')) return line;
        
        let newLine = line;
        
        if (newLine.includes(':')) {
            const parts = newLine.split(':');
            if (parts[1] && parts[1].trim().length > 0 && parts[1].length < 50) {
                return `${parts[0]}: *${parts[1].trim()}*`;
            }
        }

        if (newLine.trim().endsWith('?')) {
            const words = newLine.split(' ');
            if (words.length > 3) {
                const last3 = words.slice(-3).join(' ');
                const rest = words.slice(0, -3).join(' ');
                return `${rest} *${last3}*`;
            } else {
                return `*${newLine}*`;
            }
        }

        if (/^\d+\./.test(newLine)) {
             const words = newLine.split(' ');
             const lastWord = words.pop();
             const cleanLast = lastWord.replace(/[.,!?]/g, '');
             const punct = lastWord.slice(cleanLast.length);
             return `${words.join(' ')} *${cleanLast}*${punct}`;
        }

        return newLine;
    });
    setRawText(processedLines.join('\n'));
  };

  // --- PDF EXPORT ---
  const handleExportPDF = async () => {
    const element = previewRef.current;
    if (!element) {
        alert("Bitte erst zur Vorschau wechseln.");
        setActiveTab('preview');
        return;
    }
    
    setIsExporting(true);
    try {
      const canvas = await html2canvas(element, {
        scale: 2, 
        useCORS: true,
        backgroundColor: config.colors.background,
        logging: false
      });
      
      const imgData = canvas.toDataURL('image/jpeg', 0.9);
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      
      pdf.addImage(imgData, 'JPEG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Worksheet_${title.substring(0, 15).replace(/[^a-z0-9]/gi, '_')}.pdf`);
    } catch (err) {
      console.error(err);
      alert("Fehler beim Export.");
    } finally {
      setIsExporting(false);
    }
  };

  // --- RENDER HELPERS ---
  const renderRichText = (text) => {
    if (!text) return null;
    const parts = text.split(/(\*[^*]+\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('*') && part.endsWith('*')) {
        return (
          <span key={i} style={{ 
            color: config.colors.accent, 
            fontFamily: config.typography.accentFontFamily || config.typography.fontFamily,
            fontStyle: 'italic'
          }}>
            {part.slice(1, -1)}
          </span>
        );
      }
      return <span key={i}>{part}</span>;
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-gray-100 overflow-hidden">
      {/* HEADER / TOOLBAR */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between shadow-sm z-20 shrink-0">
        <h2 className="text-sm font-bold text-gray-900 flex items-center">
          <SafeIcon icon={FiFileText} className="mr-2 text-purple-600" />
          <span className="hidden sm:inline">Worksheet Designer</span>
          <span className="sm:hidden">Worksheet</span>
        </h2>
        
        {/* MOBILE TABS CENTER */}
        <div className="flex bg-gray-100 rounded-lg p-1 mx-2 sm:hidden">
            <button 
                onClick={() => setActiveTab('editor')}
                className={`px-3 py-1.5 rounded text-xs font-bold transition-all ${activeTab === 'editor' ? 'bg-white shadow text-purple-700' : 'text-gray-500'}`}
            >
                <SafeIcon icon={FiEdit3} />
            </button>
            <button 
                onClick={() => setActiveTab('preview')}
                className={`px-3 py-1.5 rounded text-xs font-bold transition-all ${activeTab === 'preview' ? 'bg-white shadow text-purple-700' : 'text-gray-500'}`}
            >
                <SafeIcon icon={FiEye} />
            </button>
        </div>

        <div className="flex items-center space-x-2">
          {/* Style Shifter Toggle */}
          <button 
            onClick={() => setShowShifter(!showShifter)}
            className={`flex items-center px-3 py-2 rounded-lg border transition-all text-xs font-bold ${showShifter ? 'bg-purple-600 text-white border-purple-600' : 'bg-white border-purple-200 text-purple-700 hover:bg-purple-50'}`}
            title="Style Shifter (Fonts/Colors)"
          >
            <SafeIcon icon={FiRefreshCw} className="sm:mr-2" />
            <span className="hidden sm:inline">Style Shifter</span>
          </button>

          {/* Zoom controls */}
          <div className={`items-center space-x-1 bg-gray-100 rounded-lg p-1 hidden md:flex`}>
            <button onClick={() => setZoom(Math.max(0.3, zoom - 0.1))} className="px-2 font-bold text-gray-500 hover:bg-white rounded">-</button>
            <span className="text-xs font-mono w-8 text-center">{Math.round(zoom * 100)}%</span>
            <button onClick={() => setZoom(Math.min(1.5, zoom + 0.1))} className="px-2 font-bold text-gray-500 hover:bg-white rounded">+</button>
          </div>

          <button 
            onClick={handleExportPDF} 
            disabled={isExporting}
            className="bg-gray-900 text-white px-3 sm:px-4 py-2 rounded-lg font-bold text-xs sm:text-sm shadow-md hover:bg-black transition-all flex items-center disabled:opacity-70"
          >
            {isExporting ? <SafeIcon icon={FiRefreshCw} className="animate-spin"/> : <SafeIcon icon={FiDownload} className="sm:mr-2" />}
            <span className="hidden sm:inline">Download PDF</span>
          </button>
        </div>
      </div>

      {/* SHIFTER PANEL (Conditionally Visible) */}
      <AnimatePresence>
        {showShifter && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }} 
            animate={{ height: 'auto', opacity: 1 }} 
            exit={{ height: 0, opacity: 0 }} 
            className="overflow-hidden border-b border-gray-200 bg-gray-50 z-20"
          >
            <div className="p-2 max-w-2xl mx-auto">
              <StyleShifter mode="bar" />
              <p className="text-[10px] text-gray-400 text-center mt-1">Änderungen werden sofort sichtbar.</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* CONTENT AREA */}
      <div className="flex flex-1 overflow-hidden relative">
        
        {/* LEFT: EDITOR */}
        <div className={`w-full md:w-1/3 min-w-[320px] max-w-[500px] bg-white border-r border-gray-200 flex flex-col z-10 absolute md:relative inset-0 transition-transform duration-300 ${activeTab === 'editor' ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
          <div className="p-4 flex-1 flex flex-col">
            <div className="flex justify-between items-center mb-2">
                <label className="text-xs font-bold text-gray-500 uppercase flex items-center">
                    <SafeIcon icon={FiAlignLeft} className="mr-1"/> Inhalt (Alles in einem)
                </label>
                <button 
                  onClick={applySmartHighlights}
                  className="text-[10px] bg-purple-50 text-purple-700 px-2 py-1 rounded font-bold hover:bg-purple-100 transition-colors flex items-center border border-purple-100"
                >
                  <SafeIcon icon={FiZap} className="mr-1" /> Auto-Highlight
                </button>
            </div>
            
            <div className="flex-1 relative">
                <textarea 
                  value={rawText} 
                  onChange={(e) => setRawText(e.target.value)}
                  className="w-full h-full p-4 bg-gray-50 border border-gray-200 rounded-xl font-mono text-sm leading-relaxed resize-none focus:ring-2 focus:ring-purple-500 focus:bg-white transition-all outline-none"
                  placeholder={`Zeile 1: Deine Überschrift\nZeile 2: Dein Untertitel\n\nDann dein Text...\n\nFooter: Dein Merksatz`}
                />
            </div>
            
            <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-100 text-[10px] text-blue-800 space-y-1">
                <p><strong>Struktur:</strong> 1. Zeile = Titel, 2. Zeile = Untertitel.</p>
                <p><strong>Trenner:</strong> Nutze "---" um Abschnitte zu trennen.</p>
                <p><strong>Inputs:</strong> Starte eine Zeile mit "-" für Schreiblinien.</p>
                <p><strong>Footer:</strong> Schreibe "Footer:" oder nutze die letzte Zeile.</p>
            </div>
          </div>
        </div>

        {/* RIGHT: PREVIEW */}
        <div className={`flex-1 bg-gray-800 overflow-auto flex justify-center items-start p-4 md:p-12 absolute md:relative inset-0 transition-transform duration-300 ${activeTab === 'preview' ? 'translate-x-0' : 'translate-x-full md:translate-x-0'}`}>
          <div style={{ 
            transform: `scale(${window.innerWidth < 768 ? (window.innerWidth / 850) : zoom})`, 
            transformOrigin: 'top center',
            transition: 'transform 0.2s ease-out',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
            marginTop: window.innerWidth < 768 ? '20px' : '0' 
          }}>
            <div 
              ref={previewRef} 
              className="bg-white relative text-left"
              style={{
                width: '794px', // A4 Width
                minHeight: '1123px', // A4 Height
                padding: '60px 80px',
                fontFamily: config.typography.bodyFontFamily || 'Inter',
                backgroundColor: config.colors.background,
                color: config.colors.primary,
                boxSizing: 'border-box'
              }}
            >
              {/* TOP BRANDING */}
              <div className="absolute top-8 left-8">
                <span style={{ 
                  fontFamily: config.typography.fontFamily, 
                  fontSize: '10px', 
                  letterSpacing: '0.15em', 
                  textTransform: 'uppercase', 
                  opacity: 0.5 
                }}>
                  {config.name}
                </span>
              </div>

              {/* HEADER */}
              <div className="text-center mb-12 mt-4">
                {title && (
                    <div className="inline-block border-b-2 pb-4 px-8 mb-4 border-current">
                    <h1 className="text-4xl leading-tight" style={{ 
                        fontFamily: config.typography.fontFamily, 
                        fontWeight: '400', 
                        letterSpacing: '-0.02em' 
                    }}>
                        {renderRichText(title)}
                    </h1>
                    </div>
                )}
                {subTitle && (
                    <div className="text-lg opacity-80 italic" style={{ 
                        fontFamily: config.typography.accentFontFamily || config.typography.fontFamily,
                        color: config.colors.accent 
                    }}>
                    {renderRichText(subTitle)}
                    </div>
                )}
              </div>

              {/* DYNAMIC BODY CONTENT */}
              <div className="space-y-10">
                {sections.map((section) => (
                  <div key={section.id} className="relative">
                    {/* Main Text Block */}
                    {section.text && (
                        <div className="whitespace-pre-wrap text-lg font-medium leading-relaxed mb-6">
                        {renderRichText(section.text)}
                        </div>
                    )}
                    
                    {/* Input Lines */}
                    {section.inputs.length > 0 && (
                      <div className="space-y-4 ml-2 mt-4">
                        {section.inputs.map((input, idx) => (
                          <div key={idx} className="flex items-end group">
                            <div className="w-1.5 h-1.5 rounded-full mr-4 mb-2 opacity-50" style={{ backgroundColor: config.colors.accent }}></div>
                            <div className="text-base font-bold mr-3 opacity-70 mb-1 shrink-0">
                              {input}
                            </div>
                            <div className="flex-1 border-b-2 border-dotted opacity-20 border-current h-6 mb-1"></div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Separator Line (if there are more sections following) */}
                    {section.id < sections.length - 1 && (
                      <div className="flex justify-center mt-10 mb-2 opacity-20">
                        <div className="w-16 h-px bg-current"></div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* FOOTER / MERKSATZ */}
              {footer && (
                  <div className="absolute bottom-20 left-0 right-0 px-20 text-center">
                    <div className="relative py-8">
                      <div className="absolute top-0 left-1/2 -translate-x-1/2 text-4xl opacity-20" style={{ color: config.colors.accent }}>❝</div>
                      <p className="whitespace-pre-wrap text-2xl leading-relaxed italic relative z-10" style={{ 
                        fontFamily: config.typography.accentFontFamily || config.typography.fontFamily 
                      }}>
                        {renderRichText(footer)}
                      </p>
                    </div>
                  </div>
              )}

              {/* PAGE NUMBER & COPYRIGHT */}
              <div className="absolute bottom-6 left-0 right-0 flex justify-between px-8 opacity-30 text-[10px] uppercase tracking-widest">
                <span>© {new Date().getFullYear()} {config.name}</span>
                <span>Page 01</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorksheetGenerator;