import pygame
import random
import sys
from PIL import ImageFont

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Narrative Nebula Generator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Arial", 16)

# Star-like particle
class StarParticle:
    def __init__(self, pos, story_fragment):
        self.pos = list(pos)
        self.story_fragment = story_fragment
        self.radius = random.randint(3, 6)
        self.brightness = random.uniform(0.5, 1.0)
        self.brightness_dir = 1
        self.hovered = False

    def update(self, dt):
        # Animate brightness pulse
        self.brightness += self.brightness_dir * dt * 0.5
        if self.brightness > 1:
            self.brightness = 1
            self.brightness_dir = -1
        elif self.brightness < 0.5:
            self.brightness = 0.5
            self.brightness_dir = 1

    def draw(self, surface):
        color_val = int(255 * self.brightness)
        color = (color_val, color_val, 255)
        pygame.draw.circle(surface, color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        if self.hovered:
            # Draw the story fragment nearby
            text_surf = FONT.render(self.story_fragment, True, WHITE)
            surface.blit(text_surf, (self.pos[0] + 10, self.pos[1] - 10))

    def is_hovered(self, mouse_pos):
        dx = self.pos[0] - mouse_pos[0]
        dy = self.pos[1] - mouse_pos[1]
        return (dx*dx + dy*dy) <= (self.radius + 5)**2

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    particles = []

    info_text = "Enter story fragments, press Enter to add; mouse hover stars to read."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        # Add a star particle at random position with this fragment
                        pos = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 100))
                        particles.append(StarParticle(pos, input_text.strip()))
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        mouse_pos = pygame.mouse.get_pos()
        for particle in particles:
            particle.hovered = particle.is_hovered(mouse_pos)
            particle.update(dt)
            particle.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = FONT.render("Input story fragment: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw info text
        info_surf = FONT.render(info_text, True, WHITE)
        screen.blit(info_surf, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
