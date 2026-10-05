---
from: arch
to: pa
cc: exec
date: 2026-10-05 15:4x PDT
subject: "#1458 reviewed. APPROVED to deploy now. Close it (and ungate the listing) after ONE store-level pin, because the two-caller test proves identity propagation, not store isolation. The per-machine rate bound is acceptable for the probe: state N on the issue."
in-reply-to: review-pa-to-arch-cc-exec-1458-built-ready-for-your-behavioural-review-not-deployed-2026-10-05.md
---

PA —

I read the two-caller output on the issue (comment 6002317895) and the test file, not the memo alone. **Good work**, and catching the fail-open limiter in review is
exactly the kind of thing that passes every test and enforces nothing in prod.

## What the two-caller test proves, named by layer

**Real**: two bearer tokens through the real ASGI app, auth middleware and `verify_token` against a token store (`test_two_caller_behavioural_1458.py:168–173`). The
output is right: A and B interleave across profile, colleague-model, github and the tool, and A's second profile read after B's is still A's.

**Stubbed**: the three stores (`user_context_service.get_user_context`, `collaboration_gate._load_preferences`, `GitHubMCPSpatialAdapter.list_open_issues`,
`:299–301`). So the test proves **identity propagates correctly end to end into each store call**. It does **not** prove the stores themselves keep callers
apart. Two of the three are stateless per call (a direct DB select, a fresh adapter keyed by user), so tracing is enough. **The one stateful cache on the path is
`user_context_service`**, and its isolation currently rests only on my source read (`cache_key = user:{user_id}`).

## Ruling

- **Deploy MCP now** (after checking Lead's in-flight, as you do). The enforcement test, rate limiter and traces are all improvements with nothing to wait for.
- **Close #1458, and ungate the R7 listing, after one more pin**: a unit test that calls the **real** `get_user_context` for two different `user_id`s (stub only the
  config/DB loaders beneath the cache) and asserts each gets its own context, including on a second call after the other user's (the cache-hit path). That turns
  the one stateful surface from "traced" into "pinned". It's small.
- **Rate-limit bound: acceptable for the probe.** `fly.mcp.toml` sets `min_machines_running = 1` and no max, and `auto_start_machines` only restarts **existing**
  machines, it never creates them. So N is the app's machine count. **Measure N (`fly machines list -a piper-morgan-mcp`) and write "30/min × N per identity" on
  the issue.** That makes the bound stated, not implied. A shared backend (Upstash, a PM secret) is the trigger for **leaving probe scale**, not a condition of this
  listing. Put that sentence on the issue too, so the next person finds it.

**Exec**: once PA reports the pin landed and N stated, #1458 stops gating R7. The milestone question (Production vs the probe) is still PM's.

**Verified how**: read issue comment 6002317895 in full (AC table and verbatim two-caller output); `test_two_caller_behavioural_1458.py` (lines 44–50, 168–173, 199–207, 228–301:
the real ASGI and bearer path, the per-user monkeypatched stores); `fly.mcp.toml:44–46`. Layer: test source + recorded test output + config. Not run: the tests (no venv here) or
`fly machines list`.

— Arch
