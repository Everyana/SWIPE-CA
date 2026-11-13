# SWIPES — Universal Public Information Platform
## Master product, editorial, source, technical and operating blueprint
**Deployment configuration:** Canada | **Languages:** English (en-CA) and French (fr-CA) | **Version:** 1.0 | **Date:** 12 November 2026

> **Deployment-neutral design:** All jurisdictions, official bodies, languages, time zones, regulatory regimes, domains, source priorities and geographic boundaries are tenant configuration, not hard-coded platform assumptions. Canada is the initial tenant profile, not a limitation of the product.

---

# 1. Executive mandate

**Product name:** SWIPES. **Content unit:** a Swipe. **Primary action:** Swipe. **Reader invitation:** Do the Swipe. **Social language:** I Swiped; Swipe to Know; Worth a Swipe; Your Daily Swipes. **French localization candidates:** Faites défiler; À découvrir en un geste; Je l’ai vu sur SWIPES. French copy must be editorially reviewed; do not mechanically translate the brand name or imply that *swiper* is universally understood.

**Mission:** Turn fragmented, official public information into timely, accessible, sourced, multilingual, actionable Swipes.

**Vision:** The default destination for discovering what public institutions have announced, decided, opened, closed, funded, published, scheduled, recruited, regulated or changed, from neighborhood to national level.

**Audience:** Residents, jobseekers, students, parents, researchers, journalists, community organizations, public employees, entrepreneurs seeking **public** procurement opportunities, athletes, applicants, commuters and visitors. Information is open to all; no paywall on essential public notices.

**What it is:** A public-information discovery, contextualization and navigation platform. It links to the issuing authority for applications, payments, tenders, registrations and authoritative details. **What it is not:** a government agency, an official government website, an application processor, a substitute for legal notices, a political campaign, a private-company press release feed, or a privately sponsored advertorial service.

**Editorial scope rule:** Publish announcements **originating from, formally issued by, or officially adopted by** public bodies or publicly accountable institutions. A public institution reporting a private-sector initiative is eligible only where the **public decision, program, regulation, award or expenditure** is the actual news. Do not publish private promotional material, unofficial aggregators, commercial press releases, political party messaging or unverified social media rumors. Public universities, hospitals, school boards and publicly funded cultural/sport bodies are eligible when the source is their official institutional channel. Private contractors can appear as factual parties to an official public tender or award; that does not make their marketing eligible.

**Value proposition:** “Everything public that matters to you, in one swipeable place.” No false claim of literally exhaustive coverage: measure source coverage and gaps transparently.

---

# 2. Non-negotiable product principles

1. **Source-first:** Every factual Swipe links to a specific primary source item, not just an agency homepage or general press-room index.
2. **Bilingual parity:** English and French content convey equivalent facts, dates, conditions and caveats. Neither is a machine-generated afterthought.
3. **Mobile-first, app-grade:** Full-screen cards, gesture-based continuous feed, smooth loading, persistent header, stable scroll, accessibility and offline-friendly saved cards.
4. **One card, one useful development:** Distill the user-impacting point, preserve essential qualification, attach dates and geography.
5. **Actionable:** For jobs, tenders, grants and admissions, show who, where, what, when, how, status and source.
6. **No duplication:** A source item can have multiple updates; canonicalize the underlying event and show a version history.
7. **Neutrality:** Inform, don't advocate. Label government claims and projections as claims, not independent findings.
8. **Timeliness and correction:** Detect changes, expiry, cancellations and corrections; preserve audit trails.
9. **Public-sector-only ingestion:** No private sponsored coverage, private newswires or paid influence in editorial ranking.
10. **Local relevance without isolation:** A reader may see municipal, regional, provincial/territorial, federal and cross-border public notices in one feed.
11. **Inclusive:** WCAG 2.2 AA, plain-language summaries, readable typography, reduced-motion controls and screen-reader navigation.
12. **Transparent operation:** Source directory, publication policy, correction policy, data freshness, sponsorship disclosure if monetization is ever enabled.

---

# 3. Information universe: every layer and direction

## 3.1 Jurisdiction hierarchy

- **National/federal:** Head of government, cabinet, executive offices, parliament, upper/lower houses, departments, ministries, statutory bodies, national agencies, independent regulators, auditors, courts' public administrative notices, commissions, central public corporations and federally funded institutions.
- **Province/state/territory:** Premiers/heads of government, legislative assemblies, ministries, agencies, provincial regulators, public utilities, education and health authorities, courts' administrative announcements, provincial public corporations and grant programs.
- **Regional/intermediate:** Regional districts, counties, metropolitan authorities, development regions, planning districts, public health regions, transit regions, conservation/watershed authorities and intermunicipal partnerships.
- **Municipal/local:** Cities, towns, townships, villages, districts, boroughs, wards, local councils, public libraries, parks, local emergency services, recreation and arts offices, municipal utilities, public consultation portals and local boards.
- **Special-purpose public bodies:** School districts, public colleges, universities, research institutes, hospitals, health systems, transit agencies, ports, airports operated by eligible public authorities, housing authorities, energy/water agencies, conservation authorities, sports councils, museums, archives, public broadcasters and publicly governed cultural bodies.
- **Indigenous governments:** First Nations, Inuit and Métis governing institutions and their officially published notices, with respect for their jurisdiction, naming and community-specific information-sharing protocols; do not assume all materials are intended for general republication.
- **International/intergovernmental:** Only official announcements directly relevant to the configured location (e.g. bilateral programs, treaties, international public bodies), labeled by jurisdiction and issuing authority.

