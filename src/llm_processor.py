from google import genai
import os
from dotenv import load_dotenv
import datetime
import logging

# TODO: Add topical groupings and filters

logger = logging.getLogger(__name__)
load_dotenv()

def process_article(article: str, publish_date: datetime.datetime, url: str) -> str:

    if publish_date.strftime("%Y-%m-%d") != datetime.datetime.now().strftime("%Y-%m-%d"):
        logger.info(f"Article from {publish_date.strftime('%Y-%m-%d')} is not from today, skipping. URL: {url}")
        return ""

    SYSTEM_PROMPT = """
    You are a helpful assistant that can summarize news articles into the following JSON format:
    {
        "title": "",
        "topic": "",
        "coords": [latitude, longitude],
        "info": {
            "summary": "",
            "location": "",
            "date": "",
            "url": "",
        }
    }
    The title should be the title of the article.
    The topic should be the topic of the article chosen from the following: Politics & Governance, Conflict & Security, Economy & Business, Environment & Climate, Health & Medicine, Society & Culture, Science & Technology.
    The coords should be the latitude and longitude of the location.
    The summary should be a concise summary of the article.
    The location should be the location of the article.
    The date should be the date of the article.
    The url should be the url of the article.
    
    An example of the JSON format for an article is:
    {
        "title": "Powerful Storm Disrupts Travel in Western France",
        "topic": "Environment & Climate",
        "coords": [46.603354, 1.888334],
        "info": {
            "summary": "A powerful storm disrupted travel across western France, bringing torrential rain and strong winds that felled trees and caused flash flooding. Airports experienced significant delays and cancellations, while train services faced widespread interruptions, leaving thousands of commuters and holidaymakers stranded as emergency crews worked to clear debris and restore essential transport links.",
            "location": "France",
            "date": "2025-06-29",
            "url": "https://example.com/news/western-france-storm-travel-disruption"
        }
    }
    """

    try:
        logger.info(f"Sending article to LLM for processing. URL: {url}")
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        model = "gemini-2.5-flash"
        response = client.models.generate_content(
            model=model,
            contents=SYSTEM_PROMPT + "\n\n" + article + "\n\n" + publish_date.strftime('%Y-%m-%d') + "\n\n" + url,
            config={
                "response_mime_type": "application/json"
            }
        )

        logger.info(f"LLM processing successful for URL: {url}")
        return response.text if response.text else ""
    
    except Exception as e:
        logger.error(f"LLM API call failed for URL {url}: {e}", exc_info=True)
        return ""