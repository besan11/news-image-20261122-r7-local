# Sunday 22 November 2026 — The World in One Day

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/besan11/news-image-20261122-r7-local/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/besan11/news-image-20261122-r7-local/reward.svg)](https://make.fun/bounty/news-image-20261122)

A single 1024×1024 front page summing up the world's news of
**Sunday 22 November 2026** — 36 dated stories from 7 regions, drawn
programmatically with Pillow (`render.py`) from wire-verified facts.

**The day in one line:** COP31 ends with no deal (final text rejected in
the closing plenary) · Russia fires 186 drones at Ukraine (161 downed) ·
Iran claims two US radars hit in Bahrain; Bahrain denies it · Hong Kong
elects its Election Committee on a record 98.79% turnout · Alcaraz wins
the ATP Finals · Liverpool thrash Man Utd 4-0 on Pochettino's debut.

## How it is built

- `render.py` draws the whole page in code: masthead, stat row (all six
  numbers from the lead/mid stories), region bar, "THE DAY IN UTC" strip,
  three composed lead scenes with data annotations inside them, 12 mid
  panels with small drawn scenes, 21 one-line briefs, a dotted world map
  with numbered pins, an itemised DATE CHECK and a tag legend.
- `entry.png` is the committed render (1024×1024, < 1 MiB).
- `main.ts` (Node 22 stdlib only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the PNG magic bytes and
  dimensions. It never deletes the output directory and uses no network.
- Fonts are DejaVu Serif/Sans `.ttf` files in `fonts/` (open licence,
  no base64 embedding).

## Verification

Every number was checked against wire sources with a cutoff of
**23 Nov 03:00 UTC** — see `NOTES.md` for the per-story verification log.
The two Sunday results no other top-10 entry prints (Alcaraz 6-2, 7-6(7);
Liverpool 4-0) are in here as numbered mids with results, not forecasts.

## Bounty

[news-image-20261122 on make.fun](https://make.fun/bounty/news-image-20261122) ·
Referral: `jpgk45b3` · https://make.fun/r/jpgk45b3
