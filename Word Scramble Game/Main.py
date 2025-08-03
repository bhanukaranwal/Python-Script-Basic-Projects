import random

def word_scramble():
    words = ['developer', 'python', 'assistant', 'puzzle', 'keyboard']
    word = random.choice(words)
    scrambled = ''.join(random.sample(word, len(word)))
    print(f"Unscramble this word: {scrambled}")
    guess = input("Your guess: ")
    if guess.lower() == word:
        print("Correct! 🎉")
    else:
        print(f"Oops! The word was: {word}")

if __name__ == "__main__":
    word_scramble()
