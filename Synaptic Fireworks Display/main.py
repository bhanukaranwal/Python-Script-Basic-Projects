import pygame
import numpy as np
import sys
import random
import math

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Synaptic Fireworks Display")

BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 20)

# Particle class representing synaptic sparks
class Spark:
    def __init__(self, pos, angle, speed, color):
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array([math.cos(angle), math.sin(angle)]) * speed
        self.color = color
        self.life = 1.0  # life from 1 down to 0

    def update(self, dt):
        self.pos += self.velocity * dt * 300  # scale speed
        self.velocity *= 0.98  # simulate drag
        self.life -= dt * 0.8  # fade life
        if self.life < 0:
            self.life = 0

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * self.life)
            col = (*self.color, alpha)
            s = max(1, int(5 * self.life))
            surf = pygame.Surface((s*2, s*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, col, (s, s), s)
            surface.blit(surf, (int(self.pos[0])-s, int(self.pos[1])-s))

def phrase_to_color_and_count(phrase):
    # Use the sum of character codes to pick color and spark count
    val = sum(ord(c) for c in phrase)
    base_hue = val % 360
    count = 15 + (val % 20)
    # Convert hue to RGB roughly
    c = pygame.Color(0)
    c.hsla = (base_hue, 90, 60, 100)
    return c, count

def create_firework(center, phrase):
    color, count = phrase_to_color_and_count(phrase)
    sparks = []
    for i in range(count):
        angle = (2 * math.pi / count) * i + random.uniform(-0.2, 0.2)
        speed = random.uniform(2, 5)
        sparks.append(Spark(center, angle, speed, color))
    return sparks

def main():
    clock = pygame.time.Clock()
    sparks = []
    input_text = ''
    input_active = True

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
                        # Create firework at center based on input phrase
                        new_sparks = create_firework((WIDTH/2, HEIGHT/2), input_text.strip())
                        sparks.extend(new_sparks)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 30:
                        input_text += event.unicode

        # Update and draw sparks
        for spark in sparks[:]:
            spark.update(dt)
            spark.draw(screen)
            if spark.life <= 0:
                sparks.remove(spark)

        # Draw input box and text
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_surface = FONT.render("Enter thought: " + input_text, True, (255, 255, 255))
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
