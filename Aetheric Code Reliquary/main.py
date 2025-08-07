import pygame
import sys
import ast
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aetheric Code Reliquary")

BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 18)

class Reliquary:
    def __init__(self, code_text):
        self.code_text = code_text
        self.tree = None
        self.elements = {'functions': 0, 'classes': 0, 'loops': 0, 'conditionals': 0}
        self.parse_code()
        self.angle = 0
        self.rotation_speed = random.uniform(0.01, 0.05)
        self.color = [random.randint(100, 255) for _ in range(3)]
        self.pulse_phase = 0

    def parse_code(self):
        try:
            self.tree = ast.parse(self.code_text)
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    self.elements['functions'] += 1
                elif isinstance(node, ast.ClassDef):
                    self.elements['classes'] += 1
                elif isinstance(node, (ast.For, ast.While)):
                    self.elements['loops'] += 1
                elif isinstance(node, ast.If):
                    self.elements['conditionals'] += 1
        except Exception:
            pass

    def update(self, dt):
        self.angle = (self.angle + self.rotation_speed * dt) % (2 * math.pi)
        self.pulse_phase += dt * 5

    def draw(self, surface):
        center = (WIDTH // 2, HEIGHT // 2)
        num_rings = max(1, sum(self.elements.values()))
        max_radius = 200
        radius_step = max_radius / num_rings if num_rings > 0 else max_radius

        for i, (element, count) in enumerate(self.elements.items()):
            for c in range(count):
                radius = radius_step * (i + 1) + 10 * math.sin(self.pulse_phase + c)
                alpha = int(150 + 100 * math.sin(self.pulse_phase + c))
                color = (
                    min(255, max(0, self.color[0])),
                    min(255, max(0, self.color[1])),
                    min(255, max(0, self.color[2])),
                    alpha
                )
                points = []
                num_points = 30 + c * 5
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points + self.angle + c
                    fluctuation = 0.3 * math.sin(self.pulse_phase * 3 + j)
                    r = radius * (1 + fluctuation)
                    x = center[0] + r * math.cos(angle)
                    y = center[1] + r * math.sin(angle)
                    points.append((int(x), int(y)))
                s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(s, color, points, 3)
                surface.blit(s, (0, 0))

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    reliquary = None
    instructions = "Input your Python code and press Enter to summon the reliquary."

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
                        reliquary = Reliquary(input_text)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 500:
                        input_text += event.unicode

        if reliquary:
            reliquary.update(dt)
            reliquary.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, (200, 200, 200), input_box, 2)
        input_surface = font.render("Python code: " + input_text, True, (200, 200, 200))
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw instructions
        instructions_surface = font.render(instructions, True, (150, 150, 150))
        screen.blit(instructions_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
