import sqlite3
import os
from datetime import datetime

db_file_path = "instance/moodlens.db"

def initialize_database():
    """Ensures the database and sentiment_logs table are initialized."""
    if not os.path.exists(db_file_path):
        os.makedirs(os.path.dirname(db_file_path), exist_ok=True)

    # Connect to the database and create the table if it doesn't exist
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS sentiment_logs (
        Timestamp TEXT NOT NULL,
        Input_Text TEXT NOT NULL,
        Sentiment TEXT NOT NULL,
        Confidence REAL NOT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

def log_sentiment(text, label, score):
    """Logs sentiment analysis results to the database."""
    # Initialize the database if necessary
    initialize_database()

    # Connect to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Insert the new sentiment log
    insert_query = """
    INSERT INTO sentiment_logs (Timestamp, Input_Text, Sentiment, Confidence)
    VALUES (?, ?, ?, ?);
    """
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(insert_query, (formatted_time, text, label, score))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    log_sentiment("This is a test", "POSITIVE", 0.95)
