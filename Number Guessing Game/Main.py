import random

def number_guessing_game():
    number = random.randint(1, 100)
    attempts = 0
    print("Welcome to Number Guessing Game! Guess a number between 1 and 100.")
    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            if guess < number:
                print("Too low!")
            elif guess > number:
                print("Too high!")
            else:
                print(f"Congratulations! You found the number in {attempts} attempts.")
                break
        except ValueError:
            print("Enter a valid integer.")

if __name__ == "__main__":
    number_guessing_game()
