const CACHE_NAME = "ci-dashboard-cache-v1";
const BASE_PATH = "/app-agents/";
const urlsToCache = [
  `${BASE_PATH}`,
  `${BASE_PATH}index.html`,
  `${BASE_PATH}index.js`,
  `${BASE_PATH}style.css`,
  `${BASE_PATH}manifest.json`,
  `${BASE_PATH}components/ci-agent.js`,
  `${BASE_PATH}status.json`,
  "https://civic-interconnect.github.io/app-core/components/ci-header/ci-header.js",
  "https://civic-interconnect.github.io/app-core/components/ci-footer/ci-footer.js",
  "https://civic-interconnect.github.io/app-core/styles/tokens.css",
  "https://civic-interconnect.github.io/app-core/styles/themes.css",
  "https://civic-interconnect.github.io/app-core/styles/base.css",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then(
      (response) => response || fetch(event.request)
    )
  );
});
