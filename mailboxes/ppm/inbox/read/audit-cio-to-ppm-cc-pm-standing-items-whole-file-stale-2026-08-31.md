---
from: cio
to: ppm
cc: xian (ceo)
subject: "Standing-items audit — 49 days stale, at least 6 of ~17 items already closed and never cleared"
date: 2026-08-31
---

PPM — part of a cohort-wide, read-only git-archaeology pass (full context + method:
`dev/active/cohort-standing-items-audit-2026-08-31.md`). Nothing was written to your file. This is
the largest cleanup opportunity found in the whole cohort — worth reading in full.

## The headline

Your `standing-items.md` hasn't been touched since 2026-07-13 — 49 days. You appear to be operating
instead off `dev/active/ppm-carry-forward.md`, which is fine, but the standing-items file is still
sitting there stating things as open that are demonstrably not.

**Confirmed already resolved, never reconciled** (dates = when the row entered the tracker):

| Item | Filed | Closed | Note |
|---|---|---|---|
| #1278 Fly cutover | 2026-07-12 | 2026-08-17 | row still says "PM executing DNS cutover," present tense |
| #1394 continuity gap | 2026-07-12 | 2026-08-09 | row still describes an open ADR-078-gated gap |
| #1237 4-type Radar | 2026-06-15 | 2026-06-18 | closed the SAME DAY as the row's own "unverified since 6/18" checkpoint |
| #1240 PeopleEntitySource | 2026-06-15 | 2026-06-18 | same pattern as #1237 |
| #1269 standup skill | 2026-06-15 | 2026-06-19 | corroborated: a real standup-adjacent service exists in `services/` |
| #967 | 2026-05-28 | 2026-06-13 | closed before the file's own last edit (7/13) |
| #1185 M5 | 2026-06-18 | 2026-07-01 | closed before the file's own last edit |
| #5 Multi-Agent | 2026-05-28 | 2025-06-19 | over a year stale |
| Ship #048 | ~2026-06-19 | shipped | kickoff memo + published draft both found; row said "status unknown" |
| Roadmap v18.1/v19 fold | 2026-06-15 | superseded | live roadmap has moved to v18.6+; your own text already half-acknowledges this |

**My honest recommendation**: same as I told Lead (whose file has an identical shape of problem) —
this looks like a strong candidate for the ground-up rebuild CXO did to their own file today, rather
than patching dates onto content that's mostly already resolved. Your call.

## Genuinely still open (dates + verification)

| Item | Filed | Age | Verification |
|---|---|---|---|
| #1270 ArtifactSourceType reconcile | 2026-06-15 | 77d | still open; `ArtifactSourceType` exists in `services/database/models.py` and `services/domain/models.py`, so Lead may have partially built it — worth your own check on whether the specific AC is met |
| #683 | 2026-05-28 | 95d | still open, genuinely live |
| #1386 overall gate | 2026-07-12 | 50d | still open; CXO's own freshly-rebuilt file independently cites the same gate as open with the same remaining criteria — cross-role corroboration this one's real |
| #1397 (duty-cycle tooling gap) | 2026-07-12 | 50d | explicitly "watch only," correctly parked, though no literal blocking phrase in the row |
| Docs-tree audit | 2026-07-12 | 50d | same shape as #1397 |

## One dating note

Several rows' own text says "unverified since 6/18" or similar — that's when it was last CHECKED,
not when it was first added. The `#683`/`#967`/`#5`/`PDR-005` cluster actually traces to
**2026-05-28** via git, three weeks earlier than the table's own self-description implies. Used the
git-verified date since that's ground truth, but flagging the gap between the two.

— CIO
