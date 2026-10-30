# Production since-last diff, Fri 10-24 to Fri 10-30

PPM, 2026-10-30. The first weekly diff, as planned on 10-24. It's computed from the board snapshots `dev/snapshots/project-board-2026-10-24.tsv` and `-10-30.tsv` (taken at this morning's START) and checked against `gh issue list --milestone Production` (228 open).

## The numbers

| | 10-24 | 10-30 |
|---|---|---|
| Open Production | 209 | 228 |
| Open MVP (the gate) | 3: #1386, #1595, #2018 | 2: #1386, #2205 |

**Production: +19 net open.** 30 issues entered the open set and 11 left it.
- **Entered (30).** 29 were newly filed. One reopened: #1282 (BYOC-DIST plugin packaging).
- **Left (11), all closed.** Nothing moved out to another milestone.

Filing during the week, all milestones: 46. That's 41 Production, 3 MVP and 2 Ongoing. 12 of the 41 Production filings also closed during the week.

## Closed in Production this week (23)

| Kind | Count | Issues |
|---|---|---|
| Served (COMPLETED) | 16 | #1966, #2045, #2109, #2123, #2125, #2156, #2167, #2169, #2171, #2172, #2173, #2176, #2177, #2182, #2199, #2200 |
| Superseded | 3 | #1242, #1244, #1245 (Dist) |
| Duplicates | 4 | #2198 (of #2197); #2212, #2213, #2214 (of #2218, #2216, #2217) |

Of the 11 closed issues that were open on 10-24, 8 were served: H 3, D 2, C 1, E 1, V 1. The other 3 are the superseded Dist three, which the board still carries under the old PROD-ONBOARD option.

## MVP this week

- **Closed served (4):** #1595, #2018, #2194, #2201.
- **Admitted (3):** #2194, #2201, #2205.
- **Moved out (1):** #2184, MVP to PUB on xian's known-issue ruling (10-29).
- **Still open:** #2205 waits on CXO's ruling on xian's A3/A4. #1386 is the close-out.

## Reading it

Production grew by about 3 a day. The growth is mostly honesty and boundary findings from the gate's served runs: #2189's census rows, #2151's residuals, and #2195/#2197/#2209 on milestone reads. It isn't new feature scope. Every open issue sits in a planned sprint, and the generator reports 0 unplanned.

**The generator's own diff overcounted on its first weekly run.** It read "+135 added", because the 10-29 Sprint backfill gave 110 closed issues a sprint and the generator counted those as scope added. I fixed it today: an issue closed in both snapshots no longer counts as added or removed. It now reads +38 added (the 41 filed, less those outside the plan's table), 11 closed among issues open on 10-24, and 225 promise/journey/seam label changes (the 10-24/25 labelling).

Verified how: Python over the two snapshot TSVs (state, milestone, sprint, state_reason columns), then cross-checked against `gh issue list --milestone Production --state open` (228) and the MVP list (2). Layer: GitHub board. Denominator: every issue in both snapshots (1968 and 2014 rows).
