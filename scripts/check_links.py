#!/usr/bin/env python3
"""Check that every card in the live feed still points to a reachable official page.
Writes link-report.json and, with --issue, opens/updates one GitHub issue listing broken links."""
import json, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

UA = "SWIPESCanada/0.1 (+https://ca.everyana.com; link check)"
BLOCKED_BY_BOT_WALL = {401, 403, 429}  # the page may be fine for people; report separately

def check(url, opener=urllib.request.urlopen):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with opener(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

def classify(status):
    if 200 <= status < 400:
        return "ok"
    if status in BLOCKED_BY_BOT_WALL:
        return "unverified"
    return "broken"

def run(notices, opener=urllib.request.urlopen):
    rows = []
    for n in notices:
        s = check(n["url"], opener)
        rows.append({"id": n["id"], "title": n["title"], "url": n["url"], "status": s, "result": classify(s)})
    return rows

def main():
    notices = json.loads(Path("public/data/notices.json").read_text(encoding="utf-8"))["notices"]
    rows = run(notices)
    broken = [r for r in rows if r["result"] == "broken"]
    Path("link-report.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"{len(rows)} links: {len(broken)} broken, {sum(r['result'] == 'unverified' for r in rows)} unverified")
    if "--issue" in sys.argv and broken:
        body = "Cards whose official link no longer works:\n\n" + "\n".join(f"- [{r['status']}] {r['title']} — {r['url']}" for r in broken)
        subprocess.run(["gh", "label", "create", "link-check", "--color", "fbca04", "--force"], capture_output=True)
        subprocess.run(["gh", "issue", "create", "--title", f"Broken official links ({len(broken)})", "--body", body, "--label", "link-check"], check=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
