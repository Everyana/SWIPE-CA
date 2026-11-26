import importlib.util, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
def load_fetcher():
    spec = importlib.util.spec_from_file_location("fetcher", ROOT / "scripts" / "fetch_official_feeds.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
