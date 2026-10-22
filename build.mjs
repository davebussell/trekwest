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

const TOURS = {
  '/grand-canyon-day-tour-from-flagstaff/': { price: 199, type: 'Small-group guided day tour' },
  '/grand-canyon-day-tour-from-williams/': { price: 189, type: 'Small-group guided day tour' },
  '/grand-canyon-bike-hike-day-tour/': { price: 269, type: 'Small-group e-bike and hike day tour' },
  '/private-tours-grand-canyon-sunset-dark-sky-tour/': { price: 899, from: true, type: 'Private sunset and dark-sky tour' },
  '/private-tour-guided-day-hikes-in-grand-canyon/': { price: 999, from: true, type: 'Private guided day hike' },
  '/grand-canyon-e-bike-and-hike-tour/': { price: 1100, from: true, type: 'Private e-bike and hike tour' },
};

function img(slug, sizes, eager = false) {
  const m = man[slug]; if (!m) throw new Error('missing image ' + slug);
  const fs = [...m.files].sort((a, b) => a[0] - b[0]);
  const srcset = fs.map(([w, n]) => `/img/${n} ${w}w`).join(', ');
  return `<img src="/img/${fs[fs.length - 1][1]}" srcset="${srcset}" sizes="${sizes}" width="${m.w}" height="${m.h}" alt="" loading="${eager ? 'eager' : 'lazy'}" decoding="async">`;
}

// Analytics: GTM (if gtmId set) carries GA4 + Clarity inside the container; otherwise GA4 and Clarity load directly.
function analytics() {
  const parts = [];
  if (site.gtmId) {
    parts.push(`<!-- Google Tag Manager --><script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','${site.gtmId}');</script>`);
  } else {
    if (site.gaId) parts.push(`<script async src="https://www.googletagmanager.com/gtag/js?id=${site.gaId}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${site.gaId}');</script>`);
    if (site.clarityId) parts.push(`<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","${site.clarityId}");</script>`);
  }
  return parts.join('\n');
}
const GTM_NOSCRIPT = site.gtmId ? `<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=${site.gtmId}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>` : '';

const pagesDir = join(src, 'pages');
const out = []; // {path, html, noindex, priority}
let warnCount = 0;

