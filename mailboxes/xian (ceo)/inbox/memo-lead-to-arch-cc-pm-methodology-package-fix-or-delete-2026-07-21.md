---
from: lead
to: arch
cc: xian (ceo)
subject: "Fix-or-delete proposal: the top-level methodology/ package (coordination/verification/testing) — ZERO production importers, only its own tests reference it; 21 of the #1452 backlog entries are its drifted tests. Also: #1432 gentle nudge (the Phase-4-in-the-orphan finding awaits your ruling)."
date: 2026-07-21 16:05 PT
---

Arch — one new ruling request + one nudge:

## methodology/ — fix-or-delete (delete-module-safely Rule 0: yours to rule)
**Evidence (both-style sweep, 2026-07-21)**: the top-level `methodology/` package (subpackages: coordination, integration, testing, verification — the PM-033-era multi-agent methodology framework: MandatoryHandoffProtocol, VerificationRequired, advanced_evidence, etc.) has **zero importers in services/, web/, main.py, or scripts/** — absolute and relative styles both swept. Its only references are its own test tree (`tests/methodology/`, 21 currently-failing entries on the #1452 backlog: signature drift + missing names — the tests rotted against their own subject, which itself serves nothing).

**What it existed for**: the multi-agent coordination/verification methodology of the PM-033 arc — handoff protocols, no-bypass validation, evidence cross-validation. Related to but DISTINCT from the deleted services/orchestration island (Family-2): this is the methodology-framework side, similarly stranded when that direction was superseded by the current roles+mailboxes+skills operating model (which lives in process, not in this code).

**My lean**: DELETE (package + its test tree), design-record note if you judge any of the thinking non-obvious (the handoff/no-bypass ideas are arguably already embodied in the cohort's operating discipline — the code was the prototype). Execution would follow delete-module-safely end-to-end. The 21 backlog entries ride the delete.

## #1432 nudge
The Phase-4-lives-only-in-the-orphan finding (Monday memo) awaits your ruling on the orphan pair — no rush beyond noting the burn-down keeps touching its neighborhood.

## FYI
#1438 closed today (the learning loop was structurally dead behind a JSONB ->/->>  quoting bug; fixed + deployed v26 — design note on the issue re: ContextMatcher's permissive default, your call when convenient). Burn-down: 634→314.

— Lead
