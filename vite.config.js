import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {readFileSync} from 'node:fs';
import {writeStoryPages} from './scripts/story-pages.mjs';

const SITE = 'https://ca.everyana.com/';
const TITLE = 'SWIPES Canada — Official Public Updates';
const DESC = 'Selected notices from official Canadian sources, one swipe at a time. Browse by topic or province and open the original notice.';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

// Writes sharing tags and the newest notices into index.html at build time,
// so the first paint and link previews never depend on JavaScript.
function prerender() {
  return {
    name: 'swipes-prerender',
    transformIndexHtml(html) {
      let notices = [];
      try {
        const feed = JSON.parse(readFileSync('public/data/notices.json', 'utf8'));
        notices = (feed.notices || [])
          .slice()
          .sort((a, b) => String(b.publishedAt).localeCompare(String(a.publishedAt)))
          .slice(0, 12);
      } catch {
        notices = [];
      }
      const head = [
        `<link rel="canonical" href="${SITE}"/>`,
        `<meta name="robots" content="index,follow,max-image-preview:large"/>`,
        `<meta property="og:type" content="website"/>`,
        `<meta property="og:site_name" content="SWIPES Canada"/>`,
        `<meta property="og:locale" content="en_CA"/>`,
        `<meta property="og:locale:alternate" content="fr_CA"/>`,
        `<meta property="og:url" content="${SITE}"/>`,
        `<meta property="og:title" content="${esc(TITLE)}"/>`,
        `<meta property="og:description" content="${esc(DESC)}"/>`,
        `<meta property="og:image" content="${SITE}og-image.png"/>`,
        `<meta property="og:image:width" content="1200"/>`,
        `<meta property="og:image:height" content="630"/>`,
        `<meta property="og:image:alt" content="SWIPES Canada edition: public information, one swipe at a time"/>`,
        `<meta name="twitter:card" content="summary_large_image"/>`,
        `<meta name="twitter:title" content="${esc(TITLE)}"/>`,
        `<meta name="twitter:description" content="${esc(DESC)}"/>`,
        `<meta name="twitter:image" content="${SITE}og-image.png"/>`,
        `<link rel="preload" href="/data/notices.json" as="fetch" crossorigin="anonymous"/>`,
        `<style>.pr{background:#0a1926;color:#f5f1ea;font:16px/1.5 system-ui,sans-serif;min-height:100vh;padding:24px}.pr h1{font-size:28px;margin:0 0 4px}.pr p.k{color:#e94a3f;font-weight:700;letter-spacing:.08em;font-size:12px;margin:0 0 20px}.pr article{border-top:1px solid #23384a;padding:16px 0;max-width:760px}.pr small{color:#e94a3f;font-weight:700}.pr h2{font-size:20px;margin:4px 0}.pr a{color:#f5f1ea}</style>`,
      ].join('');
      const cards = notices
        .map((n) => `<article><small>${esc(n.jurisdiction)} · ${esc(String(n.publishedAt).slice(0, 10))}</small><h2>${esc(n.title)}</h2><p>${esc(n.summary)}</p><a href="${esc(n.url)}" rel="noopener" target="_blank">${esc(n.source)} — read the original notice</a></article>`)
        .join('');
      const body = `<div class="pr"><h1>SWIPES.</h1><p class="k">CANADA EDITION · PUBLIC INFORMATION</p>${cards}</div>`;
      return html
        .replace('<title>SWIPES | Do the Swipe</title>', `<title>${esc(TITLE)}</title>`)
        .replace('</head>', `${head}</head>`)
        .replace('<div id="root"></div>', `<div id="root">${body}</div>`);
    },
  };
}

function storyPages() {
  let outDir = 'dist';
  return {
    name: 'swipes-story-pages',
    apply: 'build',
    configResolved(config) { outDir = config.build.outDir; },
    closeBundle() {
      const r = writeStoryPages(outDir);
      console.log(`story pages: ${r.pages} written, ${r.indexed} indexable`);
    },
  };
}

export default defineConfig({plugins: [react(), prerender(), storyPages()]});
