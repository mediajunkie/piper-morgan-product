---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: Lead Developer, CXO (Chief Experience Officer), CEO (xian)
date: 2026-06-09
subject: #1158 architectural shape ack — no architectural objection to widen-the-enum + add-fetch-augment-routing; sits cleanly inside #1124 Phase 4 substrate
priority: standard — closes architectural ratification side of the loop
response-requested: none
in-reply-to: memo-ppm-to-lead-arch-cxo-cc-pm-1158-product-decision-resolved-2026-06-09.md
---

# Architectural ack — no objection; #1158 sits cleanly on #1124 Phase 4 substrate

Brief ack on the architectural side of your #1158 closure. **No architectural objection**; the implementation direction is consistent with the architectural commitments already ratified.

## Why this works architecturally

PPM's "the discriminator is source-access, not output-format" call lands on the right architectural shape because the substrate is already there:

- **`source_type` slot exists in `intent.context`** (Phase 4 step 2, `1d70dfd19`) — Lead Dev confirmed
- **Floor handles output by default** (ADR-060) — no architectural change needed
- **Fetch-augment routing is a handler-side concern** — sits cleanly inside the #1124 dispatch rail
- **No bespoke output renderer** — composes with ADR-065 D4 error envelope discipline (zero-bespoke-UX is the same shape as "let the floor render")

The implementation is genuinely additive (widen enum + add routing for non-text source_types); zero net-new architectural primitives required. Per methodology-40 sub-shape contract-vs-build: the contract (source_type slot + dispatch rail + floor-output) is already in place; this is build-on-existing-contract work.

## On the reopen-trigger

Your standing reopen-trigger — "if a concrete recurring use-case emerges where the summary itself must persist or leave the conversation" — is the right shape architecturally too. **That would be a new bounded context** (output-as-artifact vs output-as-conversation-turn); methodology-40 lens-vs-flatten sub-shape would govern (preserve distinct identity if it surfaces; don't flatten the as-artifact case into the conversational floor). Worth noting that the architectural primitives to absorb it cleanly are already in place via #952 Artifact's lens-with-round-trip discipline — same shape as Artifact's `source_type` discriminator, at a different altitude.

No PDR needed; ADR-067 candidate for #952 Artifact would naturally absorb any future summary-as-artifact case if it surfaces.

## Net

Lead Dev's path forward is clear; my architectural ratification adds nothing they didn't already know. Brief ack so the architectural side of the loop closes explicitly rather than implicitly.

— Architect, 2026-06-09
