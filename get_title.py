import requests, json
from bs4 import BeautifulSoup as bs
from redis import Redis
#from celery import Celery
from concurrent.futures import ThreadPoolExecutor, as_completed

#app = Celery("on_test", broker='redis://127.0.0.01/1')


connection = Redis(db=1)


urls = []
with open('links.txt', mode='r', encoding='utf-8') as fout:
    for link in fout:
        if link.strip():
            urls.append(link)

#print(urls)

def get_html(url):
    try:
        resp = requests.get(url)
        return resp.content
    except Exception as e:
        print(e)

def extract_title(soup):
    return soup.title.string.strip()

def crawl(url):
    html = get_html(url)
    soup = bs(html, 'html.parser')
    title = extract_title(soup)
    set_content(url, title)
    print(title)
    return title


def set_content(key, value): 
    connection.hset("url&title", key=key, value=value)


def add_queue(url):
    connection.sadd('in_queue', url)

def visited(url):
    connection.sadd('visited', url)

def seen(url):
    return connection.sismember('visited', url)

def main(url):
    add_queue(url)
    if seen(url):
        print("url is before seen")
        return 0
    else:
        print('url is crawled')
        crawl(url)
        print('url is transformed from queue to visited')
        connection.smove('in_queue', 'visited', url)
        return 1


def runner():
    threads = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        for url in urls:
            threads.append(executor.submit(main, url))
        for task in as_completed(threads):
            print(task.result())


runner()

    


