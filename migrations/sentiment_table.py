import sqlite3
import pandas as pd

# Define the file path for the CSV and SQLite database
csv_file_path = r'C:\Users\gefra\Repos\MoodLens\logs\sentiment_logs.csv'
db_file_path = r'C:\Users\gefra\Repos\MoodLens\instance\moodlens.db'

# Load the CSV into a Pandas DataFrame
sentiment_logs = pd.read_csv(csv_file_path)

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Drop the table if it exists to ensure the correct schema
cursor.execute("DROP TABLE IF EXISTS sentiment_logs")

# Create the sentiment_logs table
create_table_query = """
CREATE TABLE IF NOT EXISTS sentiment_logs (
    Timestamp TEXT NOT NULL,
    Input_Text TEXT NOT NULL,
    Sentiment TEXT NOT NULL,
    Confidence REAL NOT NULL
);
"""
cursor.execute(create_table_query)

# Insert data from DataFrame into the database
insert_query = """
INSERT INTO sentiment_logs (Timestamp, Input_Text, Sentiment, Confidence)
VALUES (?, ?, ?, ?);
"""

# Iterate through the DataFrame and insert rows into the table
for _, row in sentiment_logs.iterrows():
    cursor.execute(insert_query, (row['Timestamp'], row['Input Text'], row['Sentiment'], row['Confidence']))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully inserted into the sentiment_logs table.")
