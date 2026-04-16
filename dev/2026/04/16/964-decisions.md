# #964 Phase 4 + 5: #690 Review + Gap Decisions

**Date**: 2026-04-16
**Previous**: Phase 1-3 inventory at `964-inventory-and-gaps.md`

---

## Phase 4: #690 WIRE-BOUNDARY Coverage Review

### #690 Scope (as written)

**Title**: "WIRE-BOUNDARY: Wire BoundaryEnforcer into classifier factory"
**Created**: 2026-01-26, still OPEN
**Body**: 6 lines. Cites TODO at `services/intent_service/llm_classifier_factory.py:55`:
> `boundary_enforcer=None,  # TODO: Wire BoundaryEnforcer when available`

### Actual Scope (after reading the referenced code)

The cited TODO is about injecting `EthicsBoundaryEnforcer` (legacy) into **`KnowledgeGraphService`** — not into the classifier itself. `KnowledgeGraphService.boundary_enforcer` is used for content validation when storing knowledge-graph entries (harassment / inappropriate content patterns). Distinct concern from user-message boundary checking at the IntentService entry point.

From `services/knowledge/knowledge_graph_service.py:32`:
```python
self.boundary_enforcer = boundary_enforcer  # Ethics boundaries (legacy)
```

### #690 Coverage vs Gaps Identified in Phase 3

| Gap | #690 covers? |
|-----|--------------|
| `ENABLE_ETHICS_ENFORCEMENT=false` production default | ❌ No |
| No post-generation floor response content check | ❌ No |
| Deprecated `EthicsBoundaryMiddleware` cleanup | ❌ No |
| Classifier-factory `boundary_enforcer=None` (the TODO cited) | ✅ Yes (this one, via KnowledgeGraphService content validation) |

**#690 is narrow and slightly misnamed.** It addresses KG content validation at classifier construction time, not classifier-layer user-message enforcement. The title creates a false impression that fixing #690 would close the broader boundary-enforcement gap.

### Recommendation for #690

Either:
- **Close #690 as-is** once wired (genuine but narrow fix), with a renaming comment making the scope clear.
- **Rename/retitle** #690 to "WIRE-KG-BOUNDARY-VALIDATION" or similar before completion, to reduce confusion in future audits.

Neither requires pulling other gaps into #690's scope.

---

## Phase 5: Decision Per Gap

Decision key:
- **Re-implement** = File a follow-up issue to close the gap
- **Accept** = Document rationale for leaving it; no further action
- **Defer** = Known gap, lower priority; file follow-up but mark as non-blocking

### Gap 1: `ENABLE_ETHICS_ENFORCEMENT=false` in production

| Field | Value |
|-------|-------|
| **Decision** | **Re-implement** (file follow-up) |
| **Rationale** | BoundaryEnforcer exists and works; it's one env-var flip from active. Current state is inconsistent with PDR-004 Principle 4 Mode 2 (professional decline on ethical boundary) — which implies such enforcement *should* be operating. Before enabling in production, verify: (a) false-positive rate on canonical retest queries, (b) user-facing response shape when a violation triggers (currently "Request blocked due to ethics policy: {explanation}" — unfriendly compared to PDR-004's "decline with professional judgment and tact"). |
| **Not: accept** | Because the framework is built and dormant, "accept" would mean "we have enforcement in code but not in effect" — indefensible from an audit-trail or product-claim perspective. |
| **Not: defer** | Stakes are real; shouldn't sit on a known-off enforcement. But activation requires verification work, so it's a follow-up issue, not an immediate fix. |

### Gap 2: No post-generation floor response content check

| Field | Value |
|-------|-------|
| **Decision** | **Defer** (file follow-up with rationale) |
| **Rationale** | Adding response-layer enforcement is a significant architectural decision. Options range from "trust the LLM + monitor" (current) to "generate → classify → potentially regenerate" (expensive, adds latency). PDR-004 Principle 4 design depends on the LLM's own safety training being sufficient; introducing a second layer needs PM/CXO direction on tradeoffs (latency, cost, false-positive-driven apology spiral). Not a "just do it" fix. |
| **What mitigates this today** | Floor prompt prohibitions + #960 fabrication guard + canonical retest verification + AAXT golden scenarios. Process controls, not code controls. |
| **When to revisit** | Post-alpha when we have real user-incident data. Alpha-stage risk is acceptable given the user base. |

### Gap 3: #690 WIRE-BOUNDARY incomplete

| Field | Value |
|-------|-------|
| **Decision** | **Re-implement** (finish #690, per its existing scope + retitle for clarity) |
| **Rationale** | Small scope, known wiring point, no blocking dependencies. Should be closed. The scope is narrower than the title suggests — retitling before/on close eliminates future confusion. |

### Gap 4: Deprecated `EthicsBoundaryMiddleware` cleanup

| Field | Value |
|-------|-------|
| **Decision** | **Accept** (no immediate action, but file as hygiene issue) |
| **Rationale** | The class comment explicitly says "Never activated, safe to remove in future cleanup." Low urgency because it has no effect (never instantiated in app config). Clean up alongside other deprecation removals. |

### Gap 5: Correction to #964's framing about handler-layer strictness

| Field | Value |
|-------|-------|
| **Decision** | **Accept** (document in the memo) |
| **Rationale** | "Per-service strictness levels" were never implemented in code — the issue's Context paragraph described an architectural framing that didn't match the actual state. No gap to close; verification surfaced the mismatch. The value is ensuring future architecture discussions don't assume this layer exists. |

### Summary Decision Matrix

| Gap | Decision | Action | Priority |
|-----|----------|--------|----------|
| `ENABLE_ETHICS_ENFORCEMENT=false` default | Re-implement | File follow-up: activate + validate + reshape response | P1 |
| No response content check | Defer | File follow-up: product decision + architectural scoping | P2 |
| #690 incomplete | Re-implement | Finish #690 + retitle | P3 |
| Deprecated middleware | Accept | File cleanup issue | P4 |
| Handler-strictness premise | Accept | Document in memo | N/A |

Total follow-ups to file: **4** (gaps 1-4). One memo addresses gap 5.

---

## Next Phases

- Phase 6: write findings memo to PM + CXO (cc PA) folding Phases 1-5
- Phase 7: file the 4 follow-up issues; update #964 description; close