**Horizontal coverage:** Every ministry, agency and body at a given level. **Vertical coverage:** The same subject (e.g. education, transport, health) through every level, from national policy to local implementation. **Cross-cutting:** Budgets, consultations, recruitment, procurement, compliance, funding, service disruptions, data releases and results across every body.

## 3.2 Public-sector source categories — exhaustive discovery taxonomy

| Family | Bodies / channels to discover | What to extract |
|---|---|---|
| Executive | Cabinet offices, PM/premier/mayor offices, official briefings | Decisions, orders, priorities, visits, speeches clearly labeled |
| Legislative | Parliament, legislatures, committees, municipal council agendas/minutes | Bills, votes, hearings, committee reports, bylaws, meetings |
| Ministries | All departments and portfolios, current and renamed | News releases, consultations, regulations, grants, programs |
| Regulators | Financial, telecom, transport, energy, food, drugs, privacy, competition, labour | Orders, recalls, enforcement, compliance dates, licenses |
| Recruitment | Public service commissions, agency careers, municipal careers, boards | Openings, classifications, salary, location, eligibility, close dates |
| Exams / selection | Testing bodies, certification authorities, civil service exams, public schools | Schedules, applications, admit cards, results, interviews, merit lists |
| Education | Ministries, school boards, public colleges, universities, admissions, research councils | Admissions, deadlines, scholarships, curriculum, closures, grants |
| Procurement | National and subnational tender portals, agency bids | RFP/RFQ/RFI, addenda, awards, vendor sessions, cancellations |
| Finance | Treasury, finance ministries, tax agencies, budget offices | Budgets, taxation, spending, benefit changes, financial reports |
| Public safety | Emergency management, fire, police public advisories, civil defence | Warnings, evacuations, safety guidance, exercises, public notices |
| Health | Health ministries, public health, public hospitals, regulators | Advisories, vaccination, facilities, service changes, studies |
| Housing | Housing agencies, planning boards, municipal housing | Programs, applications, developments, zoning, public hearings |
| Transport | Roads, rail, transit, aviation, marine, ports | Route changes, closures, projects, fares, schedules, safety notices |
| Infrastructure | Public works, utilities, engineering, asset management | Construction, tenders, outages, capital plans, commissioning |
| Environment | Climate, parks, forestry, fisheries, water, conservation | Alerts, permits, studies, wildlife, grants, consultations |
| Agriculture | Agriculture ministries, extension agencies, food inspection | Grants, programs, advisories, crop reports, training |
| Labour | Employment standards, workplace safety, training boards | Standards, benefits, apprenticeship, occupational guidance |
| Immigration | Official immigration departments and provincial programs | Program changes, application windows, official invitations, notices |
| Justice | Courts' administrative notices, legal aid, justice ministries | Public process changes, filing rules, official service updates |
| Indigenous affairs | Indigenous governments and public departments | Public programs, agreements, consultations, funding |
| Social services | Benefits, disability, seniors, children, families, veterans | Eligibility, applications, benefit dates, service changes |
| Science / technology | Research councils, space agencies, statistics agencies, public labs | Findings, grants, datasets, competitions, research programs |
| Digital / data | Open-data portals, cyber centres, digital-service teams | Datasets, APIs, security advisories, digital service changes |
| Sport / fitness | Public sport agencies, national/provincial bodies, city recreation | Competitions, facilities, registrations, grants, public events |
| Arts / entertainment | Public arts councils, museums, galleries, film boards, broadcasters | Festivals, exhibitions, screenings, public calls and grants |
| Tourism / heritage | Official tourism agencies, parks, heritage institutions | Public festivals, visitor notices, preservation projects |
| Elections / civic | Election authorities, ethics commissioners, public consultations | Registration, election dates, hearings, participation opportunities |
| Utilities / energy | Public utilities, energy regulators, water/sewer | Rates, outages, hearings, projects, conservation programs |
| Trade / economy | Trade commissions, export agencies, economic development | Programs, trade notices, public funding, market reports |
| Libraries / archives | Public libraries, archives, records offices | Programs, digitization, access changes, exhibitions |
| Municipal services | Waste, recycling, permits, animal services, parking, recreation | Service calendars, rule changes, closures, consultations |
| Reports / datasets | Auditors, ombuds, statistics, research offices | Reports, audits, dashboards, survey releases, data revisions |

## 3.3 Communications to monitor (not just “newsrooms”)

