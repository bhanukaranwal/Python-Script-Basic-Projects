import pygame
import numpy as np
import sys
import math

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astral Memory Weaver")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STAR_COLORS = [
    (255, 255, 255),
    (255, 215, 0),
    (135, 206, 250),
    (255, 105, 180),
    (173, 255, 47),
]

# Fonts
font = pygame.font.SysFont('Arial', 16)

# Memory class representing a celestial pattern
class Memory:
    def __init__(self, text, pos):
        self.text = text
        self.pos = np.array(pos, dtype=float)
        self.radius = 10
        self.pulse_speed = 2 + len(text) % 5
        self.color = STAR_COLORS[hash(text) % len(STAR_COLORS)]
        self.age = 0
        self.angle = hash(text) % 360
        self.sounds_freq = 200 + (sum(ord(c) for c in text) % 800)

    def update(self, dt):
        self.age += dt
        # Pulsate radius between 8 and 16
        self.radius = 12 + 4 * math.sin(self.age * self.pulse_speed)
        # Rotate position slightly around the center
        angle_rad = math.radians(self.angle + self.age * 20)
        self.pos = np.array([WIDTH/2 + 200 * math.cos(angle_rad), HEIGHT/2 + 150 * math.sin(angle_rad)])

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos.astype(int), int(self.radius))
        # Draw a textual snippet near the circle
        text_surface = font.render(self.text, True, self.color)
        surface.blit(text_surface, (self.pos[0] + int(self.radius) + 5, self.pos[1] - 10))

# Audio simple sine wave generator using pygame.mixer.Sound
def generate_tone(frequency, duration_ms=500, volume=0.1):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_amplitude = 2**15 - 1
    for s in range(n_samples):
        t = float(s) / sample_rate
        val = int(max_amplitude * volume * math.sin(2 * math.pi * frequency * t))
        buf[s][0] = val
        buf[s][1] = val
    sound = pygame.sndarray.make_sound(buf)
    return sound

def main():
    clock = pygame.time.Clock()
    memories = []
    input_text = ''
    input_active = True
    tone_cache = {}

    while True:
        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        memory = Memory(input_text.strip(), (WIDTH/2, HEIGHT/2))
                        memories.append(memory)
                        # Play tone associated with this memory
                        freq = memory.sounds_freq
                        if freq not in tone_cache:
                            tone_cache[freq] = generate_tone(freq)
                        tone_cache[freq].play()
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode

        # Update and draw all memories
        for mem in memories:
            mem.update(dt)
            mem.draw(screen)

        # Draw input box and text
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render("Enter memory: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
