// 빨강이 똑똑 놀이터 오프라인 캐시 (홈 화면 앱용)
// 앱을 고쳐서 다시 올릴 때마다 아래 버전 숫자를 하나씩 올려주세요 (v1 → v2 ...)
const CACHE = 'nori-v7';
const ASSETS = [
  './',
  './index.html',
  './nori.html',
  './manifest-nori.json',
  './icon-nori-180.png',
  './icon-nori-192.png',
  './icon-nori-512.png',
  './icon-nori-512-maskable.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS.map(u => new Request(u, {cache: 'reload'}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;

  // 페이지(HTML)는 네트워크 우선: 새 버전을 올리면 온라인일 때 바로 반영
  if (e.request.mode === 'navigate'){
    e.respondWith(
      fetch(e.request).then(res => {
        if (res.ok){ const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
        return res;
      }).catch(() => caches.match(e.request).then(hit => hit || caches.match('./nori.html')))
    );
    return;
  }

  // 나머지 리소스(아이콘, 폰트 등)는 캐시 우선
  e.respondWith(
    caches.match(e.request).then(hit =>
      hit ||
      fetch(e.request).then(res => {
        const copy = res.clone();
        if (res.ok || res.type === 'opaque'){ caches.open(CACHE).then(c => c.put(e.request, copy)); }
        return res;
      })
    )
  );
});
