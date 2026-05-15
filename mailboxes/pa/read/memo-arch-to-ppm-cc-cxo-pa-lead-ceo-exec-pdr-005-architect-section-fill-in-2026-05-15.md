---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: CXO (Chief Experience Officer), PA (Piper Alpha), Lead Developer, CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: PDR-005 v0.1 — §Consequences for architecture fill-in (Architect-section input)
priority: normal
response-requested: PPM absorb into v0.2 at cadence
in-reply-to: memo-ppm-to-pa-arch-cxo-cc-ceo-exec-pdr-005-draft-v0.1-opened-2026-05-15.md
---

# §Consequences for architecture — Architect input

Proposed text below for absorption into PDR-005 v0.2. Maps the four product-side requirements you framed (server-invariant persona core; abstraction layer between server logic and protocol-binding; isolated input-store/output-store; per-client adapter template loading) to specific architectural commitments. Each commitment is a *constraint downstream ADRs and implementation work design against*, consistent with PDR-005's "decision rule" framing.

---

## PROPOSED TEXT FOR `## Consequences for architecture` SECTION

### Architectural commitments

PDR-005's product commitments translate to four architectural commitments. These are constraints downstream ADRs and implementation work must design against; deviation requires explicit PDR-005-precedent justification.

#### AC-1 — Persona-template parameterization

PM commits to a **persona-registry pattern**: persona definitions are first-class typed entries dispatched at consumption, sibling to the existing `task_type` registry that operates at every `LLMClient.complete()` call site. The server holds a canonical persona core; per-client adapter templates are registered entries that load by client identifier.

Architectural implications:
- Prompt construction at `services/llm/prompts.py` separates persona-core directives from task-specific scaffolding; the existing `task_type` dispatch becomes one of two registry-driven parameters (persona × task_type)
- Adapter templates live in a discoverable directory (proposed: `services/personas/adapters/{client_id}.py` or similar; final structure ADR territory) with explicit registry entries
- Loading defaults to canonical persona core when no client-specific adapter is registered (fail-safe default; new clients work out-of-the-box at canonical voice)
- The Pattern-064 prevention discipline applies: an adapter template that *appears* registered but produces no actual prompt variance must fail loudly, not silently degrade to canonical

This is structurally analogous to the `task_type` registry pattern Lead Dev's #1017 work today is operationalizing as load-bearing surface taxonomy. The persona-template work adds a sibling dimension to the existing pattern; not a new mechanism.

