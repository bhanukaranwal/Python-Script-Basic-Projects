import random

def capital_quiz():
    capitals = {
        "France": "Paris",
        "Japan": "Tokyo",
        "Brazil": "Brasilia",
        "India": "New Delhi",
        "Australia": "Canberra"
    }
    country, capital = random.choice(list(capitals.items()))
    print(f"What is the capital city of {country}?")
    guess = input("Your answer: ").strip().title()
    if guess == capital:
        print("Correct! 🏆")
    else:
        print(f"Oops! The capital of {country} is {capital}.")

if __name__ == "__main__":
    capital_quiz()
