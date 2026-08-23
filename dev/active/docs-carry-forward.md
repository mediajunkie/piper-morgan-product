# Docs Carry-Forward

**Updated**: 2026-08-22 22:3x PDT (DAY-CLOSED — one post's full lifecycle: publish, fact-check,
syndicate; 2 PM process questions answered; a repeat self-caught defect)
**Session log**: `dev/2026/08/22/2026-08-22-0720-docs-code-log.md` (closed, `DAY-CLOSED` marker
written).
**Cron**: `eaf72d50` (STOP re-arm, delete-then-create, `CronList`-verified sole job), fresh 7-day
window to ~08-29. Registry row current.

**Nothing carried forward as blocking.** "The Trust Gate That Wasn't" fully closed today —
published, fact-checked (ADR-072 D5 verbatim match, incl. its own ratification date matching the
draft's dateline exactly), live-verified, and syndicated to both Medium and LinkedIn. PM's two
process questions (omnibus timing at Friday's review; whether the Monday audit ran) both answered
from primary sources, not confidence — offered to proactively flag omnibus status before future
reviews rather than answer after the fact; no action taken yet, pick up if PM takes it up.

**Watch — 2nd occurrence of a defect class**: the YAML-doubled-apostrophe-into-CSV mistake
recurred today (Wednesday: copied from frontmatter; today: typed from habit). Both self-caught
before committing, but two in three days is worth naming as a pattern — if it recurs a third
time, add an explicit check to the calendar-edit routine rather than keep relying on catching it
by habit.

**Watch, low-priority (recurring theme)**: this carry-forward file was pruned Friday and is still
lean — kept that way through today's rewrites. Keep writing fresh entries rather than letting old
detail accumulate.

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
  08-21, closing a 2-day gap cleanly; not evidence of a failing daily cadence).
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
