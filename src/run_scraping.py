from scraper import get_all_article_urls, scrape_article
from llm_processor import process_article
from map_generator import create_interactive_map_with_pins
from db import Article, Session
import json
import time
from datetime import datetime

session = Session()

scraped_urls = get_all_article_urls()
print(scraped_urls)
print(f"Found {len(scraped_urls)} articles across all sources")

for url in scraped_urls:
    result = scrape_article(url)
    if result:
        text, publish_date, final_url, source_url = result
        try:
            processed = process_article(text, publish_date, final_url)
            if not processed or (isinstance(processed, str) and processed.strip() == ""):
                print(f"Skipped empty processed result for: {url}")
                continue

            try:
                article_data = json.loads(processed) if isinstance(processed, str) else processed
            except json.JSONDecodeError:
                print(f"Invalid JSON returned from process_article for: {url}")
                continue
            
            # Skip if already in DB (based on URL)
            if session.query(Article).filter_by(url=final_url).first():
                print(f"Already in DB: {final_url}")
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
            print(f"Added: {article_data['title']}")
        except Exception as e:
            print(f"Error processing article {url}: {e}")
    time.sleep(7)

#all_articles = session.query(Article).all()
#processed_articles = [a.raw_json for a in all_articles]

#if processed_articles:
#    create_interactive_map_with_pins(processed_articles)
#else:
#    print("No articles processed.")
