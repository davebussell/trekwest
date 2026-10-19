"""Create 1200x630 JPG social images + favicons from the optimized webp set."""
import json, os
from PIL import Image
site=json.load(open('src/site.json')); man=json.load(open('src/img/manifest.json'))
os.makedirs('src/og',exist_ok=True)
slugs=set()
for k,v in site['pages'].items():
    s=v.get('og') or (v.get('strips') or [None])[0]
    if s: slugs.add(s)
def best(slug): return 'src/img/'+sorted(man[slug]['files'])[-1][1]
def crop(slug,out,size=(1200,630)):
    im=Image.open(best(slug)).convert('RGB'); w,h=im.size; tw,th=size
    r=max(tw/w,th/h); im=im.resize((int(w*r)+1,int(h*r)+1),Image.LANCZOS)
    l=(im.width-tw)//2; t=(im.height-th)//2
    im.crop((l,t,l+tw,t+th)).save(out,quality=82,optimize=True)
for s in sorted(slugs): crop(s,'src/og/%s.jpg'%s)
crop('img-2384','src/og/home.jpg')
ic=Image.open('src/img/cropped-icon-1600.webp').convert('RGB')
ic.resize((192,192),Image.LANCZOS).save('src/icon-192.png'); ic.resize((180,180),Image.LANCZOS).save('src/apple-touch-icon.png')
ic.resize((48,48),Image.LANCZOS).save('src/favicon.ico',sizes=[(48,48)])
print(len(slugs),'og images')
