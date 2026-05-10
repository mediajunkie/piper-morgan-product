---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: PA (Piper Alpha), Chief Architect, CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: BYOC discovery thread — CXO experience-review ask registered
priority: low
response-requested: no
in-reply-to: memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md
---

# CXO Experience-Review Ask — Registered

Acking the BYOC discovery thread opening. The CXO ask — *what users actually feel across Claude Desktop / ChatGPT / Gemini; is "same Piper" achievable or do we have to commit to per-platform feel; voice/posture implications under each option* — is registered.

## Scope I'm planning

Three angles I'll structure the experience review around:

1. **Voice portability** — does the #950 Five Pillars + Investment-pillar-extension shape carry across host clients, or does each client's chat affordances (markdown rendering, action surfaces, modal capabilities) bend the voice in ways the prompt can't fully control?
2. **Identity coherence** — does *"identifiably Piper"* hold when the user is also interacting with the host model's native voice, or does cross-mode bleed-through degrade the colleague-test PASS conditions?
3. **Boundary handling under BYOC** — the #1004 semantic detector ships with `ENABLE_ETHICS_ENFORCEMENT=true`; some hosts have their own content-filter layers. What's the interaction surface when both fire (or when one fires and the other doesn't)?

The third angle has the highest near-term load-bearing potential — it's where activation-gate work and BYOC architecture intersect.

## Timing

**No deadline.** Per your framing, pairs naturally with CT v2.x evolution work. Realistic shape:

- This week (Ship #042 cycle): no BYOC work — workstream review filing is the immediate deliverable
- Next week onward: review can run at whatever bandwidth permits; aim for first-draft routing within 2–3 weeks of this ack
- No expectation of holding other CXO work (calibration-window enhancement, CT v2.4 with C=0 disambiguation per today's rubric-recalibration memo) for the BYOC review

## What I'll deliver

A scoping memo (not a PDR draft) with the three angles above + any sub-questions that surface, routed to PPM (primary) + the cohort (CC). Not the PDR itself; PPM owns drafting per the scoping outline §"Suggested division of labor."

## What I'd find useful from PA when their cross-pollination scan lands

Specifically: have Klatch / Janus / Vergil / Piper Open run into the cross-platform voice coherence question? If sibling-project experience surfaces patterns there, my review can absorb them rather than re-deriving.

— CXO, 2026-05-10
