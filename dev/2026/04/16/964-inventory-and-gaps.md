# #964 Ethics Verification — Inventory + Gap Analysis

**Date**: 2026-04-16
**Phases**: 1 (pre-ADR-060 inventory) + 2 (current inventory) + 3 (gap analysis)

---

## Executive Finding (Surfaced Early)

**The premise of #964 — that routing inversion changed the ethics surface — is partially inaccurate.** Ethics enforcement has been at the service layer (IntentService) since October 2025 (#197 Phase 2D), which predates ADR-060 (March 2026). Routing inversion didn't change *where* ethics fires (pre-routing, universal entry point) — it changed *what gets generated downstream* (free-form LLM output vs. deterministic handler response).

The real gaps aren't "pre vs post ADR-060." They are:

1. **`ENABLE_ETHICS_ENFORCEMENT` defaults to `false`**, is not set anywhere in the repo's config/env files. So the BoundaryEnforcer currently **runs on no production traffic**. Identified immediately on reading `services/intent/intent_service.py:627`.
2. **Floor LLM responses have no post-generation boundary check**. The prompt has prohibitions + fabrication guard, but there's no programmatic enforcement that catches violations in the LLM output.
3. **Classifier factory still has `boundary_enforcer=None`** (#690, unresolved).

These are real, current concerns — worth the verification work even though the premise was off.

---

## Pre-ADR-060 Inventory (Phase 1)

The "pre-ADR-060 architecture" in #964 refers to the state before March 2026. But the ethics architecture at that time was already the *post-#197-Phase-2D* design (October 2025). Here's what was in place:

### 1. Service-layer `BoundaryEnforcer` (#197 Phase 2D, October 2025)

| Attribute | Value |
|-----------|-------|
| Location | `services/ethics/boundary_enforcer_refactored.py` |
| Entry point | `BoundaryEnforcer.enforce_boundaries(message, session_id, context)` |
| Called from | `services/intent/intent_service.py:631` (inside `_process_intent_internal`) |
| Gate | `if ethics_enabled:` where `ethics_enabled = os.getenv("ENABLE_ETHICS_ENFORCEMENT", "false").lower() == "true"` |
| Default state | **OFF** (no env file sets it) |
| What it checks | Harassment patterns, professional boundaries, inappropriate content — **pattern matching on user message** |
| Failure mode | Blocks request with "Request blocked due to ethics policy: {explanation}"; returns structured IntentProcessingResult with `blocked_by_ethics: True` |
| Monitoring | `services/infrastructure/monitoring/ethics_metrics.py`, `services/ethics/audit_transparency.py` |

Pattern lists visible in source (`boundary_enforcer_refactored.py:93-128`):
- **Harassment**: harass, harassment, bully, bullying, intimidate, threaten, inappropriate, unwanted, uncomfortable, offensive
- **Professional boundary**: personal, private, relationship, romantic, dating, family, home, personal life, private life
- **Inappropriate content**: explicit, sexual, violent, hate speech, discrimination, racist, sexist, homophobic, transphobic

### 2. Adaptive boundary learning (PM-087)

| Attribute | Value |
|-----------|-------|
| Location | `services/ethics/adaptive_boundaries.py` |
| Role | Learns from confirmed violations; adjusts confidence scores on the pattern check |
| Called from | Inside `BoundaryEnforcer.enforce_boundaries` — part of the flow when ethics is enabled |
| Status | Active when ethics-enabled; dormant when flag is off |

### 3. Audit transparency (`audit_transparency.py`)

| Attribute | Value |
|-----------|-------|
| Location | `services/ethics/audit_transparency.py` |
| Role | Logs ethical decisions for future review |
| Called from | Inside `BoundaryEnforcer.enforce_boundaries` |
| Status | Records decisions only when ethics check fires; dormant when flag is off |

### 4. HTTP-layer middleware (**DEPRECATED**, never activated)

| Attribute | Value |
|-----------|-------|
| Location | `services/api/middleware.py:87` (`EthicsBoundaryMiddleware`) |
| Status | Deprecated per #197 Phase 2D (Oct 2025) — "**Never activated, safe to remove in future cleanup**" |
| Why deprecated | HTTP middleware only covers web API (30-40% coverage); bypasses CLI, Slack webhooks, direct service calls. Violates ADR-029 (domain service mediation). |
| Should we care? | Only to remove it. Has no current enforcement role. |

### 5. Classifier factory `BoundaryEnforcer` hook (#690, **not wired**)

| Attribute | Value |
|-----------|-------|
| Location | `services/intent_service/llm_classifier_factory.py:55` |
| Current state | `boundary_enforcer=None,  # TODO: Wire BoundaryEnforcer when available` |
| Status | Tracked by #690 WIRE-BOUNDARY (still OPEN) |
| Effect today | Classifier never consults BoundaryEnforcer, independent of whether `ENABLE_ETHICS_ENFORCEMENT` is set |

### 6. Handler-layer ethics gates (**searched, not found**)

Checked `services/intent_service/canonical_handlers.py` current state and #963-deleted code (commit a7516fb6). The 26 methods deleted in #963 were **IDENTITY/DISCOVERY/MEMORY/TRUST response-formatters** (format_discovery_standard, handle_identity_query, etc.) — none carried boundary enforcement logic. The handler layer was response-building, not gating.

**There was no "per-service strictness level" enforcement in the handler layer** that the #964 Context paragraph implied. That framing appears to describe an architectural intention that was never implemented at that layer — the actual enforcement lived (and still lives) at the service entry point via `intent_service.py`.

### 7. Trust services (orthogonal to ethics)

| Attribute | Value |
|-----------|-------|
| Location | `services/trust/` (trust_computation_service, proactivity_gate, delegation, etc.) |
| Role | Trust gradient for *proactivity* calibration (PDR-004 Principle 2 / Vision V2 Trust-Graduated Experience) |
| Not an ethics mechanism | Trust stages gate how proactive Piper is, not whether a request is ethical |
| Used by | Greeting/response personalization, not boundary enforcement |

**Not in scope** for #964's ethics inventory, but worth noting so we don't confuse trust gates with ethics gates.

### 8. Knowledge graph ethics integration (minor)

`services/knowledge/knowledge_graph_service.py:14` imports `BoundaryEnforcer`. This is for content validation of knowledge graph entries, not user-request enforcement. Separate concern.

---

## Current Inventory (Phase 2)

The current (post-ADR-060, post-#950) enforcement architecture **is substantially the same** as the pre-ADR-060 state. What changed:

### A. Service-layer `BoundaryEnforcer` — unchanged
Same as pre-ADR-060. Still at `intent_service.py:631`, still gated by `ENABLE_ETHICS_ENFORCEMENT=false`, still doing pattern-based input screening.

### B. Floor system prompt prohibitions — **new, added by ADR-060 + #950**
`services/intent_service/conversational_floor.py:FLOOR_SYSTEM_PROMPT_ADDENDUM` (v2 post-#950, commit d9f9b3f2):

| Mechanism | What it enforces | How |
|-----------|------------------|-----|
| 7 prohibitions | No self-intro, no capability-listing, no "set up" offers, no unsure promises, no generic prompts, no chatbot warmth phrases, no instruction-parroting | Prompt-level instruction to LLM |
| #960 fabrication guard | Never invent user data (todos, projects, issues, calendar events, etc.) unless explicitly present in context | Prompt-level with explicit fallback directive |
| Context-usage directive (#950 iter 2) | Do not produce responses that could apply to any user; if unanchored, ask a concrete question | Prompt-level |
| PDR-004 Principle 4 voice guidance | Never say "I can't"; always engage; ethical boundary = professional decline | Encoded through prompt design, not a separate enforcement |

### C. Floor response pipeline — existing instrumentation, no programmatic content check
`conversational_floor.py:ConversationalFloor.respond` — catches LLM errors via `_classify_llm_error`, logs floor hits, but does NOT inspect the generated response content for boundary violations.

### D. Fabrication guard verification — done manually via canonical retest

`#960` guard is verified through canonical retest queries like "what todos do I have?" — confirms the LLM says "I don't see..." with empty context. **Not enforced programmatically** — enforced through prompt discipline + manual testing.

### E. Deprecated middleware — still present, still never activated
`EthicsBoundaryMiddleware` still exists in `services/api/middleware.py`. Not wired into app; deletion pending.

### F. Classifier factory hook — still None
`llm_classifier_factory.py:55` still has `boundary_enforcer=None`. #690 still open.

---

## Gap Analysis (Phase 3)

### Gap Table

| Enforcement mechanism | Pre-ADR-060 | Current | Gap? | Severity |
|-----------------------|-------------|---------|------|----------|
| Pre-routing message check (BoundaryEnforcer) | Present but disabled by default | Present but disabled by default | **Identical — but both states are "off in production"** | 🔴 High |
| HTTP middleware ethics check | Deprecated, never active | Deprecated, never active, still in codebase | No change | 🟢 Cleanup only |
| Classifier factory boundary hook | None (#690 open) | None (#690 still open) | No change | 🟡 Medium |
| Response-layer content check | **Did not exist** (handlers produced deterministic responses) | **Still does not exist** — floor produces LLM output without post-generation boundary check | **Real gap, new salience** | 🔴 High |
| Fabrication prevention | Handler-layer was deterministic (could not fabricate) | Floor prompt + #960 fabrication guard (prompt-level, not programmatic) | Shifted from "impossible" to "prompt-enforced" | 🟡 Medium — depends on prompt reliability |
| PDR-004 Principle 4 "never say I can't" | N/A (pre-PDR-004 design) | Encoded in prompt; ethical-boundary distinction documented; no programmatic enforcement of the distinction | Policy vs. mechanism mismatch | 🟡 Medium |
| Handler-layer strictness | **Per #964's Context paragraph**, implied to exist; **not found in code**; may have been planned but never built | Same — not present | Nothing to lose; the premise was imprecise | 🟢 No-op |
| Trust-stage gating of proactivity | Present in `services/trust/` | Unchanged | Not ethics, but adjacent | 🟢 N/A |
| Ethics monitoring/metrics | Active when ethics enabled (`ethics_metrics.py`) | Same | No gap | 🟢 OK |

### Severity Notes

**🔴 High: `ENABLE_ETHICS_ENFORCEMENT=false` is the production default.** This is not a regression from ADR-060 — it's been this way since #197 Phase 2D shipped. But any #964 verification without calling this out would be dishonest. The BoundaryEnforcer is essentially a circuit that's been wired but the breaker is off.

**🔴 High: No post-generation content check on floor output.** The prompt + fabrication guard rely on LLM compliance. When compliance fails (which it has — see #960 history, M1 UAT findings), we have no safety net. Pre-ADR-060, handlers were deterministic code — failure modes were bounded. Post-ADR-060, the floor's failure modes are open-ended because the response is LLM-generated.

**🟡 Medium: #690 remains unwired.** Even if `ENABLE_ETHICS_ENFORCEMENT` were true, classifier-layer boundary enforcement is missing. Adds a second enforcement gate closer to the LLM call. Completion would be low-cost.

**🟡 Medium: Prompt-enforced fabrication prevention is a policy without a mechanism.** Trust-graded enforcement — today we verify through canonical retest, manual testing, M1 UAT. That's a process not a product control.

**🟢 Low: Handler-layer strictness** was never present; no loss. We can correct the issue's premise without corrective action.

---

## Cross-Check: PDR-004 Principle 4

PDR-004 Principle 4 (LLM Floor Guarantee) states:

> "**Never say I can't" applies to Piper's conversational capability. It does not override ethical boundaries. When a request crosses an ethical line, Piper declines with professional judgment and tact — like a colleague exercising discretion, not a system returning an error.**
>
> The three response modes are:
> 1. Capability (floor default — always engage)
> 2. Ethical boundary (professional decline with explanation)
> 3. Action limitation (suggest alternatives naturally)

**Current design** has:
- Mode 1 ✅ well-supported (floor default + new prompt)
- Mode 2 ⚠️ partially supported — the floor's safety training from the underlying LLM provides SOME boundary enforcement, but there's no project-level enforcement of mode 2
- Mode 3 ✅ supported (prompt directs "suggest an alternative")

The tension is between mode 1 ("always engage") and mode 2 ("decline with judgment"). The design relies on the LLM correctly distinguishing these. That's a fragile mechanism for edge cases (adversarial inputs, jailbreaks, sensitive topics the LLM's safety training misjudges).

---

## Summary

The verification produced 3 significant findings, 1 correction to #964's framing, and 1 cleanup item:

1. **Finding (high)**: BoundaryEnforcer exists and is wired, but `ENABLE_ETHICS_ENFORCEMENT=false` in production. Effectively OFF.
2. **Finding (high)**: No post-generation content check on floor output — architecturally new gap created by moving to LLM-generated responses. Relies on LLM's own safety training.
3. **Finding (medium)**: #690 WIRE-BOUNDARY still unresolved — second enforcement layer missing.
4. **Correction**: #964's premise that routing inversion changed the ethics surface is partially inaccurate. Ethics has been at service layer since Oct 2025 (#197). Handler-layer strictness was never implemented. The real surface change is *response content*, not *routing*.
5. **Cleanup**: Deprecated `EthicsBoundaryMiddleware` is safe to remove.

Proceeding to Phase 4 (#690 review) and Phase 5 (decision per gap).
