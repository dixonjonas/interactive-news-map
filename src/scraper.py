import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4.element import Tag
from newspaper import Article, Config
import datetime
import time

# TODO: fix reuters scraper with selenium

def scrape_article(url: str) -> list | None:
    if "www.reuters.com" in url:
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            time.sleep(5) 

            html = driver.page_source

            config = Config()
            config.browser_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" # Still good practice
            article = Article(url, config=config)
            article.set_html(html) 
            article.parse()

            return [article.text, article.publish_date, article.url, article.source_url]

        except Exception as e:
            print(f"Error scraping {url} with Selenium: {e}")
            return None
        finally:
            if 'driver' in locals() and driver:
                driver.quit()
    else:
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
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(base_url)

        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        urls = set()

        for a_tag in soup.find_all("a", href=True):
            if isinstance(a_tag, Tag):
                href = a_tag.get("href")
                if isinstance(href, str) and href.endswith(datetime.datetime.now().strftime("%Y-%m-%d") + "/"):
                    if href.startswith("/"):
                        urls.add("https://www.reuters.com" + href)
                    else: 
                        urls.add(href)
        return list(urls)
                    
    except Exception as e:
        print(f"Error fetching Reuters URLs with Selenium: {e}")
        return [] 
    finally:
        if driver:
            driver.quit()

def get_all_article_urls() -> list[str]:
    urls = set()
    urls.update(get_cnn_urls())
    urls.update(get_ap_urls())
    urls.update(get_reuters_urls())
    return list(urls)