function render(slug, raw) {
  const mm = raw.match(/^<!--meta (.*?) -->\n/s);
  const meta = JSON.parse(mm[1]); let body = raw.slice(mm[0].length);
  const path = slug === 'home' ? '/' : `/${slug}/`;
  const cfg = site.pages[path] || {};
  const BRAND = 'TrekWest Arizona Adventure Tours';
  const baseTitle = String(meta.title).replace(/ - TrekWest Arizona Adventure Tours( page)?$/, '').replace(/&amp;/g, '&');
  const title = cfg.title || (meta.title.includes(BRAND) ? (baseTitle.length + 11 <= 60 ? baseTitle + ' | TrekWest' : baseTitle) : meta.title);
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
    const alt = (s) => esc((site.alts || {})[s] || meta.h1);
    const owned = (cfg.photos || []).filter((s) => man[s]);
    // owner-supplied photos: first is the hero, the rest sit inside the article after the opening paragraphs
    if (owned.length > 1) {
      const figs = owned.slice(1).map((s) => `<figure class="inline-photo">${img(s, '(min-width:52rem) 46rem, 92vw').replace('alt=""', `alt="${alt(s)}"`)}</figure>`).join('');
      let n = 0; rest[0] = rest[0].replace(/<\/p>/g, (m) => (++n === 2 ? m + figs : m));
      if (n < 2) rest[0] = rest[0].replace(/(<div class="col">)/, `$1${figs}`);
    }
    const photo = owned.length ? `<div class="hero-photo">${img(owned[0], '(min-width:74rem) 70rem, 96vw', true).replace('alt=""', `alt="${alt(owned[0])}"`)}</div>` : fig ? `<div class="hero-photo">${fig[1].replace('alt=""', `alt="${esc(meta.h1)}"`).replace(/sizes="[^"]*"/, 'sizes="(min-width:74rem) 70rem, 96vw"').replace('loading="lazy"', 'loading="eager"')}</div>` : '';
    h = `<section class="hero"><div class="in"><p class="crumb"><a href="/field-notes/">Field Notes</a> / From the trail</p><h1>${esc(meta.h1)}</h1><p class="meta">By TrekWest${date ? ' · ' + esc(date) : ''}${cats ? ' · ' + esc(cats) : ''}</p></div></section>${photo}<div class="article">${rest.filter((x) => x.trim()).map((x) => x + '</section>').join('\n')}</div>`;
  } else if (meta.kind === 'guide') {
    const upd = new Date((cfg.date || today) + 'T12:00:00Z').toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
    const photo = cfg.og && man[cfg.og] ? `<div class="hero-photo">${img(cfg.og, '(min-width:74rem) 70rem, 96vw', true).replace('alt=""', `alt="${esc(cfg.ogalt || meta.h1)}"`)}</div>` : '';
    h = `<section class="hero"><div class="in"><p class="crumb"><a href="/field-notes/">Field Notes</a> / ${esc(meta.cat || 'Planning')}</p><h1>${esc(meta.h1)}</h1><p class="meta">By the TrekWest guides · Updated ${upd}</p></div></section>${photo}<div class="article"><section class="band"><div class="row"><div class="col">${body}</div></div></section></div>`;
  } else if (meta.kind === 'info') {
    body = body.replace('@@H1@@', '');
    h = `<section class="hero"><div class="in"><h1>${esc(meta.h1)}</h1></div></section><div class="single">${body}</div>`;
  } else {
    h = body;
  }

  // canonical + social
  const canonical = site.url + path;
  const ogslug = (cfg.photos && cfg.photos[0]) || cfg.og || (cfg.strips && cfg.strips[0]) || null;
  const ogimage = `${site.url}/og/${path === '/' || !ogslug ? 'home' : ogslug}.jpg`;
  const abs = (u) => (u.startsWith('http') ? u : site.url + u);
  const ORG = { '@type': 'TravelAgency', '@id': site.url + '/#business', name: 'TrekWest Arizona Adventure Tours', url: site.url + '/', telephone: '+1-928-814-2432', email: 'info@trekwest.net', logo: site.url + '/icon-192.png', image: site.url + '/og/home.jpg', priceRange: '$$$',
    address: { '@type': 'PostalAddress', streetAddress: '2404 E Route 66', addressLocality: 'Flagstaff', addressRegion: 'AZ', postalCode: '86004', addressCountry: 'US' },
    areaServed: ['Flagstaff, AZ', 'Williams, AZ', 'Tusayan, AZ', 'Grand Canyon National Park'],
    sameAs: ['https://www.instagram.com/trekwesttours/', 'https://www.youtube.com/@TrekWestToursofArizona', 'https://www.tripadvisor.com/Attraction_Review-g60971-d6623125-Reviews-TrekWest_Tours_of_Arizona-Flagstaff_Arizona.html'] };
  const graph = [];
  if (meta.jsonld === 'home') {
    graph.push(ORG, { '@type': 'WebSite', '@id': site.url + '/#website', url: site.url + '/', name: 'TrekWest Arizona Adventure Tours', publisher: { '@id': site.url + '/#business' }, inLanguage: 'en-US' });
  } else if (!noindex) {
    const crumbs = [{ name: 'Home', url: site.url + '/' }];
    if (meta.kind === 'post' || meta.kind === 'guide') crumbs.push({ name: 'Field Notes', url: site.url + '/field-notes/' });
    crumbs.push({ name: meta.h1 || baseTitle, url: canonical });
    graph.push({ '@type': 'BreadcrumbList', itemListElement: crumbs.map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: c.url })) });
    const pageImg = ogimage;
    if (meta.kind === 'post' || meta.kind === 'guide') {
      graph.push({ '@type': meta.kind === 'guide' ? 'Article' : 'BlogPosting', headline: meta.h1, description: desc, image: [pageImg], mainEntityOfPage: canonical, datePublished: cfg.date || '2026-04-01', dateModified: cfg.date || '2026-04-01', author: { '@type': 'Organization', name: 'TrekWest Tours', url: site.url + '/' }, publisher: { '@type': 'Organization', name: 'TrekWest Arizona Adventure Tours', logo: { '@type': 'ImageObject', url: site.url + '/icon-192.png' } } });
    } else if (meta.kind === 'tour' && TOURS[path]) {
      const t = TOURS[path];
      const offer = t.from ? { '@type': 'AggregateOffer', priceCurrency: 'USD', lowPrice: t.price, offerCount: 1, availability: 'https://schema.org/InStock', url: canonical } : { '@type': 'Offer', priceCurrency: 'USD', price: t.price, availability: 'https://schema.org/InStock', url: canonical };
      graph.push({ '@type': 'TouristTrip', name: meta.h1, description: desc, image: [pageImg], url: canonical, touristType: t.type, provider: { '@id': site.url + '/#business' }, offers: offer });
    }
  }
  const jsonld = graph.length ? '<script type="application/ld+json">' + JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }) + '</script>' : '';
  const gsc = site.gscVerification ? `<meta name="google-site-verification" content="${esc(site.gscVerification)}">` : '';
  let head = P.head
    .replaceAll('{{title}}', esc(title)).replaceAll('{{description}}', esc(desc))
    .replaceAll('{{canonical}}', canonical).replaceAll('{{robots}}', noindex ? 'noindex, follow' : 'index, follow, max-image-preview:large')
    .replaceAll('{{ogtype}}', meta.kind === 'post' || meta.kind === 'guide' ? 'article' : 'website').replaceAll('{{ogimage}}', ogimage)
    .replaceAll('{{buildid}}', buildid).replaceAll('{{gsc}}', gsc).replaceAll('{{analytics}}', analytics()).replaceAll('{{jsonld}}', jsonld)
    .replaceAll('{{ogalt}}', esc(cfg.ogalt || meta.h1 || BRAND)).replaceAll('{{extra}}', meta.kind === 'post' || meta.kind === 'guide' ? `<meta property="article:published_time" content="${cfg.date || '2026-04-01'}"><meta property="article:author" content="TrekWest Tours"><meta property="article:section" content="Northern Arizona travel">` : '');

  const isBlog = path === '/field-notes/' || meta.kind === 'post' || meta.kind === 'guide';
  const header = GTM_NOSCRIPT + P.header.replace('{{hclass}}', path === '/' ? ' on-hero' : '').replace(/\{\{cur:([^}]+)\}\}/g, (_, k) => {
    const cur = k === 'group' ? GROUP.has(path) : k === 'private' ? PRIVATE.has(path) && path !== '/private-tour-inquire-about-customized-private-tours/' || false : k === 'blog' ? isBlog : k === path;
    return cur ? ' aria-current="page"' : '';
  });
  const hasFH = h.includes('fareharbor.com/embeds/book');
  const footer = P.footer.replace('{{year}}', year)
    .replace('{{bookbar}}', meta.nobookbar || noindex ? '' : '<a class="bookbar" href="/book-your-tour/">Book a tour</a>')
    .replace('{{extrascripts}}', hasFH ? '<script src="https://fareharbor.com/embeds/api/v1/?autolightframe=yes" defer></script>' : '');
  let html = head + header + h + footer;
  html = html.replace(/<img\b[^>]*>/g, (tag) => {
    if (!tag.includes('alt=""')) return tag;
    const m = tag.match(/src="\/img\/(.+?)-\d+\.webp"/); const a = m && (site.alts || {})[m[1]];
    return a ? tag.replace('alt=""', `alt="${esc(a)}"`) : tag;
  });
  out.push({ kind: meta.kind, cat: meta.cat || 'Planning', date: cfg.date || '2026-04-01', title: meta.h1 || title, path, html, noindex, priority: cfg.priority ?? 0.5, file: slug === '404' ? '404.html' : (path === '/' ? 'index.html' : path.slice(1) + 'index.html') });
}

