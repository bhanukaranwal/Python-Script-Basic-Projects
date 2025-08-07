import pygame
import numpy as np
import sounddevice as sd
import sys
import random
import math
import threading

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interstice Signal Harvester")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 18)

# Generate ambient sounds based on frequency
def generate_tone(frequency, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32)

class GlitchVisual:
    def __init__(self):
        self.lines = []
        for _ in range(50):
            x_start = random.randint(0, WIDTH)
            y_start = random.randint(0, HEIGHT)
            length = random.randint(20, 100)
            self.lines.append([x_start, y_start, length, random.choice([1, -1])])

    def update(self):
        for line in self.lines:
            line[0] += line[3] * random.randint(1, 3)
            # Wrap around
            if line[0] > WIDTH:
                line[0] = 0
                line[1] = random.randint(0, HEIGHT)
            elif line[0] < 0:
                line[0] = WIDTH
                line[1] = random.randint(0, HEIGHT)

    def draw(self, surface):
        for line in self.lines:
            pygame.draw.line(surface, WHITE, (line[0], line[1]), (line[0] + line[2], line[1]), 1)

class SignalSound:
    def __init__(self, base_freq):
        self.base_freq = base_freq
        self.duration = 0.5
        self.sample_rate = 44100
        self.thread = threading.Thread(target=self.play_loop)
        self.running = True
        self.thread.start()

    def generate_signal(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        # Modulate signal with noise and frequency shift
        freq_shift = random.uniform(-10, 10)
        carrier = np.sin(2 * np.pi * (self.base_freq + freq_shift) * t)
        noise = np.random.normal(0, 0.1, carrier.shape)
        signal = carrier + noise
        signal = signal * 0.3
        return signal.astype(np.float32)

    def play_loop(self):
        while self.running:
            signal = self.generate_signal()
            sd.play(signal, self.sample_rate)
            sd.wait()

    def stop(self):
        self.running = False
        self.thread.join()

def main():
    input_active = True
    input_text = ''
    glitch_visual = None
    signal_sound = None

    instructions = "Describe a liminal space and press Enter to harvest its signal."

    while True:
        dt = pygame.time.Clock().tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if signal_sound:
                    signal_sound.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        seed = sum(ord(c) for c in input_text)
                        random.seed(seed)
                        glitch_visual = GlitchVisual()
                        base_freq = 200 + seed % 800
                        if signal_sound:
                            signal_sound.stop()
                        signal_sound = SignalSound(base_freq)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 50:
                        input_text += event.unicode

        if glitch_visual:
            glitch_visual.update()
            glitch_visual.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render("Liminal space: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw instructions
        instr_surface = font.render(instructions, True, WHITE)
        screen.blit(instr_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
