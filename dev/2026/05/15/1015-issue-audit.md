# #1015 RequestContext Migration — Phase 0 Audit

**Date**: 2026-05-15 PM
**Author**: Lead Developer
**Branch**: `claude/1015-requestcontext-migration` (worktree)
**Issue**: #1015 ARCH: Complete ADR-051 RequestContext migration — finish Phase 2/3 partial adoption

## Headline finding

**The Apr 27 issue body's specific premise is materially outdated.** Three weeks of route-handler evolution have shifted the identity-flow picture. The dual pattern still exists but in a much narrower scope than the body described. The "Complete Phase 2/3 migration" framing isn't the only viable disposition — three are viable, and the right call depends on whether RequestContext earns its keep relative to the dependency-injection pattern that's already canonical everywhere else.

## What the Apr 27 body said

> "All other route handlers (personality.py, documents.py, todos.py, projects.py, files.py, lists.py, work_items.py, learning.py, settings_integrations.py, repositories.py, conversations.py, feedback.py, etc. — most of `web/api/routes/`) extract `user_id` from `request.state.user_id` (set by AuthMiddleware), bypassing RequestContext entirely"

The body's mental model: routes read `request.state.user_id`; one route (intent.py) constructs RequestContext; the gap is wide and growing.

## What's actually in the code (verified 2026-05-15)

### Route handlers (29 files in `web/api/routes/`)

**None** of them read `request.state.user_id` directly. The pattern across the board is FastAPI dependency injection:

```python
from services.auth.auth_middleware import get_current_user

@router.get("/...")
async def some_route(
    current_user: JWTClaims = Depends(get_current_user),
    ...
):
    user_id = current_user.sub
```

`get_current_user` extracts the JWT from Authorization header or cookie, validates it, and returns `JWTClaims`. AuthMiddleware also sets `request.state.user_id` as a side-effect (still happens at `services/auth/auth_middleware.py:176`), but **no route in `web/api/routes/` reads `request.state.user_id`** (verified via `grep -c "request.state.user_id" web/api/routes/*.py` — all zero).

The dependency-injection pattern is the de-facto canonical identity flow today. It's cleaner than the body's described state because identity is extracted at the route signature level, not pulled from middleware state.

### RequestContext adoption

`RequestContext` (defined `services/domain/models.py:63-150`) is referenced in only **4 files** in `services/`:

