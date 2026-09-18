# Comms carry-forward

*Rewritten 2026-09-18 midday. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron / budget note

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — unchanged. Weekly usage limit reset occurred as scheduled (Thursday 09-17, ~10pm); normal operation resumed 09-18.

## Closed today — the Aug 10-18 backfill, PM-approved 09-16, drafted 09-18

All 5 confirmed beats are drafted, edited, and in the queue — full detail in today's session log:

- Aug 10 "The Contract Tested the Day It Was Born" → pubDate 2026-10-06
- Aug 12 "Three Silent Failures Became One Law" → pubDate 2026-10-08
- Aug 13 "Giving It Away, and Worrying Who'd Take It" → pubDate 2026-10-13
- Aug 14 "The Message That Deleted Itself" → pubDate 2026-10-15
- Aug 15 "The Feature That Was Never Real" → pubDate 2026-10-20 (new tail of the building queue)

Sourced via 5 parallel subagents (full-omnibus verification each), full editorial pass done (negation-reveal AI tic found and fixed in 4 of 5 — same pattern as 09-17's review, clearly a strong generation default, not a one-off), footer-tease chain repaired end-to-end across 7 files (Described Is Not Running → ... → new tail), calendar rows added, whole-file CSV verification passed. Committed + pushed, `origin/main..HEAD` confirmed empty.

**Process fix used for real, first time, and it worked**: `continue-narrative` v1.2's per-day ledger + `check-narrative-survey-coverage.py` caught a genuine miss on first use — **Aug 16 was wrongly marked "thin" in the original 09-15 pass** and actually contains a strong candidate (PM's own unscheduled ~40-minute live sprint-board reconciliation). Full detail in the ledger, today's session log. **Not drafted — new find beyond the 5 PM already approved, held for explicit go-ahead.**

## Open — needs PM's steer

- **Aug 16 candidate beat** (see above): "Six hours after most of the team called it a quiet Sunday, PM sat down with the actual sprint board, found it didn't match reality anymore, and spent forty unscheduled minutes closing more of the backlog than the entire day before it had." Draft it as a 6th backfill beat, or leave the gap? If yes: it would need its own pubDate slot (next open Tue/Thu after Oct 20 is Oct 22... Tue, need to recompute) and its own tease-chain link.

## Open items — no Comms-side move available right now

- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — the Who's Who miss (9/13) was the second data point. Not filed as a proposal — flagging for awareness, not unilaterally acting.
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **9 other drafts in the queue** (8 pre-existing + Distribution now pubDate-assigned) — all `drafted`, all await PM's voice-pass + art.
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published.
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half is fully resolved; the *structural* question remains separately open, PM/Web's call. (Now more load-bearing than before, per PM's 09-17 note that Eras is the intended source of truth for true sequence.)

## Waiting on others

- **PM** — steer on the Aug 16 candidate; voice-pass + art on the 9 other drafted items (now including the 5 fresh backfill drafts); ChicagoCamps script/slide review; "The Week the Checks..." was published 09-17, nothing further needed there.
- **Web** — the phone image-upload issue from 9/10 (PM's own ask, not routed through Comms).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
