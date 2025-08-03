import time
import random

def memory_challenge():
    numbers = [random.randint(10, 99) for _ in range(5)]
    print("Remember these numbers:")
    print(*numbers)
    time.sleep(3)
    print("\033c", end="")  # Clears the screen on some consoles
    guess = input("Enter the numbers you remember, separated by spaces: ")
    guess_list = list(map(int, guess.strip().split()))
    correct = sum([1 for a, b in zip(numbers, guess_list) if a == b])
    print(f"You remembered {correct}/5 numbers!")

if __name__ == "__main__":
    memory_challenge()
