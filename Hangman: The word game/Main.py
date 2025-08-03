import random

def hangman():
    words = ['python', 'algorithm', 'function', 'variable', 'machine', 'learning']
    word = random.choice(words)
    guessed = set()
    tries = 6
    while tries > 0:
        masked = ''.join([char if char in guessed else '_' for char in word])
        print("Word: ", masked, f"  Tries left: {tries}")
        if '_' not in masked:
            print("You won!")
            return
        guess = input("Guess a letter: ").lower()
        if guess in word:
            guessed.add(guess)
        else:
            tries -= 1
            print("Wrong!")
    print(f"Game Over. The word was: {word}")

if __name__ == "__main__":
    hangman()
