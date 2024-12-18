import os
from transformers import pipeline

# Suppress symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", revision="714eb0f")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    return result[0]['label'], result[0]['score']

if __name__ == "__main__":
    user_input = input("Enter a sentence: ")
    label, score = analyze_sentiment(user_input)
    print(f"Sentiment: {label} (Confidence: {score:.2f})")