from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import string
import base64
from io import BytesIO

class TextAnalyzer:
    stop_words = set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
        "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
        "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
        "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
        "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
        "at", "by", "for", "with", "about", "against", "between", "into", "through",
        "during", "before", "after", "above", "below", "to", "from", "up", "down",
        "in", "out", "on", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "any",
        "both", "each", "few", "more", "most", "other", "some", "such", "no",
        "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
        "can", "will", "just", "don", "should", "now"
    ])
    
    @staticmethod
    def get_most_frequent_words(data, sentiment):
        # Filter data by sentiment
        filtered = data[data['Sentiment'] == sentiment]['Input Text']
        all_words = " ".join(filtered).split()
        
        # Remove stop words and punctuation
        cleaned_words = [
            word.strip(string.punctuation).lower() 
            for word in all_words 
            if word.lower() not in TextAnalyzer.stop_words
        ]
        
        most_common = Counter(cleaned_words).most_common(10)
        return most_common

    @staticmethod
    def generate_wordcloud(data, sentiment):
        # Filter text by sentiment
        text = " ".join(data[data['Sentiment'] == sentiment]['Input Text'])
        
        # Remove stop words
        cleaned_text = " ".join(
            word for word in text.split() if word.lower() not in TextAnalyzer.stop_words
        )
        
        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(cleaned_text)
        
        # Save the word cloud to a BytesIO object
        img = BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        # Convert to Base64 for rendering in HTML
        return base64.b64encode(img.getvalue()).decode('utf8')
