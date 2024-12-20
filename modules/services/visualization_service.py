import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.express as px
import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend


def generate_chart(data):
    """
    Generates a bar chart and a pie chart for sentiment distribution.
    
    Args:
        data (pd.DataFrame): The dataset containing sentiment data.
    
    Returns:
        str: Base64 encoded string of the combined chart image.
    """
    # Ensure timestamps are in datetime format
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

    # Sentiment counts
    sentiment_counts = data['Sentiment'].value_counts()

    # Create charts
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

    # Bar Chart
    ax[0].bar(sentiment_counts.index, sentiment_counts.values, color=['red', 'green', 'gray'])
    ax[0].set_title("Sentiment Distribution")
    ax[0].set_ylabel("Count")

    # Pie Chart
    ax[1].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['red', 'green', 'gray'])
    ax[1].set_title("Sentiment Proportions")

    # Save the chart as an in-memory image
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return chart_url


def generate_interactive_line_chart(data):
    """
    Generates an interactive line chart of sentiment trends over time.
    
    Args:
        data (pd.DataFrame): The dataset containing sentiment data.
    
    Returns:
        str: HTML representation of the interactive Plotly chart.
    """
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    grouped = data.groupby([data['Timestamp'].dt.date, 'Sentiment']).size().reset_index(name="Count")

    fig = px.line(grouped, x='Timestamp', y='Count', color='Sentiment',
                  title="Sentiment Trends Over Time",
                  labels={'Timestamp': 'Date', 'Count': 'Count'},
                  template="plotly_white")
    fig.update_xaxes(title="Date", tickangle=45)
    fig.update_yaxes(title="Count")
    return fig.to_html(full_html=False)


def get_average_confidence(data):
    """
    Calculates the average confidence score for each sentiment.
    
    Args:
        data (pd.DataFrame): The dataset containing sentiment data.
    
    Returns:
        dict: A dictionary mapping sentiment labels to their average confidence scores.
    """
    if 'Confidence' not in data.columns or data.empty:
        return {}
    return data.groupby('Sentiment')['Confidence'].mean().to_dict()
