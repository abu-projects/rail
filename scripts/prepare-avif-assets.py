"""Generate smaller AVIF alternatives from originals; keep WebP fallbacks.

Requires Pillow with AVIF support. Run only when source photographs change.
The deployment build needs no image processing dependencies.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/home'
manifest = json.loads((OUT / 'sources.json').read_text())


def prepare(entry):
    name, info = entry
    before = after = 0
    with Image.open(ROOT / info['source']) as source:
        original = ImageOps.exif_transpose(source).convert('RGB')
        for width in info['widths']:
            resized = original.resize((width, round(original.height * width / original.width)), Image.Resampling.LANCZOS)
            target = OUT / f'{name}-{width}.avif'
            resized.save(target, quality=65, speed=6)
            before += (OUT / f'{name}-{width}.webp').stat().st_size
            after += target.stat().st_size
    return before, after


with ThreadPoolExecutor(max_workers=4) as pool:
    totals = list(pool.map(prepare, manifest.items()))
before, after = map(sum, zip(*totals))
print(f'AVIF: {before:,} -> {after:,} bytes ({100 * (1 - after / before):.1f}% smaller than WebP).')
