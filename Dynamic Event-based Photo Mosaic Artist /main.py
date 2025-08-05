# Dynamic Event-based Photo Mosaic Artist — main.py

from PIL import Image
import os
import math

class PhotoMosaicArtist:
    def __init__(self, images_folder, tile_size=50):
        self.images_folder = images_folder
        self.tile_size = tile_size
        self.tiles = []

    def load_images(self):
        # Load all images from the folder and resize to tile size
        for filename in os.listdir(self.images_folder):
            if filename.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(self.images_folder, filename)
                img = Image.open(img_path).resize((self.tile_size, self.tile_size))
                self.tiles.append(img)

    def create_mosaic(self, output_path='mosaic_output.jpg'):
        if not self.tiles:
            raise ValueError('No images loaded for mosaic.')

        cols = int(math.sqrt(len(self.tiles)))
        rows = math.ceil(len(self.tiles) / cols)

        mosaic_img = Image.new('RGB', (cols * self.tile_size, rows * self.tile_size))

        for i, tile in enumerate(self.tiles):
            x = (i % cols) * self.tile_size
            y = (i // cols) * self.tile_size
            mosaic_img.paste(tile, (x, y))

        mosaic_img.save(output_path)
        print(f'Mosaic created and saved to {output_path}')

if __name__ == '__main__':
    folder_path = 'photos/'  # Folder containing input photos

    artist = PhotoMosaicArtist(folder_path, tile_size=50)
    artist.load_images()

    try:
        artist.create_mosaic()
    except Exception as e:
        print(f'Error creating mosaic: {e}')

# Next steps:
# - Apply style transfer or color matching to tiles
# - Generate mosaics targeted at event themes (wedding, vacation, etc.)
# - Add high-res and zoomable UI
# - Create time-lapse videos of mosaic assembly
# - Use image metadata for chronological or content-aware arrangement
