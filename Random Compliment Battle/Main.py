import random

def compliment_battle():
    compliments = [
        "You have the best ideas!",
        "Your positivity is infectious!",
        "You're a true problem-solver!",
        "Your kindness inspires others."
    ]
    print("Player 1:", random.choice(compliments))
    print("Player 2:", random.choice(compliments))
    print("Which compliment wins? Decide together! 🚀")

if __name__ == "__main__":
    compliment_battle()
