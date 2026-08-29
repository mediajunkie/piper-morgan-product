# Docs Carry-Forward

**Updated**: 2026-08-29 ~07:4x PDT (Fire 1 — 08-28 omnibus done, chain continuous through 08-28)
**Session log**: `dev/2026/08/29/2026-08-29-0727-docs-code-log.md` (open).
**Cron**: `5e2279de`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-04.

**08-28 omnibus done** (`28eb629a8` + `6d9f590aa`), chain now continuous through 08-28.
**Noted, not mine to chase**: Arch/CIO/HOST stayed dark 21+ hours past PM's stated account-wide
freeze window while every other role recovered by dawn — both their own logs flag an unresolved
second cause, neither explains it. Arch/CIO/HOST's own lane.

**08-28's threads (PDR-007 ratified, heading-defect class fully closed, brokering protocol
ratified) are all resolved** — see 08-28's session log for full detail, not re-detailing here.

**Heading-defect class fully closed** (spanned 08-27→08-28): started as 2 posts, ended as 9 —
checked the other 9 of Dispatch-PM's original 11 rather than accept "probably not worth it," found
7 more genuinely live-broken, fixed source + live layers on all, live-verified. 2 correctly
excluded with stated reasons. All 11 rows now accounted for. Comms/Dispatch-PM notified. Done.

**Cross-project reply protocol formally ratified by PM today** — was already how I'd been
operating since 08-25; both DIRECTORY.md follow-up asks Dispatch-PM raised were already satisfied
by my 08-25 edit, confirmed rather than assumed. Standing practice unchanged: real recipient in
`to:`, cc `exec`, deliver to `exec/inbox/`, Exec relays or points; Dispatch-PM's own sweep is the
backstop.

**⚠️ Standing practice, added 08-27, read this at every fire**: a duty-cycle sync from earlier in
the session is a timestamped fact, not a durable one. Before reading file/git state to answer a
PM question or start work — not just at a scheduled fire's START — `git fetch` + fast-forward
first if meaningful time has passed. Fixed durably in `CLAUDE.md`'s "Never guess at facts" section
(`60ad50267`). Applied every fire since without incident.

**Ship #058 contributor report filed** (`3b4baaf34`) — window Aug 21-27, full detail in the
report itself, not re-duplicating here.

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
