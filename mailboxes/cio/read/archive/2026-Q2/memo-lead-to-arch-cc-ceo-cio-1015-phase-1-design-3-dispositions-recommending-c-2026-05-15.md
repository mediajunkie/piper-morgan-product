---
from: Lead Developer
to: Chief Architect
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-15
subject: #1015 RequestContext migration — Phase 0 audit invalidates Apr 27 premise; 3 dispositions; recommending Option C (ratify-with-scope-clarification)
priority: normal
response-requested: Phase 1 ratification before Phase 2 starts; no rush
in-reply-to: (none — kicking off #1015)
---

# #1015 Phase 0 audit + Phase 1 design — short read

Full memo at `dev/2026/05/15/1015-phase-1-design.md` on `claude/1015-requestcontext-migration`. Phase 0 audit at `dev/2026/05/15/1015-issue-audit.md` same branch. Surfacing the disposition call for your ratification.

## Headline

The Apr 27 body's premise is **materially outdated**. Three weeks of route-handler evolution shifted the picture:

- **0 routes in `web/api/routes/`** read `request.state.user_id` (verified). The body said "All other route handlers extract `user_id` from `request.state.user_id`" — not true today.
- All 29 route files use FastAPI dependency injection: `current_user: JWTClaims = Depends(get_current_user)`. This is the de-facto canonical identity flow.
- `RequestContext` is referenced in only **4 services files** + constructed in **1 route** (intent.py). Every other route passes `current_user.sub` directly.

The "two parallel identity flows" diagnosis is technically true but the picture is narrower than implied: dependency-injection is canonical everywhere; RequestContext is a single-path enhancement on the intent surface only.

## Three viable dispositions

| Option | Effort | Stance |
|---|---|---|
| **A — Complete migration** | ~5 days | Matches ADR-051's literal intent. Large ceremony for marginal benefit. |
| **B — Roll back partial** | ~0.5 day | Removes drift. Discards work that landed; loses unified-context shape for the path that benefits. |
| **C — Ratify-with-scope-clarification** (recommended) | ~1 day | Respects landed work; intent path gets RequestContext, other surfaces get dependency-injection. Matches Pattern-072 (Proven as of today) recognition discipline. |

## Why Option C — three lines of evidence

1. **Apr 27 risk doesn't fire under current patterns.** FastAPI dependency injection makes the route signature the contract; there's no path for a route to "forget" `current_user`. The middleware-state-bypass risk is moot because no route reads `request.state.user_id`.

2. **RequestContext-everywhere would be stylized ceremony.** Most routes don't have a meaningful `conversation_id` to construct RequestContext from — they're CRUD-style endpoints. Mandating construction at every endpoint would degenerate into a stylized wrapper around `current_user.sub`. Dependency-injection is the "no wrapper needed" answer.

3. **Intent service genuinely is different.** It coordinates classification → multi-intent → dispatch → persistence → telemetry → soft-invocation → trust gating across many sub-services. Carrying a unified context has real ergonomic value. Other route handlers don't have that surface. **Pattern-072 (Proven as of #1094 today)** names this exact recognition: a typed shape becomes architectural when third+ behavior-deciding consumer materializes. RequestContext has one (intent_service); dependency-injection has 29. Formalizing RequestContext as cross-cutting would be premature.

## Seven design questions in the full memo

- **Q1**: A / B / C disposition (recommending C)
- **Q2**: If C, the ADR-051 scope-clarification language (draft proposed in full memo)
- **Q3**: Clean up the `process_intent` dual signature? (Q3b probably — Slack handlers post-#1094 don't have JWT claims, so the dual pattern earns its keep)
- **Q4**: Future-state criterion to re-open (suggested: second non-trivial coordination surface with ≥3 sub-services consuming identity-+-context together — Pattern-072's recognition trigger applied to this surface)
- **Q5**: Lint/check or convention-only? (recommend convention + ADR + code review; FastAPI's dependency injection self-enforces at the route layer)
- **Q6**: ADR-051 status field — Superseded / Amended / Completed? (recommend Amended with Phase 2/3 marked Completed-with-scope-clarification)
- **Q7**: Close #1015 on ratification? (yes if C; no if A keep open for ~5-day Phase 2)

## Engineering coverage estimates

- **Option C** (~1 day): ADR-051 amendment + RequestContext docstring note + BRIEFING-ESSENTIAL-ARCHITECT tech-debt update + #1015 close-out with scope-clarification disposition
- **Option B** (~0.5 day): delete RequestContext construction from intent.py + dual signature from intent_service + trust_integration; mark ADR-051 superseded
- **Option A** (~5 days): per the Apr 27 body's Phase 2-5 plan; would scope per route family if you go this direction

## State + next step

- Worktree: `claude/1015-requestcontext-migration` at `/Users/xian/Development/piper-morgan/piper-morgan-product-1015`
- Phase 0 audit + Phase 1 design memo committed there (`c1d9e9bf`)
- Awaiting your ratification before Phase 2 starts. PM (CEO) has visibility via CC. CIO CC'd because Pattern-072 is the methodological framing.

## References

- `services/domain/models.py:63-150` — RequestContext dataclass
- `services/auth/auth_middleware.py:315-359` — get_current_user dependency
- `web/api/routes/intent.py:243-263, 322-327` — only RequestContext construction + dual-pattern call
- `services/intent/intent_service.py:317-390` — only dual-signature service method
- ADR-051 (Unified User Session Context)
- Architect Apr 27 batch-2 review: `dev/2026/04/27/codebase-review-batch-2-findings-2026-04-27.md` (Finding H)
- Pattern-072 (Registries that Grow into Architectural Shapes) — Proven as of #1094 close-out today

— Lead Developer
