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
from urllib.parse import urlparse

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
]
NS = {"a":"http://www.w3.org/2005/Atom"}
def plain(value):
    value = re.sub(r"<[^>]*>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()
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
def parse(xml, source):
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
    out=[]
    for title,summary,link,date in items:
        title=plain(title)[:240]
        summary=plain(summary)[:650]
        date=date_iso(date)
        if not title or not date or not host_ok(link,source["hosts"]): continue
        out.append({"id":hashlib.sha256(link.encode()).hexdigest()[:20],"title":title,"summary":summary or title,"url":link,"publishedAt":date,"source":source["name"],"jurisdiction":source["jurisdiction"],"language":source["lang"],"category":"Public updates"})
    return out
def main():
    all_items=[]; errors=[]; successful=0
    for source in SOURCES:
        try:
            req=urllib.request.Request(source["url"],headers={"User-Agent":"SWIPESCanada/0.1 (+https://ca.everyana.com; official feed aggregator)","Accept":"application/atom+xml,application/rss+xml,application/xml,text/xml"})
            with urllib.request.urlopen(req,timeout=22) as response:
                xml=response.read(3_000_000)
            parsed=parse(xml,source)
            if not parsed: raise ValueError("No valid official items returned")
            successful+=1; all_items.extend(parsed)
            print(source["name"],len(parsed))
        except Exception as e:
            errors.append(source["name"]+": "+str(e)[:160])
            print("WARNING",errors[-1])
    if not successful: raise SystemExit("No official feeds succeeded; refusing to overwrite published data")
    dedup={}
    for item in all_items:
        key=item["url"].rstrip("/")
        if key not in dedup: dedup[key]=item
    ranked=sorted(dedup.values(),key=lambda x:x["publishedAt"],reverse=True)
    preferred=["British Columbia","Alberta","Saskatchewan","Manitoba","Ontario","Quebec","New Brunswick","Nova Scotia","Prince Edward Island","Newfoundland and Labrador","Yukon","Northwest Territories","Nunavut"]
    records=[]; selected=set()
    for jurisdiction in preferred:
        item=next((x for x in ranked if x["jurisdiction"]==jurisdiction),None)
        if item:
            records.append(item); selected.add(item["id"])
    for item in ranked:
        if len(records)>=20: break
        if item["id"] not in selected:
            records.append(item); selected.add(item["id"])
    records=sorted(records,key=lambda x:x["publishedAt"],reverse=True)
    path=Path("public/data/notices.json");path.parent.mkdir(parents=True,exist_ok=True)
    payload={"updatedAt":dt.datetime.now(dt.timezone.utc).isoformat(),"sourcesSucceeded":successful,"sourcesConfigured":len(SOURCES),"coverage":sorted({x["jurisdiction"] for x in records}),"coverageTarget":13,"notices":records}
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Wrote",len(records),"verified-link feed items;",len(errors),"source failures")
if __name__=="__main__": main()
