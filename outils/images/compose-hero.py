import sys
from PIL import Image, ImageDraw, ImageFilter
# Usage : python compose-hero.py <dossier sources> <dossier du site>
# (sources : OneDrive\Sauvegarde site-vitrine\sources)
src, site = sys.argv[1:3]
BEZEL = (24, 22, 28, 255)

def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=r, fill=255)
    im = im.convert("RGBA"); im.putalpha(m); return im

def framed(screen, height, bez_ratio=0.035, r_ratio=0.13):
    """Encadre une capture brute dans un téléphone sombre aux coins arrondis."""
    sw = round(screen.width * height / screen.height)
    s = screen.convert("RGB").resize((sw, height), Image.LANCZOS)
    bez = max(8, round(sw * bez_ratio)); r = round(sw * r_ratio)
    s = rounded(s, r - bez // 2)
    ph = Image.new("RGBA", (sw + 2 * bez, height + 2 * bez), (0, 0, 0, 0))
    ImageDraw.Draw(ph).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), radius=r, fill=BEZEL)
    ph.alpha_composite(s, (bez, bez)); return ph

def place(canvas, im, x, y, blur=28, alpha=0.30, dy=26):
    pad = 80
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", im.size, (37, 31, 42, 255)); sh.putalpha(a)
    layer = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    layer.alpha_composite(sh, (pad, pad)); layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer, (max(0, x - pad), max(0, y - pad + dy)), (max(0, pad - x), max(0, pad - y - dy)))
    canvas.alpha_composite(im, (x, y))

# Klotho : écran seul (à l'intérieur du cadre d'origine), recadré dans un téléphone complet
k3 = Image.open(f"{src}/klotho/k3.png").convert("RGB")
klotho_screen = k3.crop((166, 486, 913, k3.height))
# Wim et FreyAge (version mobile du site) : captures brutes
wim_screen = Image.open(f"{src}/fournies-par-laura/wim-swipe.jpg")
freyage_screen = Image.open(f"{src}/freyage/mobile-accueil.png")

W, H = 1200, 924
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
klotho = framed(klotho_screen, 760)
wim = framed(wim_screen, 640)
freyage = framed(freyage_screen, 660)
cx = W // 2
kx, ky = cx - klotho.width // 2, 50
wx, wy = kx - wim.width + 40, ky + 150
fx, fy = kx + klotho.width - 40, ky + 140
print("téléphones :", wim.size, klotho.size, freyage.size, "| x :", wx, kx, fx, "| droite max :", fx + freyage.width)
place(canvas, wim, wx, wy); place(canvas, freyage, fx, fy); place(canvas, klotho, kx, ky)
canvas.save(f"{site}/assets/hero-projets.webp", "WEBP", quality=86, method=6)

# Image de partage (LinkedIn, Facebook…) 1200 x 630
og = Image.new("RGB", (1200, 630), (0xF8, 0xF3, 0xF0)); d = ImageDraw.Draw(og)
d.ellipse((-160, 300, 360, 820), fill=(0xEA, 0xDD, 0xE2)); d.ellipse((900, -220, 1380, 260), fill=(0xEA, 0xDD, 0xE2))
logo = Image.open(f"{src}/fournies-par-laura/logo-laura-bojon.png").convert("RGBA"); logo = logo.crop(logo.getchannel("A").getbbox())
logo = logo.resize((round(logo.width * 520 / logo.height), 520), Image.LANCZOS)
og.paste(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2), logo)
og.save(f"{site}/assets/partage.jpg", "JPEG", quality=88, optimize=True, progressive=True)
print("ok")
