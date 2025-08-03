import random

def story_generator():
    print("Let's make a story together!")
    name = input("Name of a person: ")
    place = input("A place: ")
    animal = input("An animal: ")
    action = input("A verb ending in -ing: ")
    item = input("Something you can hold: ")
    twist = random.choice([
        f"Suddenly, {name} discovered the {item} was magical!",
        f"Out of nowhere, a {animal} started {action} in {place}.",
        f"But then a mysterious wind swept {item} away!",
    ])
    print("\nStory Time!")
    print(f"One day, {name} went to {place}. There, they saw a {animal} {action} with a {item}. {twist}")

if __name__ == "__main__":
    story_generator()
