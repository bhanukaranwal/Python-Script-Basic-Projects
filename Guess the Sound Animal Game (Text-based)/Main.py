def guess_the_animal():
    sounds = {
        "meow": "cat",
        "woof": "dog",
        "quack": "duck",
        "moo": "cow",
        "neigh": "horse"
    }
    import random
    sound, animal = random.choice(list(sounds.items()))
    print(f"Which animal makes this sound: '{sound}'?")
    guess = input("Your answer: ").lower()
    if guess == animal:
        print("Correct! 🐾")
    else:
        print(f"Oops, it's a {animal}!")

if __name__ == "__main__":
    guess_the_animal()
