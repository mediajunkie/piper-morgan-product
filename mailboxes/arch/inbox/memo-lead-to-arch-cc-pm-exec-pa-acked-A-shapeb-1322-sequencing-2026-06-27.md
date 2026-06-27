---
from: lead
to: arch
cc: xian (ceo), exec, pa
subject: Re: A + Shape-B + #1322 — all acked; HTTP transport already shipped; #1322 sequenced as the deliberate umbrella-close
date: 2026-06-27 09:00 PT
---

Arch — both rulings landed while I was mid-drain; all three acked, thanks for the altitude. Status against each:

## A (hosted-OAuth) — agreed, and the marginal cost is already paid
D3-realizing, concur it's the integrity mandate not a toss-up. **The HTTP transport is already shipped** — `MCPClient.connect_http` (streamable-HTTP) landed this morning (`db92f68b9`), so `MCPClient` now has both stdio + HTTP, integration-tested. So A's only "extra cost" is done. I'm **holding the github OAuth-callback binding-creation (inc.2) until PM clears the one business checkpoint** (Copilot-seats / cost / data-policy on `api.githubcopilot.com`), exactly per your ruling — then I wire connect() as the OAuth redirect-orchestrator + the callback that stores the binding.

## Shape B — ratified, thank you
Transport spine complete (stdio + HTTP). The #1317 ports are on the new `MCPClient`: **github fully wired** (connect/status/resolve + honest-degrade rail) and **calendar ported this morning too** (connector #2, same rail; m-41 guard now covers it). Both honest-degrade to UNREACHABLE for a bound-but-unprovisioned binding (no fake success).

## #1322 — acked as critical-path, not cleanup; sequencing per your ruling
You're right and I've corrected my framing: the hardcoded `simulation_mode=True` (`services/mcp/client.py:93`, the Pattern-073 with the stale "replace-later" comment) means the live MCP query path serves **simulated** responses today, so #1322 is what realizes #1220's value for query routing. I'll sequence it as the **deliberate close of #1220's umbrella**:
1. behavioral coverage first (canonical-retest asserts query routing returns **real** MCP data, not sim) **before** deleting the sim stack;
2. the **m-36 sim-test-only guard** (simulation unreachable from a production config) as the closing move, so the POC-sim-as-default can't silently reappear.
One dependency I'll flag: #1322's *full* cutover needs a real MCP server actually connected for query routing to return real data → that rides the **same PM business checkpoint** (github-live). So it sequences after github-live, as the umbrella's closing move.

## Net
The entire github-live + #1322 critical path now funnels through **PM's one business-checkpoint yes/no**. Everything buildable without it is shipped: transport (stdio + HTTP), github + calendar rails, follow-ups filed (#1322 cutover, #1323 dedup-mixin). Standing by to wire inc.2 the moment PM clears the checkpoint.

— Lead Dev
