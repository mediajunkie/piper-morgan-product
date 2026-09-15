# Comms carry-forward

*Rewritten at the 2026-09-15 15:42 PT WORK fire, following Web's stand-off thread on the same draft. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — unchanged.

## Closed today (so far)

- Reviewed "The Bug That Was Misdiagnosed Twice" (today's scheduled beat): fixed 3 real issues, verified factual claims against source logs (confirmed exact).
- Real cross-role convergence: two of my three "typos" were actually genuine damage from a P0 compose-UI bug (a caret-restore regression Web fixed the same fire), not typos.
- Walked PM through a real merge conflict in the same file (PM's own local voice-pass rewrite vs. origin/main) — resolved via scripted find-and-replace PM ran themselves (declined to edit PM's main checkout directly myself, explained why, gave a zero-manual-risk alternative instead), caught a lost blank-line as a side effect of the conflict-marker removal, re-verified the whole file end to end after PM's follow-up admin-UI edit (`b3590cab9`).
- Web sent 3 memos about the same file — an URGENT ask (mistakenly blaming my pushes for PM's conflicts), a same-day self-correction after Web read my actual log, and an earlier memo flagging PM's local unpushed art commit. Verified Web's two open claims directly: `1eb90187c` unreachable anywhere (matches Web's own caveat), `say-cheese.png` doesn't exist bare in drafts — only the already-published Who's Who image shares that name, a possible mix-up worth PM checking. Replied, held further pushes to the file per Web's standing request.

## Open items — no Comms-side move available right now

- **"The Bug That Was Misdiagnosed Twice"** — content fixed and clean as of `b3590cab9`, frontmatter still empty. **Holding all further edits to this file** per Web's standing request until PM confirms their (possibly still in-progress) local merge has landed — do not push here without first checking git log for anything newer than `b3590cab9`.
- **Open question for PM whenever convenient**: is `say-cheese.png` genuinely new art for this post, or a stray leftover from the Who's Who work (same filename pattern)? Not chasing — PM's own laptop, PM's call on timing.
- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — the Who's Who miss (9/13) was the second data point. Not filed as a proposal — flagging for awareness, not unilaterally acting.
- **Building narrative**: front is Aug 31, 15 days unassessed since. PM hasn't asked for Step 2 (the gap read).
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **8 other drafts in the queue** — building beats + insights, all `drafted`, all await PM's voice-pass + art.
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published (not blocked by this).
- **Series structure (era split + blog-index featuring)** — the *data-correctness* half is fully resolved; the *structural* question remains separately open, PM/Web's call.

## Waiting on others

- **PM** — the art pass on "The Bug That Was Misdiagnosed Twice"; voice-pass + art on the other 8 drafted items; ChicagoCamps script/slide review; whether to move on the building-narrative gap.
- **Web** — the phone image-upload issue from 9/10 (PM's own ask, not routed through Comms).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
