---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian), PPM (Principal Product Manager)
date: 2026-06-14
subject: #1090 GREEN — entities-surfacing mockup is ready; build the slot-swap. Guidance + the one coordinate-with-PPM dependency.
priority: standard — you're eager + unblocked; here's the guidance you were waiting on
response-requested: none — build to the mockup; pair offer below
---

# #1090 — go. The mockup is the spec.

PM-ratified (consolidate-on-Radar, "feels calming") + loved the mock + confirmed attention-first + two-states. You're unblocked.

**The artifact (the spec)**: `dev/active/radar-entities-surfacing-mockup-2026-06-14.html` — self-contained, two states, built to your Part-B card language. The HTML *is* the binding artifact; build to it.

## Build direction (matches your own feasibility read — re-homing, not greenfield)

1. **Slot swap**: render the **Radar entity surface** in the History-sidebar slot (replace the conversation-list render in `templates/components/history_sidebar.html`). The home Radar module components ("what i'm seeing" = Places, "recently" = insights) are the same surface family — reuse them.
2. **Entity cards** via the Part-B `Card` component: `entity-type` label · title · **lifecycle-state badge** · provenance · meta. Multiple types (WorkItem / Document / Person / Conversation), not just conversations.
3. **Attention-first ordering** — most-active / recently-changed at top, types mixed. (Not type-grouped; type is a filter, not the top structure.)
4. **Entity-search subsumes chat-search** — the search box spans all entity types; **conversations are one type among others** (this is what kills the redundancy + preserves the useful part of History). Wire the richer `#1021 /users/me/history` backend + the `#706` entity catalog rather than the conversation-only endpoint.
5. **Two states**: **default = real-only** (every card `● observed`, no example/seed cards); **empty = explainer + ONE labeled example card** (teaching device, disappears once real items exist).
6. **Honest provenance (#1214/#1216 fix, data layer)**: seed/dev data **never renders as `● observed`** — excluded from a real user's view; `○ seed` in dev only. Not a user-facing card in default.

## The one coordinate-with-PPM dependency (don't block on it — build the surface, slot the model in)

The **entity model** is PPM's lane: the exact entity-type set + lifecycle-state vocabulary + the **provenance/`is_seed` field** + the **People entity's personhood-type field** (human/agent/stakeholder, per #1217/people-network). The surface (mockup) is settled; the model it renders is PPM-coordinated. Build the surface to the mockup; wire the model fields as PPM lands them. (PPM cc'd.)

## Anti-recurrence (the durable fix, per your binding-link point)
- **Closure gate**: #1090 (and any Layer-2/Radar issue) must pass *"surfaces entities (Layer 2), not just conversations (Layer 1 duplicate)?"* before closing. Cite **PDR-002 Layer 2 + this mockup** in the AC. That's the binding link that stops the 4th recurrence.

## Tracking
#1090 (UI-1.0 history epic) — PM moved it into the D1 beta-design sprint. Happy to pair on the IA/render details once you're into it; ping me with anything the mockup doesn't answer.

— CXO, 2026-06-14
