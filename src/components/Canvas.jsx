import React, { useRef, useEffect, forwardRef, useImperativeHandle, useState } from 'react';
import { fabric } from 'fabric';
import { renderSlide } from '../utils/canvasRenderer';

const Canvas = forwardRef(({ data, width = 400, height = 500, brandName = "", asImage = false }, ref) => {
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);
  const [fontLoaded, setFontLoaded] = useState(false);
  // asImage: render once, export as JPEG, dispose the fabric canvas. Live
  // canvases cost ~10-30MB each on iOS (retina backing store); many at once
  // exceed Safari's canvas memory limit and white-screen the page.
  const [imgUrl, setImgUrl] = useState(null);

  // Initialize Fonts — load the specific families this slide uses (Playfair
  // for editorial headlines, Montserrat for CAPS, plus any brand fonts), THEN
  // mark ready. Measuring before the real font loads makes the fit loop
  // under-shrink and the text overflows (was visible only on first render in
  // the Editor). Re-runs when the slide's fonts change.
  useEffect(() => {
    const fams = ['Playfair Display', 'Montserrat', 'Inter'];
    if (data?.fontFamily) fams.push(data.fontFamily);
    if (data?.accentFontFamily) fams.push(data.accentFontFamily);
    if (data?.bodyFontFamily) fams.push(data.bodyFontFamily);
    let cancelled = false;
    const loads = fams.filter(Boolean).flatMap((f) => [
      document.fonts.load(`16px "${f}"`),
      document.fonts.load(`600 16px "${f}"`),
    ]);
    Promise.race([
      Promise.all(loads).then(() => document.fonts.ready),
      new Promise((res) => setTimeout(res, 3000)),
    ]).then(() => { if (!cancelled) setFontLoaded(true); });
    return () => { cancelled = true; };
  }, [data?.fontFamily, data?.accentFontFamily, data?.bodyFontFamily]);

  // Expose API
  useImperativeHandle(ref, () => ({
    getDataURL: () => fabricRef.current?.toDataURL({ format: 'png', multiplier: 1 }),
    getBlob: async () => {
      const dataUrl = fabricRef.current?.toDataURL({ format: 'png', multiplier: 1 });
      if (!dataUrl) return null;
      const byteString = atob(dataUrl.split(',')[1]);
      const mimeString = dataUrl.split(',')[0].split(':')[1].split(';')[0];
      const ab = new ArrayBuffer(byteString.length);
      const ia = new Uint8Array(ab);
      for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i);
      return new Blob([ab], { type: mimeString });
    },
    downloadImage: async (fileName = 'brand-post.png') => {
      if (!fabricRef.current) return;
      const dataUrl = fabricRef.current.toDataURL({ format: 'png', multiplier: 2 }); // 2x for Retina download
      const link = document.createElement('a');
      link.download = fileName;
      link.href = dataUrl;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
  }));

  // Initialize Fabric
  useEffect(() => {
    if (!canvasRef.current) return;

    // Create Fabric instance
    const canvas = new fabric.StaticCanvas(canvasRef.current, {
      enableRetinaScaling: !asImage,
      renderOnAddRemove: false,
    });
    fabricRef.current = canvas;

    return () => {
      canvas.dispose();
      fabricRef.current = null;
    };
  }, [imgUrl]);

  // Render Content
  useEffect(() => {
    const canvas = fabricRef.current;
    if (!canvas || !data) return;

    // Dimensions (internal render resolution — kept high for crisp scaling)
    let canvasWidth = 800;
    let canvasHeight = 1000;

    if (data.format === '16:9') {
      canvasWidth = 960;
      canvasHeight = 540;
    } else if (data.format === '9:16') {
      canvasWidth = 800;
      canvasHeight = 1422;
    } else if (data.format === '1:1') {
        canvasWidth = 800;
        canvasHeight = 800;
    } else if (data.format === '4:5') {
        canvasWidth = 800;
        canvasHeight = 1000;
    }

    // Update Dimensions
    canvas.setDimensions({ width: canvasWidth, height: canvasHeight });

    // Render — scale fonts/spacing proportionally to the internal width.
    // Base design width was 400px, so scale = width/400 keeps text proportions.
    const renderScale = canvasWidth / 400;
    Promise.resolve(
      renderSlide(canvas, data, canvasWidth, canvasHeight, { 
        slideIndex: data.slideNumber ? data.slideNumber - 1 : 0, 
        totalSlides: data.totalSlides || (data.slideNumber ? 2 : 1), 
        scale: renderScale, 
        // A per-slide brandText (Footer Text) overrides the global brand mark.
        globalBrandName: (typeof data.brandText === 'string' && data.brandText.trim())
          ? data.brandText
          : brandName
      })
    ).then(() => {
      if (asImage && fabricRef.current) {
        try {
          const url = fabricRef.current.toDataURL({ format: 'jpeg', quality: 0.85, multiplier: 0.6 });
          if (url && url.length > 50) setImgUrl(url);
        } catch (e) { /* keep live canvas as fallback */ }
      }
    }).catch((err) => {
      // never let a render error crash the page
      console.error('renderSlide failed:', err);
    });

    // FIX: Fabric renders at an internal resolution (e.g. 400x500). Scale the
    // visible <canvas> to the container WIDTH while keeping aspect ratio, so the
    // content shrinks/grows proportionally instead of being cut off or oversized.
    const el = canvas.lowerCanvasEl;
    if (el) {
      el.style.width = '100%';
      el.style.height = 'auto';
      el.style.display = 'block';
      el.style.maxHeight = '100%';
      el.style.objectFit = 'contain';
    }

  }, [data, fontLoaded, brandName]);

  return (
    <div className="w-full h-full bg-white overflow-hidden shadow-sm relative flex items-center justify-center">
      {asImage && imgUrl ? (
        <img src={imgUrl} alt="" className="w-full h-auto block max-h-full object-contain" />
      ) : (
        <canvas ref={canvasRef} />
      )}
    </div>
  );
});

export default React.memo(Canvas);