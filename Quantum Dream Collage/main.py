from PIL import Image, ImageDraw
import numpy as np
import random

WIDTH, HEIGHT = 800, 600
NUM_CELLS = 6  # number of cells horizontally and vertically

# Quantum-inspired states for each cell
class QuantumCell:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.state = random.randint(0, 4)  # states 0 to 4
        self.collapsed = False
        self.color_palette = [
            (255, 0, 150),
            (0, 255, 200),
            (255, 255, 0),
            (120, 0, 255),
            (0, 150, 255),
        ]

    def evolve_state(self):
        if not self.collapsed:
            # Randomly shift state
            shift = random.choice([-1, 0, 1])
            self.state = (self.state + shift) % len(self.color_palette)

    def collapse(self):
        self.collapsed = True

    def draw(self, draw_obj):
        x, y = self.pos
        sz = self.size
        base_color = self.color_palette[self.state]
        # Create a gradient fill for dreamlike look
        for i in range(sz):
            fill_color = (
                int(base_color[0] * (i / sz)),
                int(base_color[1] * (i / sz)),
                int(base_color[2] * (i / sz)),
            )
            # Draw horizontal lines to create texture gradient
            draw_obj.line([(x, y + i), (x + sz, y + i)], fill=fill_color)

def main():
    img = Image.new('RGB', (WIDTH, HEIGHT), (10, 10, 10))
    draw_obj = ImageDraw.Draw(img)
    cell_size = WIDTH // NUM_CELLS

    # Initialize grid of quantum cells
    grid = []
    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS):
            pos = (col * cell_size, row * cell_size)
            cell = QuantumCell(pos, cell_size)
            grid.append(cell)

    iterations = 0
    max_iterations = 100

    while iterations < max_iterations:
        # Evolve states and draw current image
        img = Image.new('RGB', (WIDTH, HEIGHT), (10, 10, 10))
        draw_obj = ImageDraw.Draw(img)
        for cell in grid:
            if not cell.collapsed:
                cell.evolve_state()
            cell.draw(draw_obj)

        img.show()

        # Ask user for cells to collapse by coordinate input (row,col)
        user_input = input("Enter cells to collapse as 'row,col' (or 'quit' to end): ")
        if user_input.strip().lower() == 'quit':
            break
        try:
            row_str, col_str = user_input.split(',')
            r, c = int(row_str), int(col_str)
            idx = r * NUM_CELLS + c
            if 0 <= idx < len(grid):
                grid[idx].collapse()
            else:
                print("Invalid cell coordinates.")
        except Exception:
            print("Invalid input format. Use 'row,col'.")

        iterations += 1

    print("Quantum Dream Collage complete. Close the image window to exit.")

if __name__ == "__main__":
    main()
