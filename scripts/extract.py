import re,sys,os,glob
from bs4 import BeautifulSoup, NavigableString
src,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
def img_name(u):
    n=u.split('/wp-content/uploads/')[-1]
    n=re.sub(r'-\d{2,4}x\d{2,4}(?=\.\w+$)','',n)
    n=re.sub(r'-scaled(?=\.\w+$)','',n)
    base=n.split('/',2)[-1] if n.count('/')>=2 else n
    base=os.path.splitext(base)[0]
    return re.sub(r'[^a-z0-9]+','-',base.lower()).strip('-')
def walk(el,L):
    for c in el.children:
        if isinstance(c,NavigableString): continue
        cls=' '.join(c.get('class',[]))
        t=c.name
        if t in('script','style','noscript','form'):
            if t=='form': L.append('[FORM %s]'%(c.get('id') or c.get('action')))
            continue
        if 'et_pb_section' in cls and t=='div': L.append('\n=== SECTION ==='); walk(c,L); continue
        if t in('h1','h2','h3','h4','h5','h6'):
            L.append('#'*int(t[1])+' '+c.get_text(' ',strip=True)); continue
        if t=='p':
            s=str(c); L.append('P: '+inline(c)); continue
        if t in('ul','ol'):
            for li in c.find_all('li',recursive=False): L.append('- '+inline(li))
            continue
        if t=='img':
            L.append('IMG: %s | alt=%s'%(img_name(c.get('data-src') or c.get('src','')),c.get('alt',''))); continue
        if t=='a' and not c.find(['p','h1','h2','h3','h4','div']):
            L.append('LINK: %s -> %s'%(c.get_text(' ',strip=True),c.get('href'))); 
            for i in c.find_all('img'): L.append('IMG: %s | alt=%s'%(img_name(i.get('data-src') or i.get('src','')),i.get('alt','')))
            continue
        if t=='iframe' or t=='video': L.append('EMBED: %s'%(c.get('src') or c.get('data-src')) ); continue
        if 'et_pb_button' in cls and t=='a': L.append('BUTTON: %s -> %s'%(c.get_text(' ',strip=True),c.get('href'))); continue
        if t=='div' and ('et_pb_row' in cls): L.append('--- row ---')
        if t=='div' and 'et_pb_column' in cls: L.append('-- col --')
        if 'et_pb_section' in cls and t=='section': pass
        if t=='div' and c.get('style') and 'background-image' in c.get('style',''):
            m=re.search(r'url\(([^)]+)\)',c['style']); 
            if m: L.append('BGIMG: '+img_name(m.group(1).strip('"\'')))
        # css bg sometimes only in style tags; skip
        walk(c,L)
def inline(c):
    for a in c.find_all('a'):
        a.replace_with('[%s](%s)'%(a.get_text('',strip=False),a.get('href','')))
    for b in c.find_all(['strong','b']): b.replace_with('**%s**'%b.get_text())
    for br in c.find_all('br'): br.replace_with(' / ')
    return re.sub(r'\s+',' ',c.get_text()).strip()
for f in sorted(glob.glob(src+'/*.html')):
    h=open(f,encoding='utf8',errors='ignore').read()
    s=BeautifulSoup(h,'lxml')
    meta={}
    t=s.find('title'); meta['title']=t.get_text() if t else ''
    d=s.find('meta',attrs={'name':'description'}); meta['desc']=d['content'] if d else ''
    og=s.find('meta',property='og:image'); meta['og']=og['content'] if og else ''
    mc=s.find(id='main-content')
    L=['TITLE: '+meta['title'],'DESC: '+meta['desc'],'OG: '+meta['og']]
    walk(mc,L)
    open(os.path.join(out,os.path.basename(f).replace('.html','.txt')),'w').write('\n'.join(L))
