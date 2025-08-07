from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

WIDTH, HEIGHT = 800, 600

def generate_noise_background(width, height):
    # Generate a noise-based abstract background using random colors and shapes
    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    for _ in range(500):
        x0 = random.randint(0, width)
        y0 = random.randint(0, height)
        x1 = x0 + random.randint(10, 50)
        y1 = y0 + random.randint(10, 50)
        color = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )
        shape_type = random.choice(['ellipse', 'rectangle'])
        if shape_type == 'ellipse':
            draw.ellipse([x0, y0, x1, y1], fill=color, outline=None)
        else:
            draw.rectangle([x0, y0, x1, y1], fill=color, outline=None)
    
    # Slight blur for dreamy effect
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    return img

def generate_cryptic_text(draw, width, height):
    # Cryptic postcard messages
    messages = [
        "Greetings from the Void of Echoes",
        "Wish you were here, across dimensions",
        "Parallel dreams whisper to you",
        "Beneath alien skies, we wander",
        "Echoes of forgotten stars",
        "Lost in the cosmic tides",
        "Between time and space, we meet",
    ]
    msg = random.choice(messages)
    
    # Select random font size and style (use default font as fallback)
    font_size = random.randint(24, 36)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(msg, font=font)
    x = (width - text_width) // 2 + random.randint(-20, 20)
    y = height - text_height - 30 + random.randint(-10, 10)
    
    # Draw text shadow
    shadow_color = (0, 0, 0, 150)
    draw.text((x+2, y+2), msg, font=font, fill=shadow_color)
    # Draw main text with random color
    main_color = (
        random.randint(150, 255),
        random.randint(150, 255),
        random.randint(150, 255),
    )
    draw.text((x, y), msg, font=font, fill=main_color)
    return msg

def main():
    img = generate_noise_background(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(img)
    msg = generate_cryptic_text(draw, WIDTH, HEIGHT)

    # Save the image
    output_filename = "interdimensional_postcard.png"
    img.save(output_filename)
    print(f"Postcard generated and saved as {output_filename}")
    print(f"Message: {msg}")

if __name__ == "__main__":
    main()
