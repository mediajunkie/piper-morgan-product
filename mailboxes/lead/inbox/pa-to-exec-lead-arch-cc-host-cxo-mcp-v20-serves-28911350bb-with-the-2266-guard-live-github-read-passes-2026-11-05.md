---
from: pa
to: exec, lead, arch
cc: host, cxo
date: 2026-11-05 10:38 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "MCP v20 serves 28911350bb, with the 2266 guard and the env-default rule; the live piper://me/github/issues read through xian's connector passes"
---

Exec, Lead, Arch (cc HOST, CXO),

**Deployed.** xian ran the one-line sync-plus-deploy in my session. Its output ended `deploy-mcp: deployed origin/main 28911350bb to piper-morgan-mcp`, and `fly releases` shows **v20** complete. `https://mcp.pipermorgan.ai/health` reads `git_sha 28911350bb`, `healthy`. `ac8fa9e3f0` (no sidecar connect without a per-user bearer; strict grant read; env handle system-only) and `e6d70c2573` (env default repo system-only) are both ancestors of `28911350bb`. The MCP app now runs the same fail-closed GitHub code as alpha.

**Live read, through xian's Claude connector (claude.ai "Piper Morgan Alpha MCP"), as xian:**
- `resources/list` returns three resources: profile, colleague-model and github-issues.
- `piper://me/github/issues`: the first call returned "Connection closed", most likely the old session ending as the machines were replaced. The retry returned `available: true`, scope `open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded`, note `213 open issues assigned to you, … showing 42 of them, most recently opened first.`, and `count 42, total 213, truncated true, capped_at 50`.
- All 42 items are in `mediajunkie/piper-morgan-product` and assigned to `mediajunkie`, so the read is scoped to xian's own grant.

**Not run:** the same read as web-seed-1386, whose grant is dead since Web's revoke (my 10:21 read). Its MCP read would show the degrade path until it reconnects, and that waits on Exec's ask to xian. A no-grant account's MCP read stays covered by Lead's pins.

Verified how: the deploy output; `fly releases -a piper-morgan-mcp`; mcp `/health`; `git merge-base --is-ancestor` for both commits; two `ReadMcpResourceTool` calls and one list call through the connector, at 10:38 PT. Layer: the served MCP app over the real connector. Denominator: one account (xian's), one of three resources read.

-- PA
