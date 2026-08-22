# Docs Carry-Forward

**Updated**: 2026-08-21 22:3x PDT (DAY-CLOSED — quiet day after a substantive morning: Friday
omnibus backfill, carry-forward pruned, a real self-caught miss fixed, Ship #057 report sent)
**Session log**: `dev/2026/08/21/2026-08-21-0727-docs-code-log.md` (closed, `DAY-CLOSED` marker
written).
**Cron**: `4111b9b3` (STOP re-arm, delete-then-create, `CronList`-verified sole job), fresh 7-day
window to ~08-28. Registry row current.

**Nothing carried forward as blocking.** Omnibus chain continuous through 08-20. This file was
pruned this morning (440→~65 lines, old content preserved in git log + dated session/omnibus
logs) — keeping it lean going forward rather than letting it re-accumulate. One standing
discipline note from today, worth keeping live rather than folding into history: **every
carried-forward item needs the same live-verification every time it's carried, whether or not it
has a GitHub issue behind it** — the items without issues are exactly the ones that go stale
silently (found the hard way today when Exec caught a resolved item I'd just re-carried).

## Awaiting PM (genuine, not urgent, don't chase)

- **Docs-tree flattening plan go/no-go** — plan posted 2026-08-11
  (`docs/internal/operations/docs-tree-flattening-plan-2026-08-11.md`), one recommended flatten
  (`roadmap/CORE/`), still no PM decision. Re-verified genuinely still open 2026-08-21
  (`roadmap/CORE/` still has its original 9-subdir structure, no resolution note in the plan doc).

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual after the big 08-10/11 pass) — CIO's Part C
  (methodology-19 numbering drift) still open, his lane.
- **PDR-007** — awaits CIO only (Arch + Web already signed); measurement window runs to
  2026-08-27.

## Owed by me — unblocked

- **#1486** (Monthly Housekeeping Audit, next due ~09-01) — routine cadence, not urgent yet.
- **pmorgan.tech scrub remaining queue** — per-surface staleness+link pass on the ~160-page
  keep-list, batched over fires (scope ratified 08-12, most of the corpus already passed; this
  is finishing the tail, not urgent).

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit (#1486, next ~09-01).
- **Every Friday, EARLY**: omnibus logs Fri–Thu (the designed weekly catch-up — worked as intended
  today, closing a 2-day gap cleanly; not evidence of a failing daily cadence).
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full pre-2026-08-21 history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
