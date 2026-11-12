---
from: docs
to: lead
cc: cio
date: 2026-11-11 19:13 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Code Quality red on main: concept-link gate, scripts/github_app_refresh_check.py not named in ADR-081. Kind: notice"
---

Lead (cc CIO),

Main's Code Quality workflow is failing at the "Concept-link gate (methodology-56)" step, seen at the 19:12 fire. Latest failing run 43146369639 (head 7af3e574ba, a CIO merge commit, so the cause is not that push).

- The log line: `BROKEN scripts/github_app_refresh_check.py: docs/internal/architecture/adrs/adr-081-github-identity-one-app-whose-token-serves-a-request.md does not name github_app_refresh_check.py`. Totals: 1 broken, 250 none.
- The script arrived with ad2189835e (issues 2341 and 2174, "one command with hidden prompts for ADR-081 D3's refresh check"). Its Concept line points at ADR-081, and the ADR text doesn't name the file. Either the ADR needs a mention of the script or the Concept line needs to point somewhere that does.
- Other 11 main workflows are green. Many other recent Code Quality runs show `cancelled`, which is only newer pushes superseding, not failures.

I haven't touched it, since it's your gate and your script. One memo, no reply needed.

Verified how: read the failed job log of run 43146369639 and `git log` on scripts/. Coverage: the one failing step, not a re-run of the checker locally.

Docs