Official newsroom articles; press releases; media advisories; public notices; gazettes; regulatory bulletins; orders in council; laws and amendments; legislative calendars; meeting agendas, minutes and decisions; tender notices, bid addenda and award results; procurement RSS and APIs; grants calls; program guidelines; scholarships; competitions; challenge calls; application forms; recruitment boards; vacancy notices; job listings; exam timetables; admit-card announcements; answer keys; provisional/final results; interview lists; counselling rounds; waitlists; admissions portals; public dashboards; annual/quarterly reports; audits; open datasets; statistical tables; service alerts; road closures; transit alerts; emergency warnings; consultations; public hearings; newsletters; official calendars; institutional event listings; official blogs; accessible public PDFs; publicly released maps; official YouTube transcripts/videos; official social posts **only when the account is verified as an official institution and the post is the primary announcement or links to it**; official podcasts with transcripts; archival notices when still operationally relevant.

**Update detection:** Published, amended, extended, corrected, suspended, withdrawn, cancelled, reopened, results issued, award issued, deadline passed, event completed, superseded. A notice may be important even when it does not have a newsroom article.

---

# 4. Canada source registry — initial configuration

Canada has federal, 10 provincial, 3 territorial and extensive municipal/Indigenous/public-institution layers. Registry entries must be discovered and maintained; this is a **seed directory**, not a claim of complete live source enrollment.

## 4.1 Federal seed authorities and primary hubs

- Government of Canada (`canada.ca`): departmental news, notices, consultations, grants, services, regulations.
- Government of Canada news (`canada.ca/en/news.html`) and individual department newsrooms.
- Canada Gazette (`gazette.gc.ca`): regulations and official notices.
- Parliament of Canada (`parl.ca`), House of Commons (`ourcommons.ca`), Senate (`sencanada.ca`): bills, committee notices and proceedings.
- Public Service Commission / GC Jobs (`jobs.gc.ca` and official Government of Canada job pathways): federal jobs, hiring and tests.
- CanadaBuys (`canadabuys.canada.ca`): procurement notices, bid opportunities, amendments and awards.
- Open Government (`open.canada.ca`): datasets, proactive disclosures, consultations.
- Statistics Canada (`statcan.gc.ca`): official releases, tables and census data.
- Treasury Board Secretariat, Department of Finance, Canada Revenue Agency, Employment and Social Development Canada / Service Canada, Immigration Refugees and Citizenship Canada, Global Affairs Canada, Public Services and Procurement Canada, Innovation Science and Economic Development Canada.
- Health Canada, Public Health Agency of Canada, Canadian Food Inspection Agency, Canadian Institutes of Health Research.
- Transport Canada, Canadian Transportation Agency, Canadian Air Transport Security Authority, NAV CANADA **only when qualifying as an official public-interest authority source**; distinguish corporate and government status.
- Environment and Climate Change Canada, Parks Canada, Fisheries and Oceans Canada, Natural Resources Canada, Canadian Energy Regulator, Impact Assessment Agency.
- Agriculture and Agri-Food Canada, Canadian Grain Commission, Farm Credit Canada (public Crown corporation).
- Department of National Defence / Canadian Armed Forces, Veterans Affairs Canada, Public Safety Canada, Emergency Management, RCMP official releases, Canadian Centre for Cyber Security.
- Canadian Radio-television and Telecommunications Commission, Competition Bureau, Office of the Privacy Commissioner, Auditor General, Elections Canada, Canadian Human Rights Commission.
- Indigenous Services Canada, Crown-Indigenous Relations, official Indigenous governing bodies (subject to publication protocols).
- Canadian Heritage, Canada Council for the Arts, National Film Board, National Arts Centre, Library and Archives Canada, Canadian Museum institutions, Sport Canada, public broadcasting entities (editorial restrictions below).
- Canadian Space Agency, National Research Council, Natural Sciences and Engineering Research Council, Social Sciences and Humanities Research Council.
- Official federal courts and tribunals' **administrative** notices, not unsolicited publication of sensitive personal case details.

**Qualification:** Being government-owned or publicly funded does not automatically make every corporate, editorial or third-party item suitable. Ingest only official institutional notices and announcements meeting the public-information test.

## 4.2 Provincial and territorial government portals

| Jurisdiction | Primary government entry point |
|---|---|
| Alberta | alberta.ca |
| British Columbia | gov.bc.ca |
| Manitoba | gov.mb.ca |
| New Brunswick | gnb.ca |
| Newfoundland and Labrador | gov.nl.ca |
| Nova Scotia | novascotia.ca |
| Ontario | ontario.ca |
| Prince Edward Island | princeedwardisland.ca |
| Québec | quebec.ca |
| Saskatchewan | saskatchewan.ca |
| Northwest Territories | gov.nt.ca |
| Nunavut | gov.nu.ca |
| Yukon | yukon.ca |

For **each** jurisdiction register: cabinet/premier, every ministry and successor department, provincial legislature, public-service careers, public procurement, provincial gazette/regulations, courts' administrative news, health authorities, school boards, public colleges/universities, public agencies, utilities, sport and arts councils, parks, emergency alerts, statistical agencies, local government associations, public transit and public consultation portals. Support English/French plus Indigenous-language content where rights and editorial capability permit; Canada launch's guaranteed editorial languages are English and French.

## 4.3 Municipal, regional and local discovery

Do **not** manually hard-code a few popular cities and declare Canada covered. Build authoritative locality inventory from official provincial municipal registries and Statistics Canada geographic codes. For every municipality and region discover official domains, departments, council meeting portals, local job boards, tender portals, event calendars, libraries, parks, recreation, fire/emergency notices, planning/zoning, public works, transit and public consultation channels. Include special-purpose local boards and public institutions. Maintain official source ownership verification and last-check timestamps.

