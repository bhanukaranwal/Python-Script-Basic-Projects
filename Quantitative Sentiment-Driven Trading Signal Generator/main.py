import requests
import time
from textblob import TextBlob
import matplotlib.pyplot as plt
import random

# Replace with your free NewsAPI key if available
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
NEWS_API_URL = (
    "https://newsapi.org/v2/top-headlines?language=en&category=business&pageSize=5&apiKey=" + NEWS_API_KEY
)

# Simulate asset price (for demo, since no real trading/execution)
def simulate_price_series(n=100, start=100):
    series = [start]
    for _ in range(n-1):
        change = random.gauss(0, 0.5)
        series.append(round(series[-1] + change, 2))
    return series

def get_headlines():
    try:
        res = requests.get(NEWS_API_URL)
        data = res.json()
        headlines = [a['title'] for a in data.get('articles', [])]
        if not headlines:
            # fallback sample
            headlines = [
                "Stocks rise amid economic optimism",
                "Fed signals rate hike pause",
                "Oil prices tumble after surprise release",
                "Tech sector sees major layoffs",
                "Retail sales growth surges in June"
            ]
        return headlines
    except Exception as e:
        print(f"Error fetching headlines: {e}")
        return [
            "Stocks rise amid economic optimism",
            "Fed signals rate hike pause",
            "Oil prices tumble after surprise release",
            "Tech sector sees major layoffs",
            "Retail sales growth surges in June"
        ]

def analyze_sentiment(headlines):
    sentiments = []
    for text in headlines:
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        sentiments.append(score)
    avg = sum(sentiments) / len(sentiments)
    return avg

def get_signal(sentiment, buy_thresh=0.10, sell_thresh=-0.10):
    if sentiment > buy_thresh:
        return 'BUY'
    elif sentiment < sell_thresh:
        return 'SELL'
    else:
        return 'HOLD'

def simulate_trading(price_series, signals):
    position = 0
    cash = 10000
    holdings = 0
    pl_history = []

    for i, signal in enumerate(signals):
        price = price_series[i]
        if signal == 'BUY' and position == 0:
            holdings = cash // price
            cash -= holdings * price
            position = 1
        elif signal == 'SELL' and position == 1:
            cash += holdings * price
            holdings = 0
            position = 0
        # track marked-to-market value
        total_value = cash + holdings * price
        pl_history.append(total_value)
    return pl_history

def main():
    time_steps = 50
    headline_history = []
    sentiment_history = []
    signal_history = []

    price_series = simulate_price_series(time_steps)

    for t in range(time_steps):
        headlines = get_headlines()
        sentiment = analyze_sentiment(headlines)
        signal = get_signal(sentiment)
        headline_history.append(headlines)
        sentiment_history.append(sentiment)
        signal_history.append(signal)
        print(f"Timestep {t+1}: Sentiment {sentiment:.2f} | Signal: {signal}")
        time.sleep(0.01)  # API throttle, make longer if hitting rate limits

    pl_history = simulate_trading(price_series, signal_history)

    # Plot Sentiment and P/L over time
    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    plt.plot(sentiment_history, marker="o")
    plt.axhline(0, color='grey', linestyle='--', label="Neutral")
    plt.title("Headline Sentiment Over Time")
    plt.ylabel("Sentiment Polarity")
    plt.legend(['Sentiment', 'Neutral'])
    plt.subplot(2,1,2)
    plt.plot(pl_history, color='g')
    plt.title("Portfolio Value ($) Over Time")
    plt.ylabel("Portfolio Value")
    plt.xlabel("Time Step")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
