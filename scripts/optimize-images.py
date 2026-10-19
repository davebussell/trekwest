"""Convert WP originals to responsive WebP (1600w + 800w). Usage: optimize-images.py <orig_dir> <out_dir>
Skips '-scaled' duplicates when the full original exists. Writes manifest.json mapping slug -> dims."""
import os, sys, re, json
from PIL import Image, ImageOps
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
files = sorted(os.listdir(src))
names = set(files)
manifest = {}
for f in files:
    base, ext = os.path.splitext(f)
    if ext.lower() not in ('.jpg','.jpeg','.png','.webp'): continue
    if base.endswith('-scaled') and (base[:-7]+ext) in names: continue
    if re.search(r'-1$', base) and base.startswith('2026__05__IMG_1444'): continue
    slug = re.sub(r'[^a-z0-9]+','-', base.split('__',2)[-1].lower()).strip('-')
    slug = slug.replace('-scaled','')
    keep_png = base.endswith('logo_onlight') or 'pale_logo' in base or 'reviews' in base
    im = Image.open(os.path.join(src,f)); im = ImageOps.exif_transpose(im)
    w,h = im.size
    has_alpha = im.mode in ('RGBA','LA','P')
    im = im.convert('RGBA' if has_alpha else 'RGB')
    sizes = []
    for target in (1600, 800):
        if w < target and target != 800: 
            tw = w
        else:
            tw = min(target, w)
        th = round(h*tw/w)
        r = im.resize((tw,th), Image.LANCZOS) if tw != w else im
        name = f"{slug}-{target}.webp" if tw != w or target==1600 else f"{slug}-{target}.webp"
        if target==800 and tw==sizes[-1][0] if sizes else False: continue
        r.save(os.path.join(out,name),'WEBP',quality=80 if not has_alpha else 85,method=6)
        sizes.append((tw,name))
    manifest[slug]={'w':w,'h':h,'files':sizes,'src':f}
json.dump(manifest, open(os.path.join(out,'manifest.json'),'w'), indent=1)
print(len(manifest),'images ->',out)
