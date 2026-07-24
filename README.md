# ClaudeFPL

Claude-managed Fantasy Premier League team for the **2026/27** season. Goal:
win Terry's mini league.

## How this works

- The day before each gameweek deadline, Terry runs one session with Claude.
- Claude decides the squad, transfers, captaincy, and chip usage for that GW.
- Terry applies the changes in the real FPL game and reports results back.
- Every session's decisions and reasoning are committed here so the whole
  campaign is auditable and each session can build on the last.

## Layout

```
scripts/
  fetch_data.py     # snapshot the public FPL API into data/ (run first each session)
  analyze.py        # value/premium/fixture tables from the latest snapshot
  squad_check.py    # validate a 15-man squad file against the rules
data/
  *_latest.json     # newest snapshot (git-ignored; regenerate with fetch_data.py)
  *_YYYYMMDD.json   # dated snapshots kept for the record
squads/
  gwNN_*.txt        # squad files (one player per line, web_name|TEAM)
sessions/
  YYYY-MM-DD-*.md   # per-session decision log + reasoning
STRATEGY.md         # season-long strategy: chips, transfer policy, principles
```

## Session workflow

```bash
python scripts/fetch_data.py                       # pull fresh data
python scripts/analyze.py --top 10 --next 6        # scan the market
python scripts/squad_check.py squads/gwNN.txt      # validate before committing
```

Then write the decisions into `sessions/` and commit.

## Data notes

- Source: the public, unauthenticated FPL API (`fantasy.premierleague.com/api`).
- **Preseason caveat:** per-player counting stats (points, minutes, clean sheets)
  reflect *last* season (2025/26); `now_cost` is the *new* season price. Players
  who changed clubs carry stats from their old context — verify roles before
  trusting the history.

## Status

- **2026-07-24** — Repo bootstrapped in preseason. GW1 deadline **Fri 21 Aug
  2026, 17:30 UTC**. Tooling built, market analyzed, provisional GW1 squad
  drafted (`squads/gw01_provisional.txt`). Squad to be finalized at the pre-GW1
  session. See `sessions/2026-07-24-preseason-setup.md`.
