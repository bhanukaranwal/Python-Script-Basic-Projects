import random

def dungeon_escape():
    print("\nWelcome to Dungeon Escape! Try to escape the mysterious dungeon.")
    position = "entrance"
    inventory = []

    while True:
        print(f"\nYou are at the {position}.")
        if position == "entrance":
            action = input("Go 'north' to hallway or 'east' to kitchen? ").lower()
            if action == "north":
                position = "hallway"
            elif action == "east":
                position = "kitchen"
            else:
                print("Invalid direction.")
        elif position == "hallway":
            action = input("Go 'south' to entrance or 'up' to tower stairs? ").lower()
            if action == "south":
                position = "entrance"
            elif action == "up":
                position = "tower stairs"
            else:
                print("Invalid direction.")
        elif position == "kitchen":
            if "key" not in inventory:
                print("You found a rusty key on the floor!")
                inventory.append("key")
            action = input("Go 'west' to entrance or try to 'open door' to the cellar? ").lower()
            if action == "west":
                position = "entrance"
            elif action == "open door":
                if "key" in inventory:
                    position = "cellar"
                else:
                    print("Door is locked. You need a key.")
            else:
                print("Invalid action.")
        elif position == "tower stairs":
            action = input("Go 'down' to hallway or 'climb' the tower? ").lower()
            if action == "down":
                position = "hallway"
            elif action == "climb":
                position = "tower top"
            else:
                print("Invalid action.")
        elif position == "cellar":
            action = input("A dragon blocks your way! 'fight' or 'run'? ").lower()
            if action == "fight":
                if "sword" in inventory:
                    print("You slayed the dragon and escaped! You win! 🐉")
                    break
                else:
                    print("You have no sword! Game over.")
                    break
            elif action == "run":
                position = "kitchen"
            else:
                print("Invalid action.")
        elif position == "tower top":
            if "sword" not in inventory:
                print("You found a shining sword!")
                inventory.append("sword")
            action = input("Go 'down' or 'jump' out the window? ").lower()
            if action == "down":
                position = "tower stairs"
            elif action == "jump":
                print("You jumped to freedom! You win! 🦸")
                break
            else:
                print("Invalid action.")

if __name__ == "__main__":
    dungeon_escape()
