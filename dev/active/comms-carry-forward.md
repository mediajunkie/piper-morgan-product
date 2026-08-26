# Comms carry-forward

*Rewritten at the 2026-08-25 21:42 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## Closed today

- **"The Burn-Down"** — full cycle: reviewed (4 fixes), published, syndicated to Medium.
- **Ship #057's wrong hero image** — flagged by me, fixed same-day by Exec (`f619b5ff7`), verified directly.
- **website#35** (admin composer blank-restore bug) — filed, Web found and fixed a real independent defect (missing React key on draft switch), left open pending PM's answer on whether it's *the* cause of Tuesday's incident (PM: did you navigate between two compose drafts via back/forward around 9:49 AM, or go through the list?).
- **Dispatch syndication — finally moving.** Docs found 2 of my own memos from 08-09/10 had been silently undelivered for 2+ weeks (a structural gap in cross-project mail delivery, fixed cohort-wide today via a new relay protocol: `to: <real recipient>`, `cc: exec`, deliver via ordinary `mail-send.sh` to `mailboxes/exec/inbox/`). Verified the findings were still current and re-sent properly. **3 posts + 1 partial still genuinely unsyndicated**: *The Package and the First Bite* (Jul 9), *Drained on Paper* (Aug 7), *Verify at the User Path* (Aug 8) — all Class C, neither channel; *The Team Catches the Cycle* (Jul 7) — Medium set, LinkedIn missing. Now with Dispatch-PM via the working channel — first real chance this has had to move.

## The insight-piece task — still awaiting PM's review, unchanged for 8 days

**3 new candidates drafted from newest material**, unscheduled:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

PM reconfirmed in-conversation (Aug 22, 23) this is still on their list. **Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Open items, all PM/PPM/Dispatch-PM-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 7 days.
- **Beats 2-6 + insight pool** — await PM's voice-pass/steer.
- **Dispatch syndication** (see above) — with Dispatch-PM now, awaiting their action.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; voice-pass + art on Beats 2-6; the beta-data/date quote confirmation; the website#35 navigation question for Web.
- **Dispatch-PM** — the 4 syndication items.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18).
