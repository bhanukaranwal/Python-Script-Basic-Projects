# Personalized Nutrition and Meal Recommendation System — main.py

from typing import List, Dict

class UserProfile:
    def __init__(self, name: str, dietary_preferences: List[str], allergies: List[str], goals: Dict[str, float]):
        self.name = name
        self.dietary_preferences = dietary_preferences
        self.allergies = allergies
        self.goals = goals  # e.g., {'calories': 2000, 'protein': 150}

class Recipe:
    def __init__(self, name: str, ingredients: Dict[str, float], nutrition: Dict[str, float]):
        self.name = name
        self.ingredients = ingredients  # {ingredient_name: quantity_in_grams}
        self.nutrition = nutrition      # e.g., {'calories': 500, 'protein': 30, 'carbs': 50, 'fat': 20}

class NutritionRecommender:
    def __init__(self, user: UserProfile, recipes: List[Recipe]):
        self.user = user
        self.recipes = recipes

    def filter_recipes(self) -> List[Recipe]:
        filtered = []
        for recipe in self.recipes:
            if any(allergy in recipe.ingredients for allergy in self.user.allergies):
                continue
            # Check basic dietary preferences (vegetarian, vegan, etc.)
            if 'vegetarian' in self.user.dietary_preferences and 'meat' in recipe.ingredients:
                continue
            if 'vegan' in self.user.dietary_preferences and any(item in recipe.ingredients for item in ['meat', 'egg', 'milk']):
                continue
            filtered.append(recipe)
        return filtered

    def recommend_meals(self):
        filtered = self.filter_recipes()
        recommendations = []
        for recipe in filtered:
            # Simple goal matching: calories and protein
            calorie_ok = recipe.nutrition.get('calories', 0) <= self.user.goals.get('calories', float('inf'))
            protein_ok = recipe.nutrition.get('protein', 0) >= self.user.goals.get('protein', 0)
            if calorie_ok and protein_ok:
                recommendations.append(recipe)
        return recommendations

if __name__ == '__main__':
    user = UserProfile(
        name='Alice',
        dietary_preferences=['vegetarian'],
        allergies=['peanut'],
        goals={'calories': 600, 'protein': 20}
    )

    recipes = [
        Recipe('Grilled Tofu Salad', {'tofu': 150, 'lettuce': 100, 'olive oil': 20}, {'calories': 450, 'protein': 35, 'carbs': 20, 'fat': 15}),
        Recipe('Peanut Butter Sandwich', {'bread': 100, 'peanut butter': 50}, {'calories': 700, 'protein': 25, 'carbs': 50, 'fat': 30}),
        Recipe('Veggie Stir Fry', {'broccoli': 100, 'carrot': 80, 'soy sauce': 10}, {'calories': 350, 'protein': 15, 'carbs': 40, 'fat': 5}),
        Recipe('Chicken Wrap', {'chicken': 120, 'tortilla': 80, 'lettuce': 40}, {'calories': 600, 'protein': 40, 'carbs': 45, 'fat': 20}),
    ]

    recommender = NutritionRecommender(user, recipes)
    suitable_meals = recommender.recommend_meals()

    print(f"Recommended meals for {user.name}:")
    for meal in suitable_meals:
        print(f"- {meal.name}")

# Extensions:
# - Integrate with real-world nutrition databases (like the USDA API)
# - Use computer vision for logging meals from photos
# - Plan multi-day meal plans with grocery lists export
# - Provide suggestions based on personal fridge inventory
# - Deploy as a mobile/web app with voice (NLP) or chatbot interaction
