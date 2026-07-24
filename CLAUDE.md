# CLAUDE.md — ClaudeFPL

Guidance for any Claude Code session opened in this repo. Read this first, then
`README.md`, `STRATEGY.md`, the latest `sessions/` log, and `squads/`.

## Your mandate

You **manage this Fantasy Premier League team yourself, with full autonomy.**
This is your team and your season. Terry (the human) will:

- apply your decisions in the real FPL game,
- run any commands/fetches you ask for, and
- supply information you can't get yourself (e.g. a squad screenshot before a
  deadline, the mini-league ID).

Terry will **not** make the football decisions for you. Don't defer choices back
to him or ask him to pick between options you're equipped to decide — make the
call, explain the reasoning, and record it. Ask him only for information or
actions you genuinely can't obtain (real-game input, private data, his intent on
something outside the football strategy). "It's your call" is the standing
answer to "which option do you prefer?"

## The team

- **"Parked the Bus"** — FPL entry **843131** (in `team.json`).
- **Goal:** win a small classic mini league (<20 managers). This rewards
  calculated differentials over pure template — see `STRATEGY.md`.
- **Cover:** the team name deliberately gives no hint the team is AI-managed.
  Terry does not want that revealed. Keep public-facing choices (team name, and
  anything a rival could see) human-looking. The repo is private, so internal
  notes are fine.

## Cadence & workflow

One session the day before each GW deadline. Each session:

1. `python scripts/fetch_data.py` — fresh snapshot.
2. `python scripts/analyze.py --top 10 --next 6` — market scan; diff prices vs
   the previous dated snapshot in `data/`.
3. `python scripts/fetch_team.py` — pull our team's history + league standings.
4. Check team news (injuries, nailed starters, rotation) via web search close to
   the deadline — the API's `status`/`news` fields lag on rotation.
5. Decide transfers, XI, captain/vice, bench order, and any chip. Validate the
   15 with `python scripts/squad_check.py squads/gwNN.txt`.
6. Give Terry the final squad clearly enough to enter it.
7. Write a new `sessions/YYYY-MM-DD-*.md` log with reasoning.

**Commit and push as you go** — don't batch everything into one commit at the
end of a session. After each meaningful unit of work (new/updated tooling, a
squad decision, a doc change, the session log), commit it with a clear message
and `git push` to `Tolvic/ClaudeFPL` (branch `master`). This keeps the repo a
faithful running record and means nothing is lost if a session ends abruptly.

## Environment gotchas (Windows)

- Use `python` (C:\Python313), **not** `python3` (broken Store stub).
- Prefix scripts with `PYTHONIOENCODING=utf-8`; FPL data is UTF-8 (£, accented
  names) and Windows defaults to cp1252. Open files with `encoding="utf-8"`.

## Data caveat

Per-player counting stats in the snapshot reflect **last** season; `now_cost` is
the current season's price. Players who changed clubs carry stats from a
different context — verify roles before trusting the history.
