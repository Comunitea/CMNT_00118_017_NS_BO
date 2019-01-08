/* Service Worker for Progressive Web App and SEO */
importScripts('/theme_adds/static/js/cache-polyfill.js');

self.addEventListener('install', function(e) {
 e.waitUntil(
   caches.open('nostrum_cache').then(function(cache) {
     return cache.addAll([
        '/',
        '/shop',
        '/shop?homescreen=1',
        '/page/contactus',
        '/page/entrega',
        '/page/sobre-nosotros',
        '/page/pago-seguro',
        '/page/devoluciones',
        '/page/politica-de-cookies',
        '/page/condiciones-legales',
        '/legal/terms-of-use',
        '/legal/privacy-policy',
        '/legal/advice',
        '/shop/cart',
        '/blog/blog-1',
     ]);
   })
 );
});

self.addEventListener('fetch', function(event) {
  console.log(event.request.url);
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});