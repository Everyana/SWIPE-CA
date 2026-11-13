# SWIPES — Canada Edition

A GitHub-ready, mobile-first proof-of-concept for a bilingual public-information swipe reader.

## Run locally

```bash
npm install
npm run dev
```

Open the local URL printed by Vite. Build with `npm run build`.

## Included

- Responsive, full-height, snap-scrolling swipe cards
- English/French interface and content toggle
- Topic and jurisdiction filters
- Search, bookmarking, sharing, keyboard navigation
- Source links and clearly marked sample content
- Installable PWA manifest and offline app shell (after first visit)
- No external data collection or analytics in the demo

## Important

The included stories are **fictional interface examples**, not current public notices. This prototype does not claim live coverage, ingest government sources, publish news automatically, send alerts, or provide a production CMS. See `BLUEPRINT.md` for the full production design, implementation phases and acceptance criteria.

## Production stack recommendation

Next.js + TypeScript, PostgreSQL/PostGIS, Redis, background workers, object storage, OpenSearch, OAuth/OIDC, observability, GitHub Actions, IaC. See the blueprint for specifics.
