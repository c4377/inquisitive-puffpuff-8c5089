// Eine Folie zeichnen. Zwei Arten:
//   Foto  — Foto mit Text unter (oder ueber) dem Gesicht
//   Text  — farbige Flaeche mit Text (Textpost)
// Rollen: "titel" (erste Folie eines Tages, mittig), "folge" (weitere Folien,
// Text linksbuendig im Eck) und "story" (9:16).
import { teileFolie, markierungen } from "../lib/importParser.js";
import { fotoZeichnen } from "./foto.js";
import { setzen, einpassen, zeichnen, einfach, einfachZeichnen } from "./text.js";

export const FORMATE = { feed: [1080, 1350], story: [1080, 1920] };

function hashZahl(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 99991;
  return h;
}

// Welcher Detail-Ausschnitt? Aus Text und Foto gewuerfelt, damit dasselbe
// Foto an verschiedenen Tagen verschieden geschnitten wird.
export function detailWahl(look, rolle, text, fotoId, index = 0) {
  const reihe = rolle === "titel" ? look.detailTitel : look.detailFolge;
  if (!reihe || !reihe.length) return null;
  const w = reihe[(hashZahl(String(fotoId) + "|" + text) * 7 + index * 3 + 1) % reihe.length];
  return w && w !== "-" ? w : null;
}

function akzentAuto(absaetze, akzentGesehen) {
  if (akzentGesehen) return;
  const letzteZeile = [...absaetze].reverse().flat().find((z) => z.length);
  const alle = absaetze.flat(2);
  if (letzteZeile && alle.length > 2) letzteZeile[letzteZeile.length - 1].akzent = true;
}

// Freie Flaeche fuer den Text, in Anteilen der Hoehe.
function textBand(box, rolle) {
  const oben = 0.1, unten = rolle === "story" ? 0.86 : 0.885;
  if (!box) return { von: 0.42, bis: unten, lage: "unten" };
  if (box.y1 < oben + 0.05 || box.y0 > unten - 0.05) return { von: Math.max(0.4, unten - 0.46), bis: unten, lage: "unten" };
  const unter = { von: box.y1 + 0.025, bis: unten };
  const ueber = { von: oben, bis: box.y0 - 0.025 };
  const hu = unter.bis - unter.von, ho = ueber.bis - ueber.von;
  if (hu >= 0.28 || hu >= ho) return { ...unter, lage: "unten" };
  return { ...ueber, lage: "oben" };
}

