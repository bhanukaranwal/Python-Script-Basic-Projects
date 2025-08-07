import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Thread Spinner")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Arial", 16)

class ThreadNode:
    def __init__(self, text, pos):
        self.text = text
        self.pos = list(pos)
        self.radius = 20
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.connected = []

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        text_surf = FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        dx = self.pos[0] - mouse_pos[0]
        dy = self.pos[1] - mouse_pos[1]
        return dx * dx + dy * dy <= self.radius * self.radius

def connect_nodes(nodes):
    # Connect each node with at least one other node randomly
    for node in nodes:
        possible = [n for n in nodes if n != node]
        if possible:
            connected_node = random.choice(possible)
            if connected_node not in node.connected:
                node.connected.append(connected_node)
                connected_node.connected.append(node)

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    nodes = []
    info_text = "Enter words or phrases to weave the cosmic thread."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        # Create new node at random position
                        pos = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 100))
                        node = ThreadNode(input_text.strip(), pos)
                        nodes.append(node)
                        connect_nodes(nodes)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 30:
                        input_text += event.unicode

        # Draw connections
        for node in nodes:
            for connected_node in node.connected:
                pygame.draw.line(screen, WHITE, (int(node.pos[0]), int(node.pos[1])), (int(connected_node.pos[0]), int(connected_node.pos[1])), 2)

        # Draw nodes
        for node in nodes:
            node.draw(screen)
            if node.is_hovered(mouse_pos):
                # Highlight node and show text
                highlight_surf = FONT.render(node.text, True, WHITE)
                screen.blit(highlight_surf, (mouse_pos[0] + 10, mouse_pos[1]))

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = FONT.render("Input phrase: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw instructions
        info_surface = FONT.render(info_text, True, WHITE)
        screen.blit(info_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
