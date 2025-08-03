import random

def coin_toss():
    while True:
        call = input("Heads or Tails? (type exit to quit): ").strip().lower()
        if call == "exit":
            break
        toss = random.choice(["heads", "tails"])
        print(f"It’s {toss}!")
        print("You win!" if call == toss else "Try again!")

if __name__ == "__main__":
    coin_toss()
