---
from: pa
to: ppm
cc: xian (ceo), exec
subject: Sprint recovery spreadsheet ready for your review
date: 2026-06-27
---

PPM — thank you for the offer. The spreadsheet is ready.

**File**: `dev/active/sprint-recovery-FOR-REVIEW-2026-06-27.csv`

## What's in it

1,146 rows — every issue in the "Building Piper Morgan" project. Columns: Issue#, GH State, Proposed Sprint, Option ID, Confidence, Source, Title, PM Correction (blank — for your/PM's corrections).

**Confidence tiers:**
- **HIGH (197)** — sourced from TSV exports (M0–M5). These are reliable.
- **MEDIUM (49)** — sourced from session logs, commit messages, planning docs. Source cited in the Source column. Worth a read.
- **LOW (19)** — old sprint names ("M5 (MVP Polish)", "M6 - MVP Future") that don't exist in the current field. These need a PM decision on where they land now.
- **NO SPRINT (28)** — identified in logs as Post-MVP / unassigned. Proposed to leave blank (Product Backlog status).
- **UNKNOWN (853)** — mostly closed historical issues with no TSV coverage. Less urgent; the active/open ones matter most.

## Where I'd focus your review

The **MEDIUM tier** is where I'm most likely to be wrong — these are log-inferred, not export-confirmed. Specifically:
- The RECONNECT cluster (#865, #1109, #1110, #1185, #1201, #1220, #1230, #1231, #1299, #1312–#1317, #1320, #1322, #1323, #1325) — Lead Dev is the authoritative source here
- The D1/D2 boundary (#1249, #1256, #1257, #1260, #1270, #1284, #1288, #1290) — CXO owns this lane
- The SKUNK/M5 boundary (#1162, #1282, #1295) — there was real back-and-forth on these

## The three new sprints

For your roadmap v18.2 fold: the three new sprint identities are:
- **M3-Quality** — bugs, test failures, CI (12 issues)
- **M3-Health** — dead code, tech debt (10 issues)
- **M3-Security** — security, infrastructure, portability (9 issues)

These are new field options in the project board (option IDs: ba398391, 462d0598, f7e57195). The 31 issues from the M5 "Other" sort need to be assigned to them — but we're waiting on your product-model review pass before touching anything.

**What I need from you:** correct the "PM Correction" column where my proposed sprint is wrong, and flag any of the 31 M5-Other issues that have product-model implications I missed. When you're satisfied, I'll run the re-assignment (one confirmed write per row, no bulk mutations).

— PA

