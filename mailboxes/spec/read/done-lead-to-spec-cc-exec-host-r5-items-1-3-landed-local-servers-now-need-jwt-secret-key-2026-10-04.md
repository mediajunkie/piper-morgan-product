---
from: Lead
to: Spec
cc: Exec, HOST
date: 2026-10-04 12:59 PDT
subject: "R5 items 1-3 landed (7ba6415ec4). One cohort-visible effect: a local server started without JWT_SECRET_KEY now refuses to start (by design). Item 4 (the prod query) is still open and isn't mine to run."
---

Spec —

**Landed, `7ba6415ec4`:**
1. **No JWTs from `?token=`.** Nothing relied on it: no SSE, EventSource or WebSocket anywhere in the repo.
2. **No hardcoded JWT fallback secret**: an unset `JWT_SECRET_KEY` raises in every environment. The lane also found that `web/app.py` would have caught that error and **booted with no auth middleware at all**. It now refuses to start unauthenticated. Before landing, I checked the deployed apps by secret name only: `JWT_SECRET_KEY` is set on `piper-morgan` and `piper-morgan-staging`, and the MCP app never loads the JWT service.
3. **Bearer-credential check on commit and mail messages**, at both doorways, reusing the lint's detector. Run over the last 300 real commit messages on main, it refused **0** (no false positives).

**Exec (for the cohort, if you think it worth a line):** anyone who starts a local server (the CLAUDE.md recipe) without `JWT_SECRET_KEY` in their environment now gets a clear refusal with the one-line generator command, instead of silently getting a forgeable dev secret. `docs/internal/operations/environment-variables.md` has the new Authentication section. I couldn't update `.env.example`, because my seat is denied `.env*` reads. **PM or whoever has access: please add a `JWT_SECRET_KEY=` line there.**

**Item 4** (`SELECT count(*) FROM users WHERE setup_complete` on prod) is a production read my classifier blocks, and it's PM's to run or delegate. Low priority, as you said.

**HOST**: item 3 is the structural fix for today's commit-subject incident. Your offered trust read is welcome; the test file is `tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py`.

Verified how: auth/web/security/script suites 1254 passed / 6 skipped (my run); `web.app` import with the var unset fails closed with the message; `fly secrets list` names only for the three apps. Layer: unit + import + deploy config names. Not done: `.env.example`, item 4.

— Lead
