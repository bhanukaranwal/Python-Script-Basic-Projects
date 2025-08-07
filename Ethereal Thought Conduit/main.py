import pygame
import random
import sys
from textblob import TextBlob
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ethereal Thought Conduit")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont('Consolas', 24)
SMALL_FONT = pygame.font.SysFont('Consolas', 16)

GLYPHS = ['∴', '∞', '∷', '∝', '∵', '∑', '∏', '∆', '∇', '∫', '≈', '≡', '⋆', '★', '☆']

class Glyph:
    def __init__(self, char, pos):
        self.char = char
        self.base_pos = pos
        self.pos = list(pos)
        self.size = random.randint(20, 40)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.alpha = 255
        self.angle = random.uniform(0, 360)
        self.angle_speed = random.uniform(-30, 30)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.connected = []
    
    def update(self, dt, sentiment_factor):
        self.angle = (self.angle + self.angle_speed * dt) % 360
        self.pulse_phase += dt * (1 + sentiment_factor * 5)
        pulse = (math.sin(self.pulse_phase) + 1) / 2  # 0 to 1
        self.size = 20 + int(20 * pulse * sentiment_factor)
        self.alpha = int(128 + 127 * pulse * sentiment_factor)
        # Slight positional oscillation around base_pos
        self.pos[0] = self.base_pos[0] + 5 * math.sin(self.pulse_phase * 2)
        self.pos[1] = self.base_pos[1] + 5 * math.cos(self.pulse_phase * 2)

    def draw(self, surface):
        glyph_surface = FONT.render(self.char, True, self.color)
        glyph_surface.set_alpha(self.alpha)
        scaled_surface = pygame.transform.rotozoom(glyph_surface, self.angle, self.size / 30)
        rect = scaled_surface.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(scaled_surface, rect)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    return max(0.1, polarity + 1) / 2  # scale to 0.05 to 1

def create_glyphs(text):
    glyphs = []
    positions = []
    for c in text:
        if c.strip():
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 150)
            positions.append((x, y))
    used_chars = []
    for pos in positions:
        char = random.choice(GLYPHS)
        glyph = Glyph(char, pos)
        glyphs.append(glyph)
    # Randomly connect glyphs to form a flowing stream
    for i in range(len(glyphs) - 1):
        if random.random() < 0.5:
            glyphs[i].connected.append(glyphs[i+1])
            glyphs[i+1].connected.append(glyphs[i])
    return glyphs

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    glyphs = []
    sentiment_factor = 0.5  # default

    instructions = "Type your thoughts and press Enter to channel the conduit."

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
                        sentiment_factor = analyze_sentiment(input_text.strip())
                        glyphs = create_glyphs(input_text.strip())
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 200:
                        input_text += event.unicode

        # Update and draw connections
        for glyph in glyphs:
            for connected_glyph in glyph.connected:
                pygame.draw.line(screen, WHITE, glyph.pos, connected_glyph.pos, 2)

        # Update and draw glyphs
        for glyph in glyphs:
            glyph.update(dt, sentiment_factor)
            glyph.draw(screen)

        # Draw input box and instructions
        input_box = pygame.Rect(10, HEIGHT - 50, WIDTH - 20, 40)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = SMALL_FONT.render("Thoughts: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 10))

        instr_surface = SMALL_FONT.render(instructions, True, WHITE)
        screen.blit(instr_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
