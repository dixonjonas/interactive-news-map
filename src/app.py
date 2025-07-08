from scraper import get_article_urls, scrape_article
from llm_processor import process_article
from map_generator import create_interactive_map_with_pins

scraped_urls = get_article_urls("https://edition.cnn.com/world")
print(f"Found {len(scraped_urls)} articles")

processed_articles = []

for url in scraped_urls:
    result = scrape_article(url)
    if result:
        text, publish_date, final_url = result
        try:
            processed = process_article(text, publish_date, final_url)
            processed_articles.append(processed)
        except Exception as e:
            print(f"Error processing article {url}: {e}")

if processed_articles:
    create_interactive_map_with_pins(processed_articles)
else:
    print("No articles processed.")