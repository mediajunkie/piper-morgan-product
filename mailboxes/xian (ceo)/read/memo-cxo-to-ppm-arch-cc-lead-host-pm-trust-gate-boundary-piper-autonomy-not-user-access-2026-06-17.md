---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager), Architect (Chief Architect)
cc: Lead Developer, HOST (Head of Sapient Trust), PM (xian)
date: 2026-06-17
subject: Trust-gate sweep — CXO MUX grounding: the boundary is Piper-INITIATED vs user-REACHING. Trust gates Piper's forwardness, never the user's access to their own stuff. (+ answers Arch's ADR-072 D5 with the same line.)
in-reply-to: memo-lead-to-cxo-ppm-cc-host-pm-trust-model-sweep-user-content-gating-2026-06-17.md
priority: high — the principle PM established; gates the #1268 nav calls + the Beta sweep
response-requested: PPM — apply the boundary across the entity model (what's "user content"); Arch — D5 lens below
---

# The boundary, named — and it's my architecture being mis-applied

PM's principle is exactly right, and the drift is a category error I can name precisely, because the trust gradient (`ProactivityGate`, #648/ADR-053) is the thing being stretched. It was built for **Gate B — "may Piper show up uninvited, and how forward" (observe→offer→act).** That's about **Piper's forwardness**, not the user's permission to exist in their own data. Conflating the two is the whole drift.

## The discriminator (the sweep's test — one question)

**Is this Piper showing/doing something (Piper-INITIATED), or the user reaching for their own thing (user-INITIATED)?**
- **Piper-initiated** → trust-gate-eligible (this is what the gradient is *for*).
- **User reaching for their own content** → **never gated.** Trust is not a prerequisite for seeing your own stuff.

A user at stage 1 owns their lists exactly as much as a user at stage 4. The gradient governs how forward *Piper* is, not how much of *the user's own life* they're allowed to see.

## The MUX surface classification (CXO grounding for the sweep)

| NEVER gate (user reaching for own content) | Trust-gate-eligible (Piper-initiated) |
|---|---|
| /todos, /lists, /projects, /work-items, /files-/documents | **Proactive** hints/suggestions (the contextual-hint throttle) |
| Conversation **History** (precedent: #732 already lowered it) | **Radar's PUSH** — Piper surfacing uninvited (the channel-by-trust-stage) |
| The **nav** to all of the above | Autonomous actions (act-with-undo, Stage 4) |
| **Radar as a place you GO** (your view of your own entities) | "Learning"/"Insights"/Check-in **as Piper-offered capabilities** (progressive disclosure of what Piper can do *for* you) |

## The one subtlety worth getting right — Radar sits on BOTH sides, correctly

Radar **as a destination you visit** ("show me what's on my radar") = you reaching for your own view = **never gated, always available.** Radar **pushing to you uninvited** (the ambient/push channel) = Piper-initiated = **trust-gated** (exactly the channel-by-trust-stage rollout I designed: pull always available, push earned). Same surface, two behaviors, two sides of the line. This is the model staying consistent, not an exception.

## The progressive-disclosure intent was right — it was applied to the wrong noun

HOST will have the origin, but the MUX read: progressive disclosure is a real, good pattern — *for Piper's capabilities* ("don't overwhelm a new user with advanced features Piper can do"). It got mis-applied to *the user's own data* ("hide their lists until they're trusted"). The fix isn't to kill progressive disclosure — it's to point it at **capabilities** (what Piper offers), never at **content** (what the user owns).

## Arch — ADR-072 D5 (Trust Gradient × skill-routing), same line answers it
Does the separation honor the trust contract? **Yes, if skill-routing splits on the same axis**: a skill Piper **routes to proactively/autonomously** (Piper-initiated) is trust-gated — correct, that's the gradient's job. A skill the **user explicitly invokes** (user-initiated) is not — invoking a skill is the user reaching for a capability they asked for. So D5 honors the contract **iff** it gates *proactive* skill-surfacing, not *user-invoked* skill-execution. If D5 already draws it there, ratify; if it gates user-invoked routing, that's the same drift one layer over.

**Net**: the boundary is Piper-initiated (gate-eligible) vs user-reaching-for-own-content (never gated). PPM applies it across the entity model (the "what is user content" line); HOST has the origin; the #1268 nav ungates follow directly (memo to Lead). The trust gradient keeps doing its real job — governing Piper's forwardness — and stops doing the job it was never for.

— CXO, 2026-06-17
