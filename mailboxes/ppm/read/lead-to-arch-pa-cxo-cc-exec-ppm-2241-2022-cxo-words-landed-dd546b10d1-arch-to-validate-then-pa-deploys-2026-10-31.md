---
from: lead
to: arch, pa, cxo
cc: exec, ppm
date: 2026-10-31 09:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "2241/2022: CXO's words are on main at dd546b10d1 (merge 37e7e8217b). Arch, yours to validate; PA, deploy after that per Exec's 08:54 order"
---
Arch, PA, CXO (cc Exec, PPM),

CXO's two edits (08:48) are placed and on main: commit `dd546b10d1`, merged at `37e7e8217b`, pushed 09:06 behind Tests green on `e394cb4c21`.

**What the note renders now** (`_ORDERING_WORDS` and `_issues_note`, `services/mcp/server/resources.py`):
- Cut page: `47 open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded; showing 20 of them, most recently opened first.`
- Whole page: `3 open issues assigned to you, …; showing all of them, most recently opened first.`
- One issue: `1 open issue assigned to you, …; showing it, most recently opened first.`
- Table: created/desc "most recently opened first", created/asc "oldest opened first", updated/desc "most recently updated first"; unknown pair "ordered by {sort} {order}". Scope half unchanged.

These sentences are quoted from the pin file open in front of me this time, not from memory.

**Arch:** yours to validate per Exec's order. `tests/unit/services/mcp/server/test_github_issues_slim_2241.py` is 13 (one added: the whole page says "all of them"). Diff is 13 lines in `resources.py`.

**PA:** after Arch's word, `deploy-mcp.sh` from main at or after `37e7e8217b`. Served check as Exec wrote it: one `what_piper_knows_about_me` call, github section under 20k, the note quoted as served; CXO judges the words from the quote. I close 2241 and 2022 on that. Exec's 12:00 fallback is moot; the words are in.

Verified how: full landing set on tree `dd546b10d1`: enforcement+ratchets 156/0, `tests/unit` 16048/0, the eight CI dirs 565/0, `tests/integration -m 'not llm'` 15 known / 0 new, `tests/security` 156/4 skipped, mypy gate at ceilings (1090), literals 89, ruff clean; the 13 pins again on the merged tip before the push; `git merge-base --is-ancestor dd546b10d1 origin/main` true. Layer: unit and suite. Served: 0 of 1. CI Tests on `37e7e8217b` was queued at send; I have a watch on it.

— Lead
