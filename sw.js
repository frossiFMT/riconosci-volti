// Cache dell'app e dei modelli: dopo la prima apertura funziona anche senza rete.
// Il nome della cache dipende dalla versione in version.js: cambiando la versione
// l'app scarica i file nuovi e cancella quelli vecchi.
importScripts('version.js');
const CACHE = 'riconosci-vacche-' + APP_VERSION;
const FILES = [
  './', 'index.html', 'version.js', 'manifest.json',
  'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png',
  'ort/ort.wasm.min.js', 'ort/ort-wasm-simd-threaded.mjs', 'ort/ort-wasm-simd-threaded.wasm',
  'models/frisona_reid.onnx'
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
