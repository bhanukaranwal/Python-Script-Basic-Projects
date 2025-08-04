def alien_language_translator():
    print("\nWelcome to the Alien Language Translator! 🌌")
    alien_alphabet = {
        'a': '@', 'b': '#', 'c': '$', 'd': '%', 'e': '^', 'f': '&', 'g': '*',
        'h': '!', 'i': '?', 'j': '+', 'k': '-', 'l': '=', 'm': '~', 'n': '<',
        'o': '>', 'p': '/', 'q': '[', 'r': ']', 's': '{', 't': '}', 'u': '|',
        'v': ':', 'w': ';', 'x': '_', 'y': '`', 'z': '.'
    }
    def translate(text):
        return ''.join(alien_alphabet.get(c.lower(), c) for c in text)
    while True:
        phrase = input("Type something to translate (or type 'exit' to quit): ")
        if phrase.lower() == 'exit':
            print("Goodbye, Earthling! 👽")
            break
        print(f"Alien translation: {translate(phrase)}\n")

if __name__ == "__main__":
    alien_language_translator()
