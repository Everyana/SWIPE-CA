#!/usr/bin/env python3
"""Fetch approved primary-source RSS/Atom headlines for SWIPES.
No AI-generated facts or translations; preserves official title/excerpt and links.
"""
import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse

REGISTRY = Path(__file__).with_name("sources.json")

def load_sources(path=REGISTRY):
    """Active sources from the registry, in the shape the fetcher uses."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for e in data["sources"]:
        if e.get("status") != "active":
            continue
        src = {"name": e["name"], "jurisdiction": e["jurisdiction"], "lang": e["lang"], "url": e["url"], "hosts": e["hosts"]}
        if e["access"].startswith(("page:", "json:")):
            src["format"] = e["access"].split(":", 1)[1]
        out.append(src)
    return out

SOURCES = load_sources()
NS = {"a":"http://www.w3.org/2005/Atom"}
def plain(value):
    value = re.sub(r"<[^>]*>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()
ADVISORY = re.compile(r"^(?:media advisory|avis (?:aux )?m[ée]dias|/?r ?e ?p ?r ?i ?s ?e|invitation (?:[àa] la presse|aux m[ée]dias)|agenda public)"
                      r"|\bto hold a (?:press conference|photo opportunity|media availability)\b|\bavailable to media\b"
                      r"|\bactivities advisory\b|^(?:update\s*[-–]\s*)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday), \w+ \d{1,2}, \d{4}$", re.I)

TEST_ITEM = re.compile(r"^test[\s_-]", re.I)

def is_advisory(title, url=""):
    """Media advisories, itineraries and press invitations tell journalists where to be; they are not public information cards."""
    return bool(ADVISORY.search(title.strip())) or "/media-advisories/" in url or bool(TEST_ITEM.match(title.strip()))

TOPIC_PATTERNS = {
    "Public consultations": r"public consultation|consultation publique|public hearing",
    "Tenders": r"request for proposals|call for tenders|appel d.offres|procurement",
    "Immigration": r"immigration|newcomers|nouveaux arrivants|refugees|réfugiés",
    "Jobs and training": r"job fair|apprenticeship|skills training|formation professionnelle|salon de l.emploi",
    "Health": r"health|hospital|long.term care|screening|therapy|vaccin|santé|hôpital|dépistage|cystic fibrosis",
    "Education": r"school|universit|scholarship|student|école|étudiant|research chair|graduation",
    "Transport": r"highway|traffic.pattern|traffic advisor|winter driving|road closure|bridge|public transit|autoroute|ponts?|circulation",
    "Housing": r"housing|logement",
    "Environment": r"environment|conservation|tropical forests|climate|environnement|climat",
    "Public safety": r"polic(e|ing)|public safety|emergency preparedness|sécurité publique",
    "Sport and recreation": r"sport|soccer|championship|loisirs",
    "Grants and funding": r"grant program|funding application|subventions|grants? to|invest(?:s|ing)? \$|provides up to \$|aide financi[eè]re|financement",
    "Laws and regulations": r"act\b|legislation|amendments?|regulations?|bill \d+|projet de loi|loi\b|r[eè]glement",
    "Budget and finance": r"budget|fiscal|financial report|surplus|deficit|tax|deduction|imp[oô]t|finances publiques",
    "Economy and business": r"economy|economic|business|investment|trade|mines?\b|minerals|industry|PME|[ée]conomi|entreprises?",
    "Culture and awards": r"award|prix du|artist|museum|mus[ée]e|festival|culture|heritage|patrimoine|music",
    "Indigenous": r"indigenous|first nations?|m[ée]tis|inuit|autochtones?|premi[eè]res nations|innus?",
    "Reports and data": r"report\b|rapport|survey results|statistics|indicators",
}

def topic(title):
    for category, pattern in TOPIC_PATTERNS.items():
        if re.search(r"\b(?:" + pattern + r")", title, re.I):
            return category
    return "Public updates"

def clean_excerpt(summary, title):
    text = plain(summary)
    # The PM's Drupal feed appends an author and a raw timestamp to excerpts.
    text = re.split(r"\s+pm@pm\.gc\.ca\b", text, maxsplit=1, flags=re.I)[0]
    return text[:650].strip() or title

def host_ok(url, domains):
    try:
        parsed=urlparse(url)
        host=(parsed.hostname or "").lower()
        return parsed.scheme=="https" and any(host==d or host.endswith("."+d) for d in domains)
    except ValueError:
        return False
def date_iso(raw):
    try:
        return email.utils.parsedate_to_datetime(raw).astimezone(dt.timezone.utc).isoformat()
    except Exception:
        try:
            return dt.datetime.fromisoformat(raw.replace("Z","+00:00")).astimezone(dt.timezone.utc).isoformat()
        except Exception:
            return None
def children(node, name):
    # Atom names use the "a:" prefix, so the namespace map is required or the text is silently lost.
    return node.findtext(name, namespaces=NS) or ""
def xml_entries(xml):
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        if "undefined entity" not in str(exc):
            raise
        # Some RSS publishers use HTML entities without declaring them in XML.
        xml = re.sub(
            rb"&([A-Za-z][A-Za-z0-9]+);",
            lambda match: (
                "".join(f"&#{ord(char)};" for char in html.entities.html5[match[1].decode() + ";"]).encode()
                if match[1] not in {b"amp", b"lt", b"gt", b"quot", b"apos"}
                and match[1].decode() + ";" in html.entities.html5
                else match[0]
            ),
            xml,
        )
        root = ET.fromstring(xml)
    items=[]
    if root.tag.endswith("feed"):
        for entry in root.findall("a:entry",NS):
            link=""
            for el in entry.findall("a:link",NS):
                if el.attrib.get("rel","alternate")=="alternate" and el.attrib.get("href"):
                    link=el.attrib["href"]; break
            items.append((children(entry,"a:title"),children(entry,"a:summary") or children(entry,"a:content"),link,children(entry,"a:published") or children(entry,"a:updated")))
    else:
        for entry in root.findall(".//item"):
            items.append((children(entry,"title"),children(entry,"description"),children(entry,"link"),children(entry,"pubDate") or children(entry,"{http://purl.org/dc/elements/1.1/}date")))
    return items

def newsroom_entries(page, source):
    page = page.decode("utf-8")
    if source["format"] == "gnwt":
        pattern = (r'<span\s+class="teaser-date[^"]*">([^<]+)</span>'
                   r'<h2 class="teaser-title[^"]*"><a\s+href="(/newsroom/[^"]+)">(.*?)</a></h2>')
        entries = re.findall(pattern, page, re.S)
        return [(title, "", urljoin(source["url"], path),
                 dt.datetime.strptime(date, "%B %d, %Y").replace(tzinfo=dt.timezone.utc).isoformat())
                for date, path, title in entries]
    pattern = (r'>News release</div></div><div class="views-field views-field-title">'
               r'<span class="field-content"><a href="(/en/(\d{4}/\d{2}/\d{2})/[^"]+)"[^>]*>(.*?)</a>')
    return [(title, "", urljoin(source["url"], path), date.replace("/", "-") + "T00:00:00+00:00")
            for path, date, title in re.findall(pattern, page, re.S)]

MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                      "september", "october", "november", "december"], 1)}
MONTHS.update({m[:3]: i for m, i in list(MONTHS.items())})
MONTHS.update({"sept": 9})
MOIS = {m: i for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                                    "septembre", "octobre", "novembre", "décembre"], 1)}
EN_CUE = r"(?:deadline(?:\s+(?:is|of|to\s+apply\s+is))?|(?:submit(?:ted)?|apply|register|send)(?:\s+[a-z]+){0,3}\s+by|closes?\s+(?:on\s+)?|closing\s+date(?:\s+is)?|due\s+(?:by|on)|no\s+later\s+than|until|before)"
EN_DATE = r"(?:(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+)?([a-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s+(\d{4}))?"
ACTION = r"(?:appl(?:y|ication)|submi|regist|feedback|comment|nominat|bids?\b|proposal|enrol|survey|demande|inscri|commentaire|soumett|candidat|proposition|sondage|consultation)"
FR_CUE = r"(?:date\s+limite(?:\s+(?:est|:))?|jusqu.au|au\s+plus\s+tard\s+le|avant\s+le|d.ici\s+le)"
FR_DATE = r"(?:le\s+)?(\d{1,2})(?:er)?\s+([a-zéû]+)(?:\s+(\d{4}))?"

def extract_deadline(text, published_iso):
    """Return an ISO date for an explicit deadline in the notice text, or None.
    Only dates introduced by a deadline cue count; the year defaults to the publication year,
    rolled forward if the date would fall before publication."""
    if not text:
        return None
    pub = dt.datetime.fromisoformat(published_iso).date()
    low = text.lower()
    candidates = []
    def action_before(start):
        # "until"/"before"/"jusqu'au" also mark event end dates; only count them after an action word.
        return re.search(ACTION, low[max(0, start - 90):start]) is not None
    for m in re.finditer(EN_CUE + r"[:\s]+" + EN_DATE, low):
        month = MONTHS.get(m.group(1).rstrip("."))
        if re.match(r"(?:until|before)\b", m.group(0)) and not action_before(m.start()):
            continue
        if month:
            candidates.append((month, int(m.group(2)), m.group(3)))
    for m in re.finditer(FR_CUE + r"[:\s]+" + FR_DATE, low):
        month = MOIS.get(m.group(2))
        if re.match(r"(?:jusqu|avant|d.ici)", m.group(0)) and not action_before(m.start()):
            continue
        if month:
            candidates.append((month, int(m.group(1)), m.group(3)))
    for month, day, year in candidates:
        try:
            d = dt.date(int(year) if year else pub.year, month, day)
        except ValueError:
            continue
        if not year and d < pub:
            try:
                d = d.replace(year=pub.year + 1)
            except ValueError:
                continue
        if pub <= d <= pub + dt.timedelta(days=400):
            return d.isoformat()
    return None

def gnb_entries(data, lang):
    """New Brunswick newswire JSON (the data behind www.gnb.ca/en/news/newswire.html)."""
    rows = json.loads(data.decode("utf-8"))["data"]["newsModelList"]["items"]
    out = []
    for r in rows:
        path = (r.get("detailUrl") or "").replace("/content/GNB3", "", 1)
        if not path.startswith("/"):
            continue
        out.append((r.get(f"title_{lang}") or r.get("displayTitle") or "", r.get(f"leadLine_{lang}") or r.get("displayLead") or "",
                    "https://www.gnb.ca" + path, r.get("datePublished") or ""))
    return out

def parse(data, source):
    if source.get("format") == "gnb":
        items = gnb_entries(data, source["lang"])
    else:
        items = newsroom_entries(data, source) if source.get("format") else xml_entries(data)
    out=[]
    for title,summary,link,date in items:
        title=plain(title)[:240]
        summary=clean_excerpt(summary,title)
        date=date_iso(date)
        if not title or not date or not host_ok(link,source["hosts"]): continue
        if is_advisory(title, link): continue
        out.append({"id":hashlib.sha256(link.encode()).hexdigest()[:20],"title":title,"summary":summary or title,"url":link,"publishedAt":date,"source":source["name"],"jurisdiction":source["jurisdiction"],"language":source["lang"],"category":topic(title)})
        deadline = extract_deadline(title + ". " + summary, date)
        if deadline:
            out[-1]["deadline"] = deadline
    return out
def select_notices(items, curated):
    ranked = sorted(items, key=lambda item: item["publishedAt"], reverse=True)
    latest_by_jurisdiction = {}
    for item in ranked:
        latest_by_jurisdiction.setdefault(item["jurisdiction"], item)
    selected = {item["id"]: item for item in curated}
    covered = {item["jurisdiction"] for item in curated}
    for jurisdiction, item in latest_by_jurisdiction.items():
        if len(selected) >= 40:
            break
        if jurisdiction not in covered:
            selected[item["id"]] = item
    for item in ranked:
        if len(selected) >= 40:
            break
        selected.setdefault(item["id"], item)
    return sorted(selected.values(), key=lambda item: item["publishedAt"], reverse=True)

HEALTH_PATH = Path("public/data/source-health.json")
ALERT_AFTER = 3  # consecutive failed runs before a source is flagged for attention

def build_health(results, previous, registry, now_iso):
    """results: {source name: {"ok": bool, "items": int, "error": str}}.
    Carries lastSuccess and consecutiveFailures forward from the previous health file."""
    prev = {s["name"]: s for s in (previous or {}).get("sources", [])}
    out = []
    for entry in registry:
        name = entry["name"]
        before = prev.get(name, {})
        if entry.get("status") != "active":
            out.append({"id": entry["id"], "name": name, "jurisdiction": entry["jurisdiction"], "status": entry["status"],
                        "note": entry.get("note", ""), "items": 0, "lastSuccess": before.get("lastSuccess"),
                        "consecutiveFailures": 0, "needsAttention": False})
            continue
        r = results.get(name, {"ok": False, "items": 0, "error": "not run"})
        fails = 0 if r["ok"] else int(before.get("consecutiveFailures", 0)) + 1
        out.append({"id": entry["id"], "name": name, "jurisdiction": entry["jurisdiction"],
                    "status": "ok" if r["ok"] else "error", "items": r["items"], "error": r.get("error", ""),
                    "lastSuccess": now_iso if r["ok"] else before.get("lastSuccess"),
                    "consecutiveFailures": fails, "needsAttention": fails >= ALERT_AFTER})
    return {"checkedAt": now_iso, "alertAfter": ALERT_AFTER, "sources": out}

def main():
    all_items=[]; errors=[]; successful=0
    failed_sources = {}
    results = {}
    for source in SOURCES:
        try:
            req=urllib.request.Request(source["url"],headers={"User-Agent":"SWIPESCanada/0.1 (+https://ca.everyana.com; official feed aggregator)","Accept":"application/atom+xml,application/rss+xml,application/xml,text/xml,text/html"})
            with urllib.request.urlopen(req,timeout=22) as response:
                xml=response.read(3_000_000)
            parsed=parse(xml,source)
            if not parsed: raise ValueError("No valid official items returned")
            successful+=1; all_items.extend(parsed)
            results[source["name"]] = {"ok": True, "items": len(parsed)}
            print(source["name"],len(parsed))
        except Exception as e:
            failed_sources[source["name"]] = source
            errors.append(source["name"]+": "+str(e)[:160])
            results[source["name"]] = {"ok": False, "items": 0, "error": str(e)[:160]}
            print("WARNING",errors[-1])
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))["sources"]
    previous_health = json.loads(HEALTH_PATH.read_text(encoding="utf-8")) if HEALTH_PATH.exists() else None
    health = build_health(results, previous_health, registry, dt.datetime.now(dt.timezone.utc).isoformat())
    HEALTH_PATH.parent.mkdir(parents=True, exist_ok=True)
    HEALTH_PATH.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not successful: raise SystemExit("No official feeds succeeded; refusing to overwrite published data")
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=14)
    path = Path("public/data/notices.json")
    if path.exists():
        previous = json.loads(path.read_text(encoding="utf-8"))
        for item in previous.get("notices", []):
            source = failed_sources.get(item["source"])
            if (source and host_ok(item["url"], source["hosts"])
                    and dt.datetime.fromisoformat(item["publishedAt"]) >= cutoff):
                all_items.append(item)
    curated_path = Path("scripts/curated_notices.json")
    curated = [item for item in json.loads(curated_path.read_text(encoding="utf-8"))
               if dt.datetime.fromisoformat(item["publishedAt"]) >= cutoff
               and (not item.get("expiresAt") or dt.datetime.fromisoformat(item["expiresAt"]) > now)]
    dedup = {}
    for item in curated + all_items:
        key = item["url"].rstrip("/")
        if urlparse(key).hostname == "www.alberta.ca":
            key = key.replace("/announcements.cfm?", "/release.cfm?")
        dedup.setdefault(key, item)
    records = select_notices(dedup.values(), curated)
    path.parent.mkdir(parents=True,exist_ok=True)
    payload={"updatedAt":dt.datetime.now(dt.timezone.utc).isoformat(),"sourcesSucceeded":successful,"sourcesConfigured":len(SOURCES),"sourceFailures":errors,"coverage":sorted({x["jurisdiction"] for x in records}),"coverageTarget":14,"notices":records}
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Keep every notice ever published so its story page stays online after it leaves the feed.
    archive_path = Path("public/data/archive.json")
    archive = json.loads(archive_path.read_text(encoding="utf-8")) if archive_path.exists() else {"notices": []}
    kept = {item["id"]: item for item in archive.get("notices", [])}
    for item in records:
        kept[item["id"]] = {**kept.get(item["id"], {}), **item}
    curated_ids = {item["id"] for item in json.loads(curated_path.read_text(encoding="utf-8"))}
    for item in kept.values():
        # Re-tag with the current topic rules; hand-curated notices keep the category an editor gave them.
        if item["id"] not in curated_ids:
            item["category"] = topic(item["title"])
    archive_path.write_text(json.dumps({"updatedAt": payload["updatedAt"], "notices": sorted(kept.values(), key=lambda x: x["publishedAt"], reverse=True)}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Wrote",len(records),"verified-link feed items;",len(errors),"source failures")
if __name__=="__main__": main()
