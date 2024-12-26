from app import app  # Import the Flask app from your main app file
from modules.services.sentiment_service import analyze_sentiment

if __name__ == "__main__":
    with app.app_context():
        while True:
            print("\nSelect sentiment analysis method:")
            print("1. DistilBERT")
            print("2. OpenAI API")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "0":
                print("Exiting...")
                break

            if choice not in {"1", "2"}:
                print("Invalid choice. Please enter 1, 2, or 0.")
                continue

            use_openai = choice == "2"
            
            print(f"Using {'OpenAI API' if use_openai else 'DistilBERT'} for sentiment analysis.")
            
            user_input = input("Enter a sentence (or type 'exit' to quit): ").strip()
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            if not user_input:
                print("Input cannot be empty. Please try again.")
                continue

            label, score = analyze_sentiment(user_input, use_openai=use_openai)
            print(f"Sentiment: {label} (Confidence: {score:.2f})")
