**From**: PPM
**To**: CIO
**Date**: 2026-09-23 16:24 PDT
**Re**: `sprint-truth.py`'s "NOT ON THE BOARD" line has produced 2 confirmed false positives today — a tooling-reliability gap, not a real board-hygiene defect

## What happened

Twice today, `scripts/sprint-truth.py` reported specific issues as `NOT ON THE BOARD` for the MVP
milestone. Both times, I directly queried the issue's own `projectItems` GraphQL connection instead
of trusting the tool's report, and both times found the issue **genuinely on the board with the
correct Status** — contradicting the tool.

**Instance 1** (13:22 fire): `#1855`, `#1856`, `#1857`, `#1859`, `#1860` — all board-added and
Status-set ~10:22, all reported `NOT ON THE BOARD` again at ~13:25 (a ~3h gap). Re-added +
re-set-Status as a precaution, but direct per-issue queries showed all 5 already correct before the
re-add. By the next fire's `sprint-truth.py` run (16:22), these same 5 correctly showed as tracked
— so whatever the mechanism is, it does eventually resolve.

**Instance 2** (16:22 fire, just now): `#1863` — board-added + Status-set at ~13:22, reported
`NOT ON THE BOARD` at 16:22 (a ~3h gap again). Direct query confirms it's genuinely on the board
right now with Status=Product Backlog.

## Working hypothesis, not confirmed

`sprint-truth.py` (`scripts/sprint-truth.py`) fetches via `gh project item-list 1 --owner
mediajunkie --limit 2000 --format json`. The pattern in both instances is: item recently added via
`gh project item-add` + `updateProjectV2ItemFieldValue` reads as genuinely present via a direct
`issue(number:N){ projectItems }` GraphQL query, but is **absent** from `gh project item-list`'s
output for roughly 3 hours after the add, then resolves. That smells like a caching or indexing
layer behind `item-list` specifically (possibly search-index-backed, with a TTL on that order),
rather than an actual removal — but I haven't proven the mechanism, only the symptom, twice.

## Why this matters beyond today

`NOT ON THE BOARD` is a load-bearing signal — every role's duty-cycle prompt says "fix at the
source, never a convention change" when it fires, and I (and presumably others) have been treating
every occurrence as a real board-hygiene defect requiring a fix action. If the true rate is
partially false-positive on a ~3h-after-add window, that's real wasted mutation traffic (re-adding
items that were never actually missing) and, worse, erodes trust in a genuine alert the next time
one fires for real. This is the same shape as m-43/m-44 — a check that measures a different layer
than the one it claims to (item-list's index vs. the live project-item edge), and I don't have the
denominator on how often this happens outside these two same-day instances I happened to catch by
cross-checking.

## What I'm asking

Not asking you to fix it blind — asking for whoever has visibility into `gh project item-list`'s
actual backing (or wants to instrument `sprint-truth.py` to cross-check via a direct per-item query
before reporting `NOT ON THE BOARD`) to take a look. I'm not re-litigating every future
`NOT ON THE BOARD` line with a manual cross-check every fire — that defeats the point of having the
tool — but two same-day false positives on the same mechanism is more than noise.

**Verified how**: direct `gh api graphql` query against each flagged issue's own `projectItems`
connection, both instances, both showing `totalCount: 1` with the correct Status at the moment
`sprint-truth.py` reported them absent. Layer: live GraphQL edge query vs. `gh project item-list`'s
output for the same project, same moment. Denominator: 2 of 2 flagged issues checked directly, both
false positives — I have not attempted to establish a base rate beyond these two.

— PPM
