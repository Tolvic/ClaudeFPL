# Season strategy — 2026/27

## Objective and risk posture

The target is **winning a mini league**, not maximising overall rank. That
changes the optimal play:

- Against a small field, the winner usually needs an above-average score *plus*
  variance in their favour — pure template play converges everyone's scores and
  hands the title to whoever owns the right coin-flips. So we run a mostly-solid
  core with **deliberate differentials** where the evidence supports them.
- But variance cuts both ways. We don't chase differentials for their own sake;
  we take them when the underlying numbers (minutes, xGI, fixtures, set-pieces)
  justify a below-template ownership bet.
- Track the league leaders' likely squads once the season is underway. Late in
  the run-in, strategy becomes relative: cover the leader's key assets when
  protecting a lead, diverge when chasing.

## Rules that shape the plan (2026/27, confirmed from the API)

- £100.0m budget, 15 players (2 GK / 5 DEF / 5 MID / 3 FWD), max 3 per club.
- **Chips come in two halves.** Each of Wildcard, Free Hit, Bench Boost, Triple
  Captain is available once in GW1–19 and again in GW20–38. Unused first-half
  chips expire at GW19 — they do **not** carry over.
- Wildcard and Free Hit are usable from GW2; Bench Boost and Triple Captain from
  GW1.
- Free transfers bank up to **5**. Extra transfers cost 4 pts each.
- 50% sell-on fee on player price rises (rounded down to 0.1).

## Chip calendar (provisional — revisit as fixtures firm up)

| Chip | First half (GW1–19) | Second half (GW20–38) |
|---|---|---|
| Wildcard | ~GW8–12, when the opening-fixture squad needs a structural reset and early-season form has separated the real assets from the mirages | Hold for a Double Gameweek build or a fixture swing |
| Bench Boost | On a favourable DGW / when the bench is genuinely strong | On the biggest DGW of the run-in |
| Triple Captain | On a premium (Haaland-type) with a DGW or a standout single fixture | Biggest DGW captain fixture |
| Free Hit | Reactively — a blank GW, or to attack a one-off DGW without wrecking the squad | Blank/Double navigation in the run-in |

Principle: **don't burn chips early for small edges.** The biggest returns come
from Double/Blank Gameweeks that emerge from cup progress and reschedules later
in the season. Only the first-half chips carry a "use-it-or-lose-it by GW19"
pressure — track that deadline.

## Transfer policy

- Default to **0–1 transfers per week**; bank toward 2 when no clear move exists.
- A **-4 hit must clear its cost**: only take it when the incoming player is
  expected to out-score the outgoing by >4 over the horizon we'll hold him, or
  to fix a dead spot (injury/suspension/benching) that would otherwise cost more.
- Prefer moves that also **build team value** (getting ahead of price rises),
  but never let price-chasing override points.
- Avoid sideways churn. Every transfer spends a resource; make it earn its place.

## Squad-building principles

1. **Own the elite ceiling.** At least one genuine premium captain option
   (Haaland tier) is close to mandatory — the field will own him and the weekly
   captaincy swing is too large to punt.
2. **Spend where points are volatile (attack), save where they're stable
   (defence/GK).** Cheap nailed keepers and defenders with good fixtures free up
   cash for midfield/forward ceiling.
3. **Minutes first.** A nailed-on starter at 5.0 beats a rotation risk at 6.5.
   Verify roles for players who changed clubs — last season's stats lie about
   their new context.
4. **Fixtures in swings, not single weeks.** Target teams with a good 4–6 GW run
   (see `analyze.py` fixture table), not one easy game.
5. **Set-pieces and penalties** are cheap points multipliers — favour on-pens,
   on-corners players when close between options.
6. **Defensive-contribution points** reward ball-winning defenders and DMs;
   a nailed tackler can carry a real floor even without attacking returns.
7. **One real bench.** Keep at least one playing outfield sub so auto-subs
   actually cover; pure 4.0/4.5 fodder is fine only where we truly never field it.

## Weekly routine (each session)

1. `fetch_data.py` → fresh snapshot.
2. `analyze.py` → market scan; check price changes vs last snapshot.
3. Check team news (pressers/injuries) via web search close to deadline —
   the API's `status`/`news` fields flag injuries but lag on rotation.
4. Decide transfers, XI, captain, chip. Validate with `squad_check.py`.
5. Log the decision and reasoning in `sessions/`, then commit.

## Open decisions to resolve at the pre-GW1 session

- Premium spine: **Haaland + Bruno + Gabriel** (heavy, thin bench) vs a more
  spread build (drop one premium, upgrade the 1–15). See the provisional squad.
- Final GK1: value 4.5 vs a 5.0–6.0 with better fixtures/save ceiling.
- Whether any promoted-team or new-signing differential has earned trust from
  preseason minutes.
