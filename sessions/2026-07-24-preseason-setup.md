# Session — 2026-07-24 (preseason setup)

**Context:** First session. Repo was empty. 2026/27 FPL game just launched.
GW1 deadline **Fri 21 Aug 2026, 17:30 UTC** — ~4 weeks out. No transfers/chips
to submit yet; this session builds the foundation and a provisional GW1 squad.

## What I did

- Built tooling: `fetch_data.py`, `analyze.py`, `squad_check.py`.
- Snapshotted the API (`data/*_20260724.json`).
- Analyzed the market and drafted a provisional GW1 squad.

## Market read (from the 2026-07-24 snapshot)

Per-player stats are **last season (2025/26)**; prices are 2026/27. Standouts:

- **Forwards:** Haaland (£15.5m, 239 pts, 71% owned) — the non-negotiable
  captain anchor. Next tier: Thiago (£8.0 BRE, 181), João Pedro (£7.5 CHE, 177),
  Watkins (£8.0 AVL, 167). Gyökeres now at ARS (£7.5, 128 pts at old club).
- **Midfielders:** B.Fernandes (£12.0 MUN, 235) leads; Semenyo (£8.5, now MCI,
  202), Gibbs-White (£8.0 NFO, 188), Rice (£7.5 ARS, 184). Value: Anderson
  (£6.5 MCI, 180), Wilson (£6.5 LEE, 168), Yarmoliuk (£5.0 BRE, 104, nailed).
- **Defenders:** Gabriel (£8.0 ARS, 209) elite. Value: Guéhi (£6.0, now MCI,
  179 — role at City unconfirmed), Virgil (£6.5 LIV), Senesi (£6.0 TOT),
  Tarkowski (£6.0 EVE, great fixtures), Mitchell (£4.5 CRY, 135 — cheap+playing).
- **Goalkeepers:** best value Verbruggen (£4.5 BHA, 130), Kelleher (£5.0 BRE,
  143), Petrović (£4.5 BOU). Rare cheap starter: Dubravka (£4.0 TOT, 3150 mins).
- **Cheap enablers that actually play:** Hughes (£4.5 CRY MID), Diop (£4.0 IPS
  DEF), Dubravka (£4.0 TOT GK).

**Transfers reflected in the data** (stats earned at old clubs — verify new
roles before trusting): Guéhi & Semenyo → Man City, Gyökeres → Arsenal,
João Pedro → Chelsea, Ekitiké → Liverpool.

**Best opening fixtures (avg FDR, first 6 GWs):** EVE, MUN, NEW, LIV (all 2.83),
then ARS/TOT/CHE/MCI (3.0). MUN's start (HUL, IPS at home-ish) is soft — bodes
well for Bruno as early captain/vice. Worst: BOU (3.67), FUL (3.33).

## Provisional GW1 squad (£100.0m exactly) — `squads/gw01_provisional.txt`

| Pos | Player | £m | Rationale |
|---|---|---|---|
| GK | Verbruggen (BHA) | 4.5 | Best-value keeper, nailed. |
| GK | Dubravka (TOT) | 4.0 | £4.0 backup; plays enough to cover if needed. |
| DEF | Gabriel (ARS) | 8.0 | Elite defender, attacking + CS ceiling. |
| DEF | Tarkowski (EVE) | 6.0 | Everton's soft opening run. |
| DEF | Truffert (BOU) | 5.5 | Attacking fullback, 165 pts. |
| DEF | Mitchell (CRY) | 4.5 | Cheap, nailed, productive. |
| DEF | Diop (IPS) | 4.0 | Pure fodder / value enabler. |
| MID | B.Fernandes (MUN) | 12.0 | Premium mid, easy start, pens. |
| MID | Gibbs-White (NFO) | 8.0 | 188 pts, set-pieces. |
| MID | Wilson (LEE) | 6.5 | Value mid, 168 pts. |
| MID | Yarmoliuk (BRE) | 5.0 | Nailed 2652-min enabler at 5.0. |
| MID | Hughes (CRY) | 4.5 | Cheap playing enabler. |
| FWD | Haaland (MCI) | 15.5 | Captain. Non-negotiable. |
| FWD | João Pedro (CHE) | 7.5 | Mid-price scorer, decent fixtures. |
| FWD | Kusi-Asare (FUL) | 4.5 | Bench fodder (won't be fielded). |

**Provisional XI (4-4-2):** Verbruggen; Gabriel, Tarkowski, Mitchell, Truffert;
B.Fernandes, Gibbs-White, Wilson, Yarmoliuk; Haaland, João Pedro.
**Captain:** Haaland (MCI v BOU, H). **Vice:** B.Fernandes (MUN v HUL, A).
**Bench order:** Hughes (plays) → Diop → Kusi-Asare; GK bench Dubravka.

4-4-2 is the strongest shape here — it fields four real defenders and three real
mids plus one nailed enabler (Yarmoliuk), rather than starting both cheap
enablers. Watch items before lock: Truffert has the only hard opener (MCI away) —
bench candidate; confirm Gabriel/João Pedro fit and nailed; captaincy could tilt
to Bruno as a differential if Haaland carries any knock.

Constraints verified by `squad_check.py`: 15/15, £100.0m, positions OK, max 2
per club.

## Why provisional, not final

Locking a squad 4 weeks out wastes information. Before the pre-GW1 session,
these will move: player **prices** (rise/fall with transfers in/out), **preseason
minutes** (who's actually nailed, esp. at new clubs), and **injuries/team news**.
The tool already caught one: Onana (my first 5.0 mid pick) has a knee injury —
swapped to Yarmoliuk.

## To do at the pre-GW1 session (the day before 21 Aug)

1. Re-fetch; diff prices vs this snapshot.
2. Resolve the premium-spine vs spread question (see STRATEGY.md).
3. Confirm nailed roles for club-changers (Guéhi/Semenyo at City especially).
4. Check final pressers for GW1 team news; set captain on confirmed-fit premium.
5. Lock the 15, XI, captain. No wildcard available in GW1 (starts GW2), so the
   opening squad must be right — it can only be repaired by transfers or a GW2+
   wildcard.
