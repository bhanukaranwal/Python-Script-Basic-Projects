import random
import time

def potato_hot_seat():
    print("Welcome to Potato Hot Seat!")
    input("Press Enter to start passing the virtual potato...")
    turns = random.randint(3, 8)
    for i in range(turns):
        input(f"Pass {i+1}! Press Enter quickly...")
    print("Boom! The potato exploded! 🍠💥\nHaha, hope you were fast enough.")

if __name__ == "__main__":
    potato_hot_seat()
