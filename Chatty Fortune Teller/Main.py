import random

def fortune_teller():
    fortunes = [
        "You will have a surprising encounter today!",
        "Happiness is around the corner.",
        "Now is a good time to try something new.",
        "Be cautious with your decisions.",
        "Luck will follow your hard work."
    ]
    print("Welcome to the Fortune Teller!")
    name = input("What is your name? ")
    input(f"Hi {name}! Ask me a question about your future and press Enter: ")
    print("🔮", random.choice(fortunes))

if __name__ == "__main__":
    fortune_teller()
