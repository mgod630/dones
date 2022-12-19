const APP_SHELL_CACHE_NAME = 'app-shell-cache-v28';
const APP_SHELL_CACHE_URLS = [
  '/',
  '/static/css/fontawesome.min.css',
  '/static/css/bootstrap.min.css',
  '/static/css/layout.css',
  '/static/css/index.css',
  '/static/js/app.js',
  '/static/js/jquery-3.4.1.min.js',
  '/static/js/bootstrap.bundle.min.js',
  '/static/js/main.js',
  '/static/template/samah_logo.png',
  '/static/contents/ins_logo_2.jpg',
  '/static/fonts/fa-solid-900.woff',
  '/static/fonts/IRANSansWeb_400.woff',
  '/static/fonts/IRANSansWeb_800.woff',
  '/static/fonts/fa-light-300.woff',
  '/static/fonts/fa-regular-400.woff',
  '/static/fonts/IRANSansWeb_600.woff',
  '/static/contents/course_1.jpg',
  '/static/template/social-medias.png',
  '/static/template/samah_logo_white.png',
  '/static/template/samandehi.png',
  '/static/template/etemad.png',
  '/static/template/favicon.ico',
  '/static/css/layout.css',
  '/static/css/index.css',
  '/static/pwa_files/manifest.json',
  '/static/pwa_files/images/icons/icon-144x144.png',
  '/static/css/layout.css?4',
  '/static/css/index.css?2',
  '/course-info/course_1',
];

const DYNAMIC_CACHE_NAME = 'dynamic-cache-v14';
const DYNAMIC_CACHE_URLS = [
  '/page1',
];

// install event
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    async function () {
      const cache = await caches.open(APP_SHELL_CACHE_NAME);
      console.log(APP_SHELL_CACHE_NAME + ':')
      APP_SHELL_CACHE_URLS.forEach(item => {
        cache.add(new Request(item))//.then(reuslt => console.log('request: "' + item + '" was added!'),
        //error => console.log('request: "' + item + '" was not added!'));
      })
    }()
  )
})

// activate event
self.addEventListener('activate', evt => {
  evt.waitUntil(
    caches.keys().then(keys => {
      keys.forEach(key => {
        if (key !== APP_SHELL_CACHE_NAME) {
          caches.delete(key).then(() => console.log(key, 'deleted.'))
        }
      });
    })
  );
});

// fetch events
self.addEventListener('fetch', event => {
  event.respondWith(async function () {
    const request_url = event.request.url.substring(event.request.url.indexOf('/', 8));
    // if (DYNAMIC_CACHE_URLS.includes(request_url)) {
    if (APP_SHELL_CACHE_URLS.includes(request_url) == false) {
      caches.open(DYNAMIC_CACHE_NAME).then(function (cache) { cache.add(event.request); });
    }
    let response = null;
    try {
      //response = await caches.match(event.request) || await fetch(event.request);
      response = await caches.match(event.request);
      if (!response) {
        console.log(event.request.url);
        response = await fetch(event.request);
      }
    } catch (error) {
      response = caches.match('/fallback');
    }
    return response;
  }());
});
