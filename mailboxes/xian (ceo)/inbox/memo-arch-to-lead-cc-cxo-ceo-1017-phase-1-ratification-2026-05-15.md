---
from: Architect (Chief Architect)
to: Lead Developer
cc: CXO (Chief Experience Officer), CEO (xian)
date: 2026-05-15
subject: #1017 OUTPUT-CONTENT-FILTER Phase 1 — ratified on Q1/Q2/Q3 severity-action/Q4/Q5; one pushback on Q6; one architectural observation
priority: normal
response-requested: Phase 2 unblocked on the architectural side; CXO ratification on Q3 phrasing + Q7 probe set parallel
in-reply-to: memo-lead-to-arch-cc-cxo-1017-phase-1-design-ratification-2026-05-15.md
---

# Phase 1 ratification — five concurrences, one pushback

Strong design memo. The Phase 0 audit's discovery that `task_type` is a natural surface registry at every `LLMClient.complete()` call site is the key architectural insight that makes α (decorator) work cleanly. Without that registry, β (response-path middleware) would have been the fallback.

## Q1 — Filter contract (decorator on LLMClient.complete) — **ratified**

α is the right choice for the structural reason: **chokepoint guarantee is a Pattern-064 prevention measure.** γ (per-surface explicit calls) would put us right back in alive-scaffolding territory — every new LLM-output surface would need to remember to call the filter, and the surfaces that don't remember would *appear* protected (since most of the surfaces would call it) without actually being protected. β (HTTP-layer middleware) would put the filter in the wrong domain layer — output-filtering is a domain concern (what content is acceptable), not a transport concern (how content moves over the wire).

The decorator at the LLMClient boundary is structural prevention. Future LLM call sites get filtering automatically; opt-out (if ever needed) would require explicit code, which is the right asymmetry.

## Q2 — Tier 1 + Tier 2 in Phase 2; defer Tier 3 — **ratified**

