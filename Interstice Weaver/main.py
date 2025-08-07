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
pygame.display.set_caption("Interstice Weaver")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('Arial', 18)

# Generate ambient sounds based on frequency
def generate_tone(frequency, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32)

class AbstractShape:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=float)
        self.radius = random.randint(20, 50)
        self.color = (
            random.randint(100, 200),
            random.randint(100, 200),
            random.randint(100, 200),
            100,
        )
        self.speed = np.random.uniform(-20, 20, 2)
        self.angle = 0
        self.angular_speed = random.uniform(-30, 30)

    def update(self, dt):
        self.pos += self.speed * dt
        self.angle = (self.angle + self.angular_speed * dt) % 360

        # Bounce from edges
        if self.pos[0] - self.radius < 0 or self.pos[0] + self.radius > WIDTH:
            self.speed[0] *= -1
        if self.pos[1] - self.radius < 0 or self.pos[1] + self.radius > HEIGHT:
            self.speed[1] *= -1

    def draw(self, surface):
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, self.color, (self.radius, self.radius), self.radius)
        rotated = pygame.transform.rotate(s, self.angle)
        rect = rotated.get_rect(center=self.pos)
        surface.blit(rotated, rect.topleft)

class AmbientSound:
    def __init__(self, base_freq):
        self.base_freq = base_freq
        self.duration = 1.0
        self.sample_rate = 44100
        self.thread = threading.Thread(target=self.play_loop)
        self.running = True
        self.thread.start()

    def play_loop(self):
        while self.running:
            tone = generate_tone(self.base_freq, self.duration, self.sample_rate)
            sd.play(tone, self.sample_rate)
            sd.wait()
            # Slightly vary the frequency for organic effect
            self.base_freq += random.uniform(-1, 1)
            if self.base_freq < 100:
                self.base_freq = 100
            elif self.base_freq > 1000:
                self.base_freq = 1000

    def stop(self):
        self.running = False
        self.thread.join()

def main():
    input_active = True
    input_text = ''
    shapes = []
    ambient_sound = None

    while True:
        dt = pygame.time.Clock().tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if ambient_sound:
                    ambient_sound.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        # Generate shapes and ambient sound based on input_text
                        random.seed(sum(ord(c) for c in input_text))
                        shapes = [AbstractShape((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 150))) for _ in range(15)]
                        freq_base = 200 + sum(ord(c) for c in input_text) % 800
                        if ambient_sound:
                            ambient_sound.stop()
                        ambient_sound = AmbientSound(freq_base)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 50:
                        input_text += event.unicode

        for shape in shapes:
            shape.update(dt)
            shape.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render("Describe a liminal space: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
