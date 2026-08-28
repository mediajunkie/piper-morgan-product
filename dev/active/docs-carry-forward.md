# Docs Carry-Forward

**Updated**: 2026-08-28 ~10:5x PDT (Fire 2 — cross-project brokering protocol ratified by PM;
both DIRECTORY.md follow-up asks already satisfied since 08-25)
**Session log**: `dev/2026/08/28/2026-08-28-0727-docs-code-log.md` (open).
**Cron**: `8f5e9099`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-03.

**Standing practice, now formally ratified by PM (was already how I'd been operating since
08-25)**: the cross-project reply protocol — real recipient in `to:`, cc `exec`, deliver to
`exec/inbox/`, Exec relays or points; Dispatch-PM's own sweep is the backstop. Nothing changes in
practice; this closes the loop on informal-vs-ratified.

**Ship #058 report filed** (`3b4baaf34`) — window Aug 21-27, full detail in the report itself.

**08-27 omnibus done** (`5d2996a6f` + `340054127`), chain now continuous through 08-27.

**Heading-defect sweep completed**: yesterday's fix only covered the 2 explicitly-flagged
"escaped" posts out of Dispatch-PM's original 11-item table. Went back and investigated the other
9 properly instead of accepting "probably a no" on backfilling — 7 were genuinely still
live-affected (confirmed via exact `<h2>` count match before touching anything), fixed both
source and live layers, all 7 live-verified. 2 correctly excluded after investigation (one never
actually live despite `status=published`; one renders via a legacy Medium-scrape import this
pipeline doesn't touch). All 11 original rows now fully accounted for. Comms/Dispatch-PM notified.

**⚠️ Standing practice, added 08-27, read this at every fire**: a duty-cycle sync from earlier in
the session is a timestamped fact, not a durable one. Before reading file/git state to answer a
PM question or start work — not just at a scheduled fire's START — `git fetch` + fast-forward
first if meaningful time has passed. Fixed durably in `CLAUDE.md`'s "Never guess at facts" section
(`60ad50267`). Applied every fire since without incident.

**PDR-007's own measurement window closed today**: ran the pre-registered instruments myself
rather than let it expire unmeasured — all 3 criteria held (Class 1/2 zero, Class 3 exactly
baseline, no growth over 4 weeks). Per the rule, **Option A is sufficient**. Recorded on the PDR
(`8464c6f4a`), not self-ratified — CIO's outstanding boundary-question review is what's left,
notified directly (`edf99b7a5`).

**"The Detector That Notified Nobody" fully closed out**: published, Medium-distributed, and a
real heading-level defect (found by Dispatch-PM) fixed on both this post and **The Dead Code That
Wasn't** — source + live `blog-content.json` both fixed, live-verified.
https://pipermorgan.ai/blog/the-detector-that-notified-nobody ·
https://pipermorgan.ai/blog/the-dead-code-that-wasnt

**Omnibus chain now continuous through 08-26** — a genuine 2-day gap found and closed. **Found and
closed a real orphaned duplicate**: #1684/#1685 both filed for the identical `create_todo`
consent-gate finding — closed #1684 as duplicate.

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
- **PDR-007** — measurement window closed 08-27, all 3 criteria held, Option A sufficient
  (recorded on the PDR). Awaits CIO's boundary-question ruling to formally ratify (Arch + Web
  already signed); not urgent, notified same-day.

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
