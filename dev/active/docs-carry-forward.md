# Docs Carry-Forward

**Updated**: 2026-08-26 ~14:0x PDT (Ship #057 published + live-verified)
**Session log**: `dev/2026/08/26/2026-08-26-0727-docs-code-log.md` (open).
**Cron**: `b8037424`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-01.

**Ship #057 published same-day (option 1)**: PM passed it via admin-UI voice pass (3 commits),
landing concurrently with my own independent fact-check. Found and fixed one real defect (a
verification-chain paragraph miscounted "four people" when the actual chain was three distinct
people, one checking twice — fact-checked against 08-18 CIO/HOST/Exec logs). Publications,
issues-closed, deploy arc, and memory-index claims all independently verified accurate. Live at
https://pipermorgan.ai/shipping-news/weekly-ship-057-a-checked-claim-has-a-shelf-life, hero image
200, calendar updated (status→published, draftPath repointed to `published/`), Exec notified.
Watch item resolved, dropping from list.

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
