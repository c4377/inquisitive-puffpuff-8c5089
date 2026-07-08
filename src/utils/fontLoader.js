// fontLoader.js
// Load arbitrary Google Fonts at runtime (for Brandsheet imports).
// Injects a stylesheet link, then waits until the fonts are actually usable
// so the fabric canvas measures/renders them correctly on first paint.

const loadedFamilies = new Set();

const linkLoaded = (link) =>
  new Promise((resolve) => {
    link.onload = () => resolve(true);
    link.onerror = () => resolve(false);
    // Safety net if events never fire.
    setTimeout(() => resolve(true), 2500);
  });

export const loadGoogleFonts = async (names = []) => {
  if (typeof document === 'undefined') return;
  const need = [...new Set(names.map((n) => (n || '').trim()).filter(Boolean))]
    .filter((n) => !loadedFamilies.has(n));
  if (!need.length) return;

  const fam = need
    .map((n) => `family=${encodeURIComponent(n).replace(/%20/g, '+')}:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500`)
    .join('&');
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `https://fonts.googleapis.com/css2?${fam}&display=swap`;
  document.head.appendChild(link);
  need.forEach((n) => loadedFamilies.add(n));

  await linkLoaded(link);
  // Ask the browser to actually fetch/activate the faces (with a timeout so a
  // typo'd font name can never hang the import).
  try {
    await Promise.race([
      Promise.all(
        need.flatMap((n) => [
          document.fonts.load(`16px "${n}"`),
          document.fonts.load(`600 16px "${n}"`),
          document.fonts.load(`italic 16px "${n}"`),
        ])
      ),
      new Promise((res) => setTimeout(res, 3500)),
    ]);
  } catch (e) { /* fall back silently — canvas will use a fallback font */ }
};
