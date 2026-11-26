# Changelog
- Tests: Python unittest for the feed fetcher and Node tests for story pages; `npm test` runs both.
- CI workflow runs tests and the production build on every push and pull request.
- Fix: Atom feeds (Government of Canada EN/FR) lost every title and date because namespaced fields were read without the namespace map; federal notices return to the feed.
