import random

def magic_8_ball():
    responses = [
        "Yes, definitely!",
        "Ask again later.",
        "No way!",
        "Absolutely!",
        "It is uncertain.",
        "Very likely.",
        "Don’t count on it.",
        "You may rely on it.",
        "Cannot predict now.",
        "My sources say no."
    ]
    print("🎱 Welcome to the Magic 8-Ball!")
    while True:
        question = input("Ask a yes/no question (or type 'exit' to stop): ")
        if question.lower() == 'exit':
            print("Goodbye, your future awaits!")
            break
        print("8-Ball says:", random.choice(responses))

if __name__ == '__main__':
    magic_8_ball()
