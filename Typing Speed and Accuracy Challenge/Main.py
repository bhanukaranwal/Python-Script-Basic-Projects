import time
import random

def typing_challenge():
    sentences = [
        "Python programming is a lot of fun.",
        "The quick brown fox jumps over the lazy dog.",
        "Never stop learning and exploring.",
        "Artificial intelligence is changing the world."
    ]
    sentence = random.choice(sentences)
    print("Type the following sentence as fast as you can:\n")
    print(sentence)
    input("Press Enter when ready...")
    start = time.time()
    typed = input("\nStart typing: ")
    end = time.time()
    correct = sum(1 for a, b in zip(typed, sentence) if a == b)
    accuracy = correct / len(sentence) * 100
    print(f"\nTime taken: {end - start:.2f} seconds")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    typing_challenge()
