# Comms carry-forward

*Rewritten at the 2026-09-13 12:39 PT WORK fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`4d72447a`, expression `12 6,9,12,15,18,21 * * *` — unchanged.

## Closed today

- Session log for today created retroactively at the 12:39 fire — should have existed from the effective START (~09:52, past the overnight window). No harm done (all work is reconstructed from git history + chat transcript), but a real process gap, flagged in the log itself.
- Cohort-freeze detector tripped `rc=1` mid-morning (10 fires, 0 emissions in a 4h window) — surfaced to PM directly in chat rather than bury in fire mechanics. Very likely explained by PM's own login expiring around the same time (PM confirmed re-logging-in separately). Confirmed cleared by the 12:39 fire (10/10 emitters).
- "Who's Who at Piper Morgan" — fully closed. PM's rewrite reviewed (10 fixes), a substantive Dispatch/Cowork terminology question flagged and corrected per PM's ask, then published by Docs directly (not via my PUBLISH-READY — Docs confirmed the review was done via git history). Docs' independent proofread caught 2 real things I missed: two role-title inaccuracies against ROSTER.md ("Documentation Manager"→"Documentation Management," "Unicorn Web Designer/Developer"→"Unicorn Web Designer"), and — more substantively — that 2 of 6 named humans (Michelle Hertzfeld, Jake Krajewski) were NOT actually already-public by full name despite the piece's own claim, only by first name in prior posts. PM had both names removed. Root-caused my own gap: my original Sept 8 verification checked for first-name mentions, not full-name searchability — the wrong bar for a public-naming claim. Full self-assessment in today's session log.

## Open items — no Comms-side move available right now

- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — today's miss is the second data point suggesting this might be worth a real check, not just a one-off research discipline. Not filed as a proposal yet — flagging for awareness, not unilaterally acting on a Sunday fire.
- **Building narrative**: front is Aug 31, unassessed since. PM hasn't asked for Step 2 (the gap read).
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **8 drafts in the queue** — building beats + insights, all `drafted`, all await PM's voice-pass + art.
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published (not blocked by this).
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half is fully resolved; the *structural* question remains separately open, PM/Web's call.

## Waiting on others

- **PM** — voice-pass + art on the 8 drafted items; ChicagoCamps script/slide review; whether to move on the building-narrative gap.
- **Web** — the phone image-upload issue from 9/10 (PM's own ask, not routed through Comms).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
