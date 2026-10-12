"""Create responsive WebP images from the Feedback 3 workshop originals."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/workshop'
OUT.mkdir(parents=True, exist_ok=True)
for number in (13, 36, 44, 76):
    source = ROOT / f'imgs/Feedback-3/TruschJaNid_2022_-{number}.jpg'
    with Image.open(source) as original:
        photo = ImageOps.exif_transpose(original).convert('RGB')
        for width in (480, 800, 1200, 1600):
            resized = photo.resize((width, round(photo.height * width / photo.width)), Image.Resampling.LANCZOS)
            resized.save(OUT / f'workshop-{number}-{width}.webp', quality=85, method=6)
    print(f'Prepared {source.name}')
