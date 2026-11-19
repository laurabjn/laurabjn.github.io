import re, sys, urllib.request
css_path, out_dir, css_out = sys.argv[1:4]
css = open(css_path, encoding="utf-8").read()
blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", css, re.S)
faces, seen = [], {}
for subset, body in blocks:
    if subset != "latin":
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
    style = re.search(r"font-style:\s*(\w+)", body).group(1)
    weight = re.search(r"font-weight:\s*([\d ]+);", body).group(1).strip()
    url = re.search(r"url\((https://[^)]+\.woff2)\)", body).group(1)
    rng = re.search(r"unicode-range:\s*([^;]+);", body).group(1).strip()
    name = f"{fam.lower().replace(' ', '-')}-{style}-{weight.replace(' ', '-')}.woff2"
    if url not in seen:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req).read()
        open(f"{out_dir}/{name}", "wb").write(data); seen[url] = name
        print(f"{name:45s} {len(data)//1024} Ko")
    faces.append(f"@font-face {{\n  font-family: \"{fam}\";\n  font-style: {style};\n  font-weight: {weight};\n  font-display: swap;\n"
                 f"  src: url(\"assets/fonts/{seen[url]}\") format(\"woff2\");\n  unicode-range: {rng};\n}}")
open(css_out, "w", encoding="utf-8", newline="\n").write("/* Polices hébergées avec le site (jeu de caractères latin : français, € et ponctuation typographique) */\n" + "\n".join(faces) + "\n")
print(len(faces), "déclarations @font-face")
