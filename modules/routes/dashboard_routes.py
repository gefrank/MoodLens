import os
import sqlite3
from flask import Blueprint, request, render_template
from flask_login import login_required
from modules.services.visualization_service import (
    generate_chart,
    generate_interactive_line_chart,
    get_average_confidence
)
from modules.utilities.text_analyzer import TextAnalyzer

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.route("/")
@login_required
def dashboard():
    db_file_path = "instance/moodlens.db"

    if not os.path.exists(db_file_path):
        return "No data available yet."

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Base query
    query = "SELECT Timestamp, Input_Text, Sentiment, Confidence FROM sentiment_logs"
    conditions = []
    params = []

    # Apply date filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date:
        conditions.append("Timestamp >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("Timestamp <= ?")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Execute the query
    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    data = [
        {"Timestamp": row[0], "Input_Text": row[1], "Sentiment": row[2], "Confidence": row[3]}
        for row in rows
    ]

    conn.close()

    if not data:
        return "No data matches the filters."

    # Convert data to Pandas DataFrame for further processing
    import pandas as pd
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Insights
    total_texts = len(df)
    most_common_sentiment = df['Sentiment'].value_counts().idxmax() if not df.empty else "None"
    sentiment_counts = df['Sentiment'].value_counts().to_dict()
    avg_confidence = get_average_confidence(df)

    # Charts
    chart_url = generate_chart(df)
    interactive_chart = generate_interactive_line_chart(df)

    # Most frequent words
    positive_words = TextAnalyzer.get_most_frequent_words(df, "POSITIVE")
    negative_words = TextAnalyzer.get_most_frequent_words(df, "NEGATIVE")
    neutral_words = TextAnalyzer.get_most_frequent_words(df, "NEUTRAL")

    # Word clouds
    positive_wordcloud = TextAnalyzer.generate_wordcloud(df, "POSITIVE")
    negative_wordcloud = TextAnalyzer.generate_wordcloud(df, "NEGATIVE")
    neutral_wordcloud = TextAnalyzer.generate_wordcloud(df, "NEUTRAL")

    return render_template(
        "dashboard.html",
        total_texts=total_texts,
        most_common_sentiment=most_common_sentiment,
        sentiment_counts=sentiment_counts,
        avg_confidence=avg_confidence,
        chart_url=chart_url,
        interactive_chart=interactive_chart,
        positive_words=positive_words,
        negative_words=negative_words,
        neutral_words=neutral_words,
        positive_wordcloud=positive_wordcloud,
        negative_wordcloud=negative_wordcloud,
        neutral_wordcloud=neutral_wordcloud,
    )