## 4.4 Public education, sport, culture and research

Discover every public school district/board; public universities and colleges; student aid offices; research institutes; provincial athletic organizations with public mandates; public recreation authorities; government-supported museums, archives, arts councils, film offices and festivals **only for their own official institutional notices**. University student clubs and privately operated events are not automatically eligible. Editorial content from public broadcasters is not automatically a government announcement and should not be bulk-copied.

---

# 5. Taxonomy and content types

**Top-level navigation:** For You, Latest, Local, Jobs, Exams & Admissions, Grants & Benefits, Tenders, Public Notices, Civic & Council, Education, Health, Transport, Infrastructure, Environment, Agriculture, Science & Technology, Sports & Recreation, Arts & Culture, Events, Reports & Data, Safety & Alerts, Saved, Deadlines.

**Primary content types:** `announcement`, `job`, `exam`, `admission`, `scholarship`, `grant`, `benefit`, `tender`, `procurement_award`, `consultation`, `hearing`, `meeting`, `event`, `competition`, `training`, `policy`, `regulation`, `budget`, `report`, `dataset`, `service_alert`, `emergency`, `result`, `appointment`, `infrastructure_project`, `public_program`, `correction`, `other_public_notice`.

**Required universal fields:** stable ID, type, canonical event ID, title EN/FR, summary EN/FR, issuing organization ID, government level, geographic applicability, source item URL, source document ID/hash, source published date/time/time zone, ingested date, last verified date, status, topic, verification state, editorial author/reviewer, revision history, accessibility/translation state.

**Conditional structured fields:** opening and closing dates, timezone, fee, salary, pay range, position count, vacancy ID, employer, workplace, job category, eligibility, age/education restrictions, application route, tender ID, procurement category, bid meeting date, contract value, submission method, exam stage, admit-card URL, result URL, course/institution, event venue, accessibility accommodations, cancellation reason, consultation method, geographic boundaries, expiry rules.

**Freshness model:** `upcoming`, `open`, `closing_soon`, `closed`, `completed`, `superseded`, `cancelled`, `archived`, `unknown`. Never infer “open” merely because a page exists. Store authoritative source timezone and render in user locale with timezone shown at deadlines.

---

# 6. The Swipe: canonical content template

A Swipe must answer **What happened? Who issued it? Who is affected? Where? When? What action is needed? Where is the original?**

**Card front:** Topic badge; jurisdiction; issuing authority; source publication date; concise factual headline; 2–5 short sentences; critical deadline or impact; status label; official source button; Save, Share and Read Full. Optional photo only if relevant and rights-cleared; no generic AI faces or synthetic documentary imagery. Image-less cards must remain premium.

**Full view:** Same global header and navigation; complete original-source context in plain language; eligibility, steps, documents, deadline, source URL, amendment history, bilingual switch, related official updates, correction request, last checked. Return to exactly the same card and scroll position. Full view is not a separate broken theme.

**Examples of structured formats:**
- **Job:** Position | Organization | Location | Salary if officially given | Vacancies | Qualifications | Deadline | Apply at official site.
- **Tender:** Tender ID | Buyer | Scope | Mandatory briefing | Closing date/time/timezone | Addenda | Official tender portal.
- **Exam:** Exam authority | Eligibility | Registration window | Exam date | Admit card | Results | Official notice.
- **Grant:** Program | Beneficiary | Amount if published | Conditions | Window | Apply.
- **Public meeting:** Authority | Agenda | Location/virtual link | Public participation instructions | Date/time.
- **Emergency:** Verified alert | Area | Severity | Timestamp | Official safety action | Expiry/update status. Emergency cards require special priority, rapid refresh and a clear notice that authoritative alerts govern.

**Writing:** No hype, unsupported superlatives, false urgency, speculative predictions or claims that a proposal is approved. Identify whether amounts are proposed, budgeted, awarded or spent. Preserve units and dates. A title is not enough: summarize useful information, not just a press release headline.

---

# 7. Design system and premium reader behavior

## 7.1 Visual identity

**Brand:** SWIPES; strong typographic wordmark, distinctive directional/swipe motif; avoid resembling government seals or implying official affiliation. **Visual tone:** editorial, premium, modern, calm, trustworthy, lively in interaction, restrained in typography. **Proposed palette:** midnight navy `#08141E`, deep slate `#102634`, mint-lime `#D7FB6A`, cloud white `#F5F7F8`, muted steel `#9CB1BD`; warm amber reserved for deadline warnings. Dark and light modes; sufficient contrast and user preference. **Fonts:** licensed/open fonts such as Manrope/DM Sans, robust French accents and multilingual glyph support. **Images:** official imagery with explicit reuse rights or licensed photos; always record license and attribution; no scraped third-party photographs without permission.

## 7.2 Responsive information architecture

**Mobile:** persistent minimal header, single viewport-height swipe card, scroll-snap with touch momentum, optional bottom nav (Feed, Explore, Deadlines, Saved, Profile), swipe vertically between stories; never hijack horizontal browser back gestures. Safe areas, notches and virtual keyboard accounted for.

