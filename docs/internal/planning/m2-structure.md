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
| #992 | ETHICS-ACTIVATE: Turn on ENABLE_ETHICS_ENFORCEMENT | P1 | CXO voice guidance received 2026-04-16; ready for implementation |
| #991 | ETHICS-RESPONSE-GATE: Post-generation floor content check | P2 | PM/CXO architectural decision (options A/B/C/D in #964 memo) |
| #990 | HYGIENE-MIDDLEWARE: Remove deprecated EthicsBoundaryMiddleware | P4 | Pure code hygiene |
| #690 | WIRE-BOUNDARY: Finish KG-content-validation wiring | P3 | Retitle recommended — scope is narrower than title |

### LLM Provider Infrastructure (from Gemini wiring)
| # | Issue | Priority | Notes |
|---|-------|----------|-------|
| #988 | GEMINI-JSON: Enable structured JSON mode for classifier | ✅ Closed Apr 16 | response_mime_type wired + classifier passes response_format |
| #987 | GEMINI-QUOTA: Free tier vs paid decision | P4 | 5 RPM free-tier limit documented; awaits billing decision |

### Testing Infrastructure (from #950 verification)
| # | Issue | Priority | Notes |
|---|-------|----------|-------|
| #989 | CANONICAL-FIXTURES: Warmed-up user for canonical retest | P3 | Fixes "generic response" Context ceiling on fresh-account retests |
| #993 | TEST-PATHOLOGICAL-TAGS: expected-pass vs known_pathological tagging | P3 | PPM recommendation 2026-04-16; separates "should work" from "hard problems" |
| #994 | SCORER-VOCABULARY: Adopt AAXT six-failure-mode taxonomy | P3 | Architect + CXO endorsed 2026-04-16; Colleague Test R/C/T unchanged |
| #995 | FABRICATION-PROBES: Standalone 5-10 probe set across 5 absence categories | P3 | Architect directive 2026-04-16; CXO: separate instrument, not rubric dimension |

### Test Hygiene (from #980)
| # | Issue | Status | Notes |
|---|-------|--------|-------|
| #980 | HYGIENE: orphan scripts | ✅ Closed Apr 16 | 7 manual scripts renamed + garbled imports fixed |

---

## M2d — MUX Lifecycle

Wire lifecycle visibility into user-facing displays. Scope revised to be implementation-agnostic (CXO recommendation).

**2026-05-02 audit-cascade restructure** (Lead Dev memo `dev/2026/05/02/m2d-audit-cascade-findings.md`, CEO direction same day): #707 split into 3 child issues per surfacing mode (Pull/Passive/Push); #1033 filed as sibling to #703 covering COMPOSTED-state UX (which would otherwise have silently dropped from MVP); #714 reframed to staleness-spec-first (Lists are non-lifecycle hard objects per `objects-catalog.md`); #869 relocated to M2e (substance is IA, not MUX).

| # | Issue | Notes |
|---|-------|-------|
| #703 | MUX-LIFECYCLE-UI: Lifecycle indicator integration (tracking) | Earlier-state indicators on hard objects via MVP children #704 + #705 |
| #707 | MUX-INSIGHT-SURFACING (tracking parent) | Reframed 2026-05-02 from placeholder; split into 3 child issues |
| #1030 | MUX-INSIGHT-PULL (#707 child) | All-trust-stage; user-initiated query; P2 |
| #1031 | MUX-INSIGHT-PASSIVE (#707 child) | All-trust-stage; Insight Journal navigation; P2 |
| #1032 | MUX-INSIGHT-PUSH (#707 child) | Stage 3+ trust gate; Piper-initiated; P3 (longer-pole within MVP) |
| #714 | MUX-LISTS-STALENESS-UI: staleness display on Lists view | Reframed 2026-05-02; Lists are non-lifecycle; staleness is a separate concept |
| #1033 | MUX-COMPOSTED-EXPERIENCE: COMPOSTED state UX + "filing dreams" framing | Filed 2026-05-02; sibling to #703; covers the back-end-of-lifecycle UX that #703 doesn't |

**Gate**: Experience requirements documented and verified on at least one rendering surface; conceptual integrity preserved (no MUX-flattening — insights are SOFT objects, Lists are non-lifecycle, COMPOSTED has dedicated framing).

### M2d gate criteria — consolidated three-way concurrence (2026-05-10)

Per Architect (May 4) + Lead Dev (May 5) + CXO (May 10) concurrences, consolidated by PPM (May 10 memo: `memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-criteria-consolidated-2026-05-10`):

**Quality-threshold mapping**: M2d is UI integration; canonical-retest quality thresholds (80% conversational / 90% action handlers) do not apply. No-regression rule applies narrowly to any M2d work that modifies floor-routed paths (transition-explanation generation is the most likely candidate; flag pre-gameplan and run canonical retest as a side-check if so).

**Verification protocol**: at per-issue gate-close: (1) PPM signs off on per-issue documentation completeness (audit-cascade gap items closed); (2) fresh-account walkthrough on the rendering surface, applying the **UI Lifecycle Verification Rubric v0.1** (see `docs/internal/testing/ui-lifecycle-verification-rubric-v0.1.md`); (3) conceptual-integrity sign-off from any 2 of {PPM, CXO, Architect} per the §M2d conceptual-integrity checklist below.

**Conceptual-integrity checklist** (any 2 of {PPM, CXO, Architect} sign-off):

