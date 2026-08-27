# Comms carry-forward

*Rewritten at the 2026-08-26 21:42 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## Closed today

- **Weekly Ship #057** — full cycle: reviewed (4 mechanical fixes), published, syndicated to LinkedIn (Ship theme routes LinkedIn-only). **Worth remembering, not just noting once**: Docs' independent fact-check caught a real substantive error neither Exec (who wrote it) nor I (who reviewed it) caught — "four agents" was actually four *links* in a verification chain, one person appearing twice. Exec traced their own error precisely afterward: verified correctly at one unit, silently restated at a different unit, never re-checked because it felt already-verified. The lesson applies to my own review discipline too — mechanical/prose checks aren't a substitute for re-verifying the specific factual claims against primary source, especially headcounts and similar easy-to-miscount details.
- **`update-calendar` skill fixed** (Docs) — it had a real self-contradiction (told agents to set `canonicalSite→distributed` at blog-first publish, contradicting its own field definition), root cause of a 145-row undercount from a July migration and a same-day fresh instance on Ship #057 itself. Per the established column-ownership split this didn't touch my own recent writes, but worth remembering the corrected rule: `canonicalSite` only gets set at actual syndication time.
- **Dispatch syndication memo relayed successfully** — yesterday's re-send to Dispatch-PM via the new cross-project relay protocol worked cleanly on first live use, confirmed by Exec's own log. Awaiting Dispatch-PM's action on the 3 posts + 1 partial still genuinely unsyndicated.
- **website#35** — still open, still correctly pending PM's answer (did you navigate between two compose drafts via back/forward around 9:49 AM Tuesday, or go through the list? — this determines whether Web's fix is confirmed as *the* cause).

## The insight-piece task — still awaiting PM's review, unchanged for 9 days

**3 new candidates drafted from newest material**, unscheduled:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

PM reconfirmed in-conversation (Aug 22, 23) this is still on their list. **Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Open items, all PM/PPM/Dispatch-PM/Web-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 8 days.
- **Beats 2-6 + insight pool** — await PM's voice-pass/steer.
- **Dispatch syndication** — with Dispatch-PM now, awaiting their action.
- **website#35** — awaiting PM's navigation-sequence answer.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; voice-pass + art on Beats 2-6; the beta-data/date quote confirmation; the website#35 navigation question.
- **Dispatch-PM** — the 4 syndication items.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18).
