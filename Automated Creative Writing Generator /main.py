# Automated Creative Writing Generator — main.py

import random

class CreativeWritingGenerator:
    def __init__(self, seed_text, themes, authors_styles):
        self.seed_text = seed_text
        self.themes = themes
        self.authors_styles = authors_styles

    def generate_poem(self):
        # Simple verse generator using seed, theme, and author style
        verses = []
        for i in range(4):
            line = f"{random.choice(self.themes)} whispers {self.seed_text} in {random.choice(list(self.authors_styles.keys()))}'s style."
            verses.append(line)
        return '\n'.join(verses)

    def generate_story(self):
        # Simple short story generator
        story = f"Once upon a time, {self.seed_text} in a world full of {random.choice(self.themes)}."
        story += f" Inspired by {random.choice(list(self.authors_styles.keys()))}, it unfolds mysteriously."
        return story

if __name__ == '__main__':
    seed_text = "a distant melody"
    themes = ["love", "darkness", "hope", "magic"]
    authors_styles = {
        "Shakespeare": "iambic pentameter",
        "Poe": "gothic and melancholic",
        "Angelou": "empowering and rhythmic"
    }

    generator = CreativeWritingGenerator(seed_text, themes, authors_styles)

    print("Generated Poem:")
    print(generator.generate_poem())

    print("\nGenerated Story:")
    print(generator.generate_story())

# Extensions:
# - Integrate GPT or another LLM for language generation
# - Add genre- and style-switching logic
# - Incorporate character and relationship maps for narrative structure
# - Support collaborative or revision-based workflows
# - Export as TTS audio or e-book format
