import importlib.util, io, unittest, urllib.error
from helpers import ROOT
spec = importlib.util.spec_from_file_location("links", ROOT / "scripts" / "check_links.py")
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)

class R(io.BytesIO):
    def __init__(self, status): super().__init__(b""); self.status = status
    def __enter__(self): return self
    def __exit__(self, *a): return False

def opener_for(codes):
    def op(req, timeout=0):
        code = codes[req.full_url]
        if code is None: raise OSError("dns")
        if code >= 400: raise urllib.error.HTTPError(req.full_url, code, "x", {}, None)
        return R(code)
    return op

class LinkTests(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(L.classify(200), "ok"); self.assertEqual(L.classify(301), "ok")
        self.assertEqual(L.classify(403), "unverified"); self.assertEqual(L.classify(404), "broken"); self.assertEqual(L.classify(0), "broken")
    def test_run(self):
        notices = [{"id": "a", "title": "A", "url": "https://x.ca/a"}, {"id": "b", "title": "B", "url": "https://x.ca/b"},
                   {"id": "c", "title": "C", "url": "https://x.ca/c"}]
        rows = L.run(notices, opener_for({"https://x.ca/a": 200, "https://x.ca/b": 404, "https://x.ca/c": None}))
        self.assertEqual([r["result"] for r in rows], ["ok", "broken", "broken"])

if __name__ == "__main__":
    unittest.main()
