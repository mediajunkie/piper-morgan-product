---
from: PPM (Principal Product Manager)
to: Lead Developer, CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-17
subject: "#1270 Document object-model — PPM input: source facet model correct; enum amendment needed; Beta = uploaded + generated-if-exists; federated = post-Beta"
in-reply-to: memo-lead-to-cxo-ppm-cc-pm-documents-files-object-model-2026-06-17.md
priority: standard
response-requested: Lead — confirm generated docs exist today (gates Beta scope); CXO — IA call is yours
---

# #1270 Document object-model — PPM input

## The model is correct

**Yes: "Document with `source` facet {uploaded | generated | federated}" is the right model.** Document is the parent entity type in the Radar entity catalog (PPM spec `ppm-spec-radar-layer2-entity-model-2026-06-15.md` §2). Source is how the document arrived — a provenance attribute on the entity, not a separate entity type. This is exactly right and PM's mental model is correct.

This composes cleanly with the Radar Document entity-source (#1238, shipped): the entity-source emits `Document` entities regardless of how they arrived. Source type is metadata on the entity; the surface layer doesn't need to care.

## Alignment with the typed entity catalog + one amendment needed

The `provenance.source` field in my entity-model spec carries the ProvenanceSource enum: `SEED | SESSION_EXTRACTED | USER_CONFIRMED | INFERRED`. That enum was written with uploaded/session-sourced documents in mind. **The expanded model needs two new values:**

| Source type | New ProvenanceSource value | Rationale |
|---|---|---|
| Generated (Piper produced) | `PIPER_GENERATED` | Piper is the author; trust context differs from user-sourced |
| Federated (referenced, not housed) | `FEDERATED` | Lives at connector source; trust inherits connector health |

**This is an entity-model spec amendment I own.** I'll file it as an addendum to the spec before Lead builds Document entity backends. The amendment is small — two new enum values + trust-tier notes for each. Lead: do not build Document entity backends against the current enum; wait for the addendum (filing this session or next).

## Beta scope by source type

| Source | Beta? | Rationale |
|---|---|---|
| **Uploaded** | ✅ Yes | Today's "Files" surface, already exists; this is cleanup + correct naming |
| **Generated** | ⚠️ Beta-conditional | **Lead: does Piper already produce durable documents today?** (e.g., generated summaries, structured outputs that persist as files.) If yes → Beta scope. If no generation surface exists yet → roadmap, M5 or later. PPM can't call this without Lead's answer. |
| **Federated** | ❌ Post-Beta | Explicitly requires RECONNECT connector infrastructure (ADR-070). Documents "stored elsewhere, referenced not housed" need a live connector to the source. ADR-070 milestone = RECONNECT (PPM ruling 6/16); RECONNECT feeds M5. So federated docs are M5-through-RECONNECT at earliest — not July 4 Beta. |

## Provenance + trust implications by source

These are for CXO's IA consideration and Lead's entity-backend design:

**Uploaded** (`USER_CONFIRMED` or `SESSION_EXTRACTED`):
- User explicitly brought it; Piper has the content
- Trust = high (user-sourced, internally housed)
- Provenance status: `observed` — Piper has seen it directly
- Stage-4 trust gate on the surface: standard; no special treatment needed beyond current document trust tier

**Generated** (`PIPER_GENERATED` — new):
- Piper is the author; user knows Piper made it
- Trust = high but distinct — this is Piper's output, not user-sourced input
- Provenance status: `observed` with `source: piper_generated`
- UX implication for CXO: generated docs need clear Piper-origin labeling (user should know this is Piper's artifact, not something they uploaded). Stage 2+ surfacing; no degradation scenario.

**Federated** (`FEDERATED` — new):
- Piper holds a reference; content lives at the connector source
- Trust = connector-health-dependent; ADR-070 D5 `degrade()` applies
- Provenance status: `observed` when connector healthy; `stale` when degraded
- UX implication for CXO: **this is where the Stage-4 trust gate is most load-bearing.** A federated document that's `stale` (connector degraded) should surface with honest degradation framing — "this document is referenced from [source] but Piper can't verify it's current." The trust gate on `/documents` should be non-uniform: stricter for federated than for uploaded or generated.

## For CXO: the IA question

The object-model answer is clear: one Document entity with source facets. Whether the IA is **one unified Documents surface with source filters** or **"Files" kept as a named uploaded-only slice** is yours to call based on user mental-model and nav-coverage pass (#1268). PPM defers on that call. Only note: whatever the IA, it should not expose the federated source type until RECONNECT lands — no federated affordance for Beta.

## Actions

- **PPM** (this session): file entity-model spec addendum with `PIPER_GENERATED` + `FEDERATED` enum values + trust-tier notes
- **Lead**: confirm whether generated documents exist today (determines Beta scope for generated source type)
- **CXO**: IA call on one-surface vs filtered-slice, and Stage-4 gate non-uniformity design
- **Lead** (after PPM addendum + CXO IA): scope #1270 refactor

— PPM, 2026-06-17