for (const f of readdirSync(pagesDir).filter((f) => f.endsWith('.html')).sort()) {
  render(f.replace(/\.html$/, ''), readFileSync(join(pagesDir, f), 'utf8'));
}


// ---- recent posts strip (inner pages) ----
const NORECENT = new Set(['/', '/404/', '/thanks/', '/field-notes/', '/book-your-tour/', '/private-tour-inquire-about-customized-private-tours/']);
const postsNewest = out.filter((o) => o.kind === 'post').sort((a, b) => b.date.localeCompare(a.date) || a.path.localeCompare(b.path));
function recents(selfPath) {
  const items = postsNewest.filter((p) => p.path !== selfPath).slice(0, 3);
  const cards = items.map((p) => {
    const slug = (site.pages[p.path] || {}).og; const m = slug && man[slug]; if (!m) return '';
    const fs = [...m.files].sort((x, y) => x[0] - y[0]);
    return `<article class="post-card"><a href="${p.path}"><img src="/img/${fs[fs.length - 1][1]}" srcset="${fs.map(([w, n]) => `/img/${n} ${w}w`).join(', ')}" sizes="(min-width:52rem) 30vw, 92vw" width="${m.w}" height="${m.h}" alt="" loading="lazy" decoding="async"><h3>${esc(p.title)}</h3></a></article>`;
  }).join('');
  return `<section class="band recents" aria-label="Recent posts"><div class="wrap"><h2>Latest field notes</h2><div class="posts">${cards}</div><p class="more"><a class="arrow" href="/field-notes/">All field notes</a><a href="https://www.instagram.com/trekwesttours/" target="_blank" rel="noopener me">Follow @trekwesttours on Instagram</a></p></div></section>`;
}

