# #1015 RequestContext Migration — Phase 1 Design Memo

**To**: Chief Architect
**CC**: CEO (xian), CIO (Chief Innovation Officer), Principal Product Manager
**From**: Lead Developer
**Date**: 2026-05-15 PM
**Subject**: #1015 RequestContext migration — Phase 0 audit invalidates the Apr 27 premise; three viable dispositions; recommending Option C (ratify-with-scope-clarification)
**Priority**: normal
**Response-requested**: Phase 1 ratification before Phase 2 starts

## Headline

#1015's Apr 27 body framed a partial-migration-stall (routes reading `request.state.user_id` while intent.py uses `RequestContext`). **The premise is materially outdated.** Phase 0 audit (2026-05-15, `dev/2026/05/15/1015-issue-audit.md`) confirms:

- **0 routes in `web/api/routes/` read `request.state.user_id`**. All 29 route files use `current_user: JWTClaims = Depends(get_current_user)` dependency injection.
- **RequestContext is referenced in only 4 services files** — `domain/models.py` (definition), `auth/auth_middleware.py` (type hints only), `intent/intent_service.py` (dual-signature consumer), `trust/trust_integration.py` (forwarded from intent path).
- **Only one route constructs RequestContext**: `web/api/routes/intent.py:249`. Every other route passes `current_user.sub` as a string user_id directly to services.

The "two parallel identity flows" diagnosis is technically true but the picture is narrower than the body implied: the dependency-injection pattern via JWTClaims is the de-facto canonical flow everywhere, and RequestContext is a single-path enhancement on the intent surface only.

## Three viable dispositions

| Option | Effort | Net | Stance |
|---|---|---|---|
| **A — Complete migration** | ~5 days | All routes construct `RequestContext` at boundary; all service signatures take `ctx: RequestContext`; ADR-051 Phase 2/3 done | Matches ADR-051's literal intent (single source of truth, never optional). Large ceremony for marginal benefit since `current_user.sub` already provides clean identity flow. |
| **B — Roll back partial** | ~0.5 day | Delete RequestContext construction from intent.py + dual signature from intent_service; mark ADR-051 superseded by the dependency-injection pattern | Removes the architectural-drift instance. Discards work that landed; loses the unified-context shape for the path that actually benefits from it. |
| **C — Ratify current state with scope-clarification** *(recommended)* | ~1 day | ADR-051 amended: RequestContext is canonical **for the intent path** (intent_service coordinates multi-step processing across many sub-services); for all other routes/services, dependency-injection via `current_user: JWTClaims` is canonical and sufficient | Respects the work that landed; clarifies the rationale; doesn't impose ceremony where it doesn't earn its keep. Matches Pattern-072 spirit. |

## Why Option C — three lines of evidence

### 1. The Apr 27 risk framing doesn't fire under current patterns

The body's risk statement: *"a route forgets to pass `ctx`, a service relies on `request.state.user_id` from middleware that's bypassed in a future refactor."*

Under FastAPI dependency injection, **the route signature IS the contract**. There's no path for a route to "forget" `current_user` — the function won't be callable without it. The middleware-state-bypass risk is moot because no route reads `request.state.user_id`. The risk surface the body worried about was real in a different middleware pattern; it's not a real risk under the current pattern.

### 2. RequestContext-everywhere would be stylized ceremony

`RequestContext.from_jwt_and_request(claims, conversation_id)` constructs a unified context from JWT claims + a conversation_id. **Most routes don't have a meaningful conversation_id** — they're CRUD-style endpoints (projects, lists, files, todos) that act on user-owned objects without conversational context. If every route had to construct RequestContext, every route would either pass a synthetic conversation_id or accept `Optional[RequestContext]` everywhere — degenerating into a ceremonial wrapper around `current_user.sub`.

The dependency-injection pattern is already cleaner: route signature declares the identity dependency, FastAPI injects it, routes use `current_user.sub` directly. RequestContext is the "wrapper" answer; dependency-injection is the "no wrapper needed" answer for paths that don't need the unified-context machinery.

### 3. Intent service genuinely is different

`intent_service.process_intent` coordinates: classification → multi-intent orchestration → handler dispatch → conversation persistence → telemetry → soft-invocation → trust gating. Carrying a unified context object (with user_id, conversation_id, request_id, user_email, formality_baseline) through that flow has real ergonomic value — without RequestContext, each of those sub-systems would re-extract identity from `user_id` strings.

Other route handlers don't have that surface. A `GET /api/v1/projects` endpoint makes a single repository call. A `POST /api/v1/todos` endpoint creates one ORM object. There's no multi-step flow that would benefit from carrying a context object.

