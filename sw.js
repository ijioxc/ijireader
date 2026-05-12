const CACHE_NAME = 'english-listener-v2';
const ASSETS = [
  './index.html',
  './reader.html',
  './app.webmanifest'
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // 優先從網路獲取，失敗時從快取獲取 (Network First)
  // 因為章節內容已經用 IndexedDB 快取了，這裡主要處理 index.html 和基礎靜態資源
  e.respondWith(
    fetch(e.request).catch(async () => {
      const cached = await caches.match(e.request);
      if (cached) return cached;
      throw new Error('Network fail and no cache');
    })
  );
});
