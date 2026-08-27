# Docs Carry-Forward

**Updated**: 2026-08-27 ~07:5x PDT (Fire 1 — 2-day omnibus gap found+closed, duplicate issue
#1684 cleaned up)
**Session log**: `dev/2026/08/27/2026-08-27-0727-docs-code-log.md` (open).
**Cron**: `8bddb70d`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-02.

**Omnibus chain now continuous through 08-26** — a genuine 2-day gap (08-25, 08-26; 12+10 session
logs) found at this morning's START and closed via two sequential subagent dispatches (avoiding
the shared-CSV write race, matching the 08-24 precedent). Both ran the full skill for real, not a
shortcut synthesis. **Found and closed a real orphaned duplicate**: #1684/#1685 both filed
independently for the identical `create_todo` consent-gate finding — #1685 shipped same-day
(08-25), #1684 sat open as an orphan; closed as duplicate. A second flagged finding (#1462 vs #829
milestone conflict) turned out already resolved by PPM this morning before I even checked — no
action needed.

**Ship #057, #1683/update-calendar skill fix, and the mail-send.sh false-positive report all
fully closed out as of 08-26's STOP** — see 08-26's session log or its now-completed omnibus for
full detail, not re-detailing here.

**Standing practice, durable (from 08-25)**: cross-project replies go via the ratified relay
protocol — real recipient in `to:`, cc `exec`, deliver via ordinary `mail-send.sh` to
`exec/inbox/`, Exec relays; a twice-daily Dispatch-PM sweep is the backstop. If writing directly to
a sibling repo instead, sync first and verify the push landed before treating it as sent.

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
