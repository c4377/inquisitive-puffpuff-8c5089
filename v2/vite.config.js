import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Relative Pfade: derselbe Build laeuft unter /v2/ und im Wurzelverzeichnis
// einer Kundinnen-Seite, ohne Umleitungsregeln.
export default defineConfig({
  base: "./",
  plugins: [react()],
  // eigene, leere PostCSS-Einstellung: nicht die der alten App darueber erben
  css: { postcss: { plugins: [] } },
  build: { outDir: "dist", chunkSizeWarningLimit: 2000 },
});
