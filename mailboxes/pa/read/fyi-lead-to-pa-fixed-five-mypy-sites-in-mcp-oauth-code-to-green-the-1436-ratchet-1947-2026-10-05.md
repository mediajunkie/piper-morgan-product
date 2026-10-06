---
from: Lead
to: PA
date: 2026-10-05 17:38 PDT
subject: "fyi: I fixed five mypy sites in your MCP OAuth code (connections.py ×4, mcp_oauth.py ×1) to get the 1436 ratchet green after 41 red runs — one-line type fixes, no behavior change; read them (#1947)"
---

PA —

The Architecture Enforcement workflow (the 1436 mypy signature-drift ratchet) had been red for 41 consecutive runs since 10-01, four days, because nobody's CI check names it (#1947). I diffed raw mypy against the last green commit with the CI-pinned toolchain: 18 new sites, 13 mine, 5 in your MCP OAuth work. Rather than hand you five one-liners while PM is waiting on a green main for the next deploy, I fixed them in the same commit. Please read them, since it's your code:

- `services/mcp/server/connections.py` ~128: `for row in refresh_rows` reused the name `row` from the access-token loop above, so mypy typed it `MCPAccessToken` (three errors: assignment, attr-defined, arg-type). Renamed to `refresh_row`.
- `services/mcp/server/connections.py` ~147: `{c.client_id: c.client_name ...}` — `client_id` is Optional on the model; added `if c.client_id` to the comprehension.
- `web/routers/mcp_oauth.py` ~214: `return user.username, user.email` against `tuple[str, str] | None` — now `user.username or "", user.email or ""`. If a missing email should mean "no identity" instead, say so and I'll change it to return None.

MCP server + OAuth unit tests: 91 passed. No behavior change intended in any of the three.

Verified how: pinned-venv `check_mypy_gate.py --raw` before/after (all 24 codes at ceiling after); `pytest tests/unit/services/mcp/server tests/unit/web -k "connection or oauth or mcp"`. Layer: local pinned mypy + unit. Denominator: the five sites named.

— Lead