// home Trail Mix rows: newest 3 posts
{
  const home = out.find((o) => o.path === '/');
  const fmt = (iso) => new Date(iso + 'T12:00:00Z').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
  const rows = postsNewest.slice(0, 3).map((p, i) => {
    const cfg = site.pages[p.path] || {}; const m = man[cfg.og]; if (!m) return '';
    const fs = [...m.files].sort((x, y) => x[0] - y[0]);
    return `<a class="prow" href="${p.path}"><span class="pi"><img src="/img/${fs[fs.length - 1][1]}" srcset="${fs.map(([w, n]) => `/img/${n} ${w}w`).join(', ')}" sizes="(min-width:52rem) 50vw, 100vw" width="${m.w}" height="${m.h}" alt="" loading="lazy" decoding="async"></span><span class="pt"><span class="meta">${fmt(p.date)}</span><strong>${esc(p.title)}</strong><span>${esc(cfg.desc || '')}</span><span class="read">Read the post</span></span></a>`;
  }).join('');
  home.html = home.html.replace(/<div class="plist">[\s\S]*?<\/div>(?=\s*<\/div>\s*<\/section>)/, `<div class="plist">${rows}</div>`);
}
const CTA = `<section class="band cta-band" aria-label="Book a tour"><div class="wrap"><div><h2>Want to see it with a local guide?</h2><p>Small groups, no more than 10 guests, park fees and lunch included on our day tours. Book online or ask us anything.</p></div><div class="cta-actions"><a class="btn" href="/book-your-tour/">Book a tour</a><a class="btn-ghost" href="/contact-us/">Ask a question</a></div></div></section>`;
const IG_URL = 'https://www.instagram.com/trekwesttours';
const IG_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.6" cy="6.4" r="1.3" fill="currentColor"/></svg>';
const igReel = (s, cls) => { const m = man[s]; if (!m) return ''; const fs = [...m.files].sort((a, b) => a[0] - b[0]); return `<span class="ig-reel ${cls}"><img src="/img/${fs[0][1]}" width="${m.w}" height="${m.h}" alt="" loading="lazy" decoding="async"><span class="ig-play" aria-hidden="true"></span></span>`; };
const IG = `<section class="ig-band" aria-label="TrekWest on Instagram"><div class="ig-in"><div class="ig-copy"><p class="ig-handle">${IG_ICON}<span>@trekwesttours</span></p><h2>Dozens of reels from the trail</h2><p>Quick tips, hidden overlooks, road-trip tricks and the places we love around the Grand Canyon, Flagstaff and Sedona. New ones every week, straight from our guides.</p><a class="btn ig-btn" href="${IG_URL}" target="_blank" rel="noopener">Watch on Instagram</a></div><a class="ig-phones" href="${IG_URL}" target="_blank" rel="noopener" aria-label="Open @trekwesttours on Instagram">${igReel('img-2455', 'r1')}${igReel('img-3288', 'r2')}${igReel('557589649-10172586905680327-8570737225099137399-n', 'r3')}</a></div></section>`;
for (const o of out) { if (NORECENT.has(o.path) || o.noindex) continue; const fn = o.kind === 'post' || o.kind === 'guide'; o.html = o.html.replace('</main>', (fn ? IG + CTA : '') + recents(o.path) + '\n</main>'); }

