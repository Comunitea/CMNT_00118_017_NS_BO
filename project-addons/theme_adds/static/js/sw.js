/* Service Worker for Progressive Web App and SEO */
importScripts('/theme_adds/static/js/cache-polyfill.js');

self.addEventListener('install', function(e) {
 e.waitUntil(
   caches.open('nostrum_cache').then(function(cache) {
     return cache.addAll([
        '/shop?homescreen=1',
        '/web/static/lib/fontawesome/fonts/fontawesome-webfont.woff2',
        '/clarico_base/static/src/font/Oswald-Light.ttf',
        '/clarico_base/static/src/font/Muli-Regular.ttf',
        '/clarico_base/static/src/font/Muli-Bold.ttf',
        '/clarico_base/static/src/font/Muli-Light.ttf',
        '/clarico_base/static/src/font/Oswald-Regular.ttf',
        '/theme_adds/static/js/script.js',
        '/theme_adds/static/img/logo-head.png',
        '/theme_adds/static/img/revi-widget-demo.png',
        '/theme_adds/static/img/404-skeleton.jpg',
        '/theme_adds/static/img/404-camilla.jpg',
        '/theme_adds/static/img/favicon_512.png',
        '/theme_adds/static/img/favicon_192.png',
        '/theme_adds/static/img/favicon_144.png',
        '/theme_adds/static/img/favicon_96.png',
        '/theme_adds/static/img/favicon_72.png',
        '/theme_adds/static/img/favicon_48.png',
        '/checkout_coupon/static/js/checkout.js'
     ]);
   })
 );
});

self.addEventListener('fetch', function(event) {
//  console.log(event.request.url);
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
