import pygame
import random
import sys
from textblob import TextBlob

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echoes of Parallel Selves")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 18)

# Simple avatar representation as circles with color and size
class Avatar:
    def __init__(self, traits, pos):
        self.traits = traits
        self.pos = pos
        self.base_color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.radius = 40 + traits['confidence'] * 10
        self.dialog = self.generate_dialog()
        self.dialog_index = 0
        self.dialog_timer = 0

    def generate_dialog(self):
        base_lines = [
            "I am a reflection, shaped by choices untaken.",
            "Echoing through time and space, my story twists.",
            "What you see is but one of many possible selves.",
            "In the parallel, my dreams are your reality.",
        ]
        # Add trait-based poetic lines
        if self.traits['optimism'] > 0.5:
            base_lines.append("Hope guides my path beyond the veil.")
        else:
            base_lines.append("Shadows linger in my silent thoughts.")

        if self.traits['curiosity'] > 0.5:
            base_lines.append("I wander endlessly, seeking forgotten truths.")
        else:
            base_lines.append("I rest where certainty calms the mind.")

        random.shuffle(base_lines)
        return base_lines

    def update(self, dt):
        self.dialog_timer += dt
        if self.dialog_timer > 5:
            self.dialog_timer = 0
            self.dialog_index = (self.dialog_index + 1) % len(self.dialog)

    def draw(self, surface):
        pygame.draw.circle(surface, self.base_color, self.pos, int(self.radius))
        # Draw dialog box
        dialog_surface = FONT.render(self.dialog[self.dialog_index], True, WHITE)
        surface.blit(dialog_surface, (self.pos[0] - dialog_surface.get_width() // 2, self.pos[1] + self.radius + 10))

def analyze_bio(bio_text):
    # Analyze sentiment and extract simple traits
    blob = TextBlob(bio_text)
    polarity = blob.sentiment.polarity  # range -1 to 1
    subjectivity = blob.sentiment.subjectivity  # range 0 to 1

    # Map to traits between 0 and 1
    confidence = max(0, min(1, (polarity + 1) / 2))
    optimism = max(0, min(1, (polarity + 0.5)))
    curiosity = max(0, min(1, subjectivity))

    return {'confidence': confidence, 'optimism': optimism, 'curiosity': curiosity}

def generate_parallel_personas(bio_text, count=4):
    base_traits = analyze_bio(bio_text)
    personas = []
    for i in range(count):
        # Modify traits slightly to simulate parallel selves variation
        traits = {
            'confidence': max(0, min(1, base_traits['confidence'] + random.uniform(-0.3, 0.3))),
            'optimism': max(0, min(1, base_traits['optimism'] + random.uniform(-0.3, 0.3))),
            'curiosity': max(0, min(1, base_traits['curiosity'] + random.uniform(-0.3, 0.3))),
        }
        x = 150 + i * 150
        y = HEIGHT // 2
        personas.append(Avatar(traits, (x, y)))
    return personas

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    personas = []

    while True:
        dt = clock.tick(30) / 1000.0
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        personas = generate_parallel_personas(input_text.strip())
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 100:
                        input_text += event.unicode

        # Draw personas
        for persona in personas:
            persona.update(dt)
            persona.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        input_surface = FONT.render("Enter a short bio: " + input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()
