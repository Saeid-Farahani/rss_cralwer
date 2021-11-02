#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as bs
import concurrent.futures
from redis import Redis
from urllib.parse import urlparse


r = Redis(host='redis', port=6379 , db=1)
title_db = Redis(host='redis', port=6379, db=2)



redis_rss_set = 'rss_urls'
redis_links_set = "links"


def get_html(url):
    try:
        html = requests.get(url)
        return html.content
    except Exception as e:
        print(e)


def extract_links(url):
    xml = get_html(url)
    soup = bs(xml, 'lxml')
    return { a.link.next_sibling.strip()
            for a in soup.find_all('item')}

def extract_title(link):
    html = get_html(link)
    soup = bs(html, 'html.parser')
    return soup.title.string.strip()

def get_domain_name(url):
    url_splited = urlparse(url).netloc.split(".")
    if url_splited[1] in {'ir', 'com'}:
        return url_splited[0]
    return url_splited[1]



def save_links_to_redis(redis_links_set):
    for url in r.smembers(redis_rss_set):
        url = url.decode('utf-8')
        for link in extract_links(url):
            r.sadd(redis_links_set, link)


save_links_to_redis(redis_links_set)



def crawl(url):

    if not r.sismember("visited", url):
        r.sadd("visited", url)
        title = extract_title(url)
        name = get_domain_name(url.decode('utf-8'))
        print(f"{url} is crawling {title}")
        title_db.sadd(name, title)
        return title
    print(f"{url} is already seen")


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(crawl, r.smembers("links"))
