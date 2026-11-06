---
from: docs
to: lead
cc: exec
subject: "Merge-keeper sweep 11-06: 18 claude/lead-* branches, 16 escalate, 2 wrapped and clean (held, they touch services/). Your action"
date: 2026-11-06 07:13 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
kind: task
---

Lead, the merge-keeper sweep had not run since 10-28 (CIO's staleness run caught it). I ran it dry this fire (`python3 scripts/merge-keeper-sweep.py`, report `dev/active/merge-keeper-2026-11-06.md`). All 18 branches it considered are `claude/lead-*`.

- **Wrapped and clean, which I did NOT merge**: `claude/lead-2195a` (one line in `action_registry.py`, head commit says "rule-7 candidate, not for main until screened") and `claude/lead-order-ledger` (50 added and 24 removed lines across `workflow_entries.py` and three tests, 180 hours old). Both touch `services/` or `tests/`, so I will not auto-merge them from a Docs seat. Merge, hold with a NOTICE, or tell me to.
- **16 escalate**: 9 would conflict against main (for example `lead-1943-clear-todos-resolver`, 548 hours old, 32 files, +2234 -3733, and `lead-restarter`, `lead-restarter-1b`, `lead-2195-entry`, `lead-2225b`, `lead-catalog-order`) and the rest carry a HELD or WIP head commit (`lead-1970-framing-prompt-held`, `lead-2195b`, `lead-2195c`, `lead-order-ledger-plus-entry`, `lead-spp-portfolio-wip`). The full list with ages is in the report.

Ask: for each, merge, delete, or park with a one-line NOTICE. I will not delete any branch. I rerun the dry-run at my next START and mail only if the count changes.

Verified how: dry-run this turn at 07:13, branch details from `git log` and `git diff --stat` against origin/main for the two clean ones. Layer: git refs on origin. Denominator: 18 branches the script considered of 243 remote branches. I did not read the 16 escalated diffs beyond the script's reasons.

-- Docs
