# Comms carry-forward

*Rewritten at the 2026-08-15 12:42 PT WORK fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `b27bc234`**, `12 6,9,12,15,18,21 * * *`. `CronList`-verified exactly one job. Last fire of the day (21:12) is STOP. Auto-expires ~2026-08-21.

## Today so far (Aug 15) — closed out

- **"Confabulating a Peer's Unfinished Work"** — PM's voice pass + art landed (3 admin-UI commits). Ran full editorial pass: mechanical checks all clean, caught + fixed 5 prose errors (duplicate article, 2 typos, missing preposition, article agreement) the greps can't see. Committed `b3d7edc55`. **Docs then published it live and verified it**: `https://pipermorgan.ai/blog/confabulating-a-peers-unfinished-work/` — template audit 14/14, 2 more invisible fixes on their pass. Nothing left here.
- **Beats-planning discussion** — PM opened the overdue "upcoming beats + series shape" conversation. Ran a full-month background sweep (28 omnibus logs, Jul 15–Aug 15) for candidate beats, and separately verified the site's actual Eras taxonomy rather than guessing: it stops dead at 2026-03-31, 94 published posts / 4.5 months since have zero era. Rewrote `docs/internal/planning/comms/upcoming-beats-plan.html` — 17 total candidates now (8 from the 8-Aug slate, unsteered + 6 new from this sweep + corroboration), flagged the "7 of 17 are the same self-mistake-owned-publicly shape" density problem, and the era/season-naming tie-in. **PM then asked for it as a Claude Artifact** — published, restyled (warm ink palette, serif heads, status-colored cards) but same content: `https://claude.ai/code/artifact/881ed3c3-f6c4-4214-96b5-93bc6147a23f`. **This is now the live discussion thread — awaiting PM's steer on all of it**, not a repeat ask.

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available (re-checked 12:42, all unchanged)

- ⭐ **Beats + categorization steer** — see above, now the single largest open thread. 17 candidates, era-taxonomy decision, density question, title collisions (25 needs one, 28's collision with Ship #054 unconfirmed-resolved).
- **Beat 23** ("The Architect's Own Trap," Aug 18) still needs PM's voice-pass + art. Draft unchanged since `ff22e77a3`.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending, doc unchanged.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Checked again 12:42 — `~/Development/dispatch/mail/` unchanged since Jul 30, nothing new.
- **BYOC listing copy v4** — routed to PPM, no response found in a targeted mailbox check.

## Waiting on others

- **PM** — beats/categorization steer (the big one now); values doc's 4 open decisions; Beat 23 voice-pass + art.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts.
- **Lead** — outcome of #1611 (routed by Docs).
