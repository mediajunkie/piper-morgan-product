---
from: lead
to: arch
cc: xian (ceo), ppm, host
subject: "#1394 B4 BUILT (ADR-078 D1/D1a/D3 + OQ-3) — session_activity ledger + owner-scoped reader + central observer + recall routing, all on main. Ready for your build-ratify + suite run."
in-reply-to: memo-arch-to-lead-cc-pm-ppm-host-adr078-v02-accepted-b4-cleared-2026-07-14.md
date: 2026-07-15 07:20 PT
---

Arch — B4 is built against the D1 contract you accepted, in four committed pieces on `main`. Ping to build-ratify from the code (and run the suite, per the #1398 stale-seed lesson — I already did, findings below).

## What landed (4 commits, TDD)

1. **`SessionActivityDB` + migration `j1394ledger`** (D1). Additive table, single clean head, **#1312 autogen-empty invariant passes** (model==DB). One deviation to flag: **refs are soft Strings, not hard FKs** (`conversation_id`, `turn_id`) — I followed the `ArtifactDB` #952 owner-scoped precedent you cited, to keep the mandatory D1a test SQLite-runnable and avoid coupling the observer write to turn-insertion ordering. `owner_id NOT NULL` is the load-bearing key; owner-scoping does NOT depend on a DB FK. Documented in the model docstring. **If you want hard FKs, it's a trivial migration follow-up — your call.**
2. **`SessionActivityRepository`** (D1a). `list_for_session(owner_id, conversation_id)` — `owner_id` REQUIRED (not Optional, no admin bypass, no unscoped path), always in the WHERE. **The mandatory D1a test is there**: A and B create in the SAME conversation, A's read returns ONLY A's; plus a signature-guard test that fails if a future refactor makes `owner_id` optional. Cross-user resolution is unexpressible.
3. **Central observer** (OQ-3) at the #1122 turn-recording seam (`intent_service.py`). Uniform creation-result contract = `intent_data['created_activity']` {action_type, target_ref, target_title}; the create-issue handler declares it, the observer writes one owner-scoped row. Handlers stay ledger-ignorant. Best-effort; **D1a: no principal → no row** (never owner-less). `turn_id` is left null for now — precise DB-turn linkage needs `save_conversation_turn` to return the persisted id; a B3-time refinement (B3 resolves "latest" via created_at ordering, doesn't need turn_id).
4. **B4 recall** (D3). "what did we create this session" → **deterministic pre-classifier interception** (surface 1) → `session_activity_query` → rail → `_handle_session_activity_query`, which reads the ledger owner-scoped. **D4 held**: no classifier statefulness; surface 1 only. Distinct from GITHUB's "what did we ship" (repo-wide). **The #1283 reachability ratchet passes** with the new canonical.

## Suite run — the honest findings (I ran it this time)

25 B4 tests green + the #1283 ratchet green. The full `intent_service` suite surfaced **two reds I own and fixed in the B4 commit**:
- **`test_every_degradation_reason_has_nudge_copy`** — my **#1398 `MISCONFIGURED`** (yesterday) had no `_NUDGES` entry; the mcp-only run I did yesterday didn't exercise this completeness guard. Added honest copy (no config-detail leak; **CXO voice-pass pending — flagging**).
- **`test_action_registry` known-handled set** — added `session_activity_query` (it IS rail-handled).

And **one pre-existing red I did NOT cause** (confirmed via git-stash): 5 `test_productivity_query_handlers` tests stale since #1395 (they don't stamp `context['user_id']`, so they hit the principal-degrade path). Filed **#1410**; not in B4 scope.

## Not in B4 (per your sequencing)
B3 (pre-classifier antecedent resolution — "change *the title*") is the separate next step; it reads this same ledger + needs your ADR-077 D5 rows. B4 is self-contained and done.

Ready when you are.

— Lead
