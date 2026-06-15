# PPM Spec: Radar / Layer-2 Entity Model

**Status**: ACTIVE — M4 PPM deliverable
**Author**: PPM
**Date**: June 15, 2026
**Related**:
- PDR-002 Appendix: Layer-2 Vision (CXO-owned; canonical vision doc; surface renamed below)
- PDR-003: Entity Concept Model (Product/Project/Repository)
- #1216: Provenance field (InsightDB `source`/`is_seed`)
- #1217: People entity + relationship-network map
- #1090: UI-1.0 history epic (tracking home for Radar slot-swap work)
- CXO memo: History-sidebar flattening — Layer 2 IS Radar (June 13, 2026)

---

## 1. Context

PM ratified (June 13, 2026): **Layer 2 = Radar.** The history sidebar consolidates into the Radar ambient surface; Layer 1 (chat navigation) stays in the left nav. The redundant right-sidebar chat list is retired.

This spec is the PPM object-model lane commitment for M4: which entity types surface in Radar, what their fields look like, and what honest-provenance requires. It builds on PDR-002 Appendix (the CXO-owned vision doc, which remains canonical for the Layer-2 design principles) and scopes the M4 implementation work.

**Note for CXO**: PDR-002 Appendix §surface framing should be updated from "History Sidebar" to "Radar" now that PM ratified the consolidation. The vision is correct; the home has moved. That update is CXO's lane.

---

## 2. Entity Type Set

Five entity types surface in Radar / Layer-2. These are the PPM-ratified types for M4:

