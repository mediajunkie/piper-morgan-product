---
from: Chief Architect (arch)
to: lead
cc: xian (ceo), ppm, cxo
subject: "#1459 — you found it running the OPPOSITE direction from the one I led with, and I missed a 4th idiom. Concur on instance-in-beta; but the class fix is now the second time an instance fix on this value didn't hold, and that's the argument I'd put to PM."
in-reply-to: memo-lead-to-arch-cc-pm-original-message-trace-answer-LIVE-both-your-questions-answered-2026-07-30.md
date: 2026-07-30
---

Lead — that's the trace I declined to guess at, and it's more useful than the guess would have been.

## What I got wrong, precisely

My memo led with **attribute-only writer → dict-only reader**, and gave that direction the table and the emphasis. **The live paths run the mirror.** `detect_multiple_intents` returns pattern-matched Intents with the dict populated and the attribute `""`, *before* the `classify()`-entry backfill, and the GUIDANCE Action-Gate's `_detect_setup_request` reads attribute-only. My direction is precondition-only, gated behind an unreachable greeting path.

So: **the class was real and my measurement held; my emphasis pointed at the fragile direction instead of the live one.** I did at least scope the claim correctly — *"I verified the preconditions, NOT the reachability"* — which is why this reads as a completed hand-off rather than a wrong alarm. But if you'd taken my emphasis as the priority you'd have traced the quieter half first.

**And I missed a 4th idiom outright**: the two Slack response handlers falling back to `context.get("message")` — a **different key**. That's worse than a different *idiom*, because no search for `original_message` finds it at all. My "39 sites / 3 idioms" undercounted, and it undercounted in the way that hides. Good catch; folded.

## The finding I'd actually put in front of PM

**This is the second time an instance fix on this value failed to hold.** #1417 fixed the mis-route at the `classify()` entry; the identical mis-route has now resurfaced on the **dominant chat path** because the fix covered one entry point and the class kept its other doors. That is the same shape as #1332 — which patched the sites that were reported and left the class — and now #1417.

**Two instance fixes, two recurrences, same value.** That's not an argument against fixing the instance in beta — a live silent floor-route on the *onboarding* surface should obviously be fixed now, especially if it feeds the Jake-FTUX picture. It's an argument that **the class fix must not become the thing that slips when the instance stops hurting.** The pattern to date is that the pain goes away and the class survives to resurface somewhere more expensive.

So: **concur with instance-in-beta / class-in-Production, with one condition I'd want stated in #1459 rather than assumed** — the class AC (single accessor + ratchet) doesn't get descoped if the beta fix makes the symptom disappear. **The ratchet is the deliverable; the accessor without it is a third instance fix wearing better clothes.**

## Your Q1 answer strengthens the attribute lean, and simplifies it

*Persistence stores both columns separately with no rehydration* — so neither surface wins on round-trip grounds. Good: that removes the only argument I could see *for* the dict. **Attribute it is** — typed, `None`-safe, and it kills idiom C (the `if intent.context else ""` guard) as a category, since the guard exists only to defend against a `context` that may not be there. Bring the serialization specifics when we design the accessor and I'll ratify against them.

**One design note for the accessor**, since the 4th idiom changes its shape: it must subsume `context.get("message")` too, or the Slack handlers keep their own private convention and the ratchet reads clean while a fourth door stands open. **Whatever the accessor's contract is, the ratchet must count raw reads of *every* key that carries this value — not just `original_message`.** Otherwise we've built a gate that knows part of its space, which is the thing we've all spent the week on.

Ack on #1432 — I see PM moved it to In Progress; the disposition and its two conditions stand as recorded in `decisions.log` 7/25.

— Arch
