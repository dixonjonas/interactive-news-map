import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from newspaper import Article
import datetime
import logging

logger = logging.getLogger(__name__)

def scrape_article(url: str) -> list | None:
    try:
        article = Article(url)
        article.download()
        article.parse()
        if not article.text or not article.publish_date:
            logger.warning(f"Failed to extract text or date from {url}, skipping.")
            return None
        return [article.text, article.publish_date, article.url, article.source_url]
    except Exception as e:
        logger.error(f"Error downloading or parsing {url}: {e}", exc_info=True)
        return None

def get_cnn_urls() -> list[str]:
    base_url = "https://edition.cnn.com/world"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = set()
    for a_tag in soup.find_all("a", href=True):
        if isinstance(a_tag, Tag):
            href = a_tag.get("href")
            if isinstance(href, str) and href.startswith("/" + datetime.datetime.now().strftime("%Y/%m/%d")) and "/video/" not in href:
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
            if isinstance(href, str) and href.startswith("https://apnews.com/article/") and "/video/" not in href:
                urls.add(href)
    return list(urls)

def get_nbc_urls() -> list[str]:
    base_url = "https://www.nbcnews.com/world"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    min_length = 70
    excluded_segments = ["/video/", "/live-blog/"]

    urls = set()
    for a_tag in soup.find_all("a", href=True):
        if isinstance(a_tag, Tag):
            href = a_tag.get("href")
            if isinstance(href, str) and href.startswith("https://www.nbcnews.com/") and len(href) >= min_length:
                is_excluded = False
                for segment in excluded_segments:
                    if segment in href:
                        is_excluded = True
                        break 
                if is_excluded == False:
                    urls.add(href)
    return list(urls)

def get_all_article_urls() -> list[str]:
    urls = set()
    urls.update(get_cnn_urls())
    urls.update(get_ap_urls())
    urls.update(get_nbc_urls())
    return list(urls)
