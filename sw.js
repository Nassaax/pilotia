// Pilotia, service worker : site installable et page « hors connexion »
// (sur le modèle de LALLAT). Le réseau passe toujours en premier, pour que
// chaque visite affiche la dernière version ; la copie gardée ne sert que
// sans réseau. Les fonctions /api ne sont jamais mises en cache.
const VERSION = 'pilotia-v1';
const COQUILLE = ['/offline.html', '/style.css', '/fonts/fonts.css', '/fonts/inter-latin.woff2',
  '/app.js', '/animations.js', '/logo-header-light.png', '/logo-header-dark.png', '/icon-192.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(COQUILLE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((cles) => Promise.all(cles.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Réseau d'abord ; une réponse valide est gardée pour la prochaine fois sans réseau.
function reseauPuisCopie(req, secours) {
  return fetch(req).then((r) => {
    if (r.ok && r.type === 'basic') {
      const copie = r.clone();
      caches.open(VERSION).then((c) => c.put(req, copie));
    }
    return r;
  }).catch(() => caches.match(req).then((r) => r || secours()));
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin || url.pathname.startsWith('/api/')) return;
  if (req.mode === 'navigate') {
    e.respondWith(reseauPuisCopie(req, () => caches.match('/offline.html')));
  } else {
    e.respondWith(reseauPuisCopie(req, () => Response.error()));
  }
});
