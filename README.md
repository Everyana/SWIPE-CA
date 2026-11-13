# Swipes Canada

Swipes Canada is an independent reader for Canadian public notices and updates. Readers can search, filter, bookmark and open the issuing agency's original notice. The interface supports English and French. Curated summaries may be available in both languages, and notices imported from public feeds retain the source language.

## Build

Run `npm install`, then `npm run build`. Vite writes the static site to `dist/`. Use `npm run dev` for local development.

## Feed and publishing

`public/data/notices.json` contains the public feed. The refresh script pulls from configured public feeds and keeps curated cards whose IDs start with `editorial-`. The published site displays the latest feed snapshot deployed to its host. See the source links on each card for current details and deadlines.

Production serves the built site at https://ca.everyana.com/ on Hostinger. A GitHub Pages deployment does not update that Hostinger installation.
