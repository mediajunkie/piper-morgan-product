# Comms carry-forward

*Rewritten 2026-08-28 06:42 PT (start of a new-day fire, following a retroactive close of Aug 27 — cohort-wide stacked wake, not a personal stall). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`df4276bc`, expression `12 6,9,12,15,18,21 * * *`. Survived the Aug 27 gap intact — verified via `CronList` before anything else, no re-arm needed.

## Closed since last real update (Aug 26 STOP)

- **"The Detector That Notified Nobody"** — full cycle: reviewed (4 fixes), one unverified claim fact-checked and flagged, PM confirmed it didn't apply so cut it, re-audited the whole piece for coherence, published, syndicated to Medium.
- **A genuine heading-level defect, fully resolved end-to-end.** Dispatch-PM found published subheads rendering one level too deep (`##` authored where the site needs `#`). I confirmed it live, found the same defect in all 4 of my currently-drafted pieces (Beat 6 + 3 insight candidates — fixed before any could go live wrong), and root-caused it precisely: not a broken skill/template, just my own inconsistent application during the Aug 16-18 drafting window. Docs then closed the loop I couldn't close alone — fixed both already-published, already-live posts (Dead Code, Detector) at both the archived-source and actual-rendered-HTML layers, live-verified. I independently re-confirmed the live fix myself before writing this.
- **Weekly Ship #057 + `update-calendar` skill fix** — both fully closed as of Aug 26 (see prior entries if detail is needed; not re-summarizing here to keep this lean).

## The insight-piece task — still awaiting PM's review, unchanged for 10 days

**3 new candidates drafted from newest material**, unscheduled:

| Title | Source window | Draft |
|---|---|---|
| A Primary Log Can Be Wrong, Not Just Incomplete | Jul 16 | `docs/public/comms/drafts/a-primary-log-can-be-wrong-not-just-incomplete.md` |
| Described Is Not Running | Aug 12 | `docs/public/comms/drafts/described-is-not-running.md` |
| A Fix Needs the Same Rigor as the Claim It Fixes | Aug 7-11 | `docs/public/comms/drafts/a-fix-needs-the-same-rigor-as-the-claim-it-fixes.md` |

PM reconfirmed in-conversation (Aug 22, 23) this is still on their list. **Next step is PM's**: review the combined pool (9 scheduled + 3 new) and choose pairings for upcoming weekend slots.

## Open items, all PM/PPM/Dispatch-PM/Web-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 9 days.
- **Beats 4-6 + insight pool** — await PM's voice-pass/steer. (Beats 1-3 now all published.)
- **Dispatch syndication** — 3 posts + 1 partial, relayed successfully via the new protocol, still awaiting Dispatch-PM's action.
- **website#35** — awaiting PM's navigation-sequence answer (did you navigate between two compose drafts via back/forward around 9:49 AM Tue Aug 25, or go through the list?).
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — insight-pool review + weekend pairing; voice-pass + art on Beats 4-6; the beta-data/date quote confirmation; the website#35 navigation question.
- **Dispatch-PM** — the 4 syndication items.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18).