| File | Role |
|------|------|
| `services/domain/models.py` | Defines `RequestContext` dataclass + `from_jwt_and_request()` factory |
| `services/auth/auth_middleware.py` | Imports — but uses only for type hints in the middleware layer (doesn't construct or pass) |
| `services/intent/intent_service.py` | Receives `ctx: Optional[RequestContext]` in `process_intent()` + `_process_intent_internal()`; extracts `effective_user_id = str(ctx.user_id) if ctx else user_id` |
| `services/trust/trust_integration.py` | Type signature accepts `ctx: Optional[RequestContext]` (called from intent path) |

Only **one route** in `web/api/routes/` constructs RequestContext: `web/api/routes/intent.py:249` — `ctx = RequestContext.from_jwt_and_request(claims=current_user, conversation_id=session_id)`. Every other route uses `current_user.sub` directly.

### Service-layer signatures

Services accept `user_id: str` and `session_id: str` as primary identity parameters across the board. Sample:

- `services/personality/personality_profile.py:74` — `user_id: str`
- `services/personality/conversation_analyzer.py` — every method takes `user_id: str` (10+ occurrences)
- Repository methods: `repo.get_by_owner(ctx.user_id)` is rare; `repo.get_by_owner(user_id)` with a string is the norm

The `ctx: Optional[RequestContext] = None` dual-pattern parameter exists ONLY in `intent_service.process_intent()` and its `_process_intent_internal()` helper. No other service has this dual signature.

## What this means for the migration call

The Apr 27 body framed two options implicitly: complete the migration or let the dual pattern persist. The actual state surfaces a third (or strengthens the "leave it alone" case):

### Option A — Complete the migration (Architect Apr 27 implied)

Every route constructs RequestContext at the boundary. Every service signature requires `ctx: RequestContext` (or kwarg-only with deprecation on the old params). ADR-051 Phase 2/3 marked done.

**Effort**: ~5 days. 28 route files need RequestContext construction at every endpoint that touches user data (~20-25 functions touched in projects.py + lists.py + standup.py + todos.py + settings_integrations.py alone). All service signatures change.

**Pro**: matches ADR-051's stated intent ("single source of truth, never optional, never reconstructed").

**Con**: massive surface change for marginal benefit. `current_user.sub` is already the canonical identity at every route; wrapping it in RequestContext at every endpoint adds ceremony without changing what's actually flowing through.

### Option B — Roll back the partial migration

Delete RequestContext construction from intent.py + delete the dual signature from intent_service.process_intent(). Mark ADR-051 superseded by the dependency-injection pattern. Update ADR-051 to "Superseded — current pattern: `current_user: JWTClaims = Depends(get_current_user)` provides cleaner identity flow than RequestContext layer."

**Effort**: ~0.5 day. Delete ~40 LOC from intent.py + intent_service.py; update ADR-051; commit.

**Pro**: removes the only architectural-drift instance. The dependency-injection pattern is provably working everywhere else.

**Con**: discards the work that landed (ADR-051 Phase 2 + Phase 3 partial). Anyone who specifically wanted the unified-context shape (e.g., multi-tenant workspace_id, request_id tracing, formality_baseline pre-loading) would need to reconstruct that case.

### Option C — Ratify the current state as canonical

Declare the partial migration the **completed** end-state. ADR-051 Phase 2/3 marked done-with-scope-clarification: RequestContext is the canonical identity object **for the intent path** specifically (because intent_service has unique needs — coordinates multi-step processing across many sub-services, benefits from a unified context object). For all other paths, the dependency-injection pattern via `current_user: JWTClaims` is canonical and sufficient.

**Effort**: ~1 day. Update ADR-051 with the scope-clarification. Add a docstring note to `RequestContext` defining its intent-path-specific role. Audit the intent path to ensure dual-pattern handling is robust (e.g., ctx-when-authenticated, fallback when not). Possibly merge the `ctx is None` and `ctx is not None` branches in intent_service for cleaner code. Update BRIEFING-ESSENTIAL-ARCHITECT.md.

**Pro**: respects the work that landed; clarifies the rationale; doesn't impose ceremony on routes that don't need it. Matches Pattern-072 spirit (a registry/shape becomes architectural only when third+ behavior-deciding consumer materializes — RequestContext has one real consumer today, intent_service).

**Con**: requires explicit framing of "intent_service is special" which some engineers will find ad hoc. Mitigation: document the special-ness clearly in ADR-051.

### Why Option C is the right call (preliminary recommendation)

Three lines of evidence:

1. **No evidence the dual pattern bites in practice.** No bug reports, no in-production failures attributed to the dual identity flow. The Apr 27 risk framing ("a route forgets to pass ctx") isn't a real risk under FastAPI's dependency-injection pattern because the route signature is the contract — there's no path for a route to "forget" `current_user`.

2. **The dependency-injection pattern is cleaner than RequestContext-everywhere would be.** RequestContext is itself constructed from `claims`; if every route had to construct it, every route would do `ctx = RequestContext.from_jwt_and_request(claims=current_user, conversation_id=???)` — and most routes don't have a meaningful `conversation_id`. The construction would degenerate into a stylized wrapper around `current_user.sub` for most routes.

3. **Intent service genuinely is different.** It coordinates classification + dispatch + multi-handler routing + conversation persistence + telemetry across many sub-services. Carrying a unified context object through that flow has real ergonomic value. Other route handlers don't have that surface; they make a single repository call or a single service call.

Option C ratifies the working pattern, documents the rationale, and avoids the make-work of Option A.

## Phase 1 design questions (for the design memo)

1. **A / B / C disposition** — which option does Architect concur with?
2. **If Option C**: how should ADR-051 v2 read? Specifically, what's the scope-clarification language that doesn't sound ad hoc?
3. **If Option C**: should the dual-pattern in `intent_service.process_intent` be cleaned up (e.g., make `ctx` required when authenticated, simplify the `effective_user_id = ...` extraction)?
4. **If Option C**: any future-state criteria that would re-open the migration question (e.g., if a second service domain starts needing a unified context, that becomes Pattern-072's third-consumer trigger for RequestContext-as-registry-architecture)?
5. **What's the criterion for "this is settled"?** The risk in leaving #1015 open is the perpetual drift the Apr 27 finding worried about. The risk in closing as Option C is calcifying the special case. Whichever option ratified, what's the signal that the disposition is durable?
6. **Test coverage** — do we want a lint/check to enforce the chosen pattern? E.g., "no route in `web/api/routes/` may read `request.state.user_id`" or "intent.py is the only constructor of RequestContext outside services/".
7. **ADR-051 status** — Superseded, Amended, or Phase-Complete? Naming matters because Architect's roadmap-of-ADRs uses these statuses with specific meanings.

## Out of scope (for clarity)

- Adding new RequestContext fields (workspace_id is already there with DEFAULT_WORKSPACE_ID; multi-tenant work is downstream)
- Changing the auth model (JWT extraction is working)
- Migrating away from FastAPI dependency injection (it's the cleanest pattern; not on the table)

## Worktree state

- Branch: `claude/1015-requestcontext-migration`
- Worktree: `/Users/xian/Development/piper-morgan/piper-morgan-product-1015`
- This audit committed here; Phase 1 design memo will follow in the same worktree before routing to Architect via main.

## References

- `services/domain/models.py:63-150` — RequestContext dataclass + factory
- `services/auth/auth_middleware.py:176, 315-359` — middleware sets state, dependency-injection extracts JWT
- `web/api/routes/intent.py:243-263, 322-327` — only RequestContext construction site + dual-pattern call
- `services/intent/intent_service.py:317-390` — only dual-signature service method
- ADR-051 (Unified User Session Context) — original intent
- Architect Apr 27 batch-2 review: `dev/2026/04/27/codebase-review-batch-2-findings-2026-04-27.md` (Finding H)
- Pattern-072 (Registries that Grow into Architectural Shapes) — Proven as of today; same recognition discipline applies to RequestContext-as-context-registry
