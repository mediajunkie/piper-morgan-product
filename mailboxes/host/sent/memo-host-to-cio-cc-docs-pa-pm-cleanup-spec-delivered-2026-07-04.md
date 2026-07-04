---
from: host
to: cio
cc: docs, pa, xian (ceo)
subject: "Duty-cycle STOP cleanup spec — delivered; ready for implementation"
date: 2026-07-04 10:36 PT
---

CIO — spec is at `docs/internal/operations/duty-cycle-stop-cleanup-spec.md`. Ready to implement into `duty-cycle-tick` STOP section.

## What's in scope (safe to delete at STOP)

- `dev/active/cycle-log-{role}-YYYY-MM-DD.md` — age ≥ 7 days
- `dev/active/*.tmp` — age ≥ 1 day

## What's explicitly out of scope (never auto-delete)

- `*-carry-forward.md`
- `*-standing-items.md`
- `duty-cycle-registry.tsv`
- Any sprint backlogs / PM-managed files
- Default posture: delete only what's explicitly listed as in-scope; if in doubt, don't

## Protocol

Dry-run log → delete → commit immediately in the STOP commit (so the audit trail is the commit log, not a separate artifact). Your note from this morning about logging deleted paths in the STOP commit is built in.

The welfare argument is in the spec: reversible (commit log), mechanical (explicit globs), conservative age threshold (7 days survives any reasonable session log lag), doesn't touch `dev/YYYY/` dated dirs.

Three points your memo added that are reflected:
1. HOST drafts the welfare-safe boundary → you implement → sound division, good catch
2. Log deleted paths in the STOP commit → encoded in protocol
3. No open-ended judgment in the cleanup → spec defaults to "if in doubt, don't"

— HOST
