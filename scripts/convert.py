"""Convert extracted WordPress page text (scripts/extract.py output) into body fragments in src/pages/.
Fragments are plain HTML with a leading <!--meta {json} --> line. Hand-built pages (home, about, contact,
book, inquire, blog indexes) are written by hand and skipped here."""
import re, sys, os, json, html
txtdir, out = sys.argv[1], sys.argv[2]
man = json.load(open('src/img/manifest.json'))
SKIP = {'home','our-guides-the-trekwest-story','contact-us','book-your-tour','private-tour-inquire-about-customized-private-tours','grand-canyon-blog','trail-mix-trekwest-tours-northern-arizona-blog-newsletter'}
TOUR = {'grand-canyon-day-tour-from-flagstaff','grand-canyon-day-tour-from-williams','grand-canyon-bike-hike-day-tour','grand-canyon-e-bike-and-hike-tour','grand-canyon-sunset-star-gazing-tour','private-tours-grand-canyon-sunset-dark-sky-tour','private-guided-tours-from-flagstaff-williams-grand-canyon','private-tour-guided-day-hikes-in-grand-canyon'}
POSTS = {'flagstaff-arizonas-best-day-hikes','rim-to-river-day-grand-canyon-day-hike-what-when-how','best-places-to-eat-in-flagstaff-arizona','finding-your-basecamp-where-to-stay-when-visiting-grand-canyon','arizonas-best-water-hikes-a-guide-to-desert-oases','packing-snacks-for-your-hike-think-like-an-astronaut'}
SMALL = {'a','an','and','at','by','for','from','in','of','on','or','the','to','vs','with','n','&'}
KEEP = {'AZ','GC','FALL2026','FAQ','FAQS','ID','US','NPS','NAU','PHX','RV','VRBO','AIRBNB'}
def titlecase(s):
    letters=[c for c in s if c.isalpha()]
    if not letters: return s
    up=sum(c.isupper() for c in letters)/len(letters)
    if up<0.5: return s
    out=[]
    for i,w in enumerate(s.split()):
        core=re.sub(r'[^A-Za-z0-9]','',w).upper()
        if core in KEEP: out.append(w); continue
        lw=w.lower()
        if i>0 and lw.strip('.,:!?') in SMALL: out.append(lw)
        else: out.append(re.sub(r"^(\W*)(\w)",lambda m:m.group(1)+m.group(2).upper(),lw))
    return ' '.join(out)
def fixurl(u):
    u=(u or '').strip()
    m=re.match(r'https://www\.google\.com/search\?q=(https?://.*)',u)
    if m: u=m.group(1)
    u=re.sub(r'^https?://(www\.)?trekwest\.net','',u)
    if u=='' : u='/'
    if u.startswith('/international-travelers'): u='/international-park-entrance-fees-to-grand-canyon/'
    return u
def inline(t):
    t=html.escape(t,quote=False)
    def link(m):
        txt,u=m.group(1),m.group(2)
        u=fixurl(html.unescape(u))
        if u.startswith('/author/') or u.startswith('/category/') or u.startswith('/the-outpost') or 'trekwest.net/the-outpost' in u or u in('','#'): return txt
        ext=' target="_blank" rel="noopener"' if u.startswith('http') else ''
        return '<a href="%s"%s>%s</a>'%(html.escape(u),ext,txt)
    t=re.sub(r'\[([^\]]*)\]\(([^)]*)\)',link,t)
    t=re.sub(r'\*\*\s*\*\*','',t)
    t=re.sub(r'\*\*(.+?)\*\*',lambda m:'<strong>%s</strong>'%m.group(1).strip() if m.group(1).strip() else '',t)
    t=t.replace('****','').replace(' / ','<br>')
    return t.strip()
def img(slug,alt,eager=False,sizes='(min-width:900px) 40vw, 92vw'):
    if slug not in man: print('  MISSING IMG',slug); return ''
    m=man[slug]; fs=sorted(m['files'])
    src=fs[-1][1]
    ss=', '.join('/img/%s %dw'%(n,w) for w,n in fs)
    return '<img src="/img/%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s" loading="%s" decoding="async">'%(src,ss,sizes,m['w'],m['h'],html.escape(alt.strip(),quote=True),'eager' if eager else 'lazy')
