# M2 Super-Epic Structure: Conscious Floor + Action Handlers

**Created**: 2026-04-14
**Last Updated**: 2026-04-14
**Sprint theme**: Make the differentiator stack's first two pillars operational

---

## Sub-Epic Overview

| Sub-Epic | Theme | Status | Gate |
|----------|-------|--------|------|
| **M2a** | Foundation cleanup | ✅ COMPLETE (10/10) | Canonical retest: 93% routing, 63% quality |
| **M2b** | Test infrastructure | Not started | E2E + AAXT running, CI integrated |
| **M2c** | Conversational depth | Not started | Conversational quality ≥80% on floor queries |
| **M2d** | MUX lifecycle | Not started | Experience requirements documented |
| **M2e** | Integrations | Not started | Integration smoke tests pass |
| **M2f** | Security + infra | Not started | May defer to M3/M5 |

---

## M2a — Foundation Cleanup ✅ COMPLETE

Closed M1 debt, established quality baseline, unblocked everything else.

| # | Issue | Status |
|---|-------|--------|
| #949 | Server restart reliability | ✅ Closed Apr 11 |
| #965 | Temporal quality → floor migration | ✅ Closed Apr 12 |
| #968 | Routing reconciliation | ✅ Closed Apr 12 |
| #969 | GitHub adapter bugs | ✅ Closed Apr 12 |
| #946 | Stale keychain consent | ✅ Closed Apr 12 |
| #947 | Dual LLM systems (Phase 1) | ✅ Closed Apr 12 |
| #962 | Inversion sweep | ✅ Closed Apr 12 |
| #925 | STATUS/PRIORITY floor-first | ✅ Closed Apr 13 |
| #960 | Floor guardrails (deeper) | ✅ Closed Apr 14 |
| #961 | Floor route audit | ✅ Closed Apr 14 |

**Gate result**: Canonical retest Run 3 (Apr 13): 93.4% routing, 62.3% quality.

---

## M2b — Test Infrastructure

Build the quality safety net before deeper feature work. PA memo flagged this as "from sprint start, not the end."

| # | Issue | Notes |
|---|-------|-------|
| #927 | E2E: Task lifecycle smoke tests | Through /api/v1/intent |
| #928 | E2E: Automated canonical conversation suite | Builds on canonical retest runner |
| #929 | AAXT: Golden scenarios with DeepEval LLM-as-judge | Quality regression detection |
| #930 | CI: Integration for E2E + AAXT nightly | Automated runs |
| #963 | Pattern-045 dead canonical handler code cleanup | Remaining dead code from floor migrations |

**Gate**: E2E + AAXT running in CI, canonical retest automated.

---

## M2c — Conversational Depth

The heart of M2. Make the floor conscious and context-rich.

| # | Issue | Notes |
|---|-------|-------|
| #950 | FLOOR-PROMPT: Conscious floor system prompt | Five Pillars + grammar. CXO reviews at start. |
| #951 | CONTEXT-ASSEMBLER-EXPAND: Context for all floor categories | Data source scoping needed (PA + PPM + Architect) |
| #964 | FLOOR-ETHICS-VERIFY: Ethics/boundary coverage in floor pipeline | Verify floor matches pre-ADR-060 enforcement |
| #922 | Conversation continuity (#922) | "OK" affirmation handling — M1 carryover |
| #970 | LLM access consolidation (ServiceRegistry) | Needs Architect input |
| #971 | Adapter infrastructure decision | Needs Architect + CXO input |

**Folded into #951** (per PA memo):
- #100 (Project Portfolio) → context shape, not standalone service
- #101 (Temporal Context) → context shape, not standalone service

**Gate**: Conversational quality ≥80% on floor-routed queries. No-regression on current 63% baseline.

---

## M2d — MUX Lifecycle

Wire lifecycle visibility into user-facing displays. Scope revised to be implementation-agnostic (CXO recommendation).

| # | Issue | Notes |
|---|-------|-------|
| #703 | MUX-LIFECYCLE-UI: Lifecycle indicator integration | Reframed as experience requirements |
| #707 | MUX-INSIGHT-SURFACING: Insight surfacing rules | |
| #714 | MUX-LISTS-LIFECYCLE-UI: Wire lifecycle to lists | |
| #869 | Project configuration IA | Project Detail as primary, Settings as overview |

**Gate**: Experience requirements documented and verified on at least one rendering surface.

---

## M2e — Integrations

Activate and wire the integration handlers.

| # | Issue | Notes |
|---|-------|-------|
| #790 | Trust-gated calendar integration | |
| #900 | Standup 3-part structural collection | |
| #864 | Pre-classifier patterns for milestones/labels/releases | |
| #948 | Server orphaned processes (#949 follow-up) | |

**Note**: Several WIRE-* issues from the original M2 list (#690-695) may be partially superseded by floor migration. Needs triage.

**Gate**: Integration smoke tests pass for configured integrations.

---

## M2f — Security + Infrastructure

May defer to M3 or M5 depending on prioritization.

| # | Issue | Notes |
|---|-------|-------|
| #933 | SEC: API key validation re-enable | No re-enable plan |
| #932 | SEC: HIBP integration stub | Returns false safe result |
| #936 | UserService in-memory dicts | Data lost on restart |
| #935 | BudgetManager/APIUsageTracker no persistence | |
| #921 | FastAPI/Starlette/httpx upgrade | Dependency conflicts |
| #857 | Token refresh mechanism | Session continuity |

**Gate**: Deferred items explicitly documented with PM disposition.

---

## Sub-Epic Gating Protocol

Per CXO + PPM guidance (Apr 11 memos):

1. **Per-sub-epic quality gates**: Each sub-epic defines which canonical queries it affects. Those queries must reach quality threshold (7+ Colleague Test) to close.
2. **No-regression rule**: Any query that currently passes cannot regress without a filed issue and PM disposition.
3. **Aggregate target**: M2 closes with ≥75% quality PASS (north star, not hard gate).
4. **Quality thresholds by type** (PPM):
   - Conversational depth: ≥80% quality PASS
   - Action handlers: ≥90% quality PASS
   - General floor: track trajectory, tolerate marginal early

---

## M2a Gate Checkpoint (Apr 14)

**Status**: COMPLETE

**Canonical retest baseline**: Run 3 (Apr 13)
- Routing: 93.4% (57/61)
- Quality: 62.3% (38/61 PASS)
- Quality MARGINAL: 16.4% (10/61)
- Quality FAIL: 16.4% (10/61)

**Key M2a achievements**:
- Floor inversion complete for all read-only categories (IDENTITY, DISCOVERY, TRUST, MEMORY, TEMPORAL, STATUS, PRIORITY, CONVERSATION non-greeting, UNKNOWN)
- Context assembly for all floor-routed categories
- Fabrication guardrails (system prompt + context contract + violation logging)
- Server restart reliability (#949)
- Stale keychain consent fix (#946)
- LLM config unification (#947 Phase 1)
- Inversion sweep complete (#962)

**Carried into M2b+**: #970 (ServiceRegistry, needs Architect), #971 (adapter decision, needs Architect+CXO), known_pathological test category.

---

*This document is the reference for M2 sub-epic tracking. Update as issues are closed or re-prioritized.*
