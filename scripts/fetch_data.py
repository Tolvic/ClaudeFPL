"""Fetch and snapshot public FPL API data.

The FPL API is unauthenticated and public. We snapshot the key endpoints to
data/ with a date stamp so every session has a reproducible record of what the
game looked like at decision time.

Usage:
    python scripts/fetch_data.py
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

BASE = "https://fantasy.premierleague.com/api"
ENDPOINTS = {
    "bootstrap": "/bootstrap-static/",
    "fixtures": "/fixtures/",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")


def fetch(path: str) -> object:
    url = BASE + path
    req = urllib.request.Request(url, headers={"User-Agent": "ClaudeFPL/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    os.makedirs(DATA_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    for name, path in ENDPOINTS.items():
        data = fetch(path)
        # Dated snapshot for the historical record.
        dated = os.path.join(DATA_DIR, f"{name}_{stamp}.json")
        # Stable "latest" pointer the analysis script reads by default.
        latest = os.path.join(DATA_DIR, f"{name}_latest.json")
        for out in (dated, latest):
            with open(out, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        print(f"wrote {name}: {dated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
