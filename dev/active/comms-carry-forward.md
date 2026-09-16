# Comms carry-forward

*Rewritten 2026-09-16 mid-morning. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron / budget note

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — unchanged. **Weekly usage limit hit; PM added credit for essential work only through Thursday evening reset (2026-09-16/17).** Bias toward essential, scoped work — hold discretionary/exploratory work for after reset.

## Lead item — building-narrative backfill: BOTH HALVES APPROVED 2026-09-16, drafting deferred to Friday

PM approved both the backfill slate and the process-fix design (see 2026-09-15 session log for the full research trail). Status:

1. **Process fix — DONE.** `continue-narrative` bumped to v1.2: Step 2 now requires an explicit per-calendar-day ledger (`candidate`/`thin`, machine-parseable HTML-comment block in the session log) before any slate reaches PM, enforced by a new `scripts/check-narrative-survey-coverage.py` (smoke-tested: clean range, gap, and no-ledger cases all behave correctly). Committed + pushed 2026-09-16 (`d813d3f5e`).
2. **Backfill slate — approved, drafting HELD until Friday** (PM: "put off writing new drafts until Friday"). The 5 confirmed beats, in work-date order: Aug 10 ("The Contract Tested the Day It Was Born"), Aug 12 ("Three Silent Failures Became One Law"), Aug 13 ("Giving It Away, and Worrying Who'd Take It"), Aug 14 ("The Message That Deleted Itself"), Aug 15 ("The Feature That Was Never Real"). No calendar rows added yet — per `draft-blog-post` Phase 1 the row belongs at draft-file creation, and no draft files exist yet. **Friday: draft all 5 using the v1.2 ledger discipline** (worth writing the retroactive Aug 10-18 ledger into the record then too, since the source re-read already happened 09-15 — just wasn't in the new machine-checkable format yet), add calendar rows, work out the pubDate cascade for the downstream queue.

## Closed 2026-09-15/16

- "The Bug That Was Misdiagnosed Twice" — fully closed, published, distributed.
- Weekly Ship #060 "Four Bugs, One Contract" — editorial review done 09-16 (title-case fix, typo fix, schedule-slip claim verified against calendar), PUBLISH-READY sent to Docs.

## Open items — no Comms-side move available right now

- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — the Who's Who miss (9/13) was the second data point. Not filed as a proposal — flagging for awareness, not unilaterally acting.
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **8 other drafts in the queue** — building beats + insights, all `drafted`, all await PM's voice-pass + art. (Independent of the Aug 10-18 backfill, which would add up to 5 more.)
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published (not blocked by this).
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half is fully resolved; the *structural* question remains separately open, PM/Web's call.

## Waiting on others

- **PM** — voice-pass + art on the other 8 drafted items; ChicagoCamps script/slide review; Ship #060 publish.
- **Friday (self)** — draft the 5-beat Aug 10-18 backfill slate, now unblocked.
- **Web** — the phone image-upload issue from 9/10 (PM's own ask, not routed through Comms).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
