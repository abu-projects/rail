"""Prepare web images from the client feedback originals. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/feedback'
OUT.mkdir(exist_ok=True)
for path in sorted((ROOT / 'imgs/Feedback/social').glob('*.png')):
    image = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    image.thumbnail((1600, 1600))
    image.save(OUT / f'social-{path.stem.split("-")[-1]}.webp', quality=88)
for path in sorted((ROOT / 'imgs/Feedback/action').glob('*.jpg')):
    original = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    for width in (480, 800, 1200):
        image = original.copy()
        image.thumbnail((width, round(original.height * width / original.width)))
        image.save(OUT / f'{path.stem}-{width}.webp', quality=85)
print('Prepared 4 social photographs and 11 responsive action photographs.')
