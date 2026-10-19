// TrekWest static build: src/ -> dist/. No dependencies. Run: node build.mjs
import { readFileSync, writeFileSync, mkdirSync, rmSync, readdirSync, copyFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';

const root = new URL('.', import.meta.url).pathname;
const src = join(root, 'src'), dist = join(root, 'dist');
const site = JSON.parse(readFileSync(join(src, 'site.json'), 'utf8'));
const man = JSON.parse(readFileSync(join(src, 'img/manifest.json'), 'utf8'));
const today = new Date().toISOString().slice(0, 10);
const year = new Date().getFullYear();
const buildid = Date.now().toString(36);

const part = (n) => readFileSync(join(src, 'partials', n + '.html'), 'utf8');
const P = { head: part('head'), header: part('header'), footer: part('footer') };
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

const GROUP = new Set(['/grand-canyon-day-tour-from-flagstaff/', '/grand-canyon-day-tour-from-williams/', '/grand-canyon-bike-hike-day-tour/', '/grand-canyon-sunset-star-gazing-tour/']);
const PRIVATE = new Set(['/private-guided-tours-from-flagstaff-williams-grand-canyon/', '/private-tours-grand-canyon-sunset-dark-sky-tour/', '/private-tour-guided-day-hikes-in-grand-canyon/', '/grand-canyon-e-bike-and-hike-tour/', '/private-tour-inquire-about-customized-private-tours/']);

function img(slug, sizes, eager = false) {
  const m = man[slug]; if (!m) throw new Error('missing image ' + slug);
  const fs = [...m.files].sort((a, b) => a[0] - b[0]);
  const srcset = fs.map(([w, n]) => `/img/${n} ${w}w`).join(', ');
  return `<img src="/img/${fs[fs.length - 1][1]}" srcset="${srcset}" sizes="${sizes}" width="${m.w}" height="${m.h}" alt="" loading="${eager ? 'eager' : 'lazy'}" decoding="async">`;
}

const pagesDir = join(src, 'pages');
const out = []; // {path, html, noindex, priority}

function render(slug, raw) {
  const mm = raw.match(/^<!--meta (.*?) -->\n/s);
  const meta = JSON.parse(mm[1]); let body = raw.slice(mm[0].length);
  const path = slug === 'home' ? '/' : `/${slug}/`;
  const cfg = site.pages[path] || {};
  const title = meta.title;
  const desc = cfg.desc || meta.desc || '';
  const noindex = !!meta.noindex;
  let h = '';

  if (meta.kind === 'tour') {
    const [first, ...rest] = body.split('</section>');
    let intro = first.replace(/<section class="band">|<div class="row">|<div class="col">|<\/div>|@@H1@@/g, '').trim();
    const crumb = cfg.crumb ? `<p class="crumb"><a href="/">Home</a> / ${esc(cfg.crumb)}</p>` : '';
    const strips = (cfg.strips || []).map((s) => `<figure>${img(s, '(min-width:52rem) 38vw, 40vw', true)}</figure>`).join('');
    h = `<section class="hero"><div class="in">${crumb}<h1>${esc(meta.h1.replace('Stargze', 'Star Gazing').replace('Star Gazing Tour', 'Star Gazing Tour'))}</h1><div class="intro">${intro}</div><div class="strips" aria-hidden="true">${strips}</div></div></section>` + rest.filter((x) => x.trim()).map((x) => x + '</section>').join('\n');
  } else if (meta.kind === 'post') {
    const [first, ...rest] = body.split('</section>');
    const byline = first.match(/<p>by ([^<]*?)(?:\s*\|\s*<a[^>]*>0 comments<\/a>)?<\/p>/);
    let date = '', cats = '';
    if (byline) { const parts = byline[1].split('|').map((s) => s.trim()); date = parts[1] || ''; cats = parts[2] || ''; }
    const fig = first.match(/<figure>(.*?)<\/figure>/s);
    const photo = fig ? `<div class="hero-photo">${fig[1].replace('alt=""', `alt="${esc(meta.h1)}"`).replace(/sizes="[^"]*"/, 'sizes="(min-width:74rem) 70rem, 96vw"').replace('loading="lazy"', 'loading="eager"')}</div>` : '';
    h = `<section class="hero"><div class="in"><p class="crumb"><a href="/trail-mix-trekwest-tours-northern-arizona-blog-newsletter/">Trail Mix blog</a></p><h1>${esc(meta.h1)}</h1><p class="meta">By TrekWest${date ? ' · ' + esc(date) : ''}${cats ? ' · ' + esc(cats) : ''}</p></div></section>${photo}<div class="article">${rest.filter((x) => x.trim()).map((x) => x + '</section>').join('\n')}</div>`;
  } else if (meta.kind === 'info') {
    body = body.replace('@@H1@@', '');
    h = `<section class="hero"><div class="in"><h1>${esc(meta.h1)}</h1></div></section><div class="single">${body}</div>`;
  } else {
    h = body;
  }

  // canonical + social
  const canonical = site.url + path;
  const ogslug = cfg.og || (cfg.strips && cfg.strips[0]) || null;
  const ogimage = `${site.url}/og/${path === '/' || !ogslug ? 'home' : ogslug}.jpg`;
  let jsonld = '';
  if (meta.jsonld === 'home') {
    jsonld = '<script type="application/ld+json">' + JSON.stringify({
      '@context': 'https://schema.org', '@type': 'TravelAgency', name: 'TrekWest Arizona Adventure Tours',
      url: site.url + '/', telephone: '+1-928-814-2432', email: 'info@trekwest.net', logo: site.url + '/icon-192.png',
      image: site.url + '/og/home.jpg',
      address: { '@type': 'PostalAddress', streetAddress: '2404 E Route 66', addressLocality: 'Flagstaff', addressRegion: 'AZ', postalCode: '86004', addressCountry: 'US' },
      sameAs: ['https://www.instagram.com/trekwesttours/', 'https://www.youtube.com/@TrekWestToursofArizona', 'https://www.tripadvisor.com/Attraction_Review-g60971-d6623125-Reviews-TrekWest_Tours_of_Arizona-Flagstaff_Arizona.html'],
    }) + '</script>';
  }
  const gsc = site.gscVerification ? `<meta name="google-site-verification" content="${esc(site.gscVerification)}">` : '';
  let head = P.head
    .replaceAll('{{title}}', esc(title)).replaceAll('{{description}}', esc(desc))
    .replaceAll('{{canonical}}', canonical).replaceAll('{{robots}}', noindex ? 'noindex, follow' : 'index, follow, max-image-preview:large')
    .replaceAll('{{ogtype}}', meta.kind === 'post' ? 'article' : 'website').replaceAll('{{ogimage}}', ogimage)
    .replaceAll('{{buildid}}', buildid).replaceAll('{{gsc}}', gsc).replaceAll('{{gaid}}', site.gaId).replaceAll('{{jsonld}}', jsonld);

  const isBlog = path.includes('blog') || meta.kind === 'post';
  const header = P.header.replace('{{hclass}}', path === '/' ? ' on-hero' : '').replace(/\{\{cur:([^}]+)\}\}/g, (_, k) => {
    const cur = k === 'group' ? GROUP.has(path) : k === 'private' ? PRIVATE.has(path) && path !== '/private-tour-inquire-about-customized-private-tours/' || false : k === 'blog' ? isBlog : k === path;
    return cur ? ' aria-current="page"' : '';
  });
  const hasFH = h.includes('fareharbor.com/embeds/book');
  const footer = P.footer.replace('{{year}}', year)
    .replace('{{bookbar}}', meta.nobookbar || noindex ? '' : '<a class="bookbar" href="/book-your-tour/">Book a tour</a>')
    .replace('{{extrascripts}}', hasFH ? '<script src="https://fareharbor.com/embeds/api/v1/?autolightframe=yes" defer></script>' : '');
  const html = head + header + h + footer;
  out.push({ path, html, noindex, priority: cfg.priority ?? 0.5, file: slug === '404' ? '404.html' : (path === '/' ? 'index.html' : path.slice(1) + 'index.html') });
}

