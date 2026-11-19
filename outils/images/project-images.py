import sys, os
from PIL import Image, ImageDraw

dl, img_dir, site = sys.argv[1:4]
base = f"{site}/assets/projets"
for d in ("klotho", "wim"):
    os.makedirs(f"{base}/{d}", exist_ok=True)

BEZEL = (24, 22, 28, 255)
BLUSH = (0xEA, 0xDD, 0xE2)
PAPER_ON_BLUSH = (0xF2, 0xEA, 0xEA)


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


def save(im, path, q=84):
    im.save(path, "WEBP", quality=q, method=6)
    print(f"{path.split('assets/')[-1]:38s} {im.size[0]}x{im.size[1]}  {os.path.getsize(path) // 1024} Ko")


H = 1000
# Klotho : les 6 visuels Google Play (9:16), réduits
for i in range(1, 7):
    im = Image.open(f"{dl}/klotho/play/k{i}.png").convert("RGB").resize((720, 1280), Image.LANCZOS)
    save(im, f"{base}/klotho/k{i}.webp", q=80)

# Wim : la capture dans un téléphone + le logo
save(framed(Image.open(f"{img_dir}/13.jpg"), H - 40), f"{base}/wim/ecran.webp")
logo = Image.open(f"{img_dir}/12.jpg").convert("RGB").resize((560, 560), Image.LANCZOS)
save(rounded(logo, 120), f"{base}/wim/logo.webp")

# Images de partage par projet (1200 x 630)
for name in ("klotho", "wim"):
    og = Image.new("RGBA", (1200, 630), BLUSH + (255,))
    d = ImageDraw.Draw(og)
    d.ellipse((300, 40, 900, 640), fill=PAPER_ON_BLUSH + (255,))
    p = Image.open(f"{base}/{name}.webp").convert("RGBA")
    p = p.crop(p.getbbox())
    p = p.resize((round(p.width * 590 / p.height), 590), Image.LANCZOS)
    y = 630 - p.height if name == "klotho" else (630 - p.height) // 2 + 10
    og.alpha_composite(p, ((1200 - p.width) // 2, y))
    path = f"{base}/{name}-partage.jpg"
    og.convert("RGB").save(path, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"{path.split('assets/')[-1]:38s} 1200x630  {os.path.getsize(path) // 1024} Ko")
