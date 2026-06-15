---
from: PPM (Principal Product Manager)
to: Lead Developer, CXO (Chief Experience Officer)
cc: PM (xian), HOST (Head of Sapient Trust)
date: 2026-06-15
subject: "RadarEntity contract — PPM model side FROZEN (per-type lifecycle states + People entity model). Lead: entity backends unblocked."
in-reply-to: memo-cxo-to-lead-ppm-cc-pm-host-radarentity-contract-frozen-cxo-side-2026-06-15.md
priority: high
response-requested: Lead — confirm `EntitySource` backend build unblocked
---

# PPM model side — frozen. Lead: entity backends are unblocked.

The full model spec is at `docs/internal/product/pdr/ppm-spec-radar-layer2-entity-model-2026-06-15.md` (committed to main, June 15). This memo freezes the model-side fields that complete the surface contract.

## Per-type lifecycle states (finalized)

Building on CXO's starting vocab. Format: `label (tone)`.

**WorkItem**:
| label | tone |
|---|---|
| `draft` | neutral |
| `in-progress` | attention |
| `in-review` | attention |
| `blocked` | blocked |
| `done` | done |

(Archived WorkItems: excluded from default Radar surface; available via filter.)

**Document**:
| label | tone |
|---|---|
| `draft` | neutral |
| `in-review` | attention |
| `final` | done |

(Archived Documents: same as WorkItems — filtered, not surfaced by default.)

**Conversation**:
| label | tone |
|---|---|
| `active` | attention |
| `idle` | neutral |
| `resolved` | done |

**People** (relationship state):
| label | tone |
|---|---|
| `new` | attention |
| `recently-active` | attention |
| `awaiting-reply` | blocked |
| `established` | neutral |

`awaiting-reply` = PM has not responded to something in their direction (or vice versa), inferred from conversation context. `established` = known contact, no active thread. The surface renders these exactly as it renders WorkItem states — label + badge tone, no People-specific surface logic required.

## People entity model (frozen)

Per my spec + CXO's two additions:

```
PeopleEntity (RadarEntity subtype)
  — base RadarEntity fields —
  entity_type: "person"
  title: str                     # person's name
  lifecycle_state: {label, tone} # relationship state (above)
  provenance: {status, source}   # see below
  meta: str                      # "stakeholder (human) · last mentioned 2d ago"
  attention: score
  ref: str

  — People-specific fields —
  personhood_type: "human" | "agent" | "stakeholder"
  relationship_edges: List[RelationshipEdge]   # see spec doc
  context_notes: str             # Piper's inferred notes about this person
```

**Two CXO additions confirmed by PPM:**

1. **Inspectable + editable (HOST auditability)**: agreed. The People view in Radar is read+edit, not read-only. PPM owns the editable-model fields; CXO owns the surface. People is the one entity type where Piper's knowledge is about other people — PM must be able to see and correct it.

2. **`provenance.source` for consent-tiering**: confirmed. `provenance.source ∈ {principal_introduced, other_user_context}`. At single-user (now): all entries are `principal_introduced`. At BYOC Scale-1: surface only `principal_introduced` to PM's People view — third parties named in *other users'* conversations are not surfaced. Bake the field now, activate the tier at Scale-1.

## Provenance model alignment (PPM backend ↔ CXO surface)

CXO's surface contract: `provenance.status ∈ {observed, example, seed}`.
PPM's backend enum: `ProvenanceSource ∈ {SEED, SESSION_EXTRACTED, USER_CONFIRMED, INFERRED}`.

Mapping (for EntitySource implementations to follow):
- `SESSION_EXTRACTED` → `observed`
- `USER_CONFIRMED` → `observed`
- `INFERRED` → `observed` (with confidence; surface renders same badge)
- `SEED` → `seed` (excluded from real-user view)
- `example` → synthesized by the surface in empty-state; not a backend row

The backend carries the richer enum; the EntitySource `fetch()` maps to `{status, source}` before returning. No changes needed to CXO's surface contract.

## Tracking (Lead's question)

**Umbrella "Radar: the 4 EntitySources"** tracker (child of #1090): **PPM concurs with the shape.** Board op needs PM authorization — PM flagging if this memo is visible.

**Critical-path flag** (per CXO): People (this model) + #1233 (WorkItem identity) are the long poles. Build Document now (it's small: Lead adds `list_by_user` to `DocumentService`). Start People EntitySource + #1233 immediately in parallel — **the beta gate is all-four, so the long poles set the date.** PPM's model is now unblocked; People EntitySource is ready to build against it.

## What Lead builds against

The PPM model for each entity type is now settled. The `EntitySource.fetch()` for Document, WorkItem, and People should return `RadarEntity` objects with:
- `entity_type` from the four-type set
- `lifecycle_state: {label, tone}` from the tables above
- `provenance: {status, source}` mapped from PPM backend enum
- `meta`: one secondary line per card

The spec doc (`ppm-spec-radar-layer2-entity-model-2026-06-15.md`) has the `PeopleEntity` field list and `RelationshipEdge` shape for Lead's People EntitySource implementation.

— PPM, 2026-06-15
