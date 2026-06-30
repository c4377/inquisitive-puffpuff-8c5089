export const generatePattern = (type, colors, width = 1080, height = 1350) => {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');

  // Fallback Colors if brand colors are missing
  const bg = colors.background || '#ffffff';
  const prim = colors.primary || '#000000';
  const sec = colors.secondary || '#cccccc';
  const acc = colors.accent || '#ff0000';

  // Clear
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, width, height);

  switch (type) {
    case 'soft_gradient':
      // Smooth diagonal gradient
      const grd = ctx.createLinearGradient(0, 0, width, height);
      grd.addColorStop(0, bg);
      grd.addColorStop(0.5, sec);
      grd.addColorStop(1, bg);
      ctx.fillStyle = grd;
      ctx.fillRect(0, 0, width, height);
      break;

    case 'deep_aura':
      // Dark center glow
      const r = Math.max(width, height) * 0.8;
      const grdRad = ctx.createRadialGradient(width / 2, height / 2, 0, width / 2, height / 2, r);
      grdRad.addColorStop(0, acc); // Center glow
      grdRad.addColorStop(0.4, bg); // Fade out
      grdRad.addColorStop(1, bg);
      ctx.fillStyle = grdRad;
      ctx.fillRect(0, 0, width, height);
      
      // Add subtle noise overlay
      addNoise(ctx, width, height, 0.05);
      break;

    case 'geometric_minimal':
      // Simple geometric shapes
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, width, height);
      
      ctx.beginPath();
      ctx.arc(width * 0.8, height * 0.2, width * 0.3, 0, 2 * Math.PI);
      ctx.fillStyle = sec;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(width * 0.1, height * 0.8, width * 0.4, 0, 2 * Math.PI);
      ctx.fillStyle = acc;
      ctx.globalAlpha = 0.5;
      ctx.fill();
      ctx.globalAlpha = 1.0;
      break;

    case 'noise_texture':
      // Solid color with heavy aesthetic grain
      ctx.fillStyle = sec;
      ctx.fillRect(0, 0, width, height);
      addNoise(ctx, width, height, 0.15);
      break;

    case 'mesh_gradient':
      // Complex multi-point gradient simulation
      // 1. Top Left
      const g1 = ctx.createRadialGradient(0, 0, 0, 0, 0, width * 0.8);
      g1.addColorStop(0, acc);
      g1.addColorStop(1, 'transparent');
      ctx.fillStyle = g1;
      ctx.fillRect(0, 0, width, height);

      // 2. Bottom Right
      const g2 = ctx.createRadialGradient(width, height, 0, width, height, width * 0.8);
      g2.addColorStop(0, sec);
      g2.addColorStop(1, 'transparent');
      ctx.fillStyle = g2;
      ctx.fillRect(0, 0, width, height);
      
      // Blur everything for mesh effect
      // Note: Context filter is not supported in all environments perfectly, but works in modern browsers
      // Since we can't easily blur the canvas itself after drawing without performance hit or re-drawing image,
      // we rely on the radial gradients being soft enough.
      addNoise(ctx, width, height, 0.08);
      break;
      
    case 'stripes_modern':
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, width, height);
      ctx.lineWidth = 2;
      ctx.strokeStyle = sec;
      ctx.globalAlpha = 0.3;
      
      const step = 40;
      for (let i = -height; i < width; i += step) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i + height, height);
        ctx.stroke();
      }
      ctx.globalAlpha = 1.0;
      break;

    default:
      break;
  }

  return canvas.toDataURL('image/png');
};

// Helper for Grain/Noise
const addNoise = (ctx, w, h, opacity) => {
  const iData = ctx.getImageData(0, 0, w, h);
  const buffer32 = new Uint32Array(iData.data.buffer);
  const len = buffer32.length;

  for (let i = 0; i < len; i++) {
    if (Math.random() < 0.5) {
      // We manipulate the alpha of existing pixels slightly or overlay noise
      // Ideally, we create a separate noise canvas, but direct pixel manipulation is faster for simple noise
      // However, modifying Uint32Array directly deals with Endianness. 
      // A safer, simpler approach for "overlay" noise without complex pixel manipulation:
    }
  }
  // Revert to simple canvas API for noise to ensure color safety
  ctx.save();
  ctx.globalCompositeOperation = 'overlay';
  ctx.globalAlpha = opacity;
  
  // Create a small noise pattern
  const noiseCanvas = document.createElement('canvas');
  noiseCanvas.width = 100;
  noiseCanvas.height = 100;
  const nCtx = noiseCanvas.getContext('2d');
  const imgData = nCtx.createImageData(100, 100);
  const data = imgData.data;
  for (let i = 0; i < data.length; i += 4) {
    const val = Math.random() * 255;
    data[i] = val;     // r
    data[i + 1] = val; // g
    data[i + 2] = val; // b
    data[i + 3] = 100; // alpha
  }
  nCtx.putImageData(imgData, 0, 0);
  
  const pattern = ctx.createPattern(noiseCanvas, 'repeat');
  ctx.fillStyle = pattern;
  ctx.fillRect(0, 0, w, h);
  
  ctx.restore();
};