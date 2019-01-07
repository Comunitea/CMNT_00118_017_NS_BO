/* Service Worker for Progressive Web App and SEO */
importScripts('/cache-polyfill.js');

/* cache the page assets */
self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('airhorner').then(function(cache) {
            console.log("Page Assets Cached");
            return cache.addAll([
                '/',
                '/shop',
                '/page/contactus',
                '/page/entrega',
                '/page/sobre-nosotros',
                '/page/pago-seguro',
                '/page/devoluciones',
                '/page/politica-de-cookies',
                '/page/condiciones-legales',
                '/terms-of-use',
                '/privacy-policy',
                '/legal/advice',
                '/blog/blog-1',
                '/theme_adds/static/js/script.js',
                '/theme_adds/static/img/404-camilla.jpg'
            ]);
        })
    );
});

/* To make the application work offline it is need to pull the request from the cache, if it is available */
self.addEventListener('fetch', function(event) {
    /* log the requests made from the parent page */
    console.log(event.request.url);
    event.respondWith(
        caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
        })
    );
});