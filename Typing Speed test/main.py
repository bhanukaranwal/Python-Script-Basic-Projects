import time
import random

def typing_speed_test():
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "Python programming is super fun.",
        "I love learning new things every day.",
        "Code, debug, and repeat!"
    ]
    target = random.choice(sentences)
    print("Type this as fast as you can!\n")
    print(target)
    input("Press Enter to start...")
    start_time = time.time()
    typed = input()
    end_time = time.time()
    accuracy = len(set(typed.split()) & set(target.split())) / len(target.split()) * 100
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == '__main__':
    typing_speed_test()
