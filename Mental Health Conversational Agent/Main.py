# Mental Health Conversational Agent — main.py

import random

class MentalHealthAgent:
    def __init__(self):
        self.mood = "neutral"

    def analyze_text(self, user_text):
        positive_words = ['happy', 'good', 'great', 'love']
        negative_words = ['sad', 'bad', 'stress', 'angry', 'depressed']
        score = 0
        for word in positive_words:
            if word in user_text.lower():
                score += 1
        for word in negative_words:
            if word in user_text.lower():
                score -= 1
        if score > 0:
            self.mood = 'positive'
        elif score < 0:
            self.mood = 'negative'
        else:
            self.mood = 'neutral'
        return self.mood

    def suggest_activity(self):
        activities = {
            'positive': [
                'Keep up the great mood! How about journaling your thoughts today?',
                'Try sharing your happiness with a friend.'
            ],
            'neutral': [
                'Consider a 5-minute mindfulness exercise to maintain calm.',
                'Take a short walk outside for fresh air and relaxation.'
            ],
            'negative': [
                'Try a breathing exercise to reduce stress.',
                'Consider writing down what’s bothering you in a journal.',
                'Try a guided meditation to improve your mood.'
            ]
        }
        return random.choice(activities[self.mood])

if __name__ == '__main__':
    agent = MentalHealthAgent()
    print("Welcome to your Mental Health Conversational Agent. Type your thoughts or 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Take care! Remember, I'm here if you need to talk.")
            break
        agent.analyze_text(user_input)
        suggestion = agent.suggest_activity()
        print(f"Agent: {suggestion}")

# Extension ideas:
# - Use NLP models for deep stress/mood analysis
# - Integrate CBT/mindfulness APIs and local events
# - Add persistent mood tracking and journaling
# - Multichannel interface: mobile app, chatbot, or voice
