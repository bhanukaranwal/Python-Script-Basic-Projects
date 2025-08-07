import pygame
import random
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echoes of Forgotten Data")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GLITCH_COLORS = [(255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255)]

font = pygame.font.SysFont('Consolas', 20)

# Fragment class representing pieces of lost data
class Fragment:
    def __init__(self, text, pos):
        self.text = text
        self.full_text = text
        self.pos = list(pos)
        self.age = 0
        self.revealed = False
        self.color = random.choice(GLITCH_COLORS)
        self.glitch_intensity = random.randint(1, 3)
        self.visible_text = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in text)

    def update(self, dt):
        self.age += dt
        if not self.revealed:
            # Glitch effect: randomly change some letters to simulate decay
            glitched = list(self.visible_text)
            for _ in range(self.glitch_intensity):
                idx = random.randint(0, len(glitched)-1)
                glitched[idx] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            self.visible_text = ''.join(glitched)

    def draw(self, surface):
        text_surface = font.render(self.visible_text if not self.revealed else self.full_text, True, self.color)
        surface.blit(text_surface, self.pos)

    def is_clicked(self, mouse_pos):
        text_surface = font.render(self.visible_text if not self.revealed else self.full_text, True, self.color)
        rect = text_surface.get_rect(topleft=self.pos)
        return rect.collidepoint(mouse_pos)

    def reveal(self):
        self.revealed = True
        self.color = WHITE

def main():
    clock = pygame.time.Clock()
    fragments = []
    sample_texts = [
        "RELIC", "DATA", "LOST", "BINARY", "MEMORY", "CODE", "ARCHIVE", "FRAGMENT", "GHOST", "ECHO"
    ]

    # Randomly scatter fragments on the screen
    for text in sample_texts:
        x = random.randint(50, WIDTH - 150)
        y = random.randint(50, HEIGHT - 50)
        fragments.append(Fragment(text, (x, y)))

    running = True
    while running:
        dt = clock.tick(30) / 1000
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for frag in fragments:
                    if frag.is_clicked(event.pos) and not frag.revealed:
                        frag.reveal()

        for frag in fragments:
            frag.update(dt)
            frag.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
