# ADR-071: User-Auth Anchoring Pattern for Content Stores

**Status**: v0.1 (Lead-authored 2026-06-15) — **RATIFIED by Arch 2026-06-15** ("clean fold; every guidance point folded faithfully"; 2 minor cross-refs folded below). Grounded in the #1241 content-anchoring audit (PM-directed systemic flag 2026-06-14; Arch D1 ruling + D1–D7 grounding-confirm 2026-06-15). Companion to **ADR-058** (Multi-Tenancy Isolation) at the *content* altitude — same make-impossible-by-construction shape, one layer down from credentials.

**Date**: 2026-06-15

**Authors**: Lead Developer (audit owner)

**Reviewers**: Chief Architect (ratifier; D1 ruling + D2/D4 expansions), CXO (trust framing), PPM (entity-model lane — the Radar People/WorkItem backends consume this), CIO (methodology — m-30/m-40/m-41), CEO (xian — directed the systemic flag + endorsed "an architectural decision and a consolidating refactor")

---

## Status

- **v0.1** Lead-authored 2026-06-15 from the #1241 audit (`dev/2026/06/15/1241-content-anchoring-audit.md`). Arch greenlit the draft after the D1 ruling, then **ratified v0.1 as-is 2026-06-15 ~13:15 PT** (the 2 cross-refs below are the only folds since ratification — polish, not redlines).
- **Gates**: the doc-store remediation (#1238); the Radar entity-source backends (#1237 umbrella — Document/WorkItem/People sources build *to* this pattern); the consolidating refactor PM endorsed.
- **Composes with**: ADR-058 (credentials altitude — same shape), ADR-070 D8/D9 (RECONNECT identity unification finishes ADR-058; this anchors at the auth-resolution layer above it).
- No M3 dependency. Milestone placement PPM's call (the entity model lands M4; this pattern + the (c,3) privacy remediation are the prerequisite).

---

## Context

### What problem does this ADR solve?

The #1241 audit (PM: *"this is not our first attempt to anchor content to user auth… how systematic is it? It needs deep plumbing-out"*) found that Piper anchors content to the authenticated principal **three inconsistent ways, with no canonical one**:

- **`owner_id`** — UUID `ForeignKey("users.id")`; read-scope = JOIN through `users`. (knowledge_nodes, lists, uploaded_files, artifacts, projects, …)
- **`user_id`** — the external auth-principal, frequently `Column(String)` and **not** a FK; read-scope = filter by the principal string. (conversations, insights, feedback, memory, standup, …)
- **none** — no anchor column at all.

This inconsistency *is* the recurrence cause: a new content type inherits no pattern, so it re-derives ownership (or omits it). Three concrete failure classes fell out of the audit:

1. **`(c,3)` store gaps** (no owner column + global reads) — the **ChromaDB doc store** (`document_service.py` queries by timeframe / empty `where`) and **`stakeholders`** (the People-entity backend). These are live cross-user-leak risks under multi-tenancy (ADR-058).
2. **`(a,3)` leak paths** in owner-stamped stores — specific read methods that *don't* apply the filter: `conversations.get_by_id():1544` (PK fetch, no owner check), `insights.get_for_object():2316` (object_id only), `knowledge_nodes` (owner filter only if passed), `artifacts.get_by_id` (post-hoc filter). Verified by hand.
3. **Resolution degradation (the dominant vector)** — the principal *is* resolved correctly at the host boundary (`auth_middleware.py:177/316`) but is then **re-fetched opportunistically** as `user_id = intent.context.get("user_id") if intent.context else None` at **40+ sites** (`classifier.py`, `conversation_handler.py`, `intent_service.py` handlers). A missing/empty context silently degrades the principal to `None`; some downstream paths then proceed unscoped.

### Why this is architectural, not a per-store patch

Patching the doc store bespoke (e.g., adding `list_by_user`) without a content-wide contract just defers the next variant — which is exactly the recurrence PM named. The fix is a **canonical, enforced anchoring pattern** that new content types inherit by construction. (m-30 Consumer-Trace Verification is the meta-discipline that surfaced this; this ADR is m-30 instance #6 at the content-anchoring boundary.)

### Trust framing (CXO)
Anchoring is a **trust prerequisite, not just data hygiene**: content Piper holds about a principal that can leak across principals — or memory that can't distinguish whose it is — is not trustworthy memory. The (c,3) gaps are trust defects, not only schema defects.

### Prior art / cross-references
- **ADR-058** (Multi-Tenancy Isolation, APPROVED) — user-scoped credentials; this is the *same shape at content altitude*.
- **ADR-063** (actor_chain) — the principal carries through the chain; D4 is the content-read instantiation.
- **ADR-066 v0.2 D7** (server-owned config) — same architectural-boundary altitude.
- **ADR-069** (Domain Concept Projection Contract) — same make-impossible-by-construction family.
- **m-30** (Consumer-Trace Verification — surfaced the recurrence), **m-40** (Layer-Then-Migrate — D2/D4/D6 migration shape), **m-41** (Mechanism Displaces Unreferenced Discipline — D5 guard).

---

## Decision

### D1 — When does content need user-auth anchoring? (+ the global-by-design exemption)

Anchoring is **required** whenever **(i)** content has a user-attributable origin **AND (ii)** it is rendered through a per-user surface. The two-part test is the **over-anchoring guard**: global *system* configuration doesn't need user-anchoring (per-tenant config is ADR-058's lane).

**PM-domain cluster ruling (Arch, 2026-06-15)**: `products`, `features`, `work_items`, `intents`, `workflows`, `tasks` are **PM-system-state, not user-content**, in the current single-PM model — there is no other principal to scope to, so anchoring them now is premature schema cost with no behavioral difference. They are **global-by-design — but with three non-negotiable disciplines** (the "explicit-discipline-not-silent-absence" posture that prevents the recurrence):

1. **Explicit exemption at the schema layer** — these tables are tagged `is_global_pm_domain` (mechanism deferred to the implementation PR; see Open Questions). A reader sees *intent*, not a gap.
2. **Per-user-render guard at the consumer boundary** — surfaces that render PM-domain content per-user (Radar; future similar) MUST assert `principal == pm_user_id` at the render boundary and render empty (or 403) otherwise. This is the defense-in-depth safety net for the multi-tenant future. **Consequence: the Radar WorkItem leg (#1239) needs the render-guard, NOT a `work_items` schema change, before it ships.**
3. **Named multi-tenant migration path** — see D7 (`tenant_id`, not `user_id`).

### D2 — Ownership-stamped-at-write invariant + the canonical convention (the consolidating refactor)

Every persisted **user-content** type carries a non-Optional owner at the data layer; content cannot be constructed without one. **The canonical convention (resolves the three-style inconsistency — this is the PM-endorsed consolidating refactor):**

- **Canonical**: **`owner_id`** — UUID `ForeignKey("users.id")`. Read-scope via JOIN through `users`.
- **Deprecated**: `user_id` (auth-principal *string* column, not a FK — the conversations/projects style). Migrate to `owner_id` FK.
- **Forbidden**: no anchor column on a user-content table.

**Migration shape (m-40 layer-then-migrate)**: convert deprecated `user_id` columns to `owner_id` FKs one caller-chain at a time; hold the deprecated column as a **shim** until callers complete migration, then drop it. (See D6 for sequencing.)

### D3 — Scoping-filtered-at-read invariant

Every read of a user-content store carries an explicit principal and **filters at the data layer** (the query's WHERE/JOIN), never via application-layer post-hoc filtering — that's the failure mode where a missed filter leaks the global set. The audit's `(a,3)` leak paths (`conversations.get_by_id`, `insights.get_for_object`, `knowledge_nodes` conditional, `artifacts` post-hoc) are the concrete bugs this invariant + the D5 guard catch.

### D4 — Principal-resolution-at-the-boundary (carries half this ADR's weight)

The audit's dominant finding: the principal is resolved correctly at the boundary but degrades to `None` across 40+ opportunistic re-fetches. Four sub-decisions:

- **D4.1 — Single origination**: the principal originates at exactly one place — the host boundary (HTTP middleware `auth_middleware.py:177/316`; the MCP handshake surface; CLI invocation).
- **D4.2 — Threaded as a required parameter**: the principal is passed through call chains as a **required, non-Optional parameter**, never re-resolved from mutable context. **Named anti-pattern**: `user_id = intent.context.get("user_id") if intent.context else None`.
- **D4.3 — Migration (m-40)**: the 40+ degradation sites get the principal threaded as a required param, one call-chain at a time; the deprecated context-fetch is held as a shim that logs a WARNING during the migration window.
- **D4.4 — Guard composability**: the D5 AST test flags any `intent.context.get("user_id")` outside the boundary-resolution sites.

**Composition with ADR-070 D8 (cross-ref)**: D4.1's "the principal originates at exactly one host boundary" assumes a *unified* identity model. Identity unification (ADR-070 D8, WS-9 #1233 at the RECONNECT lane) is therefore prerequisite-ordered before the D4 resolution cleanup completes — until it lands, D4 must handle the multi-identity-per-human case (a human reachable via more than one principal). The discipline is unchanged; the ordering dependency is named so the refactor doesn't thread a principal that the identity model can't yet resolve to one human.

### D5 — Guard pattern (m-41: mechanism displaces unreferenced discipline)

AST-level enforcement test (mirrors `TestSessionScopeCommitContract` from ADR-069 D5): a persisted user-content model lacking an owner column (and not on the `is_global_pm_domain` exemption list) **fails the build**; a read path on a user-content store that doesn't accept + apply a principal **fails the build**; an `intent.context.get("user_id")` outside the D4.1 boundary sites **fails the build**. Discipline that isn't mechanized regresses (m-41) — this is the recurrence-prevention.

**Guard-introduction pattern (cross-ref)**: land each guard via the **baseline-ratchet** shape already in production for the F3 #1172 token-lint (`scripts/token_lint.py`) and the F1 #1170 native-dialog gate (`scripts/native_dialog_lint.py`) — snapshot existing violations to a baseline file, fail CI only on the *multiset-new* delta, ratchet the baseline to zero as the migration lands. A guard that hard-fails the build on day one against 40+ pre-existing sites is unshippable; the ratchet makes the guard land immediately (catching new violations) while the migration drains the baseline.

### D6 — Migration shape (layer-then-migrate, m-40)

Per store: introduce the owner as Optional → backfill where possible OR mark `is_global_pm_domain` (D1) → flip Optional→required + drop the shim. **Privacy-first ordering**: the `(c,3)` population (doc store + `stakeholders`) goes first (live leak risk); the `(a,3)` leak paths follow; the D4 resolution cleanup runs in parallel with the store migrations. The doc store is the **worked example** (#1238). *(The detailed per-store PR sequence is an implementation artifact, not ADR-decision text — see Implementation Sequencing.)*

### D7 — Multi-tenancy evolution path (names it; does not pre-author it)

Anchoring at `user_id`/`owner_id` today is the single-tenant shape. When multi-tenancy lands (PDR-005 BYOC future + Skunkworks Phase 2c + #1185 per-user keys), the **principal type evolves** — the PM-domain cluster gains `tenant_id` (org/workspace level), and per-user-render guards evolve to `principal IN tenant_set`. **The discipline doesn't change; the principal type does.** Authoring the multi-tenant ADR now would conflate single-tenant remediation with multi-tenant evolution (the variant-preservation trap, m-41 one altitude up) — deferred to a future artifact.

**Concrete first instance (2026-07-05, #1260)**: `resolve_pm_owner_id`'s "which account is the configured PM" resolution moved off a hardcoded `username == 'xian'` literal onto server-owned config (`PiperConfigLoader.load_pm_identity_config()`, the "PM Identity" section of `PIPER.user.md` — ADR-066 D7 convention). Still single-tenant (one configured username) — this is the seam D7 describes, not the multi-tenant migration itself; when `tenant_id` lands, this same config surface is where the principal-type evolution would land.

---

## Implementation sequencing (suggested for the refactor; not ADR-decision text)
1. **Doc store** (#1238) — the worked example: anchor (or `is_global` escape per D6) → unblocks the Radar Document source.
2. **`stakeholders`** — the People-entity backend (#1240 dependency).
3. **`(a,3)` leak paths** — add the read-side filter to the four named methods (D3).
4. **D4 resolution cleanup** — thread the principal as a required param across the 40+ sites, chain by chain (parallel track).
5. **D5 guards** — land each guard as its target population reaches zero violations (ratchet, like the F3 #1172 token-lint baseline).
6. **`user_id`→`owner_id` consolidation** — the deprecated-column migration, shim-then-drop.

*Don't pre-commit beyond doc-store-first; the rest sequences by the implementation PR fan-out.*

## Consequences

### Positive
- One canonical anchoring pattern; new content types inherit it by construction (recurrence closed).
- The (c,3) privacy gaps closed; trust property restored (CXO framing).
- The Radar entity-source backends build to a known contract; #1239 unblocked via the render-guard with no schema churn.
- D5 guards make the discipline self-enforcing (mechanism, not vigilance).

### Negative / tradeoffs
- The `user_id`→`owner_id` consolidation touches many call chains (m-40 shim window has dual-read complexity until chains migrate).
- The D4 cleanup is broad (40+ sites); WARNING-logged shims add transient noise.
- Per-user-render guards are defense-in-depth, not a substitute for eventual anchoring — they must not become a permanent excuse to skip it.

### Non-consequences
- Does **not** change the entity-model spec (PPM's lane — per-type lifecycle/fields).
- Does **not** implement multi-tenancy (D7 names the path only).
- Does **not** alter ADR-058 (credentials) — composes with it.

## Evolution
Single-tenant `owner_id` → multi-tenant `tenant_id` (D7). The per-user-render guards become `principal IN tenant_set`. Future ADR authors the multi-tenant model when BYOC scopes.

## Open questions (v0.1)
- **Exemption-list mechanism** (D1): marker column vs. code registry vs. docstring constant the D5 guard recognizes — three options; pick after the first migration attempt (cheaper post-evidence). Not committed in this ADR.
- **`conversation_turns`** transitive scoping — confirm it scopes via the `conversations` FK (likely; minor).
- Backfill policy for existing global doc-store rows — designated-PM-owner bucket vs. `is_global_content` escape (D6). Routes through cohort + PM at the doc-store PR.

## What this ADR is NOT
- Not the multi-tenant ADR (D7 names the path).
- Not the entity-model spec (PPM).
- Not a commitment to a specific migration order beyond doc-store-first.
- Not a commitment to a specific exemption-list mechanism.

## decisions.log entry (per CLAUDE.md recording-decisions discipline)
`2026-06-15 — ADR-071 v0.1 (Lead-authored, **Arch-ratified ~13:15 PT**): canonical user-auth anchoring pattern for content stores. owner_id FK canonical / user_id string deprecated / none forbidden (D2, consolidating refactor). Principal threaded as required param from the host boundary; the context.get("user_id") opportunistic re-fetch is the named anti-pattern (D4, 40+ sites). PM-domain cluster global-by-design with explicit-exemption + per-user-render-guard + tenant_id migration path (D1). AST guards (D5). Doc store + stakeholders remediate first (privacy). Grounded in the #1241 audit.`

---

## Appendix — audit evidence (the (a,3) leak paths + 2-axis classification)
From `dev/2026/06/15/1241-content-anchoring-audit.md`:
- **(c,3)** (no owner, global reads): ChromaDB doc store; `stakeholders`.
- **(a,3)** (owner-stamped, unscoped read path): `conversations.get_by_id():1544`; `insights.get_for_object():2316`; `knowledge_nodes` (conditional owner filter); `artifacts.get_by_id` (post-hoc).
- **(a,1)** (correct): conversational_memory; uploaded_files; lists; conversations (list/search/get_latest); insights (list_for_user/get_unsurfaced).
- **owner-anchored majority** via `user_id` (string) or `owner_id` (FK) — the inconsistency D2 consolidates.
- **resolution degradation**: 40+ `intent.context.get("user_id") … else None` sites (classifier.py, conversation_handler.py, intent_service.py).
- **global-by-design** (D1 ruling): products/features/work_items/intents/workflows/tasks.
