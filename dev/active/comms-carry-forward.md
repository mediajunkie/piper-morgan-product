# Comms carry-forward

*Rewritten at the 2026-08-18 21:42 PT STOP fire (content unchanged since the 12:39 WORK fire — nothing moved on any thread for the rest of the day, confirmed at each subsequent fire, not assumed). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Re-armed at this STOP via delete-then-create — see below for new job ID. Expression `12 6,9,12,15,18,21 * * *` unchanged.

## The insight-piece task — categorized, 3 new candidates drafted, ready for PM's review

**Categorization** (queried the live calendar directly): all 9 existing insight drafts already have pubDates (Aug 22 – Sep 19) — nothing sits in "planned but unscheduled" limbo. That bucket is genuinely empty, checked, not missed.

**3 new candidates drafted from newest material**, all fact-checked against primary sources, unscheduled (pool items, no pubDate — footers left as explicit placeholders pending PM's slot assignment):

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

Deliberately stopped at 3 rather than drafting the full ~10+ candidate list already identified during the beats research — a real, reviewable pool, not a rush to exhaust the backlog before getting PM's steer. More can be drafted once PM reacts to these.

**Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots, per PM's own framing of the task.

## This morning's incident — fully resolved, filed as #1647

Merge-conflict cascade caused a brief, fully-corrected regression of ~18 mailbox files off `origin/main`; fixed via `mail-send.sh` same session. Full trace: `dev/active/URGENT-mailbox-regression-2026-08-18.md` (now marked RESOLVED). Filed #1647 for a genuine hook bug found along the way.

## Also from today

- **Beat 6 ("More Than Anyone Ever Reported to Me")** drafted with PM's explicit go-ahead. **All 6 approved beats are now drafted.** One flagged item: the primary-source quote reads "beta data" not "beta date" (near-certain transcription artifact, used "date," flagged for PM's confirmation, not resolved unilaterally).
- **Beat 23** published live and cross-posted (Docs).

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **Era-taxonomy proposal** — still awaiting PM's ratification, unchanged since Aug 15.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 posts genuinely missing cross-post, gated on PM starting a Dispatch session.
- **BYOC listing copy v4** — routed to PPM, no response found.
- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass.

## New, not yet actioned

- **Weekly Ship #056 draft** ("Fundamentals First") from Exec — still no review request in mail.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; era ratification; voice-pass + art on Beats 1-6; the beta-data/date quote confirmation.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Lead** — outcome of #1611 (routed by Docs).
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed today).
