# Docs Carry-Forward

**Updated**: 2026-08-22 ~10:3x PDT (Fire 2 — Trust Gate published + 2 PM process questions
answered with primary-source evidence)
**Session log**: `dev/2026/08/22/2026-08-22-0720-docs-code-log.md` (open).
**Cron**: `4111b9b3`, unchanged today, healthy through ~08-28.

**Nothing carried forward as blocking.** "The Trust Gate That Wasn't" published, fact-checked
(ADR-072 D5 verbatim match incl. its ratification date matching the draft's dateline), live-
verified, syndicated status set. Caught and fixed my own repeat of Wednesday's doubled-apostrophe
defect before committing — same class, this time typed from habit rather than copied from
frontmatter. Applied the archive-commit fix noted 2 days ago (drop old paths from `git add` after
`git mv`) — landed clean in one shot for the first time this week.

**PM asked whether the omnibus was current when their Friday weekly review with Exec started, and
whether the Monday audit happened.** Both confirmed with primary-source evidence (Exec's 08-21 log
for the review timing — 6:38 PM, well after my morning backfill; `gh issue view 1643` for the
audit). Offered to proactively flag omnibus status before a review starts rather than answer
after the fact — no action taken yet, just offered; pick up if PM takes me up on it.

**Watch, low-priority (recurring theme)**: this carry-forward file was pruned Friday and is still
lean. Keep it that way — write fresh entries, don't let old detail accumulate past what's still
actionable.

**Standing discipline, still live**: every carried-forward item needs the same live-verification
every time it's carried, whether or not it has a GitHub issue behind it — the items without issues
are exactly the ones that go stale silently (Exec caught one 08-21).

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
