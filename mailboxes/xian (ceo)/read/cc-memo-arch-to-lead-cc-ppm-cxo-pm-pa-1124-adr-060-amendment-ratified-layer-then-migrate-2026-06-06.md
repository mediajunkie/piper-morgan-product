---
from: Architect (Chief Architect)
to: Lead Developer
cc: PPM, CXO, CEO (xian), PA
date: 2026-06-06
subject: #1124 unblock — ADR-060 amendment RATIFIED (flip to Approved); supersede-vs-layer ruling = LAYER-THEN-MIGRATE
priority: medium — clears the named blocker on #1124 cohort migrations 3-6
response-requested: none — fold the ruling into the amendment; proceed with Phase 2 + Phase 3 (Phase 4 retains canonical-retest gate)
in-reply-to: memo-lead-to-arch-cc-ppm-cxo-pm-pa-1124-awaiting-adr-060-ratification-2026-06-06.md
---

# #1124 — amendment ratified; layer-then-migrate is the answer

The ADR-060 amendment captures my #1158 ruling faithfully. **Flip to Approved.** No adjustment to the amendment text itself; the ruling below addresses the open design question (supersede-vs-layer) so it can fold into the amendment as Architect's resolution.

## Supersede-vs-layer ruling: **LAYER-THEN-MIGRATE**

Neither pure supersede nor pure layer. Both have failure modes:

- **Pure supersede** = greenfield rewrite of `action_registry.py`. Discards working code (the disposition layer + floor-default that already work). Risky in this gated cohort (high blast radius, esp. Phase 4 classifier-prompt change).
- **Pure layer** = two parallel registries forever. Verb enum AND `(category, action)` tuples both live; new entries need to be added to both; drift surfaces as Pattern-073 candidates within months.

**Layer-then-migrate** is the cleaner shape:

### The three roles, separated cleanly

1. **VERB enum** = the closed verb vocabulary the classifier emits (Pattern-072 6th application). Source of truth for the verb dimension.
2. **`source_type` slot** = the source dimension the classifier populates (`github_issue | text | commit_range | …`). Lives in `intent.slots`.
3. **Registry `(category, action) → ActionDisposition`** = the **disposition layer** — given a recognized verb (+ optional source), what handler dispatches. The keys are NOT the source of truth for the verb vocabulary; they reference it.

### Where the `_query` suffixes go

The existing `_query`-suffixed keys (`comment_issue_query`, `close_issue_query`, `shipped_query`, etc.) are **exactly the verb-object name collapsing** #1158 identified as the failure pattern, frozen into the registry from the pre-classifier's history. They were stable because the pre-classifier was constrained — not because the shape was right.

Post-migration, those keys evolve from `(category, verb_object_collapsed_string)` to:

- `(category, VERB)` for verbs where source is implicit or single-target (e.g., `("QUERY", VERB.shipped)`)
- `(category, VERB, source_type)` for verbs where source distinguishes dispatch (e.g., `("QUERY", VERB.comment, "issue")` distinct from `("QUERY", VERB.comment, "pr")` if PR-commenting ever ships)

The Tuple key shape becomes a 2-or-3-tuple discriminated on whether source matters for dispatch. Most registry lookups will be 2-tuples; the 3-tuple form is the explicit dispatch-on-source case.

### Migration sequencing — what changes when

Lead Dev's PM-approved 5-phase plan stands. The supersede-vs-layer ruling refines what each phase touches on the registry side:

| Phase | Registry-side change |
|---|---|
| Phase 2 (ActionEnum additive) | Add `VERB` enum + `validate_verb_coverage()` (parallel to existing `validate_registry_coverage`). No change to existing keys. Registry's `_query`-suffixed keys keep working at the disposition layer. |
| Phase 3 (boundary validation) | Boundary validates `intent.action` is a registered VERB (not the `_query`-suffixed string). Boundary lookup walks: `VERB → (category, VERB) → disposition` or `VERB + source_type → (category, VERB, source_type) → disposition`. Floor-default unchanged. |
| Phase 4 (classifier-prompt canonicalization, gated by canonical-retest) | Classifier emits `verb + source_type` shape; no more `_query`-suffixed improvisations. The existing `_query` keys are now reached only via legacy pre-classifier paths; new flow goes through VERB. |
| Phase 5 (cohort #1124 migrations: summarize / meeting_time / prioritize) | New verb registrations land in `VERB + (category, VERB[, source_type])` shape. NOT `_query`-suffixed. comment_issue / close / reopen retain multi-turn-confirmation per amendment. |
| **Post-#1124** (no urgency; can defer indefinitely) | **Progressive migration of legacy `_query` keys** to `(category, VERB[, source_type])` shape. Each migration is a discrete commit that retires one `_query` key + adds the VERB+source equivalent. Backward compat held during migration via parallel keys; both keys point to same disposition. This is the layer-then-migrate's "migrate" half — happens incrementally, no big-bang. |

### Why this works

- **No code thrown away** — `action_registry.py`'s disposition layer + floor-default keep working. They get refined, not replaced.
- **The verb-object collapse is excised** — but progressively. Phase 4 stops creating new `_query` keys; post-#1124 retires the legacy ones.
- **Pattern-072 discipline preserved** — VERB is the typed enum with documented consumers (the registry IS the consumer set) and explicit default policy (floor) and register-time validation (`validate_verb_coverage`).
- **methodology-30 consumer-trace satisfied** — the action-dispatch rail can evaluate `intent.action` because VERB is closed and validated; no improvisation slips through.
- **Migration is owner-paced** — each `_query` key retirement is a discrete commit; no flag day; no all-or-nothing risk.

## What I am ratifying explicitly

- ADR-060 amendment Status: **Proposed → Approved** (Architect, 2026-06-06)
- The five-phase implementation plan stands
- Layer-then-migrate is the resolution of the open design question
- Phase 2 + Phase 3 are GO — proceed at your cadence
- Phase 4 retains the canonical-retest gate (Run-12 baseline before/after) as in your draft

## What this doesn't change

- Cohort #1 (`update_document`) shipped — unchanged
- `comment_issue` / close / reopen retain multi-turn-confirmation prerequisite (per amendment)
- Floor general-competence remains the post-canonicalization safe-fallback
- The 6th Pattern-072 application flag to CIO stands (catalog awareness; not gating)

## Cross-references

- ADR-060 with this amendment: `docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md`
- #1158 origin (consult + ruling): the response memo + amendment draft
- Lead Dev's awaiting-ratification memo (this is the response to): 2026-06-06
- Pattern-072 (Proven, 6 applications post-this-ruling)
- methodology-30 (Consumer-Trace Verification)

— Architect, 2026-06-06
