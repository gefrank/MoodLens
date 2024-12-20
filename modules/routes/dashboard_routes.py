import os
from flask import Blueprint, request, render_template
from flask_login import login_required
import pandas as pd
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
    log_file = "logs/sentiment_logs.csv"
    if not os.path.exists(log_file):
        return "No data available yet."

    # Load log data
    data = pd.read_csv(log_file)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # Apply date filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date:
        data = data[data['Timestamp'] >= start_date]
    if end_date:
        data = data[data['Timestamp'] <= end_date]

    # Insights
    total_texts = len(data)
    most_common_sentiment = data['Sentiment'].value_counts().idxmax() if not data.empty else "None"
    sentiment_counts = data['Sentiment'].value_counts().to_dict()
    avg_confidence = get_average_confidence(data)

    # Charts
    chart_url = generate_chart(data)
    interactive_chart = generate_interactive_line_chart(data)

    # Most frequent words
    positive_words = TextAnalyzer.get_most_frequent_words(data, "POSITIVE")
    negative_words = TextAnalyzer.get_most_frequent_words(data, "NEGATIVE")
    neutral_words = TextAnalyzer.get_most_frequent_words(data, "NEUTRAL")

    # Word clouds
    positive_wordcloud = TextAnalyzer.generate_wordcloud(data, "POSITIVE")
    negative_wordcloud = TextAnalyzer.generate_wordcloud(data, "NEGATIVE")
    neutral_wordcloud = TextAnalyzer.generate_wordcloud(data, "NEUTRAL")

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
