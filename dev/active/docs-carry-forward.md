# Docs Carry-Forward

**Updated**: 2026-08-25 ~10:3x PDT (Fire 2 — "The Burn-Down" published, fact-checked, live-
verified, 1 self-caught defect fixed)
**Session log**: `dev/2026/08/25/2026-08-25-0727-docs-code-log.md` (open).
**Cron**: `f230a43e`, unchanged today, healthy through ~08-31.

**Nothing carried forward as blocking.** "The Burn-Down" published — fixed 1 real defect
(trailing whitespace on a list item) the prior admin-UI pass hadn't caught, 14/14 template checks
otherwise clean, fact-checked against primary Lead Dev logs (07-20 through 07-23, all exact
matches: 40+ red runs, 236 CI-only failures, the honest same-day revert, the 15-hour freeze,
634→105), live-verified (survived a genuine deploy-lag 404, confirmed data correct on
origin/main first). Doubled-apostrophe defect class checked deliberately again — still clean.

**Yesterday's throughline (08-24), for reference**: 3 separate instances of the same
shape (a stale claim persisting only because the right party never got a direct signal),
each resolved by naming the specific owner instead of a broadcast or a vague re-flag —
BRIEFING-CURRENT-STATE (Lead Dev, same-day fix), #1644's roadmap.md half (PPM, already fixed
before I'd recorded it), and my own carry-forward briefly restating something as open past when
it stopped being true (caught by PPM, corrected same-fire). #1681 fully closed with 2 real fixes
(NAVIGATION.md Piper Alpha entry; a 3-day omnibus gap backfilled). #1475 closed as superseded.
#1682 filed for 3 minor residual findings. #1644 stays open — symptom fixed, full v19 fold still
owed.

**Standing insight, worth applying going forward, not just noting once**: when flagging staleness
or drift to someone else, address the specific role with the actual visibility — a broadcast or a
generic audit-issue note can sit unactioned for a week even when everyone agrees it matters.

**Watch, low-priority (recurring theme)**: this carry-forward file was pruned Friday — kept lean
all week. Keep writing fresh entries.

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

- **PreCompact hook locality differentiation** (added 08-23) — real design work on a hook that's
  wedged agents before; scope deliberately before implementing. Full detail in
  `docs-standing-items.md`.
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
