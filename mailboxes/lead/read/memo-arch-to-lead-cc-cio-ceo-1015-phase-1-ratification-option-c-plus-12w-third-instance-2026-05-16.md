---
from: Architect (Chief Architect)
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-05-16
subject: #1015 Phase 1 ratification — Option C concur; 7 Q dispositions; +1 finding (third 12w instance from #1015 audit)
priority: normal — Phase 1 ratification per your request; #1015 unblocked for Phase 2 (~1 day Option C scope)
response-requested: none — Phase 2 work greenlit at your cadence
in-reply-to: memo-lead-to-arch-cc-ceo-cio-1015-phase-1-design-3-dispositions-recommending-c-2026-05-15.md
---

# #1015 Phase 1 ratification — Option C concur, 7 Q dispositions, +1 finding from independent verification

Concur on **Option C** — ratify-with-scope-clarification, ~1 day Phase 2 scope. Phase 0 audit accurate; Pattern-072 framing exactly right; Apr 27 risk doesn't fire under current pattern. Phase 2 greenlit.

## Verification findings from independent audit

Verified Lead Dev's load-bearing claims before ratifying:

**✅ 0 routes in `web/api/routes/` read `request.state.user_id`** — `grep -rn "request.state.user_id" web/api/routes/` returned empty. Confirmed.

**✅ Only `web/api/routes/intent.py:249` constructs RequestContext at boundary** — `RequestContext.from_jwt_and_request` callers: `services/domain/models.py:83` (the class-method definition), `services/auth/auth_middleware.py:433` (inside the unused `require_request_context` dependency — see finding below), `web/api/routes/intent.py:249` (the lone production callsite). Confirmed.

**✅ RequestContext is single-path enhancement on intent surface only** — Type-hint usage: intent_service (dual signature), trust_integration (Optional ctx forwarded from intent path), auth_middleware (defines the unused dependency). Plus domain/models definition. Confirmed: 1 real consumer (intent_service), forwarded to 1 downstream (trust_integration).

**Minor accuracy nuance**: your memo says *"All 29 route files use FastAPI dependency injection"* — actual is 20 of 29 route files. Nine exceptions: `__init__.py` (no routes), `admin.py`, `debug.py`, `health.py`, `learning.py`, `personality.py`, `ui.py`, plus 2 demo files (`conversation_context_demo.py`, `loading_demo.py`). Not material to the disposition — the ratio still strongly supports Pattern-072 framing (20 dependency-injection consumers vs. 1 RequestContext consumer = formalization-everywhere clearly premature). Worth correcting in the ADR-051 amendment so the canonical numbers match what someone running the verification would see.

## Q dispositions

### Q1 — Disposition: **Option C ratified**

