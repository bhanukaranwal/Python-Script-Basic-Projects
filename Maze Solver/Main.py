def maze_game():
    maze = [
        ['S', ' ', ' ', '#', ' ', ' ', ' '],
        [' ', '#', ' ', '#', ' ', '#', ' '],
        [' ', '#', ' ', ' ', ' ', '#', ' '],
        [' ', ' ', '#', '#', ' ', ' ', ' '],
        ['#', ' ', '#', 'E', '#', '#', ' ']
    ]
    position = [0, 0]

    def print_maze():
        for r, row in enumerate(maze):
            line = ''
            for c, tile in enumerate(row):
                if [r, c] == position:
                    line += 'P '
                else:
                    line += tile + ' '
            print(line)

    print("\nWelcome to Maze Solver!")
    print("Find the exit 'E' starting from 'S'. Use 'up', 'down', 'left', 'right' to move.")

    while True:
        print_maze()
        move = input("Move: ").lower()
        r, c = position
        if move == 'up' and r > 0 and maze[r-1][c] != '#':
            position = [r-1, c]
        elif move == 'down' and r < len(maze)-1 and maze[r+1][c] != '#':
            position = [r+1, c]
        elif move == 'left' and c > 0 and maze[r][c-1] != '#':
            position = [r, c-1]
        elif move == 'right' and c < len(maze[0])-1 and maze[r][c+1] != '#':
            position = [r, c+1]
        else:
            print("Invalid move or blocked by wall.")
            continue
        if maze[position[0]][position[1]] == 'E':
            print("Congratulations! You escaped the maze!")
            break

if __name__ == '__main__':
    maze_game()
