from flask import Flask, render_template, request, jsonify
from db import Session, Article
import logging
from logging.handlers import RotatingFileHandler
import os
from sqlalchemy import func

app = Flask(__name__)

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

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Closes the database session at the end of the request."""
    Session.remove()

@app.route('/', methods=['GET'])
def index():
    """Renders the main map page."""
    all_topics = sorted({a.topic for a in Session.query(Article.topic).distinct()})
    all_dates = sorted({a.publish_date.strftime('%Y-%m-%d') for a in Session.query(Article.publish_date).all()}, reverse=True)
    all_sources = sorted({a.source_url for a in Session.query(Article.source_url).distinct()})
    
    app.logger.info("Serving main index.html page.")
    return render_template("index.html", all_dates=all_dates, all_sources=all_sources, all_topics=all_topics)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Provides article data as JSON based on query filters."""
    selected_date = request.args.get('date')
    selected_source = request.args.get('source')
    selected_topic = request.args.get('topic')
    
    app.logger.info(f"API request for articles with filters: topic='{selected_topic}', date='{selected_date}', source='{selected_source}'")
    
    query = Session.query(Article)
    if selected_topic:
        query = query.filter(Article.topic == selected_topic)
    if selected_date:
        query = query.filter(Article.publish_date == selected_date)
    if selected_source:
        query = query.filter(Article.source_url == selected_source)

    articles = query.all()
    
    articles_data = []
    for article in articles:
        articles_data.append({
            "title": article.title,
            "topic": article.topic,
            "coords": [article.latitude, article.longitude],
            "info": {
                "summary": article.summary,
                "location": article.location,
                "date": article.publish_date.strftime('%Y-%m-%d'),
                "url": article.url,
            },
            "source": article.source_url
        })
        
    app.logger.info(f"API sending {len(articles_data)} articles.")
    return jsonify(articles_data)

if __name__ == '__main__':
    app.run(debug=True)
