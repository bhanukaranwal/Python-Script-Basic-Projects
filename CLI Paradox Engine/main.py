import random

PARADOX_STATES = [
    {
        "description": "You open the door to find yourself entering.",
        "choices": {
            "Step inside": "mirror_room",
            "Close the door quickly": "end_loop"
        },
        "ascii_art": """
  _______
 |       |
 |  YOU  |
 |_______|
"""
    },
    {
        "description": "A mirror reflects your reflection reflecting endlessly.",
        "choices": {
            "Touch the mirror": "broken_reflection",
            "Look away": "void"
        },
        "ascii_art": """
  |*****|
  |* * *|
  |*****|
"""
    },
    {
        "description": "Your hand reaches out but never quite touches the object.",
        "choices": {
            "Keep reaching": "infinite_reach",
            "Withdraw": "safe_zone"
        },
        "ascii_art": """
   (\_/)
  ( •_•)
  />🖐
"""
    },
    {
        "description": "An infinite loop traps your thoughts, spiraling inward.",
        "choices": {
            "Try to escape": "escape_attempt",
            "Accept the loop": "paradox_end"
        },
        "ascii_art": """
   @@@@@@
  @      @
  @ LOOP @
  @@@@@@@@
"""
    },
    {
        "description": "Time flows backward here, your past selves greet you.",
        "choices": {
            "Join them": "time_merge",
            "Run forward": "forward_walk"
        },
        "ascii_art": """
  <======
  Time Warp
  =======>
"""
    },
    # Terminal or ending states
    {
        "description": "You find yourself outside the paradox, sanity restored.",
        "choices": {},
        "ascii_art": """
   _______
  |       |
  |  END  |
  |_______|
"""
    },
    {
        "description": "Your consciousness collapses into silence.",
        "choices": {},
        "ascii_art": """
   .......
  .       .
  . SILENCE.
  .       .
   .......
"""
    }
]

# Helper to find state by description
def find_state(desc):
    for state in PARADOX_STATES:
        if state['description'] == desc:
            return state
    return None

# Transition map for choices
TRANSITIONS = {
    "You open the door to find yourself entering.": {
        "Step inside": "A mirror reflects your reflection reflecting endlessly.",
        "Close the door quickly": "You find yourself outside the paradox, sanity restored."
    },
    "A mirror reflects your reflection reflecting endlessly.": {
        "Touch the mirror": "Your hand reaches out but never quite touches the object.",
        "Look away": "Your consciousness collapses into silence."
    },
    "Your hand reaches out but never quite touches the object.": {
        "Keep reaching": "An infinite loop traps your thoughts, spiraling inward.",
        "Withdraw": "You find yourself outside the paradox, sanity restored."
    },
    "An infinite loop traps your thoughts, spiraling inward.": {
        "Try to escape": "Time flows backward here, your past selves greet you.",
        "Accept the loop": "Your consciousness collapses into silence."
    },
    "Time flows backward here, your past selves greet you.": {
        "Join them": "You find yourself outside the paradox, sanity restored.",
        "Run forward": "An infinite loop traps your thoughts, spiraling inward."
    }
}

def main():
    print("Welcome to the CLI Paradox Engine.")
    current_desc = "You open the door to find yourself entering."

    while True:
        state = find_state(current_desc)
        if not state:
            print("The paradox folds in on itself. End of line.")
            break

        print("\n" + state["ascii_art"])
        print(state["description"])

        if not state["choices"]:
            print("\nThe paradox concludes.")
            break

        print("\nChoices:")
        for idx, choice in enumerate(state["choices"], 1):
            print(f"{idx}. {choice}")

        try:
            selection = int(input("Choose an option (number): "))
            choices_list = list(state["choices"].keys())
            if 1 <= selection <= len(choices_list):
                chosen = choices_list[selection - 1]
                current_desc = TRANSITIONS[current_desc][chosen]
            else:
                print("Invalid choice number.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
