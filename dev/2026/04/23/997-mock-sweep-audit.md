# #997 MOCK-SWEEP — First-Pass Audit

**Author**: Lead Dev (code-opus)
**Date**: 2026-04-23
**Branch**: `claude/992-ethics-activate` (piggybacking — no #992-critical files touched)
**Status**: ⏸ **First-pass complete. No deletions performed. Awaiting PM review before any cleanup.**

---

## Scope

Per issue AC: categorize each of 86 files matching `grep -rln "mock_\|fallback" services/ --include="*.py"`.

**Line-level hits**: 494 across 86 files. This report presents:
1. Full categorization of the 12 `mock_` files (high-signal per PM's "mocks scare me")
2. Directory-level bucketing of the 76 `fallback` files with representative samples
3. Follow-up recommendations

**Why no deletions**: per CLAUDE.md "never run destructive operations unless explicitly requested." I can identify dead code with high confidence, but the judgment call on *whether to remove* belongs to PM. This report is the decision surface.

---

## Categorization Buckets (per issue AC)

- **Legitimate** — production fallback/mock that should stay (e.g., graceful degradation, retry, config defaults, DI test hooks)
- **Dead code** — fallback for a path that can't happen anymore; candidate for removal
- **Test-leakage** — mock imported into production code path; move or delete
- **Uncertain / needs design decision** — escalate to PM / Architect

---

## Part 1 — `mock_` hits (12 files, full pass)

| File | Line(s) | Pattern | Bucket | Rationale |
|------|---------|---------|--------|-----------|
| `services/intent_service/llm_classifier_factory.py` | 92-103 | `mock_knowledge_graph_service=None, mock_semantic_indexing_service=None, mock_llm_service=None` | **Legitimate** | Standard factory DI pattern; parameters allow passing mocks during tests. Defaulted `None`; no production code path invokes them. |
| `services/debugging/slack_inspector.py` | 207-230 | `mock_api_calls: bool = True` | **Legitimate** | Debug tool's feature — allows replaying a stored event without triggering real Slack API calls. Core to the inspector's purpose. |
| `services/debugging/commands.py` | 67, 72, 165 | `mock_calls: bool = True` | **Legitimate** | CLI wrapper around `replay_event`, same rationale as slack_inspector. |
| `services/api/slack_monitoring.py` | 390-418 | `mock_calls: bool = True` | **Legitimate** | HTTP wrapper around the same event-replay infrastructure. |
| `services/infrastructure/config/feature_flags.py` | 273-283 | `def should_use_mock_services()` | **Uncertain / possibly dead** | Defined with docstring + env var `USE_MOCK_SERVICES`, but grep shows **zero consumers** in code. Only reference outside the definition is line 424 in the same file (flag summary dict). May be a reserved flag for future use. |
| `services/integrations/slack/tests/test_slack_config.py` | many | test fixture mocks | **Legitimate (test)** | Tests living inside services/ tree by convention. |
| `services/integrations/slack/tests/test_workflow_integration.py` | many | test fixture mocks | **Legitimate (test)** | Same. |
| `services/integrations/slack/tests/script_attention_scenarios_validation.py` | many | test fixture mocks | **Legitimate (test)** | Same. |
| `services/integrations/slack/tests/test_spatial_workflow_factory.py` | many | test fixture mocks | **Legitimate (test)** | Same. |
| `services/integrations/slack/tests/test_spatial_integration.py` | many | test fixture mocks | **Legitimate (test)** | Same. |
| `services/integrations/slack/tests/test_spatial_system_integration.py` | many | test fixture mocks | **Legitimate (test)** | Same. |
| `services/integrations/slack/tests/test_workflow_pipeline_integration.py` | many | test fixture mocks | **Legitimate (test)** | Same. |

**Tally**: 11 Legitimate, 1 Uncertain, 0 Dead code, 0 Test-leakage.

### Findings (`mock_` section)

- **No test-leakage into production code.** The 7 Slack test files use `services/integrations/slack/tests/` — a known convention where integration test fixtures live alongside the code they test. Not leakage; this is a directory-structure question, not a code-quality question.
- **No dead mock code.** All 4 debug/factory mock references are part of actively-used DI or replay infrastructure.
- **One uncertain finding** worth PM's attention: `FeatureFlags.should_use_mock_services()` is defined but never consumed. Options:
  1. Remove it (dead flag)
  2. Keep it (reserved for future e.g. `USE_MOCK_SERVICES=true` override in dev containers)
  3. Document it in the feature-flags registry if that exists
- **PM's "mocks scare me" framing did not find anything to fear** in the `mock_` hits. The mock naming is doing its job — anywhere you see `mock_` it's clearly mock infrastructure, not surprise real mocks.

---

## Part 2 — `fallback` hits (76 files, directory-level bucketing)

Distribution by top-level directory under `services/`:

| Directory | Files | Representative pattern | Initial bucket |
|-----------|-------|------------------------|----------------|
| `intent_service/` | 9 | Progressive parse fallback (classifier, llm_classifier), error-fallback messages in conversational_floor (#940 work) | **Legitimate** (graceful degradation) |
| `integrations/slack/` | 4 | Adapter fallback paths | **Legitimate** (spot-checked) |
| `integrations/github/` | 4 | GitHub API error fallbacks | **Legitimate** (spot-checked) |
| `ui_messages/` | 3 | Default/fallback message templates | **Legitimate** (spot-checked) |
| `trust/` | 3 | Trust-graduation fallback defaults | **Legitimate** (spot-checked) |
| `queries/` | 3 | Query handler fallbacks | **Legitimate** (spot-checked) |
| `orchestration/` | 3 | Orchestration retry paths | **Legitimate** (spot-checked) |
| `mcp/consumer/` | 3 | MCP consumer fallback | **Uncertain** (new subsystem, not deeply inspected) |
| `features/` | 3 | Feature fallback defaults | **Legitimate** (spot-checked) |
| `auth/` | 3 | Auth fallback paths | **Legitimate** (spot-checked) — sensitive; PM + Sec review if edited |
| `slot_filling/` | 2 | Slot inference fallback | **Legitimate** (spot-checked) |
| `llm/` | 2 | LLM provider fallback | **Legitimate** (active after #971/#979) |
| `knowledge_graph/` | 2 | KG query fallback | **Legitimate** (spot-checked) |
| `integrations/calendar/` | 2 | Calendar data fallback | **Legitimate** (spot-checked) |
| `infrastructure/` | 2 | Infrastructure config defaults | **Legitimate** (spot-checked) |
| `domain/` | 2 | Domain model defaults | **Legitimate** (spot-checked) |
| `publishing/` | 1 | Publisher retry — **explicit non-goal** per issue | **Legitimate** (out of scope to touch) |
| `database/` | 1 | Redis → DB fallback | **Legitimate** (architectural decision) |
| `configuration/` | 1 | Config loader fallbacks | **Legitimate** (spot-checked) |
| ...smaller dirs... | ~15 | various | Mostly **Legitimate**, representative samples checked |

### Specific flags worth PM attention

1. **`services/intent_service/classifier.py:132`** and **`services/intent_service/llm_classifier.py:78`** — both have a `ServiceContainer()` fallback with the comment *"This fallback will be removed when horizontal scaling is enabled"* (Issue #322 - ARCH-FIX-SINGLETON). These are documented deprecations, **not** MOCK-SWEEP scope. If #322 is still tracked, this is a follow-up there, not here.

2. **`services/mcp/consumer/`** — 3 files with fallback patterns in what looks like a newer subsystem I haven't worked in. Worth a targeted look by whoever owns the MCP consumer (Architect?) before accepting these as "Legitimate." Flagging as uncertain.

3. **`services/publishing/publisher.py`** — issue explicitly lists `services/publishing/` retry logic as out-of-scope without PM sign-off. Confirmed: `publisher.py:102` is a publisher fallback. Not touching.

4. **`services/auth/`** — 3 fallback files in authentication. Security-adjacent; any change here needs PM + whoever owns auth.

---

## Follow-Up Recommendations (for PM)

Ordered by effort / risk:

### Low-effort, low-risk
1. **Decide on `should_use_mock_services()` feature flag** (feature_flags.py:273). Either remove it or document it as reserved. Can be done in a single PR.

### Medium-effort, coordination required
2. **Close the #322 ServiceContainer fallback** when horizontal scaling lands. Track in #322's own closure, not here.

3. **Targeted review of `services/mcp/consumer/` fallback paths** — hand to Architect to confirm these are legitimate for the MCP subsystem.

### High-effort, out of scope for #997
4. **Full audit of the 494 line-level hits** — would require line-by-line review. Ahead of this work I'd want PM input on whether the current pattern-level categorization satisfies #997's AC or whether true line-by-line rigor is required. I can do the deeper pass as a follow-up session if PM wants.

---

## What I'm NOT Recommending

- **Do not bulk-delete anything based on this first pass.** The report is a decision surface, not an action plan. Every "Legitimate" call here has been validated by spot-check or pattern-recognition, not by exhaustive per-line analysis.
- **Do not treat this as #997's closure.** The issue's AC calls for rigorous line-by-line categorization + deletions where warranted. This first pass is necessary groundwork but not sufficient closure.

---

## Tally Summary

| Bucket | `mock_` files | `fallback` files (directory-level estimate) | Total |
|--------|---------------|---------------------------------------------|-------|
| Legitimate | 11 | ~69 | ~80 |
| Dead code | 0 | 0 | 0 |
| Test-leakage | 0 | 0 | 0 |
| Uncertain | 1 | ~3 (mcp/consumer + possibly a few in auth) | ~4 |

**Headline**: the 86-file list is dominated by legitimate graceful-degradation patterns. No genuine test-leakage found. One confirmed uncertain case (`should_use_mock_services()` feature flag), a few worth closer look (`mcp/consumer/`, `auth/`), and two documented deprecations tied to separate issues (#322).

---

## Next Step (awaiting PM decision)

One of:
- **A**: Accept pattern-level categorization, bucket the known-Uncertain cases, close #997 with no deletions
- **B**: Do the full line-by-line pass in a follow-up session
- **C**: Act on the low-effort recommendation (`should_use_mock_services()`) in a targeted PR and close rest as "no action needed"

I'll wait for direction before proceeding.
