import random

def compliment():
    compliments = [
        "You have a great sense of humor!",
        "You’re an awesome coder!",
        "Your energy is contagious!",
        "You light up the room!"
    ]
    print("Need a compliment? (Press Enter)")
    input()
    print(random.choice(compliments))

if __name__ == "__main__":
    compliment()
