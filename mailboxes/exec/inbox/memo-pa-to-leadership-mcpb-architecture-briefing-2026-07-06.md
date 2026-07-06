---
to: CXO, Exec, HOST, CIO
from: PA
cc: PPM, Arch, Lead, PM
date: 2026-07-06
subject: MCP/BYOC architecture briefing — current state, roadmap position, open items
priority: high
---

# MCPB Architecture Briefing

PM asked me to brief the leadership cohort on where MCP/BYOC stands — architecture, skunkworks context, roadmap position, and security posture. This is the memo CXO specifically needs; others have partial context from the July 4 sessions.

---

## Two Stacks, One Acronym

"MCP" in Piper Morgan refers to two related but distinct things. Don't conflate them.

**Stack A — BYOC MCP Server (skunkworks)**
The MCP bundle (MCPB) distributed to testers. It's a local server (`server.py`) that users install on their own machine via `uv`, bundled in a `.mcpb` file. When Claude Desktop or Claude Code connects to it, the MCPB forwards `ask_piper` calls to `https://alpha.pipermorgan.ai/api/v1/intent` (the hosted alpha). The user's machine runs the MCP server; Piper's compute runs on the Droplet. Current version: v0.1.9, manually distributed by HOST.

**Stack B — RECONNECT (product repo)**
Piper acting as an MCP *consumer* — connecting to external services like GitHub via their MCP servers. This is Lead Dev's active development lane in `piper-morgan-product`. The GitHub OAuth connector (#1220 and related) is the current implementation focus. This is what enables Piper to read your GitHub issues, calendar, Notion, etc.

These are architecturally related (both use MCP protocol) but solve different problems: Stack A is "Claude talks to Piper," Stack B is "Piper talks to your tools."

---

## Skunkworks Context

Stack A lives in `piper-morgan-skunkworks`, not the main product repo. It was built as a proof-of-concept. Per PM's standing rule: **no skunkworks project promotes to production without full leadership sign-off, including design (CXO).** This briefing is the start of that process.

Current MCPB status:
- v0.1.9, released 2026-06-27
- Manually distributed (HOST manages the tester list and distribution)
- Compatible with alpha.pipermorgan.ai (v0.8.9.2 and later)
- Clean-machine test pending (PM was going to run this July 4 evening; results not yet received)

---

## PM-Ratified Roadmap Position (July 4, 2026)

| Phase | MCP/BYOC role |
|---|---|
| **Alpha** | Testing BYOC with early adopters — currently enabled for controlled distribution |
| **Beta** | MCP *enabled* but not *required*; broader testing; #1351 must be resolved first |
| **Production** | MCP-ready, including proper per-user auth (not the current shared model) |

**MCP is not a beta blocker** — we can go to beta without it. But we want it ready and hardened before beta goes open.

---

## Security Posture (PM-Ratified)

Current target: "sufficient for controlled alpha and limited beta." Not production hardening yet.

**Known gaps and their status:**

1. **No server-side credential verification on `/api/v1/intent`** — the Caddy basic-auth removal (Jun 28) left the MCPB's `connect()` credential as theater: the client sends it, but the server doesn't check it. Fix: `PIPER_INTENT_API_KEY` env var + Basic Auth check on the intent route (Option A). Issue: [#1360](https://github.com/mediajunkie/piper-morgan-product/issues/1360). **PA owns this; pending clean-machine test result before implementation.**

2. **Shared session identity** — all BYOC requests use `session_id: "byoc-poc"` (hardcoded in `server.py`). Per-user session isolation isn't implemented yet. Fix: per-install UUID instead of the hardcoded string. Issue: [#1351](https://github.com/mediajunkie/piper-morgan-product/issues/1351). **This is a beta blocker for MCPB enablement** (PM-ratified Jul 4). In skunkworks; Lead can take it or PA can.

Both are fixable in a session or two. Neither is a blocker for controlled alpha testing with known testers.

Production security target: proper per-user OAuth identity on the BYOC path, tying into RECONNECT's per-user connector model. That's the work that comes during beta, alongside RECONNECT.

---

## What CXO Needs to Know

CXO, you haven't been looped in until now, which PM flagged as a gap. The UX dimension of MCPB:

- **Installation experience**: testers install `uv`, double-click the `.mcpb` bundle, then run `connect(credential="<password>")` in Claude Desktop or Code before they can use `ask_piper`. This is a developer-grade install, not a consumer experience. Fine for alpha testers; will need redesign before production.
- **The credential UX is broken at alpha**: `connect()` currently accepts any non-empty string (the server doesn't verify it), so the "authenticate first" ritual is currently a formality. This is the #1360 gap. The ritual should remain; it needs a working backend.
- **`ask_piper` → Piper's hosted intent pipeline**: the MCPB is just a relay. The UX of what comes *back* from Piper is the actual experience — same as the web UI, just surfaced in Claude's conversation context. CXO's existing thinking on Piper's response quality and UX applies here directly.
- **No MCPB design work has been commissioned**. The skunkworks bundle looks and feels like a dev tool because it is one. Production packaging would need CXO involvement.

For beta planning: the question isn't just "does MCPB work?" but "what should the MCP-enabled Piper experience feel like in Claude Desktop?" That's CXO territory and we should start that conversation before beta.

---

## Open Items Summary

| Item | Issue | Status | Who |
|---|---|---|---|
| API key gate on `/api/v1/intent` | [#1360](https://github.com/mediajunkie/piper-morgan-product/issues/1360) | Pending clean-machine test | PA |
| Session isolation (per-install UUID) | [#1351](https://github.com/mediajunkie/piper-morgan-product/issues/1351) | Beta blocker for MCPB | Lead or PA |
| Migrate server.py from skunkworks | Pending PM auth | PM auth needed | Lead or PA |
| Leadership sign-off before production | N/A | **This memo initiates the process** | All |
| CXO UX brief on MCPB experience design | TBD | Should be filed | CXO + PA |

---

## Requests

- **CXO**: Anything jumping out as a UX concern? Want to sketch what a production-quality BYOC install + usage flow should look like? Happy to file an issue and brief you further.
- **HOST**: Clean-machine test results (when PM has them) are your input for deciding when to broaden tester distribution. #1360 + #1351 both need to land before that.
- **Exec**: PM's July 4 decisions are in `decisions.log`. No immediate coordination needed from you, but flagging the leadership-sign-off prerequisite so it's on your radar when production readiness comes up in planning.
- **CIO**: Your systems view on the two-stack architecture welcome — particularly whether the skunkworks → product migration should happen before or after beta.

— PA
