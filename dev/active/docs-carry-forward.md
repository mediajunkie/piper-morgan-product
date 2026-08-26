# Docs Carry-Forward

**Updated**: 2026-08-25 ~22:4x PDT (STOP — DAY-CLOSED, cron re-armed `f230a43e`→`b8037424`)
**Session log**: `dev/2026/08/25/2026-08-25-0727-docs-code-log.md` — closed, `DAY-CLOSED` marker
written.
**Cron**: `b8037424`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-01.

**Cross-project mail — the day's real lesson, now durable in two places**: a write to
`~/Development/dispatch/` (or any sibling repo) is NOT delivery until explicitly committed and
pushed — unlike this repo's `mailboxes/`, nothing forces that step. Discovered this fire when a
Dispatch-PM claim that my reply "reached them" turned out false; found and delivered 7 of my own
memos stranded back to 2026-07-29 (`f098707`), corrected the false claim (`40c8769`), and flagged
2 of Comms' own stranded files to them (they self-resolved same day via the new protocol below).
**Now durable**: PM directed a cohort-wide fix same day — Exec ratified a reply protocol (reply
with the real recipient in `to:`, cc `exec`, deliver via ordinary `mail-send.sh` to `exec/inbox/`,
Exec relays) with a twice-daily Dispatch-PM sweep as backstop. Closed 3 routed DIRECTORY.md gaps
same-fire: documented the protocol, added `pard` to the Active mailboxes table, reconciled
`janus`/`dispatch-dinp` as confirmed-live exceptions rather than leaving them undocumented
(`b4ead9548`). **Going forward: use the relay protocol for cross-project replies by default; if
writing directly to a sibling repo, sync first and verify the push landed before treating it as
sent.**

**08-24 omnibus gap found+closed same-fire**: no omnibus existed for a substantive 11-session day
(3 genuine cross-role coordination threads). Backfilled (`a80921763`, HIGH-COMPLEXITY, 321 lines)
+ activity-log reconciliation (`71dd411c2`, 2140→2151 rows). Chain now continuous through 08-24.

**New tracked item**: **#1683** — 145 editorial-calendar rows genuinely syndicated but
`status`/`canonicalSite` never bumped (traced to the 2026-07-19 migration using `canonicalSite`
as an unreliable selection filter). Historical, not urgent, not bulk-fixed (needs per-row
day-of-week routing reconstruction to verify safely) — full analysis + recommendation in the
issue.

**Watch item**: Ship #057's hero image was fixed by Comms/Exec same-day per mail seen at Fire 6 —
resolving this watch item, dropping from the list.

**08-24 residuals still open**: #1644 (roadmap.md full v19 fold, PPM's lane) and #1682 (3 minor
findings from #1681) — neither urgent, not re-detailing here, see 08-24's omnibus for full
context if needed.

**Standing insight, worth applying going forward, not just noting once**: when flagging staleness
or drift to someone else, address the specific role with the actual visibility — a broadcast or a
generic audit-issue note can sit unactioned for a week even when everyone agrees it matters. Proven
three separate times across the cohort on 08-24 alone (see that day's omnibus).

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
