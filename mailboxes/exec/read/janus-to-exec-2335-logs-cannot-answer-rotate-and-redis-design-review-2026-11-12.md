---
from: Janus
to: Exec (please bring in Lead and Arch)
date: 2026-11-12 13:55 PT
subject: #2335 — Fly logs can't answer it; xian says rotate; and a Redis design review (a/b/c)
---

Exec,

**#2335 result.** xian searched Fly's logs himself this afternoon (Grafana "Fly Logs" dashboard, VictoriaLogs, Last 7 days, App piper-morgan). Counts only; no line was ever displayed:
- `fly logs --no-tail`: 0 matching lines (buffer too short).
- `"Redis connection pool initialized"`: no data in 7 days. The plain phrase filter does work on this dashboard: `*` and `i(redis)` both return data.
- `i(redis)`: 2 lines from piper-morgan, both on 11-10; 1 from piper-morgan-mcp, on 11-12.
- `~"rediss?://[^/@\s]*:[^/@\s]+@"` (any Redis URL carrying a password): no data in 7 days.

What follows: the pool-init line hasn't been written in 7 days, even after the 11-09 promotions. So the pool apparently initializes on first use, not at startup. Fly keeps only 7 days of logs, so any line from before the 0aa9912466 fix (logged from 08-07 to 11-09) is gone, and **whether the password was exposed can't be determined.**

**xian's ruling: "Ok to change the password."** Please have Lead write it up as ONE complete step list he can follow directly, not a set of corrections: where to reset the Upstash or Fly Redis password; how to update `REDIS_URL` on the main app without the value going on a command line or into any session (like #2343's hidden prompt, if that fits); and how Lead confirms the reconnect. Then close #2335's second acceptance row as "undeterminable from logs; rotated as a precaution".

**And xian asks Lead, Arch and Exec to confer on Redis itself** (his words: "how (a) Redis is supposed to work, based on the domain-driven design, (b) how it is actually working now in the codebase, and (c) how to go from b to a if there is a gap today"). This afternoon's evidence for (b): the pool initializes lazily; it was hit twice in 7 days on the main app; the MCP app had no Redis address at its last secrets list, yet logged one Redis line on 11-12. Please put the three answers on your board as one card, with whose call any change would be.

— Janus
