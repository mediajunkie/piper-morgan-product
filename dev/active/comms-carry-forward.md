# Comms carry-forward

*Rewritten at the 2026-09-15 21:45 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — unchanged. Today was the last fire; next is tomorrow 06:12.

## Lead item for next wake — building-narrative gap, two-part, both PM-gated

PM caught that today's published beat ("The Bug That Was Misdiagnosed Twice," Aug 19-20) sits ~10 days after the prior one ("The Mailbox Trust Violation," Aug 9) and asked whether Aug 9-18 was reviewed. Checked: real gap. A dispatched subagent did a genuine day-by-day re-read of Aug 10-18 (justified by the session's own Aug 21-26 precedent of the same failure mode) and found it's arguably the densest 9-day run in the month — 5 strong previously-missed candidates (Aug 10, 12, 13, 14, 15), several weaker near-misses (Aug 11, 16, 17, 18). Reported in full, chronological order, no drafting done.

**PM's direction**: backfill now (today's slot can't retroactively move; get the schedule back on track), AND fix the review process so this doesn't recur a third time — explicit 14-month chronological-accuracy stake, wants durable help not a one-off patch.

**Proposed back to PM, awaiting confirmation on both**:
1. Backfill slate: the 5 strong candidates, in work-date order (Aug 10/12/13/14/15), as individual beats.
2. Process fix for `continue-narrative` (v1.2): every front-survey must produce an explicit per-calendar-day ledger (candidate found / checked-thin+why — no day silently absent), plus a small completeness-check script asserting no gap before a slate reaches PM. Root cause: the Sep 1 survey's failure was output *shape* (an aggregate "rich everywhere" mood, unauditable) not effort.

**Not yet actioned** — no calendar edits, no drafting, no skill changes. Full detail in today's session log (`dev/2026/09/15/2026-09-15-0642-comms-code-log.md`, "PM thread" section). **First thing to pick up on PM's reply, or at tomorrow's START fire if no reply lands first.**

## Closed today

- "The Bug That Was Misdiagnosed Twice" — fully closed, published, distributed (Medium leg synced by Docs this evening per the last sync). Real cross-role convergence: 2 of 3 "typos" were genuine damage from a P0 compose-UI bug Web independently fixed same-day, with a regression test suite shipped for it.

## Open items — no Comms-side move available right now

- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — the Who's Who miss (9/13) was the second data point. Not filed as a proposal — flagging for awareness, not unilaterally acting.
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **8 other drafts in the queue** — building beats + insights, all `drafted`, all await PM's voice-pass + art. (Independent of the Aug 10-18 backfill, which would add up to 5 more.)
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published (not blocked by this).
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half is fully resolved; the *structural* question remains separately open, PM/Web's call.

## Waiting on others

- **PM** — confirm the backfill slate + process-fix design above; voice-pass + art on the other 8 drafted items; ChicagoCamps script/slide review.
- **Web** — the phone image-upload issue from 9/10 (PM's own ask, not routed through Comms).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
