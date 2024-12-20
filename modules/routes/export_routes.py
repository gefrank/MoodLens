from flask import Blueprint, request, Response, make_response
import os
import pandas as pd
from modules.utilities.text_analyzer import TextAnalyzer
import base64

export_routes = Blueprint('export', __name__)

@export_routes.route("/", methods=["GET"])
def export_csv():
    log_file = "logs/sentiment_logs.csv"
    if not os.path.exists(log_file):
        return "No data available to export."

    # Load data
    data = pd.read_csv(log_file)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # Apply filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sentiment = request.args.get('sentiment')

    if start_date:
        data = data[data['Timestamp'] >= start_date]
    if end_date:
        data = data[data['Timestamp'] <= end_date]
    if sentiment:
        data = data[data['Sentiment'].str.upper() == sentiment.upper()]

    if data.empty:
        return "No data matches the filters."

    # Convert to CSV
    csv_data = data.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=filtered_sentiments.csv"}
    )


@export_routes.route("/download_wordcloud", methods=["GET"])
def download_wordcloud():
    sentiment = request.args.get("sentiment")
    if not sentiment:
        return "Sentiment parameter is required.", 400

    # Load the dataset (ensure path is correct)
    log_file = "logs/sentiment_logs.csv"
    if not os.path.exists(log_file):
        return "No data available to generate the WordCloud."

    data = pd.read_csv(log_file)

    # Generate the WordCloud image
    wordcloud_img = TextAnalyzer.generate_wordcloud(data, sentiment)

    # Decode the Base64 image
    img_bytes = base64.b64decode(wordcloud_img)

    # Create a downloadable response
    response = make_response(img_bytes)
    response.headers.set("Content-Type", "image/png")
    response.headers.set("Content-Disposition", f"attachment; filename={sentiment}_wordcloud.png")
    return response