**This isn't ad hoc — it's the same recognition Pattern-072 names** (Registries that Grow into Architectural Shapes, promoted to Proven today via #1094). The pattern says a registry / typed shape becomes architectural when third+ behavior-deciding consumer materializes. RequestContext currently has one real consumer (intent_service); the dependency-injection pattern has 29. Formalizing RequestContext as cross-cutting infrastructure would be premature.

## Seven design questions for ratification

### Q1 — Disposition: A / B / C?

Option C recommended for the reasons above. Open to Architect ratification or pushback to A / B.

### Q2 — If Option C, what's the ADR-051 scope-clarification language?

Proposed (subject to your edit):

> ADR-051 Phase 2/3 status: **Completed with scope-clarification**. `RequestContext` is the canonical identity-and-context object for the intent processing path (`web/api/routes/intent.py` → `services/intent/intent_service.py` → trust + conversation persistence + multi-handler dispatch). For all other route/service surfaces, the dependency-injection pattern (`current_user: JWTClaims = Depends(get_current_user)` at routes; `user_id: str` parameters in services) provides the canonical identity flow and is sufficient. The two patterns are not in conflict: dependency-injection is the boundary mechanism, RequestContext is the cross-handler coordination object for the intent path specifically. Adopting RequestContext beyond the intent path is a Pattern-072 recognition-trigger decision keyed to a second multi-handler coordination surface emerging.

Honest framing of why the partial-migration is the right end-state, not a stall.

### Q3 — Clean up the dual signature in `intent_service.process_intent`?

Current:
```python
async def process_intent(
    self,
    message: str,
    session_id: str = "default_session",
    user_id: str = None,
    ctx: Optional[RequestContext] = None,
) -> IntentProcessingResult:
    effective_user_id = str(ctx.user_id) if ctx else user_id
    effective_session_id = str(ctx.conversation_id) if ctx else session_id
```

Two cleanup options:

- **Q3a — Make `ctx` required when authenticated, deprecate user_id/session_id direct params**: forces intent.py to always construct ctx; drops the fallback path. Cleaner signature; one less branch.
- **Q3b — Leave as-is**: the dual signature absorbs unauthenticated cases (Slack handler dispatch, anonymous testing) where there's no JWT to construct ctx from. Cleaner ergonomics in tests.

Q3b probably right because the Slack handler path (post-#1094) calls `intent_service.process_intent` and doesn't have authenticated claims to construct ctx from. Worth confirming with you that the dual signature stays as the intent path's official shape.

### Q4 — Future-state criterion for re-opening the migration question?

If a second service domain emerges that needs cross-handler coordination (e.g., a new agent-routing layer, a workspace-aware multi-tenant flow with per-workspace state, a streaming-conversation lifecycle), that's the trigger to consider promoting RequestContext to cross-cutting. Until then, the partial adoption is the right end-state. Suggested criterion: **second non-trivial coordination surface with ≥3 sub-services consuming identity-+-context together**. Captures the spirit of Pattern-072's third-consumer threshold applied to this specific surface.

### Q5 — Lint/check to enforce the chosen pattern?

Proposed: ADR-051 v2 includes a written convention but no automated check. Reasons:
- The dependency-injection pattern is enforced by FastAPI itself (route signatures must declare the dependency)
- The "intent.py is the only RequestContext constructor outside services/" boundary would need a lint that knows the intent path is special — fragile to maintain
- If a developer needs to construct RequestContext somewhere new, that's the Q4 trigger to re-open the question, not a lint violation

Soft enforcement via convention + ADR + code review feels right for this size of surface.

### Q6 — ADR-051 status field: Superseded / Amended / Completed?

Recommend **Amended** (with Phase 2/3 marked Completed with scope-clarification per Q2). Superseded would suggest the entire ADR is replaced; Amended preserves the ADR's foundation while clarifying the scope.

### Q7 — Should this issue stay open or close on ratification?

If Option C ratified + Q2 wording landed in ADR-051 + Q3 disposition + Q4 future-state criterion captured → **close as completed-with-scope-clarification**. The issue's premise (incomplete migration) becomes "completed migration with intent-path scope, by ratification."

If Option A ratified → keep open for the ~5-day implementation work.

## Engineering coverage if Option C ratified (~1 day)

1. Update ADR-051 with the Q2 scope-clarification language (and Q3 + Q4 + Q6 + Q7 outcomes baked in)
2. Add docstring note to `RequestContext` defining its intent-path-specific role + Pattern-072 connection
3. Update BRIEFING-ESSENTIAL-ARCHITECT.md tech-debt list (mark #1015 resolved with disposition)
4. Close #1015 with status banner + AC checkboxes (most ACs marked N/A or completed-with-scope-clarification)

## Engineering coverage if Option A ratified (~5 days)

Per the Apr 27 body's Phase 2-5 plan. I'll need a more detailed estimate per route family if you go this direction.

## Engineering coverage if Option B ratified (~0.5 day)

1. Delete RequestContext construction from `intent.py:243-263`
2. Delete `ctx` param from `intent_service.process_intent` + `_process_intent_internal`
3. Delete `ctx` param from `trust_integration.py` consumer
4. Optionally: remove `RequestContext` dataclass entirely (or keep as dormant for future re-introduction)
5. Update ADR-051 to Superseded
6. Tests: ensure intent path still works without ctx (should — the fallback to user_id/session_id was already exercised)

## What I'm not changing without your call

- The recommendation. C is preliminary; you might pushback to A (we owe ADR-051 the migration) or B (we owe ADR-051 a clean death). I have a lean but I'd rather hear your read first.
- Any ADR-051 edits. Q2 wording is a starting point, not a commit.
- The dual signature in `intent_service.process_intent`. Q3a vs Q3b is your call.

## State

- Worktree: `claude/1015-requestcontext-migration` at `/Users/xian/Development/piper-morgan/piper-morgan-product-1015`
- Phase 0 audit committed there (`dev/2026/05/15/1015-issue-audit.md`)
- This memo will commit there and route via main per mailbox-discipline
- Awaiting your ratification before Phase 2 starts

## References

- `services/domain/models.py:63-150` — RequestContext dataclass
- `services/auth/auth_middleware.py:315-359` — get_current_user dependency
- `web/api/routes/intent.py:243-263, 322-327` — only RequestContext construction + dual-pattern call
- `services/intent/intent_service.py:317-390` — only dual-signature service method
- ADR-051 (Unified User Session Context)
- Architect Apr 27 batch-2 review: `dev/2026/04/27/codebase-review-batch-2-findings-2026-04-27.md` (Finding H)
- Pattern-072 (Registries that Grow into Architectural Shapes) — Proven as of #1094 close-out today; same recognition discipline frames this disposition

— Lead Developer
