---
from: pa
to: cxo
cc: lead, arch
date: 2026-10-31 12:53 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2241 guard served: MCP v18 at 12:50:13 PT, sha a8a01b96b4, 0.9.0.0. Served quote is the many-issues form; zero and one forms not reachable from xian's account"
---
CXO (cc Lead, Arch),

On Arch's validation (09:59), I deployed with `scripts/deploy-mcp.sh` from origin/main `a8a01b96b4` (descends from the guard merge `eef219a196`). Fly release **v18**, complete at 19:50:13Z = **12:50:13 PT**.

Served `what_piper_knows_about_me`, one call from xian's connector at about 12:51:

> "245 open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded; showing 42 of them, most recently opened first."

`count` 42, `total` 245, `truncated` true, `capped_at` 50. Rendered inline, no "too large". The total moved from 255 (v16, 09:30) to 245, since issues closed in between; the page still trims to 42 at the budget.

The zero form and the singular form can't show on xian's account (245 open), so as Lead said, those are yours to judge from source and the pins.

Test plan (`docs/internal/operations/mcp-test-plan-pm.md`) is updated to v18 and the new figure, with a note that the total moves.

Verified how: `curl https://mcp.pipermorgan.ai/health` → healthy, version 0.9.0.0, git_sha a8a01b96b4…; `fly releases --json` for v18's time; one served tool call through the hosted connector. Layer: served MCP app, tool output (not a Claude-side render judgment beyond "no size error"). Denominator: 1 call, the many-issues branch of 3.

— PA
