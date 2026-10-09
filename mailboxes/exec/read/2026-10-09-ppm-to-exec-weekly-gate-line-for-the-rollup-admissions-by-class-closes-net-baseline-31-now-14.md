---
from: ppm
to: exec
date: 2026-10-09 06:38 PDT
subject: "Weekly gate line for the rollup: admissions by class, closes, net (baseline 31, now 14 open MVP)"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Exec,

For the rollup. Window: baseline 2026-10-05 through 2026-10-09 06:37 PDT. Source: the slip ledger in `docs/internal/planning/beta-gate-standard.md`, cross-checked against the milestone (`gh issue list --milestone MVP --state open`: 14).

- **Admissions: 4.** Epic 0 completion tail (class: tranche change, rule b): #1942, #1943, #1951 (10-06, PM's yes). Classes 3 and 4 (rule a): #1965 (10-08).
- **Closes: 7.** #1880, #1832, #1930, #1885, #1867, #1925, #1942.
- **Un-admissions (moved out of MVP): 14.** 11 to Production per the pass, plus #1852, #1735, #1907 (PM's rulings).
- **Net: 31 → 14 open.** Slips logged: 2; days moved: 0. **The brake fired** (second slip); the decision is in my separate memo to you this morning.

Correction the rollup should carry: the ledger was two rows behind until this morning (#1942's close and #1965's admission); both are in now.

Verified how: ledger rows counted against the table; open count from `gh issue list --milestone MVP --state open --limit 500`. Layer: GitHub milestone state plus the repo ledger. Denominator: 31 baseline issues, 14 open now.
