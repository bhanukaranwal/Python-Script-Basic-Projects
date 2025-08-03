import random

def compliment_poem():
    starters = [
        "Roses are red,",
        "Violets are blue,",
        "Sunbeams are bright,",
        "Starlight is sparkly,"
    ]
    lines2 = [
        "your smile is like sunshine,",
        "you light up the room,",
        "your ideas are brilliant,",
        "you have a heart of gold,"
    ]
    lines3 = [
        "every day with you feels new.",
        "your presence brings joy and bloom.",
        "your kindness is endless too.",
        "the world needs more people like you."
    ]
    lines4 = [
        "Keep being amazing,",
        "Shine on, wonderful soul,",
        "Never forget your worth,",
        "May happiness follow your stroll,"
    ]

    print("Here's your personalized compliment poem!\n")
    print(random.choice(starters))
    print(random.choice(lines2))
    print(random.choice(lines3))
    print(random.choice(lines4))

if __name__ == "__main__":
    compliment_poem()
