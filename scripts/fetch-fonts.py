"""Self-host Archivo + Source Serif 4 (latin subset only). Writes src/fonts/*.woff2 and src/css/fonts.css."""
import re, subprocess, os
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
url="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap"
css=subprocess.run(['curl','-sS','-m','30','-A',UA,url],capture_output=True,text=True,check=True).stdout
os.makedirs('src/fonts',exist_ok=True)
out=[]
for blk in re.findall(r'/\* (\S+) \*/\s*(@font-face \{.*?\})',css,re.S):
    sub,face=blk
    if sub!='latin': continue
    fam=re.search(r"font-family: '([^']+)'",face).group(1); sty=re.search(r'font-style: (\w+)',face).group(1)
    u=re.search(r'url\((https[^)]+)\)',face).group(1)
    name=('%s-%s.woff2'%(fam.replace(' ','').lower(),sty))
    subprocess.run(['curl','-sS','-m','60','-o','src/fonts/'+name,u],check=True)
    out.append(re.sub(r'url\([^)]+\)','url(/fonts/%s)'%name,face))
open('src/css/fonts.css','w').write('\n'.join(out)+'\n')
print(os.listdir('src/fonts'))
