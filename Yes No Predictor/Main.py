import random

def yes_no_predictor():
    print("Ask any YES/NO question to the predictor!")
    input("Your question: ")
    print(random.choice(["Yes", "No", "Maybe", "Absolutely!", "Not at all!", "Ask again later!"]))

if __name__ == "__main__":
    yes_no_predictor()
