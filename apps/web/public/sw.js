/**
 * Service Worker for Nagpur Krishi Data PWA.
 * Provides offline operation for farmers in Nagpur district with poor/no connectivity.
 */

const CACHE_NAME = "nagpur-krishi-v1";
const API_CACHE_NAME = "nagpur-krishi-api-v1";

const STATIC_ASSETS = [
  "/",
  "/manifest.json",
  "/icons/icon-192.svg",
  "/icons/icon-512.svg",
];

// Install Event
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate Event: Clear old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key !== API_CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Event: Network-first for API with offline cache fallback
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle API Requests: Network First, fallback to cached API response
  if (url.pathname.startsWith("/api/v1/")) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(API_CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            return new Response(
              JSON.stringify({
                error: "Offline",
                detail: "इंटरनेट कनेक्शन उपलब्ध नाही. कृपया आधी सिंक केलेला डेटा पहा.",
                status: 503,
              }),
              {
                status: 503,
                headers: { "Content-Type": "application/json" },
              }
            );
          });
        })
    );
    return;
  }

  // Handle Static Pages & Assets: Cache first with network fallback
  event.respondWith(
    caches.match(request).then((cached) => {
      return (
        cached ||
        fetch(request)
          .then((response) => {
            if (response && response.status === 200 && request.method === "GET") {
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseClone);
              });
            }
            return response;
          })
          .catch(() => caches.match("/"))
      );
    })
  );
});
