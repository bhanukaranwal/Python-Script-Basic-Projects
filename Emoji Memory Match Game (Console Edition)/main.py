import random
import time

def emoji_memory_match():
    print("Welcome to Emoji Memory Match!")
    emojis = ['🍎', '🌸', '🚗', '🎲', '🐱', '🍕']
    board = emojis * 2
    random.shuffle(board)
    revealed = ['❓'] * 12
    def show_board():
        for i, v in enumerate(revealed):
            sep = '\n' if (i+1) % 4 == 0 else ' '
            print(f'{v}({i+1})', end=sep)
        print()
    while '?' in revealed or '❓' in revealed:
        show_board()
        try:
            f1 = int(input("Pick first (1-12): ")) - 1
            f2 = int(input("Pick second (1-12): ")) - 1
            if f1 == f2 or not (0 <= f1 < 12) or not (0 <= f2 < 12) or revealed[f1] != '❓' or revealed[f2] != '❓':
                print("Invalid picks, try again.")
                continue
            revealed[f1], revealed[f2] = board[f1], board[f2]
            show_board()
            if board[f1] != board[f2]:
                print("No match! Hiding again...")
                time.sleep(1.5)
                revealed[f1], revealed[f2] = '❓', '❓'
            else:
                print("Match found! 🎉")
        except Exception:
            print("Please enter valid positions.")
        if all(x != '❓' for x in revealed):
            print("You matched them all! Well done! 🏆")
            break

if __name__ == "__main__":
    emoji_memory_match()
