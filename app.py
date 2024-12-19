import os
import pandas as pd
from text_analyzer import TextAnalyzer
from flask import Flask, request, render_template, Response, make_response
from transformers import pipeline
from logger import log_sentiment  # Import logging function

# Visualization imports
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.dates as mdates
import plotly.express as px

# Most common words
from collections import Counter
import string

# Word cloud
from wordcloud import WordCloud

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

# Visualization code
def generate_chart(data):
    # Ensure timestamps are in datetime format
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

    # Sentiment counts
    sentiment_counts = data['Sentiment'].value_counts()

    # Create charts
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

    # Bar Chart
    ax[0].bar(sentiment_counts.index, sentiment_counts.values, color=['red', 'green', 'gray'])
    ax[0].set_title("Sentiment Distribution")
    ax[0].set_ylabel("Count")

    # Pie Chart
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


def generate_interactive_line_chart(data):
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    grouped = data.groupby([data['Timestamp'].dt.date, 'Sentiment']).size().reset_index(name="Count")

    fig = px.line(grouped, x='Timestamp', y='Count', color='Sentiment',
                  title="Sentiment Trends Over Time",
                  labels={'Timestamp': 'Date', 'Count': 'Count'},
                  template="plotly_white")
    fig.update_xaxes(title="Date", tickangle=45)
    fig.update_yaxes(title="Count")
    return fig.to_html(full_html=False)


def get_average_confidence(data):
    return data.groupby('Sentiment')['Confidence'].mean().to_dict()


def generate_wordcloud(data, sentiment):
    # Filter text by sentiment
    text = " ".join(data[data['Sentiment'] == sentiment]['Input Text'])
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    # Save the word cloud to a BytesIO object
    img = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    # Convert to Base64 for rendering in HTML
    return base64.b64encode(img.getvalue()).decode('utf8')


@app.route('/dashboard')
def dashboard():
    log_file = "sentiment_logs.csv"
    if not os.path.exists(log_file):
        return "No data available yet."

    data = pd.read_csv(log_file)

    # Apply filters if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date:
        data = data[data['Timestamp'] >= start_date]
    if end_date:
        data = data[data['Timestamp'] <= end_date]

    # Calculate insights
    total_texts = len(data)
    most_common_sentiment = data['Sentiment'].value_counts().idxmax() if not data.empty else "None"
    sentiment_counts = data['Sentiment'].value_counts().to_dict()

    # Generate charts
    chart_url = generate_chart(data)

    interactive_chart = generate_interactive_line_chart(data)

    # Generate most frequent words
    positive_words = TextAnalyzer.get_most_frequent_words(data, 'POSITIVE')
    negative_words = TextAnalyzer.get_most_frequent_words(data, 'NEGATIVE')
    neutral_words = TextAnalyzer.get_most_frequent_words(data, 'NEUTRAL')

    # Generate word clouds
    positive_wordcloud = TextAnalyzer.generate_wordcloud(data, "POSITIVE")
    negative_wordcloud = TextAnalyzer.generate_wordcloud(data, "NEGATIVE")
    neutral_wordcloud = TextAnalyzer.generate_wordcloud(data, "NEUTRAL")    

    avg_confidence = get_average_confidence(data)

    return render_template(
        'dashboard.html',
        total_texts=total_texts,
        most_common_sentiment=most_common_sentiment,
        sentiment_counts=sentiment_counts,
        chart_url=chart_url,
        interactive_chart=interactive_chart,
        positive_words=positive_words,
        negative_words=negative_words,
        neutral_words=neutral_words,
        positive_wordcloud=positive_wordcloud,
        negative_wordcloud=negative_wordcloud,
        neutral_wordcloud=neutral_wordcloud,        
        avg_confidence=avg_confidence,        
    )


@app.route('/export', methods=['GET'])
def export_csv():
    log_file = "sentiment_logs.csv"
    if not os.path.exists(log_file):
        return "No data available to export."

    # Read the data from the CSV file
    data = pd.read_csv(log_file)

    # Apply filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sentiment = request.args.get('sentiment')

    if start_date and start_date != "None":
        data = data[data['Timestamp'] >= start_date]
    if end_date and end_date != "None":
        data = data[data['Timestamp'] <= end_date]
    if sentiment and sentiment != "None":
        data = data[data['Sentiment'].str.upper() == sentiment.upper()]

    # Debug: Print filtered data
    print("Filtered Data:\n", data)

    # Check if the data is empty
    if data.empty:
        return "No data matches the filters."

    # Convert the filtered data to CSV format
    csv_data = data.to_csv(index=False)

    # Return the CSV as a download
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=filtered_sentiments.csv"}
    )

@app.route("/download_wordcloud")
def download_wordcloud():
    sentiment = request.args.get("sentiment")
    # Load the dataset (adjust path if necessary)
    data = pd.read_csv("sentiment_logs.csv")
    wordcloud_img = TextAnalyzer.generate_wordcloud(data, sentiment)
    img_bytes = base64.b64decode(wordcloud_img)
    response = make_response(img_bytes)
    response.headers.set("Content-Type", "image/png")
    response.headers.set("Content-Disposition", f"attachment; filename={sentiment}_wordcloud.png")
    return response


if __name__ == "__main__":
    app.run(debug=True)
