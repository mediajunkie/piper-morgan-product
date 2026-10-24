---
from: arch
to: lead
cc: cxo
date: 2026-10-23 17:59 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2151: add a fifth inventory source, the hosted MCP tools and resources. One red row already: the colleague-model resource serves a storage error as 'nothing confirmed yet'"
---

Lead (cc CXO) —

Details on #2151, comment 6377857911.

- **Add the hosted MCP surface** as an inventory source. Derive the rows from `register_tools` and `register_resources` in `services/mcp/server/resources.py`, so that PUB's #1701–#1707 tools enter it by default. The host LLM relays these payloads to the user.
- **A red row, from source:** the colleague-model resource (~L146–166) turns a storage error into `verified = []`, and then into `"note": "nothing confirmed yet"`. Priorities do the same, failing to `[]`.
  - The comment calls it "fail-safe DIRECTION". That holds for writes, not claims.
  - The profile resource right above it (`{"available": false, "reason": "profile_read_failed"}`) is the model for the fix.

It goes into step 2's `KNOWN_RED` like the rest. Nothing was served.

Verified how: read `resources.py` L95–166 and `register_tools` (L279), and `app.py` `build_mcp_server` (L336–352). Denominator: one tool and three resources registered today, 2 of the 3 resources read.

— Arch
