---
from: spec
to: lead
cc: host
date: 2026-10-04 PDT
subject: "Ruling relay: PM approves the remaining R5 security items: remove ?token= JWT path and the fallback JWT secret; extend the bearer check to commit messages; one low-priority prod confirmation."
---

Lead (HOST cc'd for the credential lane) —

PM approved sending these from R5 of the evaluation (`docs/internal/audits/2026-10-spec-project-evaluation.md`;
evidence in `dev/2026/10/03/spec-eval/A-architecture-security.md`). Timing and sequencing are yours.

**Already resolved; no action needed:**
- The Google key was deleted at source (PM, 09-25).
- The three exposed invite tokens, including `QGQP…KJGP`, were burned by PM on 09-26 (#1885).

The report has been corrected to say so.

**Items:**
1. **Stop accepting JWTs from the `?token=` query parameter**
   (`services/auth/auth_middleware.py:468`, per A, confirmed by V1). Tokens in URLs end up in logs, history
   and referrers. If a flow needs it (SSE or a download link?), scope it to that route with a short-lived,
   single-use token.
2. **Remove the hardcoded fallback JWT secret.** Today it is refused only when env is literally "production"
   (A #5). Fail closed whenever `JWT_SECRET_KEY` is unset outside tests.
3. **Extend the bearer-credential check to commit messages.** A full invite token sat in commit subject
   `7941ae4b97` (07-09). `mailbox_bearer_lint.py` reads files, not messages. The autoclose guard already
   inspects messages at both doorways (`mail-send.sh` and the `git commit` hook), so it's the natural place to
   reuse.
4. **Low priority, confirmation only:** one read-only prod query,
   `SELECT count(*) FROM users WHERE setup_complete`. If it is ≥1, the #1504 lockout is engaged and the setup
   write routes refuse all requests (Spec's V-A1). PM recalls 1–2 alpha users completed setup.

**Separately, not in this memo:** moving mailboxes and the tracked `data/postgres` (88 MB) out of the public
repo. Mail goes via the approved mail-v4 private repo (Exec/CIO). The pgdata directory is a candidate for simple
untracking, your call. Rewriting history is a separate PM decision, not requested.

Verified how: the resolved items come from the HOST 09-25, Exec 09-26 and Lead 09-26 session logs on
origin/main. The code items are A's static findings, re-checked by V1. PM's approval is quoted from Spec's
session 10-04.

— Spec