// ---- guides index: existing trail posts first, then the planning guides ----
{
  const gi = out.find((o) => o.path === '/field-notes/');
  const fmt = (iso) => new Date(iso + 'T12:00:00Z').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
  const card = (p, sub) => {
    const cfg = site.pages[p.path] || {}; const m = cfg.og && man[cfg.og]; if (!m) { console.warn('  ! no og image for', p.path); warnCount++; return ''; }
    const fs = [...m.files].sort((x, y) => x[0] - y[0]);
    return `<article class="post-card"><a href="${p.path}"><img src="/img/${fs[fs.length - 1][1]}" srcset="${fs.map(([w, n]) => `/img/${n} ${w}w`).join(', ')}" sizes="(min-width:62rem) 30vw, (min-width:36rem) 45vw, 92vw" width="${m.w}" height="${m.h}" alt="${esc(cfg.ogalt || p.title)}" loading="lazy" decoding="async"><p class="meta">${esc(sub)}</p><h3>${esc(p.title)}</h3><p>${esc(cfg.desc || '')}</p></a></article>`;
  };
  const guides = out.filter((o) => o.kind === 'guide').sort((a, b) => ((site.pages[a.path] || {}).rank ?? 99) - ((site.pages[b.path] || {}).rank ?? 99));
  const cats = [...new Set(guides.map((g) => g.cat))];
  const sections = [`<section class="band gsec"><div class="wrap"><h2>From the trail</h2><p class="sub">Trip notes and local favourites from our guides.</p><div class="posts">${postsNewest.map((p) => card(p, fmt(p.date))).join('')}</div></div></section>`,
    ...cats.map((c) => `<section class="band gsec"><div class="wrap"><h2>${esc(c)}</h2><div class="posts">${guides.filter((g) => g.cat === c).map((g) => card(g, c)).join('')}</div></div></section>`)];
  gi.html = gi.html.replace('@@GUIDE_INDEX@@', sections.join('\n'));
}

