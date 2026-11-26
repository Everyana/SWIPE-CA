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

class DeadlineTests(unittest.TestCase):
    P = "2026-11-13T00:00:00+00:00"
    def test_english_cues(self):
        self.assertEqual(F.extract_deadline("The state portal lists December 2 as the closing date. Apply by December 2, 2026.", self.P), "2026-12-02")
        self.assertEqual(F.extract_deadline("Applications are open until January 15.", self.P), "2027-01-15")
        self.assertEqual(F.extract_deadline("Deadline: Nov. 30", self.P), "2026-11-30")
        self.assertEqual(F.extract_deadline("Submit bids by November 30.", self.P), "2026-11-30")
    def test_french_cues(self):
        self.assertEqual(F.extract_deadline("Consultation jusqu'au 15 décembre 2026.", self.P), "2026-12-15")
        self.assertEqual(F.extract_deadline("Date limite : 1er février", self.P), "2027-02-01")
    def test_no_cue_no_deadline(self):
        self.assertIsNone(F.extract_deadline("The games run December 11 to 22.", self.P))
        self.assertIsNone(F.extract_deadline("", self.P))
        self.assertIsNone(F.extract_deadline("before the meeting", self.P))
    def test_parse_sets_deadline(self):
        rss = b"""<rss><channel><item><title>Grant intake opens</title><description>Apply by January 31, 2027.</description>
        <link>https://news.ontario.ca/en/release/9</link><pubDate>Tue, 24 Nov 2026 12:00:00 GMT</pubDate></item></channel></rss>"""
        self.assertEqual(F.parse(rss, SRC)[0]["deadline"], "2027-01-31")

class DeadlineEventTests(unittest.TestCase):
    P = "2026-11-21T00:00:00+00:00"
    def test_event_end_is_not_a_deadline(self):
        self.assertIsNone(F.extract_deadline("Plan ahead in coastal areas from Tuesday, Nov. 24 until Thursday, Nov. 26, 2026.", self.P))
        self.assertIsNone(F.extract_deadline("Le Grand Marché de Noël se déroule jusqu'au 24 décembre.", self.P))
    def test_feedback_until_is_a_deadline(self):
        self.assertEqual(F.extract_deadline("Residents can share feedback until February 8, 2027.", self.P), "2027-02-08")
        self.assertEqual(F.extract_deadline("Les commentaires sont acceptés jusqu'au 15 décembre.", self.P), "2026-12-15")

class TopicAdvisoryTests(unittest.TestCase):
    def test_advisories_are_dropped(self):
        for t in ["Media Advisory: Minister X Available to Media", "Minister Sarkaria to Hold a Press Conference",
                  "Wednesday, November 25, 2026", "Avis médias - Agenda public du premier ministre du Québec - 25 novembre 2026",
                  "/R E P R I S E -- INVITATION À LA PRESSE - La machine"]:
            self.assertTrue(F.is_advisory(t), t)
        self.assertTrue(F.is_advisory("Itinerary", "https://www.pm.gc.ca/en/news/media-advisories/2026/11/24/x"))
        self.assertFalse(F.is_advisory("Province opens school registration"))
    def test_new_topics(self):
        self.assertEqual(F.topic("Provincial Government Introduces New Cities Act"), "Laws and regulations")
        self.assertEqual(F.topic("Government of Saskatchewan Releases Mid-Year Financial Report"), "Budget and finance")
        self.assertEqual(F.topic("Ontario Announces Bold Plan to Build Mines Faster"), "Economy and business")
        self.assertEqual(F.topic("Prix du Québec 2026 : X reçoit le prix"), "Culture and awards")
    def test_parse_skips_advisory(self):
        rss = b"""<rss><channel><item><title>Media Advisory: Minister to speak</title>
        <link>https://news.ontario.ca/en/advisory/1</link><pubDate>Tue, 24 Nov 2026 12:00:00 GMT</pubDate></item></channel></rss>"""
        self.assertEqual(F.parse(rss, SRC), [])

GNB = b'{"data":{"newsModelList":{"items":[{"datePublished":"2026-11-25T10:46:00.000-04:00","title_en":"Public participation process begins for air quality approval","leadLine_en":"Comments are accepted until May 24, 2027.","title_fr":"D\\u00e9but du processus","leadLine_fr":"x","detailUrl":"/content/GNB3/en/news/n-b.2026.11.public-participation.html"},{"datePublished":"2026-11-25T10:00:00.000-04:00","title_en":"Bad","detailUrl":"https://evil.example/x"}]}}}'

class GnbTests(unittest.TestCase):
    def test_gnb_json(self):
        src = {"name": "Government of New Brunswick", "jurisdiction": "New Brunswick", "lang": "en", "url": "https://www.gnb.ca/bin/gnb/newswire", "hosts": ["gnb.ca"], "format": "gnb"}
        items = F.parse(GNB, src)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["url"], "https://www.gnb.ca/en/news/n-b.2026.11.public-participation.html")
        self.assertEqual(items[0]["summary"], "Comments are accepted until May 24, 2027.")
        self.assertEqual(items[0]["deadline"], "2027-05-24")
        self.assertTrue(items[0]["publishedAt"].startswith("2026-11-25T14:46"))

class NoiseTests(unittest.TestCase):
    def test_test_items_and_weekly_advisories(self):
        self.assertTrue(F.is_advisory("test-nov22-212pm"))
        self.assertTrue(F.is_advisory("Ministerial Activities Advisory for the week of November 24-30, 2026"))
        self.assertTrue(F.is_advisory("UPDATE – Saturday, November 21, 2026"))
        self.assertFalse(F.is_advisory("Testing emergency alerts to cellphones"))
        self.assertFalse(F.is_advisory("Province Advises of Alert Ready Test Tomorrow"))
