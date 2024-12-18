import os
import pandas as pd
from flask import Flask, request, render_template
from transformers import pipeline
from logger import log_sentiment  # Import logging function

# Visualization imports
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Suppress symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

app = Flask(__name__)

sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", 
    revision="714eb0f")

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        text = request.form["text"].strip()
        if not text:
            result = "Please enter some text to analyze."
        else:
            sentiment = sentiment_pipeline(text)
            label = sentiment[0]["label"]
            score = sentiment[0]["score"]
            result = f"Sentiment: {label} (Confidence: {score:.2f})"

            # Log the result
            log_sentiment(text, label, score)
    else:
        text = ""
    return render_template("index.html", result=result)


def generate_chart(data):
    # Sentiment counts
    sentiment_counts = data['Sentiment'].value_counts()

    # Generate Bar Chart
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))  # Two side-by-side charts
    ax[0].bar(sentiment_counts.index, sentiment_counts.values, color=['red', 'green', 'gray'])
    ax[0].set_title("Sentiment Distribution")
    ax[0].set_ylabel("Count")

    # Generate Pie Chart
    ax[1].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['red', 'green', 'gray'])
    ax[1].set_title("Sentiment Proportions")

    # Save the chart as an in-memory image
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return chart_url


@app.route('/dashboard')
def dashboard():
    log_file = "sentiment_logs.csv"
    if not os.path.exists(log_file):
        return "No data available yet."

    data = pd.read_csv(log_file)

    # Calculate insights
    total_texts = len(data)
    most_common_sentiment = data['Sentiment'].value_counts().idxmax()
    sentiment_counts = data['Sentiment'].value_counts().to_dict()

    # Generate the chart
    chart_url = generate_chart(data)

    return render_template(
        'dashboard.html',
        total_texts=total_texts,
        most_common_sentiment=most_common_sentiment,
        sentiment_counts=sentiment_counts,
        chart_url=chart_url
    )

if __name__ == "__main__":
    app.run(debug=True)
