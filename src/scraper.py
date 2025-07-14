import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4.element import Tag
from newspaper import Article, Config
import datetime

def scrape_article(url: str) -> list | None:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return [article.text, article.publish_date, article.url, article.source_url]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def get_cnn_urls() -> list[str]:
    base_url = "https://edition.cnn.com/world"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = set()
    for a_tag in soup.find_all("a", href=True):
        if isinstance(a_tag, Tag):
            href = a_tag.get("href")
            if isinstance(href, str) and href.startswith("/" + datetime.datetime.now().strftime("%Y/%m/%d")):
                urls.add("https://edition.cnn.com" + href)
    return list(urls)

def get_ap_urls() -> list[str]:
    base_url = "https://apnews.com/world-news"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = set()
    for a_tag in soup.find_all("a", href=True):
        if isinstance(a_tag, Tag):
            href = a_tag.get("href")
            if isinstance(href, str) and href.startswith("https://apnews.com/article/"):
                urls.add(href)
    return list(urls)

def get_reuters_urls() -> list[str]:
    base_url = "https://www.reuters.com/world/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = set()
    for a_tag in soup.find_all("a", href=True):
        if isinstance(a_tag, Tag):
            href = a_tag.get("href")
            if isinstance(href, str) and href.endswith(datetime.datetime.now().strftime("%Y-%m-%d") + "/"):
                urls.add("https://www.reuters.com" + href)
    return list(urls)

def get_all_article_urls() -> list[str]:
    urls = set()
    urls.update(get_cnn_urls())
    urls.update(get_ap_urls())
    urls.update(get_reuters_urls())
    return list(urls)
