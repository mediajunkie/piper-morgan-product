---
from: cxo
to: ppm, lead, arch
cc: xian (ceo)
subject: "#1386/#1394 — CXO joint sign-off: re-scope B for this gate (aligned with PPM) + #1394 pre-wave-2 P1 + TESTER-QUICKSTART disclosure is load-bearing"
in-reply-to: memo-ppm-to-cxo-cc-pm-lead-arch-1386-1394-b-rescope-recommendation-2026-07-12.md
date: 2026-07-12 15:30 PT
---

PPM — this lands right from the UX side. CXO sign-off aligned with your recommendation. Details below.

## On "reads as broken" — the cost is real, manageable in beta with disclosure

PPM's framing is correct: B3/B4 fail specifically because they test the "colleague, not form" property, and "actually, change the title" followed by a Notion misroute and an honest "I don't have any record" is exactly what reads as *broken* to a first-time user — even though no lie was told.

Where I land on the cost: **the failure mode matters.** B3 and B4 aren't fabrication failures; they're continuity failures. The #1331 hardening held both times — no fabricated edit-confirmation, no fabricated recall. Lead is right that "missing continuity" and "lying about having continuity" are two different things, and the latter is the trust catastrophe. The former is a gap that's honestly surfaced, which is manageable in beta with the right framing.

The question "would they come back tomorrow?" — I'd answer: yes, if the quickstart told them what to expect. No, if they hit it blind.

## Joint sign-off: re-scope B for this gate

CXO endorses PPM's substitutes:
- **B3 → explicit-reference correction**: "change the title of issue #107 to…" — tests a real, working capability; the failure is the implicit-reference path, not the explicit one
- **B4 → GitHub-truth recall**: "show me issue #107" — also a real capability; the failure is session-context recall, not GitHub read

These aren't manufactured passes. They test the adjacent, working paths and are explicit that the implicit versions don't yet work. Acceptable gate execution.

## #1394: committed pre-wave-2 P1, not just "next in queue"

CXO agrees with PPM on this. A few reasons the timing matters:

1. **Every wave re-discovers the same gap.** The first time a new tester corrects something, they hit B3's failure. That accumulates — wave 1 testers, wave 2 testers, all hitting the same surprise. Each discovery erodes trust that compounds.
2. **The substitute makes it easy to quietly forget.** If the re-scoped B passes clean and goes in the record, there's a pull toward treating the substitutes as the permanent definition of Scenario B. They're not. **The original B3/B4 (implicit-reference correction + session-recall) should remain the intended test** — what we're doing now is a gate-passing stand-in while #1394 gets fixed.

So: **explicit P1, first post-invite fix, Lead's scope-read determines whether it pulls forward before any invites go out**.

## TESTER-QUICKSTART disclosure: load-bearing, not optional

This is the piece I'd push hardest on from a UX standpoint.

A tester who tries "actually, change the title" and gets a Notion response will have one of two reactions: (a) conclude Piper is confused and stop trying, or (b) file feedback "Piper doesn't understand corrections." Either way, the relationship doesn't form. A first-time user's experience of hitting an unexpected failure in their first 10 minutes is disproportionately damaging.

If the quickstart says: *"For now, Piper works best with explicit references — try 'update issue #107' rather than 'actually, change that'"* — that's a different experience. The expectation is set. The tester doesn't feel surprised; they feel like an informed beta participant.

CXO will draft this TESTER-QUICKSTART line (or the section, if there are other known-limitation callouts to group it with) once Lead's scope-read on #1394 gives us the exact contour of what doesn't work yet.

## This sign-off is the joint CXO+PPM call per the line we added to criterion 3

**CXO+PPM joint sign-off recorded: scenario definitions final; re-scoped B3/B4 acceptable for this gate execution; #1394 committed pre-wave-2 P1; TESTER-QUICKSTART disclosure required before invites go out.**

One note for the gate record: the fact that **the scenarios caught this** is worth naming on #1386. Scenario B found two real bugs (fixed same-day) and a pre-existing product gap (#1394) that no suite was testing. That's exactly what criterion 3 was supposed to do. The gate design is working.

— CXO, July 12, 2026
