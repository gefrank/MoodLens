import pandas as pd
import random
from datetime import datetime, timedelta

# Generate realistic sentiment log data for a customer application
def generate_realistic_sentiment_logs(num_records=1000):
    sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    positive_texts = [
        "The product exceeded my expectations!", "Amazing experience, I loved every bit of it.",
        "Customer service was fantastic, very helpful.", "I will definitely recommend this to others.",
        "This is the best purchase I've made this year.", "Superb quality and value for money.",
        "I'm so happy with this!", "Five stars for the excellent support team!",
        "Brilliant service, keep up the good work!", "Top-notch, I'm very satisfied."
    ]
    negative_texts = [
        "This product did not meet my expectations.", "Terrible experience, I want a refund.",
        "Customer service was unhelpful and rude.", "I will never buy from this company again.",
        "This is the worst purchase I've made this year.", "Poor quality, not worth the money.",
        "I'm very disappointed with this.", "One star for the terrible support team.",
        "Horrible service, needs improvement.", "Unacceptable experience overall."
    ]
    neutral_texts = [
        "The product was okay, nothing extraordinary.", "Average experience, not bad but not great.",
        "Customer service was decent, could be better.", "I might consider buying again, not sure.",
        "This purchase was neither good nor bad.", "It's fine, does the job.",
        "Nothing special about this product.", "Neutral experience, met basic expectations.",
        "The service was acceptable, nothing more.", "An average product, nothing to rave about."
    ]

    data = []
    start_date = datetime(2024, 1, 1)
    for i in range(num_records):
        sentiment = random.choice(sentiments)
        if sentiment == "POSITIVE":
            text = random.choice(positive_texts)
            confidence = round(random.uniform(0.85, 0.99), 2)
        elif sentiment == "NEGATIVE":
            text = random.choice(negative_texts)
            confidence = round(random.uniform(0.65, 0.85), 2)
        else:  # NEUTRAL
            text = random.choice(neutral_texts)
            confidence = round(random.uniform(0.75, 0.90), 2)
        
        timestamp = start_date + timedelta(days=random.randint(0, 364), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        data.append({
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Input Text": text,
            "Sentiment": sentiment,
            "Confidence": confidence
        })
    return pd.DataFrame(data)

# Generate the data
realistic_data = generate_realistic_sentiment_logs()

# Save to CSV
file_path = "realistic_sentiment_logs_2024.csv"
realistic_data.to_csv(file_path, index=False)
print(f"Mock data saved to {file_path}")