**Tablet:** centered reader, collapsible filters and related sources.

**Desktop:** centered card column; left rail for filters/topics; right rail for next/previous and context; keyboard arrows, PageUp/PageDown, accessible controls. Header/footer remain consistent on feed and full articles.

**Feed interaction:** Continuous virtualized cards, prefetch next 2–3, load more in pages, deduplicate IDs, stable ordering during reading, avoid auto-inserting new cards above the reader, no forced page reload, no “1/10” artificial ceiling, no broken stop after fourth card. Visible progress is optional and understated. Return to original card on navigation/back/refresh. Clear empty, loading, error and offline states.

**Swipe gestures:** Touch swipe up/down; trackpad/wheel; keyboard; on-screen next/previous. Accessible alternative list view. Respect `prefers-reduced-motion`. Scroll must remain inside feed without making header disappear. Do not rely on fragile `scrollIntoView` that scrolls the entire document.

**Search/explore:** Keyword, topic, location, issuing body, date range, status, opportunity type, deadline, jurisdiction and language. Search must match both translations and authoritative names. Saved searches and optional notifications.

**Personalization:** Optional home jurisdiction, nearby localities, interests, languages, saved items, reminders. Default feed remains usable without account or location permission. Never make sensitive demographic inferences. Allow a national view and explicit city/region switching.

**Ad policy:** No private paid content or private-sector sponsored cards under the specified scope. If future public-service sponsorship is considered, require a separately approved policy, conspicuous labeling and complete editorial independence. Never interleave fake news-looking ads in official notice cards.

---

# 8. Architecture — production web app

```text
Official public websites / RSS / APIs / sitemaps / PDF / calendars / gazettes
     ↓
Source Registry → Scheduler → Per-source Adapters → Fetch Queue → Raw Document Store
     ↓                                     ↓
Rights & robots checks                      Monitoring / retry / alerts
     ↓
Text extraction → Language detection → Entity & date parsing → Geo resolution
     ↓
Canonicalization → Duplicate / update detection → Evidence-linked draft
     ↓
EN + FR translation → Editorial QA → Human review / risk gates → Publish
     ↓
PostgreSQL (canonical records) + Object Storage (evidence) + Search Index
     ↓
Public API / CDN → Web app / PWA → Swipe feed / Search / Saved / Alerts
     ↓
Analytics / Correction queue / Source freshness and coverage dashboards
```

**Recommended production stack:** Next.js (App Router) + TypeScript + React; PostgreSQL (with PostGIS for geographic relevance), Prisma or Drizzle ORM, Redis for caching/queues, BullMQ or managed task queue, OpenSearch or Meilisearch for bilingual search, S3-compatible storage for immutable source snapshots, CDN, transactional email/push notification service, OAuth/OIDC for admin users, error tracking, OpenTelemetry, infrastructure as code and GitHub Actions CI/CD. Host in a jurisdiction appropriate to applicable privacy and data-residency requirements; do not claim Canadian data residency until verified. Prefer standards-based modules over single-vendor lock-in.

**Services:**
1. **Source registry service**: source identity, domain verification, hierarchy, terms/robots, language, crawl cadence, contact, adapter, health and coverage.
2. **Ingestion service**: conditional GET, ETag/Last-Modified, rate limits, retry/backoff, PDFs and structured APIs, anti-bot compliance; do not bypass authentication or access controls.
3. **Extraction service**: HTML/PDF text, metadata, original links, attachments, tables, deadline/date parsing with source evidence.
4. **Event resolution service**: entity matching, duplicate clustering, canonical event, revisions and official amendments.
5. **Translation/editorial service**: EN/FR drafting with structured facts locked, side-by-side comparison and approval.
6. **Publication service**: versioned API, immutable audit, feeds, sitemap, RSS, structured data, social previews.
7. **Search and personalization service**: geo filters, source types, alerts, saved searches, privacy-aware recommendations.
8. **Observability and analytics service**: ingestion failures, source freshness, correction metrics, anonymous usage.

**High-risk items:** emergencies, safety warnings, legal proceedings, allegations, public-health alerts, individual personal information, financial eligibility, immigration deadlines and contested political claims require enhanced editorial review and exact-source linking. Never automatically publish a speculative summary.

---

# 9. Core database model

**organizations** `(id, canonical_name, name_fr, level, jurisdiction_code, organization_type, parent_id, official_domains, active, verified_at)`

**sources** `(id, organization_id, source_type, canonical_url, feed_url, language, adapter, crawl_interval, last_checked, last_success, robots_policy, license_policy, priority, health_status, notes)`

**source_documents** `(id, source_id, original_url, canonical_url, fetched_at, published_at, modified_at, mime_type, etag, sha256, raw_storage_key, extracted_text_key, extraction_status, rights_metadata)`

**events** `(id, type, canonical_key, organization_id, jurisdiction_code, geo_coverage, status, event_date, opens_at, closes_at, deadline_tz, last_source_update, superseded_by, risk_level)`

**event_evidence** `(event_id, source_document_id, supporting_span, evidence_type, confidence, verified_by)`

**swipes** `(id, event_id, slug, status, published_at, updated_at, priority, editorial_version, source_verified_at, corrected_at)`

