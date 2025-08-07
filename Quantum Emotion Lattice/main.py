import pygame
import numpy as np
from textblob import TextBlob
import random
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Emotion Lattice")

BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 18)

# Map emotions to colors
EMOTION_COLORS = {
    "joy": (255, 215, 0),
    "sadness": (70, 130, 180),
    "anger": (220, 20, 60),
    "fear": (138, 43, 226),
    "surprise": (255, 140, 0),
    "trust": (60, 179, 113),
    "disgust": (139, 69, 19),
    "anticipation": (255, 105, 180),
    "neutral": (200, 200, 200),
}

# Node class representing an emotion in the lattice
class EmotionNode:
    def __init__(self, emotion, pos):
        self.emotion = emotion
        self.pos = np.array(pos, dtype=float)
        self.radius = 20
        self.color = EMOTION_COLORS.get(emotion, EMOTION_COLORS["neutral"])
        self.connections = []
        self.highlight = False

    def draw(self, surface):
        color = tuple(min(255, c + 80) if self.highlight else c for c in self.color)
        pygame.draw.circle(surface, color, self.pos.astype(int), self.radius)
        label = FONT.render(self.emotion, True, (0, 0, 0))
        label_rect = label.get_rect(center=self.pos)
        surface.blit(label, label_rect)

    def is_clicked(self, mouse_pos):
        return np.linalg.norm(self.pos - mouse_pos) <= self.radius

# Lattice managing nodes and connections
class EmotionLattice:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, emotion, pos):
        node = EmotionNode(emotion, pos)
        self.nodes.append(node)
        # Connect the new node to nearby nodes
        for other in self.nodes:
            if other != node:
                dist = np.linalg.norm(node.pos - other.pos)
                if dist < 150:  # threshold for connection
                    self.edges.append((node, other))

    def draw(self, surface):
        # Draw edges
        for n1, n2 in self.edges:
            color = (
                (n1.color[0] + n2.color[0]) // 2,
                (n1.color[1] + n2.color[1]) // 2,
                (n1.color[2] + n2.color[2]) // 2,
            )
            pygame.draw.line(surface, color, n1.pos.astype(int), n2.pos.astype(int), 3)

        # Draw nodes
        for node in self.nodes:
            node.draw(surface)

    def get_node_at_pos(self, pos):
        for node in self.nodes:
            if node.is_clicked(pos):
                return node
        return None

    def toggle_highlight(self, node):
        node.highlight = not node.highlight

def analyze_emotion(text):
    # Basic heuristic to pick predominant emotion using textblob polarity and subjectivity
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Map sentiment to an emotion
    if polarity > 0.3:
        return "joy"
    elif polarity < -0.3:
        return "sadness"
    elif subjectivity > 0.7:
        return "anticipation"
    else:
        return "neutral"

def main():
    clock = pygame.time.Clock()
    input_text = ''
    input_active = True
    lattice = EmotionLattice()
    info_text = "Type an emotion or phrase and press Enter to add nodes."

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
                        # Analyze the input for emotion
                        emotion = analyze_emotion(input_text.strip().lower())
                        # Add node to lattice at random position
                        pos = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 150))
                        lattice.add_node(emotion, pos)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 50:
                        input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = np.array(pygame.mouse.get_pos())
                node = lattice.get_node_at_pos(pos)
                if node:
                    lattice.toggle_highlight(node)

        lattice.draw(screen)

        # Draw input box
        input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_surface = FONT.render("Input emotion/phrase: " + input_text, True, (255, 255, 255))
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Draw info text
        info_surface = FONT.render(info_text, True, (255, 255, 255))
        screen.blit(info_surface, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
