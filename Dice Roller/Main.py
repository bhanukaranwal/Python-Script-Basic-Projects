import random

def show_die(n):
    faces = {
        1: [" ----- ", "|     |", "|  *  |", "|     |", " ----- "],
        2: [" ----- ", "| *   |", "|     |", "|   * |", " ----- "],
        3: [" ----- ", "| *   |", "|  *  |", "|   * |", " ----- "],
        4: [" ----- ", "| * * |", "|     |", "| * * |", " ----- "],
        5: [" ----- ", "| * * |", "|  *  |", "| * * |", " ----- "],
        6: [" ----- ", "| * * |", "| * * |", "| * * |", " ----- "],
    }
    for line in faces[n]:
        print(line)

def dice_roller():
    print("Welcome to the Dice Roller! 🎲")
    history = []
    while True:
        sides = input("How many sides? (or 'q' to quit): ")
        if sides.lower() == 'q':
            print("Roll history:", history)
            break
        if not sides.isdigit() or int(sides)<2:
            print("Enter a positive number greater than 1.")
            continue
        roll = random.randint(1, int(sides))
        print(f"You rolled a {roll}!")
        if int(sides) == 6:
            show_die(roll)
        history.append(roll)

if __name__ == "__main__":
    dice_roller()
