def who_am_i():
    print("Welcome to the 'Who Am I?' game!")
    print("I’ll think of a famous person, and you try to guess who by asking yes/no questions.")
    people = [
        {"name": "Albert Einstein", "facts": ["scientist", "theory of relativity", "crazy hair"]},
        {"name": "Taylor Swift", "facts": ["singer", "pop music", "1989 album"]},
        {"name": "Lionel Messi", "facts": ["footballer", "Argentina", "Barcelona legend"]},
        {"name": "Harry Potter", "facts": ["wizard", "Hogwarts", "scar on forehead"]},
        {"name": "Elon Musk", "facts": ["entrepreneur", "Tesla", "SpaceX"]}
    ]
    import random
    chosen = random.choice(people)
    print("I have someone in mind! Start asking yes/no questions. When you want to guess, type 'guess'.")
    asked_facts = []
    while True:
        question = input("Ask a yes/no question (or type 'guess'): ").strip().lower()
        if question == 'guess':
            guess = input("Who do you think I am? ").strip()
            if guess.lower() == chosen["name"].lower():
                print("Correct! 🎉 You win!")
                break
            else:
                print("Nope! Try more questions or make another guess.")
        else:
            # Simulate 'yes' if the question has a keyword in facts, else random answer
            matched = any(word in question for word in chosen['facts'])
            if matched:
                print("Yes!")
            else:
                print(random.choice(["No.", "Maybe.", "I can't say.", "Hmm, not really."]))
            asked_facts.append(question)
    print(f"The answer was: {chosen['name']}! Facts: {', '.join(chosen['facts'])}")

if __name__ == "__main__":
    who_am_i()
