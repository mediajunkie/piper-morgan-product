# Comms carry-forward

*Rewritten at the 2026-08-16 06:26 START fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

Armed, job `2a4258d8`, `12 6,9,12,15,18,21 * * *`. Expires ~2026-08-22.

## The one thing to check first — PM's own conversation, not this duty cycle

⭐ **PM said "we can discuss the findings when we resume tomorrow" (i.e. today)** — this is a live-conversation thread, not something duty-cycle fires should try to push forward alone:

1. **Beats sequence — APPROVED.** PM confirmed 6 beats with two title revisions. Decision record + Artifact both updated last night. **Beat 1 is now drafted** (see below) — the remaining open piece is Beat 6's go/no-go/rewrite call, which is explicitly PM's alone (PM is the protagonist).
2. **Era-taxonomy proposal — ready for review.** Two new eras proposed ("The Mechanism" Apr–Jul, "The Alpha" Aug–present), full writeup at `docs/internal/planning/comms/era-taxonomy-proposal-2026-08-15.html`. Needs PM's ratification.
3. **#1636 filed** (site's cluster data broken for 361/370 posts, not just the April-onward gap) — exists, awaiting an owner, no PM action needed for it to exist.

## This morning (Aug 16 START) — done

- **Reconciliation fix**: "15 Sessions, Fast Recovery" (Nov 2025 piece) had a stale draftPath + wrong status despite being confirmed published by PM's own commit. Fixed, verified, reconciliation clean.
- **Beat 1 drafted end-to-end**: "The Dead Code That Wasn't" — fact-checked directly against primary Jul 16-18 logs (not reused from the planning-doc pass without re-verification), calendar row added same commit, mechanical checks clean, 757 words. **Needs PM voice-pass + art.**
- **Beat 23 footer-chain fix**: now correctly teases Ship #056 (Aug 19) instead of skipping to Trust Gate (Aug 22), since Beat 1 now sits between them on the calendar.
- Mailbox triaged (3 ccs, all Docs/Web/Exec-owned matters — Dispatch calendar-staleness diagnosis, website#31 answers, a small Ship-formatting style call Exec is coordinating that includes Comms — noted below, not urgent).

## Open items, all PM/CXO/PPM/Dispatch-gated — no Comms-side move available

- **HOST's second-pass reply on the values-doc voice conversion** — sent last night, response not yet in hand.
- **Beat 23** now needs PM's voice-pass + art (draft itself unchanged, only its footer was touched this morning).
- **Beat 1** needs PM's voice-pass + art (new today).
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still pending.
- **Dispatch syndication**: 3 fully unsyndicated posts, 1 partial. Unchanged since Jul 30 — though last night's Web/Docs thread on Dispatch's *calendar-read* staleness (a different mechanism) may be worth a mention if PM asks about Dispatch friction generally.
- **BYOC listing copy v4** — routed to PPM, no response found.
- **Values doc README link** (decision 1) — flagged in the doc itself, not obviously Comms' lane.

## Small, low-urgency, Exec-coordinated

- **Ship `**Metrics**` line: bold text or real markdown heading?** PM ruled it's a team call (Docs/Comms/Exec), no PM preference, no urgency. Exec said "I'll follow up with Comms" — waiting for that rather than jumping in unprompted, but have a quick lean ready (heading, for scan-ability/template consistency) if asked directly.

## New, not yet actioned

- **Weekly Ship #056 draft** ("Fundamentals First") from Exec — no review request in mail yet, unlike #055. Watch for one.

## Waiting on others

- **PM** — beats/era discussion; Beat 6 go/no-go; era-taxonomy ratification; Beat 1 + Beat 23 voice-pass + art.
- **HOST** — values-doc second-pass reply (imminent); Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts.
- **Exec** — Metrics-heading team-call follow-up.
- **Lead** — outcome of #1611 (routed by Docs).
- **Someone (unclear who)** — values-doc README link; #1636 (cluster-data pipeline fix).
