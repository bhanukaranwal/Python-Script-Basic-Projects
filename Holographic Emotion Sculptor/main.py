import pygame
import sys
import math
from textblob import TextBlob
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Holographic Emotion Sculptor")

BLACK = (0, 0, 0)
font = pygame.font.SysFont('Arial', 20)

# Map basic sentiments to colors
EMOTION_COLORS = {
    'positive': (0, 255, 255),
    'neutral': (255, 255, 255),
    'negative': (255, 100, 100),
}

class Hologram:
    def __init__(self, emotion_word):
        self.emotion_word = emotion_word
        self.sentiment = self.analyze_sentiment(emotion_word)
        self.color = EMOTION_COLORS.get(self.sentiment, (200, 200, 200))
        self.angle = 0
        self.radius = 100
        self.position = (WIDTH // 2, HEIGHT // 2)
        self.points = self.generate_points()
        self.rotation_speed = random.uniform(0.2, 1.0)

    def analyze_sentiment(self, word):
        analysis = TextBlob(word)
        if analysis.sentiment.polarity > 0.1:
            return 'positive'
        elif analysis.sentiment.polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'

    def generate_points(self):
        # Generate points to form an abstract shape based on length and sentiment
        num_points = max(5, len(self.emotion_word) * 2)
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            variance = random.uniform(0.7, 1.3)
            r = self.radius * variance
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            points.append([x, y])
        return points

    def update(self, dt):
        self.angle += self.rotation_speed * dt
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def draw(self, surface):
        # Rotate points
        rotated_points = []
        for x, y in self.points:
            rx = x * math.cos(self.angle) - y * math.sin(self.angle)
            ry = x * math.sin(self.angle) + y * math.cos(self.angle)
            rotated_points.append((int(self.position[0] + rx), int(self.position[1] + ry)))

        # Draw lines connecting points
        if len(rotated_points) > 1:
            pygame.draw.polygon(surface, self.color, rotated_points, 2)

    def interact(self):
        # On interaction, change color and rotation speed randomly
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )
        self.rotation_speed = random.uniform(-2.0, 2.0)

def main():
    clock = pygame.time.Clock()
    holograms = []
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
                        hologram = Hologram(input_text.strip())
                        holograms.append(hologram)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for hol in holograms:
                    # Simple proximity check to the center hologram position
                    if math.dist(pos, hol.position) < hol.radius + 20:
                        hol.interact()

        for hol in holograms:
            hol.update(dt)
            hol.draw(screen)

        # Draw input box and instructions
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_surface = font.render("Enter an emotion keyword: " + input_text, True, (255, 255, 255))
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
