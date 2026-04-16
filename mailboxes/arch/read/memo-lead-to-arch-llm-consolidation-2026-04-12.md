---
from: Lead Developer
to: Chief Architect
cc: PM, CXO
date: 2026-04-12
subject: Seeking guidance — LLM access consolidation and adapter infrastructure decisions
priority: medium
response-requested: yes
---

# LLM Architecture: Two Decisions Need Your Input

Architect — during M2a foundation cleanup we decomposed #947 (dual LLM systems) into three phases. Phase 1 (unified config) is done. Phases 2 and 3 need your architectural guidance before we proceed.

## Context

The codebase has two parallel LLM systems:

1. **LLMClient** (`services/llm/clients.py`) — the workhorse. 18 files import it directly. Handles provider selection, fallback, error classification. Used by the conversational floor, intent classifier, orchestration engine, and most application code.

2. **LLMDomainService** + **LLM Adapters** (`services/domain/llm_domain_service.py`, `services/llm/adapters/`) — a wrapper layer initialized through ServiceRegistry. `complete()` delegates directly to LLMClient (thin wrapper + optional usage logging). The Pattern-012 adapters (ClaudeAdapter, OpenAIAdapter, GeminiAdapter, PerplexityAdapter) are created at startup but **never called** by the standard `complete()` flow. `ProviderSelector` is instantiated but also never called at runtime.

Phase 1 (commit 5f68f613) unified the model config so both systems read from `PROVIDER_MODELS` in `config.py`. The config drift bug from M1 UAT is fixed.

## Decision 1: ServiceRegistry as primary LLM access (#970)

**Question**: Should we rewire the 5-8 top-level callers (IntentService, ConversationalFloor, OrchestrationEngine) to access the LLM through `ServiceRegistry.get("llm")` instead of importing the global `llm_client` singleton?

**Why this matters now**: Your MCPB review (Apr 10) flagged that the context assembler should be built with MCP Resource provider interfaces in mind. If MCPB packaging in M5 requires a different LLM access pattern (e.g., LLM-as-tool via MCP rather than direct import), rewiring to ServiceRegistry now may or may not be the right intermediate step. We don't want to rewire 18 files to ServiceRegistry only to rewire them again for MCPB.

**Options**:
- (A) Rewire to ServiceRegistry now (4-6 hours). Clean intermediate step.
- (B) Skip ServiceRegistry, plan the MCPB-compatible interface first, then rewire once to the final pattern. More efficient if M5 interface is substantially different.
- (C) Leave as-is. The global singleton works fine functionally. Rewire when there's a concrete reason.

**My lean**: (C) unless you see a concrete benefit to (A) for MCPB preparation. The singleton works, and premature abstraction was one of the M1 anti-patterns we identified.

## Decision 2: Keep, absorb, or delete Pattern-012 adapters (#971)

**Question**: The LLMFactory creates adapters (ClaudeAdapter, OpenAIAdapter, etc.) at startup, but `LLMDomainService.complete()` never uses them — it delegates directly to LLMClient which has its own `_anthropic_complete()` / `_openai_complete()` methods. The adapters are effectively dead code on the hot path.

However, your MCPB review noted adapters as potentially useful for MCP packaging. Is there a concrete path from these adapters to MCPB distribution?

**Options**:
- (A) Keep adapters. They become MCP Resource handlers in M5. Worth maintaining.
- (B) Absorb into LLMClient. Refactor `_call_provider()` to use adapters internally, eliminating duplicate provider-specific code. 6-10 hours, medium risk.
- (C) Delete adapters and LLMFactory. LLMClient's direct implementation is proven in production across 5 UAT rounds. 2-3 hours, low risk. But loses the infrastructure if M5 needs it.

**My lean**: (C) with a caveat — if you tell me there's a concrete M5 reuse path, I'd switch to (A). The "keep dead code for a future sprint" pattern is exactly what #962 (inversion sweep) is designed to catch, so I want to be honest about whether this infrastructure earns its place.

## Related context

- **ProviderSelector**: Also instantiated but never called. Does task-specific routing (general→OpenAI, research→Gemini). Has this been superseded by the provider-agnostic approach (#940), or should it be revived? CXO input may be relevant here.
- **Issue #970** (Phase 2): Filed with "needs Architect input" tag
- **Issue #971** (Phase 3): Filed with "needs Architect + CXO input" tag
- **M2a Group 3**: #960 (floor guardrails), #961 (route audit), #962 (inversion sweep), #925 (STATUS/PRIORITY floor migration) — these proceed independently regardless of your guidance on Phases 2-3.

No urgency — these decisions don't block current M2a work. But your input before M2b starts would help us avoid unnecessary churn.

— Lead Dev
