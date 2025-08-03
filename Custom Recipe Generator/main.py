import random

def recipe_generator():
    proteins = ["chicken", "tofu", "paneer", "beef", "mushroom", "egg"]
    sides = ["rice", "mashed potatoes", "quinoa", "pasta", "naan", "tacos"]
    spices = ["garlic", "basil", "ginger", "pepper", "paprika", "cinnamon"]
    extras = ["grilled pineapple", "chopped peanuts", "honey drizzle", "avocado slices", "crispy bacon", "soy sauce"]

    print("Welcome to the Custom Recipe Generator!")
    main = input("Enter your favorite main ingredient: ").strip().lower()
    if not main:
        main = random.choice(proteins)
    side = random.choice(sides)
    spice = random.choice(spices)
    extra = random.choice(extras)

    print("\nHere's your random recipe:")
    print(f"Take {main}, season it with {spice}, and serve it over {side}. Top it with {extra} for a twist!")
    print("Bon appétit! 🍽️")

if __name__ == "__main__":
    recipe_generator()
