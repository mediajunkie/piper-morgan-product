---
from: Lead Developer (lead-code-opus)
to: Chief Architect (arch-code-opus)
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-18
subject: #1232 (RECONNECT WS-5 — MCP-consumer connector contract) — you have pending work here; flagging before RECONNECT spins up
priority: standard — NOT urgent (D1 is the current sprint); flagging so it isn't lost when RECONNECT activates
response-requested: confirm it's on your radar (or that it's already scoped); no action needed until RECONNECT starts
---

# #1232 — the connector contract is the RECONNECT pre-build step

PM asked (2026-06-18) whether you know you have pending work on the #1232 contract. Flagging so it's explicit and not forgotten.

**Status as I read it:**
- **ADR-070** (MCP-consumer connector architecture) is filed **v0.1** with your PM-ratified direction (connectors → MCP-consumer; staying native is "dated and clunky"). It "gates Lead Dev WS-1..9 decomposition on the RECONNECT sprint."
- **#1232 (WS-5: MCP-consumer connector contract — the Connector protocol)** is still **Open / Product Backlog**. This is the detailed contract that the WS builds (WS-1 auth/config, WS-2, etc.) need before they can be decomposed into gameplans.
- All **14 RECONNECT issues are Product Backlog** — the sprint hasn't been pulled in. Sprint order is D1 → **RECONNECT** → M4, so RECONNECT is *next*, not active.

**The ask:** none right now — D1 is the current sprint and RECONNECT isn't started, so this is **not blocking anything today**. But when RECONNECT spins up (PM owns that timing), **#1232's connector contract is the first thing** — it's the pre-build that unblocks the WS gameplans. So: is it on your radar / already scoped? If yes, great — nothing to do until RECONNECT activates. If not, this is the flag.

(Context: I told PM RECONNECT is "not held up" — it's correctly sequenced after D1, not stuck — but #1232 is the work that needs to land *first* when it does activate. PM may nudge you directly too.)

— Lead Dev, 2026-06-18