**swipe_localizations** `(swipe_id, locale, headline, deck, summary, body, eligibility, action_text, seo_title, meta_description, translation_status, reviewer_id, reviewed_at)`

**opportunities** `(event_id, opportunity_type, notice_id, salary_min, salary_max, currency, application_url, qualification_json, documents_json, award_amount, procurement_id, exam_stage)`

**users** `(id, email_nullable, preferred_locale, preferred_jurisdictions, consent_version, created_at)`; **saved_swipes**, **saved_searches**, **notifications**, **delivery_receipts**, **consents**, **audit_log**, **corrections**, **analytics_events**.

**Indices:** organization + date; jurisdiction + topic + published date; closing date + status; source URL unique; canonical event key unique; full-text per language; geo index; publication cursor. No fabricated timestamps or hardcoded jurisdiction names in IDs.

---

# 10. APIs and application contracts

- `GET /api/v1/feed?locale=en-CA&jurisdiction=CA-BC&topic=jobs&cursor=...&limit=20` → stable paginated card summaries, source, status, version.
- `GET /api/v1/swipes/{id}?locale=fr-CA` → full story, structured details, source evidence, revisions.
- `GET /api/v1/search?q=...&locale=...&filters=...` → bilingual search with facets.
- `GET /api/v1/sources` → public verified source directory and last checked dates.
- `GET /api/v1/jurisdictions` → configurable hierarchy and coverage.
- `GET /api/v1/deadlines?from=...&to=...&type=...` → verified actionable deadlines.
- `POST /api/v1/saved` → authenticated bookmarks; local-only option without account.
- `POST /api/v1/alerts` → opted-in topic/location/deadline alerts with unsubscribe.
- `POST /api/v1/corrections` → correction request, evidence, tracking ID; spam controls.
- `POST /api/v1/admin/sources`, `POST /api/v1/admin/ingest`, `POST /api/v1/admin/swipes/{id}/review`, `POST /api/v1/admin/swipes/{id}/publish` → authenticated, role-gated, audited.

**Security:** Admin authentication with MFA, RBAC (source editor, translator, fact checker, publisher, admin), CSRF protections, rate limiting, signed webhooks, server-side validation, secret manager, secure cookies, CSP, dependency scanning, backups, least privilege and retention limits. Ingestion fetchers need SSRF protection and strict allowlists.

---

# 11. Editorial SOP — from detection to correction

**Step 1 — Discover:** Fetch from a registered official source; record canonical URL, organization and time.

**Step 2 — Qualify:** Check whether the issuing body is in scope and whether the content is an official public-interest announcement rather than private promotion or political party campaigning.

**Step 3 — Verify:** Confirm primary source item, publication date, organization, jurisdiction, facts, deadlines, eligibility, amounts, contact and attachments. Never substitute a generic newsroom page for a specific notice when a specific notice exists.

**Step 4 — Deduplicate:** Match by source ID/URL, notice number, normalized headline, authority, date and semantic event cluster. If same event is amended, update the existing Swipe and mark what changed rather than create a competing copy.

**Step 5 — Structure:** Capture exact dates and time zones, official URLs, user actions and relevant geographic scope. Treat unknown as unknown.

**Step 6 — Write:** English plain-language headline and concise summary; French version written for the same meaning. Do not add facts not in source; attribute projections and claims.

**Step 7 — Check:** Automated validations for links, date consistency, locale parity, duplicate status, source evidence, PII, accessibility, spelling and legal-risk flags. Human approval for high-risk items and sampling/spot checks of routine items.

**Step 8 — Publish:** Atomic release of both languages, structured data, correct category and location, source URL, status and feed inclusion. Failed bilingual validation blocks publication rather than publishing an empty translation.

**Step 9 — Monitor:** Revisit active jobs/tenders/exams/grants more frequently near deadlines; detect extensions, cancellations, corrections and results. A published card is not “done forever.”

**Step 10 — Archive/correct:** Mark expired and cancelled, remove from active opportunity views but keep searchable historical context; corrections show timestamp, changed field and original source. Emergency alerts follow stricter expiry rules.

**Editorial gates:**
- **Auto-publish eligible:** Low-risk, high-confidence structured official notices with deterministic extraction, verified primary links, bilingual parity and no conflicting updates, **only after operational pilot validates quality**.
- **Human approval required:** High-risk/sensitive matters, conflicting notices, ambiguous deadlines, OCR-only PDFs, translation uncertainty, suspected source spoofing, allegations, personal details and politically contested claims.
- **Reject/hold:** No primary official evidence, stale unverified data, private promotion, unlicensed images, duplicate, invalid link, unknown authority or unsupported extrapolation.

**Corrections SLA proposal:** Critical public-safety error: immediate triage; material deadline/eligibility error: priority same-day; routine typo: next editorial cycle. These are proposed internal targets, not guarantees.

---

# 12. Automated source monitoring and discovery

