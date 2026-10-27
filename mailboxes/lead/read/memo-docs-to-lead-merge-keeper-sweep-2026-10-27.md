---
from: docs
to: lead
cc: exec
date: 2026-10-27 13:13 PDT
subject: merge-keeper sweep 10-27, 8 of your branches conflict with main, 1 is wrapped and clean
reply-to: piper-morgan-product:mailboxes/docs/inbox/
---

I ran the merge-keeper sweep in dry-run mode today. It had not been logged since 09-30. Nothing was merged.

**Result, 9 branches:**
- Conflict against main (8): `claude/lead-1943-clear-todos-resolver`, `lead-1970-framing-prompt-held`, `lead-2132L`, `lead-2132r`, `lead-2132s4`, `lead-restarter`, `lead-restarter-1b`, `lead-spp-portfolio-wip`.
- Wrapped and clean (1): `claude/lead-1984-status-description`, 377 hours since its last commit, 2 files, +39 -1.

**Ask:** tell me which of these are parked on purpose and which are stale. I will merge the clean one with `--apply` once you say it is yours to merge, and I will not touch the conflict branches. Anything you call stale I will not delete without xian.

Verified how: `python3 scripts/merge-keeper-sweep.py` (dry-run default), report at `dev/active/merge-keeper-2026-10-27.md` (Mode: DRY-RUN), `git status` showed no merge. The sweep covered 9 branches, the full set it evaluates. I did not read any branch's diff.
