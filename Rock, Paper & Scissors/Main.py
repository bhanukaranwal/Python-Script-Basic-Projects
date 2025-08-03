import random

def rps_game():
    options = ['rock', 'paper', 'scissors']
    user_score = 0
    comp_score = 0
    print("Enter 'exit' to stop playing.")
    while True:
        user = input("Choose rock/paper/scissors: ").lower()
        if user == 'exit':
            break
        comp = random.choice(options)
        print(f"Computer chose: {comp}")
        if user == comp:
            print("It's a tie!")
        elif (user, comp) in [('rock', 'scissors'), ('paper', 'rock'), ('scissors', 'paper')]:
            print("You win!")
            user_score += 1
        elif user in options:
            print("Computer wins!")
            comp_score += 1
        else:
            print("Invalid input.")

    print(f"Final Score: You {user_score} - Computer {comp_score}")

if __name__ == "__main__":
    rps_game()
