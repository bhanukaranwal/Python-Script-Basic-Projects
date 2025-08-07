import pygame
import sys
import math
from PIL import Image, ImageDraw

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eidetic Memory Prism")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

def create_prism_surface(size, colors):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2
    radius = size // 3

    for i, color in enumerate(colors):
        angle = i * (360 / len(colors))
        x = center + radius * math.cos(math.radians(angle))
        y = center + radius * math.sin(math.radians(angle))
        draw.polygon([
            (center, center),
            (center + radius * math.cos(math.radians(angle - 10)), center + radius * math.sin(math.radians(angle - 10))),
            (x, y),
            (center + radius * math.cos(math.radians(angle + 10)), center + radius * math.sin(math.radians(angle + 10)))
        ], fill=color+(150,), outline=None)
    return img

def pil_to_pygame(image):
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

class Prism:
    def __init__(self, memory):
        self.size = 300
        base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        # Modify colors based on memory length and content
        mod = (sum(ord(c) for c in memory) % 100) / 100.0
        self.colors = [(int(r * mod + (1 - mod) * 255), int(g * mod + (1 - mod) * 255), int(b * mod + (1 - mod) * 255)) for (r, g, b) in base_colors]
        self.angle = 0
        self.image = create_prism_surface(self.size, self.colors)
        self.pygame_image = pil_to_pygame(self.image)
        self.pos = (WIDTH // 2, HEIGHT // 2 - 50)

    def update(self, dt, mouse_pos):
        self.angle += 30 * dt
        self.angle %= 360
        # Refract effect based on mouse x and y
        offset_x = int((mouse_pos[0] - WIDTH//2) / 10)
        offset_y = int((mouse_pos[1] - HEIGHT//2) / 10)
        rotated = pygame.transform.rotozoom(self.pygame_image, self.angle, 1.0)
        # Shift image by offset to simulate refraction
        self.render_pos = (self.pos[0] - rotated.get_width() // 2 + offset_x, self.pos[1] - rotated.get_height() // 2 + offset_y)
        self.rotated_image = rotated

    def draw(self, surface):
        surface.blit(self.rotated_image, self.render_pos)

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    prism = None
    instructions = "Enter a memory and press Enter to create an Eidetic Memory Prism."

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
                        prism = Prism(input_text.strip())
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        if prism:
            prism.update(dt, mouse_pos)
            prism.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = FONT.render("Memory: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw instructions
        instr_surface = FONT.render(instructions, True, (180, 180, 180))
        screen.blit(instr_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
