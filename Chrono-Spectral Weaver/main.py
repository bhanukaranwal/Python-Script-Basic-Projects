import pygame
import numpy as np
import sounddevice as sd
import sys
import math
import threading

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrono-Spectral Weaver")

BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 18)

class SpectralThread:
    def __init__(self, x, max_height):
        self.x = x
        self.max_height = max_height
        self.points = []
        self.color = [np.random.randint(100, 255) for _ in range(3)]
        self.phase = np.random.rand() * 2 * np.pi

    def update(self, spectrum_slice, dt):
        height = np.interp(spectrum_slice, [0, 1], [10, self.max_height])
        self.phase += dt
        y = self.max_height / 2 + math.sin(self.phase) * height / 2
        self.points.append((self.x, y))
        if len(self.points) > 300:
            self.points.pop(0)

    def draw(self, surface):
        if len(self.points) > 1:
            pygame.draw.lines(surface, self.color, False, self.points, 2)

class AudioAnalyzer:
    def __init__(self, fs=44100, duration=5):
        self.fs = fs
        self.duration = duration
        self.recording = None
        self.spectrum = None
        self.recording_complete = False

    def record_audio(self):
        print("Recording audio for {} seconds...".format(self.duration))
        self.recording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=1)
        sd.wait()
        print("Recording complete.")
        self.recording_complete = True
        self.compute_spectrum()

    def compute_spectrum(self):
        audio = self.recording.flatten()
        windowed = audio * np.hanning(len(audio))
        spectrum = np.abs(np.fft.rfft(windowed))
        spectrum = spectrum / np.max(spectrum)
        self.spectrum = spectrum

def main():
    clock = pygame.time.Clock()

    analyzer = AudioAnalyzer()
    recording_thread = threading.Thread(target=analyzer.record_audio)
    recording_thread.start()

    threads = [SpectralThread(x, HEIGHT) for x in np.linspace(0, WIDTH, 50)]

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if analyzer.recording_complete:
            spectrum = analyzer.spectrum
            if spectrum is not None:
                # Update threads with spectrum data
                for i, thread in enumerate(threads):
                    idx = int(i * len(spectrum) / len(threads))
                    thread.update(spectrum[idx], dt)
                    thread.draw(screen)
        else:
            msg = font.render("Recording audio... Please wait.", True, (255, 255, 255))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
