# AI-Powered Personal Diary with Mood Analysis — main.py

import os
import datetime
import json
from textblob import TextBlob
import matplotlib.pyplot as plt

class DiaryEntry:
    def __init__(self, text, date=None):
        self.text = text
        self.date = date or datetime.datetime.now()
        self.mood = self.analyze_mood()

    def analyze_mood(self):
        # Use TextBlob's sentiment polarity to classify mood
        polarity = TextBlob(self.text).sentiment.polarity
        if polarity > 0.2:
            return 'Positive'
        elif polarity < -0.2:
            return 'Negative'
        else:
            return 'Neutral'

class PersonalDiary:
    def __init__(self, storage_file='diary_entries.json'):
        self.storage_file = storage_file
        self.entries = []
        self.load_entries()

    def load_entries(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        entry = DiaryEntry(item['text'], datetime.datetime.fromisoformat(item['date']))
                        self.entries.append(entry)
            except Exception as e:
                print(f"Error loading diary entries: {e}")

    def save_entries(self):
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump([{'text': e.text, 'date': e.date.isoformat()} for e in self.entries], f, indent=2)
        except Exception as e:
            print(f"Error saving diary entries: {e}")

    def add_entry(self, text):
        entry = DiaryEntry(text)
        self.entries.append(entry)
        self.save_entries()
        print(f"Entry added with mood: {entry.mood}")

    def show_mood_timeline(self):
        if not self.entries:
            print("No diary entries to display.")
            return

        # Sort entries by date
        self.entries.sort(key=lambda x: x.date)
        dates = [e.date for e in self.entries]
        mood_scores = []
        for e in self.entries:
            if e.mood == 'Positive':
                mood_scores.append(1)
            elif e.mood == 'Negative':
                mood_scores.append(-1)
            else:
                mood_scores.append(0)

        plt.figure(figsize=(10, 5))
        plt.plot(dates, mood_scores, marker='o')
        plt.ylim(-1.5, 1.5)
        plt.yticks([-1, 0, 1], ['Negative', 'Neutral', 'Positive'])
        plt.xlabel('Date')
        plt.ylabel('Mood')
        plt.title('Mood Timeline')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    diary = PersonalDiary()
    print("Welcome to your Personal AI-Powered Diary.")
    print("Options: [1] Add entry, [2] Show mood timeline, [3] Exit")
    
    while True:
        choice = input("Select an option: ").strip()
        if choice == '1':
            print("Enter your diary entry (type 'END' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            entry_text = '\n'.join(lines).strip()
            if entry_text:
                diary.add_entry(entry_text)
            else:
                print("Empty entry discarded.")
        elif choice == '2':
            diary.show_mood_timeline()
        elif choice == '3':
            print("Goodbye! Your diary is safely saved.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == '__main__':
    main()

# Requirements:
# pip install textblob matplotlib
# python -m textblob.download_corpora