def convert(slug,lines):
    kind='tour' if slug in TOUR else 'post' if slug in POSTS else 'info'
    meta={'kind':kind}
    for l in lines[:3]:
        k,_,v=l.partition(': '); meta[k.lower()]=v.strip()
    body=lines[3:]
    h=[]; ul=[]; cols=[]; sec_open=False; row_open=False; col_open=False; first_h1=True
    pending_bg=None; gallery_imgs=[]
    def flush_ul():
        nonlocal ul
        if ul: h.append('<ul>'+''.join('<li>%s</li>'%x for x in ul)+'</ul>'); ul=[]
    def close_col():
        nonlocal col_open,gallery_imgs
        flush_ul()
        if col_open:
            k=colstart
            piece=h[k:]
            if piece and all(x.startswith('<figure') for x in piece):
                h[k-1]='<div class="col gallery">'
            h.append('</div>'); col_open=False
    def close_row():
        nonlocal row_open
        close_col()
        if row_open: h.append('</div>'); row_open=False
    def close_sec():
        nonlocal sec_open
        close_row()
        if sec_open: h.append('</section>'); sec_open=False
    def ensure(): 
        nonlocal sec_open,row_open,col_open,colstart
        if not sec_open: h.append('<section class="band">'); sec_open=True
        if not row_open: h.append('<div class="row">'); row_open=True
        if not col_open: h.append('<div class="col">'); col_open=True; colstart=len(h)
    colstart=0
    hero_h1=None; hero_p=[]
    i=0; seen_first_section=False
    img_count=0
    for l in body:
        l=l.rstrip()
        if l=='=== SECTION ===': 
            close_sec(); seen_first_section=True; continue
        if l=='--- row ---': close_row(); ensure_row=True; h.append('') ; 
        if l=='--- row ---': 
            if not sec_open: h.append('<section class="band">'); sec_open=True
            h.append('<div class="row">'); row_open=True; continue
        if l=='-- col --':
            if not sec_open: h.append('<section class="band">'); sec_open=True
            if not row_open: h.append('<div class="row">'); row_open=True
            close_col(); h.append('<div class="col">'); col_open=True; colstart=len(h); continue
        m=re.match(r'^(#+) ?(.*)$',l)
        if m:
            t=m.group(2).strip()
            if not t: continue
            lvl=len(m.group(1))
            ensure(); flush_ul()
            if lvl==1 and first_h1 and kind!='info' or (lvl==1 and first_h1 and slug in('frequently-asked-questions','privacy','international-park-entrance-fees-to-grand-canyon')):
                first_h1=False; meta['h1']=titlecase(re.sub(r'\s+',' ',t)); h.append('@@H1@@'); continue
            tag='h2' if lvl<=2 else 'h3'
            h.append('<%s>%s</%s>'%(tag,html.escape(titlecase(t),quote=False),tag)); continue
        if l.startswith('P:'):
            t=l[2:].strip()
            if not t or re.fullmatch(r'[\*\s/]*',t): continue
            ensure(); flush_ul()
            if pending_bg:
                mm=re.match(r'^\*\*(.+?)\*\*\s*(.*)$',t.replace('/ **','**').lstrip('/ '),re.S)
                if mm:
                    h.append('<blockquote class="review" style="--bg:url(/img/%s)"><p>%s</p><footer>%s</footer></blockquote>'%(sorted(man[pending_bg]['files'])[0][1] if pending_bg in man else '', inline(mm.group(1)), html.escape(mm.group(2).strip(),quote=False)))
                else:
                    h.append('<blockquote class="review" style="--bg:url(/img/%s)"><p>%s</p></blockquote>'%(sorted(man[pending_bg]['files'])[0][1] if pending_bg in man else '',inline(t)))
                pending_bg=None; continue
            if re.match(r'^\*\*[^*]*\d[^*]*\|[^*]*\*\*\s*(\*\*)?\s*$',t) or re.match(r'^\*\*\d[^*]*\|',t) and t.count('**')==2:
                h.append('<p class="stop">%s</p>'%inline(t)); continue
            h.append('<p>%s</p>'%inline(t)); continue
        if l.startswith('- '):
            ensure(); ul.append(inline(l[2:])); continue
        if l.startswith('BGIMG:'):
            pending_bg=l.split(':',1)[1].strip(); continue
        if l.startswith('IMG:'):
            ensure(); flush_ul()
            s,_,alt=l[4:].partition('| alt='); s=s.strip()
            img_count+=1
            h.append('<figure>%s</figure>'%img(s,alt.strip()))
            if 'og_img' not in meta: meta['og_img']=s
            continue
        if l.startswith('LINK:') or l.startswith('BUTTON:'):
            txt,_,u=l.split(':',1)[1].partition(' -> ')
            txt=txt.strip(); u=fixurl(u)
            if not txt: continue
            ensure(); flush_ul()
            if gallery_imgs: pass
            if u in('','#'): u='/book-your-tour/'
            cls='btn'
            if 'fareharbor.com' in u: cls='btn btn-book'
            ext=' target="_blank" rel="noopener"' if u.startswith('http') and 'fareharbor' not in u else ''
            h.append('<p class="cta"><a class="%s" href="%s"%s>%s</a></p>'%(cls,html.escape(u),ext,html.escape(titlecase(txt),quote=False)))
            continue
        if l.startswith('EMBED:'):
            u=l[6:].strip()
            mm=re.search(r'youtube\.com/embed/([\w-]+)',u)
            if mm:
                ensure(); close_col_gallery=False
                h.append('<div class="video" data-yt="%s"><a href="https://www.youtube.com/watch?v=%s" class="video-play" aria-label="Play the TrekWest tour video"><img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" width="480" height="360" alt="Video: a TrekWest day at the Grand Canyon" loading="lazy"><span aria-hidden="true"></span></a></div>'%(mm.group(1),mm.group(1),mm.group(1)))
            continue
        if l.startswith('[FORM'): continue
    close_sec()
    doc='\n'.join(x for x in h if x!='')
    return meta,doc
os.makedirs(out,exist_ok=True)
for f in sorted(os.listdir(txtdir)):
    slug=f[:-4]
    if slug in SKIP: continue
    lines=open(os.path.join(txtdir,f)).read().split('\n')
    print(slug)
    meta,doc=convert(slug,lines)
    # recover title/h1/intro handled in build via meta
    open(os.path.join(out,slug+'.html'),'w').write('<!--meta %s -->\n%s\n'%(json.dumps(meta,ensure_ascii=False),doc))
