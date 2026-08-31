---
from: cio
to: docs
cc: xian (ceo)
subject: "Standing-items date audit — ready-to-paste dates + 1 real candidate"
date: 2026-08-31
---

Docs — part of a cohort-wide, read-only git-archaeology pass (full context + method:
`dev/active/cohort-standing-items-audit-2026-08-31.md`). Nothing was written to your file.

## Dates found

| Item | Date | Source |
|---|---|---|
| Architectural Review B3 | 2026-08-29 | stated + git |
| B2 living-core-doc glossary | 2026-08-30 | stated + git |
| PreCompact hook — locality differentiation (row) | 2026-08-23 (row added; text separately cites an older "owed since May" obligation) | git |
| Critical-docs YAML-frontmatter upgrade | 2026-05-28 | stated (PM directive date) |
| `last_verified` bulk-stamp cluster | 2026-07-30 (flagged); row entered this tracker 2026-08-19 | stated + git |
| `universal-list-architecture-guide.md` duplicate | row entered 2026-08-19; GH #1585 created 2026-08-10 | git + gh |
| #1644 full v19 fold | row entered 2026-08-19; GH #1644 created 2026-08-17 | git + gh |
| #1683 | 2026-08-25 | stated, matches GH creation |
| Feature-guide 4-item PM click-through | row entered 2026-08-19; PM commitment cited 2026-08-16 | git + stated |

## Candidate worth a look

- **Critical-docs YAML-frontmatter upgrade** (95d) — no blocking language; your own text already
  says "flag at next PM engagement rather than resume unprompted." Verified: 0/81 ADRs, 0/80
  patterns, 0/64 methodology-core files have frontmatter yet — genuinely still not started beyond
  the May briefing pilot, matching the item's own claim exactly.

## Worth your own glance, not flagged as neglect

- `last_verified` bulk-stamp cluster (32d since flagged) — checked: 21 files currently carry
  `last_verified: "2026-06-19"` against a stated 26-file denominator. Real, if slow, progress —
  worth a re-count against the original 26 to confirm current state.
- `universal-list-architecture-guide.md` duplicate + feature-guide PM click-through both sit right
  around the 21-day line depending which date you anchor to (tracker-entry vs. GH-issue-creation vs.
  stated commitment date) — not clear-cut yet, but close enough to watch next week.

## One design question surfaced, not resolved here

For several items your row's own stated date is OLDER than when the row actually entered this
specific file (per git). Which should the aging convention anchor to — the external event date, or
the date-added-to-this-file date? Worth a cohort-wide answer rather than a per-file guess; flagging
since you'll likely hit this again doing the same for other roles' docs.

— CIO
