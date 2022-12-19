const staticCacheName = 'site-static-v2';
const dynamicCacheName = 'site-dynamic-v1';
const assets = [
    '/',
    '/static/css/fontawesome.min.css',
    '/static/css/bootstrap.min.css',
    '/static/css/layout.css?4',
    '/static/css/index.css?2',
    '/static/js/jquery-3.4.1.min.js',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/main.js',
    '/static/js/app.js',
    '/static/template/samah_logo.png',
    '/static/redis_data_management/logo.jpeg',
    '/static/redis_data_management/dones-logo.png',
    '/static/template/samah_logo_white.png',
    '/static/redis_data_management/Corona.jpg',
    '/static/redis_data_management/english.jpg',
    '/static/template/social-medias.png',
    '/static/fonts/fa-solid-900.woff',
    '/static/fonts/IRANSansWeb_400.woff',
    '/static/fonts/IRANSansWeb_800.woff',
    '/static/fonts/fa-light-300.woff',
    '/static/fonts/fa-regular-400.woff',
    '/static/fonts/IRANSansWeb_600.woff',
    '/static/pwa_files/manifest.json',
    '/static/template/favicon.ico',
    '/static/pwa_files/images/icons/icon-144x144.png',
    // 'https://www.google-analytics.com/collect?v=1&_v=j83&a=1950364541&t=pageview&_s=1&dl=http%3A%2F%2Flocalhost%2F&ul=en-us&de=UTF-8&dt=%D8%AF%D9%88%D9%86%D8%B3&sd=24-bit&sr=2560x1440&vp=1047x410&je=0&_u=AACAAUAB~&jid=&gjid=&cid=496723534.1593067465&tid=UA-162211474-1&_gid=1030605410.1593067465&gtm=2ou6h1&z=1593376757',
    // 'https://www.google-analytics.com/analytics.js',
    // 'https://trustseal.enamad.ir/logo.aspx?id=76455&Code=WrmgefBUun3s5LRhltaB',
    // 'https://www.googletagmanager.com/gtag/js?id=UA-162211474-1',
    // 'https://logo.samandehi.ir/logo.aspx?id=99856&p=bsiybsiyaqgwujynwlbq',
];

// cache size limit function
const limitCacheSize = (name, size) => {
  caches.open(name).then(cache => {
    cache.keys().then(keys => {
      if(keys.length > size){
        cache.delete(keys[0]).then(limitCacheSize(name, size));
      }
    });
  });
};

// install event
self.addEventListener('install', evt => {
  self.skipWaiting();
  //console.log('service worker installed');
  evt.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      console.log('caching shell assets');
      cache.addAll(assets);
    })
  );
});

// activate event
self.addEventListener('activate', evt => {
  //console.log('service worker activated');
  evt.waitUntil(
    caches.keys().then(keys => {
      //console.log(keys);
      return Promise.all(keys
        .filter(key => key !== staticCacheName && key !== dynamicCacheName)
        .map(key => caches.delete(key))
      );
    })
  );
});

// fetch event
self.addEventListener('fetch', evt => {
  //console.log('fetch event', evt);
  evt.respondWith(
    caches.match(evt.request).then(cacheRes => {
      return cacheRes || fetch(evt.request).then(fetchRes => {
        return caches.open(dynamicCacheName).then(cache => {
          cache.put(evt.request.url, fetchRes.clone());
          // check cached items size
          limitCacheSize(dynamicCacheName, 15);
          return fetchRes;
        })
      });
    }).catch(() => {
      if(evt.request.url.indexOf('.html') > -1){
        return caches.match('/pages/fallback.html');
      } 
    })
  );
});