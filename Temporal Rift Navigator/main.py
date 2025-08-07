import random
import sys

RIFTS = {
    "start": {
        "description": "You stand at the crossroads where time frays and realities blur.",
        "choices": {
            "Enter the rift to the Clockwork Forest": "clockwork_forest",
            "Step through the shimmering veil": "shimmering_veil",
            "Walk back into the fading past": "fading_past"
        }
    },
    "clockwork_forest": {
        "description": "The forest hums with clockwork trees and ticking shadows.",
        "choices": {
            "Climb a giant gear tree": "gear_tree",
            "Follow the ticking river": "ticking_river",
            "Return to the crossroads": "start"
        }
    },
    "shimmering_veil": {
        "description": "A veil of shifting colors ripples, revealing strange glimpses of other worlds.",
        "choices": {
            "Reach through the veil": "other_world",
            "Step aside and watch": "watch_veil",
            "Return to the crossroads": "start"
        }
    },
    "fading_past": {
        "description": "Shadows lengthen and memories fade in this drifting past.",
        "choices": {
            "Chase a fading memory": "memory_chase",
            "Sit and wait for the future": "wait_future",
            "Return to the crossroads": "start"
        }
    },
    "gear_tree": {
        "description": "High above, the world turns in mechanical precision.",
        "choices": {
            "Jump into the gears": "gear_jump",
            "Descend carefully": "clockwork_forest"
        }
    },
    "ticking_river": {
        "description": "The river’s ticking flows backward and forwards in time.",
        "choices": {
            "Sail upstream": "upstream",
            "Sail downstream": "downstream",
            "Return to the forest": "clockwork_forest"
        }
    },
    # Additional branches with surreal descriptions
    "other_world": {
        "description": "You glimpse an impossible landscape where stars breathe.",
        "choices": {"Return to the veil": "shimmering_veil"}
    },
    "watch_veil": {
        "description": "Colors dance on the veil, whispering secrets to the patient.",
        "choices": {"Return to the veil": "shimmering_veil"}
    },
    "memory_chase": {
        "description": "Fleeting images swirl, elusive yet beckoning.",
        "choices": {"Return to fading past": "fading_past"}
    },
    "wait_future": {
        "description": "In stillness, tomorrow's possibilities shimmer faintly.",
        "choices": {"Return to fading past": "fading_past"}
    },
    "gear_jump": {
        "description": "You tumble through shifting gears, caught between moments.",
        "choices": {"Return to gear tree": "gear_tree"}
    },
    "upstream": {
        "description": "The river carries you through forgotten times.",
        "choices": {"Return to ticking river": "ticking_river"}
    },
    "downstream": {
        "description": "Future currents pull you toward unknown destinies.",
        "choices": {"Return to ticking river": "ticking_river"}
    }
}

ASCII_MAPS = {
    "start": """
   +-----------------+
   | Crossroads of   |
   | Time & Reality  |
   +-------+---------+
           |
    +------+------+
    |             |
Clockwork   Shimmering Veil
 Forest
    """,
    "clockwork_forest": """
   +----------------------+
   | Clockwork Forest     |
   | Tick, Tock, Tick...  |
   +---+---------+--------+
       |         |
 Gear Tree  Ticking River
    """,
    "shimmering_veil": """
   +-------------------------+
   | Shimmering Veil         |
   | Colors ripple & shift   |
   +-----------+-------------+
               |
          Other Worlds
    """,
    "fading_past": """
   +---------------------+
   | Fading Past         |
   | Shadows & Memories  |
   +---------+-----------+
             |
         Memories
    """
}

def display_location(name):
    loc = RIFTS.get(name)
    if not loc:
        print("Lost in the rift...")
        return None

    print("\n" + ASCII_MAPS.get(name, ""))
    print(loc["description"] + "\n")

    if not loc["choices"]:
        print("The rift closes...\n")
        return None

    print("Choices:")
    for i, choice in enumerate(loc["choices"].keys(), 1):
        print(f"{i}. {choice}")
    return loc

def main():
    print("Welcome to the Temporal Rift Navigator.\n")
    current_location = "start"

    while True:
        location = display_location(current_location)
        if not location:
            break

        user_choice = input("Select a choice (number): ").strip()
        try:
            choice_idx = int(user_choice) - 1
            choices = list(location["choices"].keys())
            if 0 <= choice_idx < len(choices):
                selected = choices[choice_idx]
                current_location = location["choices"][selected]
            else:
                print("Invalid choice number. Try again.")
        except ValueError:
            print("Please enter a number corresponding to your choice.")

    print("\nThank you for exploring the rifts of time.\n")

if __name__ == "__main__":
    main()
