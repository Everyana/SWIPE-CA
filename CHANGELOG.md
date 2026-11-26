# Changelog
- Tests: Python unittest for the feed fetcher and Node tests for story pages; `npm test` runs both.
- CI workflow runs tests and the production build on every push and pull request.
- Fix: Atom feeds (Government of Canada EN/FR) lost every title and date because namespaced fields were read without the namespace map; federal notices return to the feed.
- Source registry: official sources now live in `scripts/sources.json` (issuer, level, access method, allowed hosts, verified date, status) instead of code.
- Statistics Canada marked blocked with reason: the old URL was a help page and the real RSS sits behind a browser challenge.
- Source health: each refresh writes `public/data/source-health.json` (status, items, last success, consecutive failures per source).
- Alerts: a source that fails 3 runs in a row opens a GitHub issue labelled source-health; it closes itself when the source recovers.
