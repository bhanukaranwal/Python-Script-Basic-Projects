import random

def quiz():
    questions = {
        "What is the capital of France?": "paris",
        "What programming language is this?": "python",
        "How many legs does a spider have?": "8",
        "What color do you get by mixing red and blue?": "purple"
    }
    question = random.choice(list(questions))
    answer = questions[question]
    print("\033[1;34m" + question + "\033[0m")
    guess = input("Your answer: ").lower()
    if guess == answer:
        print("\033[1;32mCorrect! 🎉\033[0m")
    else:
        print(f"\033[1;31mNope! The answer is {answer}.\033[0m")

if __name__ == '__main__':
    quiz()
