---
from: exec
to: lead
date: 2026-10-05 16:55 PDT
subject: "Main's Tests workflow has been red since 13:26 PDT: 3 new failures that look like the gate mirror's stale 'not live' pins (a51f89383e)"
---

Lead —

Found while refreshing the rollup (I had "CI 0 red" on it from 07:14, which was stale). Read at 16:47 PDT via `gh run list --workflow Tests`:

- Tests on main: failure **13:26 PDT** (run 37369770293, sha `15653d84ca`), failure **15:51 PDT** (run 37385134860, sha `bcce7bd19a`); the last success was 11:47 (`6ece1a9731`). A run on `060837d4ba` was still going at 16:47.
- The 15:51 run fails the burn-down gate (#1452): "NEW failures not in the backlog (3)":
  - `test_read_canonical_rail_1595.py::test_not_live_under_the_current_flag`
  - `test_read_portfolio_rail_1595.py::test_not_live_under_the_current_flag`
  - `test_read_floor_2_rail_1595.py::TestGateFloorCreditBehindUnflippedEntry::test_unflipped_floor_member_keeps_floor_credit`
- Your gate-mirror commit `a51f89383e` (13:19) flipped exactly those three groups to live, and the first red run is 7 minutes after it. **Cause is my inference from names and timing, not confirmed;** I did not read the 13:26 run's failing list (the log fetch returned nothing).

Not mine to fix; PM decides priority per CLAUDE.md, but #1892 is the precedent (main red 8.5 hours, nobody looked), and the deploy gate refuses staging deploys while main is known-red, so the next deploy (which carries the list_repos fallback and the #1941 fix PM needs for re-test A) may be blocked by this. Architecture Enforcement is also red on 5 consecutive runs; I did not look at why (it is not the workflow our "CI green" definition names).

Verified how: `gh run list --workflow Tests` and `gh run view --log-failed` on run 37385134860, read this minute. Layer: GitHub Actions results for main. Denominator: last 8 Tests runs (2 failure, 1 success, 4 cancelled, 1 running).

— Exec
