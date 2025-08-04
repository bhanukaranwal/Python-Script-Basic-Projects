import random

def word_snake():
    print("🐍 Welcome to Word Snake! 🐍")
    print("Connect words by picking one that starts with the last letter of the previous word.")
    print("Try to make the snake as long as you can. Type 'q' to quit at any time.\n")

    words = [
        'apple', 'elephant', 'tiger', 'rat', 'tarantula', 'ant', 'tree',
        'emu', 'umbrella', 'antelope', 'egg', 'goat', 'tapir', 'rabbit'
    ]
    used = []
    current_word = random.choice(words)
    used.append(current_word)
    print(f"Starting word: {current_word}")
    score = 0

    while True:
        last_char = current_word[-1]
        options = [w for w in words if w[0] == last_char and w not in used]
        if not options:
            print("No more words to continue the snake. Game Over!")
            break
        print(f"\nCurrent word ends with '{last_char}'. Choose next word:")
        for i, w in enumerate(options):
            print(f"{i+1}. {w}")
        choice = input(f"Enter choice number (1-{len(options)}) or 'q' to quit: ")
        if choice.lower() == 'q':
            print(f"\nQuitting. Your final score: {score}")
            break
        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("Invalid choice, try again.")
            continue
        current_word = options[int(choice)-1]
        used.append(current_word)
        score += 1
        print(f"Great! Current score: {score}")

    print("\nThanks for playing Word Snake!")
    print(f"Words you built: {', '.join(used)}")

if __name__ == '__main__':
    word_snake()
