// Service worker di Riconosci Vacche.
// - La pagina e i file piccoli che cambiano a ogni versione (index.html, version.js,
//   firebase-config.js) si chiedono PRIMA alla rete: con la connessione arriva sempre
//   l'ultima versione; senza rete si usa la copia salvata.
// - I file grandi (modello, motore di calcolo, librerie) si prendono dalla cache.
// - La pagina registra "sw.js?v=<versione>": a ogni nuova versione il service worker
//   viene reinstallato e la cache rinnovata.
importScripts('version.js');
const CACHE = 'riconosci-vacche-' + APP_VERSION;
const FILES = [
  './', 'index.html', 'version.js', 'manifest.json', 'firebase-config.js', 'firebase-bundle.js',
  'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png',
  'ort/ort.wasm.min.js', 'ort/ort-wasm-simd-threaded.mjs', 'ort/ort-wasm-simd-threaded.wasm',
  'models/frisona_reid.onnx'
];
const FRESH = ['index.html', 'version.js', 'firebase-config.js', 'manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE)
    .then(c => c.addAll(FILES.map(f => new Request(f, {cache: 'reload'}))))
    .then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  const path = url.pathname.split('/').pop();
  const fresh = req.mode === 'navigate' || path === '' || FRESH.includes(path);
  if (fresh) {
    e.respondWith(
      fetch(req, {cache: 'no-store'})
        .then(r => { if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); } return r; })
        .catch(() => caches.match(req, {ignoreSearch: true}).then(r => r || caches.match('index.html')))
    );
    return;
  }
  e.respondWith(caches.match(req, {ignoreSearch: true}).then(r => r || fetch(req)));
});
