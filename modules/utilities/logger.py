from datetime import datetime
from modules.models import SentimentLog
from modules.utilities.database import db

def log_sentiment(Input_Text, Sentiment, Confidence):
    """
    Logs sentiment analysis results to the database using SQLAlchemy.

    Args:
        Input_Text (str): The input text analyzed.
        Sentiment (str): The sentiment label (e.g., Positive, Negative, Neutral).
        Confidence (float): The confidence score of the analysis.
    """
    # Create a new sentiment log entry
    log = SentimentLog(
        Input_Text=Input_Text,
        Sentiment=Sentiment,
        Confidence=Confidence,
        Timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    )
    db.session.add(log)
    db.session.commit()

# Example usage (Run this inside the app context)
if __name__ == "__main__":
    from app import app

    with app.app_context():
        log_sentiment("This is a test", "POSITIVE", 0.95)
        print("Sentiment log added!")
