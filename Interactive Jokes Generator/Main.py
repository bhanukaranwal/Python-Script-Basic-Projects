import random

def joke_generator():
    jokes = [
        ("Why did the computer go to the doctor?", "Because it had a virus!"),
        ("What do you call a bear with no teeth?", "A gummy bear!"),
        ("Why did the math book look sad?", "Because it had too many problems."),
        ("Why was the broom late?", "It swept in!")
    ]
    joke = random.choice(jokes)
    print(joke[0])
    input("Press Enter for the answer...")
    print(joke[1])

if __name__ == "__main__":
    joke_generator()
