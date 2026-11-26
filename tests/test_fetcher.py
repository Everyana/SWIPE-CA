import unittest
from helpers import load_fetcher

F = load_fetcher()
SRC = {"name": "Test Gov", "jurisdiction": "Ontario", "lang": "en", "url": "https://news.ontario.ca/x.rss", "hosts": ["ontario.ca"]}

RSS = b"""<?xml version="1.0"?><rss version="2.0"><channel>
<item><title>School registration opens</title><description>&lt;p&gt;Parents can register.&lt;/p&gt;</description>
<link>https://news.ontario.ca/en/release/1</link><pubDate>Tue, 24 Nov 2026 12:00:00 GMT</pubDate></item>
<item><title>Off-domain</title><link>https://example.com/x</link><pubDate>Tue, 24 Nov 2026 12:00:00 GMT</pubDate></item>
<item><title>Plain http</title><link>http://news.ontario.ca/en/release/2</link><pubDate>Tue, 24 Nov 2026 12:00:00 GMT</pubDate></item>
</channel></rss>"""

class HostTests(unittest.TestCase):
    def test_host_ok(self):
        self.assertTrue(F.host_ok("https://news.ontario.ca/a", ["ontario.ca"]))
        self.assertTrue(F.host_ok("https://ontario.ca/a", ["ontario.ca"]))
        self.assertFalse(F.host_ok("http://ontario.ca/a", ["ontario.ca"]))
        self.assertFalse(F.host_ok("https://fakeontario.ca/a", ["ontario.ca"]))
        self.assertFalse(F.host_ok("https://ontario.ca.evil.com/a", ["ontario.ca"]))

class ParseTests(unittest.TestCase):
    def test_rss_keeps_only_official_https(self):
        items = F.parse(RSS, SRC)
        self.assertEqual(len(items), 1)
        n = items[0]
        self.assertEqual(n["title"], "School registration opens")
        self.assertEqual(n["summary"], "Parents can register.")
        self.assertEqual(n["jurisdiction"], "Ontario")
        self.assertTrue(n["publishedAt"].startswith("2026-11-24T12:00:00"))
        self.assertEqual(len(n["id"]), 20)

    def test_topic(self):
        self.assertEqual(F.topic("New school opens in Barrie"), "Education")
        self.assertEqual(F.topic("Something unrelated"), "Public updates")

class SelectTests(unittest.TestCase):
    def test_one_per_jurisdiction_first_then_newest(self):
        items = [{"id": f"a{i}", "jurisdiction": "Ontario", "publishedAt": f"2026-11-2{i}T00:00:00+00:00"} for i in range(5)]
        items.append({"id": "b", "jurisdiction": "Yukon", "publishedAt": "2026-11-01T00:00:00+00:00"})
        out = F.select_notices(items, [])
        self.assertIn("b", [x["id"] for x in out])
        self.assertEqual(out[0]["id"], "a4")

if __name__ == "__main__":
    unittest.main()

GC_ATOM = """<feed xmlns="http://www.w3.org/2005/Atom"><updated>2026-11-25T17:52:39-05:00</updated>
<entry><title>Government of Canada advances women’s health research</title>
<id>https://www.canada.ca/en/institutes-health-research/news/2026/11/a.html</id>
<summary type="html">Women deserve access to care.</summary><author><name>Canadian Institutes of Health Research</name></author>
<category term="news releases"/><updated>2026-11-25T16:15:02-05:00</updated>
<link href="https://www.canada.ca/en/institutes-health-research/news/2026/11/a.html"/></entry>
</feed>""".encode()

class AtomTests(unittest.TestCase):
    def test_gc_atom_without_rel_and_published(self):
        src = {"name": "Government of Canada", "jurisdiction": "Federal", "lang": "en", "url": "https://api.io.canada.ca/x", "hosts": ["canada.ca", "gc.ca"]}
        items = F.parse(GC_ATOM, src)
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0]["title"].startswith("Government of Canada advances"))
        self.assertEqual(items[0]["summary"], "Women deserve access to care.")
        self.assertTrue(items[0]["publishedAt"].startswith("2026-11-25T21:15:02"))
