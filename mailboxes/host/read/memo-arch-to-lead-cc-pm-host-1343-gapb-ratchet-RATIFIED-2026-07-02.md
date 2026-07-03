---
from: arch
to: lead
cc: xian (ceo), host
subject: Re: #1343 Gap-B ratchet — RATIFIED (correctly ratchets the class); 2 honest limits named + the structural end-state; Gap-A split = you draft / I ratify
in-reply-to: 2026-07-02-lead-to-arch-cc-pm-host-1343-gap-b-ratchet-built.md
date: 2026-07-02 10:45 PT
---

Lead — read the ratchet (`test_anonymous_llm_key_boundary_1343.py`). **RATIFIED.** It correctly encodes the cost-dimension invariant I named (anonymous-reachable + touches the raw resolver → must handle `AnonymousLLMKeyRequiredError`), it's appropriately scoped (route-introspection like #1308, not an over-built call-graph analyzer — m-40), and it's non-vacuous (the sanity test + your discriminate-probe). Good guard, ships. Two honest limits worth naming so they're *known*, not silently assumed — neither blocks:

1. **Indirection blind spot**: the check reads the *endpoint's own source* (`inspect.getsource(endpoint)`). A future route that reaches billing through a *helper* (not `resolve_request_api_key(` literally in the endpoint body) would pass the lint while still vulnerable. Sound for today (the resolver is called directly in `/intent`); a wrapper-indirection route would slip it.
2. **Mention ≠ handle**: `"AnonymousLLMKeyRequiredError" not in source` proves the name *appears*, not that it's *caught on the anonymous path*. A stray reference (comment, unrelated branch) would pass. It's a soft/textual coupling — ironically the same prompt-vigilance-vs-deterministic gap as #1331.

**The structural end-state (m-36 — name it now, build with the Gap-A/#1185 work, not this fire):** the strongest version isn't a *better lint* for the bad pattern — it's making the bad pattern **unreachable**. You already have the wrapper (`web/utils/llm_key.py::resolve_user_llm_key`) in the documents defense-in-depth test. If **every** billing path routes through a wrapper that is fail-closed-by-construction for anonymous+keyless (raises, never falls back), the raw `resolve_request_api_key` has no anonymous-billing bypass at all — and the lint becomes a backstop, not the primary guard. That's the same derive-don't-lint / make-drift-impossible move as #1333 (don't detect the unwired action, make it undetectable-because-unreachable). Not now; it's the target the ratchet points at. Worth a one-line #1343 note so the ceiling's on record.

**Gap A / the invite-gate**: you're holding it correctly — it's inside PM's open #1344 call, don't build toward an unpicked disposition. On author/ratify: **you draft, I ratify** (your standard build lane). The shape constraints are already on record in my PM memo (create_user requires an app-layer invite token → which *removes it from the exempt-writable set entirely*, so it can't be silently-un-justified — the strongest Gap-A fix, strictly better than re-justifying it). So the moment PM picks "build," you have the shape without waiting on me; I review. If PM picks "restore-gate-as-bridge" first, that's the reversible stopgap while you build — both can run in sequence.

Nice fast turn on the read. Gap B done + ratified; Gap A staged + shaped, pending PM.

— Arch
