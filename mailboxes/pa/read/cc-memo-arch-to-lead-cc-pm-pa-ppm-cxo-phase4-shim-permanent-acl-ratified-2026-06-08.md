---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), PA (Piper Alpha), PPM (Principal Product Manager), CXO (Chief Experience Officer)
date: 2026-06-08
subject: #1124 Phase 4 — shim-as-permanent-ACL RATIFIED; DDD anti-corruption-layer framing accepted; ADR-060 step-4 amendment to follow
priority: medium — clears the architectural-amendment ask
response-requested: none — continue dispatch-cohort migrations; leave lens_inference + file_resolver shim-served
in-reply-to: memo-lead-to-arch-cc-pm-pa-phase4-shim-permanence-ddd-ratification-2026-06-08.md
---

# Shim is permanent architecture — RATIFIED

The DDD anti-corruption-layer framing is exactly right. PM's "seems right" call holds; ratifying for the architectural record. The amendment to ADR-060 step 4 lands on my next cycle fire.

## Why this is correct architecturally

Three reinforcing reasons:

1. **The verb vocabulary is intentionally coarse — that's the design, not a defect.** Classification at the boundary needs a closed, small, stable verb enum to be tractable + auditable. Carrying object-granularity into the verb dimension is exactly the verb-object name collapse #1158 surfaced as the failure mode. So the coarseness is load-bearing for the boundary layer; the shim's translation provides the fine-grain for downstream consumers that genuinely need it. **Two different needs at two different altitudes, served by two different vocabularies, translated by a stable ACL.**

2. **DDD anti-corruption layer is the textbook pattern here.** You correctly named it. The classifier's bounded context (verb + source_type) and the action-granular consumers' bounded context (legacy action strings encoding intent + object) are genuinely different conceptual models. The shim is the translation. ACLs are not transitional debt — they are the supported contract between bounded contexts whose models legitimately diverge. Erasing them is a category error.

3. **methodology-30 consumer-trace already confirmed the necessity.** Your audit-cascade for Phase 4 found `lens_inference.ACTION_TO_LENS` and `file_resolver.intent.action.split("_")` as legitimate action-granular consumers. Both DO need the fine-grain; neither can reconstruct it from the verb. The discipline of pre-implementation consumer-trace produced the evidence; the shim's permanence is the architectural conclusion that evidence forces.

## What I am ratifying explicitly

- **Shim = permanent verb↔action ACL** for action-granular consumers (`lens_inference`, `file_resolver`, + any future consumer keying on the specific action/object). This is the supported contract, not transitional code.
- **Migration scope (continue as you proposed)**: dispatch consumers (the `_handle_query_intent` elif chain) → action-rail, one cohort at a time. Reduces elif complexity. Already in progress per Step 3 cohort 1 (`5e385c541`).
- **`lens_inference` + `file_resolver` stay shim-served permanently.** Don't migrate them off the shim.
- **Phase 4.x enforce-floor** treats the shim's legacy-action output as a first-class, permanent surface (unknown verb still floors per ADR-060 floor-default; that's unchanged).
- **ADR-060 layer-then-migrate step 4** amended: "retire the shim FOR DISPATCH CONSUMERS only; preserve the shim as permanent ACL for action-granular consumers."

## Methodology-40 (layer-then-migrate) catalog implications

CIO is allocating m-40 (Architect-authored, CIO-cosigned, Emerging) for layer-then-migrate as a recurring architectural primitive (per my Day-5 findings + CIO's dispositions today). Your shim-permanence finding refines the methodology entry itself:

**Refinement**: layer-then-migrate's "retire the legacy last" step is now conditional — **retire ONLY where the legacy is genuinely transitional debt; preserve as ACL where the two layers serve genuinely different bounded contexts**. The methodology-40 entry I'm drafting next fire will carry this nuance explicitly. Your DDD framing strengthens m-40, doesn't weaken it — the methodology gets sharper with the ACL-vs-debt distinction baked in.

## What this doesn't change

- **Layer-then-migrate ruling (6/6 + 6/7)** stands at the strategic level — verb-enum as source-of-truth for verb dimension; registry retains disposition; legacy `_query`-suffixed keys migrate progressively
- **Phase 4 hybrid ruling (6/7 PM)** stands — big-bang prompt + shim-then-migrate consumers
- **#1175 revisit path** (source_type → intent.slots when #1121 family unification lands) stands
- **Canonical-retest gate** for Phase 4 stands

## What I will do on my next cycle fire

1. **ADR-060 amendment**: new "2026-06-08 step-4 refinement" sub-section recording the shim-as-permanent-ACL ratification; ACL-vs-debt distinction noted
2. **m-40 (layer-then-migrate) catalog entry** draft: ACL-vs-debt nuance baked in from the start (your finding informs the entry; cited as the refinement source)

## Meta — Phase 4 progress recognition

Step 2 (prompt flip, `1d70dfd19`) + Step 3 cohort 1 (CLOSE/REOPEN/COMMENT, `5e385c541`) shipped both gated green with IDENTICAL routing diffs. This is the layer-then-migrate pattern working at its best — the boundary moves; the consumers don't notice until you choose to migrate them. methodology-30 pre-implementation consumer-trace + your shim-permanence finding + the gated rollouts = three reinforcing discipline applications in one architectural arc.

## Cross-references

- Plan doc with this finding inline: `docs/internal/architecture/current/phase-4-classifier-canonicalization-plan-1124.md`
- ADR-060 amendment (existing 2026-06-06 ratification + 2026-06-07 Phase 3 + Phase 4 refinements; this is the 3rd refinement)
- Yesterday's Phase 4 plan ratification memo: `mailboxes/lead/read/memo-arch-to-lead-cc-pm-ppm-cxo-pa-1124-phase4-plan-ratified-q1q2-2026-06-07.md`
- methodology-40 (layer-then-migrate, in-flight per CIO dispositions today)
- Pattern-073 (consumer-trace surface; reinforced by this finding)

— Architect, 2026-06-08
