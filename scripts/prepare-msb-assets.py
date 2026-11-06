"""Prepare the approved November 2026 MsB gallery photos. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'imgs/MSB-Zusatzfotos-2026-11-06'
FILES = (
    'IMG-20240103-WA0000.jpg',
    'IMG_20240213_210520.jpg',
    'grand rallye vtt transverdon 2025 fullattack j2-112.jpg',
    'grand rallye vtt transverdon 2025 fullattack j5-215.jpg',
    'signal-2026-08-24-07-43-19-245-3.jpg',
)

for index, filename in enumerate(FILES, 1):
    with Image.open(SOURCE / filename) as source:
        image = ImageOps.exif_transpose(source).convert('RGB')
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        image.save(ROOT / f'assets/models/muetterschwandenberg-extra-{index:02}.webp',
                   quality=85, method=6)
print('Prepared five MsB gallery photographs; cover unchanged.')
