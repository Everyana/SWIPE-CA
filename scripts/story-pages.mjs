// Builds one permanent page per notice, a stories index, sitemap.xml and robots.txt.
// Runs at the end of `vite build` (see vite.config.js). Reads the live feed plus the archive,
// so a notice keeps its page after it rotates out of the swipe feed.
import {mkdirSync, readFileSync, writeFileSync, existsSync} from 'node:fs';
import {join} from 'node:path';

const SITE = 'https://ca.everyana.com';
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const readJson = (p, fallback) => (existsSync(p) ? JSON.parse(readFileSync(p, 'utf8')) : fallback);

export function loadStories() {
  const live = readJson('public/data/notices.json', {notices: []}).notices || [];
  const archive = readJson('public/data/archive.json', {notices: []}).notices || [];
  const byId = new Map();
  for (const n of [...archive, ...live]) byId.set(n.id, {...byId.get(n.id), ...n});
  const liveIds = new Set(live.map((n) => n.id));
  return [...byId.values()]
    .map((n) => ({...n, inFeed: liveIds.has(n.id)}))
    .sort((a, b) => String(b.publishedAt).localeCompare(String(a.publishedAt)));
}

// A page is offered to search engines only when the summary is our own writing.
// Feed imports carry the issuer's opening text, which we link to but do not present as our article.
const indexable = (n) => Boolean(n.editorSummary);

const page = ({title, description, path, body, lang = 'en', robots = 'index,follow,max-image-preview:large', jsonLd = ''}) => `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>${esc(title)}</title><meta name="description" content="${esc(description)}"/><meta name="robots" content="${robots}"/><link rel="canonical" href="${SITE}${path}"/><link rel="icon" type="image/svg+xml" href="/favicon.svg"/><meta property="og:type" content="article"/><meta property="og:site_name" content="SWIPES Canada"/><meta property="og:url" content="${SITE}${path}"/><meta property="og:title" content="${esc(title)}"/><meta property="og:description" content="${esc(description)}"/><meta property="og:image" content="${SITE}/og-image.png"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/><meta name="twitter:card" content="summary_large_image"/>${jsonLd}<style>body{margin:0;background:#0a1926;color:#f5f1ea;font:17px/1.6 system-ui,sans-serif}main{max-width:720px;margin:0 auto;padding:28px 20px 64px}a{color:#f5f1ea}.k{color:#e94a3f;font-weight:700;letter-spacing:.08em;font-size:12px}.brand{font-weight:800;font-size:22px;text-decoration:none}h1{font-size:30px;line-height:1.2;margin:10px 0 14px}.meta{color:#e94a3f;font-weight:700;font-size:14px}.btn{display:inline-block;margin:18px 12px 0 0;padding:10px 16px;border:1px solid #e94a3f;border-radius:8px;text-decoration:none}ul{padding-left:18px}li{margin:8px 0}footer{color:#9aa3a8;font-size:13px;margin-top:40px}</style></head><body><main><a class="brand" href="/">SWIPES.</a><div class="k">CANADA EDITION · PUBLIC INFORMATION</div>${body}<footer>Independent public-information discovery. Not a government website. Notices link to the issuing source.</footer></main></body></html>`;

const storyPath = (n) => `/story/${n.id}/`;

export function writeStoryPages(outDir) {
  const stories = loadStories();
  const today = new Date().toISOString().slice(0, 10);
  for (const n of stories) {
    const date = String(n.publishedAt).slice(0, 10);
    const summary = n.editorSummary || n.summary;
    const related = stories.filter((o) => o.id !== n.id && o.jurisdiction === n.jurisdiction).slice(0, 5);
    const ld = indexable(n)
      ? `<script type="application/ld+json">${JSON.stringify({'@context': 'https://schema.org', '@type': 'Article', headline: n.title, datePublished: n.publishedAt, inLanguage: n.language, isBasedOn: n.url, publisher: {'@type': 'Organization', name: 'SWIPES Canada', url: SITE}})}</script>`
      : '';
    const body = `<p class="meta">${esc(n.jurisdiction)} · ${esc(n.category || 'Public updates')} · ${esc(date)}</p><h1>${esc(n.title)}</h1><p>${esc(summary)}</p>${n.inFeed ? '' : '<p><em>This notice is no longer in the live feed. Check the original for current details.</em></p>'}<p>Source: <strong>${esc(n.source)}</strong></p><a class="btn" href="${esc(n.url)}" target="_blank" rel="noopener">Read the original notice ↗</a><a class="btn" href="/#${encodeURIComponent(n.id)}">Open in SWIPES</a>${related.length ? `<h2>More from ${esc(n.jurisdiction)}</h2><ul>${related.map((o) => `<li><a href="${storyPath(o)}">${esc(o.title)}</a></li>`).join('')}</ul>` : ''}`;
    const dir = join(outDir, 'story', n.id);
    mkdirSync(dir, {recursive: true});
    writeFileSync(join(dir, 'index.html'), page({title: `${n.title} | SWIPES Canada`, description: String(summary).slice(0, 155), path: storyPath(n), body, lang: n.language === 'fr' ? 'fr' : 'en', robots: indexable(n) ? 'index,follow,max-image-preview:large' : 'noindex,follow', jsonLd: ld}));
  }
  const byJur = {};
  for (const n of stories) (byJur[n.jurisdiction] ||= []).push(n);
  const index = Object.keys(byJur).sort().map((j) => `<h2>${esc(j)}</h2><ul>${byJur[j].map((n) => `<li><a href="${storyPath(n)}">${esc(n.title)}</a> <small>${esc(String(n.publishedAt).slice(0, 10))}</small></li>`).join('')}</ul>`).join('');
  mkdirSync(join(outDir, 'stories'), {recursive: true});
  writeFileSync(join(outDir, 'stories', 'index.html'), page({title: 'All notices by province and territory | SWIPES Canada', description: 'Every official notice published on SWIPES Canada, grouped by province, territory and federal.', path: '/stories/', body: `<h1>All notices</h1>${index}`}));
  const urls = [{loc: '/', lastmod: today}, {loc: '/stories/', lastmod: today}, ...stories.filter(indexable).map((n) => ({loc: storyPath(n), lastmod: String(n.publishedAt).slice(0, 10)}))];
  writeFileSync(join(outDir, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${SITE}${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>`).join('\n')}\n</urlset>\n`);
  writeFileSync(join(outDir, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: ${SITE}/sitemap.xml\n`);
  return {pages: stories.length, indexed: stories.filter(indexable).length};
}