// ---- write ----
rmSync(dist, { recursive: true, force: true });
const used = new Set();
const known = new Set(out.map((o) => o.path));
let warn = warnCount;
for (const o of out) {
  const p = join(dist, o.file); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, o.html);
  for (const m of o.html.matchAll(/\/(img|og|video)\/[^\s"',)]+/g)) used.add(m[0]);
  for (const m of o.html.matchAll(/href="(\/[^"#?]*)/g)) {
    const u = m[1];
    if (/\.(jpg|png|ico|webp|css|js|xml|txt|woff2|webmanifest)$/.test(u) || u.startsWith('/img/')) continue;
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
writeFileSync(join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((o) => `  <url><loc>${site.url}${o.path}</loc><lastmod>${o.kind === 'post' ? o.date : (o.date > '2026-10-19' ? o.date : '2026-10-19')}</lastmod><priority>${o.priority.toFixed(1)}</priority></url>`).join('\n')}\n</urlset>\n`);
writeFileSync(join(dist, 'robots.txt'), `User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: ${site.url}/sitemap.xml\n`);
writeFileSync(join(dist, '_headers'), `/img/*\n  Cache-Control: public, max-age=31536000, immutable\n/og/*\n  Cache-Control: public, max-age=604800\n/video/*\n  Cache-Control: public, max-age=31536000, immutable\n/css/*\n  Cache-Control: public, max-age=3600\n/js/*\n  Cache-Control: public, max-age=3600\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Strict-Transport-Security: max-age=31536000\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Frame-Options: SAMEORIGIN\n`);
writeFileSync(join(dist, 'site.webmanifest'), JSON.stringify({ name: 'TrekWest Arizona Adventure Tours', short_name: 'TrekWest', start_url: '/', display: 'browser', background_color: '#ffffff', theme_color: '#17465d', icons: [{ src: '/icon-192.png', sizes: '192x192', type: 'image/png' }] }));
writeFileSync(join(dist, '_redirects'), ['/home / 301', '/index.html / 301', '/guides /field-notes/ 301', '/guides/ /field-notes/ 301', '/feed /field-notes/ 301', '/feed/* /field-notes/ 301', '/blog /field-notes/ 301', '/blog/* /field-notes/ 301', '/trail-mix-trekwest-tours-northern-arizona-blog-newsletter/ /field-notes/ 301', '/trail-mix-trekwest-tours-northern-arizona-blog-newsletter/* /field-notes/ 301', '/grand-canyon-blog/ /field-notes/ 301', '/grand-canyon-blog/* /field-notes/ 301', '/category/* /field-notes/ 301', '/tag/* /field-notes/ 301', '/faq /frequently-asked-questions/ 301', '/faqs /frequently-asked-questions/ 301', '/contact /contact-us/ 301', '/about /our-guides-the-trekwest-story/ 301', '/about-us /our-guides-the-trekwest-story/ 301', '/book /book-your-tour/ 301', '/book-now /book-your-tour/ 301', '/tours /#tours 301'].join('\n') + '\n');
writeFileSync(join(dist, 'llms.txt'), `# TrekWest Arizona Adventure Tours\n\n> Family-owned boutique guide company in Flagstaff, Arizona. Small-group (max 10 guests) Grand Canyon day tours from Flagstaff and Williams, plus private tours, e-bike and hike days, sunset and dark-sky tours. Rated 5 stars on Tripadvisor and Google.\n\nPhone: 928.814.2432 | Email: info@trekwest.net | 2404 E Route 66, Flagstaff, AZ 86004\n\n## Tours\n${Object.keys(TOURS).map((p) => `- [${(out.find((o) => o.path === p) || {}).title}](${site.url}${p})`).join('\n')}\n- [Book online](${site.url}/book-your-tour/)\n\n## Guides and answers\n- [FAQs](${site.url}/frequently-asked-questions/)\n- [About our guides](${site.url}/our-guides-the-trekwest-story/)\n- [Field Notes: planning, comparisons and trail notes](${site.url}/field-notes/)\n${out.filter((o) => o.kind === 'guide').map((o) => `- [${o.title}](${site.url}${o.path})`).join('\n')}\n`);
const sizeMB = (d) => { let t = 0; const w = (x) => { for (const e of readdirSync(x)) { const p = join(x, e); const s = statSync(p); s.isDirectory() ? w(p) : (t += s.size); } }; w(d); return (t / 1e6).toFixed(1); };
console.log(`built ${out.length} pages, ${used.size} assets, ${sizeMB(dist)} MB, ${warn} warnings`);
