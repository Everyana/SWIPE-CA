# SWIPES Canada

SWIPES Canada is a mobile-first reader for selected notices from official Canadian sources. English and French interface labels are available. Notice titles and excerpts use the issuing source's language.

## Run locally

```sh
npm install
npm run dev
npm run build
```

The build output is in `dist/`. The reader checks the deployed JSON snapshot and the public GitHub feed on page load, every five minutes while visible, and when the visitor returns. It uses the newer available feed and keeps the last successful edition during a temporary fetch error.

## Refresh and publish

The GitHub refresh workflow runs every six hours and commits validated RSS and Atom notices to `public/data/notices.json`. Run `python scripts/fetch_official_feeds.py` for a manual refresh. Check the printed source failures and the feed coverage before publication. The jurisdiction filter lists all 10 provinces, all three territories, and federal notices. The About panel shows how many currently have published cards.

Hostinger serves the production domain. Publish the contents of `dist/` to that domain's document root. Deploying a new build publishes both the reader and the current feed snapshot. After the reader is deployed, scheduled feed commits can reach visitors through the public GitHub feed independently of frontend releases. New Brunswick currently uses time-limited, manually verified releases in `scripts/curated_notices.json`.
