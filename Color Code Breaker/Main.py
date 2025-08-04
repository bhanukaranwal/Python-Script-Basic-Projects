import random

def color_code_breaker():
    COLORS = ["red", "blue", "green", "yellow", "orange", "purple"]
    code = [random.choice(COLORS) for _ in range(4)]
    print("Welcome to Color Code Breaker!")
    print(f"Available colors: {', '.join(COLORS)}")
    attempts = 0
    while True:
        guess = input("Enter your guess (4 colors split by spaces): ").lower().strip().split()
        if len(guess) != 4 or any(c not in COLORS for c in guess):
            print("Invalid input. Please enter exactly 4 valid colors.")
            continue
        attempts += 1
        correct = sum(a == b for a, b in zip(guess, code))
        in_code = sum(min(guess.count(col), code.count(col)) for col in COLORS) - correct
        print(f"Correct positions: {correct}, correct colors in wrong positions: {in_code}")
        if correct == 4:
            print(f"Congratulations! You broke the code in {attempts} tries!")
            break

if __name__ == "__main__":
    color_code_breaker()
