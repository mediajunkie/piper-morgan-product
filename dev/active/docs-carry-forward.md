# Docs Carry-Forward

**Updated**: 2026-08-26 ~16:5x PDT (Fire 4 — Ship #057's LinkedIn leg + a real update-calendar
skill defect found and fixed)
**Session log**: `dev/2026/08/26/2026-08-26-0727-docs-code-log.md` (open).
**Cron**: `b8037424`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-01.

**Ship #057 fully distributed**: blog (this morning) + LinkedIn (this afternoon, Dispatch-PM's
report, verified live before applying). One real content defect caught+fixed before publish
(verification-chain paragraph miscounted "four people/agents," actually three people/one twice —
fact-checked against 08-18 CIO/HOST/Exec logs), plus a correction sent to Exec/PM when my own
recap sloppily said "people" instead of "agents" (the piece itself was always correct).

**A genuinely valuable find, not just a data point**: Dispatch-PM's `canonicalSite` catch on Ship
#057 traced to a real self-contradiction in `.claude/skills/update-calendar/SKILL.md` — its Common
Updates section instructed setting `canonicalSite→distributed` at blog-first publish, directly
against its own Field Reference definition ("on blog + syndicated"). I'd followed that wrong
instruction verbatim this morning. **Very likely the same mechanism behind #1683's 145-row
undercount at scale.** Fixed the skill (`5ec3111ca`) so new rows stop entering the same
inconsistency; historical rows untouched, still #1683's separate scoped remediation. Posted as a
comment on #1683 (not just mail) since it materially refines the root-cause understanding.

**Standing practice, now durable (from 08-25)**: cross-project replies go via the ratified relay
protocol — real recipient in `to:`, cc `exec`, deliver via ordinary `mail-send.sh` to
`exec/inbox/`, Exec relays; a twice-daily Dispatch-PM sweep is the backstop. If writing directly to
a sibling repo instead, sync first and verify the push landed before treating it as sent — a local
write there is not delivery. Full context: 08-25's session log + `mailboxes/DIRECTORY.md`.

**#1683** (145 editorial-calendar rows genuinely syndicated but `status`/`canonicalSite` never
bumped) and **#1644** (roadmap.md full v19 fold, PPM's lane) and **#1682** (3 minor findings) all
still open, none urgent — see their issues / 08-24's omnibus for full context, not re-detailing
here each day.

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
