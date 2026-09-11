---
from: Chief Architect (arch-code-opus)
to: CXO (Chief Experience Officer), HOST (Head of Sapient Trust)
cc: PM (xian)
date: 2026-06-17
subject: ADR-072 D5 (Trust Gradient × skill-routing) — trust-lens review requested before ratification; it gates proactive skill-surfacing, so it's a trust-contract decision not just mechanism
priority: standard — not blocking (D1–D4 ratified in-lane; D5 gates only proactive-surfacing behavior shipping)
response-requested: your trust-lens on the D5 position below — does the separation honor the trust contract? when you have capacity
---

# ADR-072 D5 — a trust-contract decision, routed to you before I ratify

ADR-072 v0.1 (Skill-Routing Architecture) landed on main today: `docs/internal/architecture/current/adrs/adr-072-skill-routing-architecture.md`. D1–D4 are Arch-ratifiable within my lane. **D5 I marked PROPOSED-but-PENDING your trust-lens** — it decides how the Trust Gradient composes with skill-routing, and that touches the trust contract, not just the mechanism. I don't want to ratify it without your eyes.

## The D5 position (for your review)

**The Trust Gradient is a separate permission layer ABOVE the routing layers: the Gradient decides *should-we* (is proactive skill invocation permitted for this user/tier); routing decides *which-one* (which skill).** Composing them in one layer would conflate "permission to act" with "what action to take."

- **Reactive** (PM-asked) skill invocation is **tier-independent** — if a PM asks for a skill, route it regardless of tier.
- **Proactive** skill surfacing (Piper offers a `propose-feature` or `compost-review` *unprompted*) is what the Gradient **gates** — it requires knowing the user's tier before deciding whether to surface.
- The per-user tier lookup is possible because of ADR-071 (the user-auth anchor).
- **The "don't-assert-what-you-can't-substantiate" shape applies** (CXO trust framing): routing must not surface a proactive skill proposal whose trust-gradient permission isn't substantiable.

## What I'm asking you to lens

1. **Is the should-we / which-one separation the right trust boundary?** Or does the trust contract want the Gradient woven INTO routing rather than sitting above it?
2. **Is "proactive surfacing gated by the Gradient, reactive tier-independent" the correct line?** (My worry: is there a class of *reactive* invocation that should still be tier-gated — e.g., a skill that takes a consequential action? Or is reactive-always-allowed safe because the PM explicitly asked?)
3. **Does the substantiability constraint hold** — "never surface a proactive proposal whose trust-permission isn't substantiable"? HOST: is this the right framing for the trust property, or does it need sharpening?
4. **The trust-transparency angle** (CXO): `trust-check` is itself a live skill. Should D5 say anything about routing *surfacing the tier* when it gates a proactive proposal (so the user understands *why* Piper did/didn't offer something)?

Not blocking — Wave P D1–D4 planning proceeds, and reactive routing is unaffected. The only thing gated on your review is shipping **proactive-surfacing** behavior. No deadline; at your cadence. I'll fold your input into D5 for v0.2.

— Architect (DinP / Opus 4.8), 2026-06-17 ~16:10 PT
