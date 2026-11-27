import unittest, importlib.util
from helpers import ROOT, load_fetcher
F = load_fetcher()
spec = importlib.util.spec_from_file_location("alerts", ROOT / "scripts" / "source_alerts.py")
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)

REG = [{"id": "a", "name": "A Gov", "jurisdiction": "Ontario", "status": "active"},
       {"id": "b", "name": "B Gov", "jurisdiction": "Yukon", "status": "active"},
       {"id": "c", "name": "C Gov", "jurisdiction": "Federal", "status": "blocked", "note": "403"}]

class HealthTests(unittest.TestCase):
    def test_counts_failures_and_resets(self):
        h1 = F.build_health({"A Gov": {"ok": True, "items": 5}, "B Gov": {"ok": False, "items": 0, "error": "403"}}, None, REG, "t1")
        h2 = F.build_health({"A Gov": {"ok": False, "items": 0, "error": "x"}, "B Gov": {"ok": False, "items": 0, "error": "403"}}, h1, REG, "t2")
        h3 = F.build_health({"A Gov": {"ok": True, "items": 2}, "B Gov": {"ok": False, "items": 0, "error": "403"}}, h2, REG, "t3")
        by = {s["name"]: s for s in h3["sources"]}
        self.assertEqual(by["A Gov"]["consecutiveFailures"], 0)
        self.assertEqual(by["A Gov"]["lastSuccess"], "t3")
        self.assertEqual(by["B Gov"]["consecutiveFailures"], 3)
        self.assertTrue(by["B Gov"]["needsAttention"])
        self.assertEqual(by["C Gov"]["status"], "blocked")
        self.assertFalse(by["C Gov"]["needsAttention"])
        self.assertEqual(by["A Gov"]["lastSuccess"], "t3")
        self.assertIsNone(by["B Gov"]["lastSuccess"])

    def test_alert_plan_opens_and_closes(self):
        health = {"checkedAt": "t", "sources": [
            {"name": "B Gov", "jurisdiction": "Yukon", "needsAttention": True, "consecutiveFailures": 3, "error": "403"},
            {"name": "A Gov", "jurisdiction": "Ontario", "needsAttention": False, "consecutiveFailures": 0}]}
        to_open, to_close = A.plan(health, ["Source failing: A Gov", "Unrelated issue"])
        self.assertEqual(list(to_open), ["Source failing: B Gov"])
        self.assertEqual(to_close, ["Source failing: A Gov"])
        to_open, _ = A.plan(health, ["Source failing: B Gov"])
        self.assertEqual(to_open, {})

if __name__ == "__main__":
    unittest.main()
