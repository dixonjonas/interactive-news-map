from flask import Flask, render_template, request
from db import Session, Article
from map_generator import create_interactive_map_with_pins
import json
from typing import cast

app = Flask(__name__)
session = Session()

@app.route('/', methods=['GET'])
def index():
    selected_date = request.args.get('date')
    
    query = session.query(Article)
    articles = query.all()

    # ---- START: DEBUGGING ----
    
    print(f"✅ STEP 1: Found {len(articles)} articles in the database.")

    if not articles:
        print("🔴 The query returned no articles. The database might be empty or in a different location.")

    else:
        # 1. Get the raw JSON strings
        raw_jsons = [a.raw_json for a in articles]
        print(f"✅ STEP 2: The first raw JSON string from the DB is:\n{raw_jsons[0]}")
        
        # 2. Parse JSON
        parsed_articles = []
        for article_json in raw_jsons:
            if article_json is not None:
                try:
                    parsed_articles.append(json.loads(cast(str, article_json)))
                except json.JSONDecodeError:
                    print(f"⚠️ WARNING: A JSON string was invalid and could not be parsed.")
        
        print(f"✅ STEP 3: Successfully parsed {len(parsed_articles)} articles.")

        if parsed_articles:
            print(f"✅ STEP 4: The first parsed article dictionary is:\n{parsed_articles[0]}")
            # Check this output carefully in your terminal!
            # Does it have a key like "coords"?
            # Are the values for that key valid numbers?
            # Example: {'title': '...', 'coords': [40.7128, -74.0060], ...}
    
    # ---- END: DEBUGGING ----

    # This is the original logic using the (now verified) parsed data
    map_html = create_interactive_map_with_pins(parsed_articles)

    # Write map HTML to static file
    with open("static/map.html", "w", encoding="utf-8") as f:
        f.write(map_html)

    # Get all unique publish dates
    all_dates = sorted({a.publish_date.strftime('%Y-%m-%d') for a in session.query(Article).all()}, reverse=True)

    return render_template("index.html", all_dates=all_dates, selected_date=selected_date)

if __name__ == '__main__':
    app.run(debug=True)