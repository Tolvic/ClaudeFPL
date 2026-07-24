"""Analyze the current FPL snapshot to surface squad-building signal.

Reads data/bootstrap_latest.json + data/fixtures_latest.json (run fetch_data.py
first). Prints markdown tables: value and premium picks by position, plus early
fixture difficulty by team.

Important caveat for preseason: per-player counting stats (total_points,
minutes, clean_sheets, points_per_game...) reflect LAST season (2025/26).
now_cost is the NEW season (2026/27) starting price. Players who changed clubs
or were promoted carry stats from a different context, so treat their history
with care. Season-start form/event fields are all zero until GW1 plays.

Usage:
    python scripts/analyze.py [--top N] [--next K]
"""
import argparse
import json
import os
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")

POS = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}


def load(name):
    with open(os.path.join(DATA_DIR, f"{name}_latest.json"), encoding="utf-8") as f:
        return json.load(f)


def price(el):
    return el["now_cost"] / 10.0


def build_players(boot):
    teams = {t["id"]: t["short_name"] for t in boot["teams"]}
    out = []
    for e in boot["elements"]:
        out.append({
            "id": e["id"],
            "name": e["web_name"],
            "team": teams[e["team"]],
            "team_id": e["team"],
            "pos": POS[e["element_type"]],
            "pt": e["element_type"],
            "price": price(e),
            "pts": e["total_points"],
            "ppg": float(e["points_per_game"]),
            "mins": e["minutes"],
            "starts": e["starts"],
            "cs": e["clean_sheets"],
            "goals": e["goals_scored"],
            "assists": e["assists"],
            "xgi": float(e["expected_goal_involvements"] or 0),
            "sel": float(e["selected_by_percent"]),
            "status": e["status"],
            "news": e["news"],
        })
    return out


def table(rows, cols, headers):
    line = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = []
    for r in rows:
        body.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join([line, sep] + body)


def value_col(p):
    return round(p["pts"] / p["price"], 1) if p["price"] else 0


def section_by_position(players, top):
    print("\n## Value picks by position (last-season pts per £m, min 900 mins)\n")
    for pt in (1, 2, 3, 4):
        pool = [p for p in players if p["pt"] == pt and p["mins"] >= 900]
        for p in pool:
            p["val"] = value_col(p)
        pool.sort(key=lambda p: p["val"], reverse=True)
        print(f"\n### {POS[pt]}\n")
        rows = pool[:top]
        print(table(rows,
                    ["name", "team", "price", "pts", "ppg", "val", "sel"],
                    ["Player", "Team", "£m", "Pts", "PPG", "Pts/£m", "Sel%"]))


def section_premium(players, top):
    print("\n## Top raw scorers by position (last season)\n")
    for pt in (1, 2, 3, 4):
        pool = [p for p in players if p["pt"] == pt]
        pool.sort(key=lambda p: p["pts"], reverse=True)
        print(f"\n### {POS[pt]}\n")
        print(table(pool[:top],
                    ["name", "team", "price", "pts", "ppg", "goals", "assists", "sel"],
                    ["Player", "Team", "£m", "Pts", "PPG", "G", "A", "Sel%"]))


def section_fixtures(boot, fixtures, k):
    teams = {t["id"]: t["short_name"] for t in boot["teams"]}
    # Only unfinished, scheduled fixtures with an event assigned.
    by_team = defaultdict(list)
    fx = [f for f in fixtures if f.get("event")]
    fx.sort(key=lambda f: (f["event"], f["id"]))
    for f in fx:
        h, a = f["team_h"], f["team_a"]
        by_team[h].append((f["event"], teams[a] + " (H)", f["team_h_difficulty"]))
        by_team[a].append((f["event"], teams[h] + " (A)", f["team_a_difficulty"]))
    print(f"\n## Early fixture difficulty — next {k} GWs (lower = easier)\n")
    rows = []
    for tid, games in by_team.items():
        games.sort()
        first = games[:k]
        total = sum(g[2] for g in first)
        rows.append({
            "team": teams[tid],
            "total": total,
            "avg": round(total / max(len(first), 1), 2),
            "fixtures": ", ".join(f"{g[1]}[{g[2]}]" for g in first),
        })
    rows.sort(key=lambda r: r["total"])
    print(table(rows, ["team", "avg", "fixtures"],
                ["Team", "AvgFDR", f"First {k} fixtures [FDR]"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--next", type=int, default=5)
    args = ap.parse_args()

    boot = load("bootstrap")
    fixtures = load("fixtures")
    players = build_players(boot)

    nxt = next((e for e in boot["events"] if e["is_next"]), None)
    if nxt:
        print(f"# FPL analysis — next deadline GW{nxt['id']} @ {nxt['deadline_time']}")
    section_by_position(players, args.top)
    section_premium(players, args.top)
    section_fixtures(boot, fixtures, args.next)


if __name__ == "__main__":
    main()
