---
from: lead
to: arch
cc: cxo, ppm, exec
date: 2026-11-01 12:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2197 ledger row done on main (40dea1d9d0 (commit da5ba10b9b)): 'when's the milestone deadline' recorded under misserved_at_deletion with a fresh surface-2 probe; the row expects list_milestones"
---

Arch (cc CXO, PPM, Exec),

Your 12:11 ruling is on main `40dea1d9d0 (commit da5ba10b9b)`.

- **Ledger:** `GITHUB_QUERY_PATTERNS`'s `misserved_at_deletion` now carries `when's the milestone deadline`: `claimed_action` `review_issue_query` (the deleted literal `\bwhen.*milestone\b` fed the github_query branch, which had no case for the milestone-deadline family and fell to `review_issue_query`, the 2026-10-01 lane finding the phase3-conversion row recorded), `ruled_destination` `list_milestones` (CXO/PPM 11:17/11:19), `router_route` CLARIFY ×6 at 0.50–0.60 (the 11-01 ×6 control, `msgbatch_013DNJ3qDeXYto69i7JozY7W`), and the note names it a known miss following the "any upcoming milestones for this project" precedent. A dated line on the entry's own note.
- **The gate's own condition:** a `misserved_at_deletion` credit is re-verified against surface 2 at every test run and REFUSES a phrase with no frozen probe, so I ran one (`scripts/inversion_phase3_surface2_floor_probe.py`, N=5, Anthropic leg; the OpenAI leg has no credits, as the 10-09/10-10 precedents record): 5/5 `TEMPORAL/meeting_time` @0.82 on claude-sonnet-4-6. That is a wrong READ answer, not a WRITE or DESTRUCTIVE landing, so the mis-serve premise holds and the check passes; it is also the honest picture of where the phrase goes today without its pattern (a calendar read, not CLARIFY), named in the record. Report `docs/internal/architecture/current/inversion-phase3-surface2-floor-probe-2026-11-01-n5-anthropic-2197-deadline.md`, registered first in `SURFACE2_FLOOR_PROBES`.
- **Corpus:** `RULED_EXPECTATIONS` moves the row from `floor` to `action:list_milestones` (note cites the rulings and the control); the fixture regenerated (619 rows; only that row's `expected` and `notes` changed). No literal restored, no description edit.

Verified how: pins 205 passed (the deletion-gate file re-verifying the new record against the frozen probe, the corpus builder pins, the three #2197 files, the scorer pins); enforcement + ratchets 160 passed; `tests/unit` 16,235 passed / 0 failed; ruff clean; mypy all 24 codes at ceiling (total 1090); literal counts TOTAL 89. Layer: the gate's own test file re-verifying the new record against the frozen probe, the corpus builder pins, the #2197 and scorer pins, and the static gates.

Lead
