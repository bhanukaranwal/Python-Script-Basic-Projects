import pygame
import numpy as np
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anomaly Nexus Simulator")

BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 18)

class NexusNode:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=float)
        self.radius = 25
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.anomaly_active = False
        self.anomaly_type = None
        self.anomaly_timer = 0

    def trigger_anomaly(self):
        self.anomaly_active = True
        self.anomaly_type = random.choice(['invert_gravity', 'color_bleed', 'pulse_wave', 'glitch_shift'])
        self.anomaly_timer = 0

    def update(self, dt):
        if self.anomaly_active:
            self.anomaly_timer += dt
            if self.anomaly_timer > 5:
                self.anomaly_active = False
                self.anomaly_type = None

    def draw(self, surface):
        if self.anomaly_active:
            if self.anomaly_type == 'invert_gravity':
                color = (255, 255, 255)
                pygame.draw.circle(surface, color, self.pos.astype(int), self.radius + 5, 3)
            elif self.anomaly_type == 'color_bleed':
                # Bleeding colors effect
                for i in range(3):
                    offset = i * 5
                    col = list(self.color)
                    col[i] = min(255, col[i] + 100)
                    pygame.draw.circle(surface, col, (int(self.pos[0]) + offset, int(self.pos[1])), self.radius)
            elif self.anomaly_type == 'pulse_wave':
                pulse_radius = self.radius + int(10 * np.sin(self.anomaly_timer * 10))
                pygame.draw.circle(surface, self.color, self.pos.astype(int), pulse_radius, 2)
            elif self.anomaly_type == 'glitch_shift':
                offset_x = int(5 * np.sin(self.anomaly_timer * 20))
                offset_y = int(5 * np.cos(self.anomaly_timer * 15))
                pygame.draw.circle(surface, self.color, (int(self.pos[0]) + offset_x, int(self.pos[1]) + offset_y), self.radius)
        else:
            pygame.draw.circle(surface, self.color, self.pos.astype(int), self.radius)

def main():
    clock = pygame.time.Clock()
    nodes = []
    cols = 8
    rows = 6
    margin_x = WIDTH // (cols + 1)
    margin_y = HEIGHT // (rows + 1)

    for row in range(rows):
        for col in range(cols):
            pos = ((col + 1) * margin_x, (row + 1) * margin_y)
            nodes.append(NexusNode(pos))

    info_text = "Click nodes to trigger anomalies. Watch the nexus shift and pulse."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = np.array(pygame.mouse.get_pos())
                for node in nodes:
                    if np.linalg.norm(node.pos - mouse_pos) <= node.radius:
                        node.trigger_anomaly()

        for node in nodes:
            node.update(dt)
            node.draw(screen)

        info_surface = FONT.render(info_text, True, (200, 200, 200))
        screen.blit(info_surface, (10, HEIGHT - 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()
