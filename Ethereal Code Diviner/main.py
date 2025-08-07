import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ethereal Code Diviner")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont('Consolas', 18)
POETIC_PHRASES = [
    "The future whispers in shadows.",
    "Symbols align beyond sight.",
    "Echoes weave the unseen path.",
    "Destiny dances with coded runes.",
    "Patterns dissolve into mystery.",
    "The loop unwinds silently.",
    "Obscure truths unfold in darkness.",
    "Chants of forgotten algorithms.",
    "Celestial scripts shape fate.",
    "Silent vectors navigate the void."
]

GLYPH_CHARS = ['ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚱ', 'ᚲ', 'ᚷ', 'ᚹ', 'ᚺ', 'ᚾ', 'ᛁ', 'ᛃ', 'ᛇ', 'ᛈ', 'ᛉ']

class RuneGlyph:
    def __init__(self, pos):
        self.pos = pos
        self.char = random.choice(GLYPH_CHARS)
        self.angle = random.uniform(0, 360)
        self.angle_speed = random.uniform(-30, 30)  # degrees per second
        self.size = random.randint(24, 48)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.alpha = 255
        self.alpha_direction = -60  # fade out speed

    def update(self, dt):
        self.angle = (self.angle + self.angle_speed * dt) % 360
        self.alpha += self.alpha_direction * dt
        if self.alpha <= 0:
            self.alpha = 255
        elif self.alpha >= 255:
            self.alpha = 255

    def draw(self, surface):
        glyph_surface = FONT.render(self.char, True, self.color)
        glyph_surface.set_alpha(int(self.alpha))
        # Rotate glyph
        rotated_surface = pygame.transform.rotozoom(glyph_surface, self.angle, self.size / 36)
        rect = rotated_surface.get_rect(center=self.pos)
        surface.blit(rotated_surface, rect.topleft)

def generate_poetic_response(question):
    # Create a seed based on question for reproducibility
    seed = sum(ord(c) for c in question)
    random.seed(seed)
    lines = random.sample(POETIC_PHRASES, 3)
    return lines

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    glyphs = []
    poetic_response = []

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
                        # Generate glyphs and poetic response
                        glyphs = [RuneGlyph((random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 200))) for _ in range(20)]
                        poetic_response = generate_poetic_response(input_text.strip())
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        # Draw and update glyphs
        for glyph in glyphs:
            glyph.update(dt)
            glyph.draw(screen)

        # Draw the poetic response
        y_start = HEIGHT - 150
        for i, line in enumerate(poetic_response):
            text_surface = FONT.render(line, True, WHITE)
            screen.blit(text_surface, (20, y_start + i * 30))

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = FONT.render("Ask your question: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
