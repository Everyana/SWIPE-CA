import json, unittest
from urllib.parse import urlparse
from helpers import ROOT, load_fetcher

REG = json.loads((ROOT / "scripts" / "sources.json").read_text(encoding="utf-8"))["sources"]
LEVELS = {"federal", "provincial", "territorial", "municipal", "regional", "institution"}

class RegistryTests(unittest.TestCase):
    def test_fields_and_values(self):
        ids = set()
        for s in REG:
            for k in ("id", "name", "jurisdiction", "level", "lang", "url", "access", "hosts", "verifiedAt", "status"):
                self.assertIn(k, s, f"{s.get('id')} missing {k}")
            self.assertNotIn(s["id"], ids); ids.add(s["id"])
            self.assertIn(s["level"], LEVELS)
            self.assertIn(s["lang"], ("en", "fr"))
            self.assertIn(s["status"], ("active", "blocked", "paused"))
            self.assertTrue(s["access"] in ("rss", "atom") or s["access"].startswith(("page:", "json:")))
            self.assertEqual(urlparse(s["url"]).scheme, "https", s["id"])
            self.assertTrue(s["hosts"])
            if s["status"] != "active" or s["access"].startswith("json:"):
                self.assertTrue(s.get("note"), f"{s['id']} needs a note explaining its status")

    def test_fetcher_loads_only_active(self):
        F = load_fetcher()
        active = [s["name"] for s in REG if s["status"] == "active"]
        self.assertEqual([s["name"] for s in F.SOURCES], active)
        self.assertNotIn("Statistics Canada", active)

if __name__ == "__main__":
    unittest.main()
