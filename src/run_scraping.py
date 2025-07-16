from scraper import get_all_article_urls, scrape_article
from llm_processor import process_article
from db import Article, Session
import json
import time
import logging
#from map_generator import create_interactive_map_with_pins

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraping.log"), 
        logging.StreamHandler() 
    ]
)

logger = logging.getLogger(__name__)

session = Session()

logger.info("--- Starting scraping process ---")
try:
    scraped_urls = get_all_article_urls()
    print(scraped_urls)
    logger.info(f"Found {len(scraped_urls)} unique articles across all sources.")

    for url in scraped_urls[:30]:
        logger.info(f"Processing URL: {url}")

        result = scrape_article(url)
        if result:
            text, publish_date, final_url, source_url = result
            try:
                processed = process_article(text, publish_date, final_url)
                if not processed or (isinstance(processed, str) and processed.strip() == ""):
                    logger.info(f"Skipped empty processed result for: {url}")
                    continue

                try:
                    article_data = json.loads(processed) if isinstance(processed, str) else processed
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON returned from process_article for: {url}")
                    logger.debug(f"Received content: {processed}")
                    continue
        
                if session.query(Article).filter_by(url=final_url).first():
                    logger.info(f"Already in DB: {final_url}")
                    continue

                new_article = Article(
                    title=article_data["title"],
                    url=final_url,
                    summary=article_data["info"].get("summary", ""),
                    publish_date=publish_date,
                    latitude=article_data["coords"][0],
                    longitude=article_data["coords"][1],
                    location=article_data["info"].get("location", ""),
                    source_url=source_url,
                    raw_json=processed
                )

                session.add(new_article)
                session.commit()
                logger.info(f"SUCCESS: Added: {article_data['title']}")
            except Exception as e:
                logger.error(f"Error processing or saving article {url}: {e}", exc_info=True)
                session.rollback()

        time.sleep(7)

except Exception as e:
    logger.critical(f"A fatal error occurred in the main scraping process: {e}", exc_info=True)
finally:
    logger.info("--- Scraping process finished ---")

#all_articles = session.query(Article).all()
#processed_articles = [a.raw_json for a in all_articles]

#if processed_articles:
#    create_interactive_map_with_pins(processed_articles)
#else:
#    print("No articles processed.")
