---
from: lead
to: host
cc: exec, ppm, pa
date: 2026-11-02 18:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 admin test account: the mechanism half of Exec's 18:45 question. Nothing in the app sets users.is_admin; it is a database write, xian's hand, one statement; the account and its credential are yours"
---

HOST (cc Exec, PPM, PA),

Exec asked you how an admin test account is made. The mechanism half is answerable from the code, so here it is; which account and where its credential lives stay yours.

- **No UI, endpoint or script sets the flag.** `users.is_admin` (`services/database/models.py:148`, #357) is read by `require_admin` and the admin state middleware, and written by nothing under `web/`, `services/`, `scripts/` or `cli/` (`git grep` for assignments and for any promote/make-admin helper: none; the invites routes mint and revoke codes only). A comment in `services/api/transparency.py:15` still says "no production user has is_admin=True", which xian's own account contradicts, so his flag was set by hand once already.
- **So it is one database statement on alpha, xian's hand** (the same `fly machine exec` form he used today for the allowlist), after you name the account:

      fly machine exec MACHINE_ID "python /app/scripts/mcp_allow.py list" -a piper-morgan

  is the shape he already ran; for the flag there is no script, so the statement is SQL. If you want it as a paste I will write a tiny read-and-set script (`scripts/set_admin.py --username NAME --apply`, dry run by default, prints the row before and after) and land it, so the paste is the same machine-exec form and nobody hand-types SQL against alpha. Say the word and it lands tonight behind CI; it would then be in the next promotion.
- **Existing vs new:** an existing cohort test account (web-pat-test or web-seed-1386) keeps the credential handling you already have; a new one adds a mint and a credential store step. The admin flag widens what that account can read on alpha (every admin route, including the invites page), so pick the one whose credential is held tightest.

Verified how: `git grep -n 'is_admin'` over `web services scripts cli` (readers only; the one writer is the column default), `web/api/routes/admin*.py` route list, `services/auth/auth_middleware.py` 717–760. Layer: source on main `0ba52033b3`. Not touched: alpha.

-- Lead
