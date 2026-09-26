// Textsatz auf dem Canvas: Woerter mit Stil (Akzent kursiv, fett) umbrechen,
// Zeilenumbrueche und Absaetze einhalten, auf eine Flaeche einpassen.

export function schrift({ familie, groesse, gewicht = 400, kursiv = false }) {
  return `${kursiv ? "italic " : ""}${gewicht} ${Math.round(groesse)}px "${familie}"`;
}

function wortStil(w, basis) {
  return {
    familie: basis.familie,
    groesse: basis.groesse,
    gewicht: w.fett ? 700 : basis.gewicht,
    kursiv: w.akzent,
  };
}

// absaetze: [[ [ {w, fett, akzent}, … ] (Zeile), … ] (Absatz), … ]
// Liefert Zeilen mit Wortpositionen und die Gesamthoehe.
export function setzen(ctx, absaetze, basis, maxBreite, { zeile = 1.05, absatzLuft = 0.55, versal = false } = {}) {
  const zeilen = [];
  const lh = basis.groesse * zeile;
  let hoehe = 0;
  let breiteste = 0;
  absaetze.forEach((absatz, ai) => {
    if (ai > 0) {
      hoehe += basis.groesse * absatzLuft;
      zeilen.push({ luft: basis.groesse * absatzLuft });
    }
    for (const quelle of absatz) {
      let aktuell = [];
      let breite = 0;
      const abschluss = () => {
        if (!aktuell.length) return;
        zeilen.push({ woerter: aktuell, breite });
        breiteste = Math.max(breiteste, breite);
        hoehe += lh;
        aktuell = [];
        breite = 0;
      };
      for (const w of quelle) {
        const text = versal ? w.w.toLocaleUpperCase("de-DE") : w.w;
        const stil = wortStil(w, basis);
        ctx.font = schrift(stil);
        const ww = ctx.measureText(text).width;
        const leer = ctx.measureText(" ").width;
        const neu = aktuell.length ? breite + leer + ww : ww;
        if (aktuell.length && neu > maxBreite) {
          abschluss();
          aktuell.push({ text, stil, x: 0, breite: ww, akzent: w.akzent });
          breite = ww;
        } else {
          aktuell.push({ text, stil, x: aktuell.length ? breite + leer : 0, breite: ww, akzent: w.akzent });
          breite = neu;
        }
      }
      abschluss();
    }
  });
  return { zeilen, hoehe, breiteste, lh };
}

// Sucht die groesste Schrift, bei der der Text in maxBreite x maxHoehe passt.
// untergrenze gilt nur, solange der Text dabei nicht mehr als grenzeHoehe braucht.
export function einpassen(ctx, absaetze, basis, maxBreite, maxHoehe, opt = {}) {
  let g = basis.groesse;
  const unter = opt.untergrenze || 0;
  for (let i = 0; i < 80; i++) {
    const satz = setzen(ctx, absaetze, { ...basis, groesse: g }, maxBreite, opt);
    const passt = satz.hoehe <= maxHoehe && satz.breiteste <= maxBreite * 1.001;
    const amBoden = g <= unter && satz.hoehe <= (opt.grenzeHoehe || Infinity);
    if (passt || amBoden || g < 12) return { ...satz, groesse: g };
    g *= 0.95;
  }
  return { ...setzen(ctx, absaetze, { ...basis, groesse: g }, maxBreite, opt), groesse: g };
}

// Zeichnet einen gesetzten Text. ausrichtung: "mitte" oder "links".
export function zeichnen(ctx, satz, { x, y, breite, ausrichtung = "mitte", farbe, akzentFarbe, schatten }) {
  let yy = y;
  ctx.textBaseline = "alphabetic";
  for (const z of satz.zeilen) {
    if (z.luft) { yy += z.luft; continue; }
    const start = ausrichtung === "links" ? x : x + (breite - z.breite) / 2;
    const grund = yy + satz.lh * 0.78;
    for (const w of z.woerter) {
      ctx.font = schrift(w.stil);
      ctx.fillStyle = w.akzent ? akzentFarbe || farbe : farbe;
      if (schatten) {
        ctx.shadowColor = schatten;
        ctx.shadowBlur = w.stil.groesse * 0.18;
        ctx.shadowOffsetY = w.stil.groesse * 0.03;
      }
      ctx.fillText(w.text, start + w.x, grund);
    }
    yy += satz.lh;
  }
  ctx.shadowColor = "transparent";
  ctx.shadowBlur = 0;
  ctx.shadowOffsetY = 0;
  return yy;
}

// Einfache Zeile(n) ohne Markierungen, z. B. kleines Wort oder kleine Zeile.
// laufweite in em, wird Buchstabe fuer Buchstabe gesetzt.
export function einfach(ctx, text, { familie, groesse, gewicht = 400, maxBreite, laufweite = 0 }) {
  const stil = { familie, groesse, gewicht, kursiv: false };
  ctx.font = schrift(stil);
  const abstand = laufweite * groesse;
  const mess = (t) => ctx.measureText(t).width + Math.max(0, t.length - 1) * abstand;
  const zeilen = [];
  for (const absatz of String(text).split("\n")) {
    let akt = "";
    for (const w of absatz.split(/\s+/).filter(Boolean)) {
      const neu = akt ? akt + " " + w : w;
      if (akt && mess(neu) > maxBreite) { zeilen.push(akt); akt = w; } else akt = neu;
    }
    if (akt) zeilen.push(akt);
  }
  return { zeilen, stil, abstand, lh: groesse * 1.3, hoehe: zeilen.length * groesse * 1.3, mess };
}

export function einfachZeichnen(ctx, e, { x, y, breite, ausrichtung = "mitte", farbe, schatten }) {
  ctx.font = schrift(e.stil);
  ctx.fillStyle = farbe;
  if (schatten) { ctx.shadowColor = schatten; ctx.shadowBlur = e.stil.groesse * 0.4; }
  let yy = y;
  for (const z of e.zeilen) {
    const w = e.mess(z);
    let xx = ausrichtung === "links" ? x : x + (breite - w) / 2;
    const grund = yy + e.lh * 0.75;
    if (e.abstand) {
      for (const ch of z) { ctx.fillText(ch, xx, grund); xx += ctx.measureText(ch).width + e.abstand; }
    } else ctx.fillText(z, xx, grund);
    yy += e.lh;
  }
  ctx.shadowColor = "transparent";
  ctx.shadowBlur = 0;
  return yy;
}