```
[ ] Insights treated as SOFT objects: rendered via narrative/contextual surfaces
    (Insight Journal navigation, surfacing prompts), NOT via hard-object lifecycle
    UI (no state-badge chrome, no transition animations between trust-stages).
[ ] Lists treated as non-lifecycle hard objects: staleness display per #714
    spec; no MUX-lifecycle-state rendering applied (no PROBATION, COMPOSTED, etc.
    on Lists view).
[ ] COMPOSTED state UX dedicated: per #1033 "filing dreams" framing; not flattened
    into ARCHIVED or hidden from view; user-recoverable per spec.
[ ] Surfacing modes treated as routing/timing attributes: Pull (#1030),
    Passive (#1031), Push (#1032) are not lifecycle states; mode is set at
    creation per trust-stage rules and not user-mutable post-creation.
[ ] Trust-stage gating active for Push insights: #1032 ships with Stage 3+
    trust gate enforced; Pull (#1030) and Passive (#1031) are all-trust-stage.
[ ] Transition explanations surface when state changes: per
    lifecycle-experience-guide.md "Transition Explanations" table; users
    see "why this object changed state," not just the new state label.
[ ] Surfacing modes (Pull/Passive/Push) treated as routing/timing attributes,
    not lifecycle-style state: no transition animations between modes;
    no "your insight changed surfacing mode" notifications; mode is set at
    creation per trust-stage rules and not user-mutable post-creation.
```

**Applies forward**: criteria are forward-looking from this commit. M2d issues already closed end-of-day May 3 (8 implementation issues shipped) had equivalent function served by the May 2 audit-cascade + May 3 closure work; no retroactive application needed.

---

## M2e — Integrations

Activate and wire the integration handlers.

| # | Issue | Notes |
|---|-------|-------|
| #790 | Trust-gated calendar integration | Audit-cascade ✅ 2026-05-03 |
| #900 | Standup 3-part structural collection | Audit-cascade ✅ 2026-05-03 (LLM-gated completion in MVP per Q2; ~14 hr est) |
| #1042 | PRE-1039: Remove hardcoded `piper-morgan-product` repo default | Pre-work for #1039+#1040 per CEO 2026-05-03 (#1039 Q4) |
| #1039 | INTENT-COVERAGE-A: milestones + releases | Split from #864 2026-05-03; **blocked by #1042** |
| #1040 | INTENT-COVERAGE-B: labels + branches | Split from #864 2026-05-03; ships after #1039 |
| ~~#864~~ | ~~Pre-classifier patterns for milestones/labels/releases/branches~~ | Split into #1039 + #1040 (closed 2026-05-03) |
| ~~#948~~ | ~~Server orphaned processes (#949 follow-up)~~ | ✅ Closed 2026-04-30 |
| #869 | Project configuration IA: Project Detail as primary, Settings as overview | Relocated from M2d 2026-05-02; audit-cascade ✅ 2026-05-03 (2 tabs MVP per Q1) |
| #1041 | M2-WIRE-TRIAGE: WIRE-* #690-695 superseded-by-floor-migration triage | Filed 2026-05-03 per CEO direction; resolves the WIRE-* ambiguity that was previously a footnote |
| #304 | NOTION activation — search-only scope | Phase -1 audit ✅ 2026-05-08 ("close to ready"); CEO+Lead scope disposition 2026-05-13: search-only ships (~5-8 hr; PM-blocked on token provisioning + read smoke); write + Slack-xref deferred demand-gated (see below) |

**Gate**: Integration smoke tests pass for configured integrations.

**Demand-gated NOTION followups (filed 2026-05-13, CEO+Lead co-signed)**:
- **#1080 NOTION-WRITE**: Activate `update_document` capability — demand-gated, not deprioritized. Recovery cost is zero; code stays in tree, flag-gated, ready. Triggers: alpha user asks for write capability, OR recurring PM workflow surfaces where it would compress 2+ steps, OR 1.0 feedback signals chat-driven doc updates as wanted.
- **#1081 NOTION-SLACK-XREF**: Verify Slack→Notion cross-references render correctly post-#304. Triggers: alpha user reports Slack-with-Notion-link missed context, OR Slack-Notion becomes load-bearing workflow.

**Post-MVP / followup issues filed during M2e walkthrough (2026-05-03)**:
- #1043 POST-MVP: En-masse copy review pass for new M2e handlers + standup prompts
- #1044 FOLLOWUP: Local-git "what branch are we on?" query handler
- #1045 POST-MVP: Project Detail Activity tab — design + content

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
5. **Interface-Verification gate (Layer A, #683)** — for any sub-epic acceptance criterion that asserts a consumer-relationship (*"consumer C uses/consumes/touches interface I"*: API consumption, service injection, doc-to-code-path claim, config a downstream step reads), gate-close requires a **methodology-30 Consumer-Trace** proving I's real behavior is reachable by an actual consumer (not merely declared/scaffolded/shape-present upstream). The trace — locate consumer site → trace call chain to real behavior → verify real behavior invoked (not mock/fallback/template-dispatch) → confirm an observable effect → attach the trace to the issue — is the proof; the prose claim is not. FAIL (trace bottoms out at "upstream shape exists") → AC stays `[ ]` or `[⏸]`, never `[x]`-with-a-deferred-parenthetical. This guards the #1089 spec-thinko / Pattern-064 (Extension Without Integration) family. Placement ratified by PM 2026-05-30 as a requirement on the **Class B (sub-epic gate)** review surface. Full definition: `docs/internal/development/interface-verification-dod-layer-a.md`. (Lead Dev operational-check recipe + CXO grounding-review are pending refinements.) Pairs with Layer B (experience-layer DoD: Colleague Test + MUX-doc conformance, CXO-owned).

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
