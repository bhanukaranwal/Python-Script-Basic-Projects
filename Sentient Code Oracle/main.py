import random
import hashlib
import sys

# ASCII art for the digital crystal ball
CRYSTAL_BALL = r"""
      .-"      "-.
    .'            '.
   /                \
  ;                  ;
 |                    |
 ;  .-.          .-.  ;
  \ (0 )--------(0 ) /
   '.              .'
     '-.,______.,-'
"""

# Predefined poetic code-like phrases for prophecies
PHRASES = [
    "0101: The loop of fate unwinds",
    "0xDEADBEEF: Secrets lurking in shadows",
    "while (time < infinity): hope persists",
    "nullPointer: The void awaits",
    "def destiny(): return unknown",
    "await the signal in the silence",
    "echoes of the forgotten recursive call",
    "import chaos as order",
    "lambda x: x * mystery",
    "try: seek; except: surrender",
    "#pragma once upon a time",
]

def generate_prophecy(question):
    # Use a hash of the question to seed randomness for consistent yet surprising results
    seed = int(hashlib.sha256(question.encode()).hexdigest(), 16)
    random.seed(seed)

    # Choose phrases and assemble cryptic prophecy with some randomness and variation
    prophecy_lines = []
    for _ in range(3):
        line = random.choice(PHRASES)
        # Add some random modifications like flipping case, adding dots, or numbers to add mystery
        if random.random() > 0.5:
            line = line.upper()
        if random.random() > 0.7:
            line += "..." * random.randint(1, 3)
        if random.random() > 0.8:
            line = line[::-1]  # reverse the line
        prophecy_lines.append(line)

    return prophecy_lines

def main():
    print("WELCOME TO THE SENTIENT CODE ORACLE")
    print(CRYSTAL_BALL)
    print("Ask your question to the oracle (type 'exit' to quit).")

    while True:
        question = input("\n> ")
        if question.strip().lower() == "exit":
            print("May the code guide you. Farewell.")
            break

        if not question.strip():
            print("Please ask a meaningful question.")
            continue

        print("\nThe oracle contemplates your query...\n")
        prophecy = generate_prophecy(question)
        for line in prophecy:
            print(line)
        print("\n" + CRYSTAL_BALL)

if __name__ == "__main__":
    main()
