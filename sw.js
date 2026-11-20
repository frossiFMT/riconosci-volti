// Cache dell'app e dei modelli: dopo la prima apertura funziona anche senza rete.
// Quando modifichi i file, aumenta il numero di versione qui sotto.
const CACHE = 'riconosci-volti-v1';
const FILES = [
  './', 'index.html', 'manifest.json', 'face-api.js',
  'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png',
  'models/tiny_face_detector_model-weights_manifest.json', 'models/tiny_face_detector_model.bin',
  'models/face_landmark_68_model-weights_manifest.json', 'models/face_landmark_68_model.bin',
  'models/face_recognition_model-weights_manifest.json', 'models/face_recognition_model.bin'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(r => r || fetch(e.request)));
});