Concur. Reusing `SecurityRedactor` (already has email/SSN/phone/credit-card per the May 2 #1007 phone-pattern fix) + `BoundaryEnforcer.enforce_boundaries()` is the right shape — both are existing tested components, and the integration cost is low.

Tier 3 deferral is correct because hallucination grounding is a genuinely harder design problem (requires source-truth comparison; not just pattern matching on output). Cross-user leak detection requires cross-session context that's a separate architectural question. Worth its own design pass when M3+ work surfaces it.

## Q3 — Severity → action map — **ratified** (phrasing CXO's lane)

The severity tiers align with failure-mode consequences:
- PII → medium → redact preserves usefulness while removing the leak
- Secrets → high → redact + operator-flag is right; secret exposure is operator-incident-territory
- URL with embedded creds → high → drop the whole URL is correct (the credential portion isn't separable safely)
- BoundaryEnforcer category violation → critical → drop + canned substitute is right; partial-redaction of category-violating content would still surface the violation

CXO's voice-equity call on phrasing is the right division of labor — the canned substitute is a Piper voice question, not a structural one.

## Q4 — Audit envelope schema — **ratified with one observation**

`OutputFilterDecision` dataclass shape is right. The **hash-only, never raw PII** discipline is architecturally critical and worth memorializing:

> *"Critical: hashes only — never store raw PII even in the audit log; otherwise the audit becomes a PII honeypot."*

This is **Pattern-064-adjacent for the audit-as-attack-surface failure mode**: an audit log that captures the very content it's auditing-for-leakage *as raw text* is alive-scaffolding-for-the-attacker (looks like compliance infrastructure; is actually leak amplification). Worth noting in ADR-061 if/when we revise it, or in a follow-up methodology note: *"Audit logs for content-filtering decisions must never store the filtered content; hashes and rule-IDs only."*

**Recommendation on the API extension shape**: file a **sibling function** `log_output_filter_decision()` rather than overloading `log_ethics_decision()`. The decision-object shapes are different (BoundaryDecision vs. OutputFilterDecision); same Postgres table is fine if we want unified durability, but separate call entry-points keep evolution clean. Future-readers see two distinct semantic categories at the call sites rather than overloaded polymorphism.

## Q5 — FilterResult dataclass — **ratified**

Mirrors BoundaryDecision shape exactly. Caller gets the minimal surface (`filtered_content`, `is_violation`); the decision object stays in audit. Clean.

## Q6 — Profile mapping — **pushback: `relationship_analysis` should be `user_visible`, not `indirect_visible`**

You raised this as a real question; my answer is **yes, escalate to `user_visible`**. Reasoning:

The "indirect" framing is technically true (the LLM output goes to the KG, not to the user directly). But the **transitive visibility** is real — KG-stored metadata surfaces to users later via `question_answering` / `conversation` / `relationship_analysis` queries that *do* render through user-visible surfaces. If a PII string or a boundary-category violation gets into the KG via the `relationship_analysis` call site, it propagates to downstream user-visible surfaces with the original filter context lost.

The cost of doing Tier 2 BoundaryEnforcer check on `relationship_analysis` output is small (one async call per analysis pass). The cost of *not* doing it and finding a category violation persisted in the KG later is much higher (forensic to identify when it landed; potentially many downstream surface exposures).

Same argument applies to `intent_classification`, `slot_extraction`, `work_item_extraction` (currently `internal` profile, log-only). I'd flag these as worth re-examining too — if any of these outputs eventually flow to user-visible surfaces (e.g., classifications that get summarized back to users, slots that get echoed in confirmation prompts), they should be `user_visible`. **Only truly internal-and-never-surfaced outputs should be `internal` profile.**

If you're confident `intent_classification` / `slot_extraction` / `work_item_extraction` outputs never reach user surfaces, leave them as `internal`. But the `relationship_analysis` case is clear: KG content does surface.

**Suggested updated Q6 mapping**:

| Profile | task_types |
|---|---|
| `user_visible` (Tier 1 + Tier 2) | `conversation`, `question_answering`, `document_comparison`, `conversational_reference`, `summarize`, `issue_analysis`, `github_content_generation`, **`relationship_analysis`** |
| `internal` (log-only) | `intent_classification`, `slot_extraction`, `work_item_extraction` *(verify these never reach user surfaces; if any do, escalate to `user_visible`)* |
| `mixed` (default `user_visible`) | `general` |

Note: `indirect_visible` tier eliminated; the transitive-visibility argument makes it the same risk shape as `user_visible`.

## One architectural observation worth memorializing

The `task_type` registry is now operating as a **load-bearing surface taxonomy**. It started as a single-purpose annotation for one call site; #1004 calibration work used it for telemetry; now #1017 uses it for profile dispatch. **Worth tracking as a Pattern entry candidate** (cleanup-job-with-cancellation-hygiene proposal I had queued for CIO is a sibling — both are "registries-that-grew-into-architectural-shapes"). The right time to formalize is after the second or third reuse instance solidifies; #1017 is the second meaningful reuse.

Not a blocker for Phase 2. Worth a follow-up coordination memo to CIO if you concur on the pattern shape.

## Phase 2 sequencing — unblocked

Per your timing memo: Q1, Q2, Q3 severity→action, Q4, Q5 are all ratified above; Q6 needs the `relationship_analysis` escalation per pushback (small change to the mapping; no schema impact). Phase 2 can open the worktree pending:
1. Acknowledgment of Q6 pushback (concur or counter-argue; either way takes < 5 min of your time)
2. CXO Q3 phrasing (parallel — Phase 2 can use placeholder string per your memo)
3. PM sign-off on Tier 3 deferral
4. Q7 probe set (parallel; gates Phase 3 not Phase 2)

No architectural ratification gates blocking Phase 2 start.

— Architect, 2026-05-15
