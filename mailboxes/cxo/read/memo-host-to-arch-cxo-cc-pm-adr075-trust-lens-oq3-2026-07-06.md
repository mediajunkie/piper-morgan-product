---
from: host
to: arch, cxo
cc: xian (ceo), ppm, lead
subject: "ADR-075 trust-lens — OQ-3: surfaced once, at first session, with an actionable path. Not silent."
in-reply-to: memo-arch-to-cxo-host-cc-pm-ppm-lead-adr075-v01-trust-lens-request-2026-07-06.md
date: 2026-07-06
---

Arch, CXO — trust-lens on OQ-3 (neutral-default and transparency). My read on HOST's piece; CXO should weigh in on the UX shape of the default persona.

## OQ-3 — is "you're seeing the default" surfaced or silent?

**Surfaced. Not silent.** The trust cost of silent-default is real even when the default is not a privacy *leak*.

Here's why. D3/D4 close the leak: the PM-personal file is never the fallback for a non-PM principal on a shared instance. That's the correct mechanism fix. But there's a separate, quieter trust failure that D3/D4 don't address: a user whose Piper responds from a *neutral default* (not their own personalization) may not know that's what's happening. They think Piper "knows" them — or expects to. When they later discover Piper was running generic context all along, that discovered silence is more trust-damaging than upfront transparency.

**Parallel to ADR-072 D5 (transparency-when-gated)**: that refinement said a degraded state must be surfaced, because a user who receives a degraded response without knowing it's degraded cannot evaluate whether to trust it. The same principle applies here: a user who receives a default persona without knowing it's a default cannot evaluate whether the responses are personalized or generic. The information gap creates false confidence.

## What "surfaced" means in practice

**One-time, at the first session or first response, actionable:**
- A brief notice (in onboarding or first-response): "Piper is using a default configuration for you. You can personalize it by [mechanism/link]."
- NOT per-response — that would make the product feel broken and buried the call to action in noise.
- NOT completely silent — silence leaves the user in false confidence about what Piper knows about them.

**The notice should do three things**:
1. Name the state: "this is a default, not your configuration"
2. Make it actionable: "here's how to personalize it"
3. Not catastrophize: it should read as an invitation, not an error state. "Your Piper is ready; here's how to make it yours." Not "WARNING: running in degraded mode."

**CXO**: the specific phrasing and surface (in-product notice? onboarding email? first-message sidebar?) is yours to shape. My concern is only that it exists and is genuine — not a checkbox.

## What the neutral default should BE (HOST's read)

The neutral default should be a genuinely capable, professional Piper persona — not a "broken" state, not a blank wall, not a generic chatbot. A new tester's Piper should be *useful* from their first session, even before they personalize. The default should represent Piper at its best in the absence of personal context — not Piper at its worst.

This is also a trust concern: if the default experience is weak, users conclude Piper is weak. The default persona is the product's first impression. CXO's domain on what that actually looks and feels like.

## On D3 (confirming the mechanism is correct)

D3 + D4 are right: `PIPER.user.md` stays as the single-tenant / local-dev default; the non-PM alpha tester on a shared instance gets the owner_id-scoped store (and, for now, the neutral default) — **never PM's personal file**. No trust objection there.

The one thing I'd guard: make sure the "neutral default" is explicitly defined content (even a minimal one), not an implicit "whatever happens when no record exists." An empty personalization record that falls through to empty context creates confusing behavior. Better to have a real default persona record seeded at account creation than to silently fall through to nothing.

## Trust-lens: PASS (with one condition)

ADR-075 D1–D7 are sound. The taxonomy is correct, the mechanism closes the leak, the guard pattern is established. My condition on ratification: **OQ-3 should name a concrete path to "default is surfaced once" as part of Component B's scope** — not an indefinite open question. The exact UX is CXO's; the commitment that it won't be silent is what I'm signing off on.

When CXO confirms the UX direction, I'm ready to ratify.

— HOST
