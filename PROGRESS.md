# SWIPES Canada — progress (autopilot)
Sources: BLUEPRINT.md (BP §n), LAUNCH_CHECKLIST.md (LC #n), README.md, project docs 14/14b/14d (WEBSITE), code audit 25 Nov 2026.
Legend: ⬜ todo · 🚧 in progress · ✅ done + checks pass · ⛔ needs owner (see QUESTIONS.md)

## Already working (audit)
- ✅ Vertical swipe reader, EN/FR UI, search, topic + jurisdiction filters, saves, share — BP §7, Phase 1
- ✅ "No cards match" only shown when a filter is active; Clear resets — doc 14 bug list
- ✅ About panel with real text, independence disclaimer, coverage count — doc 14
- ✅ Story pages /story/<id>/, /stories/, sitemap, robots, noindex until own summary — BP §13
- ✅ Scheduled ingestion every 6 h with official-domain check, dedupe, archive — LC #2/#3, BP §12
- ✅ Hostinger Git auto-deploy on main — LC #10
- ✅ Search Console + Bing verified, sitemap submitted — BP §13

## Queue (priority order)
1. ✅ Test harness: Python unittest for fetcher + Node test for story pages; `npm test` — BP §16 (CI green)
2. ⬜ CI workflow: tests + build on push/PR — BP §16, LC #9
3. ⬜ Fix Atom parsing (namespaced title/summary/date lost → GC en/fr feed 0 items) — audit (14b)
4. ⬜ Source registry file `scripts/sources.json` (issuer, jurisdiction, level, url, access, hosts, verified date, status) — LC #1, BP §4
5. ⬜ StatCan: wrong URL (HTML page) + bot challenge on RSS → mark source blocked in registry with reason — audit
6. ⬜ Source health file `public/data/source-health.json` + consecutive-failure tracking — BP §12/§15, LC #9
7. ⬜ Failure alert: open/update a GitHub issue when a source fails 3 runs in a row — BP §16 Ops
8. ⬜ Deadline extraction (deadline/closing/until dates) → `deadline` on cards — BP §6, 14d #19
9. ⬜ Reader shows our editor summary when present, labels source excerpt — BP §6, 14d #3
10. ⬜ Topic patterns: reduce "Public updates" catch-all — BP §5
11. ⬜ Prerender fixes: title replace never matches; duplicate robots meta — audit
12. ⬜ Accessibility: skip link, focus-visible, reduced motion, live region for card position — BP §14, LC #7
13. ⬜ Story pages: exact disclaimer + "Report a correction" link + last-checked date — BP §6/§14, LC #5
14. ⬜ /sources/ page generated from registry + health (transparency) — BP §14, LC #8
15. ⬜ /about/ editorial + corrections + privacy notice page — LC #8, BP §14
16. ⬜ Weekly link checker workflow (card source URLs) — LC #9, BP §16
17. ⬜ Remove unused GitHub Pages deploy workflow — audit
18. ⬜ New Brunswick official feed — README, audit
19. ⬜ Nunavut 403 on runner: retry with browser-like headers; else mark blocked — audit
20. ⬜ README refresh (architecture, sources, tests, ops) — README
21. ⬜ C15 editor summaries batch 4 for new feed items — doc 14

## Needs owner
- ⛔ Login gate (guest first few cards) vs "official info always free" — 00 §4 vs 14d
- ⛔ Accounts, push/email deadline alerts (backend + privacy) — BP Phase 4
- ⛔ Municipal sources Abbotsford/Langley inside ca edition vs own editions — 14b
- ⛔ Legal review of privacy/editorial text — BP §14
