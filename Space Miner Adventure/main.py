import random

def space_miner():
    print("\nWelcome to Space Miner! Mine precious space minerals and avoid hazards! 🚀")
    minerals = 0
    moves = 0
    while True:
        action = input("Choose action - mine, shield, or quit: ").lower()
        if action == 'quit':
            print(f"Mission ended. You mined {minerals} units in {moves} moves!")
            break
        elif action == 'mine':
            hazard = random.choice([True, False, False])  # 1/3 chance of hazard
            if hazard:
                print("Asteroid strike! You lost some minerals.")
                lost = random.randint(1, minerals) if minerals > 0 else 0
                minerals -= lost
            else:
                found = random.randint(1, 10)
                print(f"You mined {found} units of minerals.")
                minerals += found
            moves += 1
        elif action == 'shield':
            print("Shield activated for next move! No hazard damage.")
            moves += 1
            if input("Next move mine or quit? ").lower() == 'mine':
                found = random.randint(1, 10)
                print(f"Shield protected! You safely mined {found} units.")
                minerals += found
                moves += 1
            else:
                print(f"Mission ended. You mined {minerals} units in {moves} moves!")
                break
        else:
            print("Invalid action. Try mine, shield, or quit.")

if __name__ == "__main__":
    space_miner()