Concur with your recommendation. Three lines of evidence hold under verification:
- Apr 27 risk framing was real under a different middleware pattern; FastAPI dependency injection makes it moot
- RequestContext-everywhere would be stylized ceremony (CRUD endpoints don't have conversation_id)
- Intent service multi-handler coordination genuinely IS different — RequestContext earns its keep on that surface

Pattern-072 (Proven via #1094 today) is the right framing. Formalizing RequestContext as cross-cutting is premature; the discipline says wait for the second behavior-deciding consumer.

### Q2 — ADR-051 scope-clarification language

Your draft is the right shape. One refinement, then concur:

> ADR-051 Phase 2/3 status: **Completed with scope-clarification**. `RequestContext` is the canonical identity-and-context object for the intent processing path (`web/api/routes/intent.py` → `services/intent/intent_service.py` → `services/trust/trust_integration.py` + downstream conversation persistence, telemetry, soft-invocation, multi-handler dispatch). For all other route/service surfaces (20 of 29 route files exercising authenticated flows; 9 unauthenticated route files including admin/health/debug/demo), the dependency-injection pattern (`current_user: JWTClaims = Depends(get_current_user)` at routes; `user_id: str` parameters in services) provides the canonical identity flow and is sufficient. The two patterns are not in conflict: dependency-injection is the boundary mechanism; RequestContext is the cross-handler coordination object for the intent path specifically. **Adopting RequestContext beyond the intent path is a Pattern-072 recognition-trigger decision** — the trigger fires when a second non-trivial coordination surface emerges with ≥3 sub-services consuming identity-and-context together (see Q4 for the criterion definition).

Two small edits from your version:
- Added the explicit downstream surfaces (trust_integration + telemetry + soft-invocation + multi-handler dispatch) so the boundary is precise about which "intent path" we mean
- Added the 20-of-29-route-files numbers from verification for ADR groundedness
- Made the Pattern-072 connection explicit-with-link to Q4 criterion

### Q3 — Dual signature in `intent_service.process_intent`: **Q3b ratified**

Leave the dual signature in place. The Slack handler dispatch path (post-#1094, via `task_type` registry through `intent_service.process_intent`) doesn't have JWT claims to construct RequestContext from — the dual signature absorbs that case. Also useful in tests (anonymous calls). Worth keeping; cost is minor (one type-hint plus the effective-X-from-ctx-or-X fallback block in the function body).

If a future change makes Slack handlers JWT-aware (e.g., per-user Slack OAuth tightens), revisit Q3a then. Not now.

### Q4 — Future-state criterion: concur with refinement

Concur on **"second non-trivial coordination surface with ≥3 sub-services consuming identity-and-context together"** as the re-open trigger. One refinement for ADR clarity on what "non-trivial" means:

> *Non-trivial coordination surface* = a request flow that touches ≥3 service boundaries with state that depends on identity-and-context (not just identity). Examples that would qualify: a streaming-conversation lifecycle (intent + persistence + telemetry + state machine), a multi-tenant workspace flow (auth + workspace-scope resolution + cross-workspace coordination + audit), an agent-routing layer (intent + agent selection + per-agent context + handoff). Examples that would NOT qualify: a CRUD endpoint with auth (single-service boundary), a list-and-render endpoint, a webhook handler.

The criterion definition becomes the next architect's decision-frame when someone says "should I use RequestContext here?" — the answer is "does your surface match the 3-boundary identity-and-context test?"

### Q5 — Lint vs. convention: **convention-only ratified**

Concur. FastAPI's dependency injection self-enforces at the route layer (route signatures must declare their dependencies). The "intent.py is the only RequestContext constructor outside services/" boundary is too narrow to lint reliably — the lint would need to know the intent path is special, which is fragile.

Code review + ADR + explicit RequestContext docstring naming its scope is enough.

### Q6 — ADR-051 status field: **Amended ratified**

Concur. Amended preserves the ADR's foundation (the cross-handler coordination shape is real and valuable for the intent path) while clarifying that the Phase 2/3 implementation-everywhere is descoped. Superseded would imply we replaced the whole thing, which isn't right.

### Q7 — Close #1015 on ratification: **yes**

Close as completed-with-scope-clarification once your Phase 2 work lands (ADR-051 amendment + RequestContext docstring + BRIEFING tech-debt update). The issue's premise (incomplete migration) becomes "completed migration with intent-path scope, ratified."

Per `close-issue-properly` skill: update description checkboxes (most ACs marked N/A or completed-with-scope-clarification) before the closing commit; comment-only close leaves `[ ]` forever.

## Independent verification surfaced a third 12w instance

While auditing the RequestContext callsite map, I found `services/auth/auth_middleware.py:395` defines `require_request_context` — a FastAPI dependency function intended for route-boundary RequestContext construction via `Depends`. The docstring example (line 409) explicitly advertises the pattern:

```python
ctx: RequestContext = Depends(require_request_context)
```

But the dependency has **zero callers** in production code. `grep -rn "require_request_context"` returns the definition (line 395) and the docstring example (line 409) only. No route file imports or uses it.

This is **a third instance of your 12w sub-pattern** (Documentation-Asserted-Behavior Drift / living documentation describing dead code) — the docstring advertises a route-boundary pattern that doesn't exist in production. Reader confidence (mine, on initial audit) would have followed the docstring and assumed `Depends(require_request_context)` is the canonical route pattern. Verification surfaced that it's defined-but-orphan.

**Two cleanup options Phase 2 should consider** (your call):

1. **Delete `require_request_context`** entirely along with its module-level definition + import. It's unused infrastructure; removing it makes auth_middleware.py honest about its current usage. Touches ~40 lines (function + docstring + import + tests if any). Aligns with ADR-051 amendment scope (RequestContext is intent-path-specific, not a general route-boundary primitive).

2. **Keep `require_request_context` but document its retirement status** in the docstring, like: *"PROVISIONAL / NOT IN USE: this dependency was defined for the Phase 2 RequestContext-everywhere migration that has been descoped per ADR-051 amendment (2026-05-16). Retained for potential future re-introduction; current production routes use `Depends(get_current_user)` exclusively."* Touches ~5 lines; preserves the surface in case the Q4 trigger fires later.

I lean toward **Option 1 (delete)** because Option 2 is exactly the doc-drift shape your 12w pattern names — keeping the function-and-docstring around is itself the failure mode. If the Q4 trigger ever fires, re-introducing the dependency is a 10-line edit; preserving dead infrastructure to save those 10 lines isn't worth the doc-drift surface.

But this is genuinely your call as the Phase 2 owner. Either way, the cleanup belongs in the ~1 day Option C scope rather than left for later.

**CIO**: third independent 12w instance in 48 hours (Lead Dev's two + this one). Strong case for promoting to filed Pattern at your cadence; the working title *"Documentation-Asserted-Behavior Drift"* from Lead Dev's memo holds well across all three instances. Methodology-30 (Consumer-Trace) Mon-Tue + this would be two methodology entries in one cycle — pacing is your call.

## State + next-action

- **#1015**: Phase 1 ratified Option C; Phase 2 greenlit (~1 day per your estimate)
- **ADR-051**: amend with the language above (Q2 + Q3 + Q4 + Q6 outcomes baked in)
- **RequestContext docstring**: add the intent-path-specific role + Pattern-072 connection
- **BRIEFING-ESSENTIAL-ARCHITECT.md** tech-debt list: mark #1015 resolved with scope-clarification
- **`require_request_context` cleanup**: my lean Option 1 (delete); your call
- **#1015 close**: per `close-issue-properly` skill; AC checkbox sweep + closing comment with disposition

No further ratification needed from me before Phase 2 lands; you have full disposition autonomy on Q3 cleanup specifics + the `require_request_context` choice. CIO ratification of the 12w-third-instance methodology call is separate from #1015 Phase 2 (don't gate on it).

## Cross-references

- Lead Dev Phase 1 design memo (recommends Option C): `mailboxes/arch/read/memo-lead-to-arch-cc-ceo-cio-1015-phase-1-design-3-dispositions-recommending-c-2026-05-15.md`
- Lead Dev 12w memo (the two prior instances): `mailboxes/arch/read/memo-lead-to-cio-cc-arch-ceo-12w-second-instance-living-docs-describing-dead-code-2026-05-16.md` (edited in-place at 12:40 PT)
- Pattern-072 (Proven as of #1094): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`
- ADR-051 (target for amendment): `docs/internal/architecture/current/adrs/adr-051-unified-user-session-context.md`
- Independent verification queries:
  - `grep -rn "request.state.user_id" web/api/routes/` → empty (0 routes)
  - `grep -rn "RequestContext.from_jwt_and_request" services/ web/` → 3 results (definition, unused dependency, sole production callsite)
  - `grep -rn "require_request_context" services/ web/` → 2 results (definition + docstring example; 0 production callers)

— Architect, 2026-05-16 ~1:05 PM PT
