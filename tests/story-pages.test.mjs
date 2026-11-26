import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {writeStoryPages, loadStories} from '../scripts/story-pages.mjs';

test('story pages, sitemap and robots are written', () => {
  const out = mkdtempSync(join(tmpdir(), 'swipes-'));
  const r = writeStoryPages(out);
  const stories = loadStories();
  assert.equal(r.pages, stories.length);
  assert.ok(r.indexed > 0 && r.indexed <= r.pages);
  const sitemap = readFileSync(join(out, 'sitemap.xml'), 'utf8');
  assert.equal((sitemap.match(/<loc>/g) || []).length, r.indexed + 4);
  assert.ok(existsSync(join(out, 'robots.txt')));
  assert.ok(existsSync(join(out, 'stories', 'index.html')));
});

test('only pages with our own summary are indexable', () => {
  const out = mkdtempSync(join(tmpdir(), 'swipes-'));
  writeStoryPages(out);
  for (const s of loadStories().slice(0, 40)) {
    const html = readFileSync(join(out, 'story', s.id, 'index.html'), 'utf8');
    const robots = html.match(/name="robots" content="([^"]+)"/)[1];
    assert.equal(robots.startsWith('index'), Boolean(s.editorSummary), s.id);
  }
});

test('a notice with a deadline shows it on its story page', () => {
  const out = mkdtempSync(join(tmpdir(), 'swipes-'));
  writeStoryPages(out);
  const withDeadline = loadStories().find((s) => s.deadline);
  if (!withDeadline) return; // feed has no deadline notices right now
  const html = readFileSync(join(out, 'story', withDeadline.id, 'index.html'), 'utf8');
  assert.match(html, new RegExp(`datetime="${withDeadline.deadline}"`));
});

test('story pages carry the disclaimer, a correction link and the last-checked date', () => {
  const out = mkdtempSync(join(tmpdir(), 'swipes-'));
  writeStoryPages(out);
  const s = loadStories()[0];
  const html = readFileSync(join(out, 'story', s.id, 'index.html'), 'utf8');
  assert.match(html, /not affiliated with or endorsed by any government/);
  assert.match(html, /href="mailto:hello@everyana\.com\?subject=SWIPES%20correction/);
  assert.match(html, /Last checked against the source feed: \d{4}-\d{2}-\d{2}/);
  assert.match(html, /href="\/about\/"/);
});

test('about and sources pages are built from the registry', () => {
  const out = mkdtempSync(join(tmpdir(), 'swipes-'));
  writeStoryPages(out);
  const sources = readFileSync(join(out, 'sources', 'index.html'), 'utf8');
  const reg = JSON.parse(readFileSync('scripts/sources.json', 'utf8')).sources;
  for (const r of reg) assert.ok(sources.includes(r.name.replace(/&/g, '&amp;')), r.name);
  assert.match(sources, /Not fetched/); // Statistics Canada is blocked
  const about = readFileSync(join(out, 'about', 'index.html'), 'utf8');
  assert.match(about, /Corrections/);
  assert.match(about, /Privacy/);
  assert.match(about, /not affiliated with or endorsed by any government/);
});