export function folieZeichnen(canvas, { format = "feed", look, brand, folie, rolle, bild, gesicht, fotoModus, detail, hand }) {
  const [W, H] = FORMATE[format];
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, W, H);
  const teile = teileFolie(folie.text);
  const { absaetze, akzentGesehen } = markierungen(teile.haupt);
  const f = look.schriftFaktor || 1;
  const handle = String(brand?.handle || "").replace(/^@/, "");

  if (bild) {
    // ---------- Foto-Folie ----------
    const z = fotoZeichnen(ctx, bild, W, H, { gesicht, detail, hand, modus: fotoModus, schwarz: look.schwarz });
    akzentAuto(absaetze, akzentGesehen);
    const band = textBand(z.box, rolle);
    const links = rolle === "folge" && look.ueberText;
    const rand = W * 0.09;
    const breite = links ? W * 0.74 : W * 0.8;
    const x = links ? rand : (W - breite) / 2;
    const versal = look.versal && teile.haupt.replace(/\s+/g, " ").length <= 120;

    const kicker = teile.kicker
      ? einfach(ctx, teile.kicker.toLocaleUpperCase("de-DE"), { familie: look.kleinSchrift, groesse: W * 0.024, maxBreite: breite, laufweite: 0.4 })
      : null;
    const unter = teile.unter
      ? einfach(ctx, look.kleinVersal ? teile.unter.toLocaleUpperCase("de-DE") : teile.unter, { familie: look.kleinSchrift, groesse: W * 0.032, maxBreite: breite * 0.95, gewicht: look.kleinGewicht })
      : null;
    const luft = W * 0.035;
    const extra = (kicker ? kicker.hoehe + luft * 0.7 : 0) + (unter ? unter.hoehe + luft : 0);
    const bandH = Math.min((band.bis - band.von) * H * 0.98, H * 0.64);
    const basisGroesse = W * (rolle === "titel" ? 0.176 : rolle === "story" ? 0.13 : 0.139) * f;
    const satz = einpassen(ctx, absaetze,
      { familie: look.fotoSchrift, groesse: basisGroesse, gewicht: look.titelGewicht },
      breite, Math.max(H * 0.12, bandH - extra),
      { zeile: 1.0, absatzLuft: 0.5, versal, untergrenze: W * 0.07 * f, grenzeHoehe: Math.max(H * 0.12, bandH - extra) * 1.1 });
    const block = extra + satz.hoehe;
    let y = band.lage === "oben" ? band.von * H + (kicker ? kicker.hoehe + luft * 0.7 : 0)
      : band.bis * H - block + (kicker ? kicker.hoehe + luft * 0.7 : 0);
    y = Math.max(H * 0.06 + (kicker ? kicker.hoehe : 0), y);

    // weicher Verlauf hinter dem Textblock, damit er lesbar bleibt
    const top = y - (kicker ? kicker.hoehe + luft : 0);
    const s0 = Math.max(0, top - H * 0.12);
    const scrim = ctx.createLinearGradient(0, s0, 0, H);
    const mitte = Math.min(0.9, Math.max(0.05, (top - s0) / (H - s0)));
    scrim.addColorStop(0, "rgba(0,0,0,0)");
    scrim.addColorStop(mitte, "rgba(0,0,0,0.28)");
    scrim.addColorStop(1, "rgba(0,0,0,0.42)");
    ctx.fillStyle = scrim;
    ctx.fillRect(0, s0, W, H - s0);

    const schatten = "rgba(0,0,0,0.35)";
    if (kicker) einfachZeichnen(ctx, kicker, { x, y: y - kicker.hoehe - luft * 0.7, breite, ausrichtung: links ? "links" : "mitte", farbe: "rgba(255,255,255,0.85)", schatten });
    const nachSatz = zeichnen(ctx, satz, { x, y, breite, ausrichtung: links ? "links" : "mitte", farbe: "#FFFFFF", akzentFarbe: look.akzent, schatten });
    if (unter) einfachZeichnen(ctx, unter, { x, y: nachSatz + luft, breite, ausrichtung: links ? "links" : "mitte", farbe: "rgba(255,255,255,0.92)", schatten });

    if (handle) {
      const n = einfach(ctx, handle, { familie: look.nameSchrift, groesse: W * look.nameGroesse, maxBreite: W, laufweite: look.nameLaufweite });
      einfachZeichnen(ctx, n, { x: 0, y: H * (rolle === "story" ? 0.93 : 0.945) - n.lh * 0.6, breite: W, farbe: "rgba(255,255,255,0.92)" });
    }
    return;
  }

  // ---------- Textpost ----------
  ctx.fillStyle = look.grund;
  ctx.fillRect(0, 0, W, H);
  const links = rolle === "folge";
  const breite = W * 0.8;
  const x = (W - breite) / 2;
  const kicker = teile.kicker
    ? einfach(ctx, teile.kicker.toLocaleUpperCase("de-DE"), { familie: look.kleinSchrift, groesse: W * 0.022, maxBreite: breite, laufweite: 0.4 })
    : null;
  const unter = teile.unter
    ? einfach(ctx, look.kleinVersal ? teile.unter.toLocaleUpperCase("de-DE") : teile.unter, { familie: look.kleinSchrift, groesse: W * 0.028, maxBreite: breite * 0.9, gewicht: look.kleinGewicht })
    : null;
  const luft = W * 0.035;
  const extra = (kicker ? kicker.hoehe + luft * 0.7 : 0) + (unter ? unter.hoehe + luft : 0);
  const satz = einpassen(ctx, absaetze,
    { familie: look.titelSchrift, groesse: W * (rolle === "story" ? 0.1 : 0.098) * f, gewicht: look.titelGewicht },
    breite, H * 0.62 - extra, { zeile: 1.04, absatzLuft: 0.6 });
  const block = extra + satz.hoehe;
  let y = H * (rolle === "story" ? 0.48 : 0.52) - block / 2 + (kicker ? kicker.hoehe + luft * 0.7 : 0);
  const aus = links ? "links" : "mitte";
  if (kicker) einfachZeichnen(ctx, kicker, { x, y: y - kicker.hoehe - luft * 0.7, breite, ausrichtung: aus, farbe: look.schrift });
  const nachSatz = zeichnen(ctx, satz, { x, y, breite, ausrichtung: aus, farbe: look.schrift, akzentFarbe: look.schrift });
  if (unter) einfachZeichnen(ctx, unter, { x, y: nachSatz + luft, breite, ausrichtung: aus, farbe: look.schrift });
  if (handle) {
    const skript = /Delafield|Caveat/.test(look.nameSchrift);
    const n = einfach(ctx, handle, { familie: look.nameSchrift, groesse: W * (skript ? 0.05 : 0.026), maxBreite: W, laufweite: skript ? 0 : 0.08 });
    einfachZeichnen(ctx, n, { x: W * 0.1, y: H * 0.905 - n.lh * 0.6, breite: W, ausrichtung: "links", farbe: look.schrift });
  }
}

// Alle Schriften eines Looks laden, bevor gezeichnet wird.
export async function schriftenLaden(look) {
  if (!document.fonts) return;
  const fam = [look.titelSchrift, look.fotoSchrift, look.kleinSchrift, look.nameSchrift];
  await Promise.all(
    fam.flatMap((f) => [`400 40px "${f}"`, `italic 400 40px "${f}"`, `700 40px "${f}"`].map((s) =>
      document.fonts.load(s).catch(() => null)))
  );
}

export { setzen };
