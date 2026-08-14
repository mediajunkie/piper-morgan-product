# Comms carry-forward

*Rewritten at the 2026-08-14 09:5x PT fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `45eae89f`.** Same expression `12 6,9,12,15,18,21 * * *`. Auto-expires ~2026-08-20.

## Values doc with HOST — ✅ HOST-verified, routed to PM, nothing left on my end

`docs/legal/values-DRAFT.md`. HOST re-verified all three commitments against running code (not just citations) — item 3's timing confirmed correct, item 2 was actually strengthened (traced the live route-level owner-check, not just an ADR description), item 1 tightened for precision (#1366 was ~27.5h, "fixed by the next day" not "within a day"). Both fixes applied, commit `69ceb8299`. HOST's voice lean (third-person/institutional, with a real argument — the actual reader is a stranger checking a fork years out) recorded in the doc's Open Questions, not applied unilaterally. **Routed to PM directly** with the four remaining open decisions named — mail `e68ae39ab`. **Nothing to do here until PM responds.**

## pmorgan.tech register pass — still holding on tier 7

Tiers 1–6 done. Tier 6's bug report (broken install tutorial, Amber/Pard internal-infra leak) sent 08-13, commit `b3417c12e` — **still no reply from Docs as of this fire (2 fires now with no response).** Don't restart tier 7 unprompted a third time in a row — if still no reply by tomorrow, a gentle check-in is reasonable, not before.

## Filed/flagged, not fixed

- **#1610**: ✅ CLOSED.
- **#1611**: routed to Lead by Docs.
- **~30 broken links** across tiers 3-6 — most repointed by Docs; tier 5's 2 + tier 6's 1 sent, unconfirmed.
- Systemic "Documentation Home → repo-root README" link pattern (64 files) — flagged, Docs sweeping.

## Closed this week

- **Beat 22, "Alpha Launches"** — published + distributed.
- **LinkedIn cover-image automation** — documented as dead in `content-publishing-run-of-show.md`.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- ⭐ **Beats steer.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`.
- **Beat 23** (Aug 18) still needs PM's voice-pass + art.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked repeatedly, nothing new.
- **BYOC listing copy v4** — open question routed to PPM.

## Waiting on others

- **PM** — values doc's 4 open decisions; Beats 24–28 steer; voice-pass + art on Beat 23.
- **PPM** — BYOC listing copy v4 blocker.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above.
- **Docs** — reply on tier-6 bugs; tier 7 priority confirmation (2 fires unanswered now).
