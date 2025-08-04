def sudoku():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    def print_board():
        for i, row in enumerate(puzzle):
            rowstr = ' '.join(str(x) if x else '.' for x in row)
            print(rowstr[:6] + " | " + rowstr[6:12] + " | " + rowstr[12:])
            if (i+1)%3 == 0 and i < 8:
                print("-"*17)
    def is_valid(r, c, n):
        if n in puzzle[r]: return False
        if n in [puzzle[x][c] for x in range(9)]: return False
        sr,sc = 3*(r//3), 3*(c//3)
        for rr in range(sr, sr+3):
            for cc in range(sc, sc+3):
                if puzzle[rr][cc] == n: return False
        return True
    print("Sudoku (enter row col num, e.g. 3 5 7; enter 0 to quit)")
    while True:
        print_board()
        move = input("Enter your move: ")
        if move.strip() == '0':
            print("Game ended.")
            break
        try:
            r, c, n = map(int, move.strip().split())
            if not (1 <= r <= 9 and 1 <= c <= 9 and 1 <= n <= 9):
                print("Values must be in 1-9.")
                continue
            if puzzle[r-1][c-1] != 0:
                print("Cell already filled.")
                continue
            if is_valid(r-1, c-1, n):
                puzzle[r-1][c-1] = n
                print("Move accepted!\n")
            else:
                print("Invalid move (violates Sudoku rules).")
        except:
            print("Invalid format. Try: row col num (e.g. 6 3 9)")
if __name__ == "__main__":
    print("Which game? [1] Tic Tac Toe  [2] Dice Roller  [3] Sudoku")
    choice = input("Your choice: ")
    if choice=='1':
        tic_tac_toe()
    elif choice=='2':
        dice_roller()
    elif choice=='3':
        sudoku()
    else:
        print("Invalid choice.")
