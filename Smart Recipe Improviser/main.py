# Smart Recipe Improviser — main.py

from typing import List

class SmartRecipeImproviser:
    def __init__(self, available_ingredients: List[str]):
        self.available_ingredients = set(ingredient.lower() for ingredient in available_ingredients)
        # A basic recipe database
        self.recipes = {
            'omelet': {'eggs', 'cheese', 'salt', 'pepper'},
            'salad': {'lettuce', 'tomato', 'cucumber', 'olive oil'},
            'pasta': {'pasta', 'tomato sauce', 'olive oil', 'garlic'},
            'grilled cheese sandwich': {'bread', 'cheese', 'butter'},
            'fruit smoothie': {'banana', 'milk', 'honey'},
        }

    def suggest_recipes(self) -> List[str]:
        suggestions = []
        for recipe, ingredients in self.recipes.items():
            missing = ingredients - self.available_ingredients
            if len(missing) == 0:
                suggestions.append(f"You can make a {recipe} with your ingredients.")
            elif len(missing) <= 2:
                suggestions.append(f"Almost! You need {', '.join(missing)} to make {recipe}.")
        if not suggestions:
            suggestions.append("No recipes match your ingredients exactly or almost. Try adding more basics!")
        return suggestions

if __name__ == '__main__':
    # Interactive version (uncomment for real use):
    # user_ingredients = input("Enter available ingredients separated by commas: ")
    # ingredients_list = [item.strip() for item in user_ingredients.split(',')]

    # For demonstration, using fixed ingredients:
    ingredients_list = ["eggs", "cheese", "bread", "butter"]

    improvisor = SmartRecipeImproviser(ingredients_list)
    recipe_suggestions = improvisor.suggest_recipes()

    print("Recipe Suggestions:")
    for suggestion in recipe_suggestions:
        print(f"- {suggestion}")

# Extensions:
# - Add NLP to handle ingredient synonyms/descriptions
# - Expand with a real recipe API or dataset and substitution logic
# - Implement an image-to-ingredient recognizer (OpenCV/CNN)
# - Build a shopping list function for nearly-complete recipes
# - Integrate nutritional scoring and meal planning
