"use strict";

const CACHE_VER = "v3";
const FILES_TO_CACHE = [
    "/sw.js",
    "/manifest.json",
    "/static/21.ico",
    "/static/21.png",
    "/static/axios.min.js",
    "/static/bulma.min.css",
    "/static/bulma-burger.js",
    "/rule",
    "/offline",
];

self.addEventListener("install", function(e) {
    console.log("등록중...");
    e.waitUntil(
        caches.open(CACHE_VER).then(function(cache) {
            return cache.addAll(FILES_TO_CACHE);
        })
    );
});

self.addEventListener("activate", function(e) {
    e.waitUntil(
        caches.keys().then(function(keyList) {
            return Promise.all(keyList.map(function(key) {
                if(key !== CACHE_VER) {
                    console.log("구버전 리소스 제거 : "+key);
                    return caches.delete(key);
                }
            }));
        })
    );
});

self.addEventListener("fetch", function(e) {
    e.respondWith(
        caches.match(e.request).then(function(r) {
            console.log("리소스 가져옴 : "+e.request.url);
            return r || fetch(e.request).then(function(response) {
                return caches.open(CACHE_VER).then(function(cache) {
                    if (e.request.url.startsWith(location.protocol+"//"+location.host+"/static/card_img/") && e.request.url.endsWith(".png") ){
                        cache.put(e.request, response.clone());
                        console.log("카드 이미지 캐싱됨 : "+e.request.url);
                    } return response;
                });
            });
        }).catch(function() {
            return caches.match("/offline");
        })
    );
});