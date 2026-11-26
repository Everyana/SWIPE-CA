#!/usr/bin/env python3
"""Open or close GitHub issues for official sources that keep failing.
Reads public/data/source-health.json; uses the gh CLI (GITHUB_TOKEN in Actions)."""
import json, subprocess, sys
from pathlib import Path

LABEL = "source-health"
PREFIX = "Source failing: "

def plan(health, open_titles):
    """Return (titles to open with body, titles to close)."""
    want = {}
    for s in health.get("sources", []):
        if s.get("needsAttention"):
            want[PREFIX + s["name"]] = (f"{s['name']} ({s['jurisdiction']}) has failed {s['consecutiveFailures']} runs in a row.\n\n"
                                        f"Last error: {s.get('error') or 'unknown'}\nLast success: {s.get('lastSuccess') or 'never'}\n"
                                        f"Checked: {health.get('checkedAt')}\n\nFix the URL in scripts/sources.json or set status to blocked with a note.")
    to_open = {t: b for t, b in want.items() if t not in open_titles}
    to_close = [t for t in open_titles if t.startswith(PREFIX) and t not in want]
    return to_open, to_close

def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout

def main():
    health = json.loads(Path("public/data/source-health.json").read_text(encoding="utf-8"))
    subprocess.run(["gh", "label", "create", LABEL, "--color", "d93f0b", "--force"], capture_output=True)
    issues = json.loads(gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number,title", "--limit", "100"))
    by_title = {i["title"]: i["number"] for i in issues}
    to_open, to_close = plan(health, list(by_title))
    for title, body in to_open.items():
        gh("issue", "create", "--title", title, "--body", body, "--label", LABEL)
        print("opened", title)
    for title in to_close:
        gh("issue", "close", str(by_title[title]), "--comment", "Source is fetching again.")
        print("closed", title)

if __name__ == "__main__":
    sys.exit(main())
