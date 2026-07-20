const DB_NAME = 'BrandStudioDB';
const STORE_NAME = 'assets';
const IMAGES_KEY = 'brand_images';
const DESIGNS_KEY = 'saved_designs';
const FONTS_KEY = 'custom_fonts';
const PLAN_KEY = 'content_plan';
const COMMUNITY_KEY = 'community_decks'; // NEW KEY

const initDB = () => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, 3); // Version bumped to 3
    request.onerror = () => reject("IndexedDB error");
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME);
      }
    };
    request.onsuccess = (event) => resolve(event.target.result);
  });
};

// --- IMAGES ---
export const saveImagesToDB = async (images) => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(images, IMAGES_KEY);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (e) {
    console.error("Failed to save images to DB", e);
    return false;
  }
};

export const loadImagesFromDB = async () => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(IMAGES_KEY);
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => resolve([]);
    });
  } catch (e) {
    console.warn("Could not init DB for loading images", e);
    return [];
  }
};

// --- DESIGNS (LIBRARY) ---
export const saveDesignsToDB = async (designs) => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(designs, DESIGNS_KEY);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (e) {
    console.error("Failed to save designs to DB", e);
    return false;
  }
};

export const loadDesignsFromDB = async () => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(DESIGNS_KEY);
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => resolve([]);
    });
  } catch (e) {
    console.warn("Could not init DB for loading designs", e);
    return [];
  }
};

// --- FONTS (CUSTOM UPLOAD) ---
export const saveFontsToDB = async (fonts) => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(fonts, FONTS_KEY);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (e) {
    console.error("Failed to save fonts to DB", e);
    return false;
  }
};

export const loadFontsFromDB = async () => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(FONTS_KEY);
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => resolve([]);
    });
  } catch (e) {
    console.warn("Could not init DB for loading fonts", e);
    return [];
  }
};

// --- CONTENT PLAN ---
export const savePlanToDB = async (plan) => {
  try {
    const db = await initDB();
    // Sanitise to a plain, structured-cloneable snapshot. If any slide picked
    // up a non-cloneable value (a function, a DOM node, an Image element via
    // _autoImage, etc.), IndexedDB's put() throws a DataCloneError and the whole
    // save silently fails. A JSON round-trip strips those and guarantees a
    // plain object tree.
    let safePlan;
    try {
      safePlan = JSON.parse(JSON.stringify(plan));
    } catch (jsonErr) {
      console.error('Plan not serialisable, saving best-effort copy', jsonErr);
      safePlan = plan;
    }
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(safePlan, PLAN_KEY);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (e) {
    console.error("Failed to save plan to DB", e);
    return false;
  }
};

export const loadPlanFromDB = async () => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(PLAN_KEY);
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => resolve([]);
    });
  } catch (e) {
    console.warn("Could not init DB for loading plan", e);
    return [];
  }
};

// --- SAVED POST SETS (named snapshots of a content plan) ---
// A "set" = { id, name, createdAt, plan: [...days] }. Stored as an array.
const SETS_KEY = 'saved_post_sets';

export const saveSetsToDB = async (sets) => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(sets, SETS_KEY);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (e) {
    console.error("Failed to save sets to DB", e);
    return false;
  }
};

export const loadSetsFromDB = async () => {
  try {
    const db = await initDB();
    return new Promise((resolve) => {
      const transaction = db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(SETS_KEY);
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => resolve([]);
    });
  } catch (e) {
    console.warn("Could not init DB for loading sets", e);
    return [];
  }
};

// --- COMMUNITY DECKS (NEW) ---
export const saveCommunityDecksToDB = async (decks) => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.put(decks, COMMUNITY_KEY);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (e) {
    console.error("Failed to save community decks to DB", e);
    return false;
  }
};

export const loadCommunityDecksFromDB = async () => {
  try {
    const db = await initDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(COMMUNITY_KEY);
      request.onsuccess = () => resolve(request.result || {});
      request.onerror = () => resolve({});
    });
  } catch (e) {
    console.warn("Could not init DB for loading community decks", e);
    return {};
  }
};