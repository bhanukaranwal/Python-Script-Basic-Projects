import random

def silly_spy_decoder():
    chars = "abcdefghijklmnopqrstuvwxyz "
    message = "meet at the secret spot"
    shift = random.randint(1, 10)
    coded = "".join(chars[(chars.index(c)+shift)%27] if c in chars else c for c in message)
    print(f"Spy message: {coded}")
    guess = input(f"Decode the message! (Hint: each letter shifted by {shift}): ").strip().lower()
    if guess == message:
        print("You cracked the code! 🕵️‍♂️")
    else:
        print(f"Oops! The correct message was: '{message}'")

if __name__ == "__main__":
    silly_spy_decoder()
