from flask import Blueprint, request, render_template
from modules.utilities.logger import log_sentiment  # Import from logger.py
from modules.services.sentiment_service import analyze_sentiment
from modules.models import AppConfig

main_routes = Blueprint('main', __name__)

@main_routes.route("/", methods=["GET", "POST"])
def index():
    result = ""
    current_model = "Unknown"
    # Fetch the current AI model from AppConfig
    config = AppConfig.query.filter_by(key="ai_model").first()
    if config:
        current_model = "OpenAI" if config.value == "openai" else "DistilBERT"

    if request.method == "POST":
        text = request.form["text"].strip()
        if not text:
            result = "Please enter some text to analyze."
        else:
            # Perform sentiment analysis
            label, score = analyze_sentiment(text)
            result = f"Sentiment: {label} (Confidence: {score:.2f})"
            
            # Log the sentiment analysis result
            log_sentiment(Input_Text=text, Sentiment=label, Confidence=score, current_model=current_model)
    return render_template("index.html", result=result, current_model=current_model)
