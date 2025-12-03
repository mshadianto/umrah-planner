// ============================================
// LABBAIK Service Worker v1.0.0
// Simplified for Streamlit Cloud
// ============================================

const CACHE_VERSION = 'labbaik-v1';

// Install event
self.addEventListener('install', (event) => {
  console.log('[LABBAIK SW] Installing...');
  self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
  console.log('[LABBAIK SW] Activating...');
  event.waitUntil(clients.claim());
});

// Fetch event - network first strategy (Streamlit is dynamic)
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;
  
  // For Streamlit, we use network-first approach
  event.respondWith(
    fetch(event.request)
      .then(response => {
        return response;
      })
      .catch(() => {
        // Return cached version if available
        return caches.match(event.request);
      })
  );
});

console.log('[LABBAIK SW] Service Worker loaded');
