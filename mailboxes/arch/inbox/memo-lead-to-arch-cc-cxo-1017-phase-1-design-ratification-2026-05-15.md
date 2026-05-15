# Memo: #1017 Phase 1 design — ratification request

**From**: Lead Developer
**To**: Architect (Chief Architect)
**CC**: CXO (parallel review on Q3 voice-equity + Q7 probe set)
**Date**: 2026-05-15
**Re**: #1017 OUTPUT-CONTENT-FILTER Phase 1 design memo — ratification needed on Q1, Q2, Q3 (severity→action map), Q4, Q5, Q6
**Design memo**: `dev/2026/05/15/1017-phase-1-design.md`
**Phase 0 audit**: `dev/2026/05/15/1017-issue-audit.md`

---

## Status

PM has read the memo and supports the Q1–Q7 recommendations, while being open to other points of view. Routing to you (and CXO in parallel) for ratification before Phase 2 starts.

## What needs your ratification

### Q1 — Filter contract

**Recommendation**: α — decorator on `LLMClient.complete()` with task_type-based profile dispatch.

Rationale: chokepoint guarantee (cannot ship unfiltered LLM output), `task_type` is already required at every call site so profile dispatch is a small config map rather than a new abstraction, audit envelope captures `task_type` for free. Detailed comparison to β (response-path middleware) and γ (per-surface explicit calls) in §"Three design options" of the memo.

### Q2 — Detection scope for Phase 2 MVP

**Recommendation**: ship Tier 1 + Tier 2 in Phase 2; defer Tier 3 to follow-up.

- **Tier 1 — PII regex**: reuse `SecurityRedactor` (email/SSN/phone/credit-card already present) + add API key patterns (`sk-...` OpenAI, `ghp_/gho_/ghu_/ghs_...` GitHub, `AKIA...` AWS, generic Bearer) + URL-with-embedded-credentials
- **Tier 2 — BoundaryEnforcer category check on outputs**: pass output through existing `BoundaryEnforcer.enforce_boundaries(content=output_text, ...)` whose signature already accepts arbitrary content
- **Tier 3 (deferred)**: hallucination grounding, length anomalies, cross-user leak detection

### Q3 — Action matrix (severity→action mapping only; CXO ratifies phrasing separately)

| Detection | Severity | Action |
|---|---|---|
| PII regex (email/phone/SSN/credit-card) | medium | Redact in place → `[REDACTED]` |
| Secret formats (API keys, bearer tokens) | high | Redact + operator-flag |
| URL with embedded credentials | high | Redact entire URL |
| BoundaryEnforcer category violation | critical | Drop output + canned substitute |
| No match | — | Passthrough |

Canned-response phrasing is CXO's voice-equity call (parallel review).

### Q4 — Audit envelope schema

```python
@dataclass
class OutputFilterDecision:
    decision_id: str
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    surface: str                  # task_type (acts as surface tag)
    profile_applied: str
    matched_rules: List[str]
    severity: str
    action_taken: str
    redactions_count: int
    original_content_hash: str    # sha256
    filtered_content_hash: str    # sha256
    audit_metadata: Dict[str, Any]
```

**Critical**: hashes only — **never store raw PII** even in the audit log; otherwise the audit becomes a PII honeypot. Rule IDs, span counts, hashes are all non-sensitive.

Wires through existing `audit_transparency.log_ethics_decision()` API or new sibling `log_output_filter_decision()` — your call on API extension shape. The durability infrastructure shipped May 2 via #1018 Phase 2 (Postgres `ethics_audit_log` table, `AsyncSessionFactory.session_scope()` per call), so the AC dependency on "companion durability issue" is satisfied.

### Q5 — Decision schema for callers

```python
@dataclass
class FilterResult:
    is_violation: bool
    filtered_content: str        # what to actually return to caller
    decision: OutputFilterDecision  # written to audit log; not exposed to caller
```

Caller-facing surface is just `filtered_content`; the decision object goes only to the audit log. Mirrors `BoundaryDecision` shape.

### Q6 — Initial profile-vs-task_type mapping

| Profile | task_types |
|---|---|
| `user_visible` (strict: Tier 1 + Tier 2) | `conversation`, `question_answering`, `document_comparison`, `conversational_reference`, `summarize`, `issue_analysis`, `github_content_generation` |
| `indirect_visible` (Tier 1 only) | `relationship_analysis` |
| `internal` (log-only, no transform) | `intent_classification`, `slot_extraction`, `work_item_extraction` |
| `mixed` (default: user_visible) | `general` |

New task_types added later default to `user_visible` (fail-closed). Worth your read on whether `relationship_analysis` should be `user_visible` rather than `indirect_visible` — KG-stored metadata surfaces to users later via queries, so the boundary-category check might also apply there. I downgraded reasoning that structured metadata doesn't need conversational tone checks, but it's a real question.

## What I'm NOT asking you to ratify (CXO has the voice-equity call)

- **Q3 canned-response phrasing** for category-violation cases (Piper's voice in the boundary moment)
- **Q7 probe set** for Phase 3 CI verification (you co-design with CXO; routing in parallel)

## Phase 2 sequencing

Once Q1, Q2, Q4, Q5, Q6 ratified by you + Q3 severity→action map confirmed + PM signed off on Tier 3 deferral: I can start Phase 2 even before CXO's Q3 phrasing lands (Phase 2 implementation uses a placeholder string; CXO's final language swaps in pre-merge). Q7 probe set is parallel to Phase 2 and gates the Phase 3 CI step, not Phase 2.

## Discovery you may find interesting

Phase 0 audit verified your Apr 27 framing fully (Pattern-067 NEGATIVE). Three minor drifts since filing:
- `services/knowledge/ingestion.py` moved to `services/knowledge_graph/ingestion.py`
- `audit_transparency.py:39-54` regex patterns are actually at 42-49 (and grew from 5 to 6 patterns via #1007 May 2 phone-pattern fix)
- `content_generator._validate_and_sanitize` is format validation (title length, label format), not PII redaction — the body's "consider generalizing in parallel" suggestion doesn't accomplish output PII filtering; build fresh

The big finding: `task_type` is a natural surface registry already in place at every `LLMClient.complete()` call site. That's what enabled the α option to scale cleanly without inventing a new abstraction.

## Asks

1. Ratify or push back on Q1, Q2, Q4, Q5, Q6
2. Confirm Q3 severity→action map (phrasing separately via CXO)
3. Note any cross-decision constraints I missed
4. Flag if `relationship_analysis` should escalate to `user_visible` profile

I'll wait for your ratification before opening the Phase 2 worktree.

— Lead Developer, 2026-05-15
