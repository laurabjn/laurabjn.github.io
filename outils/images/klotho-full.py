import sys
from PIL import Image, ImageDraw, ImageFilter

dl, site, gbp = sys.argv[1:4]
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


def place(canvas, im, x, y, blur=28, alpha=0.30, dy=26):
    pad = 80
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", im.size, (37, 31, 42, 255))
    sh.putalpha(a)
    layer = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    layer.alpha_composite(sh, (pad, pad))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer, (max(0, x - pad), max(0, y - pad + dy)), (max(0, pad - x), max(0, pad - y - dy)))
    canvas.alpha_composite(im, (x, y))


# Écran seul de chaque visuel Google Play (à l'intérieur du cadre d'origine), remis dans un téléphone complet
phones = []
for k in ("k1", "k3"):
    src = Image.open(f"{dl}/klotho/play/{k}.png").convert("RGB")
    phones.append(framed(src.crop((166, 486, 913, src.height)), 720))

W, H = 1200, 900
c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gap = 56
x0 = (W - (phones[0].width + gap + phones[1].width)) // 2
place(c, phones[0], x0, 50)
place(c, phones[1], x0 + phones[0].width + gap, 120)
c.save(f"{site}/assets/projets/klotho.webp", "WEBP", quality=86, method=6)
print("klotho.webp", c.size, "| téléphones", phones[0].size, "| bas :", 120 + phones[1].height)

# Image de partage, centrée comme les autres projets
og = Image.new("RGBA", (1200, 630), BLUSH + (255,))
ImageDraw.Draw(og).ellipse((300, 40, 900, 640), fill=PAPER_ON_BLUSH + (255,))
p = c.crop(c.getbbox())
p = p.resize((round(p.width * 580 / p.height), 580), Image.LANCZOS)
og.alpha_composite(p, ((1200 - p.width) // 2, (630 - p.height) // 2 + 6))
og.convert("RGB").save(f"{site}/assets/projets/klotho-partage.jpg", "JPEG", quality=86, optimize=True, progressive=True)
print("klotho-partage.jpg")

# Photo pour la fiche Google, carré 1080 x 1080, centrée
sq = Image.new("RGBA", (1080, 1080), BLUSH + (255,))
ImageDraw.Draw(sq).ellipse((150, 220, 930, 1000), fill=PAPER_ON_BLUSH + (255,))
p = c.crop(c.getbbox())
p = p.resize((round(p.width * 900 / p.height), 900), Image.LANCZOS)
sq.alpha_composite(p, ((1080 - p.width) // 2, (1080 - p.height) // 2 + 20))
sq.convert("RGB").save(f"{gbp}/4-projet-klotho.jpg", quality=90, optimize=True, progressive=True)
print("4-projet-klotho.jpg (fiche Google)")
