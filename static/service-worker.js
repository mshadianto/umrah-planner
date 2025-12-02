// ============================================
// LABBAIK Service Worker v1.0.0
// Progressive Web App - Offline Support
// ============================================

const CACHE_VERSION = 'labbaik-v1.0.0';
const OFFLINE_URL = '/app/static/offline.html';

// Static assets to cache immediately
const PRECACHE_ASSETS = [
  '/app/static/offline.html',
  '/app/static/icons/icon-192x192.png',
  '/app/static/icons/icon-512x512.png',
];

// Cache strategies
const CACHE_STRATEGIES = {
  // Cache first for static assets
  cacheFirst: [
    /\.(?:png|jpg|jpeg|svg|gif|webp|ico)$/,
    /\.(?:woff|woff2|ttf|eot)$/,
  ],
  // Network first for API and dynamic content
  networkFirst: [
    /\/_stcore\//,
    /\/api\//,
    /\.(?:js|css)$/,
  ],
  // Stale while revalidate for HTML
  staleWhileRevalidate: [
    /\.html$/,
    /\/$/,
  ]
};

// ============================================
// INSTALL EVENT
// ============================================
self.addEventListener('install', (event) => {
  console.log('[LABBAIK SW] Installing...');
  
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => {
        console.log('[LABBAIK SW] Caching offline assets');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(() => {
        console.log('[LABBAIK SW] Install complete');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[LABBAIK SW] Install failed:', error);
      })
  );
});

// ============================================
// ACTIVATE EVENT
// ============================================
self.addEventListener('activate', (event) => {
  console.log('[LABBAIK SW] Activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => cacheName !== CACHE_VERSION)
            .map((cacheName) => {
              console.log('[LABBAIK SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('[LABBAIK SW] Claiming clients');
        return self.clients.claim();
      })
  );
});

// ============================================
// FETCH EVENT
// ============================================
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') return;
  
  // Skip chrome-extension and other non-http(s) requests
  if (!url.protocol.startsWith('http')) return;
  
  // Skip cross-origin requests (except CDNs we trust)
  const trustedOrigins = [
    self.location.origin,
    'https://cdn.jsdelivr.net',
    'https://cdnjs.cloudflare.com',
    'https://fonts.googleapis.com',
    'https://fonts.gstatic.com',
  ];
  
  if (!trustedOrigins.some(origin => url.href.startsWith(origin))) return;
  
  // Determine strategy based on URL
  let strategy = 'networkFirst'; // default
  
  for (const [strat, patterns] of Object.entries(CACHE_STRATEGIES)) {
    if (patterns.some(pattern => pattern.test(url.pathname))) {
      strategy = strat;
      break;
    }
  }
  
  event.respondWith(handleFetch(request, strategy));
});

// ============================================
// FETCH HANDLERS
// ============================================

async function handleFetch(request, strategy) {
  switch (strategy) {
    case 'cacheFirst':
      return cacheFirst(request);
    case 'networkFirst':
      return networkFirst(request);
    case 'staleWhileRevalidate':
      return staleWhileRevalidate(request);
    default:
      return networkFirst(request);
  }
}

// Cache First Strategy
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    return getOfflineFallback(request);
  }
}

// Network First Strategy
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    return getOfflineFallback(request);
  }
}

// Stale While Revalidate Strategy
async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_VERSION);
  const cachedResponse = await cache.match(request);
  
  const networkResponsePromise = fetch(request).then((networkResponse) => {
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  }).catch(() => null);
  
  return cachedResponse || networkResponsePromise || getOfflineFallback(request);
}

// Offline Fallback
async function getOfflineFallback(request) {
  // For navigation requests, show offline page
  if (request.mode === 'navigate') {
    const offlineResponse = await caches.match(OFFLINE_URL);
    if (offlineResponse) {
      return offlineResponse;
    }
  }
  
  // For images, return a placeholder
  if (request.destination === 'image') {
    return new Response(
      '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="#1A1A1A" width="200" height="200"/><text fill="#D4AF37" x="50%" y="50%" text-anchor="middle" dy=".3em" font-family="sans-serif">Offline</text></svg>',
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }
  
  // Default offline response
  return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
}

// ============================================
// BACKGROUND SYNC (Future)
// ============================================
self.addEventListener('sync', (event) => {
  if (event.tag === 'labbaik-sync') {
    console.log('[LABBAIK SW] Background sync triggered');
    // Future: sync offline data
  }
});

// ============================================
// PUSH NOTIFICATIONS (Future)
// ============================================
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  
  const options = {
    body: data.body || 'Ada update dari LABBAIK!',
    icon: '/app/static/icons/icon-192x192.png',
    badge: '/app/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/',
      dateOfArrival: Date.now()
    },
    actions: [
      { action: 'open', title: 'Buka' },
      { action: 'close', title: 'Tutup' }
    ],
    tag: 'labbaik-notification',
    renotify: true
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'LABBAIK', options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'close') return;
  
  const urlToOpen = event.notification.data?.url || '/';
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((windowClients) => {
        // Focus existing window if available
        for (const client of windowClients) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            client.navigate(urlToOpen);
            return client.focus();
          }
        }
        // Open new window
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});

// ============================================
// MESSAGE HANDLER
// ============================================
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
  
  if (event.data === 'getVersion') {
    event.ports[0].postMessage({ version: CACHE_VERSION });
  }
});

console.log('[LABBAIK SW] Service Worker loaded');
