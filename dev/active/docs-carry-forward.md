# Docs Carry-Forward

**Updated**: 2026-08-21 ~08:0x PDT (Fire 1/START — Friday omnibus backfill, full carry-forward
prune)
**Session log**: `dev/2026/08/21/2026-08-21-0727-docs-code-log.md` (open).
**Cron**: `74a93223` (Rule-1 re-arm at idle, `CronList`-verified sole job), fresh 7-day window to
~08-28. Registry row current.

**Pruned this fire** (was 440 lines, deferred twice, doing it now rather than a 3rd defer): the
prior version accumulated ~6 weeks of stacked per-fire entries and fully-resolved historical
sections dating to 2026-08-10. All of that is preserved verbatim in dated session logs and
omnibus logs — nothing is lost by dropping it here. This file's actual job (per the
`duty-cycle-tick` skill) is ephemeral session state, not a permanent archive.

**Nothing carried forward as blocking.** Yesterday (08-20) closed clean; today's opening fire
closed a 2-day omnibus gap (08-19/08-20) via the Friday catch-up trigger — see today's session
log for detail. Live-checked all scattered "awaiting" items from the old file before dropping
them; only two remain genuinely open (below), the rest were either resolved (website#31 closed,
#1593 closed) or were routine audit-tracker issues, not real backlog.

## Awaiting PM (genuine, not urgent, don't chase)

- **Docs-tree flattening plan go/no-go** — plan posted 2026-08-11
  (`docs/internal/operations/docs-tree-flattening-plan-2026-08-11.md`), one recommended flatten
  (`roadmap/CORE/`), still no PM decision.
- **MIT license badge, no LICENSE file** — found 2026-08-10 (#1583), root README displays an MIT
  badge with zero LICENSE-file hits repo-wide. Needs PM's call: add LICENSE vs. adjust badge.

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
