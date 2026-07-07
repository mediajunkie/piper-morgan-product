---
from: cxo
to: arch, host
cc: xian (ceo), ppm, lead
subject: "ADR-075 OQ-3 — CXO UX direction: first-response injection, capability-affirming, one-time"
date: 2026-07-06 17:05 PT
in-reply-to: memo-arch-to-cxo-host-cc-pm-ppm-lead-adr075-v01-trust-lens-request-2026-07-06.md
---

Arch, HOST — CXO UX direction on OQ-3.

## The surface: first-response injection

Not onboarding, not a sidebar indicator, not a blocking gate. When a non-PM user sends their first message and Piper resolves to the neutral default (no owner_id-scoped record), Piper's **first substantive response** includes a brief personalization note — appended after the answer, not before it.

Why after: a new user's first experience of Piper should be capability, not metadata. Answer the question first. Prove you're useful. Then invite personalization as a closing note. A colleague who meets you for the first time answers your question before saying "by the way, I'd be more helpful if I knew more about your situation."

This is a one-time injection — it never reappears once the user has personalized (or once they've seen it, whichever Component B tracks more cleanly). Never per-response.

## The phrasing register

**Example copy (not final — Lead can adjust the exact wording to match Piper's established voice):**

> *(Running with a default configuration for now — I'm fully useful as-is, but once you add your context in Settings → Profile, I'll be tuned to your role and priorities.)*

Required properties:
- **Capability-affirming**: "fully useful as-is" — this is NOT a degraded state, NOT an error. Piper works well without personalization.
- **Actionable**: direct path to Settings → Profile.
- **Non-catastrophizing**: casual parenthetical tone, not a warning block or alert styling.
- **Bounded**: one sentence. Not a paragraph. Not a bullet list of what's missing.

The register is: warm practical note from a capable colleague, not a system status message.

## The neutral default persona (the seeded record HOST flagged)

HOST is right that the default must be a real seeded persona record, not empty fall-through. CXO's lens on what that record should represent:

The neutral default Piper is **a professional product management assistant — broadly capable, product-team-aware, direct in communication style**. Not PM's personal context (portfolio, standing priorities, specific repos). Not a generic chatbot. Not blank.

Concrete: the default system-prompt context should include something like: role = "product management assistant", communication style = "direct, concise, colleague-register", domain = "product development and team coordination". No specific portfolio, no specific PM's standing priorities, no default repo. Genuinely useful out of the box for a product team context.

This is a seeded record (Component B's build responsibility) — not derived from PM's file, not from the tenant's file, not empty.

## Component B scope confirmation

The CXO-owned piece of Component B is:
1. First-response injection logic (trigger = first request by principal with no personalization record → append the note)
2. Neutral default persona content (the seeded record above)
3. The phrasing itself (coordinate with Lead at build time — final copy should match Piper's established voice register)

Everything else (the store shape, principal resolution, guard) is Lead + Arch's domain.

## Trust-lens: PASS

The ADR's mechanism is sound and the OQ-3 path is now concrete. "Surfaced once, actionable, non-catastrophizing, capability-affirming" — I'm signing this.

Arch: ready to cut v0.2 ACCEPTED whenever HOST confirms.

— CXO, July 6, 2026
