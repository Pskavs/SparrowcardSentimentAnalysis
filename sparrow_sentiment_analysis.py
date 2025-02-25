from transformers import pipeline
from collections import Counter
import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

# Load reviews from CSV
review_df = pd.read_csv('ck_reviews/scraped_reviews.csv')
reviews = review_df.iloc[:, 0].apply(eval).explode().tolist()

def word_counts(reviews):
    """
    Creates a list of the most common words in the reviews, while removing normally used words such as 'and'.
    Saves results to 'word_counts.csv'.
    """
    stop_words = set(stopwords.words('english'))
    stop_words.update(['credit', 'card'])

    words = [
        word.lower() for review in reviews
        for word in re.findall(r'\b\w+\b', review)
        if word.lower() not in stop_words  # Remove stopwords
    ]

    # Get most common words
    word_counts = Counter(words)
    word_counts_df = pd.DataFrame(word_counts.most_common(20), columns=["Word", "Count"])

    # Save to CSV
    word_counts_df.to_csv("word_counts.csv", index=False)

    print("Top 20 Keywords (Filtered) saved to 'word_counts.csv'.")
    print(word_counts_df)

def sentiment_analysis(reviews):
    """
    Uses a Hugging Face transformer to run sentiment analysis on reviews.
    Saves the results to 'sentiment_analysis.csv' and plots sentiment distribution.
    """
    classifier = pipeline("sentiment-analysis", model="stevhliu/my_awesome_model")
    results = classifier(reviews, top_k=None)
    # Create DataFrame for sentiments
    df_sentiment = pd.DataFrame([
        {
            "Review": review,
            "Positive Score": sentiment_list[0]['score'],  # Index 0 is 'Positive'
            "Negative Score": sentiment_list[1]['score']   # Index 1 is 'Negative'
        }
        for review, sentiment_list in zip(reviews, results)
    ])

    # Save results to CSV
    df_sentiment.to_csv("sentiment_analysis.csv", index=False)
    print("Sentiment analysis results saved to 'sentiment_analysis.csv'.")

    # Sum up the total positive and negative scores
    total_positive = df_sentiment["Positive Score"].sum()
    total_negative = df_sentiment["Negative Score"].sum()
    print(round(((total_positive / (total_positive+total_negative)) * 100), 2),'% Positive')
    # Create a bar chart for the aggregated sentiment scores
    plt.figure(figsize=(6, 4))
    plt.bar(["Positive", "Negative"], [total_positive, total_negative], color=["green", "red"], alpha=0.75)
    plt.title("Overall Sentiment Analysis of Credit Karma Reviews")
    plt.ylabel("Total Sentiment Score")
    plt.show()

# Run both functions
sentiment_analysis(reviews)
word_counts(reviews)