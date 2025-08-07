import pygame
import numpy as np
import sounddevice as sd
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spectral Anomaly Composer")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

SAMPLE_RATE = 44100
DURATION = 0.1  # seconds for each audio chunk

def generate_tone(frequency, duration=DURATION, sample_rate=SAMPLE_RATE, volume=0.3):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    return (volume * wave).astype(np.float32)

class AnomalyVisualizer:
    def __init__(self):
        self.amplitude = 0
        self.pulse_phase = 0
        self.frequency = 220
        self.radius = 50
        self.color = (255, 255, 255)

    def update(self, amplitude):
        self.amplitude = amplitude
        self.pulse_phase += 0.1
        self.radius = 30 + 70 * min(self.amplitude, 1.0)
        # Change color based on amplitude
        col_val = min(255, int(255 * self.amplitude))
        self.color = (col_val, 255 - col_val, 150)

    def draw(self, surface):
        alpha = int(100 + 155 * min(self.amplitude, 1.0))
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(s, self.color + (alpha,), (WIDTH//2, HEIGHT//2), int(self.radius), 5)
        surface.blit(s, (0, 0))

def audio_callback(indata, frames, time, status):
    global current_amplitude
    if status:
        print(status, file=sys.stderr)
    volume_norm = np.linalg.norm(indata) / frames
    # Detect anomaly as sudden spikes in amplitude
    current_amplitude = min(volume_norm * 10, 1.0)

def main():
    global current_amplitude
    current_amplitude = 0

    pygame.display.set_caption("Spectral Anomaly Composer")

    visualizer = AnomalyVisualizer()

    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE)
    stream.start()

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stream.stop()
                pygame.quit()
                sys.exit()

        visualizer.update(current_amplitude)
        visualizer.draw(screen)

        # Optional: play tone based on amplitude
        if current_amplitude > 0.1:
            freq = 220 + 300 * current_amplitude
            tone = generate_tone(freq)
            sd.play(tone, SAMPLE_RATE, blocking=False)

        info_surface = FONT.render("Speak or make sounds to reveal spectral anomalies.", True, WHITE)
        screen.blit(info_surface, (10, HEIGHT - 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()
