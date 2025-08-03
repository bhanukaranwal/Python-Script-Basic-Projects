def emoji_board():
    print("Let's draw a 5x5 emoji board! Type an emoji or character for each cell.")
    board = []
    for row in range(5):
        current_row = []
        for col in range(5):
            char = input(f"Cell [{row+1},{col+1}]: ")
            current_row.append(char if char else '⬜')
        board.append(current_row)
    print("\nYour Emoji Board:")
    for row in board:
        print(' '.join(row))

if __name__ == "__main__":
    emoji_board()
