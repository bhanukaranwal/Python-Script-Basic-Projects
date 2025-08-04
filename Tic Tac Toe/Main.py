import random

def tic_tac_toe():
    board = [' ' for _ in range(9)]

    def print_board():
        print('\n')
        for i in range(3):
            print(' | '.join(board[i*3:(i+1)*3]))
            if i < 2:
                print('--+---+--')

    def check_winner(p):
        wins = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
        return any(board[a]==board[b]==board[c]==p for a,b,c in wins)

    def player_move():
        while True:
            move = input("Choose position (1-9): ")
            if move in [str(i) for i in range(1,10)] and board[int(move)-1]==' ':
                board[int(move)-1] = 'X'
                break
            print("Invalid move, try again.")

    def computer_move():
        empty = [i for i,v in enumerate(board) if v==' ']
        move = random.choice(empty)
        board[move] = 'O'

    print("Tic Tac Toe: You [X] vs Computer [O]")
    print_board()
    for turn in range(9):
        if turn%2==0:
            player_move()
        else:
            computer_move()
        print_board()
        if check_winner('X'):
            print("You win! 🎉")
            return
        elif check_winner('O'):
            print("Computer wins! 🤖")
            return
    print("It's a tie!")

if __name__ == "__main__":
    tic_tac_toe()
