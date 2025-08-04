import random

def animal_battle():
    print("\nWelcome to Animal Battle Arena!")
    animals = [
        {"name": "Lion", "hp": 60, "attack": 15},
        {"name": "Tiger", "hp": 55, "attack": 17},
        {"name": "Bear", "hp": 70, "attack": 13},
        {"name": "Wolf", "hp": 50, "attack": 14},
    ]

    player = random.choice(animals).copy()
    opponent = random.choice([a for a in animals if a != player]).copy()

    print(f"You are the mighty {player['name']}! Battle start!")
    print(f"Your opponent is the ferocious {opponent['name']}!")

    while player['hp'] > 0 and opponent['hp'] > 0:
        action = input("Choose 'attack' or 'heal': ").lower()
        if action == 'attack':
            opponent['hp'] -= player['attack']
            print(f"You attacked and dealt {player['attack']} damage.")
        elif action == 'heal':
            heal = random.randint(5, 15)
            player['hp'] += heal
            print(f"You healed yourself for {heal} HP.")
        else:
            print("Invalid action.")
            continue

        if opponent['hp'] <= 0:
            print(f"You defeated the {opponent['name']}! You win! 🏆")
            break

        opponent_attack = random.randint(7, opponent['attack'])
        player['hp'] -= opponent_attack
        print(f"The {opponent['name']} attacks and deals {opponent_attack} damage.")

        if player['hp'] <= 0:
            print(f"You were defeated by the {opponent['name']}. Better luck next time.")
            break

        print(f"Your HP: {player['hp']} | Opponent HP: {opponent['hp']}")

if __name__ == "__main__":
    animal_battle()
