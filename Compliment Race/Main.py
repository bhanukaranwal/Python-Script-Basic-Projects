import random
import time

def compliment_race():
    compliments = [
        "You have splendid coding style!",
        "Your laugh is contagious!",
        "Your socks probably match today!",
        "You could be a professional silly game designer.",
        "Your brain is 100% functional!"
    ]
    print("Welcome to the Compliment Race! Try to type the compliment as fast as you can!")
    compliment = random.choice(compliments)
    input("Ready? Press Enter for your compliment...")
    print(f"TYPE THIS: {compliment}")
    start = time.time()
    user = input()
    elapsed = time.time() - start
    if user.strip() == compliment:
        print(f"Speedy! You typed it in {elapsed:.2f} seconds.")
    else:
        print("Oops! Practice makes perfect in the Compliment Race.")

if __name__ == "__main__":
    compliment_race()
