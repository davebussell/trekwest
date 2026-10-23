#!/usr/bin/env python3
"""Add owner-supplied photos to src/img (webp 800/1600), the manifest, alt text, and a post's site.json `photos` list.
Usage: add-owner-photos.py <page-path> <slug>=<source-file>[::alt text] ...   (order = hero first)"""
import sys, json, pathlib
from PIL import Image, ImageOps
ROOT = pathlib.Path(__file__).resolve().parents[1]
page, items = sys.argv[1], sys.argv[2:]
man = json.load(open(ROOT / 'src/img/manifest.json'))
site = json.load(open(ROOT / 'src/site.json'))
slugs = []
for it in items:
    spec, _, alt = it.partition('::')
    slug, src = spec.split('=', 1)
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    w, h = im.size
    files = []
    for target in (1600, 800):
        tw = min(target, w)
        out = im if tw == w else im.resize((tw, round(h * tw / w)), Image.LANCZOS)
        name = f'{slug}-{target}.webp'
        out.save(ROOT / 'src/img' / name, 'WEBP', quality=80, method=6)
        files.append([tw, name])
        if tw == w: break
    man[slug] = {'w': w, 'h': h, 'files': files, 'src': pathlib.Path(src).name}
    if alt: site.setdefault('alts', {})[slug] = alt
    slugs.append(slug)
site['pages'][page]['photos'] = slugs
site['pages'][page]['og'] = slugs[0]  # cards, recents and home rows use og
json.dump(man, open(ROOT / 'src/img/manifest.json', 'w'), indent=1)
json.dump(site, open(ROOT / 'src/site.json', 'w'), indent=1, ensure_ascii=False)
# 1200x630 social image from the hero photo
im = ImageOps.exif_transpose(Image.open(items[0].split('::')[0].split('=', 1)[1])).convert('RGB')
r = max(1200 / im.width, 630 / im.height); im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
l, t = (im.width - 1200) // 2, int((im.height - 630) * 0.4)
im.crop((l, t, l + 1200, t + 630)).save(ROOT / 'src/og' / f'{slugs[0]}.jpg', quality=82, optimize=True)
print(page, slugs)
