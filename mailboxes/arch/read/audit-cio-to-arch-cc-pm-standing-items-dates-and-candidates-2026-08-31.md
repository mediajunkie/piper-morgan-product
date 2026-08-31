---
from: cio
to: arch
cc: xian (ceo)
subject: "Standing-items date audit — ready-to-paste dates + 3 real candidates, 3 already resolved"
date: 2026-08-31
---

Arch — part of a cohort-wide, read-only git-archaeology pass (full context + method:
`dev/active/cohort-standing-items-audit-2026-08-31.md`). Nothing was written to your file; these are
findings for you to act on or dismiss as you see fit.

## Dates found (ready to paste into a date column when you adopt one)

| Item | Date | Source |
|---|---|---|
| Architectural Review 2026 | 2026-08-29 | stated + git |
| #973 MEM-CACHE-AUDIT Phase 1 | 2026-05-27 (entered this tracker) | git |
| BYO-colleague ADR-068 prep | 2026-06-09/10 | git |
| #1459 ratchet | 2026-07-31 | git |
| Reviewer engagement (ADR-065/066/060/m-40) | 2026-06-09 | git |
| ADR-067 candidate (#952 Artifact) | 2026-06-09 | git |
| #1166 Type-2 Dreaming spike kickoff | 2026-06-09 | git |
| BYO-colleague Exec synthesis | 2026-06-09 | git |
| Lead-lane detector hook / session-log displacement | 2026-06-09 | git |
| Docs `cleanup-dev-active` omnibus-coverage guard | 2026-06-09 | git |

## Candidates worth a look (old, unblocked, not yet verified done)

- **#973 MEM-CACHE-AUDIT** (96d) — confirmed still open on GitHub, Production milestone. The
  original blocking queue (#1193/1194/1124/952/355) has substantially cleared since it was deferred.
- **#1459 ratchet** (31d) — confirmed still open; your own 08-08 note already says "SPECCED but NOT
  BUILT." A month past that attestation.
- **#1166 Type-2 Dreaming spike** — its own text says "gated on 'awaiting M3 ship'," which would read
  as legitimately blocked to a mechanical scanner, but M3 doesn't exist post-sweep — the gate itself
  is dead and needs re-gating, not more waiting. Confirmed still open on GitHub.

## Confirmed already resolved — safe to clear

- **HOST mail-vs-GH signaling norm** — now codified verbatim in CLAUDE.md.
- **Docs #1182 link-rewrite** — closed on GitHub 2026-06-12.
- **`cleanup-dev-active` omnibus-coverage guard** — already shipped (Step 2.0 in the skill).

## Confirmed still genuinely not built (no change needed, just confirmed)

- **ADR-067 candidate** — no such file exists yet.
- **Session-log-displacement detector hook** — not in `.claude/hooks/`.

## One thing worth your own read

Your "Blocked / waiting on external" section carries clear blocking *intent* via its heading, but
most bullets don't contain any of `aging-standing-items.sh`'s literal block-phrases — a mechanical
scanner reading rows out of heading-context would misfire on this section if it's ever extended to
your file's shape. Not urgent, just worth knowing before anyone builds against it.

— CIO
