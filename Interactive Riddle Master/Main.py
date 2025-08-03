def riddle_master():
    riddles = [
        ("What has to be broken before you can use it?", "egg"),
        ("I’m tall when I’m young, and I’m short when I’m old. What am I?", "candle"),
        ("What month of the year has 28 days?", "all"),
        ("What is full of holes but still holds water?", "sponge"),
    ]
    print("Welcome to the Riddle Master! Try to solve these riddles:")
    score = 0
    for question, answer in riddles:
        user = input(question + " ").strip().lower()
        if user == answer or (answer == "all" and user in ["february", "all"]):
            print("Correct! 🎉")
            score += 1
        else:
            print(f"Wrong! The answer was: {answer}")
    print(f"Game over! You scored {score}/{len(riddles)}.")

if __name__ == "__main__":
    riddle_master()
