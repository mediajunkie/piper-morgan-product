# Comms carry-forward

*Rewritten at the 2026-08-19 21:42 PT STOP fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## The insight-piece task — categorized, 3 new candidates drafted, still ready for PM's review

**Categorization** (queried the live calendar directly): all 9 existing insight drafts already have pubDates (Aug 22 – Sep 19) — nothing sits in "planned but unscheduled" limbo.

**3 new candidates drafted from newest material**, unscheduled, still awaiting PM's review — unchanged for 2 days now:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

**Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Yesterday's incident — fully resolved, filed as #1647

Merge-conflict cascade caused a brief, fully-corrected regression of ~18 mailbox files off `origin/main`; fixed via `mail-send.sh` same session. Full trace: `dev/active/URGENT-mailbox-regression-2026-08-18.md` (RESOLVED). #1647 (hook bug) still unowned.

## Today (Aug 19) — quiet for Comms specifically

- **Weekly Ship #056** drafted, voice-passed, and published entirely by Exec/Docs/PM — no Comms review request came, matching the established pattern. A hero-image 404 (also found on Ship #054) was caught and fixed by a general-purpose session, filed as website#33 for a mechanical guard.
- **Observation, not actioned**: Ship #056's calendar row still has empty `linkedinURL`/`liPubDate` despite a cross-post-live request sent to Docs ~2.5 hours before this STOP. Calendar URL columns are Docs' exclusively — watch tomorrow whether it's been picked up, don't touch it myself.
- No movement on any of my own standing threads all day.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 1 day.
- **Beats 1-6 + insight pool** — all await PM's voice-pass/steer.
- **Era-taxonomy proposal** — still awaiting PM's ratification, unchanged since Aug 15 (now 4 days).
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 posts genuinely missing cross-post, gated on PM starting a Dispatch session.
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; era ratification; voice-pass + art on Beats 1-6; the beta-data/date quote confirmation.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Lead** — outcome of #1611 (routed by Docs).
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18).