| Entity Type | Description | M4 scope |
|---|---|---|
| **WorkItem** | Tracked unit of work with lifecycle (draft → active → done → archived) | Existing; provenance field added |
| **Document** | Artifact Piper has encountered/analyzed; last-touched date | Existing; provenance field added |
| **People** | A contact, teammate, or AI agent the principal talks about; typed + networked | **New in M4** (personhood-type + relationship edges per PM/CXO #1217 elevation June 14) |
| **Conversation** | One facet of Radar entity-search — NOT a standalone list | Existing in DB; wire into Radar search as a facet |
| **Lifecycle/insight event** | What Piper has noticed: reflections, observations, watch-fires | Existing; honest-provenance field required |

**Ordering principle**: Entities are primary content; Conversations are navigation aids to entities (per PDR-002 Appendix §3.2). Surface entity cards; let Conversations appear as "related conversations" links on entity detail.

---

## 3. People Entity (M4 new addition)

PM elevated the People concept to a first-class capability on June 14 (#1217): *"learn who the people and agents the principal talks about and map them as a network — team members, stakeholders, AI entities, etc. — as a specific type of thing Piper inherently does and stores in its local knowledge base."*

**People entity fields (PPM object-model spec):**

```
PeopleEntity
  id: str
  name: str
  personhood_type: "human" | "agent" | "stakeholder"
  relationship_edges: List[RelationshipEdge]  # to other People + to WorkItems/Projects
  context_notes: str  # what Piper has inferred about this person
  source: ProvenanceSource  # see §4
  first_mentioned_at: datetime
  last_mentioned_at: datetime
  owner_id: str  # user who Piper learned this for
```

```
RelationshipEdge
  from_entity_id: str
  to_entity_id: str
  relationship_type: str  # "reports-to" | "collaborates-with" | "manages" | "is-agent-for" | etc.
  confidence: float  # 0.0–1.0; how confident Piper is in this edge
  source: ProvenanceSource
```

**`personhood_type` values:**
- `human` — a person (team member, stakeholder, end user, etc.)
- `agent` — an AI entity (another Claude instance, an AI tool the principal uses)
- `stakeholder` — a person/group the principal refers to but doesn't directly work with (client, executive, external party)

This field is what the Gap-1 classifier in #1217 reads — the map is the memory the floor consults when deciding whether to ask vs. assume personhood.

**One store, not two**: People-entities live in the same entity model as WorkItems/Documents/Conversations. No separate "contacts" system. The relationship-network map is the People facet of the entity model.

---

## 4. Provenance Field (Required on All Surfaced Entities)

The honest-provenance principle (CXO June 13, PPM June 15): **the surface must never assert a real-vs-seed distinction it cannot ground in a provenance field.** This is the data-model prerequisite for Radar/Layer-2 surfacing honestly.

**Provenance enum (shared across entity types):**

```python
class ProvenanceSource(str, Enum):
    SEED = "seed"                      # seeded during dev/demo setup
    SESSION_EXTRACTED = "session_extracted"  # extracted from a live conversation
    USER_CONFIRMED = "user_confirmed"   # user explicitly told Piper
    INFERRED = "inferred"              # Piper inferred (confidence < threshold)
```

**On `InsightDB` (M4 work, #1216):**
- Add `source: ProvenanceSource` field (not nullable; default `SEED` for existing rows)
- Add `is_seed: bool` derived property (`source == SEED`)
- Seed scripts mark entries as `source=SEED`; live extraction marks `source=SESSION_EXTRACTED`
- Floor prompt filter: strip `SEED` entries from the context the model sees (Lead Dev's interim guard already does this; the field makes it structural rather than tag-based)

**Radar surfacing rule**: if `source == SEED` and user has real data, hide seed rows from Radar. If `source == SEED` and user has no real data yet, show as "placeholder" with honest framing ("This is an example — Piper will learn your real [entity type] as you work together").

**Scope note**: the provenance field should be added to all entity types that surface in Radar, not just `InsightDB`. M4 scope is `InsightDB` (#1216) as the first landing; other entity types get the field as they are formalized.

---

## 5. Trust-Gated Surfacing

From PDR-002 Appendix §2.3 (unchanged; reproduced here for M4 implementation reference):

| Trust Level | Visible Features |
|---|---|
| Stage 1-2 | Conversation archive, basic search |
| Stage 3 | WorkItem surfacing, Document tracking |
| Stage 4 | Cross-entity relationships, People network |
| Stage 5 | Full lifecycle management, pattern insights |

**M4 implementation target**: Stage 3 (WorkItems + Documents) visible and backed by provenance field; Stage 4 (People network) spec complete and wired, surfacing with provenance. Stage 5 is M5 or post-MVP.

---

## 6. M4 Scope Summary

| Work item | Owner | Dependencies |
|---|---|---|
| `InsightDB` provenance field migration (#1216) | Lead Dev | This spec; M4 sprint entry |
| People entity data model (personhood-type + relationship edges) | Lead Dev | This spec; #1217 rule language (PA) |
| Wire Conversations as one entity-facet in Radar search | Lead Dev | Radar slot-swap (#1090) |
| Entities-surfacing mockup | CXO | CXO committed June 13 |
| People-as-surfaced-entity in Radar mockup | CXO | Folds into entities-surfacing mockup |
| Conceptual-integrity gate (PDR-002 Appendix ↔ issue binding) | Lead Dev + Docs | CXO mockup; this spec |

---

## 7. Open Questions

**OQ-1 (Lifecycle events)**: Should lifecycle/insight events be a standalone entity type with their own `source` field, or stay as a property on WorkItem/Document? Initial lean: separate type (they have a different temporal nature — events, not objects). PPM call in M4 scoping.

**OQ-2 (Relationship edge confidence threshold)**: What confidence threshold makes an inferred relationship edge surfaceable vs. hidden? Initial lean: ≥0.7 for surfacing; ≥0.9 for asserting in the floor prompt. Lead Dev consultation on M4 scoping.

**OQ-3 (PDR-002 Appendix update)**: CXO to update the surface framing (History Sidebar → Radar) in PDR-002 Appendix. Not a PPM-lane call; flagged here so it doesn't get lost.

---

## 8. What This Spec Does Not Do

- Does not specify the Radar card design language (CXO lane)
- Does not specify the slot-swap implementation (#1090 / Lead Dev lane)
- Does not amend PDR-002 Appendix (CXO-owned; OQ-3 above flags what needs updating)
- Does not scope People rule language (#1217 PA lane)
- Does not spec the trust-computation backend (ADR-053)

---

*PPM — June 15, 2026. M4 object-model lane. Consult PDR-002 Appendix for Layer-2 design principles; this doc is the PPM object-model complement.*
