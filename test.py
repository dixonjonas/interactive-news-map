from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

# Test the function
scrape_article_with_selenium("https://www.reuters.com/world/trump-tariffs-live-eu-trade-ministers-meeting-discuss-new-us-30-rate-2025-07-14/")