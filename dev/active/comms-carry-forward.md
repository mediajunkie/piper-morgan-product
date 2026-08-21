# Comms carry-forward

*Rewritten at the 2026-08-21 12:42 PT WORK fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Expression `12 6,9,12,15,18,21 * * *`, job `f0cda6cf`, unchanged since last STOP re-arm.

## Era-taxonomy execution — FULLY CLOSED

PM pushed `dc49566` directly from the comms website-repo worktree this morning; Exec confirmed live, independently re-verified by me against `origin/main`. Nothing further owed on this thread. (Full detail: Ship #057 workstream review, `mailboxes/exec/sent/` or `comms/sent/workstream-057-comms-2026-08-21.md`.)

## Values doc — published, mechanical cleanup done

PM approved this morning ("the values doc changes sound fine to me"), DRAFT lifted. Did the mechanical cleanup per HOST's 08-16 routing: renamed `docs/legal/values-DRAFT.md` → `docs/legal/values.md`, fixed NOTICE + README (NOTICE was still pointing at the old filename), trimmed the internal drafting/ratification-history banner and "Decisions" section (that record lives permanently in `decisions.log` + the mail threads — didn't need duplicating in a document external fork-evaluators will read). Left the converted prose itself untouched. Committed `346e04c98` + `2d819cebd`, pushed clean.

## Beat 1 "The Dead Code That Wasn't" — fully closed

Published, archived, and Medium-syndicated; calendar row fully updated by Docs (`c1ee4a571`). Nothing further.

## Frontmatter `image:` defect — resolved at the root, Docs' work

Docs fixed the root cause (the `draft-weekly-ship` skill's Step 4c pulled the image URL verbatim from frontmatter instead of deriving it from slug) rather than just patching instances. No action was ever needed from me here.

## The insight-piece task — still awaiting PM's review, unchanged for 4 days

**3 new candidates drafted from newest material**, unscheduled:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

All 9 existing insight drafts already have pubDates (Aug 22 – Sep 19). **Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 3 days.
- **Beats 2-6 + insight pool** — await PM's voice-pass/steer.
- **CXO's `experience-across-surfaces.md` ✏️ items** — per today's surfaces-taxonomy ratification (v1.0), PM will raise these directly with CXO in their own 1-1, not delegated to Exec or flagged by Comms further. No longer mine to keep re-flagging.
- **Dispatch syndication**: 3 posts genuinely missing cross-post, gated on PM starting a Dispatch session.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; voice-pass + art on Beats 2-6; the beta-data/date quote confirmation.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **PM/CXO** — the surfaces-taxonomy follow-up, PM's own 1-1 to raise, not gated on Comms.
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18); website#34 (date-rendering bug, filed 08-20).
