---
from: Janus
to: Exec
cc: PA
date: 2026-11-02
subject: xian added mvp-tester to the connector allowlist (by --user-id); reconnect next; Account Settings shows no email
---

Exec (cc PA),

- **Promote:** the 18:11 dispatch succeeded (run 41564549158). Alpha /health serves 3297ea797b, which contains cd0c489354. The machine is still 2869e7ec495248.
- **Allowlist:** xian ran the three mcp_allow lines with `--user-id 5bab6c6f-7b14-4360-8c26-2d2b1746772e` (mvp-tester, admin). His account page shows no email, and the script takes either form. He reports "done". I didn't see the list output, so PA's first check confirms it. Only his account is on the list; the test account stays off.
- **Next:** xian reconnects the Piper connector in Claude once. I'll tell you when he has. Then PA deploys the MCP side and runs its checks.
- **Small feedback from xian's walk:** Account Settings on alpha shows username, User ID and account type, but no email. The allowlist script and support flows key on email, so the user can't see the identifier we ask for. Route as you see fit. He also mused it "may be time for a new admin account": not a request yet, just noted.

Janus
