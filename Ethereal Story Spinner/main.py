import random

# Story nodes with branching narrative and poetic text
STORY_NODES = {
    "start": {
        "text": "You awaken under a twilight sky, stars whispering secrets.",
        "choices": {
            "walk towards the light": "light_path",
            "venture into the shadow": "shadow_path",
            "sit and gaze at stars": "star_gaze"
        }
    },
    "light_path": {
        "text": "Light blooms around you, petals of dawn unfurling in the ether.",
        "choices": {
            "touch the petals": "petal_touch",
            "follow the glowing trail": "glowing_trail"
        }
    },
    "shadow_path": {
        "text": "The shadow whispers a star's name, and the night deepens.",
        "choices": {
            "call the name": "call_name",
            "hide in the darkness": "hide_darkness"
        }
    },
    "star_gaze": {
        "text": "Constellations flicker into life, mapping your destiny.",
        "choices": {
            "trace the brightest star": "trace_star",
            "close your eyes": "close_eyes"
        }
    },
    "petal_touch": {
        "text": "A burst of colors floods your vision, dreams weaving anew.",
        "choices": {}
    },
    "glowing_trail": {
        "text": "You follow the trail to a cosmic garden where time flows backwards.",
        "choices": {}
    },
    "call_name": {
        "text": "Echoes respond, and a new path unfurls in the dark.",
        "choices": {}
    },
    "hide_darkness": {
        "text": "Safe in the shadow, you hear the heartbeat of the void.",
        "choices": {}
    },
    "trace_star": {
        "text": "Following the star, you unlock forgotten memories of light.",
        "choices": {}
    },
    "close_eyes": {
        "text": "In darkness, visions sparkle and the story folds inward.",
        "choices": {}
    }
}

def display_constellation(path):
    # Visualize the story path as a simple constellation map (text-based)
    stars = ['*', '+', '✦', '✧', '✩', '✪', '✫']
    print("\nConstellation Map:")
    for depth, node in enumerate(path):
        star = random.choice(stars)
        indent = " " * (depth * 4)
        print(f"{indent}{star} {node}")

def main():
    print("Welcome to the Ethereal Story Spinner.")
    current_node = "start"
    story_path = [current_node]

    while True:
        node_data = STORY_NODES[current_node]
        print("\n" + node_data["text"])
        if not node_data["choices"]:
            print("\nThe story fades here. Thank you for spinning the tale.")
            display_constellation(story_path)
            break

        print("\nChoose:")
        for i, choice in enumerate(node_data["choices"], 1):
            print(f"{i}. {choice}")

        try:
            user_input = input("Your choice (number): ").strip()
            choice_index = int(user_input) - 1
            choices_list = list(node_data["choices"].keys())
            if 0 <= choice_index < len(choices_list):
                selected_choice = choices_list[choice_index]
                current_node = node_data["choices"][selected_choice]
                story_path.append(current_node)
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Enter a valid number.")

if __name__ == "__main__":
    main()
