"""Build the current bilingual site for Cloudflare Pages (stdlib only)."""

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
PAGES = (
    "index.html", "modelle.html", "werkstatt.html", "ueber-mich.html",
    "kontakt.html", "impressum.html", "datenschutz.html", "404.html",
)

subprocess.run([sys.executable, str(ROOT / "scripts/build-site.py")], cwd=ROOT, check=True)
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir()
for name in (*PAGES, "home.css", "home.js", "rail.svg"):
    shutil.copy2(ROOT / name, OUTPUT / name)
for name in ("en", "assets"):
    shutil.copytree(ROOT / name, OUTPUT / name)

# The generated top-level 404 also prevents Pages from treating the site as an SPA.
print(f"Cloudflare Pages output: {OUTPUT}")
