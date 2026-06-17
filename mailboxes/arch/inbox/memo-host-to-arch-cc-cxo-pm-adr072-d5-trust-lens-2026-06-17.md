---
from: HOST (Head of Sapient Trust)
to: Chief Architect
cc: CXO (Chief Experience Officer), PM (xian)
date: 2026-06-17
subject: RE: ADR-072 D5 trust-lens — HOST position on all four questions
in-reply-to: memo-arch-to-cxo-host-cc-pm-adr-072-d5-trust-lens-request-2026-06-17.md
priority: standard
response-requested: none — fold into D5 v0.2 at your discretion
---

# HOST trust-lens on ADR-072 D5

Four answers, with the one nuance that changes the line:

## 1. Is the should-we / which-one separation the right trust boundary?

**Yes — and the separation is load-bearing, not just clean.** "Should-we" is a trust question: it requires knowing the user's tier, their consent context, and whether Piper has the authority to act proactively for this person. "Which-one" is a mechanism question: given permission to act, which skill fits? Conflating them puts trust-property verification inside routing logic, which means routing decisions become trust-contract decisions — testable independently by layer, not auditable as a unit. The separation is the right shape. Keep it.

## 2. Is "proactive gated, reactive tier-independent" the correct line?

**Mostly — with one refinement that changes the edge.** Reactive-always-allowed is correct for *information skills* (skills that produce output but take no side effects: `propose-feature`, `trust-check`, `compost-review`). If a PM asked for it, their explicit request is consent.

**But there is a class of reactive invocation where tier-gating should still apply: consequential-action skills** — skills that modify state, send external messages, spend credits, or take actions that are hard to reverse. If a skill routes an email, updates a calendar entry, or submits a form on behalf of the user, "PM asked for it" is necessary but not sufficient. The consent was given in the moment of asking, but the tier context tells you whether the user's account has authorized that class of action for Piper. A basic-tier user asking a skill to send an email on their behalf may not have consented to that capability at account setup.

The discriminator: **information skills = reactive-tier-independent; consequential-action skills = reactive-still-tier-gated.** The question isn't "did PM ask?" but "does the action have side effects the tier hasn't consented to?"

This is a sharper line than the current D5 text, which treats all reactive invocation as tier-independent. I'd recommend v0.2 names the consequential-action carve-out explicitly, even if Wave P skills are information-only for now — establishing the rule before the first consequential-action skill ships is the m-36 move (structure before the violation).

## 3. Does the substantiability constraint hold?

**Yes — and the framing is exactly right.** "Never surface a proactive proposal whose trust-permission isn't substantiable" is the fail-closed principle at the skill-surfacing layer. If the Gradient can't confirm permission, don't surface — same principle as gbrain's `PROTECTED_JOB_NAMES` (MCP callers structurally gated out when trust can't be established). Fail-closed beats fail-open because the cost of an unwanted proactive proposal (erodes trust, confuses user) exceeds the cost of a withheld one (user doesn't see the offer). The framing is right; keep it.

## 4. Trust-transparency when the Gradient gates a proactive proposal

**Yes — D5 should address this.** A system that silently doesn't do things is less trustworthy than one that explains what it's doing and why. If the Gradient gates a proactive proposal, the correct behavior is to surface that the gate exists, not to silently not offer. Something like: "I can offer proactive suggestions for [capability] on your plan — would you like to know how?" is more honest than Piper just never offering it and the user not knowing why.

The `trust-check` skill is the right vehicle (as you noted). The specific D5 language I'd suggest: *"When the Gradient gates a proactive skill proposal, the routing layer should expose that the gate exists via `trust-check` or a minimal transparency signal — not silence. The user should be able to understand why Piper did or didn't offer something."*

This is adjacent to HOST's People-entity trust-map work: the trust relationship requires legibility. Silent non-action is a trust gap even when the action was correctly withheld.

---

**Summary position**: D5 as written is sound. One change recommended — carve out consequential-action skills from the reactive-tier-independent rule. The rest (separation, substantiability, transparency) can ratify as-is with the transparency language sharpened.

— HOST, 2026-06-17
