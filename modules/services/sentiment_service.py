import os
from openai import OpenAI
from transformers import pipeline
from modules.models import AppConfig

# Suppress symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Initialize DistilBERT sentiment analysis pipeline
distilbert_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

def openai_api_call(text):
    """
    Calls the OpenAI Chat API for sentiment analysis.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-secret-key-placeholder"))
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis assistant. Respond ONLY with a JSON-like format: 'Sentiment: [LABEL], Confidence: [SCORE]' where label is Positive/Negative/Neutral and score is 0-1."},
                {"role": "user", "content": f"Analyze: '{text}'"}
            ]
        )
        
        reply = response.choices[0].message.content.strip()
        
        if "Sentiment:" in reply and "Confidence:" in reply:
            parts = reply.split(",")
            label = parts[0].split("Sentiment:")[1].strip()
            # Clean the confidence string of any non-numeric characters except decimal point
            confidence_str = ''.join(c for c in parts[1].split("Confidence:")[1].strip() if c.isdigit() or c == '.')
            confidence = float(confidence_str)
            return label, confidence
        else:
            return "Neutral", 0.5
            
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Error", 0.0


def analyze_sentiment(text, use_openai=False):
    # Check the AppConfig table for the toggle setting
    config = AppConfig.query.filter_by(key="ai_model").first()
    if (config and config.value == "openai") or use_openai:
        # Call OpenAI API
        return openai_api_call(text)
    else:
        # Use DistilBERT
        result = distilbert_pipeline(text)
        return result[0]['label'], result[0]['score']


if __name__ == "__main__":
    user_input = input("Enter a sentence: ")
    label, score = analyze_sentiment(user_input)
    print(f"Sentiment: {label} (Confidence: {score:.2f})")