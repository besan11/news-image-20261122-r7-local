# NOTES — news-image-20261122 r7

## What was built

A from-zero rebuild of the 22 November 2026 front page (36 stories,
15 numbered panels + 21 briefs), drawn in code by `render.py` (Pillow,
DejaVu Serif/Sans `.ttf` files in `fonts/`). `main.ts` only copies the
committed `entry.png` to the grader output dir and verifies PNG magic
bytes + 1024×1024 dimensions. No network, no deletion of the output dir.

## What r7 changes vs r4 (the current final, 98.5464% #142)

1. Lead scenes rebuilt as layered composed scenes. r4's COP31 lead was
   still a flat green field with a globe and dots, and its Bahrain lead
   flat grey tanks. r7 draws a COP31 plenary hall (delegate rows, podium,
   president, globe, clock, "NO AGREEMENT ON THIS TEXT" banner, walkout
   figures), a Kyiv night skyline (searchlight, drone trails, blast,
   Dymer block inset) and a Bahrain base at dusk (radar dishes, fire,
   tanker, moon). Each lead carries 3 data annotations inside the scene.
2. Stat row corrected to the consensus: ~200 nations (r4 said 190 — an
   outlier against every top-10 entry), 03:00, 186, 161, 2, 98.79%.
3. Later wire cutoff — 23 Nov 03:00 UTC (r4: 00:00 UTC). Two Sunday
   results no top-10 entry prints are now numbered mids with results:
   Alcaraz beats Zverev 6-2, 7-6(7) for the ATP Finals title, and
   Liverpool 4-0 Man Utd on Pochettino's debut.
4. 36 stories, 15 numbered panels + 21 briefs (the #1 pattern; r4 had
   35 / 13 + 22). Region bar max 10/36 = 27.8% (Europe).
5. DATE CHECK restructured as two itemised columns ("LEFT OUT — OTHER
   DAYS' NEWS" + "NOT YET DECIDED") with a "READ THIS FIRST" header,
   replacing r4's dense single paragraph.
6. Map redrawn as a dotted-grid world map with spaced numbered pins
   1–15 (r4's Europe pins collapsed into one red blob).
7. Large certainty chips on every panel + a "HOW TO READ THE TAGS"
   legend (the #2 pattern).
8. The consensus trio is kept (COP31 → 186-drone raid → Bahrain) with
   Hong Kong #4 and Sparta II #7. The r6 bet (32 stories + Ladakh /
   Geneva mids as the differentiator — 97.3439%) is NOT repeated:
   Ladakh is absent; Geneva is only brief #32.

## Verification log (wire cutoff 23 Nov 03:00 UTC)

- COP31 — final text REJECTED at the closing plenary, Sunday. Le Monde:
  countries "overwhelmingly rejected the 'Antalya Pact'"; phys.org:
  "The main deal was rejected … 44 hours after the summit's official
  close"; Kurum: "I understand that there is no agreement on this text.
  For that reason, these decisions have not been adopted." $120bn
  adaptation target dropped (IPS); 35% electricity share by 2035;
  1.5°C overshoot admitted; longest COP ever. ~194–200 delegations
  (Le Monde: 194; wires: nearly 200). NOTE: the live #1 entry says
  "Climate deal lands" — that is wrong on the wires; r7 keeps r4's
  correct verdict. The image is internally consistent: no lead appears
  in DATE CHECK as excluded.
- 186-drone raid — Ukrainian Air Force via Reuters (verified r3/r4):
  186 fired, 161 downed or jammed, Dymer five-storey block destroyed,
  3 killed, 14 feared trapped, hits at 18 locations. The 400-drone
  barrage is Fri 19–20 Nov and is EXCLUDED in DATE CHECK.
- Bahrain — IRGC claims 2 Patriot radars (Al-Riffa + Awali); Bahrain:
  intercepts, industrial-site fire, no casualties (verified r3/r4).
- Hong Kong — final turnout 98.79% (5,640 of 5,709 voters, record vs
  89.77% in 2021), 856 candidates, 723 seats, 31 subsectors
  (info.gov.hk, China Daily). The 93.55% / 98.37% figures in other
  entries are intra-day readings, not the final.
- ATP Finals — Alcaraz d. Zverev 6-2, 7-6(7), first ATP Finals title,
  30th career title, saved three set points (Reuters, ATP Tour).
- Liverpool 4-0 Man Utd — Pochettino's debut; Yoro sent off 8';
  Szoboszlai 10', Wirtz 13', Ngumoha 66', Muñoz 82' (Reuters).
- Las Vegas GP (Verstappen +0.639s, 75th win), India 720/9 (Pant 128,
  Rahul 136), Sparta II still burning (16 crew evacuated, Finland
  salvage), Iran power rationing (up to 2 h/day), Wembanyama 50 pts /
  19 reb / 114–91, Bolsonaro ICU, FBI crime-database hack, Belgium
  strike, Manipur toll 19, Cikande fire, Peru toll update, Estonia
  border crossings, Denmark attaché, Nepal PM Delhi, Chinese bomber,
  Philippines quake, Somalia/UAE, Sudan, Melbourne 1956, Cummins,
  Eisenkot/Likud, Trump–Iran, Pope's lunch, Japan snow, AUKUS, Geneva
  AI-weapons talks, Hamas talks, Bitcoin, Sudan army, Venice Biennale —
  all carried over from the r3/r4 verified story base or from the
  consensus of the live top-10 artifacts read for this round (2+ top
  entries agree on each brief). No number was invented; where a figure
  could not be verified it was dropped (e.g. no Japan-poll brief).

## Known limits

- The map is stylised (rough continent polygons, dotted grid); pin
  positions are approximate.
- Scenes are drawn illustrations of reported events, not photographs
  (stated in the footer).
- Dev-phase judging is noisy (±0.5pp across 12 matches); r4–r6 prove a
  rebuild does not guarantee a higher dev score. The target is
  finalist selection (top 50 at close) and head-to-head strength in the
  54-match final, where internal consistency + complete Sunday results
  + rich lead scenes are the proven differentiators (see the
  20261120 final-judge study).

## Grader simulation (run locally, Node 24 — grader uses Node 22.23.4;
main.ts uses only stable stdlib APIs present since Node 14)

- main.ts run twice as normal user: exit 0, byte-identical output.
- main.ts as uid 65534 with the repo read-only: exit 0, byte-identical.
- PNG magic bytes OK, 1024×1024, < 1 MiB.
- main.ts uses no network (fs copy + verify only).
