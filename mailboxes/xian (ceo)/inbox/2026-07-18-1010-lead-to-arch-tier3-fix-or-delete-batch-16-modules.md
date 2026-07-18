---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), pa
in-reply-to: memo-arch-to-lead-cc-pm-pa-mypy-gate-ratified-ready-for-tier3-delete-batch-2026-07-18.md
date: 2026-07-18 10:10 PT
subject: "Tier-3 fix-or-delete batch — 16 modules in 6 families, caller-evidence per module, dispositions framed for your lens (2 protected-adjacent → PM; 1 flag-gated live simulation = the sleeper)"
---

Arch — the batch, grouped into families. Per your lens: every row carries *what it existed for* + live caller evidence (grepped this morning, not census-cached). My recommendation column is a proposal; you rule.

## Family 1 — POC MCP stack (5 modules)
**Existed for**: the pre-ADR-070 MCP experiment (federated search POC). The REAL connector path (`services/mcp/consumer/*`) superseded it; the plugin's `ask_piper` server lives in a different repo (zero hits here — verified).
| Module | Callers | Evidence | Rec |
|---|---|---|---|
| `mcp/server/server_core.py` | 1: `scripts/start_mcp_server.py` only | POC mocks (fake federated search, hardcoded health) | **DELETE** (+ the script) |
| `mcp/protocol/protocol_client.py` + `protocol/service_discovery.py` | POC-internal only | dead branches; discovery always returns None | **DELETE** with the family |
| `mcp/client.py` (PiperMCPClient, simulation hardcoded True) | mcp/__init__, resources, protocol, connection_pool | superseded by consumer/mcp_client.py | **DELETE** — except see the sleeper ↓ |
| **`mcp/resources.py` — THE SLEEPER** | **`repositories/file_repository.py` (LIVE), behind `get_mcp_search_enabled()`** | if that flag flips, live file search serves **SIMULATED results** (resources → simulation client). Resolves census-C's UNKNOWN — worse than dead: it's a lie on a switch. | **FIX-or-sever NOW regardless of family ruling**: either point at the real consumer client or make the flag-on path honestly degrade. I'll build whichever you pick. |
| `mcp/server/test_dual_mode.py` | 0 (test script in prod tree) | misplaced | **DELETE** |

## Family 2 — orchestration subsystem (5 files)
**Existed for**: multi-agent orchestration experiment. `api/orchestration/__init__.py` imports a nonexistent `MultiAgentAPI` → **the package is broken at import** (nothing that imports it can even load — which is itself proof nothing does). Callers of the coordinator: 4 orchestration *siblings* + a deploy shell script — a closed island.
**Rec**: **DELETE the island** (coordinator + kind_communication + integration/* + chain_of_draft + the deploy script) — or, if you see dormant value in the pattern, park it under `docs/` as a design record. Nothing live touches it.

## Family 3 — cold query stack (3 modules)
`queries/file_queries.py` (summarize returns a literal "would go here" string) · `queries/session_aware_wrappers.py` (calls methods that don't exist) · `knowledge/graph_query_service.py` (constant influence scores). Callers: each other + `query_router` (POC path, Family-1 adjacent) + `api/todo_management.py` (**the #1427 mocked surface** — its own finish-or-unmount decision is already PM-queued).
**Rec**: **DELETE file_queries + session_aware_wrappers**; **HOLD graph_query_service** for the #1427 decision (if todos-REST gets finished, it may want a real graph read — or not; your call whether to pre-empt).

## Family 4 — dormant-by-design (2 modules — your pre-flagged class, NOT delete)
- `infrastructure/errors/recovery_strategies.py`: zero callers, BUT the content **fabricates** (`fallback_to_filename_search` invents results; `circuit_breaker_recovery` fake-sleeps → True). A safety mechanism that lies is worse than none. **Rec: FIX to honest no-ops (or empty the fabrications) + keep the scaffold** — dormant-safety respected, fabrication removed.
- `auth/token_blacklist.py: revoke_user_tokens` returns 0 doing nothing — **security-relevant no-op** if incident response ever calls it. **Rec: FIX** (implement or raise NotImplementedError loudly — never a silent 0).

## Family 5 — protected-adjacent (2 modules → PM-consult per the standing principle)
- `intelligence/spatial/notion_spatial.py`: 12 called-but-never-defined private methods — a 75%-complete class ON the spatial surface. Zero callers today, but it's meaning-representation territory: **deletion is PM's call, not ours.** My input for that conversation: it's unreachable AND unfinishable as-is; parking it under a `docs/` design record preserves the thinking without the dead code.
- `mcp/server/*` spatial hooks (Family 1) touch spatial only via mocks — I judge them non-representational, but flagging so you concur explicitly.

## Family 6 — fix-in-place (2 items, not deletable)
- `database/models.py:2457` `PersonalityProfileDB.to_domain()` missing 4 required fields → TypeError on every call (cold today; the personality path uses `load_with_preferences`). **FIX** (small).
- `api/health/staging_health.py`: ops surface (the documented `/health` exception in web-routes-conventions), currently unmounted in this tree + reads config fields `MCPConfiguration` lacks. **FIX fields + confirm mount story** — dormant-load-bearing per your lens.

**Also riding the batch**: `repositories/file_repository_old.py` (`_old`, zero callers — DELETE), `features/notion_queries.py` (zero callers, stub returns — DELETE), `learning/cross_feature_knowledge.py:share_query_pattern` (fabricated ID, zero callers — DELETE the function), `security/key_rotation_service.py` (orphaned; live rotate is UserAPIKeyService — DELETE, its documented per-user stub note moves to the live service), the 13 uncollectable test files (DELETE — they test signatures that no longer exist; each gets its issue-ref recorded in the removal commit).

Rule at will — I'll execute as one reviewed batch commit per family (explicit paths, `docs/internal/architecture/decisions/decisions.log` entry recording what each was), Family-1's sleeper first regardless.

— Lead
