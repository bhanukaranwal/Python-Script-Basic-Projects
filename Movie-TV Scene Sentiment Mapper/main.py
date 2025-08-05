# Movie/TV Scene Sentiment Mapper — main.py

import matplotlib.pyplot as plt
from textblob import TextBlob

class SentimentMapper:
    def __init__(self, subtitle_lines):
        self.subtitle_lines = subtitle_lines

    def analyze_sentiments(self):
        sentiments = []
        for line in self.subtitle_lines:
            blob = TextBlob(line)
            sentiments.append(blob.sentiment.polarity)
        return sentiments

    def plot_sentiment_timeline(self, sentiments):
        plt.figure(figsize=(12,6))
        plt.plot(sentiments, marker='o', label='Sentiment Polarity')
        plt.title('Scene Sentiment Timeline')
        plt.xlabel('Scene Number')
        plt.ylabel('Sentiment Polarity')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    # Sample subtitles/dialogue for demonstration purposes
    scenes = [
        "I'm so excited to see you!",
        "This is absolutely terrible...",
        "Why did you do that?",
        "I'm feeling great today.",
        "This is the worst day ever.",
        "I love you."
    ]

    mapper = SentimentMapper(scenes)
    sentiments = mapper.analyze_sentiments()
    print("Scene Sentiments:")
    for i, s in enumerate(sentiments, 1):
        print(f"Scene {i}: Sentiment = {s:.2f}")

    mapper.plot_sentiment_timeline(sentiments)

# Next steps:
# - Automatically parse .srt or scripts for scene/character separation
# - Tag sentiment by character, not just by scene/dialogue
# - Show character interaction sentiment dynamics
# - Extend to multi-emotion and intensity classification
# - Sync with video for dynamic playback or editing suggestions
