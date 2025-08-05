# Global Macro News Event Analyzer

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download NLTK data required for sentiment analysis
nltk.download('vader_lexicon')

# Function to scrape financial news headlines from CNBC
def fetch_news_headlines(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        # CNBC has headlines in 'LatestNews-headlineCard' which may change over time
        headlines = [item.get_text() for item in soup.find_all('a', class_='LatestNews-headlineCard')]
        return headlines
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# Function to analyze sentiment of news headlines using VADER
sia = SentimentIntensityAnalyzer()
def analyze_sentiment(headlines):
    sentiment_scores = []
    for hl in headlines:
        score = sia.polarity_scores(hl)
        sentiment_scores.append({'headline': hl, 'sentiment': score})
    return sentiment_scores

# Basic macro event detection with keyword matching
def detect_macro_events(headlines):
    events = []
    keywords = ['Fed', 'inflation', 'jobs', 'GDP', 'unemployment', 'rate']
    for hl in headlines:
        for kw in keywords:
            if kw.lower() in hl.lower():
                events.append({'headline': hl, 'event': kw})
    return events

if __name__ == '__main__':
    news_url = 'https://www.cnbc.com/finance/'
    print('Fetching news...')
    headlines = fetch_news_headlines(news_url)
    print(f'Fetched {len(headlines)} headlines.')

    print('Analyzing sentiment...')
    sentiment_results = analyze_sentiment(headlines)

    print('Detecting macro events...')
    macro_events = detect_macro_events(headlines)

    # Output some results
    print('\nSample Sentiment Results:')
    for res in sentiment_results[:5]:
        print(f"{res['headline']}\nSentiment: {res['sentiment']}\n")

    print('Detected Macro Events:')
    for event in macro_events:
        print(f"Event: {event['event']} - Headline: {event['headline']}")

    print('Global Macro News Event Analyzer base run completed.')

    # Placeholder: You can extend here to fetch historical price data and analyze impact.

