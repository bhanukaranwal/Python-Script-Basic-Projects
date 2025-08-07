import pygame
import numpy as np
import sounddevice as sd
import datetime
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrono-Sensory Garden")

BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 18)

# Plant class representing a fractal-like growing plant that sways with ambient sound
class Plant:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=float)
        self.size = 20
        self.color = (0, 255, 0)
        self.growth = 0.0  # 0 to 1
        self.sway_angle = 0.0

    def update(self, dt, growth_factor, sway_intensity):
        self.growth = min(1.0, self.growth + growth_factor * dt)
        self.sway_angle += sway_intensity * dt * 5
        self.sway_angle %= 2 * np.pi

    def draw(self, surface):
        # Draw stem
        stem_height = self.size * self.growth * 4
        sway_x = 10 * np.sin(self.sway_angle)
        start_pos = (int(self.pos[0]), int(self.pos[1]))
        end_pos = (int(self.pos[0] + sway_x), int(self.pos[1] - stem_height))
        pygame.draw.line(surface, self.color, start_pos, end_pos, 3)

        # Draw leaves as fractal-like branches
        num_branches = int(3 + 5 * self.growth)
        for i in range(num_branches):
            branch_angle = np.pi / 4 * ((-1) ** i) + sway_x * 0.1
            branch_length = self.size * 0.6 * (1 + 0.5 * np.sin(i + self.sway_angle))
            bx = end_pos[0] + branch_length * np.cos(branch_angle)
            by = end_pos[1] + branch_length * np.sin(branch_angle)
            pygame.draw.line(surface, self.color, end_pos, (bx, by), 2)

def get_ambient_noise_level(duration=0.1, fs=44100):
    # Record ambient sound and compute volume level
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
        volume_norm = np.linalg.norm(recording) / (duration * fs)
        return volume_norm
    except Exception:
        # In case sounddevice is not available, return a default low noise
        return 0.01

def map_time_to_color(hour):
    # Map hour (0-23) to a color gradient from dawn to night
    if 6 <= hour < 12:  # Morning - bright green
        return (0, 255, 100)
    elif 12 <= hour < 18:  # Afternoon - yellow-green
        return (180, 255, 0)
    elif 18 <= hour < 21:  # Evening - orange
        return (255, 140, 0)
    else:  # Night - dark blue-green
        return (0, 50, 80)

def main():
    clock = pygame.time.Clock()
    plants = [Plant((100 + i * 80, HEIGHT - 50)) for i in range(8)]

    input_active = False
    info_text = "Ambient sound controls plant sway. Local time controls growth and color."

    while True:
        dt = clock.tick(30) / 1000.0
        screen.fill(BLACK)

        # Get ambient noise level
        noise_level = get_ambient_noise_level()
        sway_intensity = min(10.0, noise_level * 1000)

        # Get current local hour
        current_hour = datetime.datetime.now().hour

        # Map hour to growth rate and color
        growth_factor = 0.1 if 6 <= current_hour < 22 else 0.02
        plant_color = map_time_to_color(current_hour)

        for plant in plants:
            plant.color = plant_color
            plant.update(dt, growth_factor, sway_intensity)
            plant.draw(screen)

        # Display info text and ambient noise level
        info_surface = font.render(info_text, True, (200, 200, 200))
        screen.blit(info_surface, (10, 10))
        noise_surface = font.render(f"Ambient Noise Level: {noise_level:.3f}", True, (200, 200, 200))
        screen.blit(noise_surface, (10, 40))
        time_surface = font.render(f"Local Hour: {current_hour}", True, (200, 200, 200))
        screen.blit(time_surface, (10, 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
