import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Void Cartographer's Compass")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

# Landmarks with descriptions
LANDMARKS = [
    "The Spire of Forgotten Light",
    "Echoing Abyss",
    "Shimmering Veil",
    "The Silent Obelisk",
    "Twilight Nexus",
    "The Shattered Echo",
    "Crystalline Rift",
    "The Lost Beacon",
]

class Landmark:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.radius = 30
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def draw(self, surface, offset):
        x, y = self.pos
        screen_pos = (int(x - offset[0]), int(y - offset[1]))
        if 0 <= screen_pos[0] <= WIDTH and 0 <= screen_pos[1] <= HEIGHT:
            pygame.draw.circle(surface, self.color, screen_pos, self.radius)
            text_surf = FONT.render(self.name, True, WHITE)
            surface.blit(text_surf, (screen_pos[0] - text_surf.get_width() // 2, screen_pos[1] + self.radius + 5))

def generate_landmarks(seed, count=10):
    random.seed(seed)
    landmarks = []
    for _ in range(count):
        name = random.choice(LANDMARKS)
        pos = (random.randint(-1000, 1000), random.randint(-1000, 1000))
        landmarks.append(Landmark(name, pos))
    return landmarks

def main():
    clock = pygame.time.Clock()
    offset = [0, 0]
    speed = 300  # pixels per second
    seed = random.randint(0, 100000)
    landmarks = generate_landmarks(seed)

    info_text = f"Exploring the void (Seed: {seed}). Use arrow keys to move."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            offset[0] -= speed * dt
        if keys[pygame.K_RIGHT]:
            offset[0] += speed * dt
        if keys[pygame.K_UP]:
            offset[1] -= speed * dt
        if keys[pygame.K_DOWN]:
            offset[1] += speed * dt
        if keys[pygame.K_r]:
            # Reset exploration with a new seed
            seed = random.randint(0, 100000)
            landmarks = generate_landmarks(seed)
            offset = [0, 0]
            info_text = f"Exploring the void (Seed: {seed}). Use arrow keys to move."

        for landmark in landmarks:
            landmark.draw(screen, offset)

        info_surface = FONT.render(info_text, True, WHITE)
        screen.blit(info_surface, (10, HEIGHT - 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()
