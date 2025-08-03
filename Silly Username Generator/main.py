import random

def username_generator():
    adjectives = ["Silly", "Quick", "Mighty", "Happy", "Sneaky", "Brave"]
    animals = ["Lion", "Penguin", "Turtle", "Fox", "Kitten", "Bear"]
    numbers = random.randint(1, 99)
    print("Need a cool username?")
    input("Press Enter to generate one: ")
    print(f"Your new username: {random.choice(adjectives)}{random.choice(animals)}{numbers}")

if __name__ == "__main__":
    username_generator()
