// Gesichtserkennung (face-api, TinyFaceDetector). Laeuft einmal pro Foto
// beim Hochladen; das Ergebnis wird mit dem Foto gespeichert. Die Box ist in
// Anteilen des Fotos angegeben (0..1), damit sie fuer jeden Zuschnitt gilt.
let faceapiPromise = null;

async function laden() {
  if (!faceapiPromise) {
    faceapiPromise = (async () => {
      const faceapi = await import("@vladmandic/face-api");
      try {
        await faceapi.tf.setBackend("webgl");
      } catch {
        await faceapi.tf.setBackend("cpu");
      }
      await faceapi.tf.ready();
      const basis = new URL("./models", document.baseURI).href;
      await faceapi.nets.tinyFaceDetector.loadFromUri(basis);
      return faceapi;
    })().catch((e) => {
      faceapiPromise = null;
      throw e;
    });
  }
  return faceapiPromise;
}

export async function gesichtFinden(bild) {
  try {
    const faceapi = await laden();
    const w = bild.naturalWidth || bild.width;
    const h = bild.naturalHeight || bild.height;
    const s = Math.min(1, 640 / Math.max(w, h));
    const c = document.createElement("canvas");
    c.width = Math.round(w * s);
    c.height = Math.round(h * s);
    c.getContext("2d").drawImage(bild, 0, 0, c.width, c.height);
    const treffer = await faceapi.detectAllFaces(
      c, new faceapi.TinyFaceDetectorOptions({ inputSize: 416, scoreThreshold: 0.45 })
    );
    if (!treffer.length) return null;
    const b = treffer.sort((a, z) => z.box.area - a.box.area)[0].box;
    return {
      x0: b.x / c.width, y0: b.y / c.height,
      x1: (b.x + b.width) / c.width, y1: (b.y + b.height) / c.height,
    };
  } catch (e) {
    console.warn("Gesichtserkennung nicht moeglich:", e);
    return null;
  }
}
