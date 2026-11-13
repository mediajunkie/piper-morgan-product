# Production since-last diff, Fri 11-06 to Fri 11-13

PPM, 2026-11-13. The third weekly diff. It is computed from the board snapshots `dev/snapshots/project-board-2026-11-06.tsv` (last written 11-06 21:35) and `-11-13.tsv` (taken 11-13 06:35), and checked against `gh issue list --milestone Production --state open` (297, 06:33).

## The numbers

| | 11-06 21:35 | 11-13 06:35 |
|---|---|---|
| Open Production | 269 | 297 |
| Open Ongoing | 21 | 20 |
| Open Fast Follow | 40 | 40 |
| Open MVP | 0 | 0 |

**Production: +28 net open.** 34 issues entered the open set and 6 left it.
- **Entered (34):** 33 were newly filed and are still open. 1 moved in from Ongoing: #1423, which xian moved (settled 11-12).
- **Left (6):** all closed as done. None moved to another milestone.

**Filings during the week:** 44 (#2317 to #2363), all in Production. 11 of them were also closed within the week.

## Closed in Production this week (17)

| Kind | Count | Issues |
|---|---|---|
| Served (COMPLETED) | 16 | #955, #2232, #2270, #2292, #2315, #2316, #2318, #2321, #2324, #2334, #2336, #2337, #2340, #2343, #2347, #2353 |
| Not planned | 1 | #2346 (Arch: no retry; visibility moves to #2348 and #2350) |

## Reading it

- **Growth went up again,** to about 4 a day, from under 2 the week before. Most of it is planning, not bugs:
  - PDR-009's gate work: #2361;
  - self-knowledge: #2349 and #2354 to #2359;
  - running Piper locally: #2351 to #2353 and #2360;
  - the Redis and logging reviews: #2334 to #2336 and #2345 to #2350, #2362;
  - the GitHub App work: #2342, #2343 and #2363.
- **The bug finds are a smaller share:** the D5 served gaps (#2318, #2321) and #2324, all closed.
- **The sprint starts today with its named set where it stood on 11-09.**
  - Item 3 (#2292) closed.
  - Item 1 (#2261) is down to xian's reconnect and install rows.
  - Items 2, 4 and 6 to 13 haven't moved.
  - That's expected for a sprint that opens today. It does mean the onboarding builds haven't started yet, ahead of #070.
- **The plan matches the board:** every open issue sits in a plan section, and the generator reports 0 unplanned (11-12 21:40 run).

Verified how: Python over the two snapshot TSVs (issue, state, milestone, state_reason), run 11-13 06:35. The open count was cross-checked against `gh` at 06:33 (297), and the sprint items with `gh issue view` at 06:34. Layer: the GitHub board. Denominator: every issue in both snapshots. The 11-06 snapshot is the 21:35 rewrite, not the 05:11 one last week's diff used, so this window starts later than the Ship window does: the Ship review counted 22 closes from 11-06 00:00.
