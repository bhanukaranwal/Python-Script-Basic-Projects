import re
import difflib
import os

WORDLIST_FILE = "words_alpha.txt"  # Download from https://github.com/dwyl/english-words

def load_word_list():
    if not os.path.exists(WORDLIST_FILE):
        print(f"Word list file '{WORDLIST_FILE}' not found.")
        print("Please download from https://github.com/dwyl/english-words and place it in this folder.")
        return set()
    with open(WORDLIST_FILE, 'r') as f:
        words = set(line.strip().lower() for line in f)
    return words

def spelling_assistant():
    print("\nWelcome to the Real-Time Spelling Assistant!")
    dictionary = load_word_list()
    if not dictionary:
        return

    print("Type sentences below. Type 'exit' to quit.")
    while True:
        text = input("Your text: ").strip()
        if text.lower() == 'exit':
            print("Goodbye!")
            break
        words = re.findall(r'\b[a-z]+\b', text.lower())
        corrections = {}
        for word in words:
            if word not in dictionary:
                suggestions = difflib.get_close_matches(word, dictionary, n=3, cutoff=0.8)
                corrections[word] = suggestions
        if corrections:
            print("Possible corrections:")
            for w, sugg in corrections.items():
                print(f"  {w} -> {sugg if sugg else 'No suggestions'}")
        else:
            print("No spelling issues detected.")

if __name__ == '__main__':
    spelling_assistant()
