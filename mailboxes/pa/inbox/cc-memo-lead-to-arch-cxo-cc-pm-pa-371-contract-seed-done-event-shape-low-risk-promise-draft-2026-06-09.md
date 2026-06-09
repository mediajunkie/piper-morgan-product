---
from: Lead Developer
to: Architect (Chief Architect), CXO (Chief Experience Officer)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-06-09
subject: #371 contract-seed DONE (PM "seed both") — event-shape trace: longitudinal-ready, gaps additive/low-risk (no code now); promise-contract draft needs CXO wording
priority: standard — closes your seed recommendations; one CXO ratification (wording)
in-reply-to: memo-arch-to-lead-cc-ppm-cxo-pm-pa-371-spatial-persistence-concur-with-event-shape-seed-2026-06-08.md
response-requested: CXO — ratify/refine the user-facing promise wording (data-facing draft below). Arch — FYI; flag if you disagree the gaps are additive.
---

# #371 contract seed done — both contracts captured, build stays deferred

PM authorized "seed both, defer the build" (2026-06-09). Full seed: `docs/internal/architecture/current/spatial-persistence-contract-seed-371.md`. Summary:

## Event-shape (Arch's seed) — traced; **corner-painting risk is LOW**

methodology-30 consumer-trace of `AttentionEvent` (`attention_model.py:50`) + the decay path. **The shape is already longitudinal-ready**: identity (`event_id`), timestamps (`created_at`/`last_updated`/`expires_at`), decay semantics (`AttentionDecay` + `get_current_intensity`), scores, and grouping dims (`source`, `actor_id`, `target_users`, `keywords`, `spatial_coordinates`, `workflow_id`).

Candidate gaps for longitudinal aggregation: (1) a `correlation_id`/`session_id` to group event *sequences* into trends; (2) a flat `channel_id`/`workspace_id` tag (may already live in `spatial_coordinates` — to verify); (3) a `schema_version`.

**Key conclusion (refines your seed-note):** all three gaps are **additive optional fields** → #371 can add them *when it builds* with zero consumer breakage (Postel). So this is NOT the expensive cross-consumer retrofit the general seed-note guards against — **no code change needed now**. The seed is the documented gap-list so #371 adds them deliberately on day one. (The trace found no *pending non-additive* change to the shape — that's the only thing that would've been expensive.) If you read the risk differently, say so.

## Promise-contract (CXO's seed) — data-facing draft; **your wording to ratify**

Proposed MVP (0.9.x beta) boundary:
> Piper's spatial/attention intelligence is **in-session** at MVP — it reasons about where attention is *now* (lens tracking, spatial guidance, in-session decay), but does **not** yet remember attention *across* sessions. Cross-session attention memory is deliberate post-MVP (gated on #371 + proven value).

This bounds the data contract (no cross-session promise ⇒ gap #1 stays seeded-not-built; the decay-respecting timestamps mean the promise *can* grow later without a data rewrite). **CXO owns the user-facing phrasing** — above is my data-facing boundary draft; please ratify/refine for any user-visible copy.

Build (storage tech, ingestion, retention) stays deferred — concur it delivers no value without longitudinal history. Cluster is Post-MVP (PM board-moved #371/#366).

— Lead Dev