**Source discovery engine:**
1. Seed official jurisdiction registries, department directories, open-data catalogues and institutional lists.
2. Crawl allowed official sitemaps, robots-declared feeds, navigation links, newsroom pages, procurement portals, public calendar feeds and search indexes.
3. Identify candidate sub-agencies and nested departments; verify official ownership and scope before activation.
4. Classify source by jurisdiction, body, subject, type, language, update cadence, legal rights and importance.
5. Check source health; alert when domain changes, pages break, RSS disappears or published content stops unexpectedly.
6. Review registry quarterly and after elections/administrative reorganizations. Preserve organization history and successor mappings.

**Suggested polling tiers:** Emergencies 5–15 min where permitted; high-impact notices and deadlines 30–60 min; recruitment/exams/tenders 1–3 hours; newsrooms 3–6 hours; reports, archives and general institutional pages daily. Respect publisher rate limits, site terms and infrastructure. Prefer push APIs/webhooks where offered. Coverage numbers are not guarantees until actual registry and monitors are operational.

**Discovery metrics:** Number of official organizations identified; sources active; sources verified; geographic coverage; categories covered; items ingested; dedup rate; source failure rate; time-to-detection; translation latency; correction rate; expired notices correctly marked; source-link integrity. Publish a coverage map with honest gaps.

---

# 13. Distribution, SEO and audience growth

**Search:** One stable canonical URL per Swipe with language alternates (`hreflang=en-CA`, `fr-CA`), canonical tags, descriptive slugs, structured `NewsArticle`/`Article`/`Event`/`JobPosting` only when schema conditions are met, accurate published/modified dates, XML sitemaps, RSS/Atom, robots rules and indexable full-story pages. Do not index thin duplicates or pages without substantive original context.

**Shareability:** Distinct OG cards, source attribution, jurisdiction and concise headline; “I Swiped this” share text, deep links to exact Swipe, share sheet, link previews, optional public collections. Never claim affiliation with issuing authority.

**Notifications:** Opt-in daily briefings, deadline reminders, local alerts, new tenders, exam/result updates, program changes. Notifications must be relevance-ranked, rate-limited and cancellable. Critical public-safety notifications must clearly state they are secondary to the official alert channel.

**Analytics:** Daily active readers, engaged sessions, completed Swipes, average dwell time, source-click rate, saves, shares, search success, return rate, EN/FR parity, deadline alert opt-in, search-to-action conversion, scroll performance, load time, error rate. Use privacy-preserving aggregate analytics, no sale of user data and consent where required. Distinguish impressions from actual reads; never inflate metrics.

**Growth channels:** Search indexing of full notices, shareable Swipes, public topic feeds, RSS, partnerships with public institutions for linking (without editorial control), newsletters, community calendars and relevant public-sector directories. Do not scrape private media and republish copyrighted text.

---

# 14. Accessibility, legal and trust

- WCAG 2.2 AA target; semantic headings, focus order, keyboard reader controls, visible focus, contrast, 200% zoom, screen-reader card announcements, alt text, skip links, captions/transcripts, accessible PDFs linked where available, reduced-motion mode.
- English and French at launch; test Canadian French terminology and locale-specific date/number formatting. Bilingual content must not be falsely described as official translation when prepared by SWIPES.
- Respect source copyright, Crown copyright, open government licenses, attribution, robots.txt, terms of use and trademark restrictions. Linking is generally preferable to wholesale copying; legal review required for reuse policies across jurisdictions.
- Privacy-by-design: collect minimum personal information; optional accounts; location off by default; meaningful consent; deletion/export; retention schedule; encrypted storage; applicable Canadian federal/provincial privacy law review.
- Editorial independence, nonpartisanship, transparent corrections and complaints, conflict-of-interest policy, no paid ranking and no hidden political targeting.
- Security: incident response, backups, disaster recovery, admin audit logs, vulnerability management, penetration tests and operational monitoring.
- **Explicit disclaimer:** “SWIPES is an independent information service and is not affiliated with or endorsed by any government. Always verify critical deadlines and requirements with the issuing authority.”

---

# 15. Editorial and engineering dashboards

**Editor dashboard:** Intake queue; new official sources; extracted evidence; duplicate clusters; bilingual side-by-side; deadlines; high-risk flags; draft/review/publish; source-link checks; corrections; expiry queue; translation status; publish history.

**Coverage dashboard:** National → provincial/territorial → regional → local drill-down; body directory; active source count; health; missing bodies; last verified; categories with zero activity; ingestion backlog; source updates not yet processed.

**Product dashboard:** DAU/WAU, Swipes read, depth, dwell, shares, saves, source clicks, deadline alerts, search failures, feed latency, mobile vs desktop, locale usage, top categories, page performance, broken links.

**Ops dashboard:** Failed adapters, 429/403 errors, stale source warnings, queue lag, OCR failures, translation inconsistencies, publishing failures, bad redirects, uptime, security alerts, backup results.

**Roles:** Product owner; editor-in-chief; source research/registry team; ingestion engineer; bilingual editors/translators; fact checker; accessibility lead; security/privacy lead; QA engineer; analytics/SEO lead. One person may hold multiple roles initially, but approval separation is required for sensitive stories.

---

# 16. Production acceptance tests (must pass before “launch-ready”)

**Reader:** 100+ cards loaded in a session without stopping; scroll/snap on iOS Safari, Android Chrome, desktop Chrome/Safari/Firefox; no header disappearance; back navigation restores exact card; no page reload for next Swipe; links open correct full article; desktop keyboard and mobile controls work; reduced motion respected.

