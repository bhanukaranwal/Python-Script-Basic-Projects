import pygame
import numpy as np
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interstellar Signal Decoder")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Consolas', 18)

def generate_noise_signal(length, freq):
    t = np.linspace(0, 1, length)
    # Alien signal as noisy sine waves with random phases
    signal = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2 * t + np.pi/4)
    noise = np.random.normal(0, 0.3, length)
    return signal + noise

def draw_waveform(surface, data, pos, size, color):
    points = []
    x, y = pos
    w, h = size
    length = len(data)
    for i in range(length):
        px = x + (i / length) * w
        py = y + h / 2 + data[i] * h / 2
        points.append((px, py))
    pygame.draw.lines(surface, color, False, points, 2)

def main():
    clock = pygame.time.Clock()
    length = 800
    base_freq = 5
    noise_level = 0.5
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    base_freq += 1
                elif event.key == pygame.K_DOWN:
                    base_freq = max(1, base_freq - 1)
                elif event.key == pygame.K_RIGHT:
                    noise_level = min(1.0, noise_level + 0.1)
                elif event.key == pygame.K_LEFT:
                    noise_level = max(0.0, noise_level - 0.1)

        # Generate alien signal
        t = np.linspace(0, 1, length)
        signal = np.sin(2 * np.pi * base_freq * t) + 0.5 * np.sin(2 * np.pi * base_freq * 2 * t + np.pi / 4)
        noise = np.random.normal(0, noise_level, length)
        combined_signal = signal + noise

        # Draw waveform
        draw_waveform(screen, combined_signal, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), WHITE)

        # Instructions
        instructions = [
            "Use UP/DOWN arrows to change frequency",
            "Use LEFT/RIGHT arrows to adjust noise level",
            f"Frequency: {base_freq} Hz",
            f"Noise level: {noise_level:.2f}"
        ]

        for i, line in enumerate(instructions):
            text_surf = FONT.render(line, True, WHITE)
            screen.blit(text_surf, (10, 10 + i * 20))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
