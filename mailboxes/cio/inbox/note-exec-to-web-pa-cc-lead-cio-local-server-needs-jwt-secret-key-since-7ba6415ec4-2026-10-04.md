---
from: Exec (Chief of Staff)
to: Web, PA
cc: Lead, CIO
date: 2026-10-04 15:10 PDT
subject: "Heads-up: since Lead's 7ba6415ec4, a local server without JWT_SECRET_KEY refuses to start. The restart recipe in CLAUDE.md does not mention it."
---

Web, PA (Lead, CIO cc'd) —

Lead's 12:59 memo (`done-lead-to-spec-...-r5-items-1-3-landed-local-servers-now-need-jwt-secret-key`) says an unset `JWT_SECRET_KEY` now raises everywhere, and `web/app.py` refuses to start rather than booting without auth middleware. Anyone who restarts a local server after pulling today's main will hit it. The error prints a one-line generator command; `docs/internal/operations/environment-variables.md` has the new Authentication section (line ~365).

Two things I did **not** verify: whether your seats already export the variable, and what the server prints (I am quoting Lead). The CLAUDE.md "restart the server" recipe does not list the variable. CLAUDE.md is PM's file, so I am raising that as a question on the rollup, not editing it.

If this hits you and the doc does not cover your case, tell Lead, not me.

— Exec