for (const f of readdirSync(pagesDir).filter((f) => f.endsWith('.html')).sort()) {
  render(f.replace(/\.html$/, ''), readFileSync(join(pagesDir, f), 'utf8'));
}

// ---- write ----
rmSync(dist, { recursive: true, force: true });
const used = new Set();
const known = new Set(out.map((o) => o.path));
let warn = 0;
for (const o of out) {
  const p = join(dist, o.file); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, o.html);
  for (const m of o.html.matchAll(/\/(img|og|video)\/[^\s"',)]+/g)) used.add(m[0]);
  for (const m of o.html.matchAll(/href="(\/[^"#?]*)/g)) {
    const u = m[1];
    if (/\.(jpg|png|ico|webp|css|js|xml|txt|woff2)$/.test(u) || u.startsWith('/img/')) continue;
    if (!known.has(u)) { console.warn(`  ! ${o.path} links to unknown ${u}`); warn++; }
  }
}
for (const u of used) {
  const f = join(src, u.slice(1).split('?')[0]);
  if (!existsSync(f)) { console.warn('  ! missing asset', u); warn++; continue; }
  mkdirSync(dirname(join(dist, u.slice(1))), { recursive: true }); copyFileSync(f, join(dist, u.slice(1)));
}
for (const f of ['favicon.ico', 'icon-192.png', 'apple-touch-icon.png']) copyFileSync(join(src, f), join(dist, f));
mkdirSync(join(dist, 'css'), { recursive: true }); writeFileSync(join(dist, 'css/styles.css'), readFileSync(join(src, 'css/fonts.css'), 'utf8') + readFileSync(join(src, 'css/styles.css'), 'utf8'));
mkdirSync(join(dist, 'fonts'), { recursive: true }); for (const f of readdirSync(join(src, 'fonts'))) copyFileSync(join(src, 'fonts', f), join(dist, 'fonts', f));
mkdirSync(join(dist, 'js'), { recursive: true }); copyFileSync(join(src, 'js/main.js'), join(dist, 'js/main.js'));
// og images for every page (collected via ogimage meta)
for (const o of out) for (const m of o.html.matchAll(/https:\/\/trekwest\.net(\/og\/[^"]+)/g)) {
  const f = join(src, m[1].slice(1)); if (existsSync(f)) { mkdirSync(join(dist, 'og'), { recursive: true }); copyFileSync(f, join(dist, m[1].slice(1))); } else { console.warn('  ! missing og', m[1]); warn++; }
}

const urls = out.filter((o) => !o.noindex).sort((a, b) => b.priority - a.priority || a.path.localeCompare(b.path));
writeFileSync(join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((o) => `  <url><loc>${site.url}${o.path}</loc><lastmod>${today}</lastmod><priority>${o.priority.toFixed(1)}</priority></url>`).join('\n')}\n</urlset>\n`);
writeFileSync(join(dist, 'robots.txt'), `User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: ${site.url}/sitemap.xml\n`);
writeFileSync(join(dist, '_headers'), `/img/*\n  Cache-Control: public, max-age=31536000, immutable\n/og/*\n  Cache-Control: public, max-age=604800\n/video/*\n  Cache-Control: public, max-age=31536000, immutable\n/css/*\n  Cache-Control: public, max-age=3600\n/js/*\n  Cache-Control: public, max-age=3600\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n`);
const sizeMB = (d) => { let t = 0; const w = (x) => { for (const e of readdirSync(x)) { const p = join(x, e); const s = statSync(p); s.isDirectory() ? w(p) : (t += s.size); } }; w(d); return (t / 1e6).toFixed(1); };
console.log(`built ${out.length} pages, ${used.size} assets, ${sizeMB(dist)} MB, ${warn} warnings`);
