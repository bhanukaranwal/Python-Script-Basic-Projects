import pygame
import sys
import ast
import random
import math

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ethereal Code Alchemist")

BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 18)

class CodePotion:
    def __init__(self, code_text):
        self.code_text = code_text
        self.tree = None
        self.elements = {'functions': 0, 'loops': 0, 'assignments': 0, 'ifs': 0}
        self.parse_code()
        self.particles = []
        self.create_particles()

    def parse_code(self):
        try:
            self.tree = ast.parse(self.code_text)
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    self.elements['functions'] += 1
                elif isinstance(node, (ast.For, ast.While)):
                    self.elements['loops'] += 1
                elif isinstance(node, ast.Assign):
                    self.elements['assignments'] += 1
                elif isinstance(node, ast.If):
                    self.elements['ifs'] += 1
        except Exception:
            # Ignore parse errors
            pass

    def create_particles(self):
        total_effects = sum(self.elements.values()) or 1
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(50, 150)
            speed = random.uniform(0.5, 2.0)
            type_choice = random.choices(
                ['functions', 'loops', 'assignments', 'ifs'],
                weights=[self.elements['functions'], self.elements['loops'], self.elements['assignments'], self.elements['ifs']],
                k=1
            )[0]
            color = {
                'functions': (200, 100, 255),
                'loops': (100, 200, 255),
                'assignments': (255, 200, 100),
                'ifs': (150, 255, 150),
            }[type_choice]
            self.particles.append({
                'angle': angle,
                'radius': radius,
                'speed': speed,
                'color': color,
                'type': type_choice,
                'size': random.randint(3, 7)
            })

    def update_and_draw(self, surface, dt):
        center = (WIDTH // 2, HEIGHT // 2)
        for p in self.particles:
            p['angle'] += p['speed'] * dt
            x = center[0] + p['radius'] * math.cos(p['angle'])
            y = center[1] + p['radius'] * math.sin(p['angle'])
            pygame.draw.circle(surface, p['color'], (int(x), int(y)), p['size'])

def main():
    clock = pygame.time.Clock()
    input_text = ''
    potion = None
    input_active = True
    info_text = "Enter Python code snippet and press Enter to brew your potion."

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
                        potion = CodePotion(input_text)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 200:
                        input_text += event.unicode

        if potion:
            potion.update_and_draw(screen, dt)
        else:
            msg = font.render(info_text, True, (200, 200, 200))
            screen.blit(msg, (20, HEIGHT // 2 - 20))

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_surface = font.render("Code snippet: " + input_text, True, (255, 255, 255))
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
