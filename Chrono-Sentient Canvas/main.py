import pygame
import sys
import random
import datetime
from textblob import TextBlob

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrono-Sentient Canvas")

BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 18)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    return polarity, subjectivity

def mood_to_color(polarity):
    # Map polarity to a color gradient from blue (negative) to green (neutral) to red (positive)
    if polarity < 0:
        # negative - shades of blue
        return (int(50 * (1 + polarity)), int(100 * (1 + polarity)), 255)
    else:
        # positive - shades of red
        r = min(255, int(255 * polarity))
        g = int(128 * (1 - polarity))
        b = int(50 * (1 - polarity))
        return (r, g, b)

class Shape:
    def __init__(self, pos, color, size, velocity, shape_type):
        self.pos = list(pos)
        self.color = color
        self.size = size
        self.velocity = list(velocity)
        self.shape_type = shape_type
        self.alpha = 150

    def update(self, dt):
        # Move shape
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        # Bounce off edges
        if self.pos[0] <= 0 or self.pos[0] >= WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.pos[1] <= 0 or self.pos[1] >= HEIGHT:
            self.velocity[1] = -self.velocity[1]

        # Change alpha based on time (pulse effect)
        self.alpha += 100 * dt
        if self.alpha > 255:
            self.alpha = 100

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        c = self.color + (int(self.alpha),)
        if self.shape_type == 'circle':
            pygame.draw.circle(s, c, (self.size, self.size), self.size)
        elif self.shape_type == 'square':
            pygame.draw.rect(s, c, (0, 0, self.size * 2, self.size * 2))
        elif self.shape_type == 'triangle':
            points = [(self.size, 0), (0, self.size * 2), (self.size * 2, self.size * 2)]
            pygame.draw.polygon(s, c, points)
        surface.blit(s, (int(self.pos[0] - self.size), int(self.pos[1] - self.size)))

def create_shapes(polarity, subjectivity, time_factor):
    shapes = []
    count = int(15 + 10 * abs(polarity))
    base_color = mood_to_color(polarity)
    for _ in range(count):
        pos = (random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        size = random.randint(20, 50)
        speed = 50 + 50 * subjectivity
        angle = random.uniform(0, 2 * 3.14159)
        velocity = (speed * time_factor * random.uniform(-1, 1), speed * time_factor * random.uniform(-1, 1))
        shape_type = random.choice(['circle', 'square', 'triangle'])
        # Slightly modify base color based on randomness and time
        color_variation = tuple(
            max(0, min(255, c + random.randint(-50, 50))) for c in base_color
        )
        shapes.append(Shape(pos, color_variation, size, velocity, shape_type))
    return shapes

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    shapes = []
    polarity, subjectivity = 0.0, 0.5
    creation_time = datetime.datetime.now()

    instructions = "Enter your current mood and press Enter to create the canvas."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        # Calculate time factor for evolution (cycles every 60 seconds)
        elapsed = (datetime.datetime.now() - creation_time).total_seconds() % 60
        time_factor = abs((elapsed / 30.0) - 1)  # oscillates 0 to 1 to 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        polarity, subjectivity = analyze_sentiment(input_text.strip())
                        shapes = create_shapes(polarity, subjectivity, time_factor)
                        creation_time = datetime.datetime.now()
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        # Update and draw shapes
        for shape in shapes:
            shape.update(dt)
            shape.draw(screen)

        # Draw input box and instructions
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, (200, 200, 200), input_box, 2)
        input_surface = FONT.render("Mood: " + input_text, True, (200, 200, 200))
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        instructions_surface = FONT.render(instructions, True, (150, 150, 150))
        screen.blit(instructions_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
