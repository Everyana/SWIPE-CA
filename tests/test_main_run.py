import io, json, os, shutil, tempfile, unittest, urllib.error
from unittest import mock
from helpers import ROOT, load_fetcher

def fake_rss(host, n=2):
    items = "".join(f"<item><title>Notice {i} from {host}</title><description>Apply by December 30, 2026.</description>"
                    f"<link>https://{host}/news/{i}</link><pubDate>Tue, 24 Nov 2026 1{i}:00:00 GMT</pubDate></item>" for i in range(n))
    return f"<rss><channel>{items}</channel></rss>".encode()

class FakeResp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False

class MainRunTests(unittest.TestCase):
    def test_full_run_writes_feed_archive_and_health(self):
        F = load_fetcher()
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "public", "data")); os.makedirs(os.path.join(tmp, "scripts"))
            shutil.copy(ROOT / "scripts" / "curated_notices.json", os.path.join(tmp, "scripts"))
            failing = F.SOURCES[0]["name"]
            def urlopen(req, timeout=0):
                src = next(s for s in F.SOURCES if s["url"] == req.full_url)
                if src["name"] == failing:
                    raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)
                if src.get("format"):
                    raise ValueError("page adapters not faked")
                return FakeResp(fake_rss(src["hosts"][0]))
            cwd = os.getcwd(); os.chdir(tmp)
            try:
                with mock.patch.object(F.urllib.request, "urlopen", urlopen):
                    F.main()
            finally:
                os.chdir(cwd)
            feed = json.load(open(os.path.join(tmp, "public/data/notices.json")))
            health = json.load(open(os.path.join(tmp, "public/data/source-health.json")))
            archive = json.load(open(os.path.join(tmp, "public/data/archive.json")))
            self.assertTrue(feed["notices"])
            self.assertLessEqual(len(feed["notices"]), 40)
            self.assertTrue(all(n["url"].startswith("https://") for n in feed["notices"]))
            self.assertTrue(any(n.get("deadline") == "2026-12-30" for n in feed["notices"]))
            by = {s["name"]: s for s in health["sources"]}
            self.assertEqual(by[failing]["status"], "error")
            self.assertEqual(by[failing]["consecutiveFailures"], 1)
            self.assertEqual(by["Statistics Canada"]["status"], "blocked")
            self.assertGreaterEqual(len(archive["notices"]), len(feed["notices"]))
        finally:
            shutil.rmtree(tmp)

if __name__ == "__main__":
    unittest.main()
