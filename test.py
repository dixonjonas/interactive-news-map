import datetime
from newspaper import Article

def scrape_article(url: str) -> list | None:
    try:
        article = Article(url)
        article.download()
        article.parse()
        print([article.publish_date, article.url])
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

scrape_article("https://apnews.com/article/texas-floods-summer-camp-counselors-240a592ce3dc1accd8d8bb56196763fe")