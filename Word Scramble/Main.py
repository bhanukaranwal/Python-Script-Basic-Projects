import random

def word_puzzle():
    print("\nWelcome to the Word Scramble Puzzle!")
    words = {"galaxy":"A huge system of stars", 'python':"A popular programming language", 
             'nebula':"A cloud of gas in space", 'rocket':"Space travel vehicle",
             'alien':"An ET being", 'planet':"A body that orbits a star", 
             'asteroid':"A small rocky object in space"}
    word, clue = random.choice(list(words.items()))
    scrambled = ''.join(random.sample(word, len(word)))
    print(f"Scrambled word: {scrambled}")
    for attempt in range(3, 0, -1):
        guess = input(f"Your guess ({attempt} attempts left): ").lower()
        if guess == word:
            print("Correct! You solved the puzzle!")
            return
        if attempt == 2:
            print("Clue:", clue)
    print(f"Out of attempts! The word was: {word}")

if __name__ == '__main__':
    word_puzzle()
