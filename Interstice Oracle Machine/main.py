import random
import pygame
import sys

USE_VISUALS = True

poetic_fragments = [
    "Whispers echo beyond the veil.",
    "Time fractures into hollow streams.",
    "Shadows fold within silent gaps.",
    "Reality blinks through fractured glass.",
    "The space between holds forgotten truths.",
    "Voices drift in perpetual twilight.",
    "Echoes riddle the void's heartbeat.",
    "Fragments dance where worlds collide."
]

glitch_patterns = [
    r"""
    .-'-.
   /|  |\
  ||    ||
  \|    |/
   `-..-'
""",
    r"""
  ##
 ####
##  ##
######
  ##
"""
]

def generate_prophecy():
    lines = random.sample(poetic_fragments, 3)
    prophecy = "\n".join(lines)
    return prophecy

def main():
    if USE_VISUALS:
        pygame.init()
        WIDTH, HEIGHT = 600, 400
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Interstice Oracle Machine")
        font = pygame.font.SysFont('Consolas', 24)
        clock = pygame.time.Clock()
        glitch_index = 0
        glitch_timer = 0

    print("Welcome to the Interstice Oracle Machine.")
    print("Ask your question, or type 'quit' to exit.\n")

    while True:
        question = input("Your question: ").strip()
        if question.lower() in ("quit", "exit"):
            print("The oracle fades back into the void.")
            break
        if not question:
            print("The void awaits a question.")
            continue

        prophecy = generate_prophecy()
        print("\nCryptic prophecy from the interstice:\n")
        print(prophecy + "\n")

        if USE_VISUALS:
            for _ in range(120):  # Display visuals for approx 2 seconds
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                screen.fill((0, 0, 0))
                glitch_timer += clock.tick(60) / 1000.0
                if glitch_timer > 0.3:
                    glitch_index = (glitch_index + 1) % len(glitch_patterns)
                    glitch_timer = 0
                glitch_text = glitch_patterns[glitch_index]
                lines = glitch_text.strip("\n").split("\n")
                y_offset = HEIGHT // 2 - len(lines) * 15
                for i, line in enumerate(lines):
                    line_surface = font.render(line, True, (100, 255, 200))
                    screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, y_offset + i * 30))
                pygame.display.flip()

if __name__ == "__main__":
    main()
