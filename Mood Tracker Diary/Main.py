import datetime
import random

def mood_tracker():
    print("Welcome to your Mood Tracker Diary!")
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    print(f"Today is {today}. How are you feeling? (e.g., happy, sad, excited, tired)")
    mood = input("Your mood: ").strip()
    compliments = [
        "Remember, you're awesome!",
        "Whatever you feel is valid. Take care of yourself!",
        "Keep your head up and smile, even on tough days.",
        "You can handle anything today brings."
    ]
    print(f"Logged mood: {mood}")
    print(random.choice(compliments))
    print("See you tomorrow for another mood check-in!")

if __name__ == "__main__":
    mood_tracker()
