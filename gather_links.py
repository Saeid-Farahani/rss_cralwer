import requests
from bs4 import BeautifulSoup as bs



rss_urls = {
        "https://www.farsnews.ir/rss",
        "https://www.irna.ir/rss",
        "https://www.mehrnews.com/rss",
        "https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D9%85%D9%87%D9%85%D8%AA%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1",
        "https://www.isna.ir/rss",
        "https://www.yjc.news/fa/rss/allnews"
       }


def get_xml(url):
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    else:
        return resp.content

def extract_links(url):
    xml = get_xml(url)
    soup = bs(xml, 'lxml')
    return {
        a.link.next_sibling.strip()
        for a in soup.find_all('item')
        }


def sotre_links():
    with open('links.txt', mode="w",
              encoding='utf-8') as fin:
        for url in rss_urls:
            links = extract_links(url)
            for link in links:
                fin.write(link)
                fin.write("\r\n")

sotre_links()


