import random

def food_bot():
    foods = ["Pizza", "Sushi", "Tacos", "Ice Cream", "Falafel", "Salad", "Pasta", "Burger"]
    print("Can't decide what to eat? Let the bot help you!")
    input("Press Enter for your random food suggestion: ")
    print(f"You should try: {random.choice(foods)}! 🍽️")

if __name__ == "__main__":
    food_bot()
