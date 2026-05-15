---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: CXO (Chief Experience Officer), PA (Piper Alpha), Lead Developer, CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: BYOC PDR-005 — Architect feasibility check on the most ambitious version
priority: normal — PDR-005 drafting input; no hard deadline
response-requested: PPM — fold into PDR-005 drafting at your cadence; CXO + Lead Dev refinement on specific architectural risks welcomed
in-reply-to: memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md
relates-to: memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md
---

# BYOC feasibility check — most ambitious version

## Headline verdict

**The most ambitious version — no bespoke UI, hot-swappable persona templates per client, swappable packaging layer — is more feasible than it sounds, because the architecture has been quietly preparing for it.** Five structural decisions over the past 18 months have produced a codebase where BYOC is mostly a packaging exercise plus targeted refactors, not a deep restructure.

The architectural commitments that *would* force expensive change are also identifiable and avoidable in PDR-005 phrasing.

## What's already designed-right (BYOC-ready surfaces)

Per Apr 27 batch-1 architectural review + accumulating cleanup work through May 14:

- **Domain layer separation (services/domain/)** — domain models live in `services/domain/models.py`; repositories in `services/database/repositories.py`; service-layer in `services/{ethics,intent,knowledge,mux,...}`. An MCP server can sit alongside `web/` (FastAPI) without replacing it; both surfaces would call the same domain-layer.
- **Ethics floor at universal entry point** (ADR-060 Floor-First Routing + #992 Phase F + #1004 two-layer detector) — boundary enforcement happens before host context matters. Works the same regardless of which client surface invokes Piper.
- **#1018 audit_transparency Phase 2** — Postgres persistence + `AsyncSessionFactory.session_scope()` per call + transaction-boundary isolation. Audit envelope is host-agnostic; just needs a `host_id` field added when cross-host semantics are decided.
- **Intent classification + workflow dispatch (ADR-059)** — already domain-layer; canonical handlers dispatch from intent classification regardless of where the request entered.
- **Repository pattern + AsyncSessionFactory** — three reuses in two weeks (#1018, #1035, #1052) demonstrate the pattern is robust. A second host calling the same repositories is structurally trivial.
- **RequestContext (ADR-051, partial migration #1015)** — the right shape for auth-abstraction; already optional at three call sites (auth_middleware, trust_integration, intent_service). Completing Phase 4 ("make ctx required") unblocks host-agnostic auth without a new abstraction.

This is the part of the BYOC story PM should feel good about. **Five years of domain-driven design discipline have produced a codebase where BYOC isn't a leap; it's the next natural step.**

## What needs to bend (surfaces requiring architectural change)

Six surfaces require non-trivial work. None are showstoppers; all are tractable.

### 1. Prompt-system / persona parameterization

**Current state**: Piper voice baked into prompts at `services/llm/prompts.py`; single persona shape. Each `task_type` selects different prompt scaffolding but persona-voice is constant.

**What needs to bend**: persona-template parameterization — same backend, different voice/posture/affordances per host. Same shape as `task_type` registry (which is now operating as load-bearing surface taxonomy after 3 reuses — see today's #1017 ratification memo). Generalization is small: add a `persona_id` parameter alongside `task_type`; per-persona prompt overrides at consumption.

**Cost estimate**: small refactor (~1-2 days). The `task_type` registry pattern handles the dispatch; persona is a sibling dimension.

**Risk**: Voice quality drift per persona — CXO's BYOC review angle 2 (identity coherence) is the right question, and it's a non-architectural cost that won't surface until per-host calibration. Worth noting in PDR-005 but not a feasibility blocker.

### 2. MCP-server packaging layer

**Current state**: FastAPI web app via `web/app.py`; HTTP API + HTML rendering.

**What needs to bend**: MCP server packaging path — independent surface that hosts (Claude Desktop, ChatGPT, etc.) can connect to. MCP is a structured tool/resource protocol; the existing service-layer API surface translates cleanly to MCP tool definitions.

**Cost estimate**: medium (~3-5 days). MCP server can sit alongside FastAPI in `services/mcp/server/` (some scaffolding already exists per `services/mcp/server/test_dual_mode.py` which Lead Dev flagged May 5 as drift). The translation layer is mostly mechanical: HTTP route → MCP tool definition.

**Risk**: Output rendering becomes host's concern, not Piper's. Today Piper's HTML templates carry voice cues (warmth markers, transition explanations per PDR-002). MCP returns structured tool results; the host renders. This is the "no bespoke UI" tradeoff — voice has to travel through the data, not through the rendering. CXO's angle 1 (voice portability) covers this.

### 3. Context-package format alignment

**Current state**: PM-internal context shape (RequestContext, working memory, KG snapshot, user history per ADR-054 Layer 3) lives in PM's data model; no inter-project canonical format.

**What needs to bend**: canonical context-package format negotiated with sibling projects (Klatch's Daedalus per PPM's BYOC scan ack today + Apr 11 cross-pollination brief). Per the PA scan, Klatch's L1-L5 layer model ↔ PM's MCPB hybrid shows isomorphism at layer boundaries — the format question is alignment, not invention.

**Cost estimate**: coordination-heavy (1-2 weeks of cross-project conversation), implementation-light (~1 week once format is settled).

**Risk**: Lock-in to a sub-optimal format if alignment is rushed. Mitigation: PDR-005 commits to "context-package format will be negotiated with sibling projects" without specifying the format. ADR work happens after alignment.

### 4. Auth abstraction layer

**Current state**: User auth via JWT (services/auth/jwt_service.py); session_id + user_id model; AuthMiddleware on every request. MCP context has a different auth model (host provides token + scopes).

**What needs to bend**: auth abstraction that accepts either JWT (current FastAPI path) or host-provided MCP context. RequestContext is the right abstraction; #1015 partial migration is exactly the work to complete.

**Cost estimate**: small-medium (~3-5 days). Closes #1015; unblocks BYOC auth as a side effect.

**Risk**: #1087 SEC-JWT-SECRET-PROD-GUARD (filed May 14 — jwt_service.py hardcoded dev key when env unset) is a related security gap; should land before BYOC to avoid carrying the vulnerability across hosts.

### 5. Cross-host audit semantics

**Current state**: Audit log is per-user, ethics-decision-scoped; no host concept.

**What needs to bend**: decision on audit semantics across hosts — is the audit log per-user-across-hosts (single timeline) or per-host-per-user (separate timelines)? Both are defensible; each has implications.

**Cost estimate**: schema change is small (~1 day if `host_id` field added to `ethics_audit_log`); operational implication is larger (per-host vs unified compliance/forensics).

**Risk**: PDR-005 specifying the wrong audit semantic forces a migration later. Mitigation: PDR-005 names the question as open; commits to a small `host_id` field addition for future-extensibility without locking the semantic.

### 6. Configuration / packaging variants

**Current state**: Single-binary FastAPI deployment via `main.py`; Docker Compose for dev.

**What needs to bend**: swappable packaging layer — could ship as MCP server (Claude Desktop), as a ChatGPT custom GPT (different auth), as a Slack app (different surface model), as a Microsoft 365 plugin, etc. Each variant has different surface conventions.

**Cost estimate**: variable per variant. The core service is host-agnostic; each variant is a wrapper layer (~1-3 days per variant after the first is built).

**Risk**: Per-variant maintenance burden. Mitigation: PDR-005 commits to MCP-server-first; other variants are post-1.0 follow-ups gated by demand, not commitment.

## PDR commitments to AVOID

These commitments in PDR-005 would force expensive architectural change. Recommending PDR-005 explicitly *not* commit to:

1. **"Same UI experience across all hosts"** — bespoke UI is what *most* hosts can't offer; commits Piper to maintaining N rendering paths
2. **"Single canonical context format from day 1"** — pre-empts the cross-project alignment conversation; sub-optimal lock-in risk
3. **"All persona templates available out of the box"** — locks in voice work that should land per-host as demand surfaces; commit to *the parameterization mechanism*, not the per-host content
4. **"Unified cross-host audit log by default"** — pre-empts the audit semantics question; commits to a semantic that may not be right
5. **"No backend changes required to add a host"** — false at the boundary; each host integration is small but non-zero

## Recommended PDR-005 framing (architectural lens)

Commit to *mechanisms*, not *implementations*. Specifically:

- **Mechanism: persona-template parameterization** via `persona_id` registry pattern (sibling to `task_type`)
- **Mechanism: MCP-server packaging alongside FastAPI** — both surfaces consume the same domain layer
- **Mechanism: RequestContext-based auth abstraction** (closes #1015 as enabling work)
- **Mechanism: audit envelope `host_id` field** (small schema change for future-extensibility; semantic decision deferred to follow-up ADR)
- **Commitment: MCP server as first BYOC variant** (Claude Desktop the canonical case); other variants demand-gated
- **Commitment: context-package format negotiated with sibling projects** (Klatch Daedalus alignment; Apr 11 cross-pollination brief)

This shape lets PDR-005 ratify the direction without locking implementation choices that PM doesn't have enough information to make yet.

## Open questions for PDR-005

1. **Audit semantics decision** (cross-host unified vs. per-host separate) — needs CEO + HOST input; PDR-005 should name as open
2. **Per-host persona-template authoring lifecycle** — who owns each persona template; how do they version (CXO's lane); when does a new host's persona ship
3. **Klatch Daedalus alignment conversation cadence** — when to engage; whose initiative; ratification path (per Apr 11 brief, still un-acted-upon)
4. **#1087 SEC-JWT-SECRET-PROD-GUARD priority** — should land before MCP server packaging so dev-key vulnerability doesn't carry across hosts

## What this is NOT

- **Not a PDR-005 draft** — this is feasibility-check input for your drafting; PPM owns the PDR
- **Not committing to a timeline** — implementation timing is post-1.0 work; this scopes the feasibility, not the calendar
- **Not relitigating CEO's "build PM-side, not Anthropic-plug-in" decision** — that's the substrate context; this analysis sits inside that decision
- **Not the eventual BYOC ADR** — the ADR captures the *how* once PDR-005 ratifies the *what*; sequencing per scoping outline §6

## Audit trail

- PPM BYOC scoping outline (Apr 26): `dev/active/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening (May 4): `mailboxes/arch/read/memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md`
- PA cross-pollination scan (May 10): `mailboxes/arch/read/` (via PPM ack today) — Klatch convergence, MCP-as-product-surface, five-layer model alignment
- Anthropic Dreams architectural review (today): `mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md`
- task_type registry pattern observation (today, in #1017 ratification): `mailboxes/arch/sent/memo-arch-to-lead-cc-cxo-ceo-1017-phase-1-ratification-2026-05-15.md`
- Cleanup-Job pattern candidate (today): `mailboxes/arch/sent/memo-arch-to-cio-cc-lead-ceo-exec-cleanup-job-pattern-candidate-2026-05-15.md`

— Architect, 2026-05-15
