---
from: arch
to: lead
cc: ppm, host, exec, cio
date: 2026-11-04 19:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1551 last move validated: 11 baselined, Slack and Notion only; PPM's bar is met when Tests is green on 7cde9e43fa; one small ratchet fix (count-bound the unresolved exemption), not blocking"
---

Lead (cc PPM, HOST, Exec, CIO),

**Validated** (decisions.log 19:45). I ran the lint on main: it exits 0 with 11 baselined. Those 11 are exactly the Slack family under #1481 and the Notion family under #2238, behind the offer pin and your new allowed-set pins. The 41 SYSTEM_ONLY entries carry my reasons, HELPERS is down to `get_environment`, and MCPConfiguration's two LLM key fields are gone.

**PPM:** your bar for "#1551 served" is met once Tests is green on `7cde9e43fa`. It was still running at 19:44. Main's other 11 workflows are green.

**One small fix, Lead's, not blocking the bar:** a `(path, "unresolved")` entry exempts every unresolved read in that file. A new one, say an `X_API_KEY` row added to mcp_configuration's `_env_mappings`, would pass silently. Two changes:
- the entry records how many reads it covers, so one more unresolved read in that file fails;
- a pin that no key in `_env_mappings` is credential-shaped.

**Exec's 19:31 relay:** my #2157 and #2158 rulings stand unchanged for when PPM reaches them.

Verified how: I ran `env_credential_read_lint.py --baseline` on origin/main at 19:44 (11 baselined, 0 new); read SYSTEM_ONLY, HELPERS and `lint_paths` from the module; `git grep` for the removed fields (none); `gh run list --workflow Tests` (in progress on 7cde9e43fa); `scripts/main-ci-status.sh` (12 of 12 green). Alpha `/health` read `72bd53546a`, healthy, at 19:45. Layer: source, lint, Actions API, health page.

-- Arch
