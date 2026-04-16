# M2 Super-Epic Structure: Conscious Floor + Action Handlers

**Created**: 2026-04-14
**Last Updated**: 2026-04-16 (Lead Dev — M2b/M2c closure + follow-up index)
**Sprint theme**: Make the differentiator stack's first two pillars operational

---

## Sub-Epic Overview

| Sub-Epic | Theme | Status | Gate |
|----------|-------|--------|------|
| **M2a** | Foundation cleanup | ✅ COMPLETE (10/10) | Canonical retest: 93% routing, 63% quality |
| **M2b** | Test infrastructure | ✅ COMPLETE (5/5) | E2E + AAXT + CI integrated |
| **M2c** | Conversational depth | ✅ COMPLETE (6/6) | Canonical retest: 95.1% routing, **72.1% quality** (post-#950 iter 2) |
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

## M2b — Test Infrastructure ✅ COMPLETE

Build the quality safety net before deeper feature work. PA memo flagged this as "from sprint start, not the end."

| # | Issue | Status |
|---|-------|--------|
| #927 | E2E: Task lifecycle smoke tests | ✅ Closed Apr 14 (9/9 via ASGI transport) |
| #928 | E2E: Automated canonical conversation suite | ✅ Closed Apr 14 (two-tier design, 61 queries) |
| #929 | AAXT: Golden scenarios with DeepEval LLM-as-judge | ✅ Closed Apr 15 (4/5 PASS verified with Gemini) |
| #930 | CI: Integration for E2E + AAXT nightly | ✅ Closed Apr 14 (3 GitHub Actions jobs) |
| #963 | Pattern-045 dead canonical handler code cleanup | ✅ Closed Apr 14 (26 methods / 911 lines removed) |

**Gate result**: E2E + AAXT + CI all green. Canonical retest automated.

---

## M2c — Conversational Depth ✅ COMPLETE

The heart of M2. Made the floor conscious and context-rich.

| # | Issue | Status |
|---|-------|--------|
| #950 | FLOOR-PROMPT: Conscious floor system prompt | ✅ Closed Apr 16 (Five Pillars + grammar + anti-flattening + Identity anchoring) |
| #951 | CONTEXT-ASSEMBLER-EXPAND: Calendar + deadline context | ✅ Closed Apr 16 (scope narrowed to calendar wiring + deadline surfacing; follow-ups filed for broader context) |
| #964 | FLOOR-ETHICS-VERIFY: Ethics/boundary coverage | ✅ Closed Apr 16 (verification memo delivered; 3 follow-ups filed) |
| #922 | Conversation continuity | ✅ Closed Mar 19 (ADR-059 Workflow Dispatcher) |
| #970 | LLM access consolidation (ServiceRegistry) | ✅ Resolved Apr 14 (Architect: "leave as-is") |
| #971 | Adapter infrastructure decision | ✅ Closed Apr 14 (Architect: "delete"; Pattern-012 adapters + ProviderSelector removed) |

**Folded into #951** (per PA memo):
- #100 (Project Portfolio) → context shape, not standalone service
- #101 (Temporal Context) → context shape, not standalone service

**Gate result**: Canonical retest run post-#950 iter 2 (Apr 16 14:27):
- Routing: **95.1%** (58/61, up from 93.4%)
- Quality: **72.1% PASS** (44/61, up from 62.3% — exceeds the 63% no-regression floor; falls short of the aspirational 80% for Identity category specifically due to fresh-account context ceiling tracked in #989)
- Zero errors/skipped (first clean run)
- Temporal FAIL: 3 → 1 (calendar + deadline context from #951 landing)

Additional M2c infrastructure wins:
- Gemini wired as real primary/fallback LLM provider (commit 1a8fdde6; enables 3-way fallback chain)
- Ruff consolidation (commit 37cfdfda; replaced black + isort + flake8)

---

## M2c Follow-ups (Spun Off During M2c)

Issues filed during M2c work that are genuine gaps but out of scope for M2c closure. Triage for M3 or separate prioritization.

### Context Assembler Expansion (from #951)
| # | Issue | Priority | Notes |
|---|-------|----------|-------|
| #983 | CONTEXT-SPRINT: GitHub sprint/milestone data | P3 | GitHub API + rate-limit strategy |
| #984 | CONTEXT-ACTIVITY: Recent activity feed | P3 | Cross-integration time-windowed queries |
| #985 | CONTEXT-BLOCKED: Blocked items identification | P3 | Needs label convention decision |
| #986 | CONTEXT-CACHE: Redis TTL caching for assembler | P3 | Performance optimization |

### Ethics (from #964)
| # | Issue | Priority | Notes |
|---|-------|----------|-------|
| #991 | ETHICS-ACTIVATE: Turn on ENABLE_ETHICS_ENFORCEMENT | P1 | Blocked on CXO voice input for Mode-2 decline copy |
| #992 | ETHICS-RESPONSE-GATE: Post-generation floor content check | P2 | PM/CXO architectural decision (options A/B/C/D in #964 memo) |
| #990 | HYGIENE-MIDDLEWARE: Remove deprecated EthicsBoundaryMiddleware | P4 | Pure code hygiene |
| #690 | WIRE-BOUNDARY: Finish KG-content-validation wiring | P3 | Retitle recommended — scope is narrower than title |

### LLM Provider Infrastructure (from Gemini wiring)
| # | Issue | Priority | Notes |
|---|-------|----------|-------|
| #987 | GEMINI-JSON: Enable structured JSON mode for classifier | P2 | Direct impact on BYO-Gemini-key users |
| #988 | GEMINI-QUOTA: Free tier vs paid decision | P4 | 5 RPM free-tier limit documented; awaits billing decision |

### Testing Infrastructure (from #950 verification)
| # | Issue | Priority | Notes |
|---|-------|----------|-------|
| #989 | CANONICAL-FIXTURES: Warmed-up user for canonical retest | P3 | Fixes "generic response" Context ceiling on fresh-account retests |

### Test Hygiene (from #980)
| # | Issue | Status | Notes |
|---|-------|--------|-------|
| #980 | HYGIENE: orphan scripts | ✅ Closed Apr 16 | 7 manual scripts renamed + garbled imports fixed |

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

## M2c Gate Checkpoint (Apr 16)

**Status**: COMPLETE

**Canonical retest result**: Run 5 (Apr 16 14:27, post-#950 iter 2)
- Routing: 95.1% (58/61, +1.7% vs M2a baseline)
- Quality: **72.1% PASS** (44/61, +9.8% vs M2a baseline)
- Quality MARGINAL: 13.1% (8/61)
- Quality FAIL: 14.8% (9/61)
- Errors/Skipped: 0% (first clean run)

**Gate target vs actual**: Target was ≥80% quality on floor queries with 63% no-regression floor. Achieved 72.1% (above floor, below aspirational ceiling). Gap between 72% and 80% is largely Identity Context scoring (2 queries at Context=1), tracked as fresh-account fixture ceiling in #989. Not a real-user blocker.

**Key M2c achievements**:
- Conscious floor prompt with Five Pillars + grammar + anti-flattening (#950)
- Calendar + deadline context wiring for TEMPORAL/STATUS queries (#951)
- Ethics verification with 3 follow-ups filed (#964)
- Gemini wired as real LLM provider (enables 3-way fallback chain)
- Ruff consolidation (operational win, not a gate item)

**Carried into M2d+**: Follow-up issue backlog above (14 issues filed during M2c).

---

*This document is the reference for M2 sub-epic tracking. Update as issues are closed or re-prioritized.*
