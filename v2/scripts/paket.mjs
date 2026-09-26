// Baut das Verkaufspaket: dist/ als Ordner "feedstudio" plus Anleitung.
import fs from "node:fs";
import path from "node:path";
import JSZip from "jszip";

const zip = new JSZip();
const ordner = zip.folder("feedstudio");
function hinzu(quelle, ziel) {
  for (const name of fs.readdirSync(quelle)) {
    const q = path.join(quelle, name);
    if (fs.statSync(q).isDirectory()) hinzu(q, ziel.folder(name));
    else ziel.file(name, fs.readFileSync(q));
  }
}
hinzu("dist", ordner);
zip.file("ANLEITUNG.md", fs.readFileSync("ANLEITUNG.md"));
const daten = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
fs.writeFileSync("feedstudio-paket.zip", daten);
console.log("feedstudio-paket.zip", Math.round(daten.length / 1024), "KB");
