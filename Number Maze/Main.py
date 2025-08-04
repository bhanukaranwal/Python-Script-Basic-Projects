import random

def number_maze():
    grid_size = 5
    player_pos = [0, 0]
    treasure = [random.randint(2, grid_size-1), random.randint(2, grid_size-1)]
    pits = set()
    while len(pits) < 5:
        pit = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        if pit != tuple(treasure) and pit != (0,0):
            pits.add(pit)
    print("Find the treasure without falling into a pit!")
    while True:
        print(f"You are at {player_pos}")
        print(f"Possible moves: up, down, left, right")
        move = input("Your move: ").lower()
        x, y = player_pos
        if move == "up" and x > 0:
            x -= 1
        elif move == "down" and x < grid_size-1:
            x += 1
        elif move == "left" and y > 0:
            y -= 1
        elif move == "right" and y < grid_size-1:
            y += 1
        else:
            print("Can't move that way.")
            continue
        player_pos = [x, y]
        if tuple(player_pos) in pits:
            print("Oh no! You fell into a pit. Game over.")
            break
        if player_pos == treasure:
            print("Congratulations! You found the treasure! 🏆")
            break

if __name__ == "__main__":
    number_maze()
