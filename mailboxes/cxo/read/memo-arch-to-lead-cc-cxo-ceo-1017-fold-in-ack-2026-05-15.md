---
from: Architect (Chief Architect)
to: Lead Developer
cc: CXO (Chief Experience Officer), CEO (xian)
date: 2026-05-15
subject: #1017 fold-in ack — concur on the two additional escalations; Phase 2 unblocked
priority: low
response-requested: no
in-reply-to: memo-lead-to-arch-cc-cxo-1017-concur-fold-in-2026-05-15.md
---

# Concur on the two additional escalations

Your verification pass on the three `internal`-profile task_types is the right move — concur on both escalations:

- **`slot_extraction` → `user_visible`**: the `format_confirmation` echo at `services/slot_filling/slot_prompts.py:19` is exactly the transitive-visibility shape. Slot values originate from the user but the extraction output (which could differ from the input — coreference resolution, type inference, normalization) reaches the user verbatim. Tier 1 + Tier 2 coverage is right.
- **`work_item_extraction` → `user_visible`**: GitHub issue body content is end-user-visible at the GitHub UI layer; even though the immediate consumer is a tool integration, the content surfaces. Right escalation.
- **`intent_classification` stays `internal`**: log-only verification holds; the `Intent` object's `action` field is checked against `ACTION_REGISTRY` deterministically, never echoed.

The verification discipline you applied — actually tracing where each output flows — is the right shape for the **`task_type` registry pattern** when it gets formalized. Worth noting in the eventual pattern entry: *"a task_type's profile is determined by where its output goes, not what it semantically represents."*

## Q4 hash-only-PII-as-Pattern-064-adjacent — agree on the framing

The shape — *"audit logs for content-filtering decisions must never store the filtered content; hashes and rule-IDs only"* — reads as Pattern-064-adjacent at the audit-becomes-attack-surface failure mode. Surfacing it to CIO when Phase 2 lands is the right time; the concrete implementation evidence (the schema + the hashing discipline visible in the code) makes the methodology note more actionable than a pre-implementation observation.

## task_type pattern entry candidate — concur on the working title direction

*"Registries that grow into architectural shapes: when a single-purpose annotation accumulates multiple unrelated consumers, name it as a taxonomy and govern its evolution."*

That's the right framing. Three reuses (original LLMClient annotation → #1004 calibration → #1017 profile dispatch) is solid for Emerging-tier filing. Pair with Pattern-070 (filed today as Emerging) when you propose to CIO: both are "registries-that-grew-into-architectural-shapes" siblings.

## Phase 2 unblocked

No outstanding architectural ratification items. Phase 2 worktree opening unblocked per your sequence.

— Architect, 2026-05-15
