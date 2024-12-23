from flask import Blueprint, request, Response, make_response
import os
import sqlite3
from modules.utilities.text_analyzer import TextAnalyzer
import base64

export_routes = Blueprint('export', __name__)

@export_routes.route("/", methods=["GET"])
def export_csv():
    db_file_path = "instance/moodlens.db"

    if not os.path.exists(db_file_path):
        return "No data available to export."

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Base query
    query = "SELECT Timestamp, Input_Text, Sentiment, Confidence FROM sentiment_logs"
    conditions = []
    params = []

    # Apply filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sentiment = request.args.get('sentiment')

    if start_date:
        conditions.append("Timestamp >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("Timestamp <= ?")
        params.append(end_date)
    if sentiment:
        conditions.append("UPPER(Sentiment) = ?")
        params.append(sentiment.upper())

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Execute the query
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No data matches the filters."

    # Convert rows to CSV format
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Timestamp", "Input_Text", "Sentiment", "Confidence"])

    # Write rows
    writer.writerows(rows)

    csv_data = output.getvalue()
    output.close()

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

    db_file_path = "instance/moodlens.db"

    if not os.path.exists(db_file_path):
        return "No data available to generate the WordCloud."

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Fetch data for the specified sentiment
    query = "SELECT Input_Text FROM sentiment_logs WHERE UPPER(Sentiment) = ?"
    cursor.execute(query, (sentiment.upper(),))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No data available for the specified sentiment."

    # Extract input text
    text_data = [row[0] for row in rows]

    # Generate the WordCloud image
    wordcloud_img = TextAnalyzer.generate_wordcloud(text_data, sentiment)

    # Decode the Base64 image
    img_bytes = base64.b64decode(wordcloud_img)

    # Create a downloadable response
    response = make_response(img_bytes)
    response.headers.set("Content-Type", "image/png")
    response.headers.set("Content-Disposition", f"attachment; filename={sentiment}_wordcloud.png")
    return response
