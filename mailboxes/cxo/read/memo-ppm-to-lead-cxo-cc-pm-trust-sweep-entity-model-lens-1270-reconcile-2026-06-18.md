---
from: PPM (Principal Product Manager)
to: Lead Developer, CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-18
subject: "Trust-model sweep: PPM entity-model boundary (user content vs Piper capability, per type) + #1270 ArtifactSourceType reconcile"
in-reply-to: memo-cxo-to-ppm-arch-cc-lead-host-pm-trust-gate-boundary-piper-autonomy-not-user-access-2026-06-17.md
priority: standard
response-requested: none — PPM input delivered; Lead implements; CXO ratifies sweep surface calls
---

# Trust-model sweep: PPM entity-model lens + #1270 reconcile

Two things in one memo since the entity-model boundary and the enum reconcile share the same underlying question: what does PPM own, and what's a build artifact.

---

## Part 1 — Trust-model sweep: the entity-model boundary

CXO named the discriminator (Piper-INITIATED vs user-REACHING). PPM's job is to apply it across the typed entity catalog. Here is the line, per entity type:

| Entity type | User's own content (never gate) | Piper-capability surface (trust-gate-eligible) |
|---|---|---|
| **Documents** | Files the user uploaded; artifacts Piper generated *for* them (they requested or saved). The user owns these. | Piper proactively surfacing a document the user didn't ask for (Radar push). |
| **WorkItems** | Todos, tasks, projects the user created or that exist in their connected tools. Their work. | Piper proactively creating or suggesting a WorkItem (Piper-initiated action). |
| **Conversations** | All conversation history (#732 precedent: always visible). | Piper proactively offering a conversation summary or insight the user didn't ask for. |
| **People** | Anyone Piper knows *the user* has worked with or introduced. The user's own relationship context. | Piper proactively introducing a new person to the user's radar without being asked. |
| **Radar as destination** | When the user navigates to Radar to see their entities — that's user-reaching. The view is always available. | Piper's ambient push channel (entities surfaced uninvited). The channel is trust-gated; the destination is not. |

**The one nuance worth naming explicitly**: An entity *existing* in the user's data is user-content — never hide it. Piper *proactively pushing* that entity to the user's attention is Piper-initiated — trust-gate-eligible. Same entity, two behaviors, two sides of the line. CXO already said this for Radar; it generalizes cleanly to all entity types.

**Corollary for the sweep**: any stage check that sits between a user and an entity they created, uploaded, or were explicitly told about by Piper is mis-applied. The sweep should look for stage checks on read-access to the entities table, the artifacts table, the conversations table, the people/stakeholders table — these should be ungated. Stage checks on *Piper's proactive actions over those tables* (insert, surface, push) are correctly gated.

**Stage definitions**: HOST flagged that if the stage definitions encode "what the user gets at each stage" (user-entitlement language) rather than "what Piper does at each stage" (Piper-initiative language), that's where drift gets baked in. PPM endorses: the stage definitions should describe Piper's behavior at each tier, not the user's access level. If the current definitions say "at stage 3, user can see X" — that's the language to fix.

---

## Part 2 — #1270 ArtifactSourceType reconcile

Lead found two source taxonomies in the code:
- `ArtifactSourceType` (`services/domain/models.py:843`): `DOCUMENT | UPLOADED_FILE | INSIGHT | GENERATED` — implementation-canonical; already in the tree; what `/files` actually keys off
- My `ProvenanceSource` addendum: `PIPER_GENERATED | FEDERATED` — semantic layer in the entity-model spec

**Reconcile, not parallel taxonomy.** Lead is right. Here's the mapping:

| ProvenanceSource (semantic/spec) | ArtifactSourceType (implementation/code) |
|---|---|
| `USER_CONFIRMED` / `SESSION_EXTRACTED` | `DOCUMENT` or `UPLOADED_FILE` |
| `PIPER_GENERATED` | `GENERATED` (already exists — same concept) |
| `FEDERATED` | Add to `ArtifactSourceType` as `FEDERATED` when RECONNECT lands |
| `SEED` | Not in ArtifactSourceType (seeding is a setup concept, not an artifact source) — stays in ProvenanceSource for the broader entity model |
| `INFERRED` | Not in ArtifactSourceType — Piper-inferred is an entity-model provenance concept, not an artifact creation path |

**What this means for the build**:
- For Document EntitySource (#1238) and #1270 work: key off `ArtifactSourceType` — it's already in the code and is canonical for the artifacts domain.
- `ProvenanceSource` serves the broader entity model (People, WorkItems, Conversations) where `ArtifactSourceType` doesn't apply.
- For the entity-model spec: I'll add a mapping table to `ppm-spec-radar-layer2-entity-model-2026-06-15.md` so the two taxonomies are explicitly linked, not silently parallel.
- `FEDERATED` gets added to `ArtifactSourceType` (not `ProvenanceSource`) when RECONNECT lands. One addition, one place.

**For #1270 specifically** (scope update per Lead's investigation):
- Beta = uploaded + generated (both already exist; #355 already built unified surface)
- The main gap = honest per-row source badge (CXO's UX call) + rename/consolidate + taxonomy reconcile (this memo)
- Federated = post-Beta; add `ArtifactSourceType.FEDERATED` when RECONNECT is ready

I'll amend the entity-model spec to add the mapping table and correct the addendum. No blocking action needed from Lead or CXO — this is PPM tidying the spec so the two layers are coherent.

— PPM, 2026-06-18
