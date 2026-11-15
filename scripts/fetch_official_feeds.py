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

SOURCES = [
    {"name":"Government of Canada", "jurisdiction":"Federal", "lang":"en", "url":"https://api.io.canada.ca/io-server/gc/news/en/v2?sort=publishedDate&orderBy=desc&pick=100&format=atom", "hosts":["canada.ca","gc.ca"]},
    {"name":"Gouvernement du Canada", "jurisdiction":"Federal", "lang":"fr", "url":"https://api.io.canada.ca/io-server/gc/news/fr/v2?sort=publishedDate&orderBy=desc&pick=100&format=atom", "hosts":["canada.ca","gc.ca"]},
    {"name":"BC Gov News", "jurisdiction":"British Columbia", "lang":"en", "url":"https://news.gov.bc.ca/feed", "hosts":["gov.bc.ca"]},
    {"name":"Prime Minister of Canada", "jurisdiction":"Federal", "lang":"en", "url":"https://www.pm.gc.ca/en/rss.xml", "hosts":["pm.gc.ca"]},
    {"name":"Statistics Canada", "jurisdiction":"Federal", "lang":"en", "url":"https://www150.statcan.gc.ca/n1/dai-quo/rss-eng.htm", "hosts":["statcan.gc.ca"]},
    {"name":"Government of Alberta", "jurisdiction":"Alberta", "lang":"en", "url":"https://www.alberta.ca/NewsRoom/newsroom.cfm", "hosts":["alberta.ca"]},
    {"name":"Government of Saskatchewan", "jurisdiction":"Saskatchewan", "lang":"en", "url":"https://www.saskatchewan.ca/Feeds/NewsFeed.ashx", "hosts":["saskatchewan.ca"]},
    {"name":"Government of Ontario", "jurisdiction":"Ontario", "lang":"en", "url":"https://news.ontario.ca/newsroom/en/rss/allnews.rss", "hosts":["ontario.ca"]},
    {"name":"Gouvernement du Québec", "jurisdiction":"Quebec", "lang":"fr", "url":"https://www.quebec.ca/fil-de-presse.rss", "hosts":["quebec.ca"]},
    {"name":"Government of Prince Edward Island", "jurisdiction":"Prince Edward Island", "lang":"en", "url":"https://www.princeedwardisland.ca/en/news/top-news.xml", "hosts":["princeedwardisland.ca"]},
    {"name":"Government of Newfoundland and Labrador", "jurisdiction":"Newfoundland and Labrador", "lang":"en", "url":"https://www.gov.nl.ca/releases/feed/", "hosts":["gov.nl.ca"]},
    {"name":"Manitoba Government", "jurisdiction":"Manitoba", "lang":"en", "url":"https://news.gov.mb.ca/news/index.rss", "hosts":["gov.mb.ca"]},
    {"name":"Government of Yukon", "jurisdiction":"Yukon", "lang":"en", "url":"https://yukon.ca/news-feed", "hosts":["yukon.ca"]},
    {"name":"Government of Nunavut", "jurisdiction":"Nunavut", "lang":"en", "url":"https://www.gov.nu.ca/en/news_rss", "hosts":["gov.nu.ca"]},
    {"name":"Government of the Northwest Territories", "jurisdiction":"Northwest Territories", "lang":"en", "url":"https://gnwt.ca/newsroom", "hosts":["gnwt.ca"], "format":"gnwt"},
    {"name":"Government of Nova Scotia", "jurisdiction":"Nova Scotia", "lang":"en", "url":"https://news.novascotia.ca/", "hosts":["novascotia.ca"], "format":"nova_scotia"},
]
NS = {"a":"http://www.w3.org/2005/Atom"}
def plain(value):
    value = re.sub(r"<[^>]*>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()
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
    "Grants and funding": r"grant program|funding application|subventions",
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
    return node.findtext(name) or ""
def xml_entries(xml):
    root=ET.fromstring(xml)
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

def parse(data, source):
    items = newsroom_entries(data, source) if source.get("format") else xml_entries(data)
    out=[]
    for title,summary,link,date in items:
        title=plain(title)[:240]
        summary=clean_excerpt(summary,title)
        date=date_iso(date)
        if not title or not date or not host_ok(link,source["hosts"]): continue
        out.append({"id":hashlib.sha256(link.encode()).hexdigest()[:20],"title":title,"summary":summary or title,"url":link,"publishedAt":date,"source":source["name"],"jurisdiction":source["jurisdiction"],"language":source["lang"],"category":topic(title)})
    return out
def select_notices(items):
    ranked = sorted(items, key=lambda item: item["publishedAt"], reverse=True)
    latest_by_jurisdiction = {}
    for item in ranked:
        latest_by_jurisdiction.setdefault(item["jurisdiction"], item)
    selected = {item["id"]: item for item in latest_by_jurisdiction.values()}
    for item in ranked:
        if len(selected) >= 40:
            break
        selected.setdefault(item["id"], item)
    return sorted(selected.values(), key=lambda item: item["publishedAt"], reverse=True)

def main():
    all_items=[]; errors=[]; successful=0
    failed_sources = {}
    for source in SOURCES:
        try:
            req=urllib.request.Request(source["url"],headers={"User-Agent":"SWIPESCanada/0.1 (+https://ca.everyana.com; official feed aggregator)","Accept":"application/atom+xml,application/rss+xml,application/xml,text/xml,text/html"})
            with urllib.request.urlopen(req,timeout=22) as response:
                xml=response.read(3_000_000)
            parsed=parse(xml,source)
            if not parsed: raise ValueError("No valid official items returned")
            successful+=1; all_items.extend(parsed)
            print(source["name"],len(parsed))
        except Exception as e:
            failed_sources[source["name"]] = source
            errors.append(source["name"]+": "+str(e)[:160])
            print("WARNING",errors[-1])
    if not successful: raise SystemExit("No official feeds succeeded; refusing to overwrite published data")
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)
    path = Path("public/data/notices.json")
    if path.exists():
        previous = json.loads(path.read_text(encoding="utf-8"))
        for item in previous.get("notices", []):
            source = failed_sources.get(item["source"])
            if (source and host_ok(item["url"], source["hosts"])
                    and dt.datetime.fromisoformat(item["publishedAt"]) >= cutoff):
                all_items.append(item)
    curated_path = Path("scripts/curated_notices.json")
    all_items.extend(item for item in json.loads(curated_path.read_text(encoding="utf-8"))
                     if dt.datetime.fromisoformat(item["publishedAt"]) >= cutoff)
    dedup={}
    for item in all_items:
        key=item["url"].rstrip("/")
        if key not in dedup: dedup[key]=item
    records = select_notices(dedup.values())
    path.parent.mkdir(parents=True,exist_ok=True)
    payload={"updatedAt":dt.datetime.now(dt.timezone.utc).isoformat(),"sourcesSucceeded":successful,"sourcesConfigured":len(SOURCES),"coverage":sorted({x["jurisdiction"] for x in records}),"coverageTarget":14,"notices":records}
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Wrote",len(records),"verified-link feed items;",len(errors),"source failures")
if __name__=="__main__": main()
