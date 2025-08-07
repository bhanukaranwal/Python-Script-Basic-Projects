import pygame
import random
import sys
from textblob import TextBlob

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Whisper Compiler")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont('Consolas', 24)
SMALL_FONT = pygame.font.SysFont('Consolas', 16)

# Fictional cosmic glyphs (Unicode runes, symbols)
COSMIC_GLYPHS = [
    '✦', '✧', '✩', '✪', '✫', '⚝', '⚛', '☥', '☬', '☯',
    '☸', '☣', '☢', '☮', '☾', '☽', '♆', '☿', '♁', '♃'
]

def analyze_text(text):
    # Basic sentiment analysis for pitch and tempo mapping
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    return polarity, subjectivity

class CosmicGlyph:
    def __init__(self, char, pos):
        self.char = char
        self.pos = list(pos)
        self.base_pos = list(pos)
        self.color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )
        self.size = random.randint(20, 48)
        self.angle = random.uniform(0, 360)
        self.angular_velocity = random.uniform(-60, 60)
        self.alpha = 255
        self.alpha_direction = -100

    def update(self, dt):
        self.angle = (self.angle + self.angular_velocity * dt) % 360
        self.alpha += self.alpha_direction * dt
        if self.alpha <= 50:
            self.alpha = 50
            self.alpha_direction = 100
        elif self.alpha >= 255:
            self.alpha = 255
            self.alpha_direction = -100
        # Slight positional oscillation
        self.pos[0] = self.base_pos[0] + 5 * random.uniform(-1, 1)
        self.pos[1] = self.base_pos[1] + 5 * random.uniform(-1, 1)

    def draw(self, surface):
        glyph_surface = FONT.render(self.char, True, self.color)
        glyph_surface.set_alpha(int(self.alpha))
        rotated_surface = pygame.transform.rotozoom(glyph_surface, self.angle, self.size / 36)
        rect = rotated_surface.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(rotated_surface, rect.topleft)

def generate_cosmic_script(text):
    # Map characters of the text into cosmic glyphs randomly
    script = []
    for ch in text:
        glyph_char = random.choice(COSMIC_GLYPHS)
        script.append(glyph_char)
    return script

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    glyphs = []
    polarity, subjectivity = 0.0, 0.5

    instructions = "Input your thoughts and press Enter to compile cosmic whispers."

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
                        polarity, subjectivity = analyze_text(input_text.strip())
                        script = generate_cosmic_script(input_text.strip())
                        # Spread glyphs over the center area
                        glyphs.clear()
                        for i, glyph_char in enumerate(script):
                            x = WIDTH // 2 + (i % 10) * 40 - 200
                            y = HEIGHT // 2 + (i // 10) * 50 - 100
                            glyphs.append(CosmicGlyph(glyph_char, (x, y)))
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        for glyph in glyphs:
            glyph.update(dt)
            glyph.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 50, WIDTH - 20, 40)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = SMALL_FONT.render("Thoughts: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 10))

        # Draw instructions
        instr_surface = SMALL_FONT.render(instructions, True, WHITE)
        screen.blit(instr_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
