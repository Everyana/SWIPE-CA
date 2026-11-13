# SWIPES Canada — Release gates

## Brand and trust
- Independent Canadian-focused public-information discovery product; do not present as a Government of Canada service.
- Maple-inspired SWIPES mark, editorial red / warm-white / charcoal palette.
- English and French labels and equivalent notice facts; human review for critical public instructions.
- Do not claim Canadian corporate ownership or government endorsement unless verified.
- All public-facing sample cards must be clearly identified as demonstrations.

## Release blockers before replacing the demonstration
1. Approved official-source registry with issuer name, jurisdiction, source URL, access method, owner, and verification date.
2. Ingestion that follows source terms, robots directives, and API limits; no unverified social or commercial press releases.
3. Each published card must have a specific primary-source notice URL, not a generic government homepage.
4. Record publication time, source time zone, update status, geography, and deadline when applicable.
5. Deduplicate, version corrections, detect expiry/cancellation, and provide a correction/reporting route.
6. Bilingual factual parity review; translation never invents eligibility, amounts, dates or application instructions.
7. Accessibility WCAG 2.2 AA checks, keyboard and screen reader testing, mobile reduced-motion checks.
8. Privacy policy, editorial/source policy, data freshness disclosure, and public contact.
9. Automated build checks, link checks, ingestion monitoring and failure alerts.
10. Verify domain, TLS, caching, and deployment rollback.

## Cost-aware architecture
- Keep GitHub for source control, code review, and static frontend publishing.
- For an initial low-volume pilot, a scheduled GitHub Actions job can fetch permitted official feeds, validate records, and commit generated static JSON.
- Avoid storing PDFs, videos, large images or raw source archives in Git.
- GitHub Pages is not a database or always-on API. Use a backend/database when real-time search, accounts, high-volume ingestion or editorial review needs it.
- Never store API keys in repository files or expose them in browser bundles.

## Release phases
A. Canadian identity and demo UI — in progress.
B. Verified registry + 10–20 official source integrations + data schema.
C. Review workflow + bilingual summaries + correction/expiry handling.
D. Search, location filters, accessibility, reliability, privacy, and production QA.
E. Gradual coverage expansion across provinces, territories, municipalities, and public institutions.
