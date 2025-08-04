import tweepy
from textblob import TextBlob

def twitter_sentiment_analyzer():
    # Fill in your details from https://developer.twitter.com/en/portal/dashboard
    BEARER_TOKEN = 'YOUR_BEARER_TOKEN_HERE'

    print("\nWelcome to Real-Time Twitter Sentiment Analyzer!")
    topic = input("Enter the topic/hashtag to analyze (e.g. Python, #AI): ")
    n_tweets = int(input("How many latest tweets to analyze? (e.g. 50): "))

    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    try:
        # Fetch live tweets for the topic (no retweets, English, most recent)
        response = client.search_recent_tweets(query=topic + " -is:retweet lang:en",
                                               tweet_fields=['text'],
                                               max_results=min(100, n_tweets))
        tweets = [tweet.text for tweet in response.data][:n_tweets]
    except Exception as e:
        print("Error fetching tweets:", e)
        return

    pos = neu = neg = 0
    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0:
            pos += 1
        elif polarity < 0:
            neg += 1
        else:
            neu += 1

    total = len(tweets)
    print(f"\nAnalyzed {total} tweets about '{topic}':")
    print(f"Positive : {pos} ({(pos/total)*100:.1f}%)")
    print(f"Neutral  : {neu} ({(neu/total)*100:.1f}%)")
    print(f"Negative : {neg} ({(neg/total)*100:.1f}%)")

    # Show samples
    if total > 0:
        print("\nSample Tweets and their Sentiment:")
        for i, tweet in enumerate(tweets[:5]):
            pol = TextBlob(tweet).sentiment.polarity
            sentiment = "Positive" if pol > 0 else ("Negative" if pol < 0 else "Neutral")
            print(f"{i+1}. {tweet} | Sentiment: {sentiment}")

if __name__ == '__main__':
    twitter_sentiment_analyzer()
