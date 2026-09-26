// Look-Vorlagen. Jede Kundin waehlt beim Einrichten eine und kann danach
// Farben und Schriften in den Einstellungen aendern (brand.anpassung).
//
// Groessen sind Anteile der Bildbreite, damit 4:5 und 9:16 gleich wirken.
export const LOOKS = {
  klassisch: {
    name: "Klassisch",
    beschreibung: "Dunkelbraun, Playfair, ruhig und edel",
    grund: "#241A14", schrift: "#F3ECE4", akzent: "#FFFFFF",
    titelSchrift: "Playfair Display", titelGewicht: 400,
    fotoSchrift: "Playfair Display",
    kleinSchrift: "Inter", kleinVersal: true, kleinGewicht: 400,
    nameSchrift: "Playfair Display", nameGroesse: 0.034, nameLaufweite: 0.06,
    versal: false,
    fotoReihe: ["farbe", "farbe", "farbe", "sw"],
  },
  bordeaux: {
    name: "Bordeaux",
    beschreibung: "Weinrot, schmale Serif in Versalien, Schreibmaschine und Handschrift",
    grund: "#6B1E1A", schrift: "#F4EDE1", akzent: "#F1D9C9",
    titelSchrift: "Instrument Serif", titelGewicht: 400,
    fotoSchrift: "Instrument Serif",
    kleinSchrift: "Courier Prime", kleinVersal: false, kleinGewicht: 400,
    nameSchrift: "Mrs Saint Delafield", nameGroesse: 0.075, nameLaufweite: 0,
    versal: true,
    fotoReihe: ["sw", "sw", "farbe", "farbe"],
  },
  bordeauxMix: {
    name: "Bordeaux Mix",
    beschreibung: "Weinrot, Textposts schmal, Fotos mit kräftiger Serif",
    grund: "#6B1E1A", schrift: "#F4EDE1", akzent: "#F1D9C9",
    titelSchrift: "Instrument Serif", titelGewicht: 400,
    fotoSchrift: "Gloock",
    kleinSchrift: "Courier Prime", kleinVersal: false, kleinGewicht: 400,
    nameSchrift: "Mrs Saint Delafield", nameGroesse: 0.075, nameLaufweite: 0,
    versal: false,
    fotoReihe: ["sw", "sw", "farbe", "farbe"],
  },
  creme: {
    name: "Creme & Espresso",
    beschreibung: "Heller Cremegrund, Kapitälchen, Handschrift",
    grund: "#F1E9DC", schrift: "#2B1D14", akzent: "#F3D6C2",
    titelSchrift: "Bodoni Moda SC", titelGewicht: 400,
    fotoSchrift: "Bodoni Moda SC",
    kleinSchrift: "Courier Prime", kleinVersal: false, kleinGewicht: 400,
    nameSchrift: "Mrs Saint Delafield", nameGroesse: 0.075, nameLaufweite: 0,
    versal: false,
    fotoReihe: ["farbe", "sw", "farbe", "sw"],
  },
};

export const SCHRIFTEN = [
  "Playfair Display", "Instrument Serif", "Gloock", "Bodoni Moda SC",
  "Inter", "Courier Prime", "Caveat", "Mrs Saint Delafield",
];

// Allgemeine Einstellungen, die fuer alle Looks gelten.
export const STANDARD = {
  textJede: 2,          // jeder 2. Tag ist ein Textpost ohne Foto
  schwarz: 0.85,        // Staerke des dunklen Verlaufs unten auf Fotos
  schriftFaktor: 1,     // 1 = normal, groesser/kleiner in den Einstellungen
  detailFolge: ["-", "lower", "-", "bust", "-", "close", "lower"],
  detailTitel: ["-", "-", "-", "bust"],
  ueberText: true,      // Text in der Ecke auf Folgefolien
};

// Der wirksame Look: Vorlage + Anpassungen der Kundin.
export function wirksamerLook(brand) {
  const basis = LOOKS[brand?.look] || LOOKS.klassisch;
  return { ...STANDARD, ...basis, ...(brand?.anpassung || {}) };
}
