"""Build the current bilingual site for Cloudflare Pages (stdlib only)."""

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
PAGES = (
    "index.html", "modelle.html", "werkstatt.html", "ueber-mich.html",
    "kontakt.html", "impressum.html", "datenschutz.html",
)

subprocess.run([sys.executable, str(ROOT / "scripts/build-site.py")], cwd=ROOT, check=True)
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
OUTPUT.mkdir()
for name in (*PAGES, "home.css", "home.js", "rail.svg"):
    shutil.copy2(ROOT / name, OUTPUT / name)
for name in ("en", "assets"):
    shutil.copytree(ROOT / name, OUTPUT / name)

# A top-level 404 prevents Pages from treating this multi-page site as an SPA.
(OUTPUT / "404.html").write_text(
    '<!doctype html><html lang="de"><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    '<title>404 — RAIL Cycles</title><h1>Seite nicht gefunden / Page not found</h1>'
    '<p><a href="/">Deutsch</a> · <a href="/en/">English</a></p></html>',
    encoding="utf-8",
)
print(f"Cloudflare Pages output: {OUTPUT}")
