import random

def fortune_cookie():
    fortunes = [
        "Today is your lucky day!",
        "A fun surprise awaits you.",
        "Keep an open mind, adventure is near.",
        "You will learn something new today!"
    ]
    input("Crack open your virtual fortune cookie (press Enter)!")
    print("Your fortune:", random.choice(fortunes))

if __name__ == "__main__":
    fortune_cookie()
