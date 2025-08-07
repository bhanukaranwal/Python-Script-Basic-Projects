import random
import sys

TIMELINES = {
    "start": {
        "description": "You stand at the Crossroads of Time, where past and future intertwine.",
        "choices": {
            "Follow the path to the Past": "past_path",
            "Step into the Future": "future_path",
            "Stay in the Present moment": "present_path"
        }
    },
    "past_path": {
        "description": "You meet your younger self, who warns you of coming events.",
        "choices": {
            "Heed the warning": "change_past",
            "Ignore and move forward": "paradox_loop"
        }
    },
    "future_path": {
        "description": "You encounter your future self, who claims they never left this place.",
        "choices": {
            "Trust your future self": "merge_timelines",
            "Doubt and seek another way": "paradox_loop"
        }
    },
    "present_path": {
        "description": "Time seems to fold around you, and you hear echoes of all timelines.",
        "choices": {
            "Embrace the echoes": "merge_timelines",
            "Resist and choose a path": "start"
        }
    },
    "change_past": {
        "description": "Your actions ripple through time, altering events in unforeseen ways.",
        "choices": {
            "Proceed cautiously": "paradox_loop",
            "Abandon changes": "start"
        }
    },
    "paradox_loop": {
        "description": "A temporal paradox loops endlessly, your decisions conflicting in a tangle.",
        "choices": {
            "Break the loop": "resolution",
            "Give in to the loop": "paradox_loop"
        }
    },
    "merge_timelines": {
        "description": "Timelines converge, blending memories and futures into one.",
        "choices": {
            "Accept the new reality": "resolution",
            "Fight to restore separation": "paradox_loop"
        }
    },
    "resolution": {
        "description": "The paradox resolves into a new timeline, strange but stable.",
        "choices": {}
    }
}

ASCII_DIAGRAMS = {
    "start": """
      +-----+
      |Start|
      +--+--+
         |
    +----+----+
    |         |
    Past    Future
    """,
    "paradox_loop": """
    /---------\\
    |  LOOP   |
    \\---------/
       ^    |
       |    v
    /---------\\
    |PARADOX  |
    \\---------/
    """,
    "resolution": """
     _____
    /     \\
   |Peace!|
    \\_____/
    """
}

def display_state(name):
    state = TIMELINES.get(name, None)
    if not state:
        print("Lost in the folds of time...")
        return False

    print("\n" + ASCII_DIAGRAMS.get(name, ""))
    print(state["description"] + "\n")

    if not state["choices"]:
        print("The timeline settles here.")
        return False

    print("Choices:")
    for i, choice in enumerate(state["choices"].keys(), 1):
        print(f"{i}. {choice}")
    return True

def main():
    print("Welcome to the Paradoxical Time Loom.\n")
    current_state = "start"

    while True:
        continue_game = display_state(current_state)
        if not continue_game:
            break

        user_input = input("Your choice (number): ").strip()
        try:
            choice_idx = int(user_input) - 1
            choices = list(TIMELINES[current_state]["choices"].keys())
            if 0 <= choice_idx < len(choices):
                selected = choices[choice_idx]
                current_state = TIMELINES[current_state]["choices"][selected]
            else:
                print("Invalid choice number. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    print("\nThank you for exploring the tangled threads of time.\n")

if __name__ == "__main__":
    main()
