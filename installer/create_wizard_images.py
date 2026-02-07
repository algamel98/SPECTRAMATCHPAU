"""
Generate the BMP wizard images required by Inno Setup.

  wizard_image.bmp      — 164x314 (left-side panel on Welcome/Finish pages)
  wizard_small.bmp      — 55x55   (top-right corner on other pages)

Uses the project logo and adds a branded gradient background.
Requires: pip install Pillow
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Source logo
logo_path = os.path.join(PROJECT_DIR, 'static', 'images', 'deslogo.png')
if not os.path.exists(logo_path):
    logo_path = os.path.join(PROJECT_DIR, 'static', 'images', 'logo_square_no_name_1024x1024.png')

if not os.path.exists(logo_path):
    print("[ERROR] No logo found.")
    sys.exit(1)

logo = Image.open(logo_path).convert('RGBA')


def make_gradient(width, height, top_color, bottom_color):
    """Create a vertical gradient image."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / max(height - 1, 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


# ── Large wizard image (164 x 314) ──────────────────────────
large = make_gradient(164, 314, (8, 12, 24), (13, 21, 54))

# Place logo centered in upper portion
logo_large = logo.resize((100, 100), Image.LANCZOS)
x = (164 - 100) // 2
y = 60
large.paste(logo_large, (x, y), logo_large)

# Add app name text below the logo
draw_large = ImageDraw.Draw(large)
try:
    font = ImageFont.truetype("segoeui.ttf", 16)
    font_small = ImageFont.truetype("segoeui.ttf", 10)
except OSError:
    font = ImageFont.load_default()
    font_small = font

text = "SpectraMatch"
bbox = draw_large.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
draw_large.text(((164 - tw) // 2, y + 110), text, fill=(224, 232, 255), font=font)

sub = "Desktop Edition"
bbox2 = draw_large.textbbox((0, 0), sub, font=font_small)
tw2 = bbox2[2] - bbox2[0]
draw_large.text(((164 - tw2) // 2, y + 132), sub, fill=(143, 168, 255), font=font_small)

ver = "v2.2.1"
bbox3 = draw_large.textbbox((0, 0), ver, font=font_small)
tw3 = bbox3[2] - bbox3[0]
draw_large.text(((164 - tw3) // 2, 290), ver, fill=(100, 120, 170), font=font_small)

large_path = os.path.join(SCRIPT_DIR, 'wizard_image.bmp')
large.save(large_path, 'BMP')
print(f"[OK] {large_path}")


# ── Small wizard image (55 x 55) ────────────────────────────
small = make_gradient(55, 55, (8, 12, 24), (13, 21, 54))
logo_small = logo.resize((40, 40), Image.LANCZOS)
small.paste(logo_small, (7, 7), logo_small)

small_path = os.path.join(SCRIPT_DIR, 'wizard_small.bmp')
small.save(small_path, 'BMP')
print(f"[OK] {small_path}")
