import os, sys
from PIL import Image, ImageDraw, ImageFilter

fdir, img_dir, site = sys.argv[1:4]
base = f"{site}/assets/projets"
os.makedirs(f"{base}/freyage", exist_ok=True)
BEZEL = (24, 22, 28, 255)
BLUSH = (0xEA, 0xDD, 0xE2)
PAPER_ON_BLUSH = (0xF2, 0xEA, 0xEA)
CHROME = (0xF1, 0xE8, 0xE6)


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=r, fill=255)
    im = im.convert("RGBA")
    im.putalpha(m)
    return im


def framed(screen, height):
    sw = round(screen.width * height / screen.height)
    s = screen.convert("RGB").resize((sw, height), Image.LANCZOS)
    bez = max(10, round(sw * 0.035))
    r = round(sw * 0.13)
    s = rounded(s, r - bez // 2)
    ph = Image.new("RGBA", (sw + 2 * bez, height + 2 * bez), (0, 0, 0, 0))
    ImageDraw.Draw(ph).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), radius=r, fill=BEZEL)
    ph.alpha_composite(s, (bez, bez))
    return ph


def browser(shot, width, url_bar=True):
    page = shot.convert("RGB").resize((width, round(shot.height * width / shot.width)), Image.LANCZOS)
    bar = round(width * 0.045)
    win = Image.new("RGBA", (width, page.height + bar), CHROME + (255,))
    win.paste(page, (0, bar))
    d = ImageDraw.Draw(win)
    dot = round(bar * 0.26)
    for k in range(3):
        cx = round(bar * 0.6) + k * round(bar * 0.55)
        d.ellipse((cx, bar // 2 - dot // 2, cx + dot, bar // 2 + dot // 2), fill=(0xC9, 0xB6, 0xC0))
    if url_bar:
        d.rounded_rectangle((round(width * 0.12), round(bar * 0.22), round(width * 0.48), round(bar * 0.78)), radius=round(bar * 0.2), fill=(0xFF, 0xFC, 0xFA))
    return rounded(win, round(width * 0.018))


def place(canvas, im, x, y, blur=26, alpha=0.28, dy=22):
    pad = 80
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", im.size, (37, 31, 42, 255))
    sh.putalpha(a)
    layer = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    layer.alpha_composite(sh, (pad, pad))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer, (max(0, x - pad), max(0, y - pad + dy)), (max(0, pad - x), max(0, pad - y - dy)))
    canvas.alpha_composite(im, (x, y))


def save(im, path, q=84):
    im.save(path, "WEBP", quality=q, method=6)
    print(f"{path.split('assets/')[-1]:36s} {im.size[0]}x{im.size[1]}  {os.path.getsize(path) // 1024} Ko")


# --- FreyAge : vignette (navigateur + téléphone), 1200 x 900 transparent
desk = Image.open(f"{fdir}/desktop-accueil.png")
mob = Image.open(f"{fdir}/mobile-accueil.png")
c = Image.new("RGBA", (1200, 900), (0, 0, 0, 0))
win = browser(desk, 860)
ph = framed(mob, 600)
place(c, win, 90, 150)
place(c, ph, 1200 - ph.width - 90, 900 - ph.height - 70)
save(c, f"{base}/freyage.webp", q=86)

# --- FreyAge : galerie (écrans mobiles dans un téléphone)
for name in ("accueil", "prestations", "mariage", "rdv", "carte-cadeau", "portfolio"):
    save(framed(Image.open(f"{fdir}/mobile-{name}.png"), 960), f"{base}/freyage/{name}.webp")

# --- Image de partage FreyAge
og = Image.new("RGBA", (1200, 630), BLUSH + (255,))
ImageDraw.Draw(og).ellipse((300, 40, 900, 640), fill=PAPER_ON_BLUSH + (255,))
p = c.crop(c.getbbox())
p = p.resize((round(p.width * 580 / p.height), 580), Image.LANCZOS)
og.alpha_composite(p, ((1200 - p.width) // 2, (630 - p.height) // 2 + 6))
og.convert("RGB").save(f"{base}/freyage-partage.jpg", "JPEG", quality=86, optimize=True, progressive=True)
print("projets/freyage-partage.jpg")

# --- Wim : nouveaux écrans
for src, name in (("21.jpg", "fiche"), ("22.jpg", "profil"), ("23.jpg", "carte"), ("25.jpg", "conversation"), ("26.jpg", "messages")):
    save(framed(Image.open(f"{img_dir}/{src}"), 960), f"{base}/wim/{name}.webp")
