// Speicher im Browser (IndexedDB). Es gibt kein Konto: alles bleibt auf dem
// Geraet der Kundin. Zwei Ablagen:
//   kv    — kleine Daten (Marke, Plan, Einstellungen) unter festen Schluesseln
//   fotos — die Fotos selbst als Blob, dazu Groesse und erkanntes Gesicht
const DB_NAME = "feedstudio";
const DB_VERSION = 1;

let dbPromise = null;
function open() {
  if (!dbPromise) {
    dbPromise = new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains("kv")) db.createObjectStore("kv");
        if (!db.objectStoreNames.contains("fotos")) db.createObjectStore("fotos", { keyPath: "id" });
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }
  return dbPromise;
}

async function run(store, mode, fn) {
  const db = await open();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(store, mode);
    const result = fn(tx.objectStore(store));
    tx.oncomplete = () => resolve(result && "result" in result ? result.result : result);
    tx.onerror = () => reject(tx.error);
  });
}

export const kvGet = (key) => run("kv", "readonly", (s) => s.get(key));
export const kvSet = (key, value) => run("kv", "readwrite", (s) => s.put(value, key));

export const fotoAlle = () => run("fotos", "readonly", (s) => s.getAll());
export const fotoSpeichern = (foto) => run("fotos", "readwrite", (s) => s.put(foto));
export const fotoLoeschen = (id) => run("fotos", "readwrite", (s) => s.delete(id));

export async function allesLoeschen() {
  await run("kv", "readwrite", (s) => s.clear());
  await run("fotos", "readwrite", (s) => s.clear());
}

export const neueId = () =>
  Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
