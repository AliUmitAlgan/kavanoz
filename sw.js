const CACHE_NAME = 'bebinin-kavanozu-v5';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './apple-touch-icon.png',
  './icon-192.png',
  './icon-512.png',
  './music.mp3'
];

// Kurulum: Dosyaları önbelleğe al ve hemen aktifleş
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Etkinleşme: Tüm eski önbellekleri temizle ve istemcileri hemen devral
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('Eski önbellek temizlendi:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// İstek Yakalama: Sayfa gezintilerinde (HTML) HER ZAMAN önce Ağ (Network-First)!
// Böylece GitHub'a her güncelleme atıldığında telefon anında yeni sürümü alır.
self.addEventListener('fetch', (event) => {
  const request = event.request;

  // Sayfa HTML istekleri: Önce ağdan al, ağ yoksa önbellekten göster
  if (request.mode === 'navigate' || request.destination === 'document') {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, networkResponse.clone());
            return networkResponse;
          });
        })
        .catch(() => {
          return caches.match('./index.html') || caches.match('/');
        })
    );
    return;
  }

  // Statik dosyalar (resimler, müzik): Önce önbellek, yoksa ağ
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return networkResponse;
      });
    })
  );
});
