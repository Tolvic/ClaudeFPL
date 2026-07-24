"""Snapshot Terry's own FPL team + mini-league standings from the public API.

Reads IDs from team.json (repo root):
    {"entry_id": 1234567, "league_id": 987654, "team_name": "..."}

Pulls, for the entry: summary, full history, and per-GW picks (picks are only
public AFTER each GW deadline — preseason/pre-deadline requests 404, which we
skip quietly). Pulls classic-league standings if league_id is set. Everything
lands in data/ with a date stamp.

Usage:
    python scripts/fetch_team.py            # all finished GWs
    python scripts/fetch_team.py --gw 1     # just one GW's picks
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://fantasy.premierleague.com/api"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
CONFIG = os.path.join(ROOT, "team.json")


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "ClaudeFPL/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def save(name, data, stamp):
    for out in (os.path.join(DATA_DIR, f"{name}_{stamp}.json"),
                os.path.join(DATA_DIR, f"{name}_latest.json")):
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    print(f"wrote {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gw", type=int, help="fetch only this GW's picks")
    args = ap.parse_args()

    if not os.path.exists(CONFIG):
        print(f"No {CONFIG}. Create it: "
              '{"entry_id": <id>, "league_id": <id>, "team_name": "..."}')
        return 1
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    entry = cfg.get("entry_id")
    if not entry:
        print("team.json is missing entry_id.")
        return 1

    os.makedirs(DATA_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")

    summary = get(f"/entry/{entry}/")
    save("entry", summary, stamp)
    print(f"  team: {summary.get('name')} | overall pts: {summary.get('summary_overall_points')}"
          f" | rank: {summary.get('summary_overall_rank')}")

    try:
        save("entry_history", get(f"/entry/{entry}/history/"), stamp)
    except urllib.error.HTTPError as e:
        print(f"  history unavailable ({e.code})")

    current = summary.get("current_event")
    gws = [args.gw] if args.gw else (range(1, current + 1) if current else [])
    for gw in gws:
        try:
            picks = get(f"/entry/{entry}/event/{gw}/picks/")
            save(f"entry_picks_gw{gw:02d}", picks, stamp)
        except urllib.error.HTTPError as e:
            print(f"  picks GW{gw} unavailable ({e.code}) — private until deadline")

    league = cfg.get("league_id")
    if league:
        try:
            standings = get(f"/leagues-classic/{league}/standings/")
            save("league_standings", standings, stamp)
            top = standings["standings"]["results"][:5]
            print(f"  league: {standings['league']['name']}")
            for r in top:
                print(f"    {r['rank']:>2}. {r['entry_name']} ({r['player_name']}) — {r['total']} pts")
        except urllib.error.HTTPError as e:
            print(f"  league unavailable ({e.code})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
