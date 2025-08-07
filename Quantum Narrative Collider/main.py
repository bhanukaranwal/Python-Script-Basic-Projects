import random
import pygame
import sys
import threading
import time

# Optional: Visual particle effects for narrative collisions
USE_VISUALS = True

WIDTH, HEIGHT = 800, 600

# Text-based story fragments for recombination
FRAGMENTS = [
    "In the shadow of the ancient stars, ",
    "a whisper carries through the void. ",
    "Time fractures into endless echoes, ",
    "where futures bleed into pasts. ",
    "The collision births a new universe, ",
    "woven from tangled dreams and shattered hopes. ",
    "Silent voices speak in cryptic riddles, ",
    "leading the lost through labyrinthine realms. ",
    "A spark ignites within the cosmic web, ",
    "setting forth the dance of creation and decay. "
]

# Particle class for optional visual effect
class Particle:
    def __init__(self):
        self.pos = [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.size = random.randint(2, 5)
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # Bounce on screen edges
        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.vel[0] = -self.vel[0]
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.vel[1] = -self.vel[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)

def visual_thread(stop_flag):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quantum Narrative Collider - Visuals")
    clock = pygame.time.Clock()

    particles = [Particle() for _ in range(100)]

    while not stop_flag[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_flag[0] = True
                break
        screen.fill((0,0,0))
        for p in particles:
            p.move()
            p.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def generate_collided_narrative(prompts):
    # Fragment input prompts and shuffle to form chaotic narrative
    fragments = []
    for prompt in prompts:
        words = prompt.split()
        # Create small fragments of 2-4 words
        i = 0
        while i < len(words):
            length = random.randint(2,4)
            frag = " ".join(words[i:i+length])
            fragments.append(frag)
            i += length
    random.shuffle(fragments)
    return " ... ".join(fragments)

def main():
    print("Welcome to the Quantum Narrative Collider.")
    print("Input story prompts. Enter a blank line to generate the narrative.")
    user_prompts = []

    stop_flag = [False]

    # Start visuals in a separate thread if enabled
    if USE_VISUALS:
        t = threading.Thread(target=visual_thread, args=(stop_flag,))
        t.start()

    try:
        while True:
            line = input("Enter a prompt: ").strip()
            if line == "":
                break
            user_prompts.append(line)
        if not user_prompts:
            print("No prompts entered. Exiting.")
            stop_flag[0] = True
            if USE_VISUALS:
                t.join()
            return
        narrative = generate_collided_narrative(user_prompts)
        print("\n--- Collided Narrative ---\n")
        for part in narrative.split(" ... "):
            print(part)
            time.sleep(0.5)  # Dramatic pacing
        print("\n--- End of Narrative ---")
    finally:
        stop_flag[0] = True
        if USE_VISUALS:
            t.join()

if __name__ == "__main__":
    main()