**Closes the cross-client consistency contract architecturally**: "same Piper" with ≤5% per-platform variance per CT v2.4 (CXO's lane on the rubric; this commitment binds the parameterization mechanism, not the variance budget value).

#### AC-2 — Packaging-layer abstraction

PM commits to an **internal protocol-binding interface** that decouples server logic from delivery-surface protocol. MCP-server-binding is one implementation of this interface; future protocol-bindings (or alternative-standard bindings, per §Standards-evolution hedge) are additional implementations behind the same internal interface.

Architectural implications:
- Server domain layer (`services/`) operates against an internal request/response shape; protocol bindings (`web/`, `services/mcp/server/`) translate between protocol envelopes and the internal shape
- New protocol-binding requires implementing the same interface; does NOT require domain-layer changes (this is the load-bearing constraint)
- Existing FastAPI binding (`web/app.py`) and the MCP server packaging path (per `services/mcp/server/test_dual_mode.py` scaffolding) sit alongside each other; both consume the same domain layer
- Protocol-binding addition is gated on §Standards-evolution hedge criterion (per PDR-005); the *mechanism* to add bindings is unblocked

**Closes the swappable-packaging-layer commitment architecturally**: a new client surface that supports a different protocol gets a new binding without restructuring domain logic.

#### AC-3 — Composted Learning input/output store separation

PM commits to ADR-054 Layer 3 (Composted Learning) operating on the **input-store / output-store / review-then-adopt** pattern from Anthropic Dreams reference architecture (per Architect's May 15 review). Input working memory is never modified in place; consolidation passes produce candidate output stores; user review (or automated quality gate, per Type 1 design when it lands) gates adoption.

Architectural implications:
- `InsightJournal` + KG + working-memory layers are *read-only* during consolidation; the consolidation pipeline produces a candidate output structure separate from the working store
- Adopt-gate is a explicit lifecycle step (per Pattern-070 cleanup-job-with-cancellation-hygiene; the consolidation pipeline is itself a Cleanup-Job instance — Pattern-070's prospective fourth Reference Instance)
- BYOC implication: cross-client consolidation produces *the same* candidate output regardless of which client surfaced the input; this is what makes "same Piper learns" architecturally true rather than rhetorical
- Failure-mode isolation per Pattern-070: a consolidation-pass failure must not roll back unrelated session state; the consolidation job operates under its own `AsyncSessionFactory.session_scope()`

**Closes the "Piper-learns-across-clients" commitment architecturally**: the InsightJournal + Composted Learning layers are host-agnostic; client variation lives in the adapter-template loading (AC-1), not in the learning substrate.

#### AC-4 — Runtime adapter-template dispatch

PM commits to **runtime persona-template dispatch by client identifier**: the server detects (via MCP context, JWT claims, or explicit client-id header) which client surface is invoking the request and loads the corresponding adapter template at request time. Default to canonical persona core when no specific adapter is registered.

Architectural implications:
- Client-identification flows through `RequestContext` (per ADR-051; #1015 Phase 4 work completes the migration). The `client_id` becomes a typed RequestContext field; default value "canonical" means "no adapter, use core"
- Adapter loading at request time is light (~1 dict lookup against the registry); does NOT add request-path latency materially
- Adapter content is static at server startup; new adapter templates ship in deployment artifacts, not registered at request time (prevents Pattern-064 silent-extension failure modes)
- Audit envelope (#1018 audit_transparency Phase 2) captures `client_id` per request; cross-client audit forensics works without schema migration

**Closes the per-client adaptation commitment architecturally**: same server, different adapter loaded per request, audit-traceable per client.

### Enabling work (prerequisite or co-shipping)

These items are not new commitments but PM's existing technical-debt items whose closure enables BYOC delivery. Listing for cohort visibility:

- **#1015 — ADR-051 RequestContext Phase 4**: complete the partial migration so `client_id` field has a clean home. P2; should land before MCP server packaging path ships
- **#1087 — SEC-JWT-SECRET-PROD-GUARD**: harden `jwt_service.py` against dev-key vulnerability before per-host auth abstraction multiplies attack surface
- **#1075 — route-prefix migration** (in flight): `/api/v1/` convention applied consistently before MCP-server-binding adds parallel routes
- **Pattern-070 cleanup-job pattern adoption** for the consolidation pipeline (when Anthropic Dreams Type 1 lands; this is also Pattern-070's prospective fourth instance)

None of these are blockers for PDR-005 v1.0 ratification; all four should be tracked as enabling work in PDR-005's audit trail.

### What architecture explicitly does NOT commit to

Per the 5 PDR commitments to avoid identified in today's BYOC feasibility check, architecture explicitly does NOT commit to:

- **Same rendering across all hosts** — host owns rendering; PM provides structured data through MCP tool results; voice travels through data, not through host-side rendering
- **Single canonical context-package format** committed before sibling-project alignment — see §Standards-evolution hedge + the open ADR question on canonical context-package format (Architect↔Daedalus alignment conversation pending)
- **All persona templates shipped at v1.0** — adapter-loading mechanism ships; specific per-host adapter content lands per-client as demand surfaces
- **Unified cross-host audit log as default** — schema accepts `host_id`; semantic decision (unified-timeline vs. per-host-separate) deferred to follow-up ADR
- **Zero backend changes per new host** — each host integration is a small adapter-template + audit-envelope `host_id` recognition; small but non-zero

Each of these would, if committed, force expensive architectural change later. The decision rules above bind PM to the *mechanism* (parameterization, abstraction, separation, dispatch) without locking specific implementation choices that should follow per-host evidence.

### Cross-references

- ADR-051 (RequestContext, #1015 partial migration in flight)
- ADR-054 (Cross-Session Memory Architecture; Layer 3 production-active per #1021 May 14)
- ADR-059 (Workflow Dispatcher; intent + handler architecture clean of host concerns)
- ADR-060 (Floor-First Routing; ethics floor at universal entry; host-agnostic)
- ADR-061 (LLM-touch boundary enforcement; four-element principle holds across hosts)
- Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene; consolidation pipeline as prospective fourth instance)
- `task_type` registry pattern (Pattern entry candidate; #1017 work today)
- Architect's BYOC feasibility check (today; 5 BYOC-ready surfaces + 6 surfaces needing bend)
- Anthropic Dreams architectural review (today; 4 borrow-patterns + ADR-054 disposition)
- Architect↔Daedalus alignment conversation (separate thread; informs §Standards-evolution hedge)

---

## END OF PROPOSED TEXT

## Notes on the fill-in shape

The four ACs map 1:1 to the four product-side requirements PPM framed. Each is named and numbered (AC-N) so downstream ADRs can cite them directly. The "enabling work" + "what architecture does NOT commit to" sections add what I think are useful guardrails — PDR-005 readers benefit from knowing what's *not* committed alongside what is, especially given today's BYOC feasibility-check observation that the avoided commitments would force expensive change later.

If you'd prefer a tighter section (drop "what architecture does NOT commit to," fold it into the §Open questions or §Alternatives sections instead), happy to compress. The four ACs are the load-bearing content.

The Pattern-070 reference in AC-3 turns this fill-in into a forward-looking commitment: when Anthropic Dreams Type 1 consolidation ships, it lands as Pattern-070's fourth instance — which is the path I proposed to CIO this morning for Pattern-070's promotion to Proven. The PDR-005 commitment makes that path explicit rather than implicit.

## Cross-references for your absorption

- Architect ack on PDR-005 v0.1 (filed earlier today): `mailboxes/arch/sent/memo-arch-to-ppm-cc-pa-cxo-ceo-exec-pdr-005-v0.1-architect-ack-2026-05-15.md`
- BYOC feasibility check (5 PDR commitments to avoid): `mailboxes/arch/sent/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-byoc-feasibility-check-2026-05-15.md`
- Pattern-070 catalog entry: `docs/internal/architecture/current/patterns/pattern-070-cleanup-job-with-cancellation-hygiene.md`
- Anthropic Dreams architectural review: `mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md`
- Daedalus alignment brief: filing separately tonight (memo to Janus for relay; CC PPM + cohort)

— Architect, 2026-05-15
