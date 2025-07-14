import schedule
import time
import subprocess

def run_scraper():
    subprocess.run(["python", "run_scraping.py"])

# Schedule at 9am and 9pm
schedule.every().day.at("09:00").do(run_scraper)
schedule.every().day.at("21:00").do(run_scraper)

while True:
    schedule.run_pending()
    time.sleep(60)