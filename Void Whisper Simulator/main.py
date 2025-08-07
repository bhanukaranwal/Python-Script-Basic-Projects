import pygame
import random
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Void Whisper Simulator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Consolas', 24)
small_font = pygame.font.SysFont('Consolas', 16)

# Glitch text characters
GLITCH_CHARS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*")

class VoidEntity:
    def __init__(self):
        self.history = []
        self.response = ""
        self.glitch_timer = 0
        self.glitch_intensity = 0

    def generate_response(self, message):
        base_responses = [
            "…beyond the silence…",
            "echoes ripple through the void…",
            "fragments of forgotten whispers…",
            "the abyss listens…",
            "shadows form cryptic patterns…",
            "whispers fade like dying stars…",
            "signals distort and shift…",
            "the void speaks in riddles…"
        ]
        # Response evolves with message length and content
        length_factor = min(len(message) / 50, 1.0)
        content_factor = sum(ord(c) for c in message) % 100 / 100.0

        response_index = int((length_factor + content_factor) * (len(base_responses) - 1))
        self.response = base_responses[response_index]
        self.glitch_intensity = int(length_factor * 10) + 1

    def draw_response(self, surface, dt):
        self.glitch_timer += dt
        if self.glitch_timer > 0.1:
            self.glitch_timer = 0
            # Glitch the response text by randomly replacing characters
            glitched_text = list(self.response)
            for _ in range(self.glitch_intensity):
                idx = random.randint(0, len(glitched_text) - 1)
                glitched_text[idx] = random.choice(GLITCH_CHARS)
            self.glitched_response = "".join(glitched_text)

        # Flicker effect with random offset
        x = random.randint(50, WIDTH - 400)
        y = random.randint(50, HEIGHT - 100)
        text_surface = font.render(self.glitched_response, True, WHITE)
        surface.blit(text_surface, (x, y))

        # Draw abstract shapes around text
        for _ in range(self.glitch_intensity * 2):
            circle_x = x + random.randint(-30, text_surface.get_width() + 30)
            circle_y = y + random.randint(-20, 50)
            radius = random.randint(3, 8)
            alpha = random.randint(50, 150)
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, alpha), (radius, radius), radius)
            surface.blit(s, (circle_x, circle_y))

def main():
    clock = pygame.time.Clock()
    void_entity = VoidEntity()
    input_text = ''
    input_active = True

    instructions = [
        "Type your message to the void and press Enter.",
        "Watch the void's cryptic response evolve.",
        "Press ESC to quit."
    ]

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        # Draw instructions
        for i, line in enumerate(instructions):
            instr_surf = small_font.render(line, True, WHITE)
            screen.blit(instr_surf, (10, 10 + i*20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        void_entity.generate_response(input_text.strip())
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        # Draw user input box
        input_box = pygame.Rect(10, HEIGHT - 50, WIDTH - 20, 40)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render(input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 5))

        # Draw void entity response
        if void_entity.response:
            void_entity.draw_response(screen, dt)

        pygame.display.flip()

if __name__ == "__main__":
    main()
