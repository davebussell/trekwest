import re, sys, os, subprocess, concurrent.futures as cf
pages = """/ /private-guided-tours-from-flagstaff-williams-grand-canyon/ /private-tour-guided-day-hikes-in-grand-canyon/ /private-tour-inquire-about-customized-private-tours/ /private-tours-grand-canyon-sunset-dark-sky-tour/ /grand-canyon-e-bike-and-hike-tour/ /contact-us/ /grand-canyon-sunset-star-gazing-tour/ /frequently-asked-questions/ /international-park-entrance-fees-to-grand-canyon/ /our-guides-the-trekwest-story/ /book-your-tour/ /grand-canyon-blog/ /grand-canyon-bike-hike-day-tour/ /grand-canyon-day-tour-from-williams/ /privacy/ /grand-canyon-day-tour-from-flagstaff/ /trail-mix-trekwest-tours-northern-arizona-blog-newsletter/ /flagstaff-arizonas-best-day-hikes/ /rim-to-river-day-grand-canyon-day-hike-what-when-how/ /best-places-to-eat-in-flagstaff-arizona/ /finding-your-basecamp-where-to-stay-when-visiting-grand-canyon/ /arizonas-best-water-hikes-a-guide-to-desert-oases/ /packing-snacks-for-your-hike-think-like-an-astronaut/""".split()
def get(u):
    return subprocess.run(['curl','-sSfL','-m','120',u],check=True,capture_output=True).stdout
urls=set()
for p in pages:
    h=get('https://trekwest.net'+p).decode('utf8','ignore')
    for m in re.finditer(r'https?://trekwest\.net/wp-content/uploads/[^"\'\s)>,]+\.(?:jpe?g|png|webp|gif|mp4|svg)',h,re.I):
        u=m.group(0)
        u=re.sub(r'-\d{2,4}x\d{2,4}(?=\.\w+$)','',u)   # strip WP size suffix -> original
        urls.add(u)
urls=sorted(urls); print(len(urls),'assets')
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
def dl(u):
    name=u.split('/wp-content/uploads/')[1].replace('/','__')
    dest=os.path.join(out,name)
    if os.path.exists(dest): return name,'cached'
    try:
        b=get(u); open(dest,'wb').write(b); return name,len(b)
    except Exception as e:
        return name,'ERR %s'%e
with cf.ThreadPoolExecutor(8) as ex:
    for n,r in ex.map(dl,urls): print(n,r)
