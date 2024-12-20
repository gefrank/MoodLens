from flask import Blueprint, request, render_template
from modules.utilities.logger import log_sentiment
from modules.services.sentiment_service import analyze_sentiment

main_routes = Blueprint('main', __name__)

@main_routes.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        text = request.form["text"].strip()
        if not text:
            result = "Please enter some text to analyze."
        else:
            label, score = analyze_sentiment(text)
            result = f"Sentiment: {label} (Confidence: {score:.2f})"
            log_sentiment(text, label, score)
    return render_template("index.html", result=result)
