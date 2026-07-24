"""Validate a 15-man FPL squad against the rules and print its shape.

Reads a squad from a text file (one player per line, `web_name` optionally
followed by `|TEAM` to disambiguate duplicate names). Resolves each to the
current snapshot, then checks: total cost <= budget, 2 GK / 5 DEF / 5 MID /
3 FWD, and max 3 per club. Also prints last-season points so you can eyeball
the squad's pedigree.

Usage:
    python scripts/squad_check.py squads/gw01.txt [--budget 100.0]
"""
import argparse
import json
import os
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
POS = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}
NEED = {"GKP": 2, "DEF": 5, "MID": 5, "FWD": 3}


def load_players():
    with open(os.path.join(DATA_DIR, "bootstrap_latest.json"), encoding="utf-8") as f:
        boot = json.load(f)
    teams = {t["id"]: t["short_name"] for t in boot["teams"]}
    players = []
    for e in boot["elements"]:
        players.append({
            "name": e["web_name"],
            "team": teams[e["team"]],
            "pos": POS[e["element_type"]],
            "price": e["now_cost"] / 10.0,
            "pts": e["total_points"],
            "status": e["status"],
            "news": e["news"],
        })
    return players


def resolve(token, players):
    name, _, team = token.partition("|")
    name, team = name.strip(), team.strip().upper()
    matches = [p for p in players if p["name"].lower() == name.lower()
               and (not team or p["team"] == team)]
    if not matches:
        matches = [p for p in players if name.lower() in p["name"].lower()
                   and (not team or p["team"] == team)]
    return matches


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("squad_file")
    ap.add_argument("--budget", type=float, default=100.0)
    args = ap.parse_args()

    players = load_players()
    with open(args.squad_file, encoding="utf-8") as f:
        tokens = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]

    picked, errors = [], []
    for tok in tokens:
        m = resolve(tok, players)
        if len(m) == 1:
            picked.append(m[0])
        elif not m:
            errors.append(f"NOT FOUND: {tok}")
        else:
            opts = ", ".join(f"{p['name']}|{p['team']}" for p in m)
            errors.append(f"AMBIGUOUS: {tok} -> {opts}")

    for e in errors:
        print("  !!", e)
    if errors:
        print("\nResolve the above before trusting totals.\n")

    by_pos = Counter(p["pos"] for p in picked)
    by_team = Counter(p["team"] for p in picked)
    total = sum(p["price"] for p in picked)

    print(f"Squad size: {len(picked)}/15   Cost: £{total:.1f}m / £{args.budget:.1f}m"
          f"   Bank: £{args.budget - total:.1f}m")
    print("Positions:", dict(by_pos),
          "OK" if all(by_pos.get(k, 0) == v for k, v in NEED.items()) else "<< WRONG")
    over = {t: c for t, c in by_team.items() if c > 3}
    print("Per-club max 3:", "OK" if not over else f"<< VIOLATION {over}")

    print("\nBy position:")
    for pos in ("GKP", "DEF", "MID", "FWD"):
        group = [p for p in picked if p["pos"] == pos]
        for p in sorted(group, key=lambda p: -p["price"]):
            flag = "" if p["status"] == "a" else f"  [{p['status']}] {p['news']}"
            print(f"  {pos} £{p['price']:>4.1f} {p['name']:16s} {p['team']:4s} "
                  f"{p['pts']:>3} pts{flag}")


if __name__ == "__main__":
    main()
