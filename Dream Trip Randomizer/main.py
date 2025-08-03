import random

def dream_trip_randomizer():
    print("Let's imagine your next dream adventure destination!")
    destinations = ["the beaches of Bali", "the mountains of Switzerland", "the nightlife of Tokyo", "the rainforests of Costa Rica", "the deserts of Morocco"]
    activities = ["surfing", "hiking", "immersing in local culture", "wildlife photography", "sampling street food"]
    travel_styles = ["solo travel", "luxury resort", "budget backpacking", "road trip", "cruise adventure"]

    input("Press Enter to generate your dream trip plan...")
    print(f"You are going to {random.choice(destinations)}, where you'll enjoy {random.choice(activities)} during a {random.choice(travel_styles)}!")
    print("Doesn't that sound amazing? 🌍✈️")

if __name__ == "__main__":
    dream_trip_randomizer()
