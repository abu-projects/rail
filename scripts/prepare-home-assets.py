"""Prepare homepage derivatives. Originals under imgs/ are never modified."""
from pathlib import Path
import json
import urllib.request
import zipfile
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'home'
OUT.mkdir(parents=True, exist_ok=True)
sources = {
    'hero-lineup': ('Home/Rail_2025__LineUp_-59.jpg', [800, 1200, 1600, 2000]),
    'hero-detail': ('Home/Rail_2025__LineUp_-86.jpg', [800, 1200, 1600, 2000]),
    'hero-lopper': ('Home/Lopper.jpg', [800, 1200, 1600, 2000]),
    'hero-mobile': ('Home/Rail_2025__LineUp_-84.jpg', [480, 800]),
    'hero-detail-mobile': ('Home/Rail_2025__LineUp_-89.jpg', [480, 800]),
    'hero-lopper-mobile': ('Home/Rail_2025__LineUp_-77.jpg', [480, 800]),
    'muetterschwandenberg': ('Rubrik Modelle/Modell Mutterschwandenberg Fully.jpg', [480, 800, 1200]),
    'truischjanid': ('Rubrik Modelle/Modell Truise Enduro Hardtail.jpg', [480, 800, 1200]),
    'wichelsee': ('Rubrik Modelle/Modell Wichselsee Gravel.jpg', [480, 800, 1200]),
    'lopper': ('Rubrik Modelle/Modell Lopper Fully.jpg', [480, 800, 1200]),
    'workshop': ('Rubrik Werkstatt/TruschJaNid_2022_-100.jpg', [800, 1200, 1600]),
    'workshop-detail': ('Rubrik Werkstatt/TruschJaNid_2022_-8.jpg', [480, 800]),
}
about_dir = next(p for p in (ROOT / 'imgs').iterdir() if 'mich' in p.name)
sources['samuel'] = (str((about_dir / 'Rail_2025__LineUp_-90.jpg').relative_to(ROOT / 'imgs')), [480, 800, 1200])
manifest = {}
for name, (source, widths) in sources.items():
    with Image.open(ROOT / 'imgs' / source) as original:
        original = ImageOps.exif_transpose(original).convert('RGB')
        manifest[name] = {'source': 'imgs/' + source, 'size': original.size, 'widths': widths}
        for width in widths:
            size = (width, round(original.height * width / original.width))
            original.resize(size, Image.Resampling.LANCZOS).save(OUT / f'{name}-{width}.webp', quality=84, method=6)

# Use the actual supplied model artwork embedded in the client's layout.
with zipfile.ZipFile(ROOT / 'Layout Website Sam.docx') as doc:
    for name, number in [('muetterschwandenberg', 3), ('truischjanid', 5), ('wichelsee', 7), ('lopper', 9)]:
        (OUT / f'{name}-wordmark.png').write_bytes(doc.read(f'word/media/image{number}.png'))

fonts = ROOT / 'assets' / 'fonts'
fonts.mkdir(exist_ok=True)
font_sources = {
    'barlow-regular': 'https://fonts.gstatic.com/s/barlow/v13/7cHpv4kjgoGqM7E_DMs5ynghnQ.woff2',
    'barlow-medium': 'https://fonts.gstatic.com/s/barlow/v13/7cHqv4kjgoGqM7E3_-gs51ostz0rdg.woff2',
    'barlow-semibold': 'https://fonts.gstatic.com/s/barlow/v13/7cHqv4kjgoGqM7E30-8s51ostz0rdg.woff2',
    'fjalla-one': 'https://fonts.gstatic.com/s/fjallaone/v16/Yq6R-LCAWCX3-6Ky7FAFrOF6kjouQb4.woff2',
}
for name, url in font_sources.items():
    (fonts / f'{name}.woff2').write_bytes(urllib.request.urlopen(url).read())
for family in ['barlow', 'fjallaone']:
    url = f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/OFL.txt'
    (fonts / f'{family}-OFL.txt').write_bytes(urllib.request.urlopen(url).read())
(OUT / 'sources.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
print(f'Prepared {len(sources)} photographs, four wordmarks and four local fonts.')
