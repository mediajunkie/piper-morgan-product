# Production since-last diff, Fri 10-30 to Fri 11-06

PPM, 2026-11-06. The second weekly diff. It's computed from the board snapshots `dev/snapshots/project-board-2026-10-30.tsv` (last written 10-30 21:58, after Go and the tracking audit) and `-11-06.tsv` (taken 11-06 05:1x), and checked against `gh issue list --milestone Production --state open` (252).

## The numbers

| | 10-30 21:58 | 11-06 05:1x |
|---|---|---|
| Open Production | 242 | 252 |
| Open MVP | 0 (closed at Go, 10-30 17:03) | 0 |
| Open Ongoing | 48 | 22 |

**Production: +10 net open.** 36 issues entered the open set and 26 left it.
- **Entered (36).** 33 newly filed; 3 moved in from Ongoing (#865, #1340, #2196). None reopened.
- **Left (26), all closed.** Nothing moved out to another milestone.

Filing during the week, all milestones: 51. That's 41 Production, 9 Ongoing and 1 Icebox.

## Closed in Production this week (34)

| Kind | Count | Issues |
|---|---|---|
| Served (COMPLETED) | 30 | see `gh issue list --milestone Production --state closed --search "closed:2026-10-31..2026-11-06"` |
| Not planned | 4 | #1131, #1357, #1371, #1506 (old test-debt rows, closed in Exec's 11-02 doc audit routing) |

Of the 26 closed issues that were open on 10-30, the served ones by sprint: D 5, H 4, TECHDEBT 4, PUB 2, Design 2, CONVO 2, RECONNECT 2, unset 1.

## Reading it

Growth slowed from about 3 a day last week to under 2. The week's filings came from two places: xian's 10-30 tracking audit (the evening of the snapshot, so mostly already in the 242) and the advisor's 11-04 beta session (#2266–#2278) with the tenancy work that followed (#2279, #2281–#2283, #2290–#2293). The closes lean to data boundaries and honesty (D 5, H 4), which is where the invite hold sits. Ongoing fell by 26: 30 left (17 closed served, 2 not planned, 8 moved to Icebox, 3 moved into Production) and 4 entered.

Every open issue sits in a planned sprint; the generator reports 0 unplanned (11-05 21:3x run).

Verified how: Python over the two snapshot TSVs (issue, state, milestone, sprint, state_reason), run 11-06; cross-checked against `gh issue list --milestone Production --state open` (252, same run). Layer: GitHub board. Denominator: every issue in both snapshots (2036 and 2087 rows). The 10-30 snapshot was rewritten at 21:58 that day, so this diff starts after the day's audit filings; against the 10-30 START count (228) the week is +24.
