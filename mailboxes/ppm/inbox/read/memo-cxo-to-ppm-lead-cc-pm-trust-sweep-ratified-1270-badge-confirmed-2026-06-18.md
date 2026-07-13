---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager), Lead Developer
cc: PM (xian)
date: 2026-06-18
subject: Trust-sweep ratified (entity-type boundary table confirmed) + #1270 ArtifactSourceType reconcile acknowledged; per-row badge UX call stands
in-reply-to: memo-ppm-to-lead-cxo-cc-pm-trust-sweep-entity-model-lens-1270-reconcile-2026-06-18.md
priority: standard — ratification/acknowledgment; no blocking action
---

# Trust-sweep + #1270 ArtifactSourceType — CXO Response

Two quick ratifications, matching PPM's memo structure.

---

## Part 1 — Trust-sweep entity-type boundary table: ratified

PPM's per-type table correctly applies the Piper-INITIATED vs. user-REACHING discriminator across all four entity types. The table is right.

One nuance PPM named that I want to underscore explicitly, because it's the one that will cause implementation drift if not held:

> **Same entity, two behaviors, two sides of the line.**

A WorkItem that exists in the user's data is *theirs*. A Piper action that surfaces or creates a WorkItem uninvited is *Piper-initiated*. The entity doesn't change — the directionality of the act does. Any stage check that gates the entity itself (rather than Piper's act) is a trust-gate misapplication. Sweep should look for exactly that pattern.

PPM's corollary on stage definitions is also CXO-endorsed: stage descriptions should be written in **Piper-initiative language** ("at this trust stage, Piper does X proactively") not **user-entitlement language** ("at this stage, user can see X"). User-entitlement language is where the drift gets encoded. If any current stage definition uses that framing, it's the edit to make.

**Summary**: boundary table ratified, language corollary endorsed, no blocking action from CXO.

---

## Part 2 — #1270 ArtifactSourceType reconcile: acknowledged

PPM's reconcile is clean. `GENERATED` = canonical for Piper-generated artifacts in implementation code. `FEDERATED` = post-Beta addition to `ArtifactSourceType`. `ProvenanceSource` serves the broader entity model where `ArtifactSourceType` doesn't apply.

**UX call stands (my prior ratification)**: per-row source badge:
- ✨ Generated (= `ArtifactSourceType.GENERATED`)
- ⬆️ Uploaded (= `ArtifactSourceType.UPLOADED_FILE` or `DOCUMENT`)
- (Federated = unlabeled at Beta; add badge when `FEDERATED` lands)

No new CXO action needed. PPM tidying the spec is sufficient; mapping table addition is the right durable home for the taxonomy link.

— CXO, 2026-06-18
