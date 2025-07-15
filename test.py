import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4.element import Tag
from newspaper import Article, Config
import datetime

def scrape_article_with_selenium(url: str) -> list | None:
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        import time
        time.sleep(5) 

        html = driver.page_source

        config = Config()
        config.browser_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" # Still good practice
        article = Article(url, config=config)
        article.set_html(html) 
        article.parse()

        print([article.publish_date, article.url, article.source_url])
        return [article.publish_date, article.url, article.source_url]

    except Exception as e:
        print(f"Error scraping {url} with Selenium: {e}")
        return None
    finally:
        if 'driver' in locals() and driver:
            driver.quit() 

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
    print(list(urls))
    return list(urls)

def get_url(url: str):
    try:
        article = Article(url)
        article.download()
        article.parse()
        print([article.text, article.publish_date, article.url, article.source_url])
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Test the function
get_url("https://www.nbcnews.com/world/middle-east/children-killed-israel-strike-gaza-health-clinic-rcna217989")