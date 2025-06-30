from newspaper import Article

def scrape_article(url: str) -> list:
    article = Article(url)
    article.download()
    article.parse()
    return [article.text, article.publish_date, article.url]