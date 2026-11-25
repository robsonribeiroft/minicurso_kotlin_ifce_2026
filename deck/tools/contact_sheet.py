"""Monta folhas de contato (2 colunas) das prévias para revisão visual rápida.

    python3 deck/tools/contact_sheet.py deck/preview OUT_DIR [por_folha=4] [inicio=1]
"""
import os
import re
import sys

from PIL import Image

src, out = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 4
start = int(sys.argv[4]) if len(sys.argv) > 4 else 1
files = sorted((f for f in os.listdir(src) if f.endswith(".png")),
               key=lambda f: int(re.findall(r"\d+", f)[0]))
files = [f for f in files if int(re.findall(r"\d+", f)[0]) >= start]
os.makedirs(out, exist_ok=True)
for k in range(0, len(files), per):
    chunk = files[k:k + per]
    ims = [Image.open(os.path.join(src, f)).convert("RGB") for f in chunk]
    w, h = ims[0].size
    cols = 2
    rows = -(-len(ims) // cols)
    sheet = Image.new("RGB", (cols * w + 10, rows * h + 10 * (rows - 1)), "#888888")
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        sheet.paste(im, (c * (w + 10), r * (h + 10)))
    name = os.path.join(out, f"sheet_{chunk[0][:-4]}.png")
    sheet.save(name)
    print(name)
