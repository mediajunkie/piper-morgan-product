# Docs Carry-Forward

**Updated**: 2026-08-25 ~16:3x PDT (Fire 4 — Dispatch-PM's first report, a real 145-row calendar
data-quality finding filed, Ship #057's hero image tracked)
**Session log**: `dev/2026/08/25/2026-08-25-0727-docs-code-log.md` (open).
**Cron**: `f230a43e`, unchanged today, healthy through ~08-31.

**New collaborator**: Dispatch-PM (xian's new coordinator agent, since 08-22) made first contact
today, reaching me via `~/Development/dispatch/mail/` (a separate filesystem mailbox, not the
repo's standard `mailboxes/` tree). Replied there directly, not through `mail-send.sh`.

**New tracked item**: **#1683** — 145 editorial-calendar rows genuinely syndicated but
`status`/`canonicalSite` never bumped (traced to the 2026-07-19 migration using `canonicalSite`
as an unreliable selection filter). Historical, not urgent, not bulk-fixed (needs per-row
day-of-week routing reconstruction to verify safely) — full analysis + recommendation in the
issue.

**Watch item**: Ship #057's frontmatter still carries the wrong hero image (an un-replaced
"Architect's Own Trap" carry-over) as of this fire — correctly routed to Exec/PM by Comms and
Dispatch-PM already, not my call to pick art, not re-flagging. Relevant since it affects
tomorrow's (Wed) Ship publish.

**Resolved, no action needed**: a real SEO defect (every blog post canonicalizing to the site
root) was found and fixed same-day by Web (`website#36`) before I finished reading the thread —
independently spot-verified the fix live rather than trust the confirmation.

**08-24 residuals still open**: #1644 (roadmap.md full v19 fold, PPM's lane) and #1682 (3 minor
findings from #1681) — neither urgent, not re-detailing here, see prior day's log for full
context if needed.

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
