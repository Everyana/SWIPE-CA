// Post-build checks on the published files. Exits non-zero on the first problem found.
import {readFileSync, existsSync} from 'node:fs';
const fail = (m) => { console.error('check-dist: ' + m); process.exit(1); };
const html = readFileSync('dist/index.html', 'utf8');
const count = (re) => (html.match(re) || []).length;
if (count(/<meta name="robots"/g) !== 1) fail('index.html must have exactly one robots meta');
if (count(/<title>/g) !== 1) fail('index.html must have exactly one <title>');
if (!html.includes('<title>SWIPES Canada — Official Public Updates</title>')) fail('title not set by prerender');
if (count(/<link rel="canonical"/g) !== 1) fail('index.html must have one canonical');
for (const p of ['og:title', 'og:description', 'og:image', 'twitter:card']) if (!html.includes(p)) fail(`missing ${p}`);
if (!html.includes('<article>')) fail('no pre-rendered notices in index.html');
for (const f of ['dist/sitemap.xml', 'dist/robots.txt', 'dist/stories/index.html', 'dist/data/notices.json']) if (!existsSync(f)) fail(`missing ${f}`);
const sm = readFileSync('dist/sitemap.xml', 'utf8');
if (!/<urlset/.test(sm) || (sm.match(/<loc>/g) || []).length < 2) fail('sitemap looks empty');
console.log('check-dist: ok');
