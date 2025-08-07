import pygame
import numpy as np
import sounddevice as sd
import sys
import threading
import queue
import math

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aural Dream Cartographer")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

# Queue for audio chunks
audio_queue = queue.Queue()

# Audio parameters
FS = 44100
DURATION = 3  # seconds to record

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(indata.copy())

def record_audio():
    print("Recording audio for {} seconds...".format(DURATION))
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=FS):
        sd.sleep(int(DURATION * 1000))
    print("Recording complete.")

def analyze_audio_data(audio_data):
    audio_flat = audio_data.flatten()
    # Compute pitch by zero crossing rate as simple proxy
    zero_crossings = np.sum(np.abs(np.diff(np.sign(audio_flat)))) / 2
    pitch = zero_crossings / DURATION
    
    # Compute volume as RMS
    volume = np.sqrt(np.mean(audio_flat**2))
    
    return pitch, volume

def generate_terrain_map(pitch, volume):
    # Map pitch and volume to terrain attributes (height, roughness)
    width, height = WIDTH, HEIGHT
    terrain = np.zeros((height, width))
    freq = pitch / 100  # scale pitch for frequency
    amplitude = volume * 50  # scale volume for amplitude
    
    for y in range(height):
        for x in range(width):
            terrain[y][x] = amplitude * math.sin(2 * math.pi * freq * (x / width) + y / 20)
    return terrain

def draw_terrain(surface, terrain):
    height, width = terrain.shape
    for y in range(height):
        for x in range(width):
            val = terrain[y][x]
            color_val = 128 + int(val)
            color_val = max(0, min(255, color_val))
            surface.set_at((x, y), (color_val, color_val, 255 - color_val))

def main():
    running = True
    terrain = None
    info_text = "Press SPACE to record your dream voice."
    recording = False
    pitch, volume = 0, 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not recording:
                    recording = True
                    audio_queue.queue.clear()
                    audio_thread = threading.Thread(target=record_audio)
                    audio_thread.start()

        if recording and audio_queue.qsize() > 0:
            # Collect audio data
            audio_data = []
            while not audio_queue.empty():
                audio_data.append(audio_queue.get())
            if audio_data:
                audio_np = np.concatenate(audio_data)
                pitch, volume = analyze_audio_data(audio_np)
                terrain = generate_terrain_map(pitch, volume)
                recording = False

        if terrain is not None:
            draw_terrain(screen, terrain)

        txt_surface = FONT.render(info_text, True, WHITE)
        screen.blit(txt_surface, (10, HEIGHT - 30))

        if pitch > 0 and volume > 0:
            info2 = f"Pitch: {pitch:.2f}, Volume: {volume:.4f}"
            txt2 = FONT.render(info2, True, WHITE)
            screen.blit(txt2, (10, HEIGHT - 60))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
