import sys
from PIL import Image, ImageDraw, ImageFilter

# Usage : python fiche-google.py <dossier sources> <dossier du site> <capture du site> <dossier de sortie>
src, site, shot_path, out = sys.argv[1:5]
CREAM = (0xF8, 0xF3, 0xF0)
BLUSH = (0xEA, 0xDD, 0xE2)
PAPER_ON_BLUSH = (0xF2, 0xEA, 0xEA)
SURFACE2 = (0xF1, 0xE8, 0xE6)


def shadow_paste(canvas, im, x, y, blur=30, alpha=0.28, dy=26):
    pad = 90
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", im.size, (37, 31, 42, 255))
    sh.putalpha(a)
    layer = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    layer.alpha_composite(sh, (pad, pad))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer, (max(0, x - pad), max(0, y - pad + dy)), (max(0, pad - x), max(0, pad - y - dy)))
    canvas.alpha_composite(im, (x, y))


def fit(im, w=None, h=None):
    if h is not None:
        return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


logo = Image.open(f"{src}/fournies-par-laura/logo-laura-bojon.png").convert("RGBA")
logo = logo.crop(logo.getchannel("A").getbbox())

# 1. Logo carré 720 x 720
c = Image.new("RGB", (720, 720), CREAM)
lg = fit(logo, h=560)
c.paste(lg, ((720 - lg.width) // 2, (720 - lg.height) // 2), lg)
c.save(f"{out}/1-logo.png", optimize=True)

# 2. Couverture 1080 x 608 (16:9) : logo à gauche, applications à droite
c = Image.new("RGBA", (1080, 608), CREAM + (255,))
d = ImageDraw.Draw(c)
d.ellipse((560, -120, 1160, 480), fill=BLUSH + (255,))
d.ellipse((-140, 380, 260, 780), fill=SURFACE2 + (255,))
lg = fit(logo, h=400)
c.alpha_composite(lg, (70, (608 - lg.height) // 2))
hero = Image.open(f"{site}/assets/hero-projets.webp").convert("RGBA")
hero = hero.crop(hero.getbbox())
hero = fit(hero, h=520)
c.alpha_composite(hero, (1080 - hero.width - 40, (608 - hero.height) // 2 + 10))
c.convert("RGB").save(f"{out}/2-couverture.jpg", quality=90, optimize=True, progressive=True)

# 3 à 5. Projets, carrés 1080 x 1080, sur le fond des cartes du site
for i, name in enumerate(("klotho", "wim", "freyage"), start=3):
    c = Image.new("RGBA", (1080, 1080), BLUSH + (255,))
    d = ImageDraw.Draw(c)
    d.ellipse((150, 220, 930, 1000), fill=PAPER_ON_BLUSH + (255,))
    p = Image.open(f"{site}/assets/projets/{name}.webp").convert("RGBA")
    p = p.crop(p.getbbox())
    p = fit(p, w=960) if p.width / p.height > 960 / 900 else fit(p, h=900)
    # Les téléphones coupés en bas (Klotho) restent posés sur le bord inférieur
    y = 1080 - p.height if name == "klotho" else (1080 - p.height) // 2 + 20
    c.alpha_composite(p, ((1080 - p.width) // 2, y))
    c.convert("RGB").save(f"{out}/{i}-projet-{name}.jpg", quality=90, optimize=True, progressive=True)

# 6. Le site laurabojon.fr dans une fenêtre de navigateur, carré 1080 x 1080
shot = Image.open(shot_path).convert("RGB")
win_w = 960
page = fit(shot, w=win_w)
bar = 46
win = Image.new("RGBA", (win_w, page.height + bar), (0, 0, 0, 0))
m = Image.new("L", win.size, 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, win.width - 1, win.height - 1), radius=18, fill=255)
body = Image.new("RGBA", win.size, SURFACE2 + (255,))
body.paste(page, (0, bar))
dd = ImageDraw.Draw(body)
for k, col in enumerate(((0xC9, 0xB6, 0xC0), (0xC9, 0xB6, 0xC0), (0xC9, 0xB6, 0xC0))):
    dd.ellipse((22 + k * 22, 17, 34 + k * 22, 29), fill=col)
dd.rounded_rectangle((110, 11, 470, 35), radius=8, fill=(0xFF, 0xFC, 0xFA))
body.putalpha(m)
c = Image.new("RGBA", (1080, 1080), BLUSH + (255,))
d = ImageDraw.Draw(c)
d.ellipse((-200, 560, 420, 1180), fill=PAPER_ON_BLUSH + (255,))
d.ellipse((640, -180, 1240, 420), fill=PAPER_ON_BLUSH + (255,))
shadow_paste(c, body, (1080 - win.width) // 2, (1080 - win.height) // 2)
c.convert("RGB").save(f"{out}/6-site-laurabojon.jpg", quality=90, optimize=True, progressive=True)
print("images créées")
