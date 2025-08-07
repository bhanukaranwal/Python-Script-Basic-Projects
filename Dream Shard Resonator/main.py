import pygame
import numpy as np
import sounddevice as sd
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dream Shard Resonator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

SAMPLE_RATE = 44100
DURATION = 0.5  # seconds

def generate_tone(frequency, duration=DURATION, sample_rate=SAMPLE_RATE, volume=0.2):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    return (volume * wave).astype(np.float32)

class Resonator:
    def __init__(self, dream_text):
        self.dream_text = dream_text
        self.base_freq = 220 + sum(ord(c) for c in dream_text) % 440
        self.phase = 0
        self.amplitude = 100
        self.time = 0

    def play_tone(self, freq):
        tone = generate_tone(freq)
        sd.play(tone, SAMPLE_RATE, blocking=False)

    def update(self, dt, input_factor=1.0):
        self.time += dt
        # Oscillate amplitude and frequency based on time and input factor
        self.amplitude = 50 + 50 * math.sin(self.time * 2 * input_factor)
        current_freq = self.base_freq + self.amplitude / 2
        self.play_tone(current_freq)

    def draw(self, surface, mouse_x):
        center_y = HEIGHT // 2
        num_points = 200
        width = WIDTH
        points = []

        # Frequency modulation based on mouse_x
        freq_mod = 0.01 + mouse_x / width * 0.05

        for i in range(num_points):
            x = i * width / num_points
            y = center_y + self.amplitude * math.sin(2 * math.pi * freq_mod * i + self.time * 5)
            points.append((int(x), int(y)))

        pygame.draw.lines(surface, WHITE, False, points, 3)

def main():
    clock = pygame.time.Clock()
    input_text = ''
    resonator = None
    input_active = True
    info_text = "Type a dream snippet and press Enter to hear its resonance."

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)
        mouse_x, _ = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sd.stop()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        resonator = Resonator(input_text.strip())
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 50:
                        input_text += event.unicode

        if resonator:
            resonator.update(dt, input_factor=mouse_x / WIDTH)
            resonator.draw(screen, mouse_x)
        else:
            msg = FONT.render(info_text, True, WHITE)
            screen.blit(msg, (20, HEIGHT // 2 - 20))

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = FONT.render("Enter dream snippet: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
