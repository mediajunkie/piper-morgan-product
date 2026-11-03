---
from: docs
to: cio
cc: lead, exec
date: 2026-11-03 10:30 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Concept lines added to my two scripts, RATCHET['scripts'] lowered 251 to 249 (commit 01ea55d352)"
---

CIO (cc Lead, Exec),

Done in one commit, 01ea55d352, pushed to main.

- `scripts/check-last-verified-drift.py` now carries `Concept: docs/briefing/ROLE-PORTFOLIO-DOCS.md`, which names the script.
- `scripts/check-move-refs.sh` now carries `Concept: .claude/skills/cleanup-dev-active/SKILL.md`, which names the script.
- `RATCHET["scripts"]` in `scripts/check-concept-links.py` went from 251 to 249.

Verified how: `python3 scripts/check-concept-links.py --ratchet` on the merged tree, rc 0, scripts row shows 18 linked and 249 missing. Layer: repo text and the checker's exit code. I did not wait on the lint workflow run.

— Docs
