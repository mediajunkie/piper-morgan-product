# #1017 OUTPUT-CONTENT-FILTER — Phase 0 audit

**Issue**: [#1017](https://github.com/mediajunkie/piper-morgan-product/issues/1017) — ARCH-DESIGN: Post-generation content filter for LLM outputs reaching users (PII/safety)
**Priority**: `priority: critical`
**Source**: Architect's Apr 27 batch-3 codebase review (Finding I) + PA Apr 17 "Gap 2"
**Date**: 2026-05-15

---

## Pattern-067 verdict: NEGATIVE

Body claims fully verified against current code, with two minor drifts (file moved, redaction pattern count grew after #1007). The substantive claim — **LLM outputs flow to users without post-generation filtering** — holds.

### Verification

| Body claim | Status |
|---|---|
| `BoundaryEnforcer` operates only on user *inputs* | ✅ `enforce_boundaries(message, ...)` at `boundary_enforcer_refactored.py:157` — docstring explicitly says "User message/content to check" |
| `services/intent_service/document_handlers.py` (453 LOC) calls LLM without output filter | ✅ 3 `llm_client.complete()` sites (lines 163, 297, 445); no post-filter |
| `services/intent_service/conversational_floor.py` (694 LOC) emits LLM responses | ✅ `llm.complete()` at line 633; the `BoundaryEnforcer` references at lines 130/191/199 handle input-side violation redirect context, not output filtering |
| `services/integrations/github/issue_analyzer.py` (298 LOC) generates content | ✅ `self.llm.complete(...)` at line 126 |
| `services/knowledge/ingestion.py` generates concept/relationship metadata | ⚠️ **PATH DRIFT** — file is at `services/knowledge_graph/ingestion.py` (likely moved post-filing). Same LLM-output shape confirmed: `self.llm.complete()` at line 108 |
| `services/intent_service/llm_classifier.py` (753 LOC) emits reasoning text in audit envelope | ✅ Two `self.llm.complete()` sites (lines 326, 554); reasoning text is operator-visible via audit log |
| `audit_transparency.py:39-54` has email/SSN/credit-card/phone/URL regex patterns | ⚠️ **MINOR DRIFT** — patterns are at lines 42-49 (off by a few lines). Pattern set now 6 patterns (email + SSN + 2 phone formats + credit card + digit-only phones), not 5; phone-format additions landed via #1007 fix 2026-05-02. Substantive claim correct: patterns exist + are applied to audit logs, not LLM-generated user-routed content. |
| `services/integrations/github/content_generator.py` has "placeholder-instruction safety pattern" | ⚠️ **INTERPRETATION DRIFT** — the file's `_validate_and_sanitize()` method (line 295) is **format validation** (title truncation, label dedup, valid priorities/types), not PII redaction. The "placeholder instructions" in the prompt at line 144 are prompt-engineering guidance for the LLM, also not output-side filtering. Body's "consider generalizing in parallel" note doesn't accomplish output PII filtering. **This is not a useful starting point for the filter; build fresh.** |

### Negative checks (confirms no existing filter)

- **`SecurityRedactor` usages**: only in `audit_transparency.py` itself (5 internal references). Zero callers in user-output paths.
- **Pattern hunt**: `grep -rE "output_filter|filter_output|post_gen|redact_output|sanitize_response"` over `services/` → **zero matches**. No latent partial implementation to discover or complete.

### Adjacent infrastructure (reusable)

- **`SecurityRedactor.redact_sensitive_data(text: str) -> str`** at `audit_transparency.py:54` — fully testable, no DB dependency, reusable for the output filter's PII pass. **#1007 fix** (2026-05-02) added phone patterns so it now matches the most common PII shape.
- **`audit_transparency` durability infrastructure** — Phase 2 shipped May 2 (`EthicsAuditRepository` + Postgres `ethics_audit_log` table + `AsyncSessionFactory.session_scope()` per call). The output filter's audit envelope can write through the existing `log_ethics_decision` path. **AC dependency "depends on companion durability issue" is satisfied.**
- **`BoundaryDecision` schema** at `boundary_enforcer_refactored.py:62` — output-filter decision schema can mirror its shape (violation flag, type, explanation, audit data).
- **`#1004 semantic detector for inputs`** (closed Apr 27) — its detection schema generalizes to outputs but doesn't trivially transplant; LLM-content failure modes differ from user-input attack patterns.

---

## Sibling/parent context

- **#1016 LLM-touch boundary principle** (OPEN, parent epic) — frames "boundary-flexibility / core-determinism" as the cross-cutting architectural shape. #1017 is one Phase 4 alignment item per body cross-ref. **#1017 doesn't need to wait for #1016**; it can ship as a specific instance of the broader principle, and its design memo can inform #1016 reciprocally.
- **#992 ETHICS-ACTIVATE** (CLOSED Apr 30, Phase F flag-flip merged) — input-side ethics enforcement live. #1017 is the output-side complement.
- **#1018 audit_transparency durability Phase 2** (CLOSED May 2) — durable audit log live. AC dependency satisfied.

---

## Scope read

This is a genuinely substantial ARCH-DESIGN issue. Architect's body estimates **~3 days Phase 1 design + ~3-5 days Phase 2 implementation + ~2 days Phase 3 verification = 8-10 days total** across multiple sessions. Phase 1 has at least 5 design questions, each material:

1. **Filter contract**: decorator on `LLMClient.complete()` / middleware / per-surface explicit call?
2. **Detection scope**: PII regex (reuse SecurityRedactor)? Add `BoundaryEnforcer` category set applied to outputs? Length/format anomalies? API key / secret formats?
3. **Action on match**: redact-in-place / canned-response / drop / operator-review? Varies by severity?
4. **Audit envelope shape**: what fields go into the durable log? (`surface, rule_matched, severity, redactions_applied, action_taken, original_hash, redacted_hash`?)
5. **Decision schema**: `OutputFilterDecision` analogous to `BoundaryDecision`?

The AC explicitly requires **Architect + CXO + PM** ratification of the design — CXO has voice equity on the redact-vs-canned-response decision (it's user-visible tone, not just engineering).

---

## Three paths

### Path A — Full Phase 1 design pass now

Write a comprehensive design memo (analogous to yesterday's `1021-phase-1-design.md`) covering the 5 design questions with options + recommendations per question, route to Architect + CXO + PM for ratification.

**Cost**: ~2-3 hours for the design memo today. Ratification turnaround is on Architect + CXO + PM (probably Mon at earliest given Friday). Phase 2 implementation starts post-ratification.

**Pro**: locks the design before implementation; matches yesterday's #1021 cadence (Phase 0 → design memo → PM ratification → Phase 2 same/next session); CXO sees their voice-equity decisions on time.
**Con**: Phase 2 implementation can't start until ratifications land; if any of three ratifiers needs clarification, sequence stretches.

### Path B — Sub-design memos by question

Split the 5 design questions into 2-3 smaller memos based on who owns the decision (engineering → Architect, voice/tone → CXO, prioritization → PM). Route in parallel.

**Cost**: ~3-4 hours for 2-3 memos today. Ratification can parallelize.
**Pro**: faster aggregate ratification; each ratifier reads a shorter, more focused memo.
**Con**: cross-decision constraints (e.g., filter contract shape constrains audit envelope) get fragmented; recombining ratified pieces into a coherent implementation gameplan adds work.

### Path C — Defer #1017; pick a smaller M2g item first

#1017 stays open; today's session covers a faster pick — **#1087** (`SEC-JWT-SECRET-PROD-GUARD`, priority:high, likely 1-2hr fix) or **#1088** (`GITHUB-ADAPTER-DEMO-FALLBACK`, priority:medium, likely 2-4hr).

**Cost**: 1-4 hr depending on pick.
**Pro**: ships something concrete today; respects PM's bandwidth for the larger #1017 conversation across multiple sessions.
**Con**: #1017 is `priority: critical` and PM picked it; deferring without a real reason isn't healthy.

---

## Recommendation: Path A

Phase 1 design memo today (~2-3 hours), routed to Architect + CXO + PM by end of session. Matches yesterday's #1021 cadence shape (audit → design memo → PM ratifies → Phase 2 same/next session). Phase 2 implementation lands next session.

The design questions are substantial enough that splitting them (Path B) creates more reassembly work than parallel ratification saves. And deferring (Path C) doesn't square with `priority: critical`.

---

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #1017 |
| Pattern-067 check | ✅ NEGATIVE (body fully verified; 2 minor drifts noted; substantive claim holds) |
| Body-vs-reality | ✅ all 7 file references verified; 1 path drift, 1 line-number drift, 1 interpretation drift documented |
| Existing infra mapped | ✅ SecurityRedactor + audit_transparency durability + BoundaryDecision schema reusable; #1018 dependency satisfied |
| Scope questions | ✅ 5 design questions surfaced; A/B/C with ratification-cadence framing |
| Risk assessment | ✅ multi-ratifier sequencing; CXO voice-equity dependency; cross-decision constraints |
| Recommended path | ✅ Path A — Phase 1 design memo today, ratify by Monday |

---

## STOP — awaiting PM disposition on A/B/C

Most consequential: do we do Phase 1 design today (A or B) or defer #1017 in favor of a smaller pick (C)?

— Lead Developer, 2026-05-15
