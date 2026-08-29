# ADR-063: User-Facing Audit Envelope Read Surface — ADR-061 Companion (Four-Element READ-Side Principle)

**Status**: **v0.1 (drafted 2026-05-16)** — pairs with Surface 7 MUX doc (CXO + Comms lane); CEO ratification of paired-deliverable approach received 2026-05-16 via MUX/UI Round 2 ratification (Architect decision walkthrough Item 2)
**Date**: 2026-05-16 (v0.1 — Phase 2 of MUX/UI Round 2 implementation; companion to #1095's Pattern-071 first fix shipped this morning)
**Supersedes**: None (extends ADR-061 with the complementary READ-side architecture)
**Issues**: #1095 (transparency auth gates — Pattern-071 first fix; user-binding + admin gates on `/api/v1/transparency/*`), #1090 (MUX/UI gap — Round 2 synthesis), #1018 (audit envelope write-side; predecessor work)
**Related**: ADR-061 (LLM-touch boundary enforcement — WRITE-side four-element principle; this ADR is the READ-side companion), Pattern-071 (Audit Logs as Attack Surface, Emerging — #1095 first fix; this ADR codifies the architectural commitments), MUX/UI Round 2 synthesis (Surface 7 as paired ADR + MUX doc deliverables)
**Deciders**: Chief Architect (drafted); Lead Developer (#1095 implementation already shipped Pattern-071 first fix); CXO (Surface 7 MUX doc paired-lane drafting); CEO ratification of paired-approach via MUX/UI Round 2 (2026-05-16)

---

## Context and Problem Statement

ADR-061 (LLM-Touch Boundary Enforcement, Ratified May 3, 2026; v1.1 amendment May 15) established the **WRITE-side** of the audit envelope architecture: every LLM-touch event records `(which surface, raw output size, validation result, action taken)` for operator legibility. The fourth element of the four-element principle — **audit envelope** — addresses that the system records each LLM-touch event with structured fields.

**The READ-side was service-only until May 16**. `services/ethics/audit_transparency.get_user_audit_log` (services/ethics/audit_transparency.py:343) provided programmatic access; the user-facing route surface was structurally absent. Per the MUX/UI Round 2 synthesis (May 15):

> "This IS the load-bearing architectural piece — without it, ADR-061's four-element principle is observably 3.5 elements in user-facing terms."

The audit envelope was being written into a surface no user could reach. Without the read surface, operator legibility is structurally one-sided: the system records what it did, but the user has no path to inspect what was recorded about them.

### What landed via #1095 (May 16, 2026 AM)

Lead Developer shipped Pattern-071's first fix this morning:

- **Routes added** to `services/api/transparency.py`: `/api/v1/transparency/audit-log/{session_id}`, `/audit-summary/{session_id}`, `/stats`, `/health`, `/cleanup`
- **User-binding rule**: user-scoped endpoints (`audit-log`, `audit-summary`) require the JWT user to own the session per `ConversationDB`. Admin override available via `is_admin` claim (SEC-RBAC pattern from `files.py`)
- **Admin-scoped endpoints** (`stats`, `cleanup`, `health`) require `is_admin` claim. Until SEC-RBAC global-admin lands, no production user has `is_admin=True`; these endpoints effectively return 403 for every caller — by design
- **Uniform 403 messaging**: avoid leaking session existence to non-owners
- **PII redactions** via `SecurityRedactor` (services/ethics/audit_transparency.py:33) — email, SSN, phone variants, credit card, plus #1017 additions (API keys, URL-with-credentials)

The implementation surfaces the read-side surface; this ADR codifies the **architectural commitments** that implementation represents and commits to the principle going forward.

### Why this ADR now (vs. accepting the implementation as-is)

Three reasons the implementation-only state is structurally insufficient:

1. **Pattern-071 is Emerging, not Proven** — the user-binding rule shipped in #1095 is the first Pattern-071 fix; future read-surface additions need the architectural commitment in place so future-author confidence ("does my new admin endpoint follow the same shape?") has a reference document, not just historical commit archeology
2. **Surface 7 MUX doc is a paired deliverable** — CXO + Comms lane drafts the user-facing voice/recovery affordances; the ADR captures the architectural commitments those affordances express. Different lanes; complementary deliverables.
3. **Pattern-072 (Proven) recognition trigger applies** — the transparency-route surface is a typed catalog of read endpoints. As more surfaces accumulate (audit-log + audit-summary + future per-user / per-admin endpoints), the architectural shape needs to be named before drift accumulates

---

## Decision

### Principle — Four-Element READ-Side Principle

ADR-061's four-element WRITE-side principle (permissive input / schema validation / safe-fallback / audit envelope) has a structural complement at the READ side. **At user-facing audit envelope read surfaces, four elements must be present at every endpoint:**

1. **User-visible field set is explicit** — each endpoint's response model enumerates which envelope fields surface to users (vs. internal-only). Fields that exist in the write-side envelope but should not surface (e.g., raw LLM output verbatim, internal hash markers, system request IDs) are explicitly excluded at the read layer. The split is **architectural commitment, not implementation accident**.
2. **Schema validation at request** — every endpoint declares a `BaseModel` response shape with type guarantees. Consumers (UI, MCP client, programmatic) can rely on the contract; schema drift is caught at the route layer rather than at the consumer.
3. **Safe-fallback path for missing/redacted data** — when entries are absent, redacted, or partially available, the endpoint returns a structured response (empty list + total_entries: 0 + timestamp), never an opaque error. Redacted fields surface as redaction markers, not silently omitted, so the user knows redaction happened.
4. **Access control is JWT-bound at the boundary** — user-scoped endpoints bind session ownership to JWT identity per `ConversationDB`; admin-scoped endpoints require explicit `is_admin` claim; uniform 403 messaging avoids existence-leak across non-owners. **Authorization is route-layer architecture, not service-layer afterthought.**

The principle's structural shape mirrors ADR-061's WRITE-side four elements:

| WRITE-side (ADR-061) | READ-side (this ADR) |
|----------------------|----------------------|
| Permissive input shape | Explicit user-visible field set |
| Schema validation at consumption | Schema validation at request (response model) |
| Safe-fallback path | Safe-fallback for missing/redacted data |
| Audit envelope | Access control bound to JWT |

### User-Visible vs. Internal Field Split (Explicit)

The audit envelope schema in `services/database/models.py` (EthicsAuditDB) captures many fields. Read-surface endpoints surface a deliberate subset:

**User-visible (surfaced via `audit-log` endpoint):**
- `session_id` (user already knows their session)
- `event_type` (what kind of decision — ethics-decline, output-filter, etc.)
- `boundary_category` (which boundary triggered — PROFESSIONAL, PERSONAL, DATA_PRIVACY, HARASSMENT, INAPPROPRIATE_CONTENT)
- `action_taken` (the action class — DECLINE, REDACT, ALLOW)
- `timestamp` (when the decision was made)
- `severity` (CRITICAL / IMPORTANT / INFORMATIONAL)
- **Redacted-where-appropriate**: PII patterns (email, SSN, phone, credit card, API keys, URL-with-credentials) detected in the recorded input/output via SecurityRedactor

**Internal-only (NOT surfaced at user-facing endpoints):**
- Raw LLM output verbatim (could re-expose harmful content the system declined)
- Hash-only markers (per #1017 Pattern-071-shaped hash-only audit invariant)
- Internal request IDs / trace IDs (operator legibility, not user-actionable)
- System telemetry fields (latency, model version, prompt hash)

**Admin-only (surfaced via `audit-summary` endpoint for admins, summarized form only):**
- Cross-session aggregations
- Event-type breakdown counts
- Boundary breakdown counts
- Date-range statistics

The split is codified at the response model layer (`AuditLogResponse`, `AuditSummaryResponse`, `TransparencyStatsResponse` in `services/api/transparency.py`). Future fields added to the WRITE-side envelope require explicit decision on which bucket they belong to — defaulting to **internal-only** unless a deliberate decision surfaces them.

### Pattern-071 Architectural Commitments (Codifying #1095)

The user-binding rule shipped in #1095 represents three architectural commitments worth codifying:

**Commitment 1 — Path-Parameter Authorization at the Route Boundary**

When a route accepts `session_id` (or any resource ID) as a path parameter, the route MUST validate the JWT-authenticated user has authorization to access that resource BEFORE proceeding to service-layer logic. The validation lives at the route layer because:
- It's the boundary; failure at the boundary is the cleanest 403 return
- Service-layer code can assume valid authorization once called (cleaner contracts)
- Centralizing in a dependency function (e.g., `_require_session_owner_or_admin`) makes the rule auditable

**Commitment 2 — Admin Capability Is Explicit Claim, Not Heuristic**

Admin-scoped endpoints check `current_user.is_admin` (a JWT claim) — not a role lookup, not a username check, not a path prefix convention. The claim is set by the auth layer; routes consume it as a boolean. **Future admin endpoints follow the same pattern.** Until SEC-RBAC global-admin lands, the claim is structurally always False in production — admin endpoints exist but return 403 for every caller. This is **by design** — the architecture is forward-compatible with SEC-RBAC; the production state during SEC-RBAC's pendency is uniformly 403.

**Commitment 3 — Uniform 403 Messaging (Pattern-071 Defensive Posture)**

Unauthorized access returns the same 403 regardless of whether the resource doesn't exist or the user lacks permission. This avoids the existence-leak attack surface Pattern-071 names — a non-owner cannot probe for valid session IDs by observing 404 vs. 403 responses.

### Endpoint Shape Conventions Going Forward

Future audit-envelope read endpoints follow these conventions:

- **Prefix**: `/api/v1/transparency/*` (already established; `/api/v1/` per project API conventions)
- **User-scoped resource shape**: `/audit-{resource}/{session_id}` — JWT user must own session per ConversationDB; admin override via is_admin claim
- **Admin-only shape**: `/{resource}` (no path-param resource ID; e.g., `/stats`, `/cleanup`, `/health`) — requires `is_admin=True` claim
- **Response models**: explicit `BaseModel` response shapes with `entries`, `total_entries`, `session_id`, `request_limit`, `timestamp` (or analogous) — never `Dict` opaquely
- **PII redactions**: applied at the service layer via `SecurityRedactor` before return; redacted fields surface as `<REDACTED-{type}>` markers, not silently dropped
- **Error handling**: structured `APIError` per `services/api/errors.py` patterns; uniform 403 for unauthorized

### Scope Boundaries

This ADR commits to architectural shape; it does NOT commit to:
- **Surface 7 MUX doc content** — CXO + Comms paired-lane work; voice register, recovery affordances, visual hierarchy. The MUX doc captures the user experience; this ADR captures the architectural commitments that experience expresses.
- **Specific future field additions** — when new fields land in the WRITE-side envelope (e.g., #1017 hash-only audit fields), the user-visible-vs-internal split decision happens at that field's filing time, not in this ADR. The ADR defaults the split to internal-only; surfacing requires explicit decision.
- **SEC-RBAC global-admin shape** — the admin-claim approach is forward-compatible with SEC-RBAC's eventual landing, but the SEC-RBAC ADR is separate (when it's drafted). Until then, admin endpoints structurally 403 in production.
- **Cross-session audit retention policy** — how long entries live, when they're purged, retention-by-category rules. Separate ADR or operations doc.
- **Per-message audit granularity** — MUX/UI Round 2 ratified per-conversation privacy for 1.0; per-message is post-1.0 expansion. This ADR is per-conversation-scoped; per-message expansion would amend.

---

## Consequences

### Positive

- **ADR-061 four-element principle is observably 4 elements** — the user-facing read surface closes the structural gap Round 2 named
- **Pattern-071 first fix codified as architecture** — future read-surface additions reference this ADR rather than reconstructing the rule from #1095 commit archeology
- **Future endpoint additions have explicit shape conventions** — endpoint prefix, response model, PII redaction, error handling all named
- **User-visible-vs-internal split is architectural commitment** — drift between WRITE-side schema and READ-side surface requires explicit decision rather than silent default
- **JWT-bound access control is route-layer architecture** — service-layer code can assume valid authorization; cleaner contracts
- **Surface 7 MUX doc has architectural commitment to anchor against** — CXO + Comms lane drafts the experience; the architectural shape is settled

### Negative / Tradeoffs

- **Admin endpoints structurally 403 in production until SEC-RBAC lands** — observed-but-not-usable surface during SEC-RBAC's pendency. Acceptable per Pattern-071 defensive posture.
- **Field-bucket decisions add filing-time overhead** — each new WRITE-side field requires explicit user-visible-vs-internal-vs-admin decision. Mitigated by default-to-internal rule (filing surfaces the question, but the default avoids ambient surfacing).
- **Response model verbosity** — every endpoint declares an explicit `BaseModel`; some endpoints have very thin response shapes. Acceptable cost for schema-at-request clarity.

### Non-Consequences (explicitly out of scope)

- **Not changing the WRITE-side ADR (ADR-061)** — this ADR is purely the READ-side companion; ADR-061 remains canonical for WRITE-side architecture
- **Not requiring all existing services to surface audit envelopes via the transparency router** — this ADR scopes to ethics-and-output-filter audit envelopes; other operational logs (request logs, telemetry, application logs) are not addressed
- **Not specifying retention or purge policy** — separate concern; cleanup endpoint exists but policy is operations-doc territory
- **Not requiring per-message granularity** — per-conversation scope ratified May 16; per-message is post-1.0 expansion path

---

## Validation

### Implementation Anchor: #1095 (Already Shipped)

The user-binding rule, admin-claim pattern, and uniform 403 messaging are already in production as of #1095 (Lead Dev commit `0161f089`, May 16 AM). This ADR codifies what #1095 implemented as architectural commitment — implementation precedes ratification by hours, which is acceptable for codifying Pattern-071 first-fix shape (the rule shipped because it was urgent; the ADR captures it now while the shape is fresh).

### Architectural Invariants the Implementation Satisfies

| Element | Implementation surface | Verification |
|---------|----------------------|--------------|
| Explicit user-visible field set | `AuditLogResponse`, `AuditSummaryResponse` BaseModels in `services/api/transparency.py:80-102` | grep for response model definitions; each endpoint returns typed BaseModel |
| Schema validation at request | `@transparency_router.get` decorators with typed `current_user: JWTClaims` dependency + typed response return | FastAPI route signature is the contract; mypy/pylint surface drift |
| Safe-fallback for missing/redacted | `get_user_audit_log` returns `[]` on error (services/ethics/audit_transparency.py:380); `SecurityRedactor` applies before return | Test coverage in #1018 audit-write integration tests; redaction patterns at audit_transparency.py:33 |
| Access control JWT-bound | `_require_session_owner_or_admin` at services/api/transparency.py and `current_user: JWTClaims = Depends(get_current_user)` on all routes | #1095 PR review + manual test of 403 cases |

### Pattern-071 Trajectory

Pattern-071 (Audit Logs as Attack Surface) was filed Emerging via #1017. #1095 was the first fix (Lead Dev's transparency auth gates). This ADR's commitments establish what future Pattern-071 fixes look like — second fix would extend the existing user-binding / admin-claim / uniform-403 shape to a new endpoint. When Pattern-071 reaches third fix consistent with this shape, the pattern reaches Proven status per the standard methodology-29 promotion trigger.

### MUX/UI Round 2 Paired Deliverable

Per Round 2 synthesis, Surface 7 is "**Full MUX doc** + separate ADR-NN companion" with CXO + Comms drafting the MUX doc in parallel. This ADR is the architectural-commitment half; the MUX doc is the experience-design half. Phase 2 build implements both. Architectural commitments shape the user-visible surface; voice register, recovery affordances, and visual hierarchy shape the experience of consuming it.

---

## Cross-references

- **ADR-061** (WRITE-side companion; four-element principle): `docs/internal/architecture/adrs/adr-061-llm-touch-boundary-enforcement.md`
- **Pattern-071** (Audit Logs as Attack Surface, Emerging): `docs/internal/architecture/patterns/pattern-071-audit-logs-as-attack-surface.md`
- **MUX/UI Round 2 synthesis** (Surface 7 paired-deliverable shape): `mailboxes/{cohort}/inbox/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **MUX/UI Round 2 CEO ratification** (this ADR triggered): `mailboxes/arch/sent/memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md`
- **#1095 transparency auth gates** (Pattern-071 first fix; Lead Dev shipped 2026-05-16 AM): commit `0161f089` + close-out `cc22560d`
- **Transparency route surface**: `services/api/transparency.py` (356 LOC; 5 endpoints)
- **Service layer**: `services/ethics/audit_transparency.py:343` (`get_user_audit_log`); `:33` (`SecurityRedactor`); `:411` (`cleanup_old_entries`)
- **Response models**: `services/api/transparency.py:80-102` (AuditLogResponse, AuditSummaryResponse, TransparencyStatsResponse)
- **Surface 7 MUX doc** (paired deliverable, CXO + Comms lane): pending Phase 2 drafting

---

## Open Items (Phase 2+ work, not gated by this ADR)

- **Surface 7 MUX doc drafting** — CXO + Comms paired-lane work; voice register, recovery affordances, visual hierarchy for the read surface (e.g., how a user reads "ethics decision: harassment-redirect" without alarm; how to surface redacted PII markers; how to handle the structurally-403'd admin endpoints in UI)
- **SEC-RBAC global-admin ADR** — when SEC-RBAC scope-decision lands, admin-claim semantics formalize; the admin endpoints in this ADR consume the resulting infrastructure
- **Field-bucket decisions for #1017 hash-only audit fields** — currently default to internal-only; surfacing decision deferred until the MUX doc work surfaces user-facing need
- **Cross-session retention policy** — separate ADR or operations doc; the `/cleanup` endpoint exists but policy is not codified
- **Per-message audit granularity** — MUX/UI Round 2 explicitly post-1.0 expansion path; this ADR is per-conversation-scoped

— Chief Architect, 2026-05-16 v0.1 (READ-side companion to ADR-061; codifies #1095's Pattern-071 first fix + future-direction commitments per MUX/UI Round 2 ratification)
