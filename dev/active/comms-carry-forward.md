# Comms carry-forward

*Rewritten at the 2026-08-16 06:46 START fire, after fully draining the approved beats sequence. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Armed, job `2a4258d8`, `12 6,9,12,15,18,21 * * *`. Expires ~2026-08-22.

## The big one — 5 of 6 beats drafted, ready for PM's voice-pass whenever

The whole approved sequence is now drafted except Beat 6, which stays gated on purpose:

| # | Title | Slot | Draft |
|---|---|---|---|
| 1 | The Dead Code That Wasn't | Aug 20 | `docs/public/comms/drafts/the-dead-code-that-wasnt.md` |
| 2 | The Burn-Down | Aug 25 | `docs/public/comms/drafts/the-burn-down.md` |
| 3 | The Detector That Notified Nobody | Aug 27 | `docs/public/comms/drafts/the-detector-that-notified-nobody.md` |
| 4 | A Sender-Impersonation Bug, Four Days Before Beta | Sep 1 | `docs/public/comms/drafts/a-sender-impersonation-bug-four-days-before-beta.md` |
| 5 | Repetition Isn't Convergence | Sep 3 | `docs/public/comms/drafts/repetition-isnt-convergence.md` |
| 6 | More Than Anyone Ever Reported to Me | Sep 8 | **not drafted — PM's own go/no-go call, PM is the protagonist** |

Every beat was fact-checked directly against primary logs (not reused from the 5-Aug/15-Aug planning-doc passes without re-verification), calendar rows added same-commit as each draft, pubDates set to match the approved slots, mechanical checks clean. Three real errors caught and fixed while drafting, not after: a mischaracterization of PA's actual role (verified against ROSTER.md), a voice-consistency slip (wrote Comms' own actions in first person, which in this register means PM), and two footer teases that were only accurate once a later beat's own row existed — checked against the live calendar each time, not assumed.

**Nothing left for me to do on Beats 1-5 until PM's voice-pass.** Beat 6 needs PM's explicit steer before it gets drafted at all.

## Also from last night, still open

1. **Era-taxonomy proposal** — two new eras proposed, `docs/internal/planning/comms/era-taxonomy-proposal-2026-08-15.html`. Needs PM's ratification.
2. **#1636 filed** (site's cluster data broken for 361/370 posts) — exists, awaiting an owner.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **HOST's second-pass reply on the values-doc voice conversion** — sent last night, response not yet in hand.
- **Beat 23** ("The Architect's Own Trap") needs PM's voice-pass + art (footer fixed this morning, draft itself unchanged).
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Unchanged since Jul 30.
- **BYOC listing copy v4** — routed to PPM, no response found.
- **Values doc README link** (decision 1) — flagged in the doc itself, not obviously Comms' lane.

## Small, low-urgency, Exec-coordinated

- **Ship `**Metrics**` line: bold text or real markdown heading?** Team call (Docs/Comms/Exec), no PM preference, no urgency. Waiting for Exec's promised follow-up rather than jumping in unprompted.

## New, not yet actioned

- **Weekly Ship #056 draft** ("Fundamentals First") from Exec — no review request in mail yet, unlike #055. Watch for one.

## Waiting on others

- **PM** — beats/era discussion; Beat 6 go/no-go; era-taxonomy ratification; voice-pass + art on Beats 1-5 and Beat 23.
- **HOST** — values-doc second-pass reply (imminent); Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts.
- **Exec** — Metrics-heading team-call follow-up.
- **Lead** — outcome of #1611 (routed by Docs).
- **Someone (unclear who)** — values-doc README link; #1636 (cluster-data pipeline fix).
