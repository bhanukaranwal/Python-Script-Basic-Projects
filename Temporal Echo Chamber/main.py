import random
import pygame
import sys

# Optional pygame visualization toggle
USE_VISUALS = True

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temporal Echo Chamber")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont("Consolas", 20)

# Distortion functions
def reverse_words(text):
    return " ".join(word[::-1] for word in text.split())

def glitch_text(text, intensity=0.3):
    GLITCH_CHARS = "!@#$%^&*()_+-=[]{};:,.<>?/~`"
    result = []
    for c in text:
        if random.random() < intensity and c.isalpha():
            result.append(random.choice(GLITCH_CHARS))
        else:
            result.append(c)
    return "".join(result)

class VisualEcho:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.alpha = 255
        self.surface = FONT.render(text, True, WHITE)
        self.surface.set_alpha(self.alpha)

    def update(self):
        self.alpha -= 3
        if self.alpha < 0:
            self.alpha = 0
        self.surface.set_alpha(self.alpha)

    def draw(self, surface):
        surface.blit(self.surface, self.pos)

def main():
    clock = pygame.time.Clock()
    input_text = ""
    output_layers = []
    visual_echoes = []

    info_text = "Type text and press Enter. Echoes distort with time. Press ESC to quit."

    while True:
        dt = clock.tick(60) / 1000.0
        if USE_VISUALS:
            screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if input_text.strip():
                        # Generate layered distortions
                        base = input_text.strip()
                        layers = [base]
                        # Progressive distortions
                        for i in range(1, 5):
                            distorted = glitch_text(reverse_words(layers[-1]), intensity=0.1 * i)
                            layers.append(distorted)
                        output_layers = layers
                        if USE_VISUALS:
                            visual_echoes.clear()
                            y_start = 150
                            for i, layer in enumerate(output_layers):
                                pos = (50, y_start + i * 40)
                                visual_echoes.append(VisualEcho(layer, pos))
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        if USE_VISUALS:
            # Update and draw visual echoes
            for echo in visual_echoes[:]:
                echo.update()
                if echo.alpha == 0:
                    visual_echoes.remove(echo)
                else:
                    echo.draw(screen)

            # Draw input box
            input_box = pygame.Rect(10, HEIGHT - 50, WIDTH - 20, 40)
            pygame.draw.rect(screen, WHITE, input_box, 2)
            input_surface = FONT.render(input_text, True, WHITE)
            screen.blit(input_surface, (input_box.x + 10, input_box.y + 8))

            # Draw info
            info_surface = FONT.render(info_text, True, WHITE)
            screen.blit(info_surface, (10, 10))

            pygame.display.flip()

        else:
            # CLI mode: print echoes to console with delay
            if output_layers:
                for layer in output_layers:
                    print(layer)
                output_layers = []

if __name__ == "__main__":
    main()
