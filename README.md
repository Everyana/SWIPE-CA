# SWIPES Canada

A mobile-first reader for notices from official Canadian government and public-institution sources, live at https://ca.everyana.com. English and French interface. Notice titles and excerpts keep the issuing source's language; summaries written by SWIPES are labelled.

## Run locally

```sh
npm install
npm run dev          # local reader
npm test             # Python fetcher tests + Node story-page tests
npm run build        # dist/ with reader, story pages, /about/, /sources/, sitemap
npm run check:dist   # post-build checks (title, robots, canonical, sitemap)
```

## How data flows

1. `scripts/sources.json` is the source registry: issuer, jurisdiction, level, language, URL, access method (`rss`, `atom`, `page:*`, `json:gnb`), allowed link hosts, verified date and status. Only `active` sources are fetched; `blocked` ones carry a note.
2. `.github/workflows/refresh-notices.yml` runs `scripts/fetch_official_feeds.py` every six hours. It keeps only https links on the source's own domains, drops media advisories and itineraries, tags topics, pulls explicit deadlines, removes duplicates, keeps 40 cards (one per jurisdiction first) and carries a failed source's cards for 14 days.
3. It writes `public/data/notices.json` (live feed), `public/data/archive.json` (every notice ever shown, so story pages stay online) and `public/data/source-health.json` (per-source status and consecutive failures), then commits them.
4. `scripts/source_alerts.py` opens a GitHub issue (label `source-health`) when a source fails three runs in a row and closes it when it recovers.
5. Hostinger Git auto-deploy builds `main` and publishes `dist/`. The reader also reads the newest feed from GitHub, so scheduled data reaches visitors without a code release.

`scripts/curated_notices.json` holds hand-verified notices with an expiry date. `public/data/editor-summaries.json` holds our own summaries; only notices with one get an indexable story page.

## Checks

- `ci.yml`: tests, build and build-output checks on every push and pull request.
- `link-check.yml`: weekly request of every card link; broken links open an issue (`link-check`).

## Known source gaps

Statistics Canada (RSS behind a browser challenge) and Nunavut (403 to automated clients) are marked blocked in the registry; see `/sources/` on the live site.
