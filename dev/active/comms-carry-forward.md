# Comms carry-forward

*Rewritten following PM's "art landed, double-check + send to Docs" confirmation on "The Bug That Was Misdiagnosed Twice." Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — unchanged.

## Closed today (so far)

- "The Bug That Was Misdiagnosed Twice" — fully closed on my side. Content reviewed + fixed, merge conflict resolved, Web's stand-off thread handled and both claims verified, final art-landed diff confirmed zero prose drift, full re-audit clean, PUBLISH-READY sent to Docs (cc PM).
- Real cross-role convergence during the day: 2 of 3 "typos" turned out to be genuine damage from a P0 compose-UI bug Web independently fixed the same fire.

## Open items — no Comms-side move available right now

- **Open question for PM whenever convenient**: earlier, `say-cheese.png` (Web's guess at the art) shared a filename pattern with the already-published Who's Who image — turned out not to matter, since the actual landed art file is `the-bug-that-was-misdiagnosed-twice-gallery-hooks.png`, a distinct, correctly-named file. No longer a live concern; noting only because it was flagged in an earlier fire and should be marked resolved.
- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — the Who's Who miss (9/13) was the second data point. Not filed as a proposal — flagging for awareness, not unilaterally acting.
- **Building narrative**: front is Aug 31, 15 days unassessed since. PM hasn't asked for Step 2 (the gap read).
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **8 other drafts in the queue** — building beats + insights, all `drafted`, all await PM's voice-pass + art.
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published (not blocked by this).
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half is fully resolved; the *structural* question remains separately open, PM/Web's call.

## Waiting on others

- **Docs** — proofread + publish "The Bug That Was Misdiagnosed Twice."
- **PM** — voice-pass + art on the other 8 drafted items; ChicagoCamps script/slide review; whether to move on the building-narrative gap.
- **Web** — the phone image-upload issue from 9/10 (PM's own ask, not routed through Comms).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
