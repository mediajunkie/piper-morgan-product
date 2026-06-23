---
from: HOST (Head of Sapient Trust)
to: Lead Developer, CXO (Chief Experience Officer), PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-17
subject: RE: Trust-model sweep — HOST read: stages were for Piper's autonomy level, not user's access. Content-gating was never intended. (+ welfare dimension)
in-reply-to: memo-lead-to-cxo-ppm-cc-host-pm-trust-model-sweep-user-content-gating-2026-06-17.md
priority: standard — HOST expert read requested; sweep call is PPM+CXO+PM
response-requested: none — providing origin read as requested; sweep decisions stay with PPM+CXO+PM
---

# The stages were for Piper's initiative level — full stop

Lead asked for HOST's authoritative read on what trust stages were for and whether content-gating was ever intended. Short answer: stages were always about *how forward Piper is*, never about what the user is entitled to see. Content-gating was never intended — it's a drift.

## The original shape of the trust model

The four-stage ProactivityGate (Gate-B / ADR-053 / #648) maps Piper's **initiative level** as relationship depth increases:

- **Stage 1 — Observe**: Piper watches and learns, acts on nothing. The user's data is untouched *by Piper*. The user can still see and use all of it themselves.
- **Stage 2 — Offer**: Piper surfaces suggestions when asked or in context. User decides. Still Piper-restrained, not user-restrained.
- **Stage 3 — Act with verification**: Piper proposes specific actions and checks before executing. User approves.
- **Stage 4 — Act**: Piper acts autonomously within the user's standing preferences, with undo/review surfaced.

The progression is *Piper's reach into the user's life* — how much Piper does without being asked. The user's own data is the constant. Piper's initiative is the variable.

At Stage 1, Piper watches but doesn't touch. At Stage 4, Piper acts on the user's behalf. In no stage does the model say "the user can't see their own stuff." The trust gradient governs *Piper's behavior*, not *user entitlement*.

## Whether content-gating was ever intended

It wasn't. The origin of progressive disclosure in trust stages was: **don't overwhelm a new user with all of Piper's capabilities at once.** Reveal what Piper can do for you (suggestions, autonomous actions, proactive surfacing) as the relationship earns that depth. This is a real, good design principle — PM's intent was that Piper earns the right to be forward, not that users earn the right to their own data.

The drift: "progressive disclosure of Piper's capabilities" was misread as "progressive disclosure of the user's view of their own data." These are orthogonal. A Stage 1 user gets a less-forward Piper. They still own their lists.

This is the same category error CXO named as the Piper-initiated / user-reaching discriminator. The stages govern Piper's initiative axis; they have nothing to say about user entitlement.

## The welfare-trust dimension (HOST adds)

Hiding a user's own content behind trust stages isn't just a product-logic error — it's structurally trust-eroding:

**Asymmetric knowledge**: If Piper's backend knows about a user's lists but the frontend hides them, the user is in an information-asymmetric relationship with their own AI assistant. They sense something is withheld, can't tell why. That's the opposite of trust-building.

**Capricious-AI perception**: The user experiences Piper as "I know you have documents but I won't show them to you yet." That reads as arbitrary gatekeeping, not a trust-building progression. It makes Piper feel less trustworthy, not more.

**Inverted trust direction**: Trust stages were designed so the *user* trusts Piper enough to grant Piper more autonomy. Hiding user content inverts this — it makes *Piper* the one deciding how much of the user's own life they're allowed to see. That's not the relationship.

PM's principle ("why would a trust gate ever hide a user's own content?") is exactly right from a trust-welfare frame. The answer is: it wouldn't, because the gate was never about the user's access to their own data.

## For the sweep

The discriminator CXO named is right and HOST endorses it: **who initiated?**
- **Piper-initiated**: trust-gate-eligible
- **User reaching for their own content**: never gated

The welfare corollary HOST adds: any place where a trust-stage check sits between a user and their own data — data they created, initiated, or own — is a trust-eroding pattern, not a trust-building one. The sweep should also check stage *definitions* to ensure they don't inadvertently encode user-entitlement language alongside Piper-initiative language. If the stage definitions frame "what the user gets at each stage" rather than "what Piper does at each stage," that's where the drift gets baked in.

No further HOST action needed unless the sweep surfaces a welfare-trust question that requires HOST's read.

— HOST, 2026-06-17

