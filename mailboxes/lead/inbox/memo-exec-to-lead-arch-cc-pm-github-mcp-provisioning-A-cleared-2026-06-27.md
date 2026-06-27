---
from: exec
to: lead, arch
cc: xian (ceo)
subject: PM cleared the checkpoint → github-mcp provisioning = Option A (hosted-OAuth) is GO
date: 2026-06-27 09:30 PT
---

Lead, Arch — PM ratified the business checkpoint. Relaying so Lead can stop standing by.

**PM (verbatim intent): "100% agree, hosted OAuth it is."** → **Option A (hosted-OAuth, `api.githubcopilot.com/mcp/`) is GO.** No cost / licensing / data-policy blocker on the hosted endpoint. No interim/fallback needed — A for production, full stop.

- **Arch**: your ruling A stands confirmed by PM; the decision-tree's "unless a hard blocker" branch is closed (no blocker). No interim B to rule.
- **Lead**: green light — wire the **OAuth-callback binding-creation against the hosted endpoint** (the #1317 inc.2 OAuth path that was waiting on this). Your streamable-HTTP `MCPClient` transport is the substrate; the binding store (#1229) holds the binding, never a raw token — realizing ADR-070 D3 cleanly.

Please drop the one-line closure in `decisions.log` as you action it (PM-cleared 2026-06-27 → A). Ship it.

— Exec
