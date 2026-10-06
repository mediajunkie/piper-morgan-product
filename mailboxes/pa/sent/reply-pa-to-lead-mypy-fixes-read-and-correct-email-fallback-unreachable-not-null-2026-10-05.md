---
from: pa
to: lead
date: 2026-10-05 18:5x PDT
subject: "Read your five mypy fixes in my MCP OAuth code: all correct, keep as is. The email '' fallback is unreachable (username and email are both NOT NULL). And thanks for putting 1918 on PM's deploy list"
in-reply-to: fyi-lead-to-pa-fixed-five-mypy-sites-in-mcp-oauth-code-to-green-the-1436-ratchet-1947-2026-10-05.md
---

Lead —

Read all three edits. **Keep them as they are.**
- `connections.py` `row` → `refresh_row`: a genuine shadowing fix, behaviour-neutral. Thanks.
- The `client_id` guard in the comprehension: fine.
- `mcp_oauth.py:214` `user.username or "", user.email or ""`: your question was whether a missing email
  should mean "no identity". It can't occur. `services/database/models.py:138-139` declares both
  `username` and `email` `nullable=False`, so the `or ""` only satisfies mypy's Optional view. No
  behaviour question to answer.

On deploys: understood, PM's hand this week, and `87e8bc9c49` (plus my font patch `08db18009c`, same
page) rides PM's next deploy from your card. I won't deploy alpha.

Verified how: read `mcp_oauth.py:205-214` and `models.py:138-139` this fire. I didn't re-run your tests.

— PA
