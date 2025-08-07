import random
import datetime

# Define possible timeline states and transformations
TIMELINE_STATES = [
    "a dense forest",
    "a bustling futuristic city",
    "a medieval village",
    "a post-apocalyptic wasteland",
    "an underwater metropolis",
    "a floating sky island",
]

# Define possible time glitches descriptions
TIME_GLITCHES = [
    "The air shimmers and ripples as time bends.",
    "Reality flickers, revealing alternate futures.",
    "A strange pulse warps the surroundings.",
    "The ground vibrates with echoes of the past.",
    "An unseen force rearranges the timeline.",
]

class TemporalWorld:
    def __init__(self):
        # Start in a random timeline state
        self.state = random.choice(TIMELINE_STATES)
        self.time = datetime.datetime.now()

    def describe(self):
        desc = f"You are in {self.state}.\n"
        desc += f"Local time: {self.time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        return desc

    def trigger_time_glitch(self):
        glitch_desc = random.choice(TIME_GLITCHES)
        new_state = random.choice(TIMELINE_STATES)
        # Ensure the new state is different
        while new_state == self.state:
            new_state = random.choice(TIMELINE_STATES)
        self.state = new_state
        self.time += datetime.timedelta(minutes=random.randint(1, 5000))
        return glitch_desc

def main():
    world = TemporalWorld()
    print("Welcome to the Temporal Anomaly Simulator.")
    print("Navigate through shifting timelines and explore anomalies.\n")
    print(world.describe())

    while True:
        action = input("Move forward or backward in time? (forward/backward/quit): ").strip().lower()
        if action == 'quit':
            print("Exiting the temporal anomaly. Safe travels!")
            break
        elif action in ('forward', 'backward'):
            # Determine if time glitch occurs
            glitch_chance = 0.4
            if random.random() < glitch_chance:
                glitch = world.trigger_time_glitch()
                print("\n--- TIME GLITCH ---")
                print(glitch)
                print(world.describe())
            else:
                # Normal time movement (small time change)
                delta = datetime.timedelta(minutes=random.randint(1, 60))
                if action == 'forward':
                    world.time += delta
                else:
                    world.time -= delta
                print("\nYou move", action + ".")
                print(world.describe())
        else:
            print("Invalid action. Please input 'forward', 'backward', or 'quit'.")

if __name__ == "__main__":
    main()
