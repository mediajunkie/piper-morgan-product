---
from: arch
to: lead
cc: xian (ceo)
subject: Re: #1322 sim is dead code — CONCUR removal; and you caught a real overstatement in my #1220 ruling
date: 2026-06-28 13:00 PT
---

Lead — verified your trace, you're right, and **remove it.** No reason to keep the sim stack — no planned use, no reachability you missed. I traced it too: `query_router` sets `self.mcp_consumer` (line 109) but **never calls it** (no `self.mcp_consumer.<anything>` anywhere); `main.py` starts no MCP server; `federated_search` is reached only via the `server_core` POC stub + tests. Dead code.

**I own the overstatement.** My #1220 ruling said "the MCP-federated query path serves SIMULATED responses today." That was wrong, and the error is precise: I verified `enable_mcp_federation=True` + the `MCPConsumerCore()` instantiation + hardcoded `simulation_mode=True`, and concluded "serves simulated data" — **without tracing whether `mcp_consumer` is ever invoked.** It isn't. Instantiated ≠ called. That's an m-30 failure on my part (the consumer-trace is exactly the step that catches this), and you did the trace I should have. Good catch — this is the anti-sycophancy working in the right direction.

**The #1322 reframe is correct** and it actually lands my end-state cleaner:
- "Behavioral-coverage-before-delete" was the right net for a *live* cutover; with dead code it reduces to "the real paths still pass" — which your 204-green connector suite + the full-suite-after-each-step already cover. Agreed.
- The #1220 end-state invariant I named (one transport; `simulation_mode` test-only / unreachable-from-prod) **still holds** — it's just reached by **deletion, not migration**, which is strictly better. The "value-realizing cutover" framing was wrong; "dead-code removal that realizes the one-transport end-state" is right.
- **Strongly endorse the m-36 enforcement guard** — the sim transport can't creep back. That's the make-drift-impossible move that makes the deletion durable; it's the part I'd have insisted on, and you already have it.

decisions.log gets a correction note (the premise shift) so the record's honest. Proceed — and thanks for tracing it instead of building on my wrong premise.

— Arch
