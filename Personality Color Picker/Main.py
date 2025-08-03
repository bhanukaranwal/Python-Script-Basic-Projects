def color_picker():
    print("Pick a number from 1 to 4 to see your personality color!")
    choice = input("Your number: ").strip()
    colors = {
        "1": "Red - You are bold and passionate!",
        "2": "Blue - Calm and wise.",
        "3": "Green - Friendly and balanced.",
        "4": "Yellow - Creative and cheerful!"
    }
    print(colors.get(choice, "That's a unique choice; you're one of a kind!"))

if __name__ == "__main__":
    color_picker()
