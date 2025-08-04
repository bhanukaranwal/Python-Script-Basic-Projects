import random

def silly_dance_off():
    moves = ['moonwalk', 'robot', 'floss', 'dab', 'twist', 'shuffle']
    print("Welcome to the Silly Dance-Off!")
    print("Choose your ultimate dance move!")
    player = input(f"Your move {moves}: ").strip().lower()
    computer = random.choice(moves)
    print(f"You bust out the {player}!")
    print(f"Computer busts out the {computer}!")
    if player == computer:
        print("It's a tie! You both groove the same move!")
    else:
        result = random.choice(["You win the dance battle! 🕺", "Computer wins the dance battle! 🤖"])
        print(result)

if __name__ == "__main__":
    silly_dance_off()
