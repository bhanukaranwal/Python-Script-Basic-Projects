import pygame
from PIL import Image, ImageDraw, ImageFilter
import datetime
import sys
import io

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Memory Fossilizer")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 20)

class FossilArtifact:
    def __init__(self, text):
        self.text = text
        self.creation_time = datetime.datetime.now()
        self.weather_stage = 0
        self.max_stage = 5
        self.base_image = self.create_base_image()
        self.weathered_images = [self.base_image]
        self.prepare_weathered_images()
        self.current_layer = 0

    def create_base_image(self):
        # Create a PIL image with crystalline pattern based on text
        img = Image.new('RGBA', (400, 300), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw text multiple times with slight offsets and opacities to create complexity
        for i in range(10):
            x_offset = i * 2
            y_offset = i * 2
            opacity = int(255 * (1 - i * 0.1))
            color = (100, 200, 255, opacity)
            draw.text((50 + x_offset, 100 + y_offset), self.text, fill=color, anchor=None)

        # Apply a blur filter to soften edges like crystalline
        img = img.filter(ImageFilter.GaussianBlur(radius=3))

        return img

    def prepare_weathered_images(self):
        # Prepare different weathered versions by adding noise, cracks, and discoloration
        for stage in range(1, self.max_stage + 1):
            img = self.weathered_images[0].copy()
            draw = ImageDraw.Draw(img)
            # Add "cracks" as random thin lines
            for _ in range(stage * 10):
                x1 = int(400 * pygame.time.get_ticks() % 1)
                y1 = int(300 * pygame.time.get_ticks() % 1)
                x2 = x1 + int(20 * (pygame.time.get_ticks() % 1))
                y2 = y1 + int(5 * (pygame.time.get_ticks() % 1))
                draw.line((x1, y1, x2, y2), fill=(150, 200, 255, 50), width=1)
            # Add discoloration as a transparent orange-ish overlay
            overlay = Image.new('RGBA', img.size, (255, 140, 0, stage * 20))
            img = Image.alpha_composite(img, overlay)

            # Slight blur to simulate wear
            img = img.filter(ImageFilter.GaussianBlur(radius=stage * 0.5))
            self.weathered_images.append(img)

    def update_weather_stage(self):
        # Calculate stage based on elapsed time (every minute moves to next stage)
        elapsed = (datetime.datetime.now() - self.creation_time).total_seconds()
        stage = min(self.max_stage, int(elapsed // 60))
        if stage != self.weather_stage:
            self.weather_stage = stage

    def draw(self, surface):
        self.update_weather_stage()
        img = self.weathered_images[self.weather_stage]

        # Convert PIL image to pygame surface
        mode = img.mode
        size = img.size
        data = img.tobytes()
        py_image = pygame.image.fromstring(data, size, mode).convert_alpha()

        # Allow "excavation" by showing layers when clicked
        y_offset = 50
        for i in range(self.weather_stage + 1):
            alpha = 255 if i == self.current_layer else 100
            layer_img = self.weathered_images[i]
            data = layer_img.tobytes()
            surf = pygame.image.fromstring(data, size, mode).convert_alpha()
            surf.set_alpha(alpha)
            surface.blit(surf, (WIDTH // 2 - size[0] // 2, y_offset + i * 30))

        # Draw input text and instructions
        instr1 = font.render("Memory fossilized at: " + self.creation_time.strftime('%H:%M:%S'), True, WHITE)
        surface.blit(instr1, (10, 10))
        instr2 = font.render("Click scenes to excavate layers", True, WHITE)
        surface.blit(instr2, (10, 40))

    def handle_click(self, pos):
        # Detect which layer clicked based on y position
        y_offset = 50
        size = self.weathered_images[0].size
        x_start = WIDTH // 2 - size[0] // 2
        x_end = x_start + size[0]
        for i in range(self.weather_stage + 1):
            y_start = y_offset + i * 30
            y_end = y_start + size[1] // 10
            if x_start <= pos[0] <= x_end and y_start <= pos[1] <= y_end:
                self.current_layer = i
                break

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    artifact = None

    while True:
        dt = clock.tick(30) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        artifact = FossilArtifact(input_text.strip())
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 30:
                        input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if artifact:
                    artifact.handle_click(event.pos)

        # Draw artifact if available
        if artifact:
            artifact.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render("Enter a memory to fossilize: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
