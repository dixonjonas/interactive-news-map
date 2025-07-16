from flask import Flask, render_template, request
from db import Session, Article
from map_generator import create_interactive_map_with_pins
import logging
from logging.handlers import RotatingFileHandler
import os

# TODO: Test logger for app and scraper

app = Flask(__name__)
session = Session()

if not app.debug:
    # In production, log to a file.
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/news_map.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('News Map startup')

@app.route('/', methods=['GET'])
def index():
    selected_date = request.args.get('date')
    selected_source = request.args.get('source')

    app.logger.info(f"Request received for map with filters: date='{selected_date}', source='{selected_source}'")
    
    query = session.query(Article)
    if selected_date:
        query = query.filter(Article.publish_date == selected_date)
    if selected_source:
        query = query.filter(Article.source_url == selected_source)

    articles = query.all()
    app.logger.info(f"Found {len(articles)} articles matching filters.")

    raw_jsons = [a.raw_json for a in articles]
    map_html = create_interactive_map_with_pins(raw_jsons)

    # Write map HTML to static file for iframe use
    with open("static/map.html", "w", encoding="utf-8") as f:
        f.write(map_html)

    # Get all unique publish dates for dropdown
    all_dates = sorted({a.publish_date.strftime('%Y-%m-%d') for a in session.query(Article).all()}, reverse=True)

    return render_template("index.html", all_dates=all_dates, selected_date=selected_date, selected_source=selected_source)

if __name__ == '__main__':
    app.run(debug=True)
