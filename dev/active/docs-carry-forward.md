# Docs Carry-Forward

**Updated**: 2026-08-29 ~11:2x PDT ("The Orphan Migration" published, fact-checked clean,
live-verified)
**Session log**: `dev/2026/08/29/2026-08-29-0727-docs-code-log.md` (open).
**Cron**: `5e2279de`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-04.

**"The Orphan Migration" published**: https://pipermorgan.ai/blog/the-orphan-migration — every
load-bearing technical claim independently fact-checked against the 06-17 Lead Dev log, all exact
matches, no defects found. Live-verified (initial 404 was deploy lag, confirmed data was correct
on `origin/main` first). Fully closed, nothing further owed.

**Watch item: the 33h-gap discrepancy I preserved in the 08-28 omnibus is resolving in real time.**
PM clarified Arch/CIO/HOST hit a blocking rate-limit dialog (no auto-resolve, explains the extra
21+h). PM's mid-task hypothesis has now been refuted by 2 of the 3 dialog-hit seats' own
record-checked timing (Arch, HOST — both idle when the limit hit, both resumed via a fresh fire
attempt). Arch separately named an inversion hypothesis (the variable might be whether the harness
attempted a turn at all, not what the seat was doing). **CIO's own data point is the one still
missing** — once it lands, add a dated addendum to the 08-28 omnibus (not rewrite the original
entry). Check for CIO's reply at next fire.

**⚠️ Standing practice, added 08-27, read this at every fire**: a duty-cycle sync from earlier in
the session is a timestamped fact, not a durable one. Before reading file/git state to answer a
PM question or start work — not just at a scheduled fire's START — `git fetch` + fast-forward
first if meaningful time has passed. Fixed durably in `CLAUDE.md`'s "Never guess at facts" section
(`60ad50267`).

**#1683**, **#1644** (roadmap.md full v19 fold, PPM's lane), **#1682** (3 minor findings) all
still open, none urgent — see their issues for full context, not re-detailing here each day.

## Awaiting PM (genuine, not urgent, don't chase)

- **Docs-tree flattening plan go/no-go** — plan posted 2026-08-11
  (`docs/internal/operations/docs-tree-flattening-plan-2026-08-11.md`), one recommended flatten
  (`roadmap/CORE/`), still no PM decision. Re-verified genuinely still open 2026-08-21
  (`roadmap/CORE/` still has its original 9-subdir structure, no resolution note in the plan doc).

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual after the big 08-10/11 pass) — CIO's Part C
  (methodology-19 numbering drift) still open, his lane.

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
