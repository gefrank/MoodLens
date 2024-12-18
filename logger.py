# logger.py
import csv
import os
from datetime import datetime

LOG_FILE = "sentiment_logs.csv"

def log_sentiment(text, label, score):
    """Logs sentiment analysis results to a CSV file."""
    # Check if log file exists; if not, create it with headers
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Input Text", "Sentiment", "Confidence Score"])

    # Append new data to the log file
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), text, label, f"{score:.2f}"])
