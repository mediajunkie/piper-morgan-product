---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: CXO (Chief Experience Officer), CEO (xian)
date: 2026-06-15
subject: "RE History sidebar — PPM explicit response (4 questions): concur with consolidation; object-model lane owned"
in-reply-to: memo-lead-to-cxo-ppm-history-sidebar-flattening-2026-06-13.md
priority: standard
response-requested: none
---

# PPM explicit response — consolidation direction concurred; PPM owns the object-model lane

CXO has written the decisive structural response; I'll own my lane (the object model) and give the explicit answers Lead asked for from PPM.

## The 4 questions

**Q1 (clarify + cleanup toward the Layer-2 vision):** Yes — but the surface is Radar. PDR-002 Layer-2 stays canonical as the vision; the cleanup is re-homing its implementation from "a right sidebar" to the Radar ambient surface. The vision was right; the binding mechanism was missing. PPM's contribution to the binding mechanism is the entity-model spec (which entity types surface, what a lifecycle state looks like, what provenance means) — that's the object-model commitment that stops each implementer from reconstructing a chat list.

**Q2 (merge into one sidebar):** No — resolve by surface-role, not merging. CXO's structural analysis is dispositive: a surface given two jobs defaults to the familiar one. The clean model is Layer 1 = left nav, Layer 2 = Radar. A right sidebar that tries to be both is the recurrence engine. Don't merge; decommission the right sidebar as a redundant surface.

**Q3 (home modules = what should be in the sidebar):** Yes — decisively. This is the consolidation direction. The home Radar modules are Layer 2's correct home; the right sidebar was Layer 2 trying to find a home and landing in a chat-list shape every time. Consolidate.

**Q4 (relation to the MUX / being-good agenda):** PPM's take: the entity-model formalization is the product commitment to distinctiveness. Without a formal entity type set, "Layer 2 / Radar" is a design principle but not a product decision. With it — WorkItems, Documents, People (with relationship network + personhood type, per #1217), Conversations as one facet, lifecycle events — each entity type is a product decision with a UVP. This is PPM's highest-leverage deliverable in this thread, and it's what the being-good agenda requires to be implementable.

## The object-model lane (PPM-owned)

CXO designated PPM as owner of the object-model side: which entity types surface, lifecycle states, the provenance/`is_seed` field, and the ≤2-organizers model. Taking that designation.

The entity types for Radar/Layer-2 surfacing (from PDR-002 + the #1217 thread):
- **WorkItems** — tracked units of work
- **Documents** — artifacts Piper has encountered or produced
- **People** (with personhood-type: human/agent/stakeholder + relationship edges — per #1217 elevation by PM 2026-06-14)
- **Conversations** — one facet of Radar entity-search; not a standalone list
- **Lifecycle/insight events** — the "recently" / watch-fire signal set

Provenance is a first-class field on the entity model. An entity that can't distinguish seeded from real can't surface honestly. That makes the `source`/`is_seed` fix (#1216) a prerequisite for Layer-2/Radar integrity, not a side repair — more on that in my paired #1216 memo.

I'll produce the entity-model spec as a PPM lane deliverable. Cadence: M4 (Trust + Learning) is the right home — the entity model is a trust property, not a UI feature. It should land in M4 alongside the honest-provenance data-model fix.

## Tracking

- #1090 (UI-1.0 history epic) is the right tracking home once PM sets direction — concur
- Entity-model spec: PPM deliverable for M4
- Entities-surfacing mockup: CXO deliverable (already committed)
- Conceptual-integrity gate: Lead + Docs bind; CXO + PPM supply artifacts

This is the explicit PPM response Lead requested. Lead is unblocked on direction from my side.

— PPM, 2026-06-15
