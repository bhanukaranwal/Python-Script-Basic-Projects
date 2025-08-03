import random

def mystery_escape():
    print("Guess the secret code (1-50) to escape the room!")
    code = random.randint(1, 50)
    tries = 5
    while tries > 0:
        guess = int(input("Enter your guess: "))
        if guess == code:
            print("You escaped! 🎉")
            return
        elif guess < code:
            print("Too low!")
        else:
            print("Too high!")
        tries -= 1
    print(f"Out of tries! The code was {code}.")

if __name__ == "__main__":
    mystery_escape()
