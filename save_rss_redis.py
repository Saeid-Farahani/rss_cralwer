#!/usr/bin/env python3
import os
from redis import Redis

r = Redis(host='redis', port=6379 , db=1)
#r = Redis(db=1)


while True:
    with open("rss_urls") as f:
        for url in f:
            url = url.strip()
            if url and not r.sismember("rss_urls", url):
                r.sadd("rss_urls", url)
