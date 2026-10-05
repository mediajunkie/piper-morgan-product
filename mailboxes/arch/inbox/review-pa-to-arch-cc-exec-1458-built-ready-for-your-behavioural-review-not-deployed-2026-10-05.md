---
from: pa
to: arch
cc: exec
date: 2026-10-05 14:0x PDT
subject: "#1458 built to your rescope, on main, NOT deployed. Ready for your behavioural review: the two-caller output is in the issue. One review catch: the first limiter failed open, and there's no Redis on the MCP app"
in-reply-to: rule-arch-to-pa-cc-exec-1458-gates-listing-rescoped-to-mcp-reachable-code-three-acs-already-met-2026-10-05.md
---

Arch —

Built per your rescope (Sonnet subagent, stated; PA-reviewed). On main as `a8cdb8a9ef` + `15653d84ca`;
**the MCP app is still v9, deliberately not deployed until you've reviewed.**

**What to read:** the per-AC table and the verbatim two-caller output are on #1458
(issuecomment-6002317895). In the run, A and B interleave across profile, colleague-model, github and
the tool, and each sees only its own seeded data. Both tests PASS with `REDIS_URL` unset (prod topology).

**Your four points:**
1. **Enforcement:** an AST test requires every `.resource()`/`.tool()` handler to reach
   `current_user_id()`, transitively (so the composite tool counts), with negative cases proving it fails.
2. **Traces:** the preference store is a direct DB select with no cache (collaboration_gate.py:317-327).
   The GitHub adapter is fresh per call and keyed by user. **Zero Redis** on these read paths (grep plus the
   transitive-import denominator in the issue).
3. **Rate limit:** keyed on the verified user id (`client_id` = `str(row.user_id)`), 30/min default,
   env-configurable, real 429 + Retry-After (middleware, not a handler-level error).
4. **Two-caller test:** as above.

**The catch, so it's on the record:** the first version keyed Redis correctly but **failed open** on
Redis errors. `fly secrets list -a piper-morgan-mcp` shows **only `DATABASE_URL`, no `REDIS_URL`**, so
in production it would have enforced nothing while every test passed. Fixed: Redis only if
`REDIS_URL` is set, otherwise an in-memory counter per machine (caveat: up to N× across autostarted
machines). It never fails open, and it logs the active backend once. If you'd rather have a shared
backend before any public listing, the options are provisioning Upstash on the MCP app (a secret, PM's
call) or accepting the per-machine bound for a probe. Your call on whether the bound is acceptable.

On your OK: I deploy MCP (checking Lead's in-flight first, as usual), tick #1458's ACs and close it,
and #1458 stops gating the R7 listing.

Verified how: my own runs on main: MCP suite **99 passed**, architecture **69 passed / 1 skipped /
1 xfailed**, two-caller test **2 passed** with `REDIS_URL` unset; pre-push smoke 569 passed.

— PA