**Languages:** EN and FR switch on every route without losing card or filter; no cross-language leakage; date/time formats correct; no missing translations; localized SEO and links work.

**Data:** 100% published cards have valid specific official source URL, issuing authority, timestamp and evidence; active opportunities have verified deadlines/status; corrections propagate; duplicates blocked; expiry rules work; stale notices clearly flagged.

**Security:** Auth and permissions tested; admin APIs inaccessible to public; SSRF prevention; backup restore rehearsal; dependency scan; rate limits; consent and deletion flows; no secrets in client bundle.

**Performance targets:** p75 LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 on supported mobile networks; 99.9% monthly availability target after production hardening; feed API p95 ≤500ms from CDN/edge where feasible. These are goals, not measured results.

**Editorial:** A sample from every source family and jurisdiction passes source/date/translation audit; no invented dates; alerts, corrections and cancellations tested; human-review path exercised.

**Operations:** Failed feed alerts reach owner; source health visible; rollback documented; GitHub CI green; staging matches production; publish/revert rehearsal complete; uptime and logging active.

---

# 17. Implementation roadmap

**Phase 0 — Discovery and governance:** Confirm ownership, domains, design identity, jurisdiction profile, legal review, seed registry, source eligibility, editorial charter and bilingual style guide. Deliver source registry with coverage gaps and legal constraints.

**Phase 1 — Premium reader MVP:** Design system, full-screen virtualized feed, EN/FR, search, topics, local selector, full articles, source links, saves, responsive layouts, accessibility, PWA, analytics and error states. Seed with **verified real public information** only in production.

**Phase 2 — Ingestion and editorial CMS:** Source registry, adapters, queue, snapshots, structured extraction, duplicate resolution, bilingual workflow, review/publish, source health, deadlines and corrections. Start with high-quality official feeds and scale by category/jurisdiction.

**Phase 3 — Canada-wide coverage:** Expand all 13 provinces/territories plus federal, municipalities, regional authorities, Indigenous governments (with protocols), public schools, higher education, health, sport, culture and agencies. Track each category's completeness; do not claim “all” until audited.

**Phase 4 — Advanced personalization:** Saved searches, deadline calendar, push/email notifications, optional accounts, geo feed, recommendation controls, collections and richer public-data views.

**Phase 5 — Internationalization and resilience:** Add new tenant country via config, source discovery, locale packs, legal policies, jurisdiction graph and editorial team; scale search, ingestion and operations without forking the codebase.

**Definition of done per feature:** Implemented + automated tests + cross-device manual verification + accessibility review + production deployment + monitoring + rollback. A saved WordPress/DB record alone is not sufficient.

---

# 18. Configuration-first country expansion

A new deployment command should supply only these parameters; the rest of the blueprint stays the same:

```yaml
platform:
  name: SWIPES
  editorial_scope: official_public_sector_only
  source_evidence_required: true
  publication_requires_all_locales: true
country:
  code: CA
  display_name: Canada
  default_locale: en-CA
  supported_locales: [en-CA, fr-CA]
  timezone_policy: source_timezone_then_user_timezone
  jurisdiction_levels: [federal, provincial, territorial, regional, municipal, indigenous, special_purpose]
  public_source_seed_registry: canada
  privacy_legal_profile: canada_review_required
  government_branding_disclaimer: true
reader:
  primary_unit: swipe
  layout: full_viewport_vertical_snap
  default_feed: latest_verified
  allow_guest_reading: true
  allow_local_bookmarks: true
  allow_optional_account: true
  preserve_position_on_return: true
content:
  types: all_public_notice_types
  include_private_sector_promotions: false
  official_primary_link_required: true
  auto_expire_opportunities: true
  correction_history: true
```

**New-country setup instruction:** “Deploy SWIPES for [COUNTRY/REGION], in [LANGUAGES]. Discover and verify all official national, subnational, regional, municipal and special-purpose public-sector sources; configure laws, language and jurisdiction hierarchies; preserve the universal design, source-first editorial policy, swipe behavior, API contracts and SOPs. Do not import another deployment's content or pretend a source registry is complete before verification.”

---

# 19. What is included in this download, and what is not

**Included:** Full master blueprint, Canada source seed registry, detailed scope, taxonomy, editorial SOP, architecture, database/API design, UI specification, security/privacy and QA plan, deployment-neutral config, and a **runnable React/Vite bilingual interactive reader prototype** with GitHub Actions build workflow.

**Not yet included / not represented as complete:** Production Next.js backend, database, live government crawling, verified source-by-source inventory, translation service, admin CMS, production auth, push notifications, analytics infrastructure, full offline sync, store-ready native apps, hosting deployment, production data, legal approval and end-to-end device tests. Prototype cards are clearly marked fictional. The demo is **not** a functioning nationwide news ingestion operation. The GitHub repo has not been created or pushed by this download.

**Recommended next delivery contract:** Convert this repository to the production stack; implement database and APIs; activate a vetted seed of official sources; pass bilingual QA; then deploy to staging and validate the acceptance suite before declaring launch readiness.
