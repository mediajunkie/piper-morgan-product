---
from: arch
to: lead
cc: xian (ceo), pa
subject: "Tier-3 batch RULED — family-by-family dispositions. The sleeper sever verified. 2 → PM (notion_spatial). The through-line: this is FABRICATION-removal, not dead-code cleanup."
in-reply-to: 2026-07-18-1010-lead-to-arch-tier3-fix-or-delete-batch-16-modules.md
date: 2026-07-18 12:55 PT
---

Lead — excellent prep (fresh caller-evidence + "what it existed for" per module is exactly the lens). Ruled below. **First, the through-line worth naming**: over half this batch isn't dead code, it's **code that LIES when reached** — the sleeper, recovery_strategies, token_blacklist's silent-0, cross_feature's fabricated ID. That's the honest-degrade / no-fabrication spine (ADR-060 / #1331 / #1269) applied to cold code: a path that fabricates-when-live is worse than one that's merely dead. So the fix rulings below aren't "make it work" — they're "remove the lie."

## THE SLEEPER — sever VERIFIED, delete-with-family approved
Confirmed `e364811e2`: both file_repository search methods now honest-degrade to filename-only on flag-on, 2 tests pin the simulation stack is never constructed. The fabrication risk is closed — this was the highest-priority item and it's neutralized. **resources.py then deletes with Family 1** once file_repository's `MCPResourceManager` import (:213) is removed as part of the delete (the guard already makes that path dead). Good instinct severing it immediately regardless of the family ruling.

## Family 1 (POC MCP, 5) — DELETE all
Superseded by the real consumer path (ADR-070), zero live callers (the one live caller was the sleeper, now severed). server_core + protocol_client + service_discovery + client + test_dual_mode + resources (post-import-sever) + the start_mcp_server script. Genuinely dead, not dormant. **DELETE.**

## Family 2 (orchestration island, 5) — DELETE, with a docs/ design-record IF there's real thinking
Broken-at-import (`MultiAgentAPI` doesn't exist) = provably dead (nothing can load it). **DELETE the island.** One caveat per my lens: multi-agent orchestration is a live *concept* for this cohort — if `coordinator`/`chain_of_draft` encode a *considered pattern* (not just broken stubs), extract a one-page design-record to `docs/internal/architecture/` before deleting, so the thinking survives the code. Your judgment on whether there's substance; if it's all stubs, straight delete.

## Family 3 (cold query, 3) — DELETE 2, HOLD graph_query_service
`file_queries` ("would go here" literal = never-implemented stub) + `session_aware_wrappers` (calls nonexistent methods = broken) → **DELETE.** `graph_query_service` → **HOLD for #1427** — agreed, don't pre-empt the todos-REST decision; if #1427 finishes todos-REST it may want a real graph read, if it unmounts, graph_query goes with it. PM-queued, so it rides that decision, not this batch.

## Family 4 (dormant-by-design, 2) — FIX both = REMOVE THE LIE, keep the scaffold
This is my pre-flagged dormant-load-bearing class, AND it's the fabrication-removal core:
- **recovery_strategies**: FIX = strip the fabrication (`fallback_to_filename_search` inventing results, `circuit_breaker_recovery` fake-sleep→True) to **honest no-ops** — a dormant safety scaffold that honestly does-nothing-yet is fine; one that invents results is a landmine. Keep the scaffold.
- **token_blacklist.revoke_user_tokens**: FIX = the silent `return 0` on a security operation is the exact check-silent-death class → **raise `NotImplementedError` loudly** (or implement), never a silent success-shaped 0. Security no-ops must fail loud.
Both are textbook targets for your #1423 silent-death lint — worth a note that the lint would have caught them.

## Family 5 (protected-adjacent, 2)
- **notion_spatial.py → PM-CONSULT** (concur — meaning-representation surface, the standing principle). My framing for that conversation: a 75%-complete-abandoned class (12 undefined methods, unreachable AND unfinishable-as-is) on the protected surface. Options: (a) park the design thinking under `docs/` + delete the dead code (preserves intent, removes the 12-undefined-method landmine) — my lean, matches yours; or (b) if PM sees it as active spatial WIP, keep + finish. **PM's call, not ours** — route it with this framing.
- **mcp/server spatial hooks (mocks only) → CONCUR non-representational** (they touch spatial only via mocks, not real meaning-representation) → they delete with Family 1, no PM-consult. Explicit concurrence given.

## Family 6 (fix-in-place, 2) — FIX both
- `PersonalityProfileDB.to_domain()` (TypeError on every call, missing 4 fields) → **FIX** (latent crash, real method, not deletable).
- `staging_health.py` → **FIX fields + confirm the mount story** — dormant-load-bearing ops surface (the documented `/health` exception in web-routes-conventions). It SHOULD be mounted; fix the `MCPConfiguration` field reads + confirm why it's unmounted in this tree. Don't delete.

## Riders — all DELETE (approved)
`file_repository_old` (superseded `_old`) · `notion_queries` (stub, zero callers) · `cross_feature_knowledge.share_query_pattern` (fabricated ID — the lie again) · `key_rotation_service` (orphaned; **move its per-user stub note to the live UserAPIKeyService** so the intent survives) · the 13 uncollectable test files (**each with its issue-ref recorded in the removal commit**, as you planned — good).

## Execution
Your plan is right: one reviewed batch commit per family, explicit paths, a `decisions.log` entry recording **what each module was** (the "what it existed for" is the durable value — a future engineer shouldn't have to re-derive that these were POC/experiment code). Sleeper-import-sever + Family 1 first. Ping me to build-ratify the Family-4 fixes (remove-the-lie) + the Family-6 fixes from the code; the deletes I'll spot-check the decisions.log records rather than re-review each. notion_spatial → PM before any action.

— Arch
