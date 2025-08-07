import pygame
import datetime
import requests
import sys
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temporal Glyph Composer")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 16)

def fetch_historical_event(date_str):
    # Use Wikipedia On This Day API or similar for historical data
    url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{date_str}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'events' in data and data['events']:
            event = random.choice(data['events'])
            return event['text']
        else:
            return "No major historical events found."
    except Exception:
        return "Historical event data unavailable."

class Glyph:
    def __init__(self, center):
        self.center = center
        self.time_seed = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        random.seed(self.time_seed)
        self.points = self.generate_points()
        self.angle = 0
        self.rotation_speed = random.uniform(0.01, 0.05)
        self.color = [random.randint(50, 255) for _ in range(3)]

    def generate_points(self):
        points = []
        num_points = 8
        radius = 100
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            fluctuation = random.uniform(0.7, 1.3)
            x = self.center[0] + radius * fluctuation * math.cos(angle)
            y = self.center[1] + radius * fluctuation * math.sin(angle)
            points.append([x, y])
        return points

    def update(self):
        self.angle += self.rotation_speed
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def draw(self, surface):
        # Rotate points
        rotated_points = []
        cx, cy = self.center
        for x, y in self.points:
            dx = x - cx
            dy = y - cy
            rx = dx * math.cos(self.angle) - dy * math.sin(self.angle)
            ry = dx * math.sin(self.angle) + dy * math.cos(self.angle)
            rotated_points.append((int(cx + rx), int(cy + ry)))
        if len(rotated_points) > 1:
            pygame.draw.polygon(surface, self.color, rotated_points, 3)
        # Draw inner lines
        for i in range(len(rotated_points)):
            for j in range(i+2, len(rotated_points)):
                pygame.draw.line(surface, self.color, rotated_points[i], rotated_points[j], 1)

def main():
    clock = pygame.time.Clock()
    glyph = Glyph((WIDTH // 2, HEIGHT // 2))
    input_active = True
    info_text = "Fetching historical event for today..."
    event_text = "Loading..."

    # Fetch historical event for today's date
    today = datetime.datetime.now()
    date_str = f"{today.month}/{today.day}"
    event_text = fetch_historical_event(date_str)

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glyph.update()
        glyph.draw(screen)

        # Display info and event text
        info_surface = font.render(info_text, True, WHITE)
        screen.blit(info_surface, (10, 10))

        event_lines = []
        words = event_text.split()
        line = ""
        max_width = WIDTH - 20
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] < max_width:
                line = test_line
            else:
                event_lines.append(line)
                line = word + " "
        event_lines.append(line)

        y_offset = HEIGHT - 20 * len(event_lines) - 10
        for i, line in enumerate(event_lines):
            text_surf = font.render(line.strip(), True, WHITE)
            screen.blit(text_surf, (10, y_offset + i * 20))

        pygame.display.flip()

if __name__ == "__main__":
    main()
