import random

def pet_name_suggester():
    pets = ["cat", "dog", "rabbit", "hamster", "parrot"]
    names = ["Whiskers", "Bolt", "Peanut", "Sunny", "Milo", "Pumpkin"]
    print("What pet do you have?")
    pet = input("Type one (cat/dog/rabbit/hamster/parrot): ").lower()
    if pet in pets:
        print(f"How about naming your {pet}: '{random.choice(names)}'? 🐾")
    else:
        print("Sorry, I don’t have names for that pet yet!")

if __name__ == '__main__':
    pet_name_suggester()
