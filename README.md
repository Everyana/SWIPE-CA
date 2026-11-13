# SWIPES — Canada Edition

Mobile-first bilingual React/Vite prototype for discovering public information.

> **Demonstration:** All five sample cards are fictional. This is not a live government news or notices feed.

## Run locally

```bash
npm install
npm run dev
```

## GitHub Pages deployment

This repository automatically builds and deploys the site from the `main` branch using `.github/workflows/deploy.yml`.

1. Set the repository to **Public** if using GitHub Pages on GitHub Free.
2. In **Settings → Pages**, select **GitHub Actions** as the build/deployment source.
3. The `public/CNAME` file configures the requested custom domain `ca.everyana.com`.
4. In **Settings → Pages → Custom domain**, set `ca.everyana.com` and save.
5. In the Cloudflare DNS zone for `everyana.com`, add:
   - Type: `CNAME`
   - Name: `ca`
   - Target: `everyana.github.io`
   - Proxy status: **DNS only** until GitHub Pages validates domain and TLS
6. After GitHub provisions a certificate, enable **Enforce HTTPS**.
7. Confirm the **Actions** run has passed and visit `https://ca.everyana.com`.

If GitHub Pages is disabled because the repository is private or your plan does not support private Pages, either make this repository public or choose a hosting option with private-repository support.

The Vite production output is `dist/`, and the custom-domain base path is `/`.

See `BLUEPRINT.md` for the production product specification and data ingestion plans.
