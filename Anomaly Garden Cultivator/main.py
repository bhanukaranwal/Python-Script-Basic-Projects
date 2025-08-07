import pygame
import numpy as np
import datetime
import sys
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anomaly Garden Cultivator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 18)

class AnomalousPlant:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=float)
        self.size = 20
        self.growth = 0.0  # 0 to 1
        self.max_growth = 1.5
        self.pulse_phase = 0.0
        self.branches = []
        self.create_branches()
        self.color = [random.randint(100, 255) for _ in range(3)]

    def create_branches(self):
        # Create fractal branches with angles and lengths
        num_branches = random.randint(3, 5)
        self.branches = []
        base_angle = random.uniform(0, 2*math.pi)
        for i in range(num_branches):
            angle = base_angle + i * (2 * math.pi / num_branches) + random.uniform(-0.3, 0.3)
            length = random.uniform(30, 70)
            self.branches.append((angle, length))

    def update(self, dt):
        # Grow plant up to max growth
        self.growth = min(self.max_growth, self.growth + dt * 0.1)
        # Pulsate branches and core based on time
        self.pulse_phase += dt * 3

    def draw(self, surface):
        x, y = int(self.pos[0]), int(self.pos[1])
        core_radius = int(self.size * self.growth * (1 + 0.3 * math.sin(self.pulse_phase)))
        pygame.draw.circle(surface, self.color, (x, y), core_radius)

        # Draw pulsating fractal branches
        for angle, length in self.branches:
            # Pulsate length
            pulsate_length = length * (0.7 + 0.3 * math.sin(self.pulse_phase * 2 + angle))
            end_x = x + int(pulsate_length * math.cos(angle))
            end_y = y + int(pulsate_length * math.sin(angle))
            branch_color = tuple(min(255, max(0, c + 50)) for c in self.color)
            pygame.draw.line(surface, branch_color, (x, y), (end_x, end_y), 3)
            # Draw secondary fractal branches
            for i in range(2):
                sub_angle = angle + (-1)**i * 0.5
                sub_length = pulsate_length / 3
                sub_end_x = end_x + int(sub_length * math.cos(sub_angle))
                sub_end_y = end_y + int(sub_length * math.sin(sub_angle))
                pygame.draw.line(surface, branch_color, (end_x, end_y), (sub_end_x, sub_end_y), 2)

    def interact(self):
        # On interaction, reset growth and randomize color and branches
        self.growth = 0.2
        self.color = [random.randint(100, 255) for _ in range(3)]
        self.create_branches()

def main():
    clock = pygame.time.Clock()
    plants = [AnomalousPlant((random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))) for _ in range(10)]

    info_text = "Click plants to interact with their anomalous growth."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())
                for plant in plants:
                    if np.linalg.norm(plant.pos - pos) < plant.size * plant.growth * 2:
                        plant.interact()

        # Update and draw plants
        for plant in plants:
            plant.update(dt)
            plant.draw(screen)

        # Draw info text
        info_surface = font.render(info_text, True, WHITE)
        screen.blit(info_surface, (10, HEIGHT - 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()
