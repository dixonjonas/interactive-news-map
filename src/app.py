from scraper import scrape_article
from llm_processor import process_article
from map_generator import create_interactive_map_with_pins

scraped_article = scrape_article("https://edition.cnn.com/2025/06/30/politics/trump-tax-spending-bill-congress")
processed_article = process_article(scraped_article[0], scraped_article[1], scraped_article[2])
create_interactive_map_with_pins([processed_article])