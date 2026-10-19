import sys, json, subprocess, time, os
from playwright.sync_api import sync_playwright
out=sys.argv[1]; pages=sys.argv[2:]
os.makedirs(out,exist_ok=True)
srv=subprocess.Popen(['python3','-m','http.server','8765','-d','dist'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium') if os.path.exists('/opt/pw-browsers/chromium') else p.chromium.launch()
    for w,h,tag in [(375,812,'m'),(1280,800,'d')]:
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1); pg=ctx.new_page()
        errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('requestfailed',lambda r: errs.append('FAILED '+r.url))
        for u in pages:
            pg.goto('http://localhost:8765'+u,wait_until='load'); pg.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,200))}window.scrollTo(0,0)}'); pg.wait_for_timeout(600)
            ov=pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            name=(u.strip('/') or 'home')[:40]
            pg.screenshot(path='%s/%s-%s.png'%(out,name,tag),full_page=True)
            print(tag,u,'overflow',ov)
        print(tag,'errors:',sorted(set(e for e in errs if 'googletagmanager' not in e and 'ytimg' not in e and 'analytics.google' not in e))[:8])
        ctx.close()
    b.close()
finally: srv.terminate()
