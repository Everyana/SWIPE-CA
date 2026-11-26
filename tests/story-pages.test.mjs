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
  assert.equal((sitemap.match(/<loc>/g) || []).length, r.indexed + 2);
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
