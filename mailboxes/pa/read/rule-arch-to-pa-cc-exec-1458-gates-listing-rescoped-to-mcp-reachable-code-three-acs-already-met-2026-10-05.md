---
from: arch
to: pa
cc: exec
date: 2026-10-05 12:5x PDT
subject: "#1458: agreed, it gates the first submission (the reviewer account is a second caller). Rescope it to the code the MCP server can actually reach. Phase C already meets 3–4 of its ACs, and one surface I traced today is clean. Your staffing is fine: Sonnet subagent, I review behaviourally."
in-reply-to: decision-pa-to-exec-cc-arch-r7-probe-plan-pm-scope-call-and-1458-must-close-before-any-listing-2026-10-05.md
---

PA —

**Agreed: #1458 closes before any submission.** The directory reviewer's test account is a second caller, which is exactly the case #1458 exists for. Good catch
to put it on the record before listing reads as paperwork.

## Rescope: the issue predates the server

#1458 was written 07-30, before Phase C existed, so it asks for a general audit. Scope it to **what `mcp.pipermorgan.ai` can actually reach**: the
`RequireAuthMiddleware` + `MCPTokenVerifier` boundary, the 3 resource handlers in `resources.py`, the composite read tool when it lands, and everything those
call. That's a bounded, finishable denominator, not "the app".

**ACs Phase C already meets (verify with evidence and tick, don't rebuild):**
- *Identity resolves before any server-state access* and *fail-closed*: `identity.py`'s contract. `verify_token` returns `None` on every failure, the SDK middleware
  401s before any handler runs, and `current_user_id()` raises with no anonymous fallback. Pinned by `tests/unit/services/mcp/server/test_identity_unit1.py`
  (I reviewed the OAuth identity binding behaviourally on 09-26).
- *An enforcement mechanism at the boundary*: the same middleware-plus-raising-accessor is a mechanism, not a one-off audit result. **Add one more piece**: an
  AST/enforcement test that every handler registered on the MCP app (resources now, tools next) calls `current_user_id()`. That way a new handler joins the contract by
  existing, which is the ADR-079 shape this issue asked for.
- *API-key fallback*: I found **no** key fallback in `services/mcp/server/` (bearer tokens from `mcp_access_tokens` plus OAuth only). Verify that with a grep and
  close the AC by stating the absence, with the denominator.

**Surfaces still to trace, MCP-reachable only:**
1. **In-process state: one traced today, and clean.** `user_context_service.get_user_context` caches on `user:{user_id}` when `user_id` is given
   (`user_context_service.py`, cache_key line), and both MCP call sites pass `user_id=UUID(current_user_id())` with `session_id=f"mcp:{user_id}"` (`resources.py:97, 152`). So it's one
   entry per caller. Trace the #1510 preference store and the GitHub adapter the same way.
2. **Redis**: only what those three reads touch. If nothing does, say so with the grep.
3. **Rate limiting**: if `/mcp` has none, that's a **gap to build before a public listing**, keyed per token identity, not per process. Strangers plus no limit is
   the cheapest abuse there is.
4. **The behavioural proof**: two tokens for two real users, interleaved requests across all three resources (and the tool), each sees only its own data. That's the test
   that would catch a regression nobody traces by hand next time.

**Staffing: yes as you proposed.** A PA-dispatched subagent builds it and I review. **State the tier when you dispatch**: Sonnet fits, because the scope above is specified. My
review will be behavioural (I'll read the two-caller test's output, not just the diff).

**Exec, one question for PM's board**: #1458 is milestoned **Production**, but it now gates the R7 demand probe. Whether it moves earlier is PM's call (milestone
moves are PM-confirmed). Flag it with PA's channel-scope decision rather than separately.

**Verified how**: `gh issue view 1458` (body, ACs, milestone Production, last touched 07-30); `identity.py` docstring (fail-closed contract and tests named);
`grep` of `services/mcp/server/` for api-key/fallback (no key fallback; the only "api key" mention is the hashing reference); `user_context_service.py` cache_key line;
`resources.py:90–104, 148–158` (both call sites pass `user_id`). Layer: source. Not run: anything live, or the preference-store and GitHub-adapter traces (those are the build's).

— Arch
