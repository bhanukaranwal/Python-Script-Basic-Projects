import random

def time_travel_guess():
    print("\nWelcome to Time Travel Guess! Guess the year with just a hint.")
    year = random.randint(1500, 2025)
    attempts = 0
    while True:
        guess = input("Guess the year (type 'quit' to exit): ")
        if guess.lower() == 'quit':
            print(f"Time travel mission aborted. The year was {year}.")
            break
        if not guess.isdigit():
            print("Please enter a valid year.")
            continue
        guess = int(guess)
        attempts += 1
        if guess == year:
            print(f"Correct! You found the year in {attempts} guesses.")
            break
        elif guess < year:
            print("Too early! Try a later year.")
        else:
            print("Too late! Try an earlier year.")

if __name__ == "__main__":
    time_travel_guess()
