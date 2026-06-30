import React, { useRef, useEffect, forwardRef, useImperativeHandle, useState } from 'react';
import { fabric } from 'fabric';
import { renderSlide } from '../utils/canvasRenderer';

const Canvas = forwardRef(({ data, width = 400, height = 500, brandName = "MUSE MENTORING" }, ref) => {
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);
  const [fontLoaded, setFontLoaded] = useState(false);

  // Initialize Fonts
  useEffect(() => {
    document.fonts.ready.then(() => setFontLoaded(true));
  }, []);

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
      enableRetinaScaling: true,
      renderOnAddRemove: false,
    });
    fabricRef.current = canvas;

    return () => {
      canvas.dispose();
      fabricRef.current = null;
    };
  }, []);

  // Render Content
  useEffect(() => {
    const canvas = fabricRef.current;
    if (!canvas || !data) return;

    // Dimensions
    let canvasWidth = 400;
    let canvasHeight = 500;

    if (data.format === '16:9') {
      canvasWidth = 960;
      canvasHeight = 540;
    } else if (data.format === '9:16') {
      canvasWidth = 400;
      canvasHeight = 711;
    } else if (data.format === '1:1') {
        canvasWidth = 500;
        canvasHeight = 500;
    }

    // Update Dimensions
    canvas.setDimensions({ width: canvasWidth, height: canvasHeight });

    // Render
    renderSlide(canvas, data, canvasWidth, canvasHeight, { 
      slideIndex: data.slideNumber ? data.slideNumber - 1 : 0, 
      totalSlides: data.totalSlides || (data.slideNumber ? 2 : 1), 
      scale: 1, 
      globalBrandName: brandName 
    });

  }, [data, fontLoaded, brandName]);

  return (
    <div className="w-full h-full bg-white overflow-hidden shadow-sm relative">
      <canvas ref={canvasRef} />
    </div>
  );
});

export default React.memo(Canvas);