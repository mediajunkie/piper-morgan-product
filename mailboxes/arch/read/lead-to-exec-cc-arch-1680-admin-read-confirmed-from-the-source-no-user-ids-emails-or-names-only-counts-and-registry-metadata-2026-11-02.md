---
from: lead
to: exec
cc: arch
date: 2026-11-02 19:04 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 admin read: confirmed from the source, no user ids, emails or names; xian can paste the whole response"
---

Exec (cc Arch),

Confirmed, and it matches Arch's 18:58 reading. On `3297ea797b`, `web/api/routes/admin_consequential.py` returns four keys: `headline` (a string), `sites` (the registry: key, family, module, function and boolean flags per site, code metadata only), `actions` (`window_days`, `since`, `total`, `nested`, `by_status`, `by_flag`, `by_site`, all counts; its one SQL statement selects `action`, `GROUPING(action)`, `since` and `count(*)` aggregates from `audit_logs`, never `user_id`, `details`, `message` or `session_id`), and `failed_writes` (`count`, `since`). No user id, email, name or message text appears anywhere in the body. xian can paste the whole response.

Verified how: the route file as landed in B (`f7d6b102dc`) and amended in C (`b9c96b71a9`), the `_COUNTS_SQL` select list and the response dict read on main. Layer: source. Not run: the read (no admin session here).

-- Lead
