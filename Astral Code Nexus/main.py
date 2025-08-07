import pygame
import sys
import ast
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astral Code Nexus")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 16)

class NexusNode:
    def __init__(self, name, node_type, pos):
        self.name = name
        self.node_type = node_type
        self.pos = list(pos)
        self.base_pos = list(pos)
        self.radius = 20 if node_type == "function" else 15
        self.color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255),
        )
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.connections = []

    def update(self, dt):
        self.pulse_phase += dt * 3
        pulse = (math.sin(self.pulse_phase) + 1) / 2  # 0 to 1
        self.radius = 15 + 10 * pulse

    def draw(self, surface):
        # Draw pulsating circle with glow effect
        alpha = int(100 + 155 * (math.sin(self.pulse_phase) + 1) / 2)
        glow_surface = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surface,
            self.color + (alpha,),
            (int(self.radius*2), int(self.radius*2)),
            int(self.radius),
        )
        surface.blit(glow_surface, (int(self.pos[0] - self.radius*2), int(self.pos[1] - self.radius*2)))
        # Draw solid core
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))

        # Draw label (abbreviated)
        label_text = self.name if len(self.name) <= 8 else self.name[:7] + "…"
        label = font.render(label_text, True, WHITE)
        label_rect = label.get_rect(center=(int(self.pos[0]), int(self.pos[1]) - self.radius - 10))
        surface.blit(label, label_rect)

def parse_code_structure(code_text):
    nodes = []
    edges = []
    try:
        tree = ast.parse(code_text)
        node_id = 0
        positions = []

        # Helper to generate node positions in a circle
        def get_pos(i, total):
            angle = 2 * math.pi * i / total
            center = (WIDTH // 2, HEIGHT // 2)
            radius = 200
            return (
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle),
            )

        funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        loops = [n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))]

        total_nodes = len(funcs) + len(loops)
        idx = 0

        # Create function nodes
        for f in funcs:
            pos = get_pos(idx, total_nodes) if total_nodes > 0 else (WIDTH//2, HEIGHT//2)
            nodes.append(NexusNode(f.name, "function", pos))
            idx += 1

        # Create loop nodes
        for l in loops:
            pos = get_pos(idx, total_nodes) if total_nodes > 0 else (WIDTH//2, HEIGHT//2)
            # Name loops generically
            nodes.append(NexusNode("loop", "loop", pos))
            idx += 1

        # Connect nodes sequentially in a circular pattern for visualization
        for i in range(len(nodes)):
            next_i = (i + 1) % len(nodes)
            edges.append((nodes[i], nodes[next_i]))

    except Exception:
        # Return empty if parse error
        pass

    return nodes, edges

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    nodes = []
    edges = []

    instructions = "Input Python code and press Enter to visualize its astral nexus."

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
                        nodes, edges = parse_code_structure(input_text)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 1000:
                        input_text += event.unicode

        # Update and draw edges
        for n1, n2 in edges:
            pygame.draw.line(screen, WHITE, n1.pos, n2.pos, 2)

        # Update and draw nodes
        for node in nodes:
            node.update(dt)
            node.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render("Python code: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw instructions
        instr_surface = font.render(instructions, True, (180, 180, 180))
        screen.blit(instr_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
