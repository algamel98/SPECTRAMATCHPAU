"""
Convert the SpectraMatch PNG logo to a multi-size .ico file.
Requires: pip install Pillow
Usage:    python installer/convert_icon.py
"""
import os
import sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Source PNG (prefer high-res 1024x1024 logo for sharp icons)
src = os.path.join(PROJECT_DIR, 'static', 'images', 'logo_square_no_name_1024x1024.png')
if not os.path.exists(src):
    src = os.path.join(PROJECT_DIR, 'static', 'images', 'deslogo.png')

if not os.path.exists(src):
    print(f"[ERROR] No source logo found at: {src}")
    sys.exit(1)

out = os.path.join(SCRIPT_DIR, 'spectramatch.ico')

img = Image.open(src).convert('RGBA')

# Standard Windows icon sizes (multi-resolution .ico)
sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
frames = [img.resize(s, Image.LANCZOS) for s in sizes]

frames[0].save(out, format='ICO', sizes=sizes, append_images=frames[1:])
print(f"[OK] Icon saved: {out}  ({len(sizes)} sizes)")
