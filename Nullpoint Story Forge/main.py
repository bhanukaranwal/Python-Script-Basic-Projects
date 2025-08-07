import random
import pygame
import sys

USE_VISUALS = True

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nullpoint Story Forge")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

class Particle:
    def __init__(self):
        self.pos = [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.size = random.randint(2, 5)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # Bounce off edges
        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.vel[0] = -self.vel[0]
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.vel[1] = -self.vel[1]

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)

def generate_nullpoint_story(seeds):
    fragments = []
    for seed in seeds:
        words = seed.split()
        # Create small random fragments
        i = 0
        while i < len(words):
            length = random.randint(1, 3)
            frag = " ".join(words[i:i+length])
            fragments.append(frag)
            i += length
    random.shuffle(fragments)
    # Spiral into surreal chaos by recombining fragments
    story = ""
    for f in fragments:
        story += f + " ... "
    return story.strip(" ... ")

def main():
    if USE_VISUALS:
        clock = pygame.time.Clock()
        particles = [Particle() for _ in range(100)]

    print("Welcome to the Nullpoint Story Forge.")
    print("Enter story seeds line by line. Submit an empty line to generate the nullpoint narrative.")

    seeds = []
    while True:
        line = input("Story seed: ").strip()
        if line == "":
            break
        seeds.append(line)

    if not seeds:
        print("No story seeds entered. Exiting.")
        return

    narrative = generate_nullpoint_story(seeds)

    print("\n--- Nullpoint Narrative ---\n")
    for part in narrative.split(" ... "):
        print(part)
    print("\n--- End of Narrative ---\n")

    # Optional visualization
    if USE_VISUALS:
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for p in particles:
                p.move()
                p.draw(screen)

            pygame.display.flip()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
