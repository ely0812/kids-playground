// 런처(루트)용 서비스워커
// 역할: 옛 통합앱(dev/game) 시절 루트 스코프에 등록됐던 'kidpac-*' 캐시를 정리한다.
// 각 앱의 오프라인 캐시는 자기 폴더 SW(/pacman/sw.js, /nori/sw.js)가 담당하므로
// 여기서는 캐시를 새로 만들지 않고, 옛 찌꺼기만 비운 뒤 네트워크로 통과시킨다.
self.addEventListener('install', e => self.skipWaiting());

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith('kidpac')).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

// fetch 핸들러 없음 → 런처 페이지 요청은 항상 네트워크로 통과 (하위 앱 스코프는 건드리지 않음)
