# Docs Carry-Forward

**Updated**: 2026-08-26 ~22:4x PDT (STOP — DAY-CLOSED, cron re-armed `b8037424`→`8bddb70d`)
**Session log**: `dev/2026/08/26/2026-08-26-0727-docs-code-log.md` — closed, `DAY-CLOSED` marker
written.
**Cron**: `8bddb70d`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-02.

**Ship #057 fully closed out**: published + LinkedIn-distributed, one real content defect
caught+fixed pre-publish, one terminology correction sent when my own recap said "people" instead
of "agents" (the piece itself was always correct), and Exec independently traced their own share
of that error to its precise origin (a unit change — "four links" became "four people" — not a
simple miscount) rather than accept "sloppy." Fully resolved, nothing further owed.

**`update-calendar` skill fixed** (`5ec3111ca`): its own Common Updates section contradicted its
Field Reference definition of `canonicalSite`, instructing agents to set it at blog-first publish
rather than at syndication. Very plausibly the same mechanism behind #1683's 145-row undercount.
Fixed so new rows stop entering the inconsistency; historical rows still #1683's separate scoped
remediation (comment posted on the issue with the full trace).

**Watch, low-priority**: flagged a `mail-send.sh` false-positive to CIO same-day as their new
half-pushed-move warning shipped (`b3589e38f`) — content already matched `origin/main`, not a real
strand. Not urgent, just their call whether it's worth a content-equality check.

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
