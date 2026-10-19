# TrekWest Tours — trekwest.net

Static rebuild of the former WordPress/Divi site for TrekWest Arizona Adventure Tours (Flagstaff, AZ).
Dependency-free: a Node script assembles pages from partials into `dist/`; Netlify serves `dist/`.

## Commands
- `node build.mjs` — build `src/` into `dist/` (prints page/asset counts and any broken internal links or missing assets).
- Preview: `python3 -m http.server 8765 -d dist`.
- Netlify: build `node build.mjs`, publish `dist` (see `netlify.toml`). Netlify Forms handle all forms.

## Layout
- `src/pages/*.html` — one fragment per page, starting with `<!--meta {json} -->`. `kind` is `tour`, `post`, `info` or `raw`. Slug = filename = URL (`/slug/`), same URLs as the old WordPress site.
- `src/site.json` — site URL, GA id, `gscVerification` (Search Console token), per-URL description/priority/OG image/hero photo strips.
- `src/partials/` — `head.html` (title/meta/canonical/OG, GA4 `GT-P8Z9WDW5`, Search Console slot), `header.html`, `footer.html`. The only place to change analytics.
- `src/css/styles.css` (+ generated `fonts.css`, inlined at build) — one stylesheet, design tokens at the top.
- `src/js/main.js` — mobile nav, YouTube click-to-load facade, reduced-motion video pause.
- `src/img`, `src/og`, `src/video`, `src/fonts` — optimized assets; build copies only what pages reference.
- `scripts/` — one-off pipeline used for the migration (fetch-assets, optimize-images, extract, convert, make-og, fetch-fonts, shots). Not needed for normal edits.

## Design
Home page: full-bleed hero photo, split nav around a centered logo tile, photo-card grid of every tour, welcome band, stats, reviews block, confidence band, blog rows (modelled on westtrek.com's layout). Inner pages: slanted photo strips. Italic slant from the logo carried into photo strips, buttons, timeline marks and dividers. Blue/coral/plum from the logo, Aspen-gold booking button. Archivo (expanded, italic headings) + Source Serif 4, self-hosted.

## Booking
FareHarbor (shortname `trekwesttours`). Tour pages link to per-item lightframe URLs; `/book-your-tour/` embeds the item grid (flow 1634484). Floating mobile "Book a tour" bar links to it.

## Open items for the owner
See the hand-off list in the migration report: email/.com typo fixes already applied; FALL2026 promo text is kept verbatim; no cookie banner (privacy page mentions cookies); GSC verification token goes in `site.json`.

## Deploy record
- GitHub: github.com/davebussell/trekwest-net
- Netlify site: trekwest-net, site ID 69498b08-f0dc-49c6-9eb0-e8f373be9128, https://trekwest-net.netlify.app (deployed via Netlify MCP upload; connect the GitHub repo for continuous deploys)
