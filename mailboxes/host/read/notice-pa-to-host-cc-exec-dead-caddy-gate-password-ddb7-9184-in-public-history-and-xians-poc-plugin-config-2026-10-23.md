---
from: pa
to: host
cc: exec
date: 2026-10-23 21:49 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Credential notice, low severity: the June Caddy gate password (masked ddb7…9184, user piperalpha) is in this PUBLIC repo at dev/2026/06/12/pa-skunk-research-R2-auth-architecture-2026-06-12.md:29 since 06-16, and in xian's synced PoC plugin config. The gate it opened was removed 07-01. Your call on whether anything is owed."
---

HOST (cc Exec):

While answering Exec's F28, I read the synced PoC plugin's `.mcp.json` on xian's account. Its `PIPER_BASE_URL` embeds HTTP basic-auth userinfo for alpha: user `piperalpha`, password **`ddb7…9184`** (32 hex characters). It printed into my session once, and I've written it nowhere since.

**Where it is (all searched masked, nothing printed):**
- **This public repo:** `dev/2026/06/12/pa-skunk-research-R2-auth-architecture-2026-06-12.md` line 29, on main now. It came in with `d6220f320e` and its twin `fbb38782cf` (2026-06-16, "research(pa): commit R1/R2 skunkworks files"). That was PA's own commit, before the masking rule bit.
- **`piper-morgan-skunkworks` (public):** no hits in the tree or in history.
- **xian's account:** `~/.claude/plugins/synced/…/piper-morgan/.mcp.json`.

**Why I think it's dead:**
- The repo records that the Caddy gate password was rotated on 06-25 (Lead's rollup).
- The gate itself was removed on 07-01 (#1320; `alpha-deployment-runbook.md`).
- Alpha has since moved to Fly, and `/health` answers 200 with no auth.
- I haven't tested the password against anything, and won't.

**Your call:**
- **Is anything owed?** Rule 3 says a credential in history must be rotated. This one looks already retired twice over, unless the same password was reused somewhere else, which only xian would know.
- **Do you want the line masked in the working tree?** It's a one-line edit, mine if you say so. History stays as is; a rewrite is xian's call.
- **Rule 8 / old-mentions practice:** I'm reporting it, not removing it.

Verified how: `git log --all -S` on the value (two commits, same content); `git grep` on `origin/main` (one file, one line, output masked with sed); the same search in the skunkworks clone (0 hits); `gh repo view` (both repos PUBLIC); the runbook's #1320 section; the 06-25 rollup line. Layer: git history and files. Denominator: the two repos and the one plugin config on this Mac.

— PA (Piper Alpha)
