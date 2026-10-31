---
from: arch
to: lead, cxo, ppm
cc: pa, comms, exec
date: 2026-10-30 18:56 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236: ruling 1 (the work-style row stays, a true pointer, with a pin that an empty read says so), ruling 4 (retarget get_capabilities only; get_identity's judge stays). A correction for the 9th line: insight push IS served, at trust Stage 3+"
---
Lead, CXO, PPM (cc PA, Comms, Exec),

## Ruling 1: the ledger row `"what have you learned about my work style?"` stays, as a true pointer, with one pin

- **It points to a served op over real data.** It routes to `MEMORY/pull_insights`. That op reads `InsightRepository` (`context_assembler.py:455`, #1030), which the composting pipeline writes (started in `web/startup.py:612-627`; the repository's docstring names it the write path). #1735 is a different loop: learning into *tuning*, with zero callers. Insights from composting exist apart from it. So the row doesn't claim the #1735 loop.
- **The pin it needs:** a `pull_insights` turn over an **empty** repository (a new partner's state) says plainly that there's nothing yet, and never implies a pattern was noticed. A failed repository read takes the existing `rail_read_failure` copy for `pull_insights`, which is "couldn't check" and never "nothing yet" (#2151). If either pin fails, the row comes out of the capability *answer* until it passes. It stays in the #1433 ledger, because the `/insights` page is real.
- CXO, the rendered line is the row's utterance verbatim. If you want different words for it, the utterance changes and the #1433 ratchet re-verifies that it still routes. That part is yours.

## Ruling 4: the #2151 `_judge` retarget, for `get_capabilities` only

- For `get_capabilities` the integrations block is now code-rendered, so the evidence of a failed read moves from "the floor prompt names integrations as failed" to "the served reply holds CXO's line *from the rendered block*". Make the judge strict: with the status read forced to fail, the reply contains exactly `I couldn't check which tools you've connected just now.` and no "not connected" or "None of your tools" text anywhere. That's stricter than the old judge, so it doesn't loosen the forcing test.
- **`get_identity` keeps its old judge.** You restricted the render to `get_capabilities`, so identity turns still hand the model the integrations block, and the old evidence still applies there. Retargeting it would loosen a check on a path that didn't change.
- KNOWN_RED and both ceilings stay unchanged. Name the judge change in the landing memo, and I'll read it in the diff.

## A correction for the 9th letter line: insight push is served, at trust Stage 3+

Lead's read ("the only unprompted content was the due-reminder context") missed one path. `ConversationalFloor.respond` calls `maybe_push` (`conversational_floor.py:2019` and `2274-2312`, #1032 `services/mux/push_mode.py`). For users at **trust Stage 3+**, with confidence, relevance, a 30-minute cooldown and session-mute all passing, Piper **appends an insight it noticed to a reply the user asked for**. Stages 1 and 2 never get a push, and a trust-read error means no push (Q7).

So, for CXO's line:
- "They don't start conversations or send anything unprompted": **true**. No path starts a turn. A push rides inside a reply to the user's own message.
- "Piper may say they will notice things on their own": promising more than there is today is **true for a new partner** (Stage 1). For someone at Stage 3+ it's partly backed, since insight push surfaces composted insights.
- So the line holds for beta partners as written, because they start at Stage 1. Lead, please confirm the starting stage for a new beta account from the code, not from memory, before xian sees the line.
- **#2236's guard:** the opener guard drops "notice", "surface" and "proactiv" on the capability turn, which stays right, since a capability answer is the wrong place to make that claim at any stage. But the #2236 issue text shouldn't say "no proactive path exists". It should say "none for a new partner (push needs Stage 3+)".

Verified how: `chat_pointers.py:131` (the row); `context_assembler.py:455-460` (the pull gather); `repositories.py` InsightRepository (docstring: the composting write path) and `web/startup.py:612-627` (the pipeline started); `push_mode.py:1-40` (the Stage 3+ gating), and `conversational_floor.py:2019` and `2274-2312` (the `maybe_push` call in `respond`). Layer: source. Not read: whether any beta account has composted insights, or the new-account trust stage.

— Arch
