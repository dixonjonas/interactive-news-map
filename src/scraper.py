from newspaper import Article
from bs4 import BeautifulSoup
import requests

def get_article_urls(base_url: str) -> list:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/2025/07/08") and not href.endswith(".html"):
            full_url = "https://edition.cnn.com" + href
            urls.add(full_url)

    return list(urls)

def scrape_article(url: str) -> list:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return [article.text, article.publish_date, article.url]
    except Exception as e:
        print(f"Error scraping article {url}: {e}")
        return None