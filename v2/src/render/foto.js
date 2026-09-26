// Foto zeichnen: Zuschnitt (Gesicht, Detail oder von Hand), Aufhellen dunkler
// Fotos, Schwarz-Weiss, dunkler Verlauf unten.

// Detail-Ausschnitte: [Fokus x, Fokus y, Zoom]. face/close/bust richten sich
// nach dem Gesicht, die anderen sind feste Bildbereiche.
function detailFokus(art, g) {
  const gx = g ? (g.x0 + g.x1) / 2 : 0.5;
  const gy = g ? (g.y0 + g.y1) / 2 : 0.34;
  switch (art) {
    case "face": return [gx, gy, 2.3];
    case "close": return [gx, gy + 0.06, 1.85];
    case "bust": return [gx, Math.min(0.95, gy + 0.22), 1.7];
    case "lower": return [0.5, 0.8, 2];
    case "wide": return [0.5, 0.55, 1.35];
    case "full": return [0.5, 0.5, 1];
    default: return null;
  }
}

// Liefert, wo das Foto auf der Flaeche liegt, und die Gesichtsbox in
// Anteilen der Flaeche (fuer die Textplatzierung).
export function zuschnitt(bw, bh, W, H, { gesicht, detail, hand }) {
  const basis = Math.max(W / bw, H / bh);
  let fx = 0.5, fy = 0.4, zoom = 1, zx = 0.5, zy = 0.4;
  if (hand) {
    fx = hand.x; fy = hand.y; zoom = hand.zoom || 1; zx = 0.5; zy = 0.5;
  } else if (detail && detailFokus(detail, gesicht)) {
    [fx, fy, zoom] = detailFokus(detail, gesicht); zx = 0.5; zy = 0.5;
  } else if (gesicht) {
    fx = (gesicht.x0 + gesicht.x1) / 2;
    fy = (gesicht.y0 + gesicht.y1) / 2;
    zoom = fy < 0.3 ? 1 : 1.12;
    zx = 0.5; zy = 0.3;
  }
  const s = basis * zoom;
  const dw = bw * s, dh = bh * s;
  const left = Math.min(0, Math.max(W - dw, zx * W - fx * dw));
  const top = Math.min(0, Math.max(H - dh, zy * H - fy * dh));
  let box = null;
  if (gesicht) {
    box = {
      x0: (left + gesicht.x0 * dw) / W, x1: (left + gesicht.x1 * dw) / W,
      y0: (top + gesicht.y0 * dh) / H, y1: (top + gesicht.y1 * dh) / H,
    };
  }
  return { left, top, dw, dh, box };
}

export function fotoZeichnen(ctx, bild, W, H, opt) {
  const bw = bild.naturalWidth || bild.width;
  const bh = bild.naturalHeight || bild.height;
  const z = zuschnitt(bw, bh, W, H, opt);
  ctx.drawImage(bild, z.left, z.top, z.dw, z.dh);

  // Aufhellen und Schwarz-Weiss in einem Durchgang ueber die Pixel.
  const img = ctx.getImageData(0, 0, W, H);
  const d = img.data;
  let summe = 0, n = 0;
  for (let i = 0; i < d.length; i += 4 * 97) {
    summe += 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
    n++;
  }
  const mittel = summe / Math.max(1, n);
  const ziel = 118;
  const gamma = mittel < ziel && mittel > 5
    ? Math.min(1.8, Math.log(ziel / 255) / Math.log(mittel / 255))
    : 1;
  const sw = opt.modus === "sw";
  if (gamma !== 1 || sw) {
    const lut = new Uint8ClampedArray(256);
    for (let v = 0; v < 256; v++) lut[v] = 255 * Math.pow(v / 255, 1 / gamma);
    for (let i = 0; i < d.length; i += 4) {
      let r = lut[d[i]], g = lut[d[i + 1]], b = lut[d[i + 2]];
      if (sw) {
        // etwas mehr Kontrast, damit Schwarz-Weiss nicht grau wirkt
        let y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
        y = Math.max(0, Math.min(255, (y - 128) * 1.1 + 128));
        r = g = b = y;
      }
      d[i] = r; d[i + 1] = g; d[i + 2] = b;
    }
    ctx.putImageData(img, 0, 0);
  }

  // dunkler Verlauf: oben leicht, unten kraeftig (Staerke = look.schwarz)
  const k = Math.max(0, Math.min(1, opt.schwarz ?? 0.85));
  const unten = ctx.createLinearGradient(0, H * 0.5, 0, H);
  unten.addColorStop(0, "rgba(0,0,0,0)");
  unten.addColorStop(1, `rgba(0,0,0,${0.85 * k})`);
  ctx.fillStyle = unten;
  ctx.fillRect(0, 0, W, H);
  const oben = ctx.createLinearGradient(0, 0, 0, H * 0.3);
  oben.addColorStop(0, `rgba(0,0,0,${0.3 * k})`);
  oben.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = oben;
  ctx.fillRect(0, 0, W, H * 0.3);
  return z;
}
